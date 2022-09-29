# Changelog

## [0.1.5] (2022-09-28)
### Added
- ImouAPIClient.log_http_requests() for enabling http request/response logging (off by default)
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
