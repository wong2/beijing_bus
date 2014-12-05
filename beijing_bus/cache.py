#-*-coding:utf-8-*-

"""
为了支持多种离线方案，使用了 dogpile.cache，支持 本地文件(默认), memcached, redis 等
参见文档：http://dogpilecache.readthedocs.org/en/latest/api.html#module-dogpile.cache.backends.memory
"""

from dogpile.cache import make_region


cache_config_null = {
    'backend': 'dogpile.cache.null'
}

cache_config_file = {
    'backend': 'dogpile.cache.dbm',
    'arguments': {
        'filename': 'offline_data/bus_offline_data.dbm'
    }
}


cache = make_region().configure(**cache_config_file)
