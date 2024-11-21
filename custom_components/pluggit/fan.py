"""Fan"""

from typing import Any

from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.percentage import (
    ordered_list_item_to_percentage,
    percentage_to_ordered_list_item,
)

from .const import DOMAIN
from .pypluggit.const import ActiveUnitMode, SpeedLevelFan
from .pypluggit.pluggit import Pluggit


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    pluggit: Pluggit = hass.data[DOMAIN][entry.entry_id]
    device = DeviceInfo(
        identifiers={(DOMAIN, pluggit.get_serial_number())},
        name="Pluggit",
        manufacturer="Pluggit",
        model=pluggit.get_unit_type(),
        sw_version=pluggit.get_firmware_version(),
    )

    async_add_entities(PluggitFan(pluggit=pluggit, device=device))


class PluggitFan(FanEntity):
    ORDERED_NAMED_FAN_SPEEDS = ["Level 1", "Level 2", "Level 3", "Level 4"]
    _attr_supported_features = (
        FanEntityFeature.PRESET_MODE
        | FanEntityFeature.SET_SPEED
        | FanEntityFeature.TURN_OFF
        | FanEntityFeature.TURN_ON
    )

    def __init__(self, pluggit: Pluggit, device: DeviceInfo) -> None:
        """Initialise sensor."""
        self._pluggit = pluggit
        self._device = device
        self._speedLevel = 0
        self._currentMode = "Standby"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return self.device

    @property
    def is_on(self) -> bool | None:
        """Return true if fan is on."""
        return self._speedLevel > 0

    @property
    def percentage(self) -> int | None:
        # TODO mit enum arbeiten von pluggit
        item: str
        if self._speedLevel == 1:
            item = "Level 1"
        elif self._speedLevel == 2:
            item = "Level 2"
        elif self._speedLevel == 3:
            item = "Level 3"
        elif self._speedLevel == 4:
            item = "Level 4"
        else:
            return 0

        return ordered_list_item_to_percentage(self.ORDERED_NAMED_FAN_SPEEDS, item)

    @property
    def speed_count(self) -> int:
        """Return the number of speeds the fan supports."""
        return len(self.ORDERED_NAMED_FAN_SPEEDS)

    @property
    def preset_mode(self) -> str | None:
        # TODO strings raus
        if self._currentMode == "Week Program":
            return self._currentMode
        else:
            return None

    @property
    def preset_modes(self) -> list[str] | None:
        # TODO strings raus
        return ["Week Program"]

    def set_preset_mode(self, preset_mode: str) -> None:
        # TODO gucken was hier ausgesucht wird
        self._pluggit.set_unit_mode(ActiveUnitMode.WEEK_PROGRAM_MODE)

    def set_percentage(self, percentage: int) -> None:
        # TODO mit ennum arbeiten von pluggit
        # TODO anlage auf manuel  stellen
        named_speed = percentage_to_ordered_list_item(
            self.ORDERED_NAMED_FAN_SPEEDS, percentage
        )
        speed: SpeedLevelFan

        if named_speed == "Level 1":
            speed = SpeedLevelFan.LEVEL_1
        elif named_speed == "Level 2":
            speed = SpeedLevelFan.LEVEL_2
        elif named_speed == "Level 3":
            speed = SpeedLevelFan.LEVEL_3
        elif named_speed == "Level 4":
            speed = SpeedLevelFan.LEVEL_4

        self._pluggit.set_speed_level(speed=speed)

    def turn_on(
        self,
        speed: str = None,
        percentage: int = None,
        preset_mode: str = None,
        **kwargs: Any,
    ) -> None:
        """Turn on the fan."""
        # TODO gucken auf was percentage gestellt ist und ob preset mode gesetzt ist, danach die anlage anschalten
        # TODO gucken was für ein modus gesetzt ist und gegenbenenfalls in manuelstellen
        self._pluggit.set_speed_level(SpeedLevelFan.LEVEL_1)

    def turn_off(self, **kwargs: Any) -> None:
        # TODO Anlage auf manuael stellen
        self._pluggit.set_speed_level(SpeedLevelFan.LEVEL_0)

    def update(self) -> None:
        """Fetch data for fan."""
        # TODO checken ob hier None kommt und dann gucken was man dann tut
        self._speedLevel = self._pluggit.get_speed_level()
        self._currentMode = self._pluggit.get_current_unit_mode()
