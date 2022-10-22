"""Classes for representing entities beloging to an Imou device."""
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from .api import ImouAPIClient
from .const import BINARY_SENSORS, IMOU_SWITCHES, SENSORS
from .exceptions import InvalidResponse

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ImouEntity(ABC):
    """A representation of a sensor within an Imou Device."""

    def __init__(
        self,
        api_client: ImouAPIClient,
        device_id: str,
        device_name: str,
        sensor_type: str,
        sensor_description: str,
    ) -> None:
        """Initialize common parameters."""
        self.api_client = api_client
        self._device_id = device_id
        self._device_name = device_name
        self._name = sensor_type
        self._description = sensor_description
        self._enabled = True
        self._updated = False

    def get_device_id(self) -> str:
        """Get device id."""
        return self._device_id

    def get_name(self) -> str:
        """Get name."""
        return self._name

    def get_description(self) -> str:
        """Get description."""
        return self._description

    def set_enabled(self, value: bool) -> None:
        """Set enable."""
        self._enabled = value

    def is_enabled(self) -> bool:
        """If enabled."""
        return self._enabled

    def is_updated(self) -> bool:
        """If has been updated at least once."""
        return self._updated

    @abstractmethod
    async def async_update(self, **kwargs):
        """Update the entity."""


class ImouSensor(ImouEntity):
    """A representation of a sensor within an IMOU Device."""

    def __init__(
        self,
        api_client: ImouAPIClient,
        device_id: str,
        device_name: str,
        sensor_type: str,
    ) -> None:
        """
        Initialize the instance.

        Parameters:
            api_client: an instance ofthe API client
            device_id: the device id
            device_name: the device name
            sensor_type: the sensor type from const SENSORS
        """
        super().__init__(api_client, device_id, device_name, sensor_type, SENSORS[sensor_type])
        # keep track of the status of the sensor
        self._state = None

    async def async_update(self, **kwargs):
        """Update the entity."""
        if not self._enabled:
            return
        if self._name == "lastAlarm":
            # get the time of the last alarm
            data = await self.api_client.async_api_getAlarmMessage(self._device_id)
            if "alarms" not in data:
                raise InvalidResponse(f"alarms not found in {data}")
            if len(data["alarms"]) > 0:
                alarm = data["alarms"][0]
                if "time" not in alarm:
                    raise InvalidResponse(f"time not found in {alarm}")
                # convert it into ISO 8601 and store it
                iso_time = datetime.utcfromtimestamp(alarm["time"]).isoformat()
                self._state = iso_time

        elif self._name == "storageUsed":
            # get the storage status
            data = await self.api_client.async_api_deviceStorage(self._device_id)
            if "totalBytes" not in data or "usedBytes" not in data:
                raise InvalidResponse(f"totalBytes or usedBytes not found in {data}")
            percentage_used = int(data["usedBytes"] * 100 / data["totalBytes"])
            self._state = percentage_used

        _LOGGER.debug(
            "[%s] updating %s, value is %s",
            self._device_name,
            self._description,
            self._state,
        )
        if not self._updated:
            self._updated = True

    def get_state(self) -> Optional[str]:
        """Return the state."""
        return self._state


class ImouBinarySensor(ImouEntity):
    """A representation of a sensor within an IMOU Device."""

    def __init__(
        self,
        api_client: ImouAPIClient,
        device_id: str,
        device_name: str,
        sensor_type: str,
    ) -> None:
        """
        Initialize the instance.

        Parameters:
            api_client: an instance ofthe API client
            device_id: the device id
            device_name: the device name
            sensor_type: the sensor type from const BINARY_SENSORS
        """
        super().__init__(api_client, device_id, device_name, sensor_type, BINARY_SENSORS[sensor_type])
        # keep track of the status of the sensor
        self._state = None

    async def async_update(self, **kwargs):
        """Update the entity."""
        if not self._enabled:
            return
        if self._name == "online":
            # get the online status
            data = await self.api_client.async_api_deviceOnline(self._device_id)
            if "onLine" not in data:
                raise InvalidResponse(f"onLine not found in {data}")
            self._state = data["onLine"] == "1"
            _LOGGER.debug(
                "[%s] updating %s, value is %s",
                self._device_name,
                self._description,
                self._state,
            )
            if not self._updated:
                self._updated = True

    def is_on(self) -> Optional[bool]:
        """Return the status of the switch."""
        return self._state


class ImouSwitch(ImouEntity):
    """A representation of a switch within an IMOU Device."""

    def __init__(
        self,
        api_client: ImouAPIClient,
        device_id: str,
        device_name: str,
        sensor_type: str,
    ) -> None:
        """
        Initialize the instance.

        Parameters:
            api_client: an instance ofthe API client
            device_id: the device id
            device_name: the device name
            sensor_type: the sensor type (from the SWITCHES constant)
        """
        super().__init__(api_client, device_id, device_name, sensor_type, IMOU_SWITCHES[sensor_type])
        self._state = None

    async def async_update(self, **kwargs):
        """Update the entity."""
        if not self._enabled:
            return
        data = await self.api_client.async_api_getDeviceCameraStatus(self._device_id, self._name)
        _LOGGER.debug(
            "[%s] updating %s, value is %s",
            self._device_name,
            self._description,
            data["status"].upper(),
        )
        self._state = data["status"] == "on"
        if not self._updated:
            self._updated = True

    def is_on(self) -> Optional[bool]:
        """Return the status of the switch."""
        return self._state

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        if not self._enabled:
            return
        _LOGGER.debug("[%s] %s requsted to turn ON", self._device_name, self._description)
        await self.api_client.async_api_setDeviceCameraStatus(self._device_id, self._name, True)
        self._state = True

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        if not self._enabled:
            return
        _LOGGER.debug("[%s] %s requsted to turn OFF", self._device_name, self._description)
        await self.api_client.async_api_setDeviceCameraStatus(self._device_id, self._name, False)
        self._state = False

    async def async_toggle(self, **kwargs):
        """Toggle the entity."""
        if not self._enabled or not self._updated:
            return
        if self._state:
            await self.async_turn_off()
        else:
            await self.async_turn_on()
