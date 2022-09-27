"""Console script for imouapi."""
import asyncio
import logging
import re
import sys

import aiohttp

from imouapi.device import ImouDevice, ImouDiscoverService
from imouapi.device_entity import ImouBinarySensor, ImouSensor, ImouSwitch
from imouapi.exceptions import ImouException


async def discover_devices(app_id: str, app_secret: str, base_url: str, timeout: int) -> None:
    """Discovered devices associated with the account."""
    session = aiohttp.ClientSession()
    try:
        discover_service = ImouDiscoverService(app_id, app_secret, session, base_url, timeout)
        await discover_service.async_connect()
        discovered_devices = await discover_service.async_discover_devices()
        print(f"Discovered {len(discovered_devices)} devices:")
        for device_name, device in discovered_devices.items():
            print(f"- {device_name}:")
            print(f"  - Model: {device.get_model()}")
            print(f"  - Device ID: {device.get_device_id()}")
            print(f"  - Firmware: {device.get_firmware()}")
    except ImouException as exception:
        print(exception.to_string())
    await session.close()


async def get_device(app_id: str, app_secret: str, device_id: str, base_url: str, timeout: int) -> None:
    """Print out the details of a given device."""
    session = aiohttp.ClientSession()
    try:
        device = ImouDevice(app_id, app_secret, device_id, session, base_url, timeout)
        await device.async_connect()
        await device.async_initialize()
        await device.async_get_data()
        print(device.dump())
    except ImouException as exception:
        print(exception.to_string())
    await session.close()


async def get_sensor(
    app_id: str, app_secret: str, device_id: str, sensor_name: str, base_url: str, timeout: int
) -> None:
    """Print out the details of a given sensor."""
    session = aiohttp.ClientSession()
    try:
        device = ImouDevice(app_id, app_secret, device_id, session, base_url, timeout)
        await device.async_connect()
        await device.async_initialize()
        await device.async_get_data()
        print(f"- {device.get_name()}:")
        sensors: list[ImouSensor] = device.get_sensors("sensor")  # type: ignore
        for sensor in sensors:
            if sensor_name == sensor.get_name():
                print(f"  - {sensor.get_description()} ({sensor.get_name()}): {sensor.get_state()}")
                break
    except ImouException as exception:
        print(exception.to_string())
    await session.close()


async def get_binary_sensor(
    app_id: str, app_secret: str, device_id: str, sensor_name: str, base_url: str, timeout: int
) -> None:
    """Print out the details of a given binary sensor."""
    session = aiohttp.ClientSession()
    try:
        device = ImouDevice(app_id, app_secret, device_id, session, base_url, timeout)
        await device.async_connect()
        await device.async_initialize()
        await device.async_get_data()
        print(f"- {device.get_name()}:")
        sensors: list[ImouBinarySensor] = device.get_sensors("binary_sensor")  # type: ignore
        for sensor in sensors:
            if sensor_name == sensor.get_name():
                status = "ON" if sensor.is_on() else "OFF"
                print(f"  - {sensor.get_description()} ({sensor.get_name()}): {status}")
                break
    except ImouException as exception:
        print(exception.to_string())
    await session.close()


async def get_switch(
    app_id: str, app_secret: str, device_id: str, sensor_name: str, base_url: str, timeout: int
) -> None:
    """Print out the details of a given switch."""
    session = aiohttp.ClientSession()
    try:
        device = ImouDevice(app_id, app_secret, device_id, session, base_url, timeout)
        await device.async_connect()
        await device.async_initialize()
        await device.async_get_data()
        print(f"- {device.get_name()}:")
        sensors: list[ImouSwitch] = device.get_sensors("switch")  # type: ignore
        for sensor in sensors:
            if sensor_name == sensor.get_name():
                status = "ON" if sensor.is_on() else "OFF"
                print(f"  - {sensor.get_description()} ({sensor.get_name()}): {status}")
                break
    except ImouException as exception:
        print(exception.to_string())
    await session.close()


async def set_switch(
    app_id: str, app_secret: str, device_id: str, sensor_name: str, value: str, base_url: str, timeout: int
) -> None:
    """Print out the details of a given switch."""
    session = aiohttp.ClientSession()
    try:
        device = ImouDevice(app_id, app_secret, device_id, session, base_url, timeout)
        await device.async_connect()
        await device.async_initialize()
        await device.async_get_data()
        sensors: list[ImouSwitch] = device.get_sensors("switch")  # type: ignore
        for sensor in sensors:
            if sensor_name == sensor.get_name():
                if value == "ON":
                    await sensor.async_turn_on()
                elif value == "OFF":
                    await sensor.async_turn_off()
                elif value == "TOGGLE":
                    await sensor.async_toggle()
                await get_switch(app_id, app_secret, device_id, sensor_name, base_url, timeout)
                break
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
        if self.app_id is None or self.app_secret is None:
            print("ERROR: provide app_id and app_secret")
            print("")
            self.print_usage()
            sys.exit(1)
        if self.command == "discover":
            asyncio.run(discover_devices(self.app_id, self.app_secret, self.base_url, self.timeout))
        elif self.command == "get_device":
            if len(self.args) == 1:
                asyncio.run(get_device(self.app_id, self.app_secret, self.args[0], self.base_url, self.timeout))
            else:
                print("ERROR: provide device id")
        elif self.command == "get_sensor":
            if len(self.args) == 2:
                asyncio.run(
                    get_sensor(self.app_id, self.app_secret, self.args[0], self.args[1], self.base_url, self.timeout)
                )
            else:
                print("ERROR: provide device_id and sensor_name")
        elif self.command == "get_binary_sensor":
            if len(self.args) == 2:
                asyncio.run(
                    get_binary_sensor(
                        self.app_id, self.app_secret, self.args[0], self.args[1], self.base_url, self.timeout
                    )
                )
            else:
                print("ERROR: provide device_id and sensor_name")
        elif self.command == "get_switch":
            if len(self.args) == 2:
                asyncio.run(
                    get_switch(self.app_id, self.app_secret, self.args[0], self.args[1], self.base_url, self.timeout)
                )
            else:
                print("ERROR: provide device_id and sensor_name")
        elif self.command == "set_switch":
            if len(self.args) == 3:
                asyncio.run(
                    set_switch(
                        self.app_id,
                        self.app_secret,
                        self.args[0],
                        self.args[1],
                        self.args[2],
                        self.base_url,
                        self.timeout,
                    )
                )
            else:
                print("ERROR: provide device_id and sensor_name")
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
