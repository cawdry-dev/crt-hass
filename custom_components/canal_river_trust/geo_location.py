"""Geo location platform for Canal & River Trust integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.geo_location import GeolocationEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, REASON_MAPPINGS, TYPE_MAPPINGS
from .coordinator import CanalRiverTrustCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Canal & River Trust geo location events based on a config entry."""
    coordinator: CanalRiverTrustCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Create geo location events for each notice with location data
    entities = []
    
    if coordinator.data:
        notices = coordinator.data.get("notices", [])
        for idx, notice in enumerate(notices):
            coordinates = _extract_coordinates(notice.get("geometry"))
            if coordinates:
                entities.append(CanalRiverTrustGeolocationEvent(coordinator, entry, notice, idx))

    if entities:
        async_add_entities(entities, True)
        _LOGGER.info("Added %d geo location events", len(entities))


def _extract_coordinates(geometry: dict[str, Any] | None) -> tuple[float, float] | None:
    """Extract coordinates from geometry object and return as (lat, lon)."""
    if not geometry:
        return None
    
    coordinates = None
    if geometry.get("type") == "GeometryCollection":
        geometries = geometry.get("geometries", [])
        if geometries and geometries[0].get("type") == "Point":
            coordinates = geometries[0].get("coordinates")
    elif geometry.get("type") == "Point":
        coordinates = geometry.get("coordinates")
    
    if coordinates and len(coordinates) >= 2:
        # GeoJSON coordinates are [longitude, latitude], but we need [latitude, longitude]
        return (coordinates[1], coordinates[0])
    
    return None


class CanalRiverTrustGeolocationEvent(CoordinatorEntity, GeolocationEvent):
    """Geo location event for Canal & River Trust notices."""

    def __init__(
        self,
        coordinator: CanalRiverTrustCoordinator,
        entry: ConfigEntry,
        notice: dict[str, Any],
        index: int,
    ) -> None:
        """Initialize the geo location event."""
        super().__init__(coordinator)
        self._entry = entry
        self._notice = notice
        self._index = index
        
        # Generate unique entity ID
        title = notice.get("title", f"notice_{index}")
        safe_id = title.lower().replace(" ", "_").replace("-", "_")
        safe_id = "".join(c for c in safe_id if c.isalnum() or c == "_")[:50]
        
        self._attr_unique_id = f"{entry.entry_id}_geo_{safe_id}_{index}"
        self._attr_name = f"CRT {title}"
        
        # Set icon based on type
        type_id = notice.get("typeId", 0)
        if type_id == 2:  # Closure
            self._attr_icon = "mdi:lock-alert"
        else:  # Stoppage or other
            self._attr_icon = "mdi:construction"

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": "Canal & River Trust",
            "manufacturer": "Canal & River Trust",
            "model": "Waterway Data Feed",
            "sw_version": "1.0.2",
            "configuration_url": "https://canalrivertrust.org.uk",
        }

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the event."""
        coordinates = _extract_coordinates(self._notice.get("geometry"))
        return coordinates[0] if coordinates else None

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the event."""
        coordinates = _extract_coordinates(self._notice.get("geometry"))
        return coordinates[1] if coordinates else None

    @property
    def distance(self) -> float | None:
        """Return distance from home in km."""
        # This would require calculating distance from Home Assistant's location
        # For now, return None to indicate unknown distance
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        notice = self._notice
        return {
            "title": notice.get("title", "Unknown"),
            "region": notice.get("region", "Unknown"),
            "waterways": notice.get("waterways", "Unknown"),
            "type": TYPE_MAPPINGS.get(notice.get("typeId", 0), "Unknown"),
            "reason": REASON_MAPPINGS.get(notice.get("reasonId", 0), "Unknown"),
            "start_date": notice.get("start"),
            "end_date": notice.get("end"),
            "state": notice.get("state", "Unknown"),
            "programme_id": notice.get("programmeId"),
            "source": DOMAIN,
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_update(self) -> None:
        """Update the event from coordinator data."""
        # Find the current notice data from coordinator
        if self.coordinator.data:
            notices = self.coordinator.data.get("notices", [])
            if self._index < len(notices):
                self._notice = notices[self._index]
