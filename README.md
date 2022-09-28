# imouapi
This python library helps in interacting with [Imou Life Open API](https://open.imoulife.com) for remote controlling programmatically your [Imou devices](https://www.imoulife.com), especially those settings such as motion detection, human detection, privacy, etc that can be changed by the Imou Life App only.

## Features

- Provide classes for both low level API interaction as well as device and sensors abastractions
- Exceptions and error handling
- Based on asyncio module

## Quickstart

- Install the library with `pip install imouapi`
- Register a developer account on [Imou Life Open API](https://open.imoulife.com) and get your `appId` and `appSecret`
- Discover registered devices (`from imouapi.device import ImouDiscoverService`)
- Either use the high level API (`from imouapi.device import ImouDevice`) or the low level API (`from imouapi.api import ImouAPIClient`) to interact with the device

Full details on the installation process, requirements, usage and classes and methods made available by the library are available at [https://user2684.github.io/imouapi](https://user2684.github.io/imouapi)
