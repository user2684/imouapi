# imouapi
This python library helps in interacting with [Imou Life Open API](https://open.imoulife.com) for remote controlling programmatically your [Imou devices](https://www.imoulife.com), especially those settings such as motion detection, human detection, privacy, etc that can be changed by the Imou Life App only.

## Features

- Provide classes for both low level API interaction as well as device and sensors abastractions
- Exceptions and error handling
- Based on asyncio module

## Quickstart

- Install the library with `pip install imouapi`
- Register a developer account on [Imou Life Open API](https://open.imoulife.com) and get your `appId` and `appSecret`
- Instantiate the Imou API client (`from imouapi.api import ImouAPIClient`) and initialize it (e.g. `api_client = ImouAPIClient(app_id, app_secret, session)`)
- Discover registered devices by importing the Discover service (`from imouapi.device import ImouDiscoverService`), inializing it (e.g. `discover_service = ImouDiscoverService(api_client)`) and running a discovery (e.g. `discovered_devices = await discover_service.async_discover_devices()`)
- Either use the high level API by importing the Imou Device class (`from imouapi.device import ImouDevice`) and initializing it (e.g. `device = ImouDevice(api_client, device_id)`) or using directly the low level API provided by `ImouAPIClient` to interact with the device

Full details on the installation process, requirements, usage and classes and methods made available by the library are available at [https://user2684.github.io/imouapi](https://user2684.github.io/imouapi)
