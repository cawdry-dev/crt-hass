"""Constants for the Canal & River Trust integration."""

DOMAIN = "canal_river_trust"

# Configuration
CONF_UPDATE_INTERVAL = "update_interval"
CONF_LOCATION_FILTER = "location_filter"
CONF_INCLUDE_PLANNED = "include_planned"
CONF_INCLUDE_EMERGENCY = "include_emergency"

# Defaults
DEFAULT_UPDATE_INTERVAL = 240  # minutes (4 hours)
DEFAULT_INCLUDE_PLANNED = True
DEFAULT_INCLUDE_EMERGENCY = True

# API URLs
API_BASE_URL = "https://canalrivertrust.org.uk/api"
STOPPAGES_ENDPOINT = f"{API_BASE_URL}/stoppage/notices"

# API Parameters for stoppages (covers both closures and stoppages)
API_PARAMS = {
    "consult": "false",
    "geometry": "point",
    "fields": "title,region,waterways,path,typeId,reasonId,programmeId,start,end,state"
}

# Sensor attributes
ATTR_NOTICES = "notices"
ATTR_LAST_UPDATED = "last_updated"
ATTR_TITLE = "title"
ATTR_REGION = "region"
ATTR_WATERWAYS = "waterways"
ATTR_START_DATE = "start_date"
ATTR_END_DATE = "end_date"
ATTR_STATE = "state"
ATTR_TYPE_ID = "type_id"
ATTR_REASON_ID = "reason_id"
ATTR_PROGRAMME_ID = "programme_id"
ATTR_COORDINATES = "coordinates"

# Type mappings (based on API response)
TYPE_MAPPINGS = {
    1: "Stoppage",
    2: "Closure", 
    3: "Restriction",
    4: "Advisory"
}

# Reason mappings (these may need to be discovered from API)
REASON_MAPPINGS = {
    1: "Maintenance",
    2: "Lock Works",
    3: "Bridge Works", 
    4: "Emergency",
    5: "Water Level",
    6: "Vegetation"
}
