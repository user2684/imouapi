"""Class representing a binary sensor belonging to an Imou device."""
import logging

from imouapi.api import ImouAPIClient
from imouapi.const import BINARY_SENSOR_ICONS, BINARY_SENSORS
from imouapi.entity import ImouEntity
from imouapi.exceptions import InvalidResponse

_LOGGER: logging.Logger = logging.getLogger(__package__)


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
            `api_client`: an instance ofthe API client
            `device_id`: the device id
            `sensor_type`: the sensor type from const BINARY_SENSORS
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
