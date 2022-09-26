"""Class for discovering IMOU devices."""
import logging

import aiohttp

from imouapi.api import ImouAPIClient
from imouapi.const import API_URL
from imouapi.device import ImouDevice
from imouapi.exceptions import InvalidResponse

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ImouDiscoverService:
    """Class for discovering IMOU devices."""

    def __init__(
        self,
        app_id: str,
        app_secret: str,
        websession: aiohttp.ClientSession,
    ) -> None:
        """
        Initialize the instance.

        Parameters:
            `app_id`: appID from https://open.imoulife.com/consoleNew/myApp/appInfo
            `app_secret`: appID from https://open.imoulife.com/consoleNew/myApp/appInfo
            `websession`: aiohttp client session
        """
        # initialize the properties
        self._app_id = app_id
        self._app_secret = app_secret
        self._websession = websession
        self._connected = False
        # setup the API client
        self.api_client = ImouAPIClient(API_URL, app_id, app_secret, websession)

    async def async_connect(self) -> bool:
        """Connect to the API."""
        status = await self.api_client.async_connect()
        if status:
            self._connected = True
        return status

    async def async_discover_devices(self) -> dict:
        """Discover registered devices and return a dict device name -> device object."""
        if not self._connected:
            await self.async_connect()
        _LOGGER.debug("Starting discovery")
        # get the list of devices
        devices_data = await self.api_client.async_api_deviceBaseList()
        if "deviceList" not in devices_data or "count" not in devices_data:
            raise InvalidResponse(f"deviceList or count not found in {devices_data}")
        _LOGGER.info("Discovered %d registered devices", devices_data["count"])
        # extract the device id for each device
        devices = {}
        for device_data in devices_data["deviceList"]:
            # create a a device instance from the device id and initialize it
            device = ImouDevice(
                self._app_id,
                self._app_secret,
                device_data["deviceId"],
                self._websession,
            )
            await device.async_connect()
            await device.async_initialize()
            _LOGGER.info("   - %s", device.to_string())
            devices[f"{device.get_name()}"] = device
        # return a dict with device name -> device instance
        return devices
