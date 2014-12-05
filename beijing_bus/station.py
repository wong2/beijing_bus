#-*-coding:utf-8-*-


class BusStation(object):
    
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return '<Station %s>' % self.name

    def get_num_in_a_line(self, line):
        try:
            return line.stations.index(self) + 1
        except ValueError:
            return 0
