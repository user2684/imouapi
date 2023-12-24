"""High level API to discover and interacting with Imou devices and their sensors."""
import asyncio
import logging
import re
from typing import Any, Dict, List, Union

from .api import ImouAPIClient
from .const import (
    BINARY_SENSORS,
    BUTTONS,
    CAMERA_WAIT_BEFORE_DOWNLOAD,
    CAMERAS,
    IMOU_CAPABILITIES,
    IMOU_SWITCHES,
    ONLINE_STATUS,
    SELECT,
    SENSORS,
    SIRENS,
    WAIT_AFTER_WAKE_UP,
)
from .device_entity import (
    ImouBinarySensor,
    ImouButton,
    ImouCamera,
    ImouEntity,
    ImouSelect,
    ImouSensor,
    ImouSiren,
    ImouSwitch,
)
from .exceptions import InvalidResponse

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
        self._status = "UNKNOWN"
        self._capabilities: List[str] = []
        self._switches: List[str] = []
        self._sensor_instances: Dict[str, list] = {
            "switch": [],
            "sensor": [],
            "binary_sensor": [],
            "select": [],
            "button": [],
            "siren": [],
            "camera": [],
        }
        self._initialized = False
        self._enabled = True
        self._sleepable = False
        self._wait_after_wakeup = WAIT_AFTER_WAKE_UP
        self._camera_wait_before_download = CAMERA_WAIT_BEFORE_DOWNLOAD

    def get_device_id(self) -> str:
        """Get device id."""
        return self._device_id

    def get_api_client(self) -> ImouAPIClient:
        """Get api client."""
        return self._api_client

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

    def get_status(self) -> str:
        """Get status."""
        return self._status

    def is_online(self) -> bool:
        """Get online status."""
        return ONLINE_STATUS[self._status] == "Online" or ONLINE_STATUS[self._status] == "Dormant"

    def get_sleepable(self) -> bool:
        """Get sleepable."""
        return self._sleepable

    def get_all_sensors(self) -> List[ImouEntity]:
        """Get all the sensor instances."""
        sensors = []
        for (
            platform,  # pylint: disable=unused-variable
            sensor_instances_array,
        ) in self._sensor_instances.items():
            for sensor_instance in sensor_instances_array:
                sensors.append(sensor_instance)
        return sensors

    def get_sensors_by_platform(self, platform: str) -> List[ImouEntity]:
        """Get sensor instances associated to a given platform."""
        if platform not in self._sensor_instances:
            return []
        return self._sensor_instances[platform]

    def get_sensor_by_name(
        self, name: str
    ) -> Union[ImouSensor, ImouBinarySensor, ImouSwitch, ImouSelect, ImouButton, None]:
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

    def set_wait_after_wakeup(self, value: float) -> None:
        """Set wait after wakeup."""
        self._wait_after_wakeup = value

    def get_wait_after_wakeup(self) -> float:
        """Get wait after wakeup."""
        return self._wait_after_wakeup

    def set_camera_wait_before_download(self, value: float) -> None:
        """Set camera wait before download."""
        self._camera_wait_before_download = value

    def get_camera_wait_before_download(self) -> float:
        """Get camera wait before download."""
        return self._camera_wait_before_download

    def _add_sensor_instance(self, platform, instance):
        """Add a sensor instance."""
        instance.set_device(self)
        self._sensor_instances[platform].append(instance)

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
            # get device capabilities
            self._capabilities = device_data["ability"].split(",")
            # Add undocumented capabilities or capabilities inherited from other capabilities
            self._capabilities.append("MotionDetect")
            if "WLM" in self._capabilities:
                self._capabilities.append("Linkagewhitelight")
            if "WLAN" in self._capabilities:
                self._capabilities.append("pushNotifications")
            switches_keys = IMOU_SWITCHES.keys()
            # add switches. For each possible switch, check if there is a capability with the same name \
            # (ref. https://open.imoulife.com/book/en/faq/feature.html)
            for switch_type in switches_keys:
                for capability in self._capabilities:
                    capability = capability.lower()
                    capability = re.sub("v\\d$", "", capability)
                    if switch_type.lower() == capability and switch_type.lower() not in self._switches:
                        self._switches.append(switch_type)
                        # create an instance and save it
                        self._add_sensor_instance(
                            "switch",
                            ImouSwitch(
                                self._api_client,
                                self._device_id,
                                self.get_name(),
                                switch_type,
                            ),
                        )
                        break
            # identify sleepable devices
            if "Dormant" in self._capabilities:
                self._sleepable = True
                self._add_sensor_instance(
                    "sensor",
                    ImouSensor(
                        self._api_client,
                        self._device_id,
                        self.get_name(),
                        "battery",
                    ),
                )
            # add storageUsed sensor
            if "LocalStorage" in self._capabilities:
                self._add_sensor_instance(
                    "sensor",
                    ImouSensor(
                        self._api_client,
                        self._device_id,
                        self.get_name(),
                        "storageUsed",
                    ),
                )
            # add callbackUrl sensor
            self._add_sensor_instance(
                "sensor",
                ImouSensor(
                    self._api_client,
                    self._device_id,
                    self.get_name(),
                    "callbackUrl",
                ),
            )
            # add status sensor
            self._add_sensor_instance(
                "sensor",
                ImouSensor(
                    self._api_client,
                    self._device_id,
                    self.get_name(),
                    "status",
                ),
            )
            # add online binary sensor
            if "WLAN" in self._capabilities:
                self._add_sensor_instance(
                    "binary_sensor",
                    ImouBinarySensor(
                        self._api_client,
                        self._device_id,
                        self.get_name(),
                        "online",
                    ),
                )
            # add motionAlarm binary sensor
            if "AlarmMD" in self._capabilities:
                self._add_sensor_instance(
                    "binary_sensor",
                    ImouBinarySensor(
                        self._api_client,
                        self._device_id,
                        self.get_name(),
                        "motionAlarm",
                    ),
                )
            # add nightVisionMode select
            if "NVM" in self._capabilities:
                self._add_sensor_instance(
                    "select",
                    ImouSelect(
                        self._api_client,
                        self._device_id,
                        self.get_name(),
                        "nightVisionMode",
                    ),
                )
            # add restartDevice button
            self._add_sensor_instance(
                "button",
                ImouButton(
                    self._api_client,
                    self._device_id,
                    self.get_name(),
                    "restartDevice",
                ),
            )
            # add refreshData button
            self._add_sensor_instance(
                "button",
                ImouButton(
                    self._api_client,
                    self._device_id,
                    self.get_name(),
                    "refreshData",
                ),
            )
            # add refreshAlarm button
            self._add_sensor_instance(
                "button",
                ImouButton(
                    self._api_client,
                    self._device_id,
                    self.get_name(),
                    "refreshAlarm",
                ),
            )
            # add siren siren
            if "Siren" in self._capabilities:
                self._add_sensor_instance(
                    "siren",
                    ImouSiren(
                        self._api_client,
                        self._device_id,
                        self.get_name(),
                        "siren",
                    ),
                )
            # add cameras
            self._add_sensor_instance(
                "camera",
                ImouCamera(
                    self._api_client,
                    self._device_id,
                    self.get_name(),
                    "camera",
                    "HD",
                ),
            )
            self._add_sensor_instance(
                "camera",
                ImouCamera(
                    self._api_client,
                    self._device_id,
                    self.get_name(),
                    "cameraSD",
                    "SD",
                ),
            )
        except Exception as exception:
            raise InvalidResponse(f" missing parameter or error parsing in {device_data}") from exception
        _LOGGER.debug("Retrieved device %s", self.to_string())
        _LOGGER.debug("Device details:\n%s", self.dump())
        # keep track that we have already asked for the device details
        self._initialized = True

    async def async_refresh_status(self) -> None:
        """Refresh status attribute."""
        data = await self._api_client.async_api_deviceOnline(self._device_id)
        if "onLine" not in data or data["onLine"] not in ONLINE_STATUS:
            raise InvalidResponse(f"onLine not valid in {data}")
        self._status = data["onLine"]

    async def async_wakeup(self) -> bool:
        """Wake up a dormant device."""
        # if this is a regular device, just return
        if not self._sleepable:
            return True
        # if the device is already online, return
        await self.async_refresh_status()
        if ONLINE_STATUS[self._status] == "Online":
            return True
        # wake up the device
        _LOGGER.debug("[%s] waking up the dormant device", self.get_name())
        await self._api_client.async_api_setDeviceCameraStatus(self._device_id, "closeDormant", True)
        # wait for the device to be fully up
        await asyncio.sleep(self._wait_after_wakeup)
        # ensure the device is up
        await self.async_refresh_status()
        if ONLINE_STATUS[self._status] == "Online":
            _LOGGER.debug("[%s] device is now online", self.get_name())
            return True
        _LOGGER.warning("[%s] failed to wake up dormant device", self.get_name())
        return False

    async def async_get_data(self) -> bool:
        """Update device properties and its sensors."""
        if not self._enabled:
            return False
        if not self._initialized:
            # get the details of the device first
            await self.async_initialize()
        _LOGGER.debug("[%s] update requested", self.get_name())

        # check if the device is online
        await self.async_refresh_status()

        # update the status of all the sensors (if the device is online)
        if self.is_online():
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

    def get_diagnostics(self) -> Dict[str, Any]:
        """Return diagnostics for the device."""
        # prepare capabilities
        capabilities = []
        for capability_name in self._capabilities:
            capability = {}
            description = (
                f"{IMOU_CAPABILITIES[capability_name]} ({capability_name})"
                if capability_name in IMOU_CAPABILITIES
                else capability_name
            )
            capability["name"] = capability_name
            capability["description"] = description
            capabilities.append(capability)
        # prepare switches
        switches = []
        for sensor_instance in self._sensor_instances["switch"]:
            sensor = {}
            sensor_name = sensor_instance.get_name()
            description = (
                f"{IMOU_SWITCHES[sensor_name]} ({sensor_name})" if sensor_name in IMOU_SWITCHES else sensor_name
            )
            sensor["name"] = sensor_name
            sensor["description"] = description
            sensor["state"] = sensor_instance.is_on()
            sensor["is_enabled"] = sensor_instance.is_enabled()
            sensor["is_updated"] = sensor_instance.is_updated()
            sensor["attributes"] = sensor_instance.get_attributes()
            switches.append(sensor)
        # prepare sensors
        sensors = []
        for sensor_instance in self._sensor_instances["sensor"]:
            sensor = {}
            sensor_name = sensor_instance.get_name()
            description = f"{SENSORS[sensor_name]} ({sensor_name})"
            sensor["name"] = sensor_name
            sensor["description"] = description
            sensor["state"] = sensor_instance.get_state()
            sensor["is_enabled"] = sensor_instance.is_enabled()
            sensor["is_updated"] = sensor_instance.is_updated()
            sensor["attributes"] = sensor_instance.get_attributes()
            sensors.append(sensor)
        # prepare binary sensors
        binary_sensors = []
        for sensor_instance in self._sensor_instances["binary_sensor"]:
            sensor = {}
            sensor_name = sensor_instance.get_name()
            description = f"{BINARY_SENSORS[sensor_name]} ({sensor_name})"
            sensor["name"] = sensor_name
            sensor["description"] = description
            sensor["state"] = sensor_instance.is_on()
            sensor["is_enabled"] = sensor_instance.is_enabled()
            sensor["is_updated"] = sensor_instance.is_updated()
            sensor["attributes"] = sensor_instance.get_attributes()
            binary_sensors.append(sensor)
        # prepare select
        selects = []
        for sensor_instance in self._sensor_instances["select"]:
            sensor = {}
            sensor_name = sensor_instance.get_name()
            description = f"{SELECT[sensor_name]} ({sensor_name})"
            sensor["name"] = sensor_name
            sensor["description"] = description
            sensor["current_option"] = sensor_instance.get_current_option()
            sensor["available_options"] = sensor_instance.get_available_options()
            sensor["is_enabled"] = sensor_instance.is_enabled()
            sensor["is_updated"] = sensor_instance.is_updated()
            sensor["attributes"] = sensor_instance.get_attributes()
            selects.append(sensor)
        # prepare button
        buttons = []
        for sensor_instance in self._sensor_instances["button"]:
            sensor = {}
            sensor_name = sensor_instance.get_name()
            description = f"{BUTTONS[sensor_name]} ({sensor_name})"
            sensor["name"] = sensor_name
            sensor["description"] = description
            sensor["is_enabled"] = sensor_instance.is_enabled()
            sensor["is_updated"] = sensor_instance.is_updated()
            sensor["attributes"] = sensor_instance.get_attributes()
            buttons.append(sensor)
        # prepare sirens
        sirens = []
        for sensor_instance in self._sensor_instances["siren"]:
            sensor = {}
            sensor_name = sensor_instance.get_name()
            description = f"{SIRENS[sensor_name]} ({sensor_name})" if sensor_name in SIRENS else sensor_name
            sensor["name"] = sensor_name
            sensor["description"] = description
            sensor["state"] = sensor_instance.is_on()
            sensor["is_enabled"] = sensor_instance.is_enabled()
            sensor["is_updated"] = sensor_instance.is_updated()
            sensor["attributes"] = sensor_instance.get_attributes()
            sirens.append(sensor)
        # prepare cameras
        cameras = []
        for sensor_instance in self._sensor_instances["camera"]:
            sensor = {}
            sensor_name = sensor_instance.get_name()
            description = f"{CAMERAS[sensor_name]} ({sensor_name})" if sensor_name in CAMERAS else sensor_name
            sensor["name"] = sensor_name
            sensor["description"] = description
            sensor["is_enabled"] = sensor_instance.is_enabled()
            sensor["is_updated"] = sensor_instance.is_updated()
            sensor["attributes"] = sensor_instance.get_attributes()
            cameras.append(sensor)
        # prepare data structure to return
        data: Dict[str, Any] = {
            "api": {
                "base_url": self._api_client.get_base_url(),
                "timeout": self._api_client.get_timeout(),
                "is_connected": self._api_client.is_connected(),
            },
            "device": {
                "device_id": self._device_id,
                "name": self._name,
                "catalog": self._catalog,
                "given_name": self._given_name,
                "model": self._device_model,
                "firmware": self._firmware,
                "manufacturer": self._manufacturer,
                "status": self._status,
                "sleepable": self._sleepable,
            },
            "capabilities": capabilities,
            "switches": switches,
            "sensors": sensors,
            "binary_sensors": binary_sensors,
            "selects": selects,
            "buttons": buttons,
            "sirens": sirens,
            "cameras": cameras,
        }
        return data

    def dump(self) -> str:
        """Return the full description of the object and its attributes."""
        data = self.get_diagnostics()
        dump = (
            f"- Device ID: {data['device']['device_id']}\n"
            + f"    Name: {data['device']['name']}\n"
            + f"    Catalog: {data['device']['catalog']}\n"
            + f"    Model: {data['device']['model']}\n"
            + f"    Firmware: {data['device']['firmware']}\n"
            + f"    Status: {ONLINE_STATUS[data['device']['status']]}\n"
            + f"    Sleepable: {data['device']['sleepable']}\n"
        )
        dump = dump + "    Capabilities: \n"
        for capability in data["capabilities"]:
            dump = dump + f"        - {capability['description']}\n"
        dump = dump + "    Switches: \n"
        for sensor in data["switches"]:
            dump = (
                dump
                + f"        - {sensor['description']}: {sensor['state']} {sensor['attributes'] if len(sensor['attributes']) > 0 else ''}\n"  # noqa: E501
            )
        dump = dump + "    Sensors: \n"
        for sensor in data["sensors"]:
            dump = (
                dump
                + f"        - {sensor['description']}: {sensor['state']} {sensor['attributes'] if len(sensor['attributes']) > 0 else ''}\n"  # noqa: E501
            )
        dump = dump + "    Binary Sensors: \n"
        for sensor in data["binary_sensors"]:
            dump = (
                dump
                + f"        - {sensor['description']}: {sensor['state']} {sensor['attributes'] if len(sensor['attributes']) > 0 else ''}\n"  # noqa: E501
            )
        dump = dump + "    Select: \n"
        for sensor in data["selects"]:
            dump = (
                dump
                + f"        - {sensor['description']}: {sensor['current_option']} {sensor['attributes'] if len(sensor['attributes']) > 0 else ''}\n"  # noqa: E501
            )
        dump = dump + "    Buttons: \n"
        for sensor in data["buttons"]:
            dump = (
                dump
                + f"        - {sensor['description']} {sensor['attributes'] if len(sensor['attributes']) > 0 else ''}\n"  # noqa: E501
            )
        dump = dump + "    Sirens: \n"
        for sensor in data["sirens"]:
            dump = (
                dump
                + f"        - {sensor['description']}: {sensor['state']} {sensor['attributes'] if len(sensor['attributes']) > 0 else ''}\n"  # noqa: E501
            )
        dump = dump + "    Cameras: \n"
        for sensor in data["cameras"]:
            dump = (
                dump
                + f"        - {sensor['description']}: {sensor['attributes'] if len(sensor['attributes']) > 0 else ''}\n"  # noqa: E501
            )
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
            try:
                await device.async_initialize()
                _LOGGER.debug("   - %s", device.to_string())
                devices[f"{device.get_name()}"] = device
            except InvalidResponse as exception:
                _LOGGER.warning(
                    "skipping unrecognized or unsupported device: ",
                    exception.to_string(),
                )
        # return a dict with device name -> device instance
        return devices
