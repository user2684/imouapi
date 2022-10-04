"""High level API to discover and interacting with Imou devices and their sensors."""
import logging
from typing import Union

from imouapi.api import ImouAPIClient
from imouapi.const import BINARY_SENSORS, IMOU_CAPABILITIES, IMOU_SWITCHES, SENSORS
from imouapi.device_entity import ImouBinarySensor, ImouEntity, ImouSensor, ImouSwitch
from imouapi.exceptions import InvalidResponse

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ImouDevice:
    """A representation of an IMOU Device."""

    def __init__(
        self,
        api_client: ImouAPIClient,
        device_id: str,
    ) -> None:
        """
        Initialize the instance.

        Parameters:
            api_client: an ImouAPIClient instance
            device_id: device id
        """
        self._api_client = api_client
        self._device_id = device_id

        self._catalog = "N.A."
        self._firmware = "N.A."
        self._name = "N.A."
        self._given_name = ""
        self._device_model = "N.A."
        self._manufacturer = "Imou"
        self._online = False
        self._capabilities: list[str] = []
        self._switches: list[str] = []
        self._sensor_instances: dict[str, list] = {"switch": [], "sensor": [], "binary_sensor": []}

        self._initialized = False
        self._enabled = True

    def get_device_id(self) -> str:
        """Get device id."""
        return self._device_id

    def get_name(self) -> str:
        """Get device name."""
        if self._given_name != "":
            return self._given_name
        return self._name

    def set_name(self, given_name: str) -> None:
        """Set device name."""
        self._given_name = given_name

    def get_model(self) -> str:
        """Get model."""
        return self._device_model

    def get_manufacturer(self) -> str:
        """Get manufacturer."""
        return self._manufacturer

    def get_firmware(self) -> str:
        """Get firmware."""
        return self._firmware

    def is_online(self) -> bool:
        """Get online."""
        return self._online

    def get_all_sensors(self) -> list[ImouEntity]:
        """Get all the sensor instances."""
        sensors = []
        for (
            platform,  # pylint: disable=unused-variable
            sensor_instances_array,
        ) in self._sensor_instances.items():
            for sensor_instance in sensor_instances_array:
                sensors.append(sensor_instance)
        return sensors

    def get_sensors_by_platform(self, platform: str) -> list[ImouEntity]:
        """Get sensor instances associated to a given platform."""
        if platform not in self._sensor_instances:
            return []
        return self._sensor_instances[platform]

    def get_sensor_by_name(self, name: str) -> Union[ImouSensor, ImouBinarySensor, ImouSwitch, None]:
        """Get sensor instance with a given name."""
        for (
            platform,  # pylint: disable=unused-variable
            sensor_instances_array,
        ) in self._sensor_instances.items():
            for sensor_instance in sensor_instances_array:
                if sensor_instance.get_name() == name:
                    return sensor_instance
        return None

    def set_enabled(self, value: bool) -> None:
        """Set enable."""
        self._enabled = value

    def is_enabled(self) -> bool:
        """Is enabled."""
        return self._enabled

    async def async_initialize(self) -> None:
        """Initialize the instance by retrieving the device details and associated sensors."""
        # get the details for this device from the API
        device_array = await self._api_client.async_api_deviceBaseDetailList([self._device_id])
        if "deviceList" not in device_array or len(device_array["deviceList"]) != 1:
            raise InvalidResponse(f"deviceList not found in {str(device_array)}")
        # reponse is an array, our data is in the first element
        device_data = device_array["deviceList"][0]
        try:
            # get device details
            self._catalog = device_data["catalog"]
            self._firmware = device_data["version"]
            self._name = device_data["name"]
            self._device_model = device_data["deviceModel"]
            self._online = device_data["status"] == "online"
            # get device capabilities
            self._capabilities = device_data["ability"].split(",")
            # For some reason motionDetect is not listed as a capability like it should
            if "motionDetect" not in self._capabilities:
                self._capabilities.append("motionDetect")
            switches_keys = IMOU_SWITCHES.keys()
            # add switches. For each possible switch, check if there is a capability with the same name \
            # (ref. https://open.imoulife.com/book/en/faq/feature.html)
            for switch_type in switches_keys:
                for capability in self._capabilities:
                    if switch_type.lower() == capability.lower():
                        self._switches.append(switch_type)
                        # create an instance and save it
                        switch_instance = ImouSwitch(
                            self._api_client,
                            self._device_id,
                            self.get_name(),
                            switch_type,
                        )
                        self._sensor_instances["switch"].append(switch_instance)
                        break
            # add lastAlarm sensor
            self._sensor_instances["sensor"].append(
                ImouSensor(
                    self._api_client,
                    self._device_id,
                    self.get_name(),
                    "lastAlarm",
                )
            )
            # add online binary sensor
            self._sensor_instances["binary_sensor"].append(
                ImouBinarySensor(
                    self._api_client,
                    self._device_id,
                    self.get_name(),
                    "online",
                )
            )
        except Exception as exception:
            raise InvalidResponse(f" missing parameter or error parsing in {device_data}") from exception
        _LOGGER.debug("Retrieved device %s", self.to_string())
        _LOGGER.debug("Device details:\n%s", self.dump())
        # keep track that we have already asked for the device details
        self._initialized = True

    async def async_get_data(self) -> bool:
        """Update device properties and its sensors."""
        if not self._enabled:
            return False
        if not self._initialized:
            # get the details of the device first
            await self.async_initialize()

        # check if the device is online
        _LOGGER.debug("[%s] update requested", self.get_name())
        data = await self._api_client.async_api_deviceOnline(self._device_id)
        self._online = data["onLine"] == "1"

        # update the status of all the sensors (if the device is online)
        if self._online:
            for (
                platform,  # pylint: disable=unused-variable
                sensor_instances_array,
            ) in self._sensor_instances.items():
                for sensor_instance in sensor_instances_array:
                    await sensor_instance.async_update()
        return True

    def to_string(self) -> str:
        """Return the object as a string."""
        return f"{self._name} ({self._device_model}, serial {self._device_id})"

    def dump(self) -> str:
        """Return the full description of the object and its attributes."""
        online = "yes" if self._online else "no"
        dump = (
            f"- Device ID: {self._device_id}\n"
            + f"    Name: {self._name}\n"
            + f"    Catalog: {self._catalog}\n"
            + f"    Model: {self._device_model}\n"
            + f"    Firmware: {self._firmware}\n"
            + f"    Online: {online}\n"
        )
        dump = dump + "    Capabilities: \n"
        for capability in self._capabilities:
            description = (
                f"{IMOU_CAPABILITIES[capability]} ({capability})" if capability in IMOU_CAPABILITIES else capability
            )
            dump = dump + f"        - {description}\n"
        dump = dump + "    Switches: \n"
        for sensor_instance in self._sensor_instances["switch"]:
            sensor_name = sensor_instance.get_name()
            description = (
                f"{IMOU_SWITCHES[sensor_name]} ({sensor_name})" if sensor_name in IMOU_SWITCHES else sensor_name
            )
            dump = dump + f"        - {description}: {sensor_instance.is_on()}\n"
        dump = dump + "    Sensors: \n"
        for sensor_instance in self._sensor_instances["sensor"]:
            sensor_name = sensor_instance.get_name()
            description = f"{SENSORS[sensor_name]} ({sensor_name})"
            dump = dump + f"        - {description}: {sensor_instance.get_state()}\n"
        dump = dump + "    Binary Sensors: \n"
        for sensor_instance in self._sensor_instances["binary_sensor"]:
            sensor_name = sensor_instance.get_name()
            description = f"{BINARY_SENSORS[sensor_name]} ({sensor_name})"
            dump = dump + f"        - {description}: {sensor_instance.is_on()}\n"
        return dump


class ImouDiscoverService:
    """Class for discovering IMOU devices."""

    def __init__(self, api_client: ImouAPIClient) -> None:
        """
        Initialize the instance.

        Parameters:
            api_client: an ImouAPIClient instance
        """
        self._api_client = api_client

    async def async_discover_devices(self) -> dict:
        """Discover registered devices and return a dict device name -> device object."""
        _LOGGER.debug("Starting discovery")
        # get the list of devices
        devices_data = await self._api_client.async_api_deviceBaseList()
        if "deviceList" not in devices_data or "count" not in devices_data:
            raise InvalidResponse(f"deviceList or count not found in {devices_data}")
        _LOGGER.debug("Discovered %d registered devices", devices_data["count"])
        # extract the device id for each device
        devices = {}
        for device_data in devices_data["deviceList"]:
            # create a a device instance from the device id and initialize it
            device = ImouDevice(self._api_client, device_data["deviceId"])
            await device.async_initialize()
            _LOGGER.debug("   - %s", device.to_string())
            devices[f"{device.get_name()}"] = device
        # return a dict with device name -> device instance
        return devices