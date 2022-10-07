# Changelog

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
