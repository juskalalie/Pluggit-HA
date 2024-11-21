"""The Pluggit integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONFIG_HOST, DOMAIN
from .pypluggit.pluggit import Pluggit

PLATFORMS = [Platform.FAN]
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up pluggit from a config entry."""
    _LOGGER.debug("Hhuhu setup entry")

    hass.data.setdefault(DOMAIN, {})

    hass.data[DOMAIN][entry.entry_id] = Pluggit(entry.data[CONFIG_HOST])
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload pluggit config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
