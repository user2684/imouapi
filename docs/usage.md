You can use the library in three different ways:

### Option 1: high-level API (Recommended)

An abstraction over the API has been built to provide representations of devices and sensors:

- `imouapi.device` provides `ImouDevice` to represent an Imou devices and all its sensors and `ImouDiscoverService` which can be used to discover devices registered with the account
- `imouapi.device_entity` provides `ImouSensor`, `ImouBinarySensor` , `ImouSwitch` , etc. representing the sensors attached to the device. Upon loading, the library is capable of enumerating available capabilities of the device and instantiate only the switches that the device suports. The API of course allows to eventually control those switches.

Examples on how to interact with ImouDevice and ImouDiscoverService are provided in the CLI implementation.

### Option 2: low-level API

With `from imouapi.api import ImouAPIClient` and calling the provided methods for connecting and calling API endpoints.
Details on the supported APIs are provided in each module's documentation.
Examples on how to interact with ImouAPIClient is provided in the high-level API implementation.

### Option 3: CLI

A command line interface is provided for testing and troubleshooting purposes.
To get a list of supported commands and options run the following:
```
python -m imouapi.cli --help
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
