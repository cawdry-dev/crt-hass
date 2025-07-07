# 🗺️ Map Setup Guide for Canal & River Trust Data

## Quick Start (5 minutes)

### Step 1: Basic Map
Add this card to your dashboard for an instant map view:

```yaml
type: map
title: "🗺️ Waterway Issues"
default_zoom: 6
entities:
  - sensor.canal_river_trust_closures
  - sensor.canal_river_trust_stoppages
```

### Step 2: Enhanced Map with Details
Copy the configuration from `simple_map_setup.yaml` for a complete map experience.

## 🎯 What You'll Get

### ✅ Working Features:
1. **Interactive Map** - Shows issue locations as markers
2. **Clickable Coordinates** - Links to Google Maps for exact locations
3. **Issue Details** - Title, location, reason, dates for each issue
4. **Regional Breakdown** - See which areas are most affected
5. **Status Summary** - Quick overview of total issues

### 📍 Map Markers:
- **Red markers** - Closures (🔒)
- **Orange markers** - Stoppages (🚧)  
- **Dark red markers** - Emergency issues (🚨)

## 🔧 How It Works

### Data Source:
The sensors already extract GPS coordinates from the Canal & River Trust API:
- Each issue includes `coordinates: [longitude, latitude]`
- The sensors have `latitude` and `longitude` properties for map display
- Home Assistant automatically plots these on the map

### Coordinate Format:
- **API provides**: `[longitude, latitude]` (e.g., `[-2.1234, 52.5678]`)
- **Map expects**: `latitude, longitude` (automatically converted)
- **Google Maps links**: Use `latitude,longitude` format

## 📱 Usage Tips

### 🗺️ Map Navigation:
- **Zoom in/out** - Use mouse wheel or touch gestures
- **Pan around** - Click and drag to move the map
- **Click markers** - Shows entity details popup
- **Full screen** - Click the expand icon

### 📍 Finding Specific Issues:
1. Look at the coordinate list below the map
2. Click any GPS coordinate link to open Google Maps
3. Use the regional breakdown to focus on specific areas

### 🔍 Filtering by Region:
The regional sensor shows which areas have the most issues:
- Check `sensor.canal_river_trust_regional_summary` attributes
- Use the regional map links to focus on specific areas

## 🚀 Advanced Options

### Custom Zoom Levels:
```yaml
default_zoom: 8  # Closer view
default_zoom: 5  # Wider view
```

### Focus on Specific Area:
```yaml
default_zoom: 10
geo_location_sources:
  - canal_river_trust
```

### Add More Entities:
```yaml
entities:
  - sensor.canal_river_trust_closures
  - sensor.canal_river_trust_stoppages
  - sensor.canal_river_trust_emergency_issues
  - sensor.canal_river_trust_upcoming_issues
```

## 🔧 Troubleshooting

### No Markers Showing?
1. Check that sensors have data: `Developer Tools > States`
2. Verify coordinates exist in sensor attributes
3. Ensure sensors have `latitude` and `longitude` properties

### Markers in Wrong Location?
- The API provides coordinates in `[longitude, latitude]` format
- Home Assistant expects `latitude` first - this is handled automatically
- If still wrong, check the coordinate extraction in `sensor.py`

### Map Not Loading?
1. Check internet connection
2. Verify Home Assistant can access map tiles
3. Try refreshing the page

## 📊 Data Available

Each marker shows:
- **Title** - Description of the issue
- **Location** - Waterway and region
- **Type** - Closure, stoppage, restriction, etc.
- **Reason** - Maintenance, emergency, etc.
- **Dates** - Start and end times
- **Coordinates** - Exact GPS location

## 🎨 Customization

### Change Map Style:
Home Assistant uses OpenStreetMap by default. For custom tiles, you'd need additional configuration.

### Marker Colors:
The built-in map uses entity icons and states to determine marker appearance.

### Add Custom Info:
Modify the markdown sections in the configuration to show different details.

## 📱 Mobile Friendly

The map configuration works great on mobile devices:
- Touch gestures for navigation
- Responsive layout
- Clickable coordinate links open in mobile Google Maps app

Enjoy exploring your waterway data on the map! 🚢🗺️
