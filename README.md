# Canal & River Trust Integration for Home Assistant

A Home Assistant custom integration that provides real-time data about canal and river closures and stoppages from the Canal & River Trust.

## Features

- **Closures Sensor**: Monitor current waterway closures
- **Stoppages Sensor**: Track planned and emergency stoppages
- **Location Filtering**: Filter by specific waterways or regions
- **Real-time Updates**: Configurable update intervals
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

- **Update Interval**: How often to fetch new data (default: 30 minutes)
- **Location Filter**: Optional filter for specific waterways or regions
- **Include Planned**: Whether to include planned stoppages (default: true)
- **Include Emergency**: Whether to include emergency closures (default: true)

## Sensors

### Closures Sensor
- **Name**: `sensor.crt_closures`
- **State**: Number of active closures
- **Attributes**: Detailed list of all closures with location, reason, and expected duration

### Stoppages Sensor
- **Name**: `sensor.crt_stoppages`
- **State**: Number of active stoppages
- **Attributes**: Detailed list of all stoppages with location, type, and schedule

## Data Source

This integration uses the Canal & River Trust Open Data API:
- **Source**: https://data-canalrivertrust.opendata.arcgis.com
- **Data Format**: ArcGIS REST Services
- **Update Frequency**: Data is typically updated by CRT every few hours

## Support

For issues and feature requests, please use the GitHub issue tracker.

## License

This project is licensed under the MIT License.
