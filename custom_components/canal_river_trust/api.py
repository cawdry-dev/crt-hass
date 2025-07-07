"""API client for Canal & River Trust data."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Any

import aiohttp

from .const import API_PARAMS, CLOSURES_ENDPOINT, STOPPAGES_ENDPOINT

_LOGGER = logging.getLogger(__name__)


class CanalRiverTrustAPI:
    """API client for Canal & River Trust data."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self._session = session

    async def get_closures(self) -> list[dict[str, Any]]:
        """Get current closures from the API."""
        try:
            async with self._session.get(
                CLOSURES_ENDPOINT, 
                params=API_PARAMS,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if "features" in data:
                        return [feature["attributes"] for feature in data["features"]]
                    return []
                else:
                    _LOGGER.error("Failed to fetch closures: HTTP %s", response.status)
                    return []
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout while fetching closures")
            return []
        except Exception as err:
            _LOGGER.error("Error fetching closures: %s", err)
            return []

    async def get_stoppages(self) -> list[dict[str, Any]]:
        """Get current stoppages from the API."""
        try:
            async with self._session.get(
                STOPPAGES_ENDPOINT, 
                params=API_PARAMS,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if "features" in data:
                        return [feature["attributes"] for feature in data["features"]]
                    return []
                else:
                    _LOGGER.error("Failed to fetch stoppages: HTTP %s", response.status)
                    return []
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout while fetching stoppages")
            return []
        except Exception as err:
            _LOGGER.error("Error fetching stoppages: %s", err)
            return []

    async def get_all_data(self) -> dict[str, Any]:
        """Get both closures and stoppages."""
        closures_task = self.get_closures()
        stoppages_task = self.get_stoppages()
        
        closures, stoppages = await asyncio.gather(
            closures_task, stoppages_task, return_exceptions=True
        )
        
        # Handle exceptions
        if isinstance(closures, Exception):
            _LOGGER.error("Error getting closures: %s", closures)
            closures = []
        
        if isinstance(stoppages, Exception):
            _LOGGER.error("Error getting stoppages: %s", stoppages)
            stoppages = []
        
        return {
            "closures": closures,
            "stoppages": stoppages,
            "last_updated": datetime.now().isoformat()
        }
