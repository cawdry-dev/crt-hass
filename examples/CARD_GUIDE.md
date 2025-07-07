# Canal & River Trust Dashboard Card Guide

## ✅ VERIFIED Working Cards

### Built-in Home Assistant Cards (Always Available)
These cards work out of the box with no additional installations:

1. **`entity`** - Basic entity display
2. **`entities`** - List of entities
3. **`gauge`** - Circular gauge display
4. **`history-graph`** - Historical data trends
5. **`horizontal-stack`** - Side-by-side layout
6. **`vertical-stack`** - Top-to-bottom layout
7. **`markdown`** - Rich text with templates
8. **`map`** - Geographic map view
9. **`statistic`** - Statistical display
10. **`conditional`** - Show/hide based on conditions
11. **`alert`** - Alert notifications

### Custom Cards (Require HACS Installation)
These are REAL custom cards available in HACS:

1. **`custom:mini-graph-card`** - Compact trend graphs
2. **`custom:apexcharts-card`** - Advanced charts and graphs
3. **`custom:auto-entities`** - Dynamic entity lists
4. **`custom:mushroom-entity-card`** - Modern, clean entity cards
5. **`custom:fold-entity-row`** - Collapsible entity rows

## ❌ Cards That DON'T Exist
Avoid these - they were mentioned in error:

- ~~`custom:timeline-card`~~ - Not a real card
- ~~`custom:banner-card`~~ - Not a real card
- ~~`custom:weather-card`~~ - Not for this purpose
- ~~`custom:animated-background`~~ - Not a real card
- ~~`custom:stack-in-card`~~ - Not a real card
- ~~`custom:mushroom-chips-card`~~ - Not a real card
- ~~`custom:multiple-entity-row`~~ - Not a real card

## 🎯 Recommended Setup

### For Beginners (No Custom Cards)
Use `examples/simple_dashboard.yaml` - works immediately with:
- Entity cards for status
- Gauge for activity level
- History graph for trends
- Markdown for summaries
- Map for locations

### For Advanced Users (With HACS)
Install these custom cards first:
```bash
# In HACS, search for and install:
- "Mini Graph Card"
- "ApexCharts Card" 
- "Auto-entities"
```

Then use `examples/enhanced_dashboard.yaml` for:
- Mini graphs with trends
- Donut charts for regional data
- Auto-generated entity lists

## 🚀 Quick Start

1. **Copy** `examples/simple_dashboard.yaml` content
2. **Paste** into your Lovelace dashboard
3. **Customize** entity names if needed
4. **Enjoy** your waterway monitoring dashboard!

## 📊 Available Data

Your sensors provide rich data including:
- **Coordinates** - For map plotting
- **Regions** - For geographic breakdown  
- **Waterways** - Specific canal/river names
- **Dates** - Start/end times
- **Reasons** - Why the issue occurred
- **Types** - Closure, stoppage, etc.

All of this can be displayed using the working cards above!
