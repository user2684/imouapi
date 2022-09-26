# imouapi
This python library helps in interacting with Imou Life Open API (https://open.imoulife.com) for remote controlling programmatically your Imou devices (https://www.imoulife.com), especially those settings such as motion detection, human detection, privacy, etc that can be changed by the Imou Life App only.

## Features
- Provide classes for both low level API interaction as well as device and sensors abastractions
- Exceptions and error handling
- Based on asyncio module

## Requirements

A valid Imou Open API `App Id` and `App Secret` are **required** to use the library.

In order to get them:
- Register an account on Imou Life if not done already
- Register a developer account on https://open.imoulife.com
- Open the Imou Console at https://open.imoulife.com/consoleNew/myApp/appInfo
  - Go to "My App", "App Information" and click on Edit
  - Fill in the required information and copy your AppId and AppSecret

## How to install

[TODO]

## How to use

### Option 1: high-level API (Recommended)

An abstraction over the API has been built to provide representations of devices and sensors:
- `ImouDevice` in `imouapi.device` to represent an Imou devices and all its sensors
- `ImouDiscoverService` in `imouapi.device_discover` can be used to discover devices registered with the account

A device has a set of properties and associated sensors. Each sensor type (sensor, binary_sensor and switch) is represented by a class and has properties and methods. Upon loading, the API is capable of enumerating available capabilities of the device and instantiate only the switches that the device suports. The API of course allows to eventually control those switches.
- Supported switches: "motionDetect", "headerDetect", "abAlarmSound", "breathingLight", if supported by the remote device
- Supported sensor: "lastAlarm"
- Supported binary_sensor: "online"

Examples on how to interact with ImouDevice and ImouDiscoverService are provided in the CLI implementation.

### Option 2: low-level API

By using `from imouapi.api import ImouAPIClient` and calling the provided methods for connecting and calling API endpoints.
The following Imou API are supported:
- deviceBaseList
- deviceBaseDetailList
- deviceOnline
- getDeviceCameraStatus
- setDeviceCameraStatus
- getAlarmMessage

Examples on how to interact with ImouAPIClient is provided in the high-level API implementation.

### Option 1: CLI

A command line interface is provided for testing and troubleshooting purposes.

```
Usage: python -m imouapi.cli [OPTIONS] COMMAND <ARGUMENTS>

Options (mandatory):
  --app-id <app_id>                                      Imou Cloud App ID
  --app-secret <app_secret>                              Imou Cloud App Secret

Commmands:
  discover                                               Discover registered devices
  get_device <device_id>                                 Get the details of the device id provided
  get_sensor <device_id> <sensor_name>                   Get the state of a sensor
  get_binary_sensor <device_id> <sensor_name>            Get the state of a binary sensor
  get_switch <device_id> <sensor_name>                   Get the state of a switch
  set_switch <device_id> <sensor_name> [on|off|toggle]  Set the state of a switch
```
