from . import area_idle, area_iv_mitm, area_mon_mitm, area_pokestops, area_raids_mitm
from .area import Area
from .auth import Auth
from .device import Device
from .devicepool import DevicePool
from .geofence import GeoFence
from .monivlist import MonIVList
from .routecalc import RouteCalc
from .walker import Walker
from .walkerarea import WalkerArea
from .. import dm_exceptions


def AreaFactory(data_manager, identifier=None, mode=None):
    if identifier is None and mode is None:
        raise dm_exceptions.InvalidArea(mode)
    elif identifier is not None:
        sql = "SELECT `mode` FROM `settings_area` WHERE `area_id` = %s and `instance_id` = %s"
        mode = data_manager.dbc.autofetch_value(sql, args=(identifier, data_manager.instance_id))
    try:
        return AREA_MAPPINGS[mode](data_manager, identifier=identifier)
    except KeyError:
        if identifier is not None:
            raise dm_exceptions.UnknownIdentifier()
        raise dm_exceptions.ModeUnknown(mode)
    except ValueError:
        raise dm_exceptions.ModeNotSpecified(mode)


MAPPINGS = {
    'area': AreaFactory,
    'area_nomode': Area,
    'auth': Auth,
    'device': Device,
    'devicepool': DevicePool,
    'geofence': GeoFence,
    'monivlist': MonIVList,
    'routecalc': RouteCalc,
    'walker': Walker,
    'walkerarea': WalkerArea
}

AREA_MAPPINGS = {
    'idle': area_idle.AreaIdle,
    'iv_mitm': area_iv_mitm.AreaIVMITM,
    'mon_mitm': area_mon_mitm.AreaMonMITM,
    'pokestops': area_pokestops.AreaPokestops,
    'raids_mitm': area_raids_mitm.AreaRaidsMITM
}
