"""Switch."""

from collections.abc import Callable
from dataclasses import dataclass
import logging
import time
from typing import Any

from homeassistant.components.switch import (
    SwitchDeviceClass,
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import StateType
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SERIAL_NUMBER
from .pypluggit.const import ActiveUnitMode
from .pypluggit.pluggit import Pluggit

_LOGGER = logging.getLogger(__name__)


@dataclass(kw_only=True)
class PluggitSwitchEntityDescription(SwitchEntityDescription):
    """Describes Pluggit switch entity."""

    on_fn: Callable[[Pluggit], None]
    off_fn: Callable[[Pluggit], None]
    get_fn: Callable[[Pluggit], StateType]


SWITCHES: tuple[PluggitSwitchEntityDescription, ...] = (
    PluggitSwitchEntityDescription(
        key="night_mode",
        translation_key="night_mode",
        entity_category=EntityCategory.CONFIG,
        device_class=SwitchDeviceClass.SWITCH,
        icon="mdi:weather-night",
        on_fn=lambda device: device.set_unit_mode(ActiveUnitMode.NIGHT_MODE),
        off_fn=lambda device: device.set_unit_mode(ActiveUnitMode.END_NIGHT_MODE),
        get_fn=lambda device: device.get_night_mode_state(),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up switch from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    pluggit: Pluggit = data[DOMAIN]
    serial_number = data[SERIAL_NUMBER]

    async_add_entities(
        (
            PluggitSwitch(
                pluggit=pluggit, serial_number=serial_number, description=description
            )
            for description in SWITCHES
        ),
        update_before_add=True,
    )


class PluggitSwitch(SwitchEntity):
    """Pluggit switch."""

    def __init__(
        self,
        pluggit: Pluggit,
        serial_number: int,
        description: PluggitSwitchEntityDescription,
    ) -> None:
        """Initialise switch."""

        self._pluggit = pluggit
        self.entity_description = description
        self._serial_number = str(serial_number)
        self._attr_unique_id = description.key
        self._attr_has_entity_name = True
        self._attr_available = False
        self._attr_is_on = False
        self._attr_native_value = 0
        self._attr_device_info = DeviceInfo(
            name="Pluggit", identifiers={(DOMAIN, self._serial_number)}
        )

    def turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        self.entity_description.on_fn(self._pluggit)

    def turn_off(self, **kwargs: Any) -> None:
        """Turn off the switch."""
        self.entity_description.off_fn(self._pluggit)

    def update(self) -> None:
        """Fetch data for switch."""
        # If a preset mode is set, there is an update. But this update is to fast,
        # the mode on the device isn't ready. So we wait here 100ms.
        time.sleep(100 / 1000)

        self._attr_native_value = self.entity_description.get_fn(self._pluggit)

        if self._attr_native_value is None:
            self._attr_available = False
            self._attr_is_on = None
        else:
            self._attr_available = True
            if self._attr_native_value == 0:
                self._attr_is_on = False
            elif self._attr_native_value == 1:
                self._attr_is_on = True
            else:
                self._attr_is_on = None
