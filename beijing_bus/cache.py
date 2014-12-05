#-*-coding:utf-8-*-

"""
为了支持多种离线方案，使用了 dogpile.cache，支持 本地文件(默认), memcached, redis 等
参见文档：http://dogpilecache.readthedocs.org/en/latest/api.html#module-dogpile.cache.backends.memory
"""

from dogpile.cache import make_region


cache_config = {
    'backend': 'dogpile.cache.dbm',
    'arguments': {
        'filename': 'offline_data/bus_offline_data.dbm'
    }
}

try:
    from .local_cache_config import cache_config
except:
    pass

cache = make_region().configure(**cache_config)
