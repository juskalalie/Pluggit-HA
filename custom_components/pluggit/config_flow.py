import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries

from .const import CONFIG_HOST, DOMAIN
from .pypluggit.pluggit import Pluggit

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {vol.Required(CONFIG_HOST, description={"suggested_value": "192.168.0.1"}): str}
)


async def validate_input(data: dict[str, Any]) -> str:
    """Check for Host and try to get serial number"""

    host = data[CONFIG_HOST]
    pluggit = Pluggit(host)

    serial_number = pluggit.get_serial_number()

    return serial_number


class PluggitConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Pluggit."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        _LOGGER.info(user_input)

        if user_input is not None:
            _LOGGER.info(user_input)
            ret = await validate_input(user_input)
            _LOGGER.info(ret)
            return self.async_create_entry(title="Pluggit", data=user_input)

        return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)
