"""Config flow for Canal & River Trust integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import (
    CONF_INCLUDE_EMERGENCY,
    CONF_INCLUDE_PLANNED,
    CONF_LOCATION_FILTER,
    CONF_UPDATE_INTERVAL,
    DEFAULT_INCLUDE_EMERGENCY,
    DEFAULT_INCLUDE_PLANNED,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default="Canal & River Trust"): str,
        vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): vol.All(
            vol.Coerce(int), vol.Range(min=5, max=1440)
        ),
        vol.Optional(CONF_LOCATION_FILTER): str,
        vol.Optional(CONF_INCLUDE_PLANNED, default=DEFAULT_INCLUDE_PLANNED): bool,
        vol.Optional(CONF_INCLUDE_EMERGENCY, default=DEFAULT_INCLUDE_EMERGENCY): bool,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Canal & River Trust."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate that we can connect to the API
            try:
                # Test API connection
                await self._test_connection()
                
                return self.async_create_entry(
                    title=user_input.get(CONF_NAME, "Canal & River Trust"),
                    data={},
                    options=user_input,
                )
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def _test_connection(self) -> None:
        """Test connection to the Canal & River Trust API."""
        from .api import CanalRiverTrustAPI
        from homeassistant.helpers.aiohttp_client import async_get_clientsession
        
        session = async_get_clientsession(self.hass)
        api = CanalRiverTrustAPI(session)
        
        # Try to fetch a small amount of data to test the connection
        await api.get_notices()

    @staticmethod
    @config_entries.callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> OptionsFlowHandler:
        """Create the options flow."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Canal & River Trust."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_UPDATE_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=5, max=1440)),
                    vol.Optional(
                        CONF_LOCATION_FILTER,
                        default=self.config_entry.options.get(CONF_LOCATION_FILTER, ""),
                    ): str,
                    vol.Optional(
                        CONF_INCLUDE_PLANNED,
                        default=self.config_entry.options.get(
                            CONF_INCLUDE_PLANNED, DEFAULT_INCLUDE_PLANNED
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_INCLUDE_EMERGENCY,
                        default=self.config_entry.options.get(
                            CONF_INCLUDE_EMERGENCY, DEFAULT_INCLUDE_EMERGENCY
                        ),
                    ): bool,
                }
            ),
        )
