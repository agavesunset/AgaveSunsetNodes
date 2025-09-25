from .type_agavesunset import TypeAgaveSunset
from .math_agavesunset import MathAgaveSunset
from .compare_agavesunset import CompareAgaveSunset
from .maprange_agavesunset import MapRangeAgaveSunset
from .switch_agavesunset import SwitchAgaveSunset
from .demux_agavesunset import DemuxAgaveSunset

NODE_CLASS_MAPPINGS = {
    "TypeAgaveSunset": TypeAgaveSunset,
    "MathAgaveSunset": MathAgaveSunset,
    "CompareAgaveSunset": CompareAgaveSunset,
    "MapRangeAgaveSunset": MapRangeAgaveSunset,
    "SwitchAgaveSunset": SwitchAgaveSunset,
    "DemuxAgaveSunset": DemuxAgaveSunset,   
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TypeAgaveSunset": "type_AgaveSunset",
    "MathAgaveSunset": "math_AgaveSunset",
    "CompareAgaveSunset": "compare_AgaveSunset",
    "MapRangeAgaveSunset": "maprange_AgaveSunset",
    "SwitchAgaveSunset": "switch_AgaveSunset",
    "DemuxAgaveSunset": "demux_AgaveSunset",
}
