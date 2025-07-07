# Map Support Documentation

## Overview

The Canal & River Trust integration now supports plotting waterway issues on interactive maps in Home Assistant. This feature provides visual representation of closures, stoppages, and other waterway issues across the canal network.

## Map Features

### Supported Platforms

The integration creates entities across multiple platforms for comprehensive map support:

1. **Sensor Platform** (`sensor.py`)
   - Sensors now include `latitude` and `longitude` properties
   - Can be displayed on Home Assistant map cards
   - Provide representative locations for groups of issues

2. **Geo-location Platform** (`geo_location.py`)
   - Individual location markers for each notice/issue
   - Precise coordinates for each closure or stoppage
   - Better granularity than sensor-based locations

3. **Device Tracker Platform** (`device_tracker.py`) 
   - Alternative tracking entities (optional)
   - GPS-based location tracking for notices

### Map Card Configuration

Add maps to your dashboards using the standard Home Assistant map card:

```yaml
- type: map
  title: "🗺️ Waterway Issues Map"
  default_zoom: 6
  entities:
    - sensor.canal_river_trust_closures
    - sensor.canal_river_trust_stoppages
  geo_location_sources:
    - canal_river_trust
```

### Map Data Sources

#### Sensor Entities (Summary Locations)
- `sensor.canal_river_trust_closures`: Representative location for all closures
- `sensor.canal_river_trust_stoppages`: Representative location for all stoppages

These provide a single point representing the general area affected by issues.

#### Geo-location Events (Individual Locations)
Each individual notice creates a geo-location entity with:
- Precise coordinates from the Canal & River Trust API
- Issue-specific details (title, region, waterway, type, reason)
- Dynamic updates when data refreshes

#### Device Trackers (Alternative)
Optional device tracker entities for compatibility with systems that prefer this entity type.

## Technical Implementation

### Coordinate Extraction

The integration extracts coordinates from the Canal & River Trust API's GeoJSON geometry:

```python
def _extract_coordinates(geometry):
    """Extract coordinates from geometry object."""
    if geometry.get("type") == "Point":
        coords = geometry.get("coordinates")
        # Convert from [longitude, latitude] to [latitude, longitude]
        return (coords[1], coords[0]) if coords else None
```

### Location Properties

Sensor entities implement location properties:

```python
@property
def latitude(self) -> float | None:
    """Return latitude for map display."""
    location = self._get_representative_location(notices)
    return location[0] if location else None

@property
def longitude(self) -> float | None:
    """Return longitude for map display."""
    location = self._get_representative_location(notices)
    return location[1] if location else None
```

## Dashboard Integration

### Enhanced Dashboard Features

The enhanced dashboard (`enhanced_dashboard.yaml`) includes:

- **Interactive Map View**: Full-screen map with all issue markers
- **Map Information Panel**: Explains marker types and functionality
- **Coordinate Display**: Shows lat/lon coordinates in issue details
- **Regional Context**: Links map data with regional breakdowns

### Simple Dashboard Features

The simple dashboard (`simple_dashboard.yaml`) includes:

- **Basic Map Card**: Standard map with sensor entities
- **Map Usage Guide**: Simple instructions for map navigation
- **Regional Summary**: Text-based location information

## Configuration

### API Changes

The API client now requests geometry data:

```python
params = {
    "fields": "title,region,waterways,path,typeId,reasonId,programmeId,start,end,state,geometry"
}
```

### Platform Loading

Multiple platforms are loaded automatically:

```python
PLATFORMS: list[Platform] = [
    Platform.SENSOR, 
    Platform.DEVICE_TRACKER, 
    Platform.GEO_LOCATION
]
```

## Troubleshooting

### No Map Markers Visible

1. **Check Entity States**: Verify sensors have location data
   ```
   Developer Tools > States > Search "canal_river_trust"
   ```

2. **Check Geo-location Entities**: Look for entities starting with `geo_location.crt_`

3. **Verify API Data**: Check integration logs for geometry data in API responses

### Map Not Loading

1. **Check Map Card Configuration**: Ensure `geo_location_sources` includes `canal_river_trust`
2. **Browser Console**: Check for JavaScript errors
3. **Home Assistant Version**: Ensure you're running a compatible version

### Location Accuracy

- **Sensor Locations**: Provide representative points (less precise)
- **Geo-location Events**: Provide exact coordinates from Canal & River Trust
- **Accuracy**: Typically within 100 meters of actual waterway location

## Example Automations

### Location-based Notifications

```yaml
- alias: "Nearby Waterway Issues"
  trigger:
    - platform: state
      entity_id: sensor.canal_river_trust_closures
  condition:
    - condition: template
      value_template: >
        {% set lat = state_attr('sensor.canal_river_trust_closures', 'latitude') %}
        {% set lon = state_attr('sensor.canal_river_trust_closures', 'longitude') %}
        {% set home_lat = states.zone.home.attributes.latitude %}
        {% set home_lon = states.zone.home.attributes.longitude %}
        {{ distance(lat, lon, home_lat, home_lon) < 10 }}
  action:
    - service: notify.mobile_app
      data:
        message: "Waterway issue detected within 10km of home"
```

### Map-based Alerts

```yaml
- alias: "New Issue on Map"
  trigger:
    - platform: event
      event_type: geo_location_new
      event_data:
        source: canal_river_trust
  action:
    - service: persistent_notification.create
      data:
        message: "New waterway issue: {{ trigger.event.data.entity_id }}"
        title: "Canal & River Trust Alert"
```

## Future Enhancements

Planned improvements for map functionality:

1. **Clustering**: Group nearby issues to reduce map clutter
2. **Custom Icons**: Different marker styles for closure types
3. **Route Integration**: Integration with navigation systems
4. **Historical Tracking**: Show issue movement over time
5. **Proximity Zones**: Automatic zone creation around frequent issue areas
