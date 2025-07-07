# Development Guide

## Setting up the Development Environment

### Prerequisites
- Python 3.11 or higher
- Home Assistant development environment
- Git

### Installation for Development

1. Clone the repository:
```bash
git clone https://github.com/cawdry/crt-hass.git
cd crt-hass
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements-dev.txt
```

### Testing the API Connection

Before integrating with Home Assistant, you can test the API connection:

```bash
python test_api.py
```

This will show you sample data from the Canal & River Trust API.

## Project Structure

```
custom_components/canal_river_trust/
├── __init__.py              # Integration setup
├── api.py                   # API client
├── config_flow.py           # Configuration UI
├── const.py                 # Constants
├── coordinator.py           # Data coordinator
├── manifest.json            # Integration metadata
├── sensor.py                # Sensor entities
├── services.yaml            # Service definitions
├── translations/            # UI translations
│   └── en.json
└── utils.py                 # Utility functions
```

## API Endpoints

The integration uses these Canal & River Trust API endpoints:

- **Closures**: `https://services1.arcgis.com/JNVHlsjck7xOTJJI/arcgis/rest/services/Closures/FeatureServer/0/query`
- **Stoppages**: `https://services1.arcgis.com/JNVHlsjck7xOTJJI/arcgis/rest/services/Stoppages/FeatureServer/0/query`

Both endpoints use ArcGIS REST API format with these parameters:
- `where=1=1` (get all records)
- `outFields=*` (get all fields)
- `f=json` (JSON format)
- `returnGeometry=false` (exclude geometry data)

## Data Structure

### Closures
Each closure typically contains:
- Location
- Waterway
- Reason
- Status
- Start/End dates
- Description
- Type

### Stoppages
Each stoppage typically contains:
- Location
- Waterway
- Type (planned, emergency, etc.)
- Status
- Start/End dates
- Description
- Reason

## Testing

### Manual Testing
1. Copy the integration to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Add the integration through Configuration → Integrations
4. Monitor the logs for any errors

### Automated Testing
```bash
# Run linting
pylint custom_components/canal_river_trust/

# Run type checking
mypy custom_components/canal_river_trust/

# Run tests (when implemented)
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

## Known Limitations

1. **No Geometry Data**: Currently, the integration doesn't use GPS coordinates from the API
2. **Limited Filtering**: Location filtering is basic string matching
3. **No Map Integration**: No visual map representation of closures/stoppages
4. **API Rate Limits**: Unknown if the CRT API has rate limits

## Future Enhancements

1. **Map Integration**: Add GPS coordinates and map visualization
2. **Enhanced Filtering**: More sophisticated location and type filtering
3. **Notifications**: Push notifications for new issues
4. **Historical Data**: Store and analyze historical closure/stoppage data
5. **Proximity Alerts**: Alerts based on distance from user's location
6. **Route Planning**: Integration with navigation apps to avoid closures

## Troubleshooting

### Common Issues

1. **No Data Appearing**
   - Check Home Assistant logs for API errors
   - Verify internet connectivity
   - Test API endpoints manually

2. **Integration Not Loading**
   - Check `manifest.json` syntax
   - Verify all required files are present
   - Check Python syntax errors

3. **Configuration Errors**
   - Validate `config_flow.py` schema
   - Check translation files

### Debug Mode

Enable debug logging in Home Assistant:

```yaml
logger:
  default: info
  logs:
    custom_components.canal_river_trust: debug
```
