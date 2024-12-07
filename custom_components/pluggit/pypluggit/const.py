from enum import Enum, auto


class Registers(Enum):
    PRM_SYSTEM_ID = auto()
    PRM_SYSTEM_SERIAL_NUM_LOW = auto()
    PRM_SYSTEM_SERIAL_NUM_HIGH = auto()
    PRM_FW_VERSION = auto()
    PRM_DATE_TIME = auto()
    PRM_DATE_TIME_SET = auto()
    PRM_WORK_TIME = auto()
    PRM_CURRENT_BL_STATE = auto()
    PRM_RAM_IDX_UNIT_MODE = auto()
    PRM_ROM_IDX_SPEED_LEVEL = auto()
    PRM_RAM_IDX_T1 = auto()
    PRM_RAM_IDX_T2 = auto()
    PRM_RAM_IDX_T3 = auto()
    PRM_RAM_IDX_T4 = auto()
    PRM_FILTER_REMAINING_TIME = auto()
    PRM_FILTER_DEFAULT_TIME = auto()
    PRM_FILTER_RESET = auto()
    PRM_FILTER_DIRTINESS_DEGREE = auto()
    PRM_BYPASS_TMIN = auto()
    PRM_BYPASS_TMAX = auto()
    PRM_RAM_IDX_BYPASS_ACTUAL_STATE = auto()
    PRM_RAM_IDX_BYPASS_MANUAL_TIMEOUT = auto()
    PRM_BYPASS_TMIN_SUMMER = auto()
    PRM_BYPASS_TMAX_SUMMER = auto()


class RegisterType(Enum):
    UINT_32 = auto()
    FLOAT = auto()


class Components(Enum):
    FP1 = 0x0001
    WEEK = 0x0002
    BYPASS = 0x0004
    LRSWITCH = 0x0008
    INTERNAL_PREHEATER = 0x0010
    SERVO_FLOW = 0x0020
    RH_SENSOR = 0x0040
    VOC_SENSOR = 0x0080
    EXT_OVERRIDE = 0x0100
    HAC1 = 0x0200
    HRC2 = 0x0400
    PC_TOOL = 0x0800
    APPS = 0x1000
    ZEEGBEE = 0x2000
    DI1_OVERRIDE = 0x4000
    DI2_OVERRIDE = 0x8000


class ActiveUnitMode(Enum):
    DEMAND_MODE = 0x0002
    MANUAL_MODE = 0x0004
    WEEK_PROGRAM_MODE = 0x0008
    AWAY_MODE = 0x0010
    FIREPLACE_MODE = 0x0040
    SUMMER_MODE = 0x0800
    END_AWAY_MODE = 0x8010
    END_FIREPLACE_MODE = 0x8040
    END_SUMMER_MODE = 0x8800


class SpeedLevelFan(Enum):
    LEVEL_0 = 0x0000
    LEVEL_1 = 0x0001
    LEVEL_2 = 0x0002
    LEVEL_3 = 0x0003
    LEVEL_4 = 0x0004


DEVICE_TYPE = {1: "AP190", 2: "AP310", 3: "AP460", 4: "AD160"}

CURRENT_UNIT_MODE = {
    0: "Standby",
    1: "Manual",
    2: "Demand",
    3: "Week Program",
    4: "Servo-flow",
    5: "Away",
    6: "Summer",
    7: "DI Override",
    8: "Hygrostat Override",
    9: "Fireplace",
    10: "Installer",
    11: "Fail Safe 1",
    12: "Fail Safe 2",
    13: "Fail Off",
    14: "Defrost Off",
    15: "Defrost",
    16: "Night",
}

DEGREE_OF_DIRTINESS = {
    0: "0 - 33%",
    1: "34 - 67%",
    2: "68 - 99%",
    3: "100%",
}

BYPASS_STATE = {
    0: "Closed",
    1: "In Process",
    32: "Closing",
    64: "Opening",
    255: "Opened",
}

REGISTER_DIC = {
    Registers.PRM_SYSTEM_ID: [2, RegisterType.UINT_32],
    Registers.PRM_SYSTEM_SERIAL_NUM_LOW: [4, RegisterType.UINT_32],
    Registers.PRM_SYSTEM_SERIAL_NUM_HIGH: [6, RegisterType.UINT_32],
    Registers.PRM_FW_VERSION: [24, RegisterType.UINT_32],
    Registers.PRM_DATE_TIME: [108, RegisterType.UINT_32],
    Registers.PRM_DATE_TIME_SET: [110, RegisterType.UINT_32],
    Registers.PRM_WORK_TIME: [624, RegisterType.UINT_32],
    Registers.PRM_CURRENT_BL_STATE: [472, RegisterType.UINT_32],
    Registers.PRM_RAM_IDX_UNIT_MODE: [168, RegisterType.UINT_32],
    Registers.PRM_ROM_IDX_SPEED_LEVEL: [324, RegisterType.UINT_32],
    Registers.PRM_RAM_IDX_T1: [132, RegisterType.FLOAT],
    Registers.PRM_RAM_IDX_T2: [134, RegisterType.FLOAT],
    Registers.PRM_RAM_IDX_T3: [136, RegisterType.FLOAT],
    Registers.PRM_RAM_IDX_T4: [138, RegisterType.FLOAT],
    Registers.PRM_FILTER_REMAINING_TIME: [554, RegisterType.UINT_32],
    Registers.PRM_FILTER_DEFAULT_TIME: [556, RegisterType.UINT_32],
    Registers.PRM_FILTER_RESET: [558, RegisterType.UINT_32],
    Registers.PRM_FILTER_DIRTINESS_DEGREE: [612, RegisterType.UINT_32],
    Registers.PRM_BYPASS_TMIN: [444, RegisterType.FLOAT],
    Registers.PRM_BYPASS_TMAX: [446, RegisterType.FLOAT],
    Registers.PRM_RAM_IDX_BYPASS_ACTUAL_STATE: [198, RegisterType.UINT_32],
    Registers.PRM_RAM_IDX_BYPASS_MANUAL_TIMEOUT: [264, RegisterType.UINT_32],
    Registers.PRM_BYPASS_TMIN_SUMMER: [766, RegisterType.FLOAT],
    Registers.PRM_BYPASS_TMAX_SUMMER: [764, RegisterType.FLOAT],
}
