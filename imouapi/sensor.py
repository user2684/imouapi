"""Class representing a sensor belonging to an Imou device."""
import logging
from datetime import datetime

from imouapi.api import ImouAPIClient
from imouapi.const import SENSOR_ICONS, SENSORS
from imouapi.entity import ImouEntity
from imouapi.exceptions import InvalidResponse

_LOGGER: logging.Logger = logging.getLogger(__package__)


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
            `api_client`: an instance ofthe API client
            `device_id`: the device id
            `sensor_type`: the sensor type from const SENSORS
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
