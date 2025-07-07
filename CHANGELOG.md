# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Map Support**: Integration now supports plotting waterway issues on Home Assistant maps
- **Geo-location Platform**: Individual location markers for each notice/issue
- **Device Tracker Platform**: Alternative tracking entities for notices
- **Location Properties**: Sensors now include latitude/longitude for map compatibility
- **Enhanced Dashboards**: Updated dashboards with interactive map views
- **Coordinate Display**: GPS coordinates shown in issue details
- **Map Documentation**: Comprehensive guide for map configuration and usage

### Changed
- **API Enhancement**: Now requests geometry data from Canal & River Trust API
- **Sensor Platform**: Added latitude/longitude properties to closure and stoppage sensors
- **Dashboard Updates**: Enhanced and simple dashboards now include map functionality
- **Version Bump**: Updated to v1.0.2 for map support features

### Planned
- **Map Clustering**: Group nearby issues to reduce map clutter
- **Custom Map Icons**: Different marker styles for closure types
- **Route Integration**: Integration with navigation systems
- **Historical Tracking**: Show issue movement over time
- **Proximity Zones**: Automatic zone creation around frequent issue areas

## [1.0.2] - 2025-01-XX

### Fixed
- Fixed dashboard entity references - removed non-existent sensors
- Corrected sensor names in dashboard examples to match actual integration sensors
- Removed unsupported custom cards from dashboard examples
- Fixed map card configuration that was incompatible with sensor data format
- Replaced custom `fold-entity-row` cards with built-in alternatives

### Added
- Dashboard troubleshooting guide (`DASHBOARD_TROUBLESHOOTING.md`)
- Updated README with correct sensor entity IDs and dashboard information
- Enhanced dashboard templates with better error handling and fallback values

### Changed
- Updated `enhanced_dashboard.yaml` to use only built-in Home Assistant cards
- Improved `simple_dashboard.yaml` for better compatibility
- Updated dashboard templates to handle missing data gracefully

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
