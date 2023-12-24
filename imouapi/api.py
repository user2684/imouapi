"""Low-level API for interacting with Imou devices."""
import hashlib
import json
import logging
import random
import re
import secrets
import time
from datetime import datetime, timedelta
from typing import List

from aiohttp import ClientSession

from .const import API_URL, DEFAULT_TIMEOUT, MAX_RETRIES, PTZ_OPERATIONS
from .exceptions import (
    APIError,
    ConnectionFailed,
    ImouException,
    InvalidConfiguration,
    InvalidResponse,
    NotAuthorized,
    NotConnected,
)

_LOGGER = logging.getLogger(__package__)


class ImouAPIClient:
    """Interact with IMOU API."""

    def __init__(self, app_id: str, app_secret: str, session: ClientSession) -> None:
        """
        Initialize the instance.

        Parameters:
            app_id: appID from https://open.imoulife.com/consoleNew/myApp/appInfo
            app_secret: appID from https://open.imoulife.com/consoleNew/myApp/appInfo
            session: aiohttp client session
        """
        self._app_id = app_id
        self._app_secret = app_secret
        self._session = session

        self._base_url = API_URL
        self._timeout = DEFAULT_TIMEOUT
        self._log_http_requests_enabled = False
        self._redact_log_message_enabled = True

        self._access_token = None
        self._access_token_expire_time = None
        self._connected = False
        self._retries = 1
        _LOGGER.debug("Initialized. Endpoint URL: %s", self._base_url)

    def _redact_log_message(self, data: str) -> str:
        """Redact log messages to remove sensitive information."""
        if not self._redact_log_message_enabled:
            return data
        for keyword in (
            "appId",
            "sign",
            "token",
            "accessToken",
            "playToken",
            "thumbUrl",
            "picUrl",
        ):
            for tick in ('"', "'"):
                data = re.sub(
                    f"{tick}{keyword}{tick}:\\s*{tick}[^{tick}]+{tick}",
                    f"{tick}{keyword}{tick}: {tick}XXXXXXXXX{tick}",
                    data,
                )
        return data

    def get_base_url(self) -> str:
        """Get base url for the API."""
        return self._base_url

    def set_base_url(self, value: str) -> None:
        """Set a custom base url for the API."""
        self._base_url = value
        _LOGGER.debug("Set endpoint URL to %s", self._base_url)

    def get_timeout(self) -> int:
        """Get timeout for the API."""
        return self._timeout

    def set_timeout(self, value: int) -> None:
        """Set a custom timeout."""
        self._timeout = value
        _LOGGER.debug("Set timeout to %s", self._base_url)

    def set_session(self, value: ClientSession) -> None:
        """Set an aiohttp client session."""
        self._session = value

    def get_session(self) -> ClientSession:
        """Return the aiohttp client session."""
        return self._session

    def set_log_http_requests(self, value: bool) -> None:
        """Set to true if you want in debug logs also HTTP requests and responses."""
        self._log_http_requests_enabled = value

    def set_redact_log_messages(self, value: bool) -> None:
        """Set to true if you want debug logs redacted from sensitive data."""
        self._redact_log_message_enabled = value

    async def async_connect(self) -> bool:
        """Authenticate against the API and retrieve an access token."""
        # check if we already have an access token and if so assume already authenticated
        if self.is_connected():
            return True
        # call the access token endpoint
        _LOGGER.debug("Connecting")
        data = await self._async_call_api("accessToken", {}, True)
        if "accessToken" not in data or "expireTime" not in data:
            raise InvalidResponse(f"accessToken not found in {data}")
        # store the access token
        self._access_token = data["accessToken"]
        self._access_token_expire_time = data["expireTime"]
        _LOGGER.debug("Retrieved access token")
        self._connected = True
        return True

    async def async_disconnect(self) -> bool:
        """Disconnect from the API."""
        self._access_token = None
        self._access_token_expire_time = None
        self._connected = False
        _LOGGER.debug("Disconnected")
        return True

    async def async_reconnect(self) -> bool:
        """Reconnect to the API."""
        await self.async_disconnect()
        return await self.async_connect()

    def is_connected(self) -> bool:
        """Return true if already connected."""
        return self._connected

    async def _async_call_api(self, api: str, payload: dict, is_connect_request: bool = False) -> dict:  # noqa: C901
        """Submit request to the HTTP API endpoint."""
        # connect if not connected
        if not is_connect_request:
            while not self.is_connected():
                _LOGGER.debug("Connection attempt %d/%d", self._retries, MAX_RETRIES)
                # if noo many attempts, give up
                if self._retries >= MAX_RETRIES:
                    _LOGGER.error("Too many unsuccesful connection attempts")
                    break
                try:
                    await self.async_connect()
                except ImouException as exception:
                    _LOGGER.error(exception.to_string())
                self._retries = self._retries + 1
            if not self.is_connected():
                raise NotConnected()

        # calculate timestamp, nonce, sign and id as per https://open.imoulife.com/book/http/develop.html
        timestamp = round(time.time())
        nonce = secrets.token_urlsafe()
        sign = hashlib.md5(f"time:{timestamp},nonce:{nonce},appSecret:{self._app_secret}".encode("utf-8")).hexdigest()
        request_id = str(random.randint(1, 10000))

        # add the access token to the payload if already available
        if self._access_token is not None:
            payload["token"] = self._access_token

        # prepare the API request
        url = f"{self._base_url}/{api}"
        body = {
            "system": {
                "ver": "1.0",
                "sign": sign,
                "appId": self._app_id,
                "time": timestamp,
                "nonce": nonce,
            },
            "params": payload,
            "id": request_id,
        }
        if self._log_http_requests_enabled:
            _LOGGER.debug("[HTTP_REQUEST] %s: %s", url, self._redact_log_message(str(body)))

        # send the request to the API endpoint
        try:
            response = await self._session.request("POST", url, json=body, timeout=self._timeout)
        except Exception as exception:
            raise ConnectionFailed(f"{exception}") from exception

        # parse the response and look for errors
        response_status = response.status
        if self._log_http_requests_enabled:
            _LOGGER.debug(
                "[HTTP_RESPONSE] %s: %s",
                response_status,
                self._redact_log_message(str(await response.text())),
            )
        if response_status != 200:
            raise APIError(f"status code {response.status}")
        try:
            response_body = json.loads(await response.text())
        except Exception as exception:
            raise InvalidResponse(f"unable to parse response text {await response.text()}") from exception
        if (
            "result" not in response_body
            or "code" not in response_body["result"]
            or "msg" not in response_body["result"]
        ):
            raise InvalidResponse(f"cannot find result, code or msg in {response_body}")
        result_code = response_body["result"]["code"]
        result_message = response_body["result"]["msg"]
        if result_code != "0":
            error_message = result_code + ": " + result_message
            if result_code in ("OP1008", "SN1001"):
                raise InvalidConfiguration(f"Invalid appId or appSecret ({error_message})")
            if result_code == "OP1009":
                raise NotAuthorized(f"{error_message}")
            # if the access token is invalid or expired, reconnect
            if result_code == "TK1002":
                await self.async_reconnect()
                response_data = await self._async_call_api(api, payload, is_connect_request)
                return response_data
            raise APIError(error_message)

        # return the payload of the reponse
        response_data = response_body["result"]["data"] if "data" in response_body["result"] else {}
        return response_data

    async def async_api_deviceBaseList(self) -> dict:  # pylint: disable=invalid-name
        """Return the list of registered devices \
            (https://open.imoulife.com/book/http/device/manage/query/deviceBaseList.html)."""
        # define the api endpoint
        api = "deviceBaseList"
        # prepare the payload
        payload = {
            "bindId": -1,
            "limit": 50,
            "type": "bindAndShare",
            "needApInfo": True,
        }
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_deviceOpenList(self) -> dict:  # pylint: disable=invalid-name
        """Return the list of registered devices (Open) \
            (https://open.imoulife.com/book/http/device/manage/query/deviceOpenList.html)."""
        # define the api endpoint
        api = "deviceOpenList"
        # prepare the payload
        payload = {
            "bindId": -1,
            "limit": 50,
            "type": "bindAndShare",
            "needApInfo": True,
        }
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_deviceBaseDetailList(self, devices: List[str]) -> dict:  # pylint: disable=invalid-name
        """Return the details of the requested devices \
            (https://open.imoulife.com/book/http/device/manage/query/deviceBaseDetailList.html)."""
        # define the api endpoint
        api = "deviceBaseDetailList"
        # prepare the payload
        device_list = []
        for device in devices:
            device_list.append(
                {
                    "deviceId": device,
                    "channelList": "0",
                }
            )
        payload = {"deviceList": device_list}
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_deviceOpenDetailList(self, devices: List[str]) -> dict:  # pylint: disable=invalid-name
        """Return the details of the requested devices (Open) \
            (https://open.imoulife.com/book/http/device/manage/query/deviceOpenDetailList.html)."""
        # define the api endpoint
        api = "deviceOpenDetailList"
        # prepare the payload
        device_list = []
        for device in devices:
            device_list.append(
                {
                    "deviceId": device,
                    "channelList": "0",
                }
            )
        payload = {"deviceList": device_list}
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_listDeviceAbility(self, devices: List[str]) -> dict:  # pylint: disable=invalid-name
        """Ability to obtain multiple devices, channels, and accessories in batches \
            (https://open.imoulife.com/book/http/device/manage/query/listDeviceAbility.html)."""
        # define the api endpoint
        api = "listDeviceAbility"
        # prepare the payload
        device_list = []
        for device in devices:
            device_list.append(
                {
                    "deviceId": device,
                    "channelList": "0",
                }
            )
        payload = {"deviceList": device_list}
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_deviceOnline(self, device_id: str) -> dict:  # pylint: disable=invalid-name
        """Device online or offline \
            (https://open.imoulife.com/book/http/device/manage/query/deviceOnline.html)."""
        # define the api endpoint
        api = "deviceOnline"
        # prepare the payload
        payload = {
            "deviceId": device_id,
        }
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_deviceStorage(self, device_id: str) -> dict:  # pylint: disable=invalid-name
        """Obtain device storage medium capacity information. \
            (https://open.imoulife.com/book/http/device/config/storage/deviceStorage.html)."""
        # define the api endpoint
        api = "deviceStorage"
        # prepare the payload
        payload = {
            "deviceId": device_id,
        }
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_getDeviceCameraStatus(  # pylint: disable=invalid-name
        self, device_id: str, enable_type: str
    ) -> dict:
        """Get the status of the device switch \
            (https://open.imoulife.com/book/http/device/config/ability/getDeviceCameraStatus.html)."""
        # define the api endpoint
        api = "getDeviceCameraStatus"
        # prepare the payload
        payload = {
            "deviceId": device_id,
            "enableType": enable_type,
            "channelId": "0",
        }
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_setDeviceCameraStatus(  # pylint: disable=invalid-name
        self, device_id: str, enable_type: str, value: bool
    ) -> dict:
        """Set a device switch \
            (https://open.imoulife.com/book/http/device/config/ability/setDeviceCameraStatus.html)."""
        # define the api endpoint
        api = "setDeviceCameraStatus"
        # prepare the payload
        payload = {
            "deviceId": device_id,
            "enableType": enable_type,
            "enable": value,
            "channelId": "0",
        }
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_getAlarmMessage(self, device_id: str) -> dict:  # pylint: disable=invalid-name
        """Get the device message list of the device channel in the specified time period \
            (https://open.imoulife.com/book/http/device/alarm/getAlarmMessage.html)."""
        # define the api endpoint
        api = "getAlarmMessage"
        # prepare the payload
        now_time = datetime.now()
        begin_time = now_time - timedelta(days=30)
        end_time = now_time + timedelta(days=1)
        payload = {
            "deviceId": device_id,
            "count": "10",
            "channelId": "0",
            "beginTime": begin_time.strftime("%Y-%m-%d %H:%M:%S"),
            "endTime": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_getNightVisionMode(self, device_id: str) -> dict:  # pylint: disable=invalid-name
        """Query the night vision mode configuration of the device \
            (https://open.imoulife.com/book/http/device/config/video/getNightVisionMode.html)."""
        # define the api endpoint
        api = "getNightVisionMode"
        # prepare the payload
        payload = {
            "deviceId": device_id,
            "channelId": "0",
        }
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_setNightVisionMode(self, device_id: str, mode: str) -> dict:  # pylint: disable=invalid-name
        """Set the night vision mode of the device \
            (https://open.imoulife.com/book/http/device/config/video/setNightVisionMode.html)."""
        # define the api endpoint
        api = "setNightVisionMode"
        # prepare the payload
        payload = {
            "deviceId": device_id,
            "channelId": "0",
            "mode": mode,
        }
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_getMessageCallback(self) -> dict:  # pylint: disable=invalid-name
        """Get the message callback address information currently set \
            (https://open.imoulife.com/book/http/push/getMessageCallback.html)."""
        # define the api endpoint
        api = "getMessageCallback"
        # prepare the payload
        payload: dict = {}
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_setMessageCallbackOn(self, callback_url: str) -> dict:  # pylint: disable=invalid-name
        """Set the message callback address. \
            (https://open.imoulife.com/book/http/push/setMessageCallback.html)."""
        # define the api endpoint
        api = "setMessageCallback"
        # prepare the payload
        payload = {
            "callbackFlag": "alarm,deviceStatus",
            # "basePush": "2",
            "callbackUrl": callback_url,
            "status": "on",
        }
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_setMessageCallbackOff(self) -> dict:  # pylint: disable=invalid-name
        """Unset the message callback address. \
            (https://open.imoulife.com/book/http/push/setMessageCallback.html)."""
        # define the api endpoint
        api = "setMessageCallback"
        # prepare the payload
        payload = {
            "status": "off",
        }
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_restartDevice(self, device_id: str) -> dict:  # pylint: disable=invalid-name
        """Restart the device. \
            (https://open.imoulife.com/book/en/http/device/operate/restartDevice.html)."""
        # define the api endpoint
        api = "restartDevice"
        # prepare the payload
        payload = {
            "deviceId": device_id,
        }
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_deviceSdcardStatus(self, device_id: str) -> dict:  # pylint: disable=invalid-name
        """Get the SD card status of the device. \
            (https://open.imoulife.com/book/en/http/device/config/storage/deviceSdcardStatus.html)."""
        # define the api endpoint
        api = "deviceSdcardStatus"
        # prepare the payload
        payload = {
            "deviceId": device_id,
        }
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_devicePTZInfo(self, device_id: str) -> dict:  # pylint: disable=invalid-name
        """Get the current PTZ position information of the device. \
            (https://open.imoulife.com/book/en/http/device/operate/devicePTZInfo.html)."""
        # define the api endpoint
        api = "devicePTZInfo"
        # prepare the payload
        payload = {
            "deviceId": device_id,
            "channelId": "0",
        }
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_controlLocationPTZ(  # pylint: disable=invalid-name
        self, device_id: str, h: float, v: float, z: float
    ) -> dict:
        """PTZ positioning interface. \
            (https://open.imoulife.com/book/en/http/device/operate/controlLocationPTZ.html)."""
        # define the api endpoint
        api = "controlLocationPTZ"
        # prepare the payload
        try:
            h = float(h)
            v = float(v)
            z = float(z)
        except Exception as exception:
            raise APIError(f"cannot convert to float h:{h}, v:{v}, z:{z}") from exception
        if (h < -1 or h > 1) or (v < -1 or v > 1):
            raise APIError(f"h and v must be [-1;1]: h:{h}, v:{v}")
        if z < 0 or z > 1:
            raise APIError(f"z must be [0;1]: z: {z}")
        payload = {
            "deviceId": device_id,
            "channelId": "0",
            "h": h,
            "v": v,
            "z": z,
        }
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_controlMovePTZ(  # pylint: disable=invalid-name
        self, device_id: str, operation: str, duration: int
    ) -> dict:
        """PTZ movement control interface. \
            (https://open.imoulife.com/book/en/http/device/operate/controlMovePTZ.html)."""
        # define the api endpoint
        api = "controlMovePTZ"
        # prepare the payload
        operation = operation.upper()
        if operation not in PTZ_OPERATIONS:
            raise APIError(f"operation must one of {PTZ_OPERATIONS.keys()}")
        payload = {
            "deviceId": device_id,
            "channelId": "0",
            "operation": str(PTZ_OPERATIONS[operation]),
            "duration": str(duration),
        }
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_setDeviceSnapEnhanced(self, device_id: str) -> dict:  # pylint: disable=invalid-name
        """Capture pictures, supports the capture frequency of 1 time per second. \
            (https://open.imoulife.com/book/en/http/device/operate/setDeviceSnapEnhanced.html)."""
        # define the api endpoint
        api = "setDeviceSnapEnhanced"
        # prepare the payload
        payload = {
            "deviceId": device_id,
            "channelId": "0",
        }
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_bindDeviceLive(self, device_id: str, profile: str) -> dict:  # pylint: disable=invalid-name
        """Create device source live broadcast address for profile (HD or SD). \
            (https://open.imoulife.com/book/en/http/device/live/bindDeviceLive.html)."""
        # define the api endpoint
        api = "bindDeviceLive"
        # prepare the payload
        profile = profile.upper()
        stream_id = 0
        if profile == "HD":
            stream_id = 0
        elif profile == "SD":
            stream_id = 1
        else:
            raise APIError("profile must one of HD, SD")
        payload = {
            "deviceId": device_id,
            "channelId": "0",
            # streamId, 0: HD main stream; 1: SD auxiliary stream
            "streamId": stream_id,
        }
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_getLiveStreamInfo(self, device_id: str) -> dict:  # pylint: disable=invalid-name
        """Obtain the live broadcast address. \
            (https://open.imoulife.com/book/en/http/device/live/getLiveStreamInfo.html)."""
        # define the api endpoint
        api = "getLiveStreamInfo"
        # prepare the payload
        payload = {
            "deviceId": device_id,
            "channelId": "0",
        }
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_liveList(self) -> dict:  # pylint: disable=invalid-name
        """Get the live broadcast details list created under the developer's current account. \
            https://open.imoulife.com/book/en/http/device/live/liveList.html)."""
        # define the api endpoint
        api = "liveList"
        # prepare the payload
        payload = {
            "queryRange": "1-20",
        }
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_unbindLive(self, live_token: str) -> dict:  # pylint: disable=invalid-name
        """Delete the live broadcast address. \
            (https://open.imoulife.com/book/en/http/device/live/unbindLive.html)."""
        # define the api endpoint
        api = "unbindLive"
        # prepare the payload
        payload = {"liveToken": live_token}
        # call the api
        return await self._async_call_api(api, payload)

    async def async_api_getDevicePowerInfo(self, device_id: str) -> dict:  # pylint: disable=invalid-name
        """Obtain battery power information. \
            (https://open.imoulife.com/book/en/http/door/getDevicePowerInfo.html)."""
        # define the api endpoint
        api = "getDevicePowerInfo"
        # prepare the payload
        payload = {
            "deviceId": device_id,
        }
        # call the api
        return await self._async_call_api(api, payload)
