"""API client for Canal & River Trust data."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any

import aiohttp

from .const import API_PARAMS, STOPPAGES_ENDPOINT

_LOGGER = logging.getLogger(__name__)


class CanalRiverTrustAPI:
    """API client for Canal & River Trust data."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self._session = session

    async def get_notices(self, start_date: str | None = None, end_date: str | None = None) -> list[dict[str, Any]]:
        """Get notices (stoppages/closures) from the API."""
        # Default to one year window if no dates provided
        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-%d")
        if not end_date:
            end_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        
        params = {
            **API_PARAMS,
            "start": start_date,
            "end": end_date
        }
        
        try:
            headers = {
                "User-Agent": "Home Assistant Canal & River Trust Integration/1.0.0"
            }
            
            _LOGGER.debug("Fetching notices from %s with params: %s", STOPPAGES_ENDPOINT, params)
            
            async with self._session.get(
                STOPPAGES_ENDPOINT,
                params=params,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    # Check content type to ensure we got JSON, not HTML
                    content_type = response.headers.get('content-type', '').lower()
                    if 'application/json' not in content_type and 'json' not in content_type:
                        error_text = await response.text()
                        if 'service unavailable' in error_text.lower() or 'html' in error_text.lower():
                            _LOGGER.error("API returned HTML error page instead of JSON data - service may be temporarily unavailable")
                            _LOGGER.debug("HTML response content: %s", error_text[:500] + "..." if len(error_text) > 500 else error_text)
                        else:
                            _LOGGER.error("API returned unexpected content type: %s", content_type)
                            _LOGGER.debug("Response content: %s", error_text[:500] + "..." if len(error_text) > 500 else error_text)
                        return []

                    try:
                        data = await response.json()
                        _LOGGER.debug("API response received with %d features", len(data.get("features", [])))

                        if isinstance(data, dict) and "features" in data:
                            # Extract properties from GeoJSON features
                            notices = []
                            for feature in data["features"]:
                                if "properties" in feature:
                                    notice = feature["properties"].copy()
                                    # Add geometry if present
                                    if "geometry" in feature and feature["geometry"]:
                                        notice["geometry"] = feature["geometry"]
                                    notices.append(notice)

                            _LOGGER.info("Successfully fetched %d notices", len(notices))
                            return notices
                        else:
                            _LOGGER.warning("Unexpected API response format: %s", type(data))
                            return []
                    except (ValueError, TypeError) as json_err:
                        error_text = await response.text()
                        _LOGGER.error("Failed to parse JSON response: %s", json_err)
                        _LOGGER.debug("Response content: %s", error_text[:500] + "..." if len(error_text) > 500 else error_text)
                        return []
                else:
                    _LOGGER.error("Failed to fetch notices: HTTP %s", response.status)
                    error_text = await response.text()
                    if 'service unavailable' in error_text.lower():
                        _LOGGER.error("Canal & River Trust API is temporarily unavailable - this is a temporary issue on their end")
                    else:
                        _LOGGER.error("Error response: %s", error_text[:500] + "..." if len(error_text) > 500 else error_text)
                    return []
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout while fetching notices")
            return []
        except Exception as err:
            _LOGGER.error("Error fetching notices: %s", err)
            return []

    async def get_all_data(self) -> dict[str, Any]:
        """Get all notice data with categorization."""
        notices = await self.get_notices()
        
        # Categorize notices by type
        closures = []
        stoppages = []
        
        for notice in notices:
            type_id = notice.get("typeId", 0)
            if type_id == 2:  # Closure type
                closures.append(notice)
            else:  # All other types treated as stoppages
                stoppages.append(notice)
        
        return {
            "notices": notices,
            "closures": closures,
            "stoppages": stoppages,
            "last_updated": datetime.now().isoformat()
        }
