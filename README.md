# Canal & River Trust Integration for Home Assistant

<div align="center">
  <img src="custom_components/canal_river_trust/icon.png" alt="Canal & River Trust Logo" width="200"/>
</div>

A Home Assistant custom integration that provides real-time data about canal and river closures and stoppages from the Canal & River Trust.

## Features

- **Closures Sensor**: Monitor current waterway closures
- **Stoppages Sensor**: Track planned and emergency stoppages
- **Emergency Issues Sensor**: Alert on urgent waterway problems
- **Regional Breakdown Sensor**: Regional distribution of issues
- **Upcoming Issues Sensor**: Planned works starting within 7 days
- **Map Support**: Plot issues on interactive Home Assistant maps
- **Location Data**: GPS coordinates for each waterway issue
- **Real-time Updates**: Configurable update intervals (default: 4 hours)
- **Rich Attributes**: Detailed information about each closure/stoppage

## Installation

### HACS (Recommended)

1. Add this repository to HACS as a custom repository
2. Search for "Canal & River Trust" in HACS
3. Install the integration
4. Restart Home Assistant
5. Add the integration through the UI

### Manual Installation

1. Copy the `custom_components/canal_river_trust` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Add the integration through the UI

## Configuration

The integration can be configured through the Home Assistant UI:

1. Go to Configuration → Integrations
2. Click "Add Integration"
3. Search for "Canal & River Trust"
4. Follow the configuration steps

### Configuration Options

- **Update Interval**: How often to fetch new data (default: 4 hours)
- **Location Filter**: Optional filter for specific waterways or regions
- **Include Planned**: Whether to include planned stoppages (default: true)
- **Include Emergency**: Whether to include emergency closures (default: true)

## Sensors

The integration creates 5 sensors:

### 1. Closures Sensor
- **Entity ID**: `sensor.canal_river_trust_closures`
- **State**: Number of active closures
- **Attributes**: Detailed list of all closures with location, reason, and expected duration

### 2. Stoppages Sensor
- **Entity ID**: `sensor.canal_river_trust_stoppages`
- **State**: Number of active stoppages
- **Attributes**: Detailed list of all stoppages with location, type, and schedule

### 3. Emergency Issues Sensor
- **Entity ID**: `sensor.canal_river_trust_emergency_issues`
- **State**: Number of emergency issues
- **Attributes**: Detailed list of emergency issues requiring immediate attention

### 4. Regional Breakdown Sensor
- **Entity ID**: `sensor.canal_river_trust_regional_breakdown`
- **State**: Total number of issues across all regions
- **Attributes**: Regional breakdown and most affected region

### 5. Upcoming Issues Sensor
- **Entity ID**: `sensor.canal_river_trust_upcoming_issues`
- **State**: Number of issues starting within 7 days
- **Attributes**: Detailed list of upcoming planned works

## Dashboards

Pre-built dashboard examples are available in the `examples/` folder:

- **`simple_dashboard.yaml`**: Basic dashboard using only built-in cards
- **`enhanced_dashboard.yaml`**: Advanced dashboard with comprehensive features including maps
- **`automations.yaml`**: Example automation triggers

### Map Support

The integration now supports plotting waterway issues on Home Assistant maps:

- **Interactive Maps**: View all closures and stoppages on a map
- **Geo-location Events**: Individual markers for each issue
- **Coordinate Data**: GPS coordinates included in sensor attributes
- **Multiple Platforms**: Sensor, geo-location, and device tracker entities

See [`MAP_SUPPORT.md`](MAP_SUPPORT.md) for detailed map configuration and usage.

### Dashboard Troubleshooting

If you encounter dashboard configuration issues, see [`DASHBOARD_TROUBLESHOOTING.md`](DASHBOARD_TROUBLESHOOTING.md) for common solutions.

## Data Source

This integration uses the Canal & River Trust Open Data API:
- **Source**: https://data-canalrivertrust.opendata.arcgis.com
- **Data Format**: ArcGIS REST Services
- **Update Frequency**: Data is typically updated by CRT every few hours

## Support

For issues and feature requests, please use the GitHub issue tracker.

## License

This project is licensed under the MIT License.
