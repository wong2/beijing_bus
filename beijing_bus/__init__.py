#-*-coding:utf-8-*-

import re

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

    @classmethod
    def extract_line_and_stations(cls, sentence):
        """
        解析 '坐847从西坝河到将台路口西' 为结构化数据: 
        {
            'line': <Line: 847(马甸桥西-雷庄村)>,
            'from_station': <Station 西坝河>,
            'to_station': <Station 将台路口西>
        }
        """
        possible_lines = cls.extract_lines(sentence)
        if not possible_lines:
            return None

        for line in possible_lines:
            matches = []
            for s in line.stations:
                index = sentence.find(s.name)
                if index > -1:
                    matches.append((index, s))
            if len(matches) >= 2 and matches[0][0] < matches[1][0]:
                break
        else:
            return None

        return {
            'line': line,
            'from_station': matches[0][1],
            'to_station': matches[1][1]
        }

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
