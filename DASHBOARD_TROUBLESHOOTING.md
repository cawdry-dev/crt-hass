# Dashboard Troubleshooting Guide

## Common Dashboard Configuration Issues

### 1. Entity Not Found Errors

**Problem:** Dashboard shows "Entity not available" or "Unknown entity"

**Solution:** Verify the correct sensor entity IDs:
- `sensor.canal_river_trust_closures`
- `sensor.canal_river_trust_stoppages`
- `sensor.canal_river_trust_emergency_issues`
- `sensor.canal_river_trust_regional_breakdown`
- `sensor.canal_river_trust_upcoming_issues`

**Check:** Go to Developer Tools > States and search for "canal_river_trust" to see all available entities.

### 2. Custom Card Errors

**Problem:** Dashboard shows "Custom element doesn't exist" errors

**Solution:** The enhanced dashboard was updated to remove all custom cards. Use only:
- `enhanced_dashboard.yaml` - Advanced features with built-in cards only
- `simple_dashboard.yaml` - Basic functionality with minimal card types

### 3. Template Errors in Markdown Cards

**Problem:** Markdown cards show template errors or "None" values

**Common fixes:**
```yaml
# Wrong:
{{ states('sensor.non_existent_sensor') }}

# Correct:
{{ states('sensor.canal_river_trust_closures') or '0' }}
{{ state_attr('sensor.canal_river_trust_closures', 'last_updated') or 'Never' }}
```

### 4. Map Card Issues

**Problem:** Map card not displaying sensor data correctly

**Solution:** The sensors don't provide location data in the format expected by the map card. Use the regional breakdown instead:

```yaml
- type: markdown
  title: "📍 Regional Information"
  content: |
    {% set regional = state_attr('sensor.canal_river_trust_regional_breakdown', 'regional_breakdown') or {} %}
    {% for region, data in regional.items() %}
    **{{ region }}:** {{ data.total }} issues
    {% endfor %}
```

### 5. Statistics Card Errors

**Problem:** Statistics cards showing "Unknown" or errors

**Solution:** Use entity cards instead of statistics cards:

```yaml
# Instead of statistic card:
- type: entity
  entity: sensor.canal_river_trust_closures
  name: "Total Closures"
```

## Recommended Dashboard Files

### For New Users
Use `simple_dashboard.yaml` - minimal configuration with basic cards only.

### For Advanced Users  
Use `enhanced_dashboard.yaml` - comprehensive dashboard with all features using built-in cards.

### For Custom Setups
Start with `simple_dashboard.yaml` and add cards gradually, testing each addition.

## Validation Steps

1. **Check Entity Availability:**
   ```
   Developer Tools > States > Search "canal_river_trust"
   ```

2. **Validate Dashboard YAML:**
   - Use YAML validation tools
   - Check for proper indentation
   - Verify entity names match exactly

3. **Test Dashboard:**
   - Add one card at a time
   - Check browser console for errors
   - Use simple entity cards first

## Getting Help

If issues persist:

1. Check the Home Assistant logs for error messages
2. Verify the Canal & River Trust integration is loaded and working
3. Test individual sensors in Developer Tools
4. Start with the simple dashboard and add complexity gradually

## API and Data Issues

If sensors show "0" or "Unknown":

1. Check integration configuration
2. Verify internet connectivity
3. Check Home Assistant logs for API errors
4. The integration updates every 4 hours by default
