"""Device tracker platform for Canal & River Trust integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.device_tracker import SourceType, TrackerEntity
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
    """Set up Canal & River Trust device trackers based on a config entry."""
    coordinator: CanalRiverTrustCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Create device trackers for each notice with location data
    entities = []
    
    if coordinator.data:
        notices = coordinator.data.get("notices", [])
        for notice in notices:
            coordinates = _extract_coordinates(notice.get("geometry"))
            if coordinates:
                entities.append(CanalRiverTrustLocationTracker(coordinator, entry, notice))

    if entities:
        async_add_entities(entities)
        _LOGGER.info("Added %d location trackers", len(entities))


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


class CanalRiverTrustLocationTracker(CoordinatorEntity, TrackerEntity):
    """Device tracker for Canal & River Trust notice locations."""

    def __init__(
        self,
        coordinator: CanalRiverTrustCoordinator,
        entry: ConfigEntry,
        notice: dict[str, Any],
    ) -> None:
        """Initialize the location tracker."""
        super().__init__(coordinator)
        self._entry = entry
        self._notice = notice
        self._notice_id = notice.get("id", notice.get("title", "unknown"))
        
        # Generate unique entity ID based on notice ID or title
        safe_id = str(self._notice_id).lower().replace(" ", "_").replace("-", "_")
        safe_id = "".join(c for c in safe_id if c.isalnum() or c == "_")[:50]
        
        self._attr_unique_id = f"{entry.entry_id}_{safe_id}_location"
        self._attr_name = f"CRT {notice.get('title', 'Unknown Notice')}"
        
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
            "sw_version": "1.0.1",
            "configuration_url": "https://canalrivertrust.org.uk",
        }

    @property
    def source_type(self) -> SourceType:
        """Return the source type of the tracker."""
        return SourceType.GPS

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        coordinates = _extract_coordinates(self._notice.get("geometry"))
        return coordinates[0] if coordinates else None

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        coordinates = _extract_coordinates(self._notice.get("geometry"))
        return coordinates[1] if coordinates else None

    @property
    def location_accuracy(self) -> int:
        """Return the location accuracy of the device."""
        return 100  # Approximate accuracy in meters

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
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_update(self) -> None:
        """Update the tracker from coordinator data."""
        # Find the current notice data from coordinator
        if self.coordinator.data:
            notices = self.coordinator.data.get("notices", [])
            # Try to find this notice by ID or title
            for notice in notices:
                notice_id = notice.get("id", notice.get("title", "unknown"))
                if notice_id == self._notice_id:
                    self._notice = notice
                    break
