"""Console script for imouapi."""
import asyncio
import json
import logging
import re
import sys

import aiohttp

from .api import ImouAPIClient
from .const import IMOU_CAPABILITIES, IMOU_SWITCHES
from .device import ImouDevice, ImouDiscoverService
from .device_entity import ImouBinarySensor, ImouButton, ImouCamera, ImouSelect, ImouSensor, ImouSiren, ImouSwitch
from .exceptions import ImouException


async def async_run_command(command: str, api_client: ImouAPIClient, args: list[str]):  # noqa: C901
    """Run a command."""
    session = aiohttp.ClientSession()
    api_client.set_session(session)
    try:
        if command == "discover":
            discover_service = ImouDiscoverService(api_client)
            discovered_devices = await discover_service.async_discover_devices()
            print(f"Discovered {len(discovered_devices)} devices:")
            for device_name, device in discovered_devices.items():
                print(f"- {device_name}:")
                print(f"  - Model: {device.get_model()}")
                print(f"  - Device ID: {device.get_device_id()}")
                print(f"  - Firmware: {device.get_firmware()}")
                print(f"  - Sleepable: {device.get_sleepable()}")

        elif command in [
            "get_device",
            "get_sensor",
            "get_binary_sensor",
            "get_switch",
            "set_switch",
            "get_select",
            "set_select",
            "press_button",
            "get_siren",
            "set_siren",
            "get_diagnostics",
            "get_camera_image",
            "get_camera_stream",
        ]:
            device_id = args[0]
            device = ImouDevice(api_client, device_id)
            await device.async_initialize()
            await device.async_get_data()

            if command == "get_device":
                print(device.dump())

            elif command == "get_sensor":
                sensor_name = args[1]
                print(f"- {device.get_name()}:")
                sensor: ImouSensor = device.get_sensor_by_name(sensor_name)
                if sensor is not None:
                    print(f"  - {sensor.get_description()} ({sensor.get_name()}): {sensor.get_state()}")
                else:
                    print(f"sensor {sensor_name} not found")

            elif command == "get_binary_sensor":
                sensor_name = args[1]
                print(f"- {device.get_name()}:")
                binary_sensor: ImouBinarySensor = device.get_sensor_by_name(sensor_name)
                if binary_sensor is not None:
                    print(
                        f"  - {binary_sensor.get_description()} ({binary_sensor.get_name()}): {binary_sensor.is_on()}"
                    )
                else:
                    print(f"sensor {sensor_name} not found")

            elif command == "get_switch":
                sensor_name = args[1]
                print(f"- {device.get_name()}:")
                get_switch: ImouSwitch = device.get_sensor_by_name(sensor_name)
                if get_switch is not None:
                    print(f"  - {get_switch.get_description()} ({get_switch.get_name()}): {get_switch.is_on()}")
                else:
                    print(f"sensor {sensor_name} not found")

            elif command == "set_switch":
                sensor_name = args[1]
                value = args[2].upper()
                set_switch: ImouSwitch = device.get_sensor_by_name(sensor_name)  # type: ignore
                if set_switch is not None:
                    if value == "ON":
                        await set_switch.async_turn_on()
                    elif value == "OFF":
                        await set_switch.async_turn_off()
                    elif value == "TOGGLE":
                        await set_switch.async_toggle()
                    await async_run_command("get_switch", api_client, [device_id, sensor_name])
                else:
                    print(f"sensor {sensor_name} not found")

            elif command == "get_select":
                sensor_name = args[1]
                print(f"- {device.get_name()}:")
                get_select: ImouSelect = device.get_sensor_by_name(sensor_name)
                if get_select is not None:
                    print(
                        f"  - {get_select.get_description()} ({get_select.get_name()}): {get_select.get_current_option()} ({get_select.get_available_options()})"  # noqa: E501
                    )
                else:
                    print(f"sensor {sensor_name} not found")

            elif command == "set_select":
                sensor_name = args[1]
                value = args[2]
                set_select: ImouSelect = device.get_sensor_by_name(sensor_name)  # type: ignore
                if set_select is not None:
                    await set_select.async_select_option(value)
                else:
                    print(f"sensor {sensor_name} not found")

            elif command == "get_siren":
                sensor_name = args[1]
                print(f"- {device.get_name()}:")
                get_siren: ImouSiren = device.get_sensor_by_name(sensor_name)
                if get_siren is not None:
                    print(f"  - {get_siren.get_description()} ({get_siren.get_name()}): {get_siren.is_on()}")
                else:
                    print(f"sensor {sensor_name} not found")

            elif command == "set_siren":
                sensor_name = args[1]
                value = args[2].upper()
                set_siren: ImouSwitch = device.get_sensor_by_name(sensor_name)  # type: ignore
                if set_siren is not None:
                    if value == "ON":
                        await set_siren.async_turn_on()
                    elif value == "OFF":
                        await set_siren.async_turn_off()
                    await async_run_command("get_siren", api_client, [device_id, sensor_name])
                else:
                    print(f"sensor {sensor_name} not found")

            elif command == "press_button":
                sensor_name = args[1]
                button: ImouButton = device.get_sensor_by_name(sensor_name)  # type: ignore
                if button is not None:
                    await button.async_press()
                else:
                    print(f"sensor {sensor_name} not found")

            elif command == "get_diagnostics":
                print(device.get_diagnostics())

            elif command == "get_camera_image":
                sensor_name = args[1]
                camera: ImouCamera = device.get_sensor_by_name(sensor_name)  # type: ignore
                if camera is not None:
                    print(await camera.async_get_image())
                else:
                    print(f"sensor {sensor_name} not found")

            elif command == "get_camera_stream":
                sensor_name = args[1]
                camera: ImouCamera = device.get_sensor_by_name(sensor_name)  # type: ignore
                if camera is not None:
                    print(await camera.async_get_stream_url())
                else:
                    print(f"sensor {sensor_name} not found")

        elif command == "get_device_raw":
            device_id = args[0]
            capabilities_to_test = list(IMOU_CAPABILITIES.keys())
            print("Capabilities:")
            for capability in capabilities_to_test:
                capability = re.sub("v\\d$", "", capability, flags=re.IGNORECASE)
                data = await api_client.async_api_getDeviceCameraStatus(device_id, capability)
                print(f"{capability}: {data['status']}")
            print("\nSwitches:")
            switches_to_test = list(IMOU_SWITCHES.keys())
            for switch in switches_to_test:
                data = await api_client.async_api_getDeviceCameraStatus(device_id, switch)
                print(f"{switch}: {data['status']}")

        elif command == "api_deviceBaseList":
            data = await api_client.async_api_deviceBaseList()
            print(json.dumps(data, indent=4))

        elif command == "api_deviceOpenList":
            data = await api_client.async_api_deviceOpenList()
            print(json.dumps(data, indent=4))

        elif command == "api_deviceBaseDetailList":
            device_id = args[0]
            data = await api_client.async_api_deviceBaseDetailList([device_id])
            print(json.dumps(data, indent=4))

        elif command == "api_deviceOpenDetailList":
            device_id = args[0]
            data = await api_client.async_api_deviceOpenDetailList([device_id])
            print(json.dumps(data, indent=4))

        elif command == "api_listDeviceAbility":
            device_id = args[0]
            data = await api_client.async_api_listDeviceAbility([device_id])
            print(json.dumps(data, indent=4))

        elif command == "api_getAlarmMessage":
            device_id = args[0]
            data = await api_client.async_api_getAlarmMessage(device_id)
            print(json.dumps(data, indent=4))

        elif command == "api_deviceStorage":
            device_id = args[0]
            data = await api_client.async_api_deviceStorage(device_id)
            print(json.dumps(data, indent=4))

        elif command == "api_setDeviceCameraStatus":
            device_id = args[0]
            sensor_name = args[1]
            value_to_set = args[2] == "on"
            data = await api_client.async_api_setDeviceCameraStatus(device_id, sensor_name, value_to_set)
            print(json.dumps(data, indent=4))

        elif command == "api_getDeviceCameraStatus":
            device_id = args[0]
            sensor_name = args[1]
            data = await api_client.async_api_getDeviceCameraStatus(device_id, sensor_name)
            print(json.dumps(data, indent=4))

        elif command == "api_getNightVisionMode":
            device_id = args[0]
            data = await api_client.async_api_getNightVisionMode(device_id)
            print(json.dumps(data, indent=4))

        elif command == "api_setNightVisionMode":
            device_id = args[0]
            mode = args[1]
            data = await api_client.async_api_setNightVisionMode(device_id, mode)
            print(json.dumps(data, indent=4))

        elif command == "api_getMessageCallback":
            data = await api_client.async_api_getMessageCallback()
            print(json.dumps(data, indent=4))

        elif command == "api_setMessageCallbackOn":
            url = args[0]
            data = await api_client.async_api_setMessageCallbackOn(url)
            print(json.dumps(data, indent=4))

        elif command == "api_setMessageCallbackOff":
            data = await api_client.async_api_setMessageCallbackOff()
            print(json.dumps(data, indent=4))

        elif command == "api_restartDevice":
            device_id = args[0]
            data = await api_client.async_api_restartDevice(device_id)
            print(json.dumps(data, indent=4))

        elif command == "api_deviceSdcardStatus":
            device_id = args[0]
            data = await api_client.async_api_deviceSdcardStatus(device_id)
            print(json.dumps(data, indent=4))

        elif command == "api_devicePTZInfo":
            device_id = args[0]
            data = await api_client.async_api_devicePTZInfo(device_id)
            print(json.dumps(data, indent=4))

        elif command == "api_controlLocationPTZ":
            device_id = args[0]
            horizontal = float(args[1])
            vertical = float(args[2])
            zoom = float(args[3])
            data = await api_client.async_api_controlLocationPTZ(device_id, horizontal, vertical, zoom)
            print(json.dumps(data, indent=4))

        elif command == "api_controlMovePTZ":
            device_id = args[0]
            operation = args[1]
            duration = int(args[2])
            data = await api_client.async_api_controlMovePTZ(device_id, operation, duration)
            print(json.dumps(data, indent=4))

        elif command == "api_setDeviceSnapEnhanced":
            device_id = args[0]
            data = await api_client.async_api_setDeviceSnapEnhanced(device_id)
            print(json.dumps(data, indent=4))

        elif command == "api_bindDeviceLive":
            device_id = args[0]
            profile = args[1]
            data = await api_client.async_api_bindDeviceLive(device_id, profile)
            print(json.dumps(data, indent=4))

        elif command == "api_getLiveStreamInfo":
            device_id = args[0]
            data = await api_client.async_api_getLiveStreamInfo(device_id)
            print(json.dumps(data, indent=4))

        elif command == "api_liveList":
            data = await api_client.async_api_liveList()
            print(json.dumps(data, indent=4))

        elif command == "api_unbindLive":
            live_token = args[0]
            data = await api_client.async_api_unbindLive(live_token)
            print(json.dumps(data, indent=4))

        elif command == "api_getDevicePowerInfo":
            device_id = args[0]
            data = await api_client.async_api_getDevicePowerInfo(device_id)
            print(json.dumps(data, indent=4))

        else:
            print("invalid command provided")

    except ImouException as exception:
        print(exception.to_string())
    await session.close()


class ImouCli:
    """CLI class."""

    def __init__(self):
        """Initialize."""
        self.app_id = None
        self.app_secret = None
        self.base_url = None
        self.timeout = None
        self.logging = "INFO"
        self.log_http_requests = None
        self.device_id = None
        self.command = None
        self.loggingconfig = {
            'level': 'INFO',
            'format': '%(asctime)s %(levelname)s <%(name)s %(module)s %(funcName)s> %(message)s',
            'datefmt': '%a, %d %b %Y %H:%M:%S',
        }
        self.args = []
        self.argv = None

    def parse_command_line(self):
        """Parse command line arguments."""
        skip_next = False
        self.argv = sys.argv if self.argv is None else self.argv
        for i in range(1, len(self.argv)):
            if skip_next:
                skip_next = False
                continue
            arg = self.argv[i]
            arg = re.sub(' +', ' ', arg)
            if arg == "--app-id":
                self.app_id = self.argv[i + 1]
                skip_next = True
                continue
            if arg == "--app-secret":
                self.app_secret = self.argv[i + 1]
                skip_next = True
                continue
            if arg == "--base-url":
                self.base_url = self.argv[i + 1]
                skip_next = True
                continue
            if arg == "--timeout":
                self.timeout = self.argv[i + 1]
                skip_next = True
                continue
            if arg == "--log-http-requests":
                self.log_http_requests = True if self.argv[i + 1] == "on" else False
                skip_next = True
                continue
            if arg == "--logging":
                self.logging = self.argv[i + 1]
                self.loggingconfig["level"] = self.logging.upper()
                logging.basicConfig(**self.loggingconfig)  # type: ignore
                skip_next = True
                continue
            if self.command is None:
                self.command = arg
                continue
            self.args.append(arg)

    def run_command(self):  # noqa: C901
        """Run the requested command."""
        # ensure app id and app secret are provided
        if self.app_id is None or self.app_secret is None:
            print("ERROR: provide app_id and app_secret")
            print("")
            self.print_usage()

        # instantiate an api client
        api_client = ImouAPIClient(self.app_id, self.app_secret, None)
        if self.base_url is not None:
            api_client.set_base_url(self.base_url)
        if self.timeout is not None:
            api_client.set_timeout(self.timeout)
        if self.log_http_requests is not None:
            api_client.set_log_http_requests(self.log_http_requests)

        if self.command == "discover":
            asyncio.run(async_run_command(self.command, api_client, self.args))

        elif self.command == "get_device":
            if len(self.args) == 1:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device id")

        elif self.command == "get_device_raw":
            if len(self.args) == 1:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id")

        elif self.command == "get_sensor":
            if len(self.args) == 2:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id and sensor_name")

        elif self.command == "get_binary_sensor":
            if len(self.args) == 2:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id and sensor_name")

        elif self.command == "get_switch":
            if len(self.args) == 2:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id and sensor_name")

        elif self.command == "set_switch":
            if len(self.args) == 3:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id, sensor_name and value")

        elif self.command == "get_select":
            if len(self.args) == 2:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id and sensor_name")

        elif self.command == "set_select":
            if len(self.args) == 3:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id, sensor_name and value")

        elif self.command == "press_button":
            if len(self.args) == 2:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id and sensor_name")

        elif self.command == "get_siren":
            if len(self.args) == 2:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id and sensor_name")

        elif self.command == "set_siren":
            if len(self.args) == 3:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id, sensor_name and value")

        elif self.command == "get_diagnostics":
            if len(self.args) == 1:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device id")

        elif self.command == "get_camera_image":
            if len(self.args) == 2:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device id, sensor_name")

        elif self.command == "get_camera_stream":
            if len(self.args) == 2:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device id, sensor_name")

        elif self.command == "api_deviceBaseList":
            asyncio.run(async_run_command(self.command, api_client, self.args))

        elif self.command == "api_deviceOpenList":
            asyncio.run(async_run_command(self.command, api_client, self.args))

        elif self.command == "api_deviceBaseDetailList":
            if len(self.args) == 1:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id")

        elif self.command == "api_deviceOpenDetailList":
            if len(self.args) == 1:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id")

        elif self.command == "api_listDeviceAbility":
            if len(self.args) == 1:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id")

        elif self.command == "api_getAlarmMessage":
            if len(self.args) == 1:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id")

        elif self.command == "api_deviceStorage":
            if len(self.args) == 1:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id")

        elif self.command == "api_getDeviceCameraStatus":
            if len(self.args) == 2:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id and sensor_name")

        elif self.command == "api_setDeviceCameraStatus":
            if len(self.args) == 3:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id, sensor_name and value")

        elif self.command == "api_getNightVisionMode":
            if len(self.args) == 1:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id")

        elif self.command == "api_setNightVisionMode":
            if len(self.args) == 2:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id and mode")

        elif self.command == "api_getMessageCallback":
            asyncio.run(async_run_command(self.command, api_client, self.args))

        elif self.command == "api_setMessageCallbackOn":
            if len(self.args) == 1:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide url")

        elif self.command == "api_setMessageCallbackOff":
            asyncio.run(async_run_command(self.command, api_client, self.args))

        elif self.command == "api_restartDevice":
            if len(self.args) == 1:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id")

        elif self.command == "api_deviceSdcardStatus":
            if len(self.args) == 1:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id")

        elif self.command == "api_devicePTZInfo":
            if len(self.args) == 1:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id")

        elif self.command == "api_controlLocationPTZ":
            if len(self.args) == 4:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id, h, v ,z")

        elif self.command == "api_controlMovePTZ":
            if len(self.args) == 3:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id, operation, duration")

        elif self.command == "api_setDeviceSnapEnhanced":
            if len(self.args) == 1:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id")

        elif self.command == "api_bindDeviceLive":
            if len(self.args) == 2:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id, profile")

        elif self.command == "api_getLiveStreamInfo":
            if len(self.args) == 1:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id")

        elif self.command == "api_liveList":
            asyncio.run(async_run_command(self.command, api_client, self.args))

        elif self.command == "api_unbindLive":
            if len(self.args) == 1:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide live_token")

        elif self.command == "api_getDevicePowerInfo":
            if len(self.args) == 1:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device_id")

        else:
            self.print_usage()

    def print_usage(self):
        """Print CLI usage."""
        print("imouapi cli")
        print("Usage: python -m imouapi.cli [OPTIONS] COMMAND <ARGUMENTS>")
        print("")
        print("Options:")
        print("  --app-id <app_id>                                                   Imou Cloud App ID (mandatory)")
        print("  --app-secret <app_secret>                                           Imou Cloud App Secret (mandatory)")
        print("  --logging <info|debug>                                              The logging level")
        print("  --base-url <base_url>                                               Set a custom base url for the API")
        print(
            "  --timeout <timeout>                                                 Set a custom timeout for API calls"
        )
        print(
            "  --log-http-requests <on|off>                                        Log HTTP request/response in debug logs"  # noqa: E501
        )
        print("")
        print("Commmands:")
        print("  discover                                                            Discover registered devices")
        print(
            "  get_device <device_id>                                              Get the details of the device id provided"  # noqa: E501
        )
        print(
            "  get_device_raw <device_id>                                          Bruteforce the state of all capabilities and switches"  # noqa: E501
        )
        print("  get_sensor <device_id> <sensor_name>                                Get the state of a sensor")
        print("  get_binary_sensor <device_id> <sensor_name>                         Get the state of a binary sensor")
        print("  get_switch <device_id> <sensor_name>                                Get the state of a switch")
        print("  set_switch <device_id> <sensor_name> <on|off|toggle>                Set the state of a switch")
        print("  get_select <device_id> <sensor_name>                                Get the state of a select sensor")
        print("  set_select <device_id> <sensor_name> <value>                        Set the state of a select sensor")
        print("  press_button <device_id> <sensor_name>                              Press a button")
        print("  get_siren <device_id> <sensor_name>                                 Get the state of a siren sensor")
        print("  set_siren <device_id> <sensor_name> <value>                         Set the state of a siren sensor")
        print(
            "  get_diagnostics <device_id>                                         Get diagnostics information of the device id"  # noqa: E501
        )
        print("  get_camera_image <device_id> <sensor_name>                          Get a snapshot from the camera")
        print("  get_camera_stream <device_id> <sensor_name>                         Get streaming url for the camera")
        print("")
        print(
            "  api_deviceBaseList                                                  Return the list of registered devices by calling directly the API"  # noqa: E501
        )
        print(
            "  api_deviceOpenList                                                  Return the list of registered devices (open) by calling directly the API"  # noqa: E501
        )
        print(
            "  api_deviceBaseDetailList <device_id>                                Return the details of the requested devices by calling directly the API"  # noqa: E501
        )
        print(
            "  api_deviceOpenDetailList <device_id>                                Return the details of the requested devices (open) by calling directly the API"  # noqa: E501
        )
        print(
            "  api_listDeviceAbility <device_id>                                   Ability of a device by calling directly the API"  # noqa: E501
        )
        print(
            "  api_getAlarmMessage <device_id>                                     Get the device alarm list by calling directly the API"  # noqa: E501
        )
        print(
            "  api_deviceStorage <device_id>                                       Obtain device storage medium capacity information by calling directly the API"  # noqa: E501
        )
        print(
            "  api_getDeviceCameraStatus <device_id> <sensor_name>                 Get the state of a switch by calling directly the API"  # noqa: E501
        )
        print(
            "  api_setDeviceCameraStatus <device_id> <sensor_name> <on|off>        Set the state of a switch by calling directly the API"  # noqa: E501
        )
        print(
            "  api_getNightVisionMode <device_id>                                  Query the night vision mode of the device by calling directly the API"  # noqa: E501
        )
        print(
            "  api_setNightVisionMode <device_id> <mode>                           Set the night vision mode of the device by calling directly the API"  # noqa: E501
        )
        print(
            "  api_getMessageCallback                                              Get the message callback address by calling directly the API"  # noqa: E501
        )
        print(
            "  api_setMessageCallbackOn <url>                                      Set the message callback address by calling directly the API"  # noqa: E501
        )
        print(
            "  api_setMessageCallbackOff                                           Unset the message callback address by calling directly the API"  # noqa: E501
        )
        print("  api_restartDevice <device_id>                                       Restart the device")
        print(
            "  api_deviceSdcardStatus <device_id>                                  Get the SD card status of the device"
        )
        print("  api_devicePTZInfo <device_id>                                       Get current PTZ position")
        print(
            "  api_controlLocationPTZ <device_id> <h> <v> <z>                      Move to the h: horizontal, v: vertical location with z: zoom "  # noqa: E501
        )
        print(
            "  api_controlMovePTZ <device_id> <operation> <duration>               Move by performing the PTZ_OPERATIONS for the duration provided"  # noqa: E501
        )
        print(
            "  api_setDeviceSnapEnhanced <device_id>                               Capture a snapshot, returns image url"  # noqa: E501
        )
        print(
            "  api_bindDeviceLive <device_id> [HD|SD]                              Create live stream with the device for the given profile. Returns HLS stream and live token"  # noqa: E501
        )
        print(
            "  api_getLiveStreamInfo <device_id>                                   Obtain the live broadcast address for a given device"  # noqa: E501
        )
        print(
            "  api_liveList                                                        Get live streams status for the entire account"  # noqa: E501
        )
        print(
            "  api_unbindLive <live_token>                                         Delete the live stream for the given live token"  # noqa: E501
        )
        print(
            "  api_getDevicePowerInfo <device_id>                                  Get battery power information"  # noqa: E501
        )


if __name__ == "__main__":
    # create an instance of the cli
    cli = ImouCli()
    # parse provided command line
    cli.parse_command_line()
    # run the command requested by the user
    cli.run_command()
