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
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseList", "deviceBaseList_ok")
            self.config_mock(mocked, "deviceBaseDetailList", "deviceBaseDetailList_ok")
            self.config_mock(mocked, "deviceOnline", "deviceOnline_ok", repeat=True)
            self.config_mock(mocked, "getAlarmMessage", "getAlarmMessage_ok")
            self.config_mock(mocked, "getDeviceCameraStatus", "getDeviceCameraStatus_ok", repeat=True)
            self.cli.argv = ["cli", "--app-id", "app_id", "--app-secret", "app_secret", "get_device", "device_id"]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "2.680.0000000.25.R.220527" in captured.out

    def test_get_switch(self, capsys):
        """Test get switch: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseList", "deviceBaseList_ok")
            self.config_mock(mocked, "deviceBaseDetailList", "deviceBaseDetailList_ok")
            self.config_mock(mocked, "deviceOnline", "deviceOnline_ok", repeat=True)
            self.config_mock(mocked, "getAlarmMessage", "getAlarmMessage_ok")
            self.config_mock(mocked, "getDeviceCameraStatus", "getDeviceCameraStatus_ok", repeat=True)
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
            assert "Head Detection (headerDetect): True" in captured.out

    def test_set_switch(self, capsys):
        """Test set switch: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseList", "deviceBaseList_ok")
            self.config_mock(mocked, "deviceBaseDetailList", "deviceBaseDetailList_ok", repeat=True)
            self.config_mock(mocked, "deviceOnline", "deviceOnline_ok", repeat=True)
            self.config_mock(mocked, "getAlarmMessage", "getAlarmMessage_ok", repeat=True)
            self.config_mock(mocked, "getDeviceCameraStatus", "getDeviceCameraStatus_ok", repeat=True)
            self.config_mock(mocked, "setDeviceCameraStatus", "setDeviceCameraStatus_ok", repeat=True)
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
            assert "Head Detection (headerDetect): True" in captured.out

    def test_get_sensor(self, capsys):
        """Test get sensor: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseList", "deviceBaseList_ok")
            self.config_mock(mocked, "deviceBaseDetailList", "deviceBaseDetailList_ok")
            self.config_mock(mocked, "deviceOnline", "deviceOnline_ok", repeat=True)
            self.config_mock(mocked, "getAlarmMessage", "getAlarmMessage_ok")
            self.config_mock(mocked, "getDeviceCameraStatus", "getDeviceCameraStatus_ok", repeat=True)
            self.cli.argv = [
                "cli",
                "--app-id",
                "app_id",
                "--app-secret",
                "app_secret",
                "get_sensor",
                "device_id",
                "lastAlarm",
            ]
            self.cli.parse_command_line()
            self.cli.run_command()
            captured = capsys.readouterr()
            assert "2022-09-25T17:36:33" in captured.out

    def test_get_binary_sensor(self, capsys):
        """Test get binary sensor: ok."""
        with aioresponses() as mocked:
            self.config_mock(mocked, "accessToken", "accessToken_ok")
            self.config_mock(mocked, "deviceBaseList", "deviceBaseList_ok")
            self.config_mock(mocked, "deviceBaseDetailList", "deviceBaseDetailList_ok")
            self.config_mock(mocked, "deviceOnline", "deviceOnline_ok", repeat=True)
            self.config_mock(mocked, "getAlarmMessage", "getAlarmMessage_ok")
            self.config_mock(mocked, "getDeviceCameraStatus", "getDeviceCameraStatus_ok", repeat=True)
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
