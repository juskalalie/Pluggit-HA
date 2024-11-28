"""Number"""

import logging
from dataclasses import dataclass
from typing import Callable

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfTemperature, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SERIAL_NUMBER
from .pypluggit.pluggit import Pluggit

_LOGGER = logging.getLogger(__name__)


@dataclass(kw_only=True)
class PluggitNumberEntityDescription(NumberEntityDescription):
    """Describes Pluggit number entity."""

    set_fn: Callable[[Pluggit, float], None]


NUMBERS: tuple[PluggitNumberEntityDescription, ...] = (
    PluggitNumberEntityDescription(
        key="bypass_tmin",
        translation_key="bypass_tmin",
        device_class=NumberDeviceClass.TEMPERATURE,
        mode=NumberMode.AUTO,
        native_max_value=15,
        native_min_value=12,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        set_fn=lambda device, temp: device.set_bypass_tmin(temp),
    ),
    PluggitNumberEntityDescription(
        key="bypass_tmax",
        translation_key="bypass_tmax",
        device_class=NumberDeviceClass.TEMPERATURE,
        mode=NumberMode.AUTO,
        native_max_value=27,
        native_min_value=21,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        set_fn=lambda device, temp: device.set_bypass_tmax(temp),
    ),
    PluggitNumberEntityDescription(
        key="bypass_tmin_summer",
        translation_key="bypass_tmin_summer",
        device_class=NumberDeviceClass.TEMPERATURE,
        mode=NumberMode.AUTO,
        native_max_value=17,
        native_min_value=12,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        set_fn=lambda device, temp: device.set_bypass_tmin_summer(temp),
    ),
    PluggitNumberEntityDescription(
        key="bypass_tmax_summer",
        translation_key="bypass_tmax_summer",
        device_class=NumberDeviceClass.TEMPERATURE,
        mode=NumberMode.AUTO,
        native_max_value=30,
        native_min_value=21,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        set_fn=lambda device, temp: device.set_bypass_tmax_summer(temp),
    ),
    PluggitNumberEntityDescription(
        key="filter_time",
        translation_key="filter_time",
        device_class=NumberDeviceClass.DURATION,
        mode=NumberMode.AUTO,
        native_max_value=360,
        native_min_value=0,
        native_unit_of_measurement=UnitOfTime.DAYS,
        set_fn=lambda device, temp: device.set_default_filter_time(int(temp)),
    ),
    PluggitNumberEntityDescription(
        key="bypass_manual_timeout",
        translation_key="bypass_manual_timeout",
        device_class=NumberDeviceClass.DURATION,
        mode=NumberMode.AUTO,
        native_max_value=480,
        native_min_value=60,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        set_fn=lambda device, temp: device.set_bypass_manual_timeout(int(temp)),
    ),
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
            PluggitSensor(
                pluggit=pluggit, serial_number=serial_number, description=description
            )
            for description in NUMBERS
        ),
        update_before_add=True,
    )


class PluggitSensor(NumberEntity):
    entity_description: PluggitNumberEntityDescription
    _attr_entity_category = EntityCategory.CONFIG
    _attr_has_entity_name = True

    def __init__(
        self,
        pluggit: Pluggit,
        serial_number: int,
        description: PluggitNumberEntityDescription,
    ) -> None:
        """Initialise Pluggit sensor."""
        self._pluggit = pluggit
        self.entity_description = description
        self._serial_number = str(serial_number)
        self._attr_unique_id = description.key
        self._attr_native_value = description.native_min_value

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(name="Pluggit", identifiers={(DOMAIN, self._serial_number)})

    def set_native_value(self, value: float) -> None:
        """Update the current value."""
        self.entity_description.set_fn(self._pluggit, value)
