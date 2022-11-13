"""Tests for `imouapi` package."""
import asyncio
import logging
import re

import aiohttp
import pytest
from aiohttp.http_exceptions import HttpProcessingError
from aioresponses import aioresponses

from imouapi.api import ImouAPIClient

from .const import MOCK_RESPONSES

logger = logging.getLogger("imouapi")
logger.setLevel(logging.DEBUG)


class TestApiClient:
    """Test suite for ImouAPIClient."""

    def setup(self):
        """Initialize the test suite."""
        self.loop = asyncio.new_event_loop()  # pylint: disable=attribute-defined-outside-init
        self.session = aiohttp.ClientSession()  # pylint: disable=attribute-defined-outside-init
        self.api_client = ImouAPIClient(  # pylint: disable=attribute-defined-outside-init
            "appId", "appSecret", self.session
        )
        self.api_client.set_log_http_requests(True)

    def config_mock(self, mocked, url: str, response: str, **kwargs):
        """Configure a mock request."""
        status = kwargs["status"] if "status" in kwargs else 200
        exception = kwargs["exception"] if "exception" in kwargs else None
        repeat = kwargs["repeat"] if "repeat" in kwargs else False
        payload = MOCK_RESPONSES[response] if response in MOCK_RESPONSES else "{invalid"
        mocked.post(re.compile(r".+/" + url + "$"), status=status, payload=payload, exception=exception, repeat=repeat)

    def test_accessToken_ok(self):  # pylint: disable=invalid-name
        """Test accessToken: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            connected = self.loop.run_until_complete(self.api_client.async_connect())
            assert connected is True

    def test_accessToken_wrong_app_id(self):  # pylint: disable=invalid-name
        """Test accessToken: wrong app id."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_wrong_app_id")
            with pytest.raises(Exception) as exception:
                self.loop.run_until_complete(self.api_client.async_connect())
            assert "InvalidConfiguration" in str(exception) and "OP1008" in str(exception)

    def test_accessToken_wrong_status_code(self):  # pylint: disable=invalid-name
        """Test accessToken: wrong status code."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok", status=500)
            with pytest.raises(Exception) as exception:
                self.loop.run_until_complete(self.api_client.async_connect())
            assert "APIError('status code 500')" in str(exception)

    def test_accessToken_invalid_response_1(self):  # pylint: disable=invalid-name
        """Test accessToken: invalid response."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_invalid_response_1")
            with pytest.raises(Exception) as exception:
                self.loop.run_until_complete(self.api_client.async_connect())
            assert "InvalidResponse" in str(exception) and "accessToken not found" in str(exception)

    def test_accessToken_invalid_response_2(self):  # pylint: disable=invalid-name
        """Test accessToken: invalid response."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_invalid_response_2")
            with pytest.raises(Exception) as exception:
                self.loop.run_until_complete(self.api_client.async_connect())
            assert "InvalidResponse" in str(exception) and "cannot find" in str(exception)

    def test_accessToken_http_error(self):  # pylint: disable=invalid-name
        """Test accessToken: http error."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok", exception=HttpProcessingError())
            with pytest.raises(Exception) as exception:
                self.loop.run_until_complete(self.api_client.async_connect())
            assert "ConnectionFailed" in str(exception)

    def test_accessToken_expired(self):  # pylint: disable=invalid-name
        """Test accessToken: expired."""
        with aioresponses() as mocked:
            # authenticate and get the status
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "getDeviceCameraStatus", "getDeviceCameraStatus_ok")
            data = self.loop.run_until_complete(
                self.api_client.async_api_getDeviceCameraStatus("8L0DF93PAZ55FD2", "headerDetect")
            )
            assert data["status"] == "on"
            # request the status again and get back a token expired error
            self.config_mock(mocked, "getDeviceCameraStatus", "accessToken_expired")
            # retry and get a new token
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            # get the status back again
            self.config_mock(mocked, "getDeviceCameraStatus", "getDeviceCameraStatus_ok")
            data = self.loop.run_until_complete(
                self.api_client.async_api_getDeviceCameraStatus("8L0DF93PAZ55FD2", "headerDetect")
            )
            assert data["status"] == "on"

    def test_deviceBaseList_ok(self):  # pylint: disable=invalid-name
        """Test deviceBaseList: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseList", "deviceBaseList_ok")
            data = self.loop.run_until_complete(self.api_client.async_api_deviceBaseList())
            assert data["deviceList"][0]["deviceId"] == "8L0DF93PAZ55FD2"

    def test_deviceBaseList_wrong_device_id(self):  # pylint: disable=invalid-name
        """Test deviceBaseList: wrong device id."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseList", "deviceBaseList_wrong_device_id")
            with pytest.raises(Exception) as exception:
                self.loop.run_until_complete(self.api_client.async_api_deviceBaseList())
            assert "NotAuthorized" in str(exception) and "OP1009" in str(exception)

    def test_deviceOpenList_ok(self):  # pylint: disable=invalid-name
        """Test deviceOpenList: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceOpenList", "deviceOpenList_ok")
            data = self.loop.run_until_complete(self.api_client.async_api_deviceOpenList())
            assert data["deviceList"][0]["deviceId"] == "8L0DF93PAZ55FD2"

    def test_deviceBaseDetailList_ok(self):  # pylint: disable=invalid-name
        """Test deviceBaseDetailList: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseDetailList", "deviceBaseDetailList_ok")
            data = self.loop.run_until_complete(self.api_client.async_api_deviceBaseDetailList(["8L0DF93PAZ55FD2"]))
            assert data["deviceList"][0]["deviceModel"] == "IPC-C22C"

    def test_deviceOpenDetailList_ok(self):  # pylint: disable=invalid-name
        """Test deviceOpenDetailList: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceOpenDetailList", "deviceOpenDetailList_ok")
            data = self.loop.run_until_complete(self.api_client.async_api_deviceOpenDetailList(["8L0DF93PAZ55FD2"]))
            assert data["deviceList"][0]["deviceModel"] == "IPC-C22C"

    def test_deviceOnline_ok(self):  # pylint: disable=invalid-name
        """Test deviceOnline: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceOnline", "deviceOnline_ok")
            data = self.loop.run_until_complete(self.api_client.async_api_deviceOnline("8L0DF93PAZ55FD2"))
            assert data["onLine"] == "1"

    def test_getDeviceCameraStatus_ok(self):  # pylint: disable=invalid-name
        """Test getDeviceCameraStatus: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "getDeviceCameraStatus", "getDeviceCameraStatus_ok")
            data = self.loop.run_until_complete(
                self.api_client.async_api_getDeviceCameraStatus("8L0DF93PAZ55FD2", "headerDetect")
            )
            assert data["status"] == "on"

    def test_setDeviceCameraStatus_ok(self):  # pylint: disable=invalid-name
        """Test setDeviceCameraStatus: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "setDeviceCameraStatus", "setDeviceCameraStatus_ok")
            self.loop.run_until_complete(
                self.api_client.async_api_setDeviceCameraStatus("8L0DF93PAZ55FD2", "headerDetect", True)
            )
            assert True is True

    def test_getAlarmMessage_ok(self):  # pylint: disable=invalid-name
        """Test getAlarmMessage: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "getAlarmMessage", "getAlarmMessage_ok")
            data = self.loop.run_until_complete(self.api_client.async_api_getAlarmMessage("8L0DF93PAZ55FD2"))
            assert data["alarms"][0]["msgType"] == "human"

    def test_listDeviceAbility_ok(self):  # pylint: disable=invalid-name
        """Test listDeviceAbility: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "listDeviceAbility", "listDeviceAbility_ok")
            data = self.loop.run_until_complete(self.api_client.async_api_listDeviceAbility("8L0DF93PAZ55FD2"))
            assert data["deviceList"][0]["deviceId"] == "8L0DF93PAZ55FD2"

    def test_deviceStorage_ok(self):  # pylint: disable=invalid-name
        """Test deviceStorage: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceStorage", "deviceStorage_ok")
            data = self.loop.run_until_complete(self.api_client.async_api_deviceStorage("8L0DF93PAZ55FD2"))
            assert data["totalBytes"] == 31254904832

    def test_getNightVisionMode_ok(self):  # pylint: disable=invalid-name
        """Test getNightVisionMode: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "getNightVisionMode", "getNightVisionMode_ok")
            data = self.loop.run_until_complete(self.api_client.async_api_getNightVisionMode("8L0DF93PAZ55FD2"))
            assert data["mode"] == "Intelligent"

    def test_setNightVisionMode_ok(self):  # pylint: disable=invalid-name
        """Test setNightVisionMode: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "setNightVisionMode", "setNightVisionMode_ok")
            self.loop.run_until_complete(self.api_client.async_api_setNightVisionMode("8L0DF93PAZ55FD2", "Intelligent"))
            assert True is True

    def test_getMessageCallback_ok(self):  # pylint: disable=invalid-name
        """Test getMessageCallback: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "getMessageCallback", "getMessageCallback_ok")
            data = self.loop.run_until_complete(self.api_client.async_api_getMessageCallback())
            assert data["status"] == "off"

    def test_setMessageCallbackOn_ok(self):  # pylint: disable=invalid-name
        """Test setMessageCallbackOn: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "setMessageCallback", "setMessageCallbackOn_ok")
            self.loop.run_until_complete(self.api_client.async_api_setMessageCallbackOn("https://url.com"))
            assert True is True

    def test_setMessageCallbackOff_ok(self):  # pylint: disable=invalid-name
        """Test setMessageCallbackOff: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "setMessageCallback", "setMessageCallbackOff_ok")
            self.loop.run_until_complete(self.api_client.async_api_setMessageCallbackOff())
            assert True is True

    def test_restartDevice_ok(self):  # pylint: disable=invalid-name
        """Test restartDevice: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "restartDevice", "restartDevice_ok")
            self.loop.run_until_complete(self.api_client.async_api_restartDevice("device_id"))
            assert True is True

    def test_deviceSdcardStatus_ok(self):  # pylint: disable=invalid-name
        """Test deviceSdcardStatus: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceSdcardStatus", "deviceSdcardStatus_ok")
            data = self.loop.run_until_complete(self.api_client.async_api_deviceSdcardStatus("device_id"))
            assert data["status"] == "normal"
