from .type_agavesunset import TypeAgaveSunset
from .math_agavesunset import MathAgaveSunset
from .compare_agavesunset import CompareAgaveSunset
from .maprange_agavesunset import MapRangeAgaveSunset
from .switch_agavesunset import SwitchAgaveSunset
from .demux8_agavesunset import Demux8AgaveSunset

NODE_CLASS_MAPPINGS = {
    "TypeAgaveSunset": TypeAgaveSunset,
    "MathAgaveSunset": MathAgaveSunset,
    "CompareAgaveSunset": CompareAgaveSunset,
    "MapRangeAgaveSunset": MapRangeAgaveSunset,
    "SwitchAgaveSunset": SwitchAgaveSunset,
    "Demux8AgaveSunset": Demux8AgaveSunset,   
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TypeAgaveSunset": "type_AgaveSunset",
    "MathAgaveSunset": "math_AgaveSunset",
    "CompareAgaveSunset": "compare_AgaveSunset",
    "MapRangeAgaveSunset": "maprange_AgaveSunset",
    "SwitchAgaveSunset": "switch_AgaveSunset",
    "Demux8AgaveSunset": "demux8_AgaveSunset",
}


