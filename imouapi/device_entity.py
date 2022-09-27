"""Classes for representing entities beloging to an Imou device."""
import logging
from abc import ABC, abstractmethod
from datetime import datetime

from imouapi.api import ImouAPIClient
from imouapi.const import BINARY_SENSOR_ICONS, BINARY_SENSORS, IMOU_SWITCHES, SENSOR_ICONS, SENSORS, SWITCH_ICONS
from imouapi.exceptions import InvalidResponse

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ImouEntity(ABC):
    """A representation of a sensor within an Imou Device."""

    @abstractmethod
    async def async_update(self, **kwargs):
        """Update the entity."""

    @abstractmethod
    def get_device_id(self) -> str:
        """Get device id."""

    @abstractmethod
    def get_name(self) -> str:
        """Get name."""

    @abstractmethod
    def get_description(self) -> str:
        """Get description."""

    @abstractmethod
    def get_icon(self) -> str:
        """Get icon."""

    @abstractmethod
    def set_enabled(self, value: bool) -> None:
        """Set enable."""


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
            sensor_type: the sensor type from const SENSORS
        """
        self.api_client = api_client
        self._device_id = device_id
        self._device_name = device_name
        self._name = sensor_type
        self._icon = SENSOR_ICONS[sensor_type]
        self._description = SENSORS[sensor_type]
        self._enabled = True
        # keep track of the status of the sensor
        self._state = ""

    def get_device_id(self) -> str:
        """Get device id."""
        return self._device_id

    def get_name(self) -> str:
        """Get name."""
        return self._name

    def get_icon(self) -> str:
        """Get icon."""
        return self._icon

    def get_description(self) -> str:
        """Get description."""
        return self._description

    def set_enabled(self, value: bool) -> None:
        """Set enable."""
        self._enabled = value

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
                iso_time = datetime.fromtimestamp(alarm["time"]).isoformat()
                self._state = iso_time
                _LOGGER.debug(
                    "[%s] updating %s, value is %s",
                    self._device_name,
                    self._description,
                    self._state,
                )

    # entity-specific methods

    def get_state(self) -> str:
        """Return the state."""
        return self._state

    def get_device_class(self) -> str:
        """Return de device class of the sensor."""
        if self._name == "lastAlarm":
            return "timestamp"
        return ""


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
            sensor_type: the sensor type from const BINARY_SENSORS
        """
        self.api_client = api_client
        self._device_id = device_id
        self._device_name = device_name
        self._name = sensor_type
        self._icon = BINARY_SENSOR_ICONS[sensor_type]
        self._description = BINARY_SENSORS[sensor_type]
        self._enabled = True
        # keep track of the status of the sensor
        self._state = False

    def get_device_id(self) -> str:
        """Get device id."""
        return self._device_id

    def get_name(self) -> str:
        """Get name."""
        return self._name

    def get_icon(self) -> str:
        """Get icon."""
        return self._icon

    def get_description(self) -> str:
        """Get description."""
        return self._description

    def set_enabled(self, value: bool) -> None:
        """Set enable."""
        self._enabled = value

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

    # entity-specific methods

    def is_on(self) -> bool:
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
            device_name: the name of the device
            sensor_type: the sensor type (from the SWITCHES constant)
        """
        self.api_client = api_client
        self._device_id = device_id
        self._device_name = device_name
        self._name = sensor_type
        self._icon = SWITCH_ICONS[sensor_type]
        self._description = IMOU_SWITCHES[sensor_type]
        self._enabled = True
        # keep track of the status of the sensor
        self._state = False

    def get_device_id(self) -> str:
        """Get device id."""
        return self._device_id

    def get_name(self) -> str:
        """Get name."""
        return self._name

    def get_description(self) -> str:
        """Get description."""
        return self._description

    def get_icon(self) -> str:
        """Get icon."""
        return self._icon

    def set_enabled(self, value: bool) -> None:
        """Set enable."""
        self._enabled = value

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

    # entity-specific methods

    def is_on(self) -> bool:
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
        if not self._enabled:
            return
        if self._state:
            await self.async_turn_off()
        else:
            await self.async_turn_on()
