# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Map visualization of closures and stoppages
- Enhanced location filtering with GPS coordinates
- Historical data storage and trends
- Push notifications for new issues
- Route planning integration

## [1.0.1] - 2025-07-07

### Changed
- Default update interval changed from 30 minutes to 4 hours (more appropriate for waterway notices)

### Added
- Integration logo/icon using official Canal & River Trust branding
- Enhanced device information with configuration URL
- Required `fields` parameter in API requests for proper data retrieval
- Enhanced error handling for malformed API responses

### Fixed
- Fixed config flow error where `get_closures()` method was not found
- Updated config flow to use correct `get_notices()` API method
- Fixed API requests by ensuring `fields` parameter is included (was causing "Service Unavailable" responses)
- Improved API client logging for better debugging
- Enhanced coordinator logging for data update tracking

## [1.0.0] - 2025-01-07

### Added
- Initial release of Canal & River Trust integration
- Support for monitoring canal and river closures
- Support for monitoring planned and emergency stoppages
- Configurable update intervals (5-1440 minutes)
- Location-based filtering of data
- Options to include/exclude planned stoppages and emergency closures
- Two main sensors:
  - `sensor.canal_river_trust_closures`: Number of active closures
  - `sensor.canal_river_trust_stoppages`: Number of active stoppages
- Rich sensor attributes with detailed information:
  - Location and waterway details
  - Reason and type of closure/stoppage
  - Start and end dates
  - Status and description
- Home Assistant UI configuration flow
- HACS compatibility
- Example automations and dashboard configurations
- Comprehensive documentation and development guide

### Technical Details
- Uses Canal & River Trust official API (https://canalrivertrust.org.uk/api/stoppage/notices)
- GeoJSON format with coordinate data for map visualization
- Async HTTP client with proper error handling and headers
- Data update coordinator for efficient polling
- Configurable through Home Assistant UI
- Full translation support (English)
- Follows Home Assistant development best practices
- Supports both closures and stoppages through single API endpoint
