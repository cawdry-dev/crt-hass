"""Data update coordinator for Canal & River Trust integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import CanalRiverTrustAPI
from .const import (
    CONF_INCLUDE_EMERGENCY,
    CONF_INCLUDE_PLANNED,
    CONF_LOCATION_FILTER,
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class CanalRiverTrustCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching Canal & River Trust data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.entry = entry
        self.api = CanalRiverTrustAPI(async_get_clientsession(hass))
        
        update_interval = timedelta(
            minutes=entry.options.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
        )
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API."""
        try:
            data = await self.api.get_all_data()
            
            # Apply filters based on configuration
            filtered_data = self._apply_filters(data)
            
            return filtered_data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    def _apply_filters(self, data: dict[str, Any]) -> dict[str, Any]:
        """Apply user-configured filters to the data."""
        filtered_data = data.copy()
        
        # Filter by location if specified
        location_filter = self.entry.options.get(CONF_LOCATION_FILTER)
        if location_filter:
            filtered_data["closures"] = [
                closure for closure in data["closures"]
                if self._matches_location_filter(closure, location_filter)
            ]
            filtered_data["stoppages"] = [
                stoppage for stoppage in data["stoppages"]
                if self._matches_location_filter(stoppage, location_filter)
            ]
        
        # Filter by type preferences
        include_planned = self.entry.options.get(CONF_INCLUDE_PLANNED, True)
        include_emergency = self.entry.options.get(CONF_INCLUDE_EMERGENCY, True)
        
        if not include_planned:
            filtered_data["stoppages"] = [
                stoppage for stoppage in filtered_data["stoppages"]
                if not self._is_planned_stoppage(stoppage)
            ]
        
        if not include_emergency:
            filtered_data["closures"] = [
                closure for closure in filtered_data["closures"]
                if not self._is_emergency_closure(closure)
            ]
        
        return filtered_data

    def _matches_location_filter(self, item: dict[str, Any], location_filter: str) -> bool:
        """Check if an item matches the location filter."""
        location_fields = ["Location", "Waterway", "Canal", "River", "Area"]
        location_filter_lower = location_filter.lower()
        
        for field in location_fields:
            if field in item and item[field]:
                if location_filter_lower in str(item[field]).lower():
                    return True
        
        return False

    def _is_planned_stoppage(self, stoppage: dict[str, Any]) -> bool:
        """Check if a stoppage is planned."""
        stoppage_type = stoppage.get("Type", "").lower()
        return "planned" in stoppage_type or "maintenance" in stoppage_type

    def _is_emergency_closure(self, closure: dict[str, Any]) -> bool:
        """Check if a closure is emergency."""
        closure_type = closure.get("Type", "").lower()
        reason = closure.get("Reason", "").lower()
        return "emergency" in closure_type or "emergency" in reason
