"""Switch."""

import logging
import time
from typing import Any

from homeassistant.components.switch import (
    SwitchDeviceClass,
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SERIAL_NUMBER
from .pypluggit.const import CURRENT_UNIT_MODE, ActiveUnitMode
from .pypluggit.pluggit import Pluggit

_LOGGER = logging.getLogger(__name__)

SWITCHES: tuple[SwitchEntityDescription, ...] = (
    SwitchEntityDescription(
        key="switch1",
        translation_key="summer_mode",
        device_class=SwitchDeviceClass.SWITCH,
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

    entity_description: SwitchEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        pluggit: Pluggit,
        serial_number: int,
        description: SwitchEntityDescription,
    ) -> None:
        """Initialise switch."""
        self._pluggit = pluggit
        self.entity_description = description
        self._serial_number = str(serial_number)
        self._attr_unique_id = description.key
        self._is_available = False
        self._currentMode = CURRENT_UNIT_MODE[0]

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(name="Pluggit", identifiers={(DOMAIN, self._serial_number)})

    @property
    def is_on(self) -> bool | None:
        """Return true if fan is on."""
        return self._currentMode == 6

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._is_available

    def turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        self._pluggit.set_unit_mode(ActiveUnitMode.SUMMER_MODE)

    def turn_off(self, **kwargs: Any) -> None:
        """Turn off the switch."""
        self._pluggit.set_unit_mode(ActiveUnitMode.END_SUMMER_MODE)

    def update(self) -> None:
        """Fetch data for switch."""
        # If a preset mode is set, there is an update. But this update is to fast,
        # the mode on the device isn't ready. So we wait here 100ms.
        time.sleep(100 / 1000)
        self._currentMode = self._pluggit.get_current_unit_mode()

        if self._currentMode is None:
            self._is_available = False
        else:
            self._is_available = True
