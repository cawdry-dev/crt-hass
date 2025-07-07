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
    ATTR_CLOSURES,
    ATTR_LAST_UPDATED,
    ATTR_STOPPAGES,
    DOMAIN,
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
            "model": "Data Feed",
            "sw_version": "1.0.0",
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success


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
            ATTR_CLOSURES: [],
        }

        for closure in closures:
            closure_info = {
                "location": closure.get("Location", "Unknown"),
                "waterway": closure.get("Waterway", "Unknown"),
                "reason": closure.get("Reason", "Not specified"),
                "status": closure.get("Status", "Unknown"),
                "start_date": closure.get("StartDate"),
                "end_date": closure.get("EndDate"),
                "description": closure.get("Description", ""),
                "type": closure.get("Type", "Unknown"),
            }
            attributes[ATTR_CLOSURES].append(closure_info)

        return attributes


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
            ATTR_STOPPAGES: [],
        }

        for stoppage in stoppages:
            stoppage_info = {
                "location": stoppage.get("Location", "Unknown"),
                "waterway": stoppage.get("Waterway", "Unknown"),
                "type": stoppage.get("Type", "Unknown"),
                "status": stoppage.get("Status", "Unknown"),
                "start_date": stoppage.get("StartDate"),
                "end_date": stoppage.get("EndDate"),
                "description": stoppage.get("Description", ""),
                "reason": stoppage.get("Reason", "Not specified"),
            }
            attributes[ATTR_STOPPAGES].append(stoppage_info)

        return attributes
