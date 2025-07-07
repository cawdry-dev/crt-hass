# Canal & River Trust Home Assistant Integration - Installation Guide

<div align="center">
  <img src="custom_components/canal_river_trust/icon.png" alt="Canal & River Trust" width="150"/>
</div>

## Quick Start

This Home Assistant custom integration provides real-time monitoring of Canal & River Trust waterway closures and stoppages.

### Features
- **Real-time Data**: Live updates from Canal & River Trust API
- **Geographic Data**: GPS coordinates for each notice
- **Smart Categorization**: Automatic separation of closures vs stoppages
- **Flexible Filtering**: Filter by region, waterway, or type
- **Rich Attributes**: Detailed information including dates, reasons, and locations

## Installation Methods

### Method 1: HACS (Recommended)

1. Ensure [HACS](https://hacs.xyz/) is installed
2. Add this repository as a custom repository in HACS
3. Search for "Canal & River Trust" and install
4. Restart Home Assistant
5. Add the integration via Settings → Integrations

### Method 2: Manual Installation

1. Download the latest release
2. Copy `custom_components/canal_river_trust/` to your Home Assistant `custom_components/` directory
3. Restart Home Assistant
4. Add via Settings → Integrations → Add Integration → Canal & River Trust

## Configuration

### Basic Setup
1. Go to Settings → Integrations
2. Click "Add Integration"
3. Search for "Canal & River Trust"
4. Configure options:
   - **Update Interval**: 5-1440 minutes (default: 30)
   - **Location Filter**: Optional text filter for specific areas
   - **Include Types**: Choose whether to include planned maintenance, emergency closures, etc.

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| Update Interval | How often to fetch data (minutes) | 30 |
| Location Filter | Filter notices by location/waterway | None |
| Include Planned | Include planned maintenance stoppages | Yes |
| Include Emergency | Include emergency closures | Yes |

## Sensors Created

### `sensor.canal_river_trust_closures`
- **State**: Number of active closures
- **Attributes**: Array of closure details

### `sensor.canal_river_trust_stoppages` 
- **State**: Number of active stoppages
- **Attributes**: Array of stoppage details

### Sensor Attributes
Each notice includes:
- `title`: Description of the issue
- `region`: Geographic region (e.g., "West Midlands")
- `waterways`: Affected waterway (e.g., "Grand Union Canal")
- `type`: Type of notice (Stoppage, Closure, Restriction, Advisory)
- `reason`: Reason category (Maintenance, Lock Works, Emergency, etc.)
- `start_date`: When the notice begins
- `end_date`: When the notice ends (if known)
- `state`: Publication state
- `coordinates`: GPS coordinates [longitude, latitude]

## Example Usage

### Automation: Daily Summary
```yaml
automation:
  - alias: "Canal Status Summary"
    trigger:
      platform: time
      at: "08:00:00"
    action:
      service: notify.notify
      data:
        title: "🚢 Waterway Status"
        message: >
          Closures: {{ states('sensor.canal_river_trust_closures') }}
          Stoppages: {{ states('sensor.canal_river_trust_stoppages') }}
```

### Dashboard Card
```yaml
type: entity
entity: sensor.canal_river_trust_closures
name: Canal Closures
icon: mdi:lock
```

### Location-Specific Alert
```yaml
automation:
  - alias: "Local Waterway Alert"
    trigger:
      platform: state
      entity_id: sensor.canal_river_trust_stoppages
    condition:
      condition: template
      value_template: >
        {% set notices = state_attr('sensor.canal_river_trust_stoppages', 'stoppages') or [] %}
        {{ notices | selectattr('waterways', 'search', 'Grand Union Canal') | list | length > 0 }}
    action:
      service: notify.notify
      data:
        title: "Grand Union Canal Alert"
        message: "New notice on Grand Union Canal"
```

## Data Source

- **API**: Canal & River Trust Official API
- **URL**: https://canalrivertrust.org.uk/api/stoppage/notices
- **Format**: GeoJSON with feature properties
- **Update Frequency**: Data typically updated by CRT every few hours
- **Geographic Coverage**: England and Wales waterways managed by Canal & River Trust

## Troubleshooting

### Common Issues

#### Config Flow Error: "get_closures() method not found"
This indicates you may have an older version of the integration files. Solution:
1. Delete the entire `custom_components/canal_river_trust/` directory
2. Restart Home Assistant
3. Reinstall the integration with the latest version
4. Try adding the integration again

### No Data Appearing
1. Check Home Assistant logs for API errors
2. Verify internet connectivity
3. Check if CRT API is accessible: https://canalrivertrust.org.uk/api/stoppage/notices

### Integration Not Loading
1. Verify all files are in `custom_components/canal_river_trust/`
2. Check Home Assistant logs for syntax errors
3. Restart Home Assistant after installation

### Configuration Issues
1. Check the Integration page in Home Assistant
2. Try removing and re-adding the integration
3. Verify your configuration options are valid

## Debug Logging

Add to `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.canal_river_trust: debug
```

## Support

- **Issues**: [GitHub Issues](https://github.com/cawdry/crt-hass/issues)
- **Documentation**: [GitHub Repository](https://github.com/cawdry/crt-hass)
- **Home Assistant Community**: Search for "Canal River Trust"

## Data Privacy

This integration:
- Only fetches publicly available data from Canal & River Trust
- Does not collect or store personal information
- Makes API requests directly from your Home Assistant instance
- Respects the Canal & River Trust API terms of use
