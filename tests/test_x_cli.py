"""Tests for `imouapi` package."""
import asyncio
import logging
import re

from aioresponses import aioresponses

from imouapi.cli import ImouCli

from .const import MOCK_RESPONSES

logger = logging.getLogger("imouapi")
logger.setLevel(logging.DEBUG)


class TestCli:
    """Test suite for ImouAPIClient."""

    def setup(self):
        """Initialize the test suite."""
        self.loop = asyncio.new_event_loop()  # pylint: disable=attribute-defined-outside-init
        self.cli = ImouCli()  # pylint: disable=attribute-defined-outside-init

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
        self.config_mock(mocked, "deviceBaseList", "deviceBaseList_ok", repeat=True)
        self.config_mock(mocked, "deviceBaseDetailList", "deviceBaseDetailList_ok", repeat=True)
        self.config_mock(mocked, "deviceOnline", "deviceOnline_ok", repeat=True)
        self.config_mock(mocked, "getAlarmMessage", "getAlarmMessage_ok", repeat=True)
        self.config_mock(mocked, "getDeviceCameraStatus", "getDeviceCameraStatus_ok", repeat=True)
        self.config_mock(mocked, "setDeviceCameraStatus", "setDeviceCameraStatus_ok", repeat=True)
        self.config_mock(mocked, "deviceStorage", "deviceStorage_ok", repeat=True)
        self.config_mock(mocked, "getNightVisionMode", "getNightVisionMode_ok", repeat=True)
        self.config_mock(mocked, "setNightVisionMode", "setNightVisionMode_ok", repeat=True)
        self.config_mock(mocked, "getMessageCallback", "getMessageCallback_ok", repeat=True)
        self.config_mock(mocked, "deviceSdcardStatus", "deviceSdcardStatus_ok", repeat=True)
        self.config_mock(mocked, "restartDevice", "restartDevice_ok", repeat=True)

    def test_discover_ok(self, capsys):
        """Test discover: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseList", "deviceBaseList_ok")
            self.config_mock(mocked, "deviceBaseDetailList", "deviceBaseDetailList_ok")
            self.cli.argv = ["cli", "--app-id", "app_id", "--app-secret", "app_secret", "discover"]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "1 devices" in captured.out

    def test_discover_no_app_id(self, capsys):
        """Test discover: no app id."""
        self.cli.argv = ["cli", "discover"]
        self.cli.parse_command_line()
        self.cli.run_command()
        captured = capsys.readouterr()
        assert "provide app_id and app_secret" in captured.out

    def test_get_device(self, capsys):
        """Test get device: ok."""
        with aioresponses() as mocked:
            self.configure_responses_ok(mocked)
            self.cli.argv = ["cli", "--app-id", "app_id", "--app-secret", "app_secret", "get_device", "device_id"]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "2.680.0000000.25.R.220527" in captured.out

    def test_get_switch(self, capsys):
        """Test get switch: ok."""
        with aioresponses() as mocked:
            self.configure_responses_ok(mocked)
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "get_switch",
                "device_id",
                "headerDetect",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "Human detection (headerDetect): True" in captured.out

    def test_set_switch(self, capsys):
        """Test set switch: ok."""
        with aioresponses() as mocked:
            self.configure_responses_ok(mocked)
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "set_switch",
                "device_id",
                "headerDetect",
                "on",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "Human detection (headerDetect): True" in captured.out

    def test_get_select(self, capsys):
        """Test get select: ok."""
        with aioresponses() as mocked:
            self.configure_responses_ok(mocked)
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "get_select",
                "device_id",
                "nightVisionMode",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "Intelligent" in captured.out

    def test_set_select(self, capsys):
        """Test set select: ok."""
        with aioresponses() as mocked:
            self.configure_responses_ok(mocked)
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "set_select",
                "device_id",
                "nightVisionMode",
                "Intelligent",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            assert True is True

    def test_get_sensor(self, capsys):
        """Test get sensor: ok."""
        with aioresponses() as mocked:
            self.configure_responses_ok(mocked)
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "get_sensor",
                "device_id",
                "storageUsed",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "storageUsed" in captured.out

    def test_get_binary_sensor(self, capsys):
        """Test get binary sensor: ok."""
        with aioresponses() as mocked:
            self.configure_responses_ok(mocked)
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "get_binary_sensor",
                "device_id",
                "online",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert " Online (online): True" in captured.out

    def test_press_button(self, capsys):
        """Test press button: ok."""
        with aioresponses() as mocked:
            self.configure_responses_ok(mocked)
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "press_button",
                "device_id",
                "restartDevice",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert captured.out == ""

    def test_get_siren(self, capsys):
        """Test get siren: ok."""
        with aioresponses() as mocked:
            self.configure_responses_ok(mocked)
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "get_siren",
                "device_id",
                "siren",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "Activate siren (siren)" in captured.out

    def test_set_siren(self, capsys):
        """Test set siren: ok."""
        with aioresponses() as mocked:
            self.configure_responses_ok(mocked)
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "set_siren",
                "device_id",
                "siren",
                "on",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "Activate siren (siren)" in captured.out

    def test_api_deviceBaseList(self, capsys):  # pylint: disable=invalid-name
        """Test api_deviceBaseList: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseList", "deviceBaseList_ok")
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "api_deviceBaseList",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "8L0DF93PAZ55FD2" in captured.out

    def test_api_deviceOpenList(self, capsys):  # pylint: disable=invalid-name
        """Test api_deviceOpenList: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceOpenList", "deviceOpenList_ok")
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "api_deviceOpenList",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "8L0DF93PAZ55FD2" in captured.out

    def test_api_deviceBaseDetailList(self, capsys):  # pylint: disable=invalid-name
        """Test api_deviceBaseDetailList: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseDetailList", "deviceBaseDetailList_ok")
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "api_deviceBaseDetailList",
                "device_id",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "8L0DF93PAZ55FD2" in captured.out

    def test_api_deviceOpenDetailList(self, capsys):  # pylint: disable=invalid-name
        """Test api_deviceOpenDetailList: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceOpenDetailList", "deviceOpenDetailList_ok")
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "api_deviceOpenDetailList",
                "device_id",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "8L0DF93PAZ55FD2" in captured.out

    def test_api_listDeviceAbility(self, capsys):  # pylint: disable=invalid-name
        """Test api_listDeviceAbility: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "listDeviceAbility", "listDeviceAbility_ok")
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "api_listDeviceAbility",
                "device_id",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "WLAN" in captured.out

    def test_api_getAlarmMessage(self, capsys):  # pylint: disable=invalid-name
        """Test api_getAlarmMessage: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "getAlarmMessage", "getAlarmMessage_ok")
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "api_getAlarmMessage",
                "device_id",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "human" in captured.out

    def test_api_deviceStorage(self, capsys):  # pylint: disable=invalid-name
        """Test api_deviceStorage: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceStorage", "deviceStorage_ok")
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "api_deviceStorage",
                "device_id",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "totalBytes" in captured.out

    def test_api_getDeviceCameraStatus(self, capsys):  # pylint: disable=invalid-name
        """Test api_getDeviceCameraStatus: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "getDeviceCameraStatus", "getDeviceCameraStatus_ok")
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "api_getDeviceCameraStatus",
                "device_id",
                "headerDetect",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "headerDetect" in captured.out

    def test_api_setDeviceCameraStatus(self, capsys):  # pylint: disable=invalid-name
        """Test api_setDeviceCameraStatus: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "setDeviceCameraStatus", "setDeviceCameraStatus_ok")
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "api_setDeviceCameraStatus",
                "device_id",
                "headerDetect",
                "on",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "{}" in captured.out

    def test_api_getNightVisionMode(self, capsys):  # pylint: disable=invalid-name
        """Test api_getNightVisionMode: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "getNightVisionMode", "getNightVisionMode_ok")
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "api_getNightVisionMode",
                "device_id",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "Intelligent" in captured.out

    def test_api_setNightVisionMode(self, capsys):  # pylint: disable=invalid-name
        """Test api_setNightVisionMode: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "setNightVisionMode", "setNightVisionMode_ok")
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "api_setNightVisionMode",
                "device_id",
                "Intelligent",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "{}" in captured.out

    def test_api_getMessageCallback(self, capsys):  # pylint: disable=invalid-name
        """Test api_getMessageCallback: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "getMessageCallback", "getMessageCallback_ok")
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "api_getMessageCallback",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "callbackUrl" in captured.out

    def test_api_setMessageCallbackOn(self, capsys):  # pylint: disable=invalid-name
        """Test api_setMessageCallbackOn: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "setMessageCallback", "setMessageCallbackOn_ok")
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "api_setMessageCallbackOn",
                "https://url.com",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "{}" in captured.out

    def test_api_setMessageCallbackOff(self, capsys):  # pylint: disable=invalid-name
        """Test api_setMessageCallbackOff: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "setMessageCallback", "setMessageCallbackOff_ok")
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "api_setMessageCallbackOff",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "{}" in captured.out

    def test_api_restartDevice(self, capsys):  # pylint: disable=invalid-name
        """Test api_restartDevice: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "restartDevice", "restartDevice_ok")
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "api_restartDevice",
                "device_id",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "{}" in captured.out

    def test_api_deviceSdcardStatus(self, capsys):  # pylint: disable=invalid-name
        """Test api_deviceSdcardStatus: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceSdcardStatus", "deviceSdcardStatus_ok")
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "api_deviceSdcardStatus",
                "device_id",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "normal" in captured.out
