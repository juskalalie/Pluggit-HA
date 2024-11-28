"""Sensor"""

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfTemperature, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN, SERIAL_NUMBER
from .pypluggit.pluggit import Pluggit

_LOGGER = logging.getLogger(__name__)


@dataclass(kw_only=True)
class PluggitSensorEntityDescription(SensorEntityDescription):
    """Describes Pluggit sensor entity."""

    value_fn: Callable[[Pluggit], StateType]


SENSORS: tuple[PluggitSensorEntityDescription, ...] = (
    PluggitSensorEntityDescription(
        key="T1",
        translation_key="t1_outdoor",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda device: device.get_temperature_t1(),
    ),
    PluggitSensorEntityDescription(
        key="T2",
        translation_key="t2_supply",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda device: device.get_temperature_t2(),
    ),
    PluggitSensorEntityDescription(
        key="T3",
        translation_key="t3_extract",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda device: device.get_temperature_t3(),
    ),
    PluggitSensorEntityDescription(
        key="T4",
        translation_key="t4_exhaust",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda device: device.get_temperature_t4(),
    ),
    PluggitSensorEntityDescription(
        key="work_time",
        translation_key="work_time",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.HOURS,
        suggested_display_precision=0,
        suggested_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda device: device.get_work_time(),
    ),
    PluggitSensorEntityDescription(
        key="filter_remain",
        translation_key="filter_remain",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.DAYS,
        suggested_display_precision=0,
        suggested_unit_of_measurement=UnitOfTime.DAYS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:air-filter",
        value_fn=lambda device: device.get_remaining_filter_time(),
    ),
    PluggitSensorEntityDescription(
        key="filter_dirtiness",
        translation_key="filter_dirtiness",
        device_class=None,
        native_unit_of_measurement=None,
        state_class=None,
        value_fn=lambda device: device.get_filter_dirtiness(),
    ),
    PluggitSensorEntityDescription(
        key="bypass_state",
        translation_key="bypass_state",
        device_class=None,
        native_unit_of_measurement=None,
        state_class=None,
        value_fn=lambda device: device.get_bypass_actual_state(),
    ),
    PluggitSensorEntityDescription(
        key="get_bypass_tmin",
        translation_key="bypass_tmin",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda device: device.get_bypass_tmin(),
    ),
    PluggitSensorEntityDescription(
        key="get_bypass_tmax",
        translation_key="bypass_tmax",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda device: device.get_bypass_tmax(),
    ),
    PluggitSensorEntityDescription(
        key="get_bypass_tmin_summer",
        translation_key="bypass_tmin_summer",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda device: device.get_bypass_tmin_summer(),
    ),
    PluggitSensorEntityDescription(
        key="get_bypass_tmax_summer",
        translation_key="bypass_tmax_summer",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda device: device.get_bypass_tmax_summer(),
    ),
    PluggitSensorEntityDescription(
        key="get_bypass_manual_timeout",
        translation_key="bypass_manual_timeout",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        suggested_display_precision=0,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda device: device.get_bypass_manual_timeout(),
    ),
    PluggitSensorEntityDescription(
        key="get_time",
        translation_key="get_time",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.TIMESTAMP,
        state_class=None,
        value_fn=lambda device: datetime.fromtimestamp(
            device.get_date_time(), tz=timezone.utc
        ),
    ),
    PluggitSensorEntityDescription(
        key="get_filter_time",
        translation_key="filter_time",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.DAYS,
        suggested_display_precision=0,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda device: device.get_filter_time(),
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
            for description in SENSORS
        ),
        update_before_add=True,
    )


class PluggitSensor(SensorEntity):
    entity_description: PluggitSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        pluggit: Pluggit,
        serial_number: int,
        description: PluggitSensorEntityDescription,
    ) -> None:
        """Initialise Pluggit sensor."""
        self._pluggit = pluggit
        self.entity_description = description
        self._serial_number = str(serial_number)
        self._attr_unique_id = description.key
        self._is_available = False

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(name="Pluggit", identifiers={(DOMAIN, self._serial_number)})

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._is_available

    def update(self) -> None:
        """Fetch data for sensors."""

        self._attr_native_value = self.entity_description.value_fn(self._pluggit)

        if self._attr_native_value is None:
            self._is_available = False
        else:
            self._is_available = True
