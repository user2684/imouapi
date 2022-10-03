You can use the library in three different ways:

### Option 1: high-level API (Recommended)

An abstraction over the API has been built to provide representations of devices and sensors:

- `imouapi.device` provides `ImouDevice` to represent an Imou devices and all its sensors and `ImouDiscoverService` which can be used to discover devices registered with the account
- `imouapi.device_entity` provides `ImouSensor`, `ImouBinarySensor` and `ImouSwitch`, representing the sensors attached to the device. Upon loading, the library is capable of enumerating available capabilities of the device and instantiate only the switches that the device suports. The API of course allows to eventually control those switches.

    - Supported switches: all the switches supported by the remote device
    - Supported sensor: "lastAlarm"
    - Supported binary_sensor: "online"

Examples on how to interact with ImouDevice and ImouDiscoverService are provided in the CLI implementation.

### Option 2: low-level API

With `from imouapi.api import ImouAPIClient` and calling the provided methods for connecting and calling API endpoints.
The following Imou API are supported:

- deviceBaseList
- deviceBaseDetailList
- deviceOnline
- getDeviceCameraStatus
- setDeviceCameraStatus
- getAlarmMessage

Examples on how to interact with ImouAPIClient is provided in the high-level API implementation.

### Option 3: CLI

A command line interface is provided for testing and troubleshooting purposes.

```
Usage: python -m imouapi.cli [OPTIONS] COMMAND <ARGUMENTS>

Options:
  --app-id <app_id>                                      Imou Cloud App ID (mandatory)
  --app-secret <app_secret>                              Imou Cloud App Secret (mandatory)
  --logging <info|debug>                                 The logging level
  --base-url <base_url>                                  Set a custom base url for the API
  --timeout <timeout>                                    Set a custom timeout for API calls

Commmands:
  discover                                               Discover registered devices
  get_device <device_id>                                 Get the details of the device id provided
  get_sensor <device_id> <sensor_name>                   Get the state of a sensor
  get_binary_sensor <device_id> <sensor_name>            Get the state of a binary sensor
  get_switch <device_id> <sensor_name>                   Get the state of a switch
  set_switch <device_id> <sensor_name> [on|off|toggle]   Set the state of a switch
```

## Exception Handling

The library provides a simplified way for handling exceptions:
```
from imouapi.exceptions import ImouException

try:
    await device.async_initialize()
except ImouException as exception:
    _LOGGER.error(exception.to_string())
    raise ImouException() from exception
```

The `ImouException` class provides a `to_string()` method which returns the name of the exception which was raised and the full stacktrace.
