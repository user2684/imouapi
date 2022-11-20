"""Classes for representing entities beloging to an Imou device."""
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Union

from .api import ImouAPIClient
from .const import BINARY_SENSORS, BUTTONS, IMOU_SWITCHES, SELECT, SENSORS, SIRENS
from .exceptions import APIError, InvalidResponse

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
        self._device_instance = None
        self._attributes: dict[str, str] = {}

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

    def set_device(self, device_instance) -> None:
        """Set the device instance this entity is belonging to."""
        self._device_instance = device_instance

    def get_attributes(self) -> dict:
        """Entity attributes."""
        return self._attributes

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

        # storageUsed sensor
        elif self._name == "storageUsed":
            # get SD card status
            data = await self.api_client.async_api_deviceSdcardStatus(self._device_id)
            if "status" not in data:
                raise InvalidResponse(f"status not found in {data}")
            if data["status"] == "normal":
                # get the storage status
                data = await self.api_client.async_api_deviceStorage(self._device_id)
                if "totalBytes" not in data or "usedBytes" not in data:
                    raise InvalidResponse(f"totalBytes or usedBytes not found in {data}")
                percentage_used = int(data["usedBytes"] * 100 / data["totalBytes"])
                self._state = percentage_used

        # callbackUrl sensor
        elif self._name == "callbackUrl":
            # get callback url
            data = await self.api_client.async_api_getMessageCallback()
            if "callbackUrl" not in data:
                raise InvalidResponse(f"callbackUrl not found in {data}")
            self._state = data["callbackUrl"]

        _LOGGER.debug(
            "[%s] updating %s, value is %s %s",
            self._device_name,
            self._description,
            self._state,
            self._attributes,
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

        # online sensor
        if self._name == "online":
            # get the online status
            data = await self.api_client.async_api_deviceOnline(self._device_id)
            if "onLine" not in data:
                raise InvalidResponse(f"onLine not found in {data}")
            self._state = data["onLine"] == "1"

        # motionAlarm sensor
        if self._name == "motionAlarm":
            # get the time of the last alarm
            data = await self.api_client.async_api_getAlarmMessage(self._device_id)
            if "alarms" not in data:
                raise InvalidResponse(f"alarms not found in {data}")
            if len(data["alarms"]) > 0:
                alarm = data["alarms"][0]
                if "time" not in alarm or "type" not in alarm or "msgType" not in alarm or "deviceId" not in alarm:
                    raise InvalidResponse(f"time, type, msgType or deviceId not found in {alarm}")
                # convert it into ISO 8601
                alarm_time = datetime.utcfromtimestamp(alarm["time"]).isoformat()
                # if previously stored alarm time is different, an alarm occurred in the mean time
                if "alarm_time" in self._attributes and alarm_time != self._attributes["alarm_time"]:
                    self._state = True
                else:
                    self._state = False
                # save attributes
                self._attributes = {
                    "alarm_time": alarm_time,
                    "alarm_type": alarm["msgType"],
                    "alarm_code": alarm["type"],
                }

        _LOGGER.debug(
            "[%s] updating %s, value is %s %s",
            self._device_name,
            self._description,
            self._state,
            self._attributes,
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
        # pushNotifications sensor
        if self._name == "pushNotifications":
            data = await self.api_client.async_api_getMessageCallback()
        # all the other dynamically created sensors
        else:
            data = await self.api_client.async_api_getDeviceCameraStatus(self._device_id, self._name)
        _LOGGER.debug(
            "[%s] updating %s, value is %s %s",
            self._device_name,
            self._description,
            data["status"].upper(),
            self._attributes,
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
        _LOGGER.debug("[%s] %s requested to turn ON (%s)", self._device_name, self._description, kwargs)
        # pushNotifications sensor
        if self._name == "pushNotifications":
            if "url" not in kwargs:
                raise APIError("url not provided")
            await self.api_client.async_api_setMessageCallbackOn(kwargs.get("url"))
        # all the other dynamically created sensors
        else:
            await self.api_client.async_api_setDeviceCameraStatus(self._device_id, self._name, True)
        self._state = True

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        if not self._enabled:
            return
        _LOGGER.debug("[%s] %s requested to turn OFF (%s)", self._device_name, self._description, kwargs)
        if self._name == "pushNotifications":
            await self.api_client.async_api_setMessageCallbackOff()
        # all the other dynamically created sensors
        else:
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


class ImouSelect(ImouEntity):
    """A representation of a select within an IMOU Device."""

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
            sensor_type: the sensor type from const SELECT
        """
        super().__init__(api_client, device_id, device_name, sensor_type, SELECT[sensor_type])
        # keep track of the status of the sensor
        self._current_option: Union[str, None] = None
        self._available_options: list[str] = []

    async def async_update(self, **kwargs):
        """Update the entity."""
        if not self._enabled:
            return
        if self._name == "nightVisionMode":
            # get the night vision mode option selected
            data = await self.api_client.async_api_getNightVisionMode(self._device_id)
            if "mode" not in data or "modes" not in data:
                raise InvalidResponse(f"mode or modes not found in {data}")
            self._current_option = data["mode"]
            self._available_options = data["modes"]
        _LOGGER.debug(
            "[%s] updating %s, value is %s %s",
            self._device_name,
            self._description,
            self._current_option,
            self._attributes,
        )
        if not self._updated:
            self._updated = True

    def get_current_option(self) -> Optional[str]:
        """Return the current option."""
        return self._current_option

    def get_available_options(self) -> list[str]:
        """Return the available options."""
        return self._available_options

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        if not self._enabled:
            return
        _LOGGER.debug("[%s] %s setting to %s", self._device_name, self._description, option)
        if self._name == "nightVisionMode":
            await self.api_client.async_api_setNightVisionMode(self._device_id, option)
            self._current_option = option


class ImouButton(ImouEntity):
    """A representation of a button within an IMOU Device."""

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
            sensor_type: the sensor type from const BUTTON
        """
        super().__init__(api_client, device_id, device_name, sensor_type, BUTTONS[sensor_type])

    async def async_press(self) -> None:
        """Press action."""
        if not self._enabled:
            return
        if self._name == "restartDevice":
            # restart the device
            await self.api_client.async_api_restartDevice(self._device_id)

        _LOGGER.debug(
            "[%s] pressed button %s",
            self._device_name,
            self._description,
        )
        if not self._updated:
            self._updated = True

    async def async_update(self, **kwargs):
        """Update the entity."""
        return


class ImouSiren(ImouEntity):
    """A representation of a siren within an IMOU Device."""

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
            sensor_type: the sensor type (from the SIRENS constant)
        """
        super().__init__(api_client, device_id, device_name, sensor_type, SIRENS[sensor_type])
        self._state = False

    async def async_update(self, **kwargs):
        """Update the entity."""
        if not self._enabled:
            return
        # siren sensor
        if self._name == "siren":
            # async_api_getDeviceCameraStatus() does not return the current state of the siren, do nothing here
            pass

    def is_on(self) -> Optional[bool]:
        """Return the status of the switch."""
        return self._state

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        if not self._enabled:
            return
        _LOGGER.debug("[%s] %s requested to turn ON (%s)", self._device_name, self._description, kwargs)
        # siren sensor
        if self._name == "siren":
            await self.api_client.async_api_setDeviceCameraStatus(self._device_id, self._name, True)
        self._state = True

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        if not self._enabled:
            return
        _LOGGER.debug("[%s] %s requested to turn OFF (%s)", self._device_name, self._description, kwargs)
        # siren sensor
        if self._name == "siren":
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
