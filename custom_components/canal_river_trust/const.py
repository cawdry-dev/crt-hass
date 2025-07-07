"""Constants for the Canal & River Trust integration."""

DOMAIN = "canal_river_trust"

# Configuration
CONF_UPDATE_INTERVAL = "update_interval"
CONF_LOCATION_FILTER = "location_filter"
CONF_INCLUDE_PLANNED = "include_planned"
CONF_INCLUDE_EMERGENCY = "include_emergency"

# Defaults
DEFAULT_UPDATE_INTERVAL = 30  # minutes
DEFAULT_INCLUDE_PLANNED = True
DEFAULT_INCLUDE_EMERGENCY = True

# API URLs
API_BASE_URL = "https://services1.arcgis.com/JNVHlsjck7xOTJJI/arcgis/rest/services"
CLOSURES_ENDPOINT = f"{API_BASE_URL}/Closures/FeatureServer/0/query"
STOPPAGES_ENDPOINT = f"{API_BASE_URL}/Stoppages/FeatureServer/0/query"

# API Parameters
API_PARAMS = {
    "where": "1=1",
    "outFields": "*",
    "f": "json",
    "returnGeometry": "false"
}

# Sensor attributes
ATTR_CLOSURES = "closures"
ATTR_STOPPAGES = "stoppages"
ATTR_LAST_UPDATED = "last_updated"
ATTR_LOCATION = "location"
ATTR_REASON = "reason"
ATTR_START_DATE = "start_date"
ATTR_END_DATE = "end_date"
ATTR_STATUS = "status"
ATTR_TYPE = "type"
ATTR_DESCRIPTION = "description"
