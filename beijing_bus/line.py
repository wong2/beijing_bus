#-*-coding:utf-8-*-

from datetime import datetime
from pytz import timezone

from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool

from . import api
from .cache import cache
from .cipher import Cipher
from .station import BusStation


class BusLine(object):
    
    def __init__(self, **kwargs):
        self.stations = []
        for name, value in kwargs.iteritems():
            setattr(self, name, value)

    def __repr__(self):
        return '<Line: %s>' % self.name

    @classmethod
    @cache.cache_on_arguments()
    def get(cls, id):
        resp_doc = api.get_bus_offline_data(id)
        busline = resp_doc['root']['busline']

        key = 'aibang%s' % id
        cipher = Cipher(key)
        d = cipher.decrypt  # for convenience

        line = cls(**{
            'id': int(busline['lineid']),
            'name': d(busline['linename']),
            'short_name': d(busline['shotname']),
            'distance': float(busline['distince']),
            'ticket_type': busline['ticket'],
            'price': float(busline['totalPrice']),
            'running_time': busline['time'],
            'line_type': busline['type'],
            'coords': d(busline['coord']),
            'status': busline['status'],
            'version': busline['version']
        })

        for station_data in busline['stations']['station']:
            name, no, lon, lat = map(d, station_data.values())
            station = BusStation(name, float(lat), float(lon))
            line.stations.append(station)

        return line

    @classmethod
    def gets(cls, ids):
        return [cls.get(id) for id in ids]

    @classmethod
    @cache.cache_on_arguments()
    def get_all_line_ids(cls):
        resp_doc = api.get_line_update_state()
        root = resp_doc['root']
        line_ids = [line['id'] for line in root['lines']['line']]
        return line_ids
    
    @classmethod
    def get_all_lines(cls):
        line_ids = cls.get_all_line_ids()
        pool = Pool(10)
        return pool.map(cls.get, line_ids)

    @classmethod
    def search(cls, name):
        for line in cls.get_all_lines():
            if name in line.name:
                yield line

    def get_realtime_data(self, station_num):
        if isinstance(station_num, BusStation):
            station_num = station_num.get_num_in_a_line(self)

        resp_doc = api.get_realtime_data(self.id, station_num)
        root = resp_doc['root']
        if not root.get('data'):
            return []

        datas = root['data']['bus']
        if not isinstance(datas, list):
            datas = [datas]

        return [self._format_realtime_data(data) for data in datas]

    def _format_realtime_data(self, data):

        def t(ts):
            if float(ts) > -1:
                return datetime.fromtimestamp(float(ts), tz=timezone('Asia/Shanghai'))

        key = 'aibang%s' % data['gt']
        d = Cipher(key).decrypt

        return {
            'id': int(data['id']),
            'lat': float(d(data['x'])),
            'lon': float(d(data['y'])),
            'next_station_name': d(data['ns']),
            'next_station_num': int(d(data['nsn'])),
            'next_station_distance': float(data['nsd']),
            'next_station_arriving_time': t(data['nst']),
            'station_distance': float(d(data['sd'])),
            'station_arriving_time': t(d(data['st'])),
        }
