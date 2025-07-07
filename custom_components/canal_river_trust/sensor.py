"""Sensor platform for Canal & River Trust integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_LAST_UPDATED,
    ATTR_NOTICES,
    DOMAIN,
    REASON_MAPPINGS,
    TYPE_MAPPINGS,
)
from .coordinator import CanalRiverTrustCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Canal & River Trust sensors based on a config entry."""
    coordinator: CanalRiverTrustCoordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        CanalRiverTrustClosuresSensor(coordinator, entry),
        CanalRiverTrustStoppagesSensor(coordinator, entry),
        CanalRiverTrustEmergencySensor(coordinator, entry),
        CanalRiverTrustRegionalSensor(coordinator, entry),
        CanalRiverTrustUpcomingSensor(coordinator, entry),
    ]

    async_add_entities(sensors)


class CanalRiverTrustSensorBase(CoordinatorEntity, SensorEntity):
    """Base class for Canal & River Trust sensors."""

    def __init__(
        self,
        coordinator: CanalRiverTrustCoordinator,
        entry: ConfigEntry,
        sensor_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._sensor_type = sensor_type
        self._attr_unique_id = f"{entry.entry_id}_{sensor_type}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Canal & River Trust",
            "manufacturer": "Canal & River Trust",
            "model": "Waterway Data Feed",
            "sw_version": "1.0.1",
            "configuration_url": "https://canalrivertrust.org.uk",
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    def _extract_coordinates(self, geometry: dict[str, Any] | None) -> list[float] | None:
        """Extract coordinates from geometry object."""
        if not geometry:
            return None
        
        if geometry.get("type") == "GeometryCollection":
            geometries = geometry.get("geometries", [])
            if geometries and geometries[0].get("type") == "Point":
                return geometries[0].get("coordinates")
        elif geometry.get("type") == "Point":
            return geometry.get("coordinates")
        
        return None

    def _get_representative_location(self, notices: list[dict[str, Any]]) -> tuple[float, float] | None:
        """Get a representative location from a list of notices."""
        valid_coords = []
        for notice in notices:
            coords = self._extract_coordinates(notice.get("geometry"))
            if coords and len(coords) >= 2:
                # Convert from [longitude, latitude] to [latitude, longitude]
                valid_coords.append((coords[1], coords[0]))
        
        if not valid_coords:
            return None
        
        # Return the first valid coordinate as representative location
        # In future versions, this could be enhanced to return center of all points
        return valid_coords[0]


class CanalRiverTrustClosuresSensor(CanalRiverTrustSensorBase):
    """Sensor for Canal & River Trust closures."""

    def __init__(
        self,
        coordinator: CanalRiverTrustCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the closures sensor."""
        super().__init__(coordinator, entry, "closures")
        self._attr_name = "Canal & River Trust Closures"
        self._attr_icon = "mdi:lock"
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return 0
        return len(self.coordinator.data.get("closures", []))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if self.coordinator.data is None:
            return {}

        closures = self.coordinator.data.get("closures", [])
        last_updated = self.coordinator.data.get("last_updated")

        attributes = {
            ATTR_LAST_UPDATED: last_updated,
            "closures": [],
        }

        for closure in closures:
            closure_info = {
                "title": closure.get("title", "Unknown"),
                "region": closure.get("region", "Unknown"),
                "waterways": closure.get("waterways", "Unknown"),
                "type": TYPE_MAPPINGS.get(closure.get("typeId", 0), "Unknown"),
                "reason": REASON_MAPPINGS.get(closure.get("reasonId", 0), "Unknown"),
                "start_date": closure.get("start"),
                "end_date": closure.get("end"),
                "state": closure.get("state", "Unknown"),
                "coordinates": self._extract_coordinates(closure.get("geometry")),
            }
            attributes["closures"].append(closure_info)

        return attributes

    @property
    def latitude(self) -> float | None:
        """Return latitude for map display."""
        if self.coordinator.data is None:
            return None
        
        closures = self.coordinator.data.get("closures", [])
        location = self._get_representative_location(closures)
        return location[0] if location else None

    @property
    def longitude(self) -> float | None:
        """Return longitude for map display."""
        if self.coordinator.data is None:
            return None
        
        closures = self.coordinator.data.get("closures", [])
        location = self._get_representative_location(closures)
        return location[1] if location else None


class CanalRiverTrustStoppagesSensor(CanalRiverTrustSensorBase):
    """Sensor for Canal & River Trust stoppages."""

    def __init__(
        self,
        coordinator: CanalRiverTrustCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the stoppages sensor."""
        super().__init__(coordinator, entry, "stoppages")
        self._attr_name = "Canal & River Trust Stoppages"
        self._attr_icon = "mdi:stop"
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return 0
        return len(self.coordinator.data.get("stoppages", []))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if self.coordinator.data is None:
            return {}

        stoppages = self.coordinator.data.get("stoppages", [])
        last_updated = self.coordinator.data.get("last_updated")

        attributes = {
            ATTR_LAST_UPDATED: last_updated,
            "stoppages": [],
        }

        for stoppage in stoppages:
            stoppage_info = {
                "title": stoppage.get("title", "Unknown"),
                "region": stoppage.get("region", "Unknown"),
                "waterways": stoppage.get("waterways", "Unknown"),
                "type": TYPE_MAPPINGS.get(stoppage.get("typeId", 0), "Unknown"),
                "reason": REASON_MAPPINGS.get(stoppage.get("reasonId", 0), "Unknown"),
                "start_date": stoppage.get("start"),
                "end_date": stoppage.get("end"),
                "state": stoppage.get("state", "Unknown"),
                "coordinates": self._extract_coordinates(stoppage.get("geometry")),
            }
            attributes["stoppages"].append(stoppage_info)

        return attributes

    @property
    def latitude(self) -> float | None:
        """Return latitude for map display."""
        if self.coordinator.data is None:
            return None
        
        stoppages = self.coordinator.data.get("stoppages", [])
        location = self._get_representative_location(stoppages)
        return location[0] if location else None

    @property
    def longitude(self) -> float | None:
        """Return longitude for map display."""
        if self.coordinator.data is None:
            return None
        
        stoppages = self.coordinator.data.get("stoppages", [])
        location = self._get_representative_location(stoppages)
        return location[1] if location else None


class CanalRiverTrustEmergencySensor(CanalRiverTrustSensorBase):
    """Sensor for emergency Canal & River Trust issues."""

    def __init__(
        self,
        coordinator: CanalRiverTrustCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the emergency sensor."""
        super().__init__(coordinator, entry, "emergency")
        self._attr_name = "Canal & River Trust Emergency Issues"
        self._attr_icon = "mdi:alert-circle"
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return 0

        all_notices = self.coordinator.data.get("notices", [])
        emergency_count = sum(1 for notice in all_notices
                            if notice.get("reasonId") == 4)  # Emergency reason ID
        return emergency_count

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if self.coordinator.data is None:
            return {}

        all_notices = self.coordinator.data.get("notices", [])
        emergency_notices = [notice for notice in all_notices
                           if notice.get("reasonId") == 4]

        attributes = {
            ATTR_LAST_UPDATED: self.coordinator.data.get("last_updated"),
            "emergency_issues": [],
        }

        for notice in emergency_notices:
            notice_info = {
                "title": notice.get("title", "Unknown"),
                "region": notice.get("region", "Unknown"),
                "waterways": notice.get("waterways", "Unknown"),
                "type": TYPE_MAPPINGS.get(notice.get("typeId", 0), "Unknown"),
                "start_date": notice.get("start"),
                "end_date": notice.get("end"),
                "coordinates": self._extract_coordinates(notice.get("geometry")),
            }
            attributes["emergency_issues"].append(notice_info)

        return attributes


class CanalRiverTrustRegionalSensor(CanalRiverTrustSensorBase):
    """Sensor showing regional breakdown of issues."""

    def __init__(
        self,
        coordinator: CanalRiverTrustCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the regional sensor."""
        super().__init__(coordinator, entry, "regional")
        self._attr_name = "Canal & River Trust Regional Summary"
        self._attr_icon = "mdi:map-marker-multiple"
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> int:
        """Return the number of regions with issues."""
        if self.coordinator.data is None:
            return 0

        all_notices = self.coordinator.data.get("notices", [])
        regions = set(notice.get("region", "Unknown") for notice in all_notices)
        return len(regions)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if self.coordinator.data is None:
            return {}

        all_notices = self.coordinator.data.get("notices", [])
        regional_breakdown = {}

        for notice in all_notices:
            region = notice.get("region", "Unknown")
            if region not in regional_breakdown:
                regional_breakdown[region] = {"closures": 0, "stoppages": 0, "total": 0}

            regional_breakdown[region]["total"] += 1
            if notice.get("typeId") == 2:  # Closure
                regional_breakdown[region]["closures"] += 1
            else:
                regional_breakdown[region]["stoppages"] += 1

        attributes = {
            ATTR_LAST_UPDATED: self.coordinator.data.get("last_updated"),
            "regional_breakdown": regional_breakdown,
            "most_affected_region": max(regional_breakdown.keys(),
                                      key=lambda k: regional_breakdown[k]["total"])
                                    if regional_breakdown else "None",
        }

        return attributes


class CanalRiverTrustUpcomingSensor(CanalRiverTrustSensorBase):
    """Sensor for upcoming Canal & River Trust issues."""

    def __init__(
        self,
        coordinator: CanalRiverTrustCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the upcoming sensor."""
        super().__init__(coordinator, entry, "upcoming")
        self._attr_name = "Canal & River Trust Upcoming Issues"
        self._attr_icon = "mdi:calendar-clock"
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> int:
        """Return the number of upcoming issues."""
        if self.coordinator.data is None:
            return 0

        from datetime import datetime, timedelta

        all_notices = self.coordinator.data.get("notices", [])
        upcoming_count = 0
        now = datetime.now()
        next_week = now + timedelta(days=7)

        for notice in all_notices:
            start_date_str = notice.get("start")
            if start_date_str:
                try:
                    # Parse the date string and make it timezone-naive for comparison
                    if 'T' in start_date_str:
                        # ISO format with time
                        start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
                        start_date = start_date.replace(tzinfo=None)  # Make timezone-naive
                    else:
                        # Date only format
                        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')

                    if now <= start_date <= next_week:
                        upcoming_count += 1
                except (ValueError, AttributeError):
                    continue

        return upcoming_count

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if self.coordinator.data is None:
            return {}

        from datetime import datetime, timedelta

        all_notices = self.coordinator.data.get("notices", [])
        upcoming_notices = []
        now = datetime.now()
        next_week = now + timedelta(days=7)

        for notice in all_notices:
            start_date_str = notice.get("start")
            if start_date_str:
                try:
                    # Parse the date string and make it timezone-naive for comparison
                    if 'T' in start_date_str:
                        # ISO format with time
                        start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
                        start_date = start_date.replace(tzinfo=None)  # Make timezone-naive
                    else:
                        # Date only format
                        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')

                    if now <= start_date <= next_week:
                        notice_info = {
                            "title": notice.get("title", "Unknown"),
                            "region": notice.get("region", "Unknown"),
                            "waterways": notice.get("waterways", "Unknown"),
                            "type": TYPE_MAPPINGS.get(notice.get("typeId", 0), "Unknown"),
                            "reason": REASON_MAPPINGS.get(notice.get("reasonId", 0), "Unknown"),
                            "start_date": notice.get("start"),
                            "end_date": notice.get("end"),
                            "days_until": (start_date - now).days,
                            "coordinates": self._extract_coordinates(notice.get("geometry")),
                        }
                        upcoming_notices.append(notice_info)
                except (ValueError, AttributeError):
                    continue

        # Sort by start date
        upcoming_notices.sort(key=lambda x: x.get("start_date", ""))

        attributes = {
            ATTR_LAST_UPDATED: self.coordinator.data.get("last_updated"),
            "upcoming_issues": upcoming_notices,
        }

        return attributes
