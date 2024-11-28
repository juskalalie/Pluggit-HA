"""Button"""
import logging
from dataclasses import dataclass
from typing import Callable
from homeassistant.components.button import (
    ButtonEntity, ButtonEntityDescription
)
from homeassistant.const import EntityCategory
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback


from .const import DOMAIN, SERIAL_NUMBER
from .pypluggit.pluggit import Pluggit

_LOGGER = logging.getLogger(__name__)


@dataclass(kw_only=True)
class PluggitButtonEntityDescription(ButtonEntityDescription):
    """Describes Pluggit button entity."""

    set_fn: Callable[[Pluggit], None]


BUTTONS: tuple[PluggitButtonEntityDescription, ...] = (
    PluggitButtonEntityDescription(
        key="filter_reset",
        translation_key="filter_reset",
        set_fn=lambda device: device.reset_filter()
    ),
    PluggitButtonEntityDescription(
        key="date_time",
        translation_key="date_time",
        set_fn=lambda device: device.set_date_time()
    )
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    data = hass.data[DOMAIN][entry.entry_id]
    pluggit: Pluggit = data[DOMAIN]
    serial_number = data[SERIAL_NUMBER]

    async_add_entities(
        (
            PluggitButton(
                pluggit=pluggit, serial_number=serial_number, description=description
            )
            for description in BUTTONS
        ),
        update_before_add=True,
    )


class PluggitButton(ButtonEntity):
    entity_description: PluggitButtonEntityDescription
    _attr_entity_category = EntityCategory.CONFIG
    _attr_has_entity_name = True

    def __init__(
        self,
        pluggit: Pluggit,
        serial_number: int,
        description: PluggitButtonEntityDescription,
    ) -> None:
        """Initialise Pluggit button."""
        self._pluggit = pluggit
        self.entity_description = description
        self._serial_number = str(serial_number)
        self._attr_unique_id = description.key

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(name="Pluggit", identifiers={(DOMAIN, self._serial_number)})

    def press(self) -> None:
        """Handle the button press."""
        self.entity_description.set_fn(self._pluggit)
