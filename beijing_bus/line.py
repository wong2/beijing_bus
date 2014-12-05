#-*-coding:utf-8-*-

from datetime import datetime

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
            'distince': float(busline['distince']),
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
        return cls.gets(line_ids)

    @classmethod
    def search(cls, name):
        for line in cls.get_all_lines():
            if name in line.name:
                yield line

    def get_realtime_data(self, station_num):

        def t(ts):
            if float(ts) > -1:
                return datetime.fromtimestamp(float(ts))

        data = []
        resp_doc = api.get_realtime_data(self.id, station_num)
        for bus_data in resp_doc['root']['data']['bus']:
            key = 'aibang%s' % bus_data['gt']
            d = Cipher(key).decrypt
            data.append({
                'id': int(bus_data['id']),
                'lat': float(d(bus_data['x'])),
                'lon': float(d(bus_data['y'])),
                'next_station_name': d(bus_data['ns']),
                'next_station_num': int(d(bus_data['nsn'])),
                'next_station_distance': float(bus_data['nsd']),
                'next_station_arriving_time': t(bus_data['nst']),
                'station_distance': float(d(bus_data['sd'])),
                'station_arriving_time': t(d(bus_data['st'])),
            })
        return data
