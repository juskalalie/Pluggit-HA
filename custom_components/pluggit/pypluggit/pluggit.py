"""Pluggit."""

from pymodbus import ModbusException
from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.exceptions import ConnectionException, ModbusIOException
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder

from .const import (
    BYPASS_STATE,
    CURRENT_UNIT_MODE,
    DEGREE_OF_DIRTINESS,
    DEVICE_TYPE,
    REGISTER_DIC,
    ActiveUnitMode,
    Registers,
    RegisterType,
    SpeedLevelFan,
    WeekProgram,
)


class Pluggit:
    """Pluggit."""

    client: ModbusTcpClient
    host: str

    def __init__(self, host: str) -> None:
        """Init host address."""
        self.host = host
        self.client = ModbusTcpClient(host=self.host)

    def __read_register(self, register: Registers):
        item = REGISTER_DIC[register]

        try:
            result = self.client.read_holding_registers(address=item[0], count=2)
            decoder = BinaryPayloadDecoder.fromRegisters(
                result.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE
            )
        except ModbusIOException:
            return None
        except ModbusException:
            return None

        if item[1] == RegisterType.UINT_32:
            return decoder.decode_32bit_uint()
        if item[1] == RegisterType.FLOAT:
            return decoder.decode_32bit_float()
        return None

    def __write_register(self, register: Registers, data: int):
        item = REGISTER_DIC[register]
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)

        if item[1] == RegisterType.UINT_32:
            builder.add_32bit_uint(data)
        elif item[1] == RegisterType.FLOAT:
            builder.add_32bit_float(data)

        try:
            self.client.write_registers(address=item[0], values=builder.to_registers())
        except ConnectionException:
            return

    def get_unit_type(self) -> str | None:
        """Get Pluggit model."""
        ret = self.__read_register(register=Registers.PRM_SYSTEM_ID)
        if ret is not None:
            return DEVICE_TYPE[(ret >> 24) & 0x0F]
        return None

    def get_serial_number(self) -> int | None:
        """Get serial number."""
        low = self.__read_register(register=Registers.PRM_SYSTEM_SERIAL_NUM_LOW)
        high = self.__read_register(register=Registers.PRM_SYSTEM_SERIAL_NUM_HIGH)

        if low and high is not None:
            return (high << 32) + low
        return None

    def get_firmware_version(self) -> str | None:
        """Get firmware version."""
        version = self.__read_register(register=Registers.PRM_FW_VERSION)

        if version is not None:
            return str(version >> 8) + "." + str(version & 0xFF)
        return None

    def get_work_time(self) -> int | None:
        """Get work time in hours."""
        return self.__read_register(register=Registers.PRM_WORK_TIME)

    def get_current_unit_mode(self) -> str | None:
        """Get current mode."""
        mode = self.__read_register(register=Registers.PRM_CURRENT_BL_STATE)

        if mode is not None:
            return CURRENT_UNIT_MODE[mode]
        return None

    def get_speed_level(self) -> int | None:
        """Get speed level."""
        return self.__read_register(register=Registers.PRM_ROM_IDX_SPEED_LEVEL)

    def get_temperature_t1(self) -> float | None:
        """Get current temperature 1 in °C."""
        return self.__read_register(register=Registers.PRM_RAM_IDX_T1)

    def get_temperature_t2(self) -> float | None:
        """Get current temperature 2 in °C."""
        return self.__read_register(register=Registers.PRM_RAM_IDX_T2)

    def get_temperature_t3(self) -> float | None:
        """Get current temperature 3 in °C."""
        return self.__read_register(register=Registers.PRM_RAM_IDX_T3)

    def get_temperature_t4(self) -> float | None:
        """Get current temperature 4 in °C."""
        return self.__read_register(register=Registers.PRM_RAM_IDX_T4)

    def get_filter_time(self) -> int | None:
        """Get filter time in days."""
        return self.__read_register(register=Registers.PRM_FILTER_DEFAULT_TIME)

    def get_remaining_filter_time(self) -> int | None:
        """Get remaining filter time in days."""
        return self.__read_register(register=Registers.PRM_FILTER_REMAINING_TIME)

    def get_filter_dirtiness(self) -> str | None:
        """Get filter dirtiness."""
        dirt = self.__read_register(register=Registers.PRM_FILTER_DIRTINESS_DEGREE)

        if dirt is not None:
            return DEGREE_OF_DIRTINESS[dirt]
        return None

    def get_bypass_tmin(self) -> float | None:
        """Get bypass tmin in °C."""
        return self.__read_register(register=Registers.PRM_BYPASS_TMIN)

    def get_bypass_tmax(self) -> float | None:
        """Get bypass tmax in °C."""
        return self.__read_register(register=Registers.PRM_BYPASS_TMAX)

    def get_bypass_tmin_summer(self) -> float | None:
        """Get bypass tmin for summer in °C."""
        return self.__read_register(register=Registers.PRM_BYPASS_TMIN_SUMMER)

    def get_bypass_tmax_summer(self) -> float | None:
        """Get bypass tmax for summer in °C."""
        return self.__read_register(register=Registers.PRM_BYPASS_TMAX_SUMMER)

    def get_bypass_actual_state(self) -> str | None:
        """Get actual state for bypass."""
        state = self.__read_register(register=Registers.PRM_RAM_IDX_BYPASS_ACTUAL_STATE)

        if state is not None:
            return BYPASS_STATE[state]
        return None

    def get_bypass_manual_timeout(self) -> int | None:
        """Get manual timeout for bypass in minutes."""
        return self.__read_register(
            register=Registers.PRM_RAM_IDX_BYPASS_MANUAL_TIMEOUT
        )

    def get_date_time(self) -> int | None:
        """Get date and time in seconds."""
        return self.__read_register(register=Registers.PRM_DATE_TIME)

    def get_week_program(self) -> WeekProgram | None:
        """Get the selected number of week program."""
        ret = self.__read_register(register=Registers.PRM_NUM_OF_WEEK_PROGRAM)

        if ret is not None:
            return WeekProgram(value=ret)

        return None

    def set_date_time(self, time_seconds: int):
        """Set date and time."""
        self.__write_register(
            register=Registers.PRM_DATE_TIME_SET,
            data=time_seconds,
        )

    def set_unit_mode(self, mode: ActiveUnitMode):
        """Set mode."""
        self.__write_register(register=Registers.PRM_RAM_IDX_UNIT_MODE, data=mode.value)

    def set_speed_level(self, speed: SpeedLevelFan):
        """Set speed fan."""
        self.__write_register(
            register=Registers.PRM_ROM_IDX_SPEED_LEVEL, data=speed.value
        )

    def set_default_filter_time(self, t: int):
        """Set default filter time."""
        self.__write_register(register=Registers.PRM_FILTER_DEFAULT_TIME, data=t)

    def reset_filter(self):
        """Reset filter."""
        self.__write_register(register=Registers.PRM_FILTER_RESET, data=1)

    def set_bypass_tmin(self, temp: float):
        """Set bypass tmin."""
        self.__write_register(register=Registers.PRM_BYPASS_TMIN, data=temp)

    def set_bypass_tmax(self, temp: float):
        """Set bypass tmax."""
        self.__write_register(register=Registers.PRM_BYPASS_TMAX, data=temp)

    def set_bypass_tmin_summer(self, temp: float):
        """Set bypass tmin summer."""
        self.__write_register(register=Registers.PRM_BYPASS_TMIN_SUMMER, data=temp)

    def set_bypass_tmax_summer(self, temp: float):
        """Set bypass tmax summer."""
        self.__write_register(register=Registers.PRM_BYPASS_TMAX_SUMMER, data=temp)

    def set_bypass_manual_timeout(self, timeout: int):
        """Set bypass manual timeout."""
        self.__write_register(
            register=Registers.PRM_RAM_IDX_BYPASS_MANUAL_TIMEOUT, data=timeout
        )

    def set_week_program(self, number: WeekProgram):
        """Set number of week program."""
        self.__write_register(
            register=Registers.PRM_NUM_OF_WEEK_PROGRAM, data=number.value
        )
