# Changelog

## [1.0.14] (2023-12-24)
### Changed
- Added channelId in the payload when calling `async_api_setDeviceCameraStatus()`
- `async_discover_devices()` now ignores with a warning unrecognized/unsupported devices instead of throwing an exception
- Updated dependencies and upgraded to Python 3.11
### Fixed
- Type errors

## [1.0.13] (2023-02-19)
### Added
- Support for`getDevicePowerInfo` Imou API through `async_api_getDevicePowerInfo()` and CLI commands
### Changed
- Motion Detect sensor added regardless of the capabilities

## [1.0.12] (2022-12-11)
### Fixed
- Dormant device logic

## [1.0.11] (2022-12-11)
### Added
- `sleepable`, `status` attributes and `get_sleepable()`, `get_status()`, `async_refresh_status()`, `async_wakeup()` functions to `ImouDevice`
- `status` sensor
- `get_api_client()` `set_wait_after_wakeup()`, `get_wait_after_wakeup()`, `set_camera_wait_before_download()`, `get_camera_wait_before_download()` to `ImouDevice`
### Changed
- Device is now marked online if either online or dormant

## [1.0.10] (2022-12-03)
### Added
- Support for `setDeviceSnapEnhanced`, `bindDeviceLive`, `queryLiveStatus`, `liveList`, `unbindLive` Imou APIs through  ``async_api_setDeviceSnapEnhanced()`, `async_api_bindDeviceLive()`, `async_api_getLiveStreamInfo()`, `async_apiliveList()`, `async_api_unbindLive()` and CLI commands
- `async_get_image()` and `async_get_stream_url()` to `ImouCamera` class and CLI commands `get_camera_image` and `get_camera_stream`

## [1.0.9] (2022-11-26)
### Added
- `ImouCamera` class exposing `async_service_ptz_location()` and `async_service_ptz_move()`
### Changed
- Usage page of the documentation

## [1.0.8] (2022-11-26)
### Added
- Support for `devicePTZInfo`, `controlLocationPTZ`, `controlMovePTZ` Imou APIs through  ``async_api_devicePTZInfo()`, `async_api_controlLocationPTZ()`, `async_api_controlMovePTZ()` and CLI commands

## [1.0.7] (2022-11-20)
### Added
- `ImouSiren` class, `get_siren()` and `set_siren()` to cli
### Removed
- `siren` switch, now implemented as `ImouSiren`

## [1.0.6] (2022-11-19)
### Added
- Attributes to `ImouEntity` class and `get_attributes()`
- `motionDetection` binary sensor and `refreshAlarm` button
### Removed
- `lastAlarm` sensor

## [1.0.5] (2022-11-13)
### Added
- Support for `restartDevice`, `deviceSdcardStatus` Imou APIs through `async_api_restartDevice()`, `async_api_deviceSdcardStatus()` and CLI commands
- Support for "Activate Siren" switch
- `ImouButton` class and `restartDevice`, `refreshData` buttons
- Support for `press_button` to CLI
- Support for `callbackUrl` sensor
- `set_device()` function to `ImouEntity`
### Changed
- Reviewed switches' labels
### Fixed
- Storage used sensor now reporting None when SD card is not present

## [1.0.4] (2022-10-22)
### Added
- `ImouSelect` class and support for `nightVisionMode` select
- `get_select` and `set_select` commands to CLI
- `pushNotifications` switch
### Changed
- Sensors (not only switches) are now added based on the available capabilities

## [1.0.3] (2022-10-22)
### Added
- Support for not documented `WLM` capability
- Support for undocumented capabilities or capabilities inherited from other capabilities
- Support for `deviceOpenList`, `deviceOpenBaseDetailList`, `listDeviceAbility`, `deviceStorage`, `getNightVisionMode`, `setNightVisionMode`, `getMessageCallback`, `setMessageCallback` APIs through `async_api_deviceOpenList()`, `async_api_deviceOpenBaseDetailList()`, `async_api_listDeviceAbility()`, `async_api_deviceStorage()`, `async_api_getNightVisionMode()`, `async_api_setNightVisionMode()`, `async_api_getMessageCallback()`, `async_api_getMessageCallbackOn()`, `async_api_setMessageCallbackOff()`
- `api_deviceBaseList`, `api_deviceOpenList`, `api_deviceBaseDetailList`, `api_deviceOpenDetailList`, `api_getDeviceCameraStatus`, `api_setDeviceCameraStatus`, `api_listDeviceAbility`, `api_getAlarmMessage`, `api_deviceStorage`, `api_getNightVisionMode`, `api_setNightVisionMode`, `api_getMessageCallback`, `api_getMessageCallbackOn`, `api_getMessageCallbackOff` commands to CLI
### Changed
- `async_api_getAlarmMessage()` now returning the last 10 alarms of the month, not just the last one
### Removed
- `get_device_class()` from `ImouSensor`

## [1.0.2] (2022-10-19)
### Fixed
- Switches mapping to versioned capabilities are now created (e.g. audioEncodeControl for capability AudioEncodeControlV2)

## [1.0.1] (2022-10-16)
### Added
- `get_diagnostics()` method to `ImouDevice` class
- `get_diagnostics` command to CLI

## [1.0.0] (2022-10-15)
### Added
- `--log-http-requests` option to CLI
### Fixed
- Last Alarm sensor unable to retrieve most recent alarms
- Last Alarm sensor shifted ahead by the local timezone

## [0.2.2] (2022-10-07)
### Added
- Test cases for most of the classes

## [0.2.1] (2022-10-04)
### Added
- Test cases for `ImouAPIClient`
- Access Token expiration handling

## [0.2.0] (2022-10-03)
### Added
- `get_sensor_by_name()` and `get_all_sensors()` added to `ImouDevice` class
### Changed
- `ImouDiscoverService` and `ImouDevice` now take an instance of `ImouAPIClient` to initialize
- In `ImouDiscoverService` and `ImouDevice`, moved `base_url` and `timeout` from constructor to function `set_base_url()` and `set_timeout()`
- There is no more concept of supported switches, all of those discovered, are made available and can be controlled
- Sensors' icons moved out of the this library since not applicable in this context
- `ImouDevice` `get_sensors()` renamed in `get_sensors_by_platform()`
- If connection failes, multiple retries are done
- Partial refactoring of the code
### Removed
- `async_connect()` from both `ImouDevice` and `ImouDiscoverService`. Connection takes place at the first API call

## [0.1.5] (2022-09-28)
### Added
- `ImouAPIClient.log_http_requests()` for enabling http request/response logging (off by default)
- If http logging is enabled, log messages are redacted from sensitive information
- ImouAPIClient.redact_log_message() for enabling log redaction (on by default)
### Changed
- Moved info logs into debug level
- By default, with debug level, no more logging HTTP requests and responses

## [0.1.4] (2022-09-28)
### Added
- Github workflow to publish on PyPI
### Changed
- Updated documentation

## [0.1.3] (2022-09-27)
### Changed
- API base URL and API timeout are not optional parameters and can be provided by the user
- Updated CLI, added logging level
- Updated documentation

## [0.1.2] (2022-09-27)
### Changed
- Re-organized the file structure
- Updated documentation

## [0.1.1] (2022-09-27)
### Added
- First development release

## [0.1.0] (2022-09-26)
### Added
- First commit
