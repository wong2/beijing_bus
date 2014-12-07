#-*-coding:utf-8-*-

import re

from .cache import cache
from .line import BusLine


class BeijingBus(object):

    @classmethod
    def build_cache(cls):
        cache.invalidate(hard=True)
        cls.get_all_lines()
        cls.get_all_stations()

    @classmethod
    def get_all_lines(cls):
        return BusLine.get_all_lines()

    @classmethod
    def search_lines(cls, keyword):
        return list(BusLine.search(str(keyword)))

    @classmethod
    @cache.cache_on_arguments()
    def get_all_stations(cls):
        stations = [s for line in cls.get_all_lines() for s in line.stations]
        return sorted(set(stations), key=lambda s: len(s.name), reverse=True)

    @classmethod
    def extract_lines(cls, sentence):
        numbers = re.findall(r'\d+', sentence)
        if not numbers:
            return []

        num = numbers[0]
        if '运通' + num in sentence:
            line_name = '运通' + num
        else:
            line_name = num

        lines = BeijingBus.search_lines(line_name)
        lines = [line for line in lines if line.short_name == line_name]
        if not lines:
            lines = BeijingBus.search_lines('运通' + line_name)
        return lines
    
    @classmethod
    def extract_stations(cls, sentence):
        original_sentence = sentence
        matches = set()
        for s in cls.get_all_stations():
            if s.name in sentence:
                matches.add(s)
                sentence = sentence.replace(s.name, '')
        # 按在sentence中出现的顺序排序
        return sorted(matches, key=lambda s: original_sentence.find(s.name))
