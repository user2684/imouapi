"""Console script for imouapi."""
import asyncio
import logging
import re
import sys

import aiohttp

from imouapi.api import ImouAPIClient
from imouapi.device import ImouDevice, ImouDiscoverService
from imouapi.device_entity import ImouBinarySensor, ImouSensor, ImouSwitch
from imouapi.exceptions import ImouException


async def async_run_command(command: str, api_client: ImouAPIClient, args: list[str]):
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

        elif command in ["get_device", "get_sensor", "get_binary_sensor", "get_switch", "set_switch"]:
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
        self.device_id = None
        self.command = None
        self.loggingconfig = {
            'level': 'INFO',
            'format': '%(asctime)s %(levelname)s <%(name)s %(module)s %(funcName)s> %(message)s',
            'datefmt': '%a, %d %b %Y %H:%M:%S',
        }
        self.args = []

    def parse_command_line(self):
        """Parse command line arguments."""
        skip_next = False
        for i in range(1, len(sys.argv)):
            if skip_next:
                skip_next = False
                continue
            arg = sys.argv[i]
            arg = re.sub(' +', ' ', arg)
            if arg == "--app-id":
                self.app_id = sys.argv[i + 1]
                skip_next = True
                continue
            if arg == "--app-secret":
                self.app_secret = sys.argv[i + 1]
                skip_next = True
                continue
            if arg == "--base-url":
                self.base_url = sys.argv[i + 1]
                skip_next = True
                continue
            if arg == "--timeout":
                self.timeout = sys.argv[i + 1]
                skip_next = True
                continue
            if arg == "--logging":
                self.logging = sys.argv[i + 1]
                self.loggingconfig["level"] = self.logging.upper()
                logging.basicConfig(**self.loggingconfig)  # type: ignore
                skip_next = True
                continue
            if self.command is None:
                self.command = arg
                continue
            self.args.append(arg)

    def run_command(self):
        """Run the requested command."""
        # ensure app id and app secret are provided
        if self.app_id is None or self.app_secret is None:
            print("ERROR: provide app_id and app_secret")
            print("")
            self.print_usage()
            sys.exit(1)

        # instantiate an api client
        api_client = ImouAPIClient(self.app_id, self.app_secret, None)
        if self.base_url is not None:
            api_client.set_base_url(self.base_url)
        if self.timeout is not None:
            api_client.set_timeout(self.timeout)

        if self.command == "discover":
            asyncio.run(async_run_command(self.command, api_client, self.args))
        elif self.command == "get_device":
            if len(self.args) == 1:
                asyncio.run(async_run_command(self.command, api_client, self.args))
            else:
                print("ERROR: provide device id")
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
        else:
            self.print_usage()

    def print_usage(self):
        """Print CLI usage."""
        print("imouapi cli")
        print("Usage: python -m imouapi.cli [OPTIONS] COMMAND <ARGUMENTS>")
        print("")
        print("Options:")
        print("  --app-id <app_id>                                      Imou Cloud App ID (mandatory)")
        print("  --app-secret <app_secret>                              Imou Cloud App Secret (mandatory)")
        print("  --logging <info|debug>                                 The logging level")
        print("  --base-url <base_url>                                  Set a custom base url for the API")
        print("  --timeout <timeout>                                    Set a custom timeout for API calls")
        print("")
        print("Commmands:")
        print("  discover                                               Discover registered devices")
        print("  get_device <device_id>                                 Get the details of the device id provided")
        print("  get_sensor <device_id> <sensor_name>                   Get the state of a sensor")
        print("  get_binary_sensor <device_id> <sensor_name>            Get the state of a binary sensor")
        print("  get_switch <device_id> <sensor_name>                   Get the state of a switch")
        print("  set_switch <device_id> <sensor_name> [on|off|toggle]   Set the state of a switch")


# create an instance of the cli
cli = ImouCli()
# parse provided command line
cli.parse_command_line()
# run the command requested by the user
cli.run_command()
