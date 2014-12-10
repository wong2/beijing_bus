## 北京实时公交

该项目是北京实时公交查询接口的Python绑定，接口逆向自其[安卓客户端](http://www.bjjtw.gov.cn/topic/bjssgj/)

### 警告

此项目通过调用非公开接口获取数据，use at your own risk.

### Quick Start

* `pip install -r requirements.txt` 安装依赖
* `python manage.py build_cache` 获取离线数据，建立本地缓存

项目自带了一个终端中的查询工具作为例子，运行： `python manage.py query`

### Examples

    >>> from beijing_bus import BeijingBus
    >>> lines = BeijingBus.get_all_lines()
    >>> lines
    [<Line: 运通122(农业展览馆-华纺易城公交场站)>, <Line: 运通101(广顺南大街北口-蓝龙家园)>, ...]
    >>> lines = BeijingBus.search_lines('847')
    >>> lines
    [<Line: 847(马甸桥西-雷庄村)>, <Line: 847(雷庄村-马甸桥西)>]
    >>> line = lines[0]
    >>> print line.id, line.name
    541 847(马甸桥西-雷庄村)
    >>> line.stations
    [<Station 马甸桥西>, <Station 马甸桥东>, <Station 安华桥西>, ...]
    >>> station = line.stations[0]
    >>> print station.name, station.lat, station.lon
    马甸桥西 39.967721 116.372921
    >>> line.get_realtime_data(1) # 参数为站点的序号，从1开始
    [
        {
            'id': 公交车id,
            'lat': 公交车的位置,
            'lon': 公交车位置,
            'next_station_name': 下一站的名字,
            'next_station_num': 下一站的序号,
            'next_station_distance': 离下一站的距离,
            'next_station_arriving_time': 预计到达下一站的时间,
            'station_distance': 离本站的距离,
            'station_arriving_time': 预计到达本站的时间,
        },
        ...
    ]


### Roadmap

- [x] 实现 beijing_bus 模块，提供需要的Python接口
- [x] 终端中的查询工具
- [x] 微信公众号，扫描二维码关注：

![公众号二维码](http://doora.qiniudn.com/bmg5w.jpg)
