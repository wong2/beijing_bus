#-*-coding:utf-8-*-

from .cache import cache
from .line import BusLine


class BeijingBus(object):

    @classmethod
    def build_cache(cls):
        cache.invalidate(hard=True)
        cls.get_all_lines()

    @classmethod
    def get_all_lines(cls):
        return BusLine.get_all_lines()

    @classmethod
    def search_lines(cls, keyword):
        return list(BusLine.search(str(keyword)))
