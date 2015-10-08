# -*-coding:utf-8-*-

from dogpile.cache import make_region

cache_config = {
    'backend': 'dogpile.cache.dbm',
    'arguments': {
        'filename': 'offline_data/bus_offline_data.dbm'
    }
}

cache = make_region().configure(**cache_config)
