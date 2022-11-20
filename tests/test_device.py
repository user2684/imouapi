"""Tests for `imouapi` package."""
import asyncio
import logging
import re

import aiohttp
import pytest
from aiohttp.http_exceptions import HttpProcessingError
from aioresponses import aioresponses

from imouapi.api import ImouAPIClient
from imouapi.device import ImouDevice, ImouDiscoverService

from .const import MOCK_RESPONSES

logger = logging.getLogger("imouapi")
logger.setLevel(logging.DEBUG)


class TestDevice:
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

    def configure_responses_ok(self, mocked):
        """Configure all responses ok."""
        self.config_mock(mocked, "accessToken", "accessToken_ok", repeat=True)
        self.config_mock(mocked, "deviceBaseDetailList", "deviceBaseDetailList_ok", repeat=True)
        self.config_mock(mocked, "deviceOnline", "deviceOnline_ok", repeat=True)
        self.config_mock(mocked, "getAlarmMessage", "getAlarmMessage_ok", repeat=True)
        self.config_mock(mocked, "getDeviceCameraStatus", "getDeviceCameraStatus_ok", repeat=True)
        self.config_mock(mocked, "deviceStorage", "deviceStorage_ok", repeat=True)
        self.config_mock(mocked, "getNightVisionMode", "getNightVisionMode_ok", repeat=True)
        self.config_mock(mocked, "getNightVisionMode", "getNightVisionMode_ok", repeat=True)
        self.config_mock(mocked, "getMessageCallback", "getMessageCallback_ok", repeat=True)
        self.config_mock(mocked, "getDeviceCameraStatus", "getDeviceCameraStatus_ok", repeat=True)
        self.config_mock(mocked, "deviceSdcardStatus", "deviceSdcardStatus_ok", repeat=True)

    def test_discover_ok(self):
        """Test ImouDiscoverService: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseList", "deviceBaseList_ok")
            self.config_mock(mocked, "deviceBaseDetailList", "deviceBaseDetailList_ok")
            discover_service = ImouDiscoverService(self.api_client)
            discovered_devices = self.loop.run_until_complete(discover_service.async_discover_devices())
            device: ImouDevice = discovered_devices["webcam"]
            assert device.get_device_id() == "8L0DF93PAZ55FD2"

    def test_discover_malformed_response(self):
        """Test ImouDiscoverService: malformed response."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseList", "deviceBaseList_malformed")
            self.config_mock(mocked, "deviceBaseDetailList", "deviceBaseDetailList_ok")
            discover_service = ImouDiscoverService(self.api_client)
            with pytest.raises(Exception) as exception:
                self.loop.run_until_complete(discover_service.async_discover_devices())
            assert "InvalidResponse" in str(exception) and "not found in" in str(exception)

    def test_get_device_ok(self):
        """Test get device: ok."""
        with aioresponses() as mocked:
            self.configure_responses_ok(mocked)
            device = ImouDevice(self.api_client, "8L0DF93PAZ55FD2")
            self.loop.run_until_complete(device.async_initialize())
            assert device.get_device_id() == "8L0DF93PAZ55FD2"
            assert device.get_firmware() == "2.680.0000000.25.R.220527"
            assert device.is_online() is True
            self.loop.run_until_complete(device.async_get_data())
            assert device.get_sensor_by_name("online").is_on() is True
            assert device.get_sensor_by_name("breathingLight").is_on() is True
            assert device.get_sensor_by_name("localRecord").is_on() is True

    def test_get_device_processing_error(self):
        """Test get device: processing error."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseDetailList", "deviceBaseDetailList_ok", exception=HttpProcessingError())
            device = ImouDevice(self.api_client, "8L0DF93PAZ55FD2")
            with pytest.raises(Exception) as exception:
                self.loop.run_until_complete(device.async_initialize())
            assert "ConnectionFailed" in str(exception)

    def test_get_device_missing_data(self):
        """Test get device: missing data."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseDetailList", "deviceBaseDetailList_missing_data")
            device = ImouDevice(self.api_client, "8L0DF93PAZ55FD2")
            with pytest.raises(Exception) as exception:
                self.loop.run_until_complete(device.async_initialize())
            assert "InvalidResponse" in str(exception) and "missing parameter" in str(exception)

    def test_get_sensor_uknown(self):
        """Test get sensor: unknown."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseDetailList", "deviceBaseDetailList_ok")
            device = ImouDevice(self.api_client, "8L0DF93PAZ55FD2")
            self.loop.run_until_complete(device.async_initialize())
            sensor = device.get_sensor_by_name("unknown")
            assert sensor is None

    def test_get_online_malformed(self):
        """Test get alarm message: malformed."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseDetailList", "deviceBaseDetailList_ok")
            device = ImouDevice(self.api_client, "8L0DF93PAZ55FD2")
            self.loop.run_until_complete(device.async_initialize())
            self.config_mock(mocked, "deviceOnline", "deviceOnline_malformed")
            self.config_mock(mocked, "getAlarmMessage", "getAlarmMessage_ok")
            self.config_mock(mocked, "getDeviceCameraStatus", "getDeviceCameraStatus_ok", repeat=True)
            self.config_mock(mocked, "getMessageCallback", "getMessageCallback_ok", repeat=True)
            with pytest.raises(Exception) as exception:
                self.loop.run_until_complete(device.async_get_data())
            assert "InvalidResponse" in str(exception) and "onLine not found" in str(exception)

    def test_set_status_ok(self):
        """Test set status: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseDetailList", "deviceBaseDetailList_ok")
            device = ImouDevice(self.api_client, "8L0DF93PAZ55FD2")
            self.loop.run_until_complete(device.async_initialize())
            self.config_mock(mocked, "deviceOnline", "deviceOnline_ok", repeat=True)
            self.config_mock(mocked, "getAlarmMessage", "getAlarmMessage_ok")
            self.config_mock(mocked, "getDeviceCameraStatus", "getDeviceCameraStatus_ok", repeat=True)
            self.config_mock(mocked, "setDeviceCameraStatus", "setDeviceCameraStatus_ok", repeat=True)
            self.config_mock(mocked, "deviceStorage", "deviceStorage_ok")
            self.config_mock(mocked, "getMessageCallback", "getMessageCallback_ok", repeat=True)
            self.config_mock(mocked, "getNightVisionMode", "getNightVisionMode_ok", repeat=True)
            self.config_mock(mocked, "deviceSdcardStatus", "deviceSdcardStatus_ok")
            self.loop.run_until_complete(device.async_get_data())
            set_switch = device.get_sensor_by_name("headerDetect")
            self.loop.run_until_complete(set_switch.async_turn_on())
            assert set_switch.is_on() is True
            self.loop.run_until_complete(set_switch.async_turn_off())
            assert set_switch.is_on() is False
            self.loop.run_until_complete(set_switch.async_toggle())
            assert set_switch.is_on() is True

    def test_set_status_error(self):
        """Test set status: error."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseDetailList", "deviceBaseDetailList_ok")
            device = ImouDevice(self.api_client, "8L0DF93PAZ55FD2")
            self.loop.run_until_complete(device.async_initialize())
            self.config_mock(mocked, "deviceOnline", "deviceOnline_ok", repeat=True)
            self.config_mock(mocked, "getAlarmMessage", "getAlarmMessage_ok")
            self.config_mock(mocked, "getDeviceCameraStatus", "getDeviceCameraStatus_ok", repeat=True)
            self.config_mock(mocked, "setDeviceCameraStatus", "setDeviceCameraStatus_error")
            self.config_mock(mocked, "deviceStorage", "deviceStorage_ok")
            self.config_mock(mocked, "getNightVisionMode", "getNightVisionMode_ok")
            self.config_mock(mocked, "getMessageCallback", "getMessageCallback_ok", repeat=True)
            self.config_mock(mocked, "deviceSdcardStatus", "deviceSdcardStatus_ok")
            self.loop.run_until_complete(device.async_get_data())
            set_switch = device.get_sensor_by_name("headerDetect")
            with pytest.raises(Exception) as exception:
                self.loop.run_until_complete(set_switch.async_turn_on())
            assert "APIError" in str(exception)

    def test_press_button_ok(self):
        """Test press button: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseDetailList", "deviceBaseDetailList_ok")
            device = ImouDevice(self.api_client, "8L0DF93PAZ55FD2")
            self.loop.run_until_complete(device.async_initialize())
            self.config_mock(mocked, "deviceOnline", "deviceOnline_ok", repeat=True)
            self.config_mock(mocked, "getAlarmMessage", "getAlarmMessage_ok")
            self.config_mock(mocked, "getDeviceCameraStatus", "getDeviceCameraStatus_ok", repeat=True)
            self.config_mock(mocked, "setDeviceCameraStatus", "setDeviceCameraStatus_error")
            self.config_mock(mocked, "deviceStorage", "deviceStorage_ok")
            self.config_mock(mocked, "getNightVisionMode", "getNightVisionMode_ok")
            self.config_mock(mocked, "getMessageCallback", "getMessageCallback_ok", repeat=True)
            self.config_mock(mocked, "restartDevice", "restartDevice_ok")
            self.config_mock(mocked, "deviceSdcardStatus", "deviceSdcardStatus_ok")
            self.loop.run_until_complete(device.async_get_data())
            button = device.get_sensor_by_name("restartDevice")
            self.loop.run_until_complete(button.async_press())
            assert True is True

    def test_siren_ok(self):
        """Test siren: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseDetailList", "deviceBaseDetailList_ok")
            device = ImouDevice(self.api_client, "8L0DF93PAZ55FD2")
            self.loop.run_until_complete(device.async_initialize())
            self.config_mock(mocked, "deviceOnline", "deviceOnline_ok", repeat=True)
            self.config_mock(mocked, "getAlarmMessage", "getAlarmMessage_ok")
            self.config_mock(mocked, "getDeviceCameraStatus", "getDeviceCameraStatus_ok", repeat=True)
            self.config_mock(mocked, "setDeviceCameraStatus", "setDeviceCameraStatus_ok", repeat=True)
            self.config_mock(mocked, "deviceStorage", "deviceStorage_ok")
            self.config_mock(mocked, "getNightVisionMode", "getNightVisionMode_ok")
            self.config_mock(mocked, "getMessageCallback", "getMessageCallback_ok", repeat=True)
            self.config_mock(mocked, "restartDevice", "restartDevice_ok")
            self.config_mock(mocked, "deviceSdcardStatus", "deviceSdcardStatus_ok")
            self.loop.run_until_complete(device.async_get_data())
            siren = device.get_sensor_by_name("siren")
            self.loop.run_until_complete(siren.async_turn_on())
            assert siren.is_on() is True
            self.loop.run_until_complete(siren.async_turn_off())
            assert siren.is_on() is False
