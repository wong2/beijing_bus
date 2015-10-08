# -*-coding:utf-8-*-

from flask import Flask, render_template
from flask_weixin import Weixin

from beijing_bus import BeijingBus


# 查询示例
QUERY_EXAMPLE = '查询示例： 从西坝河到将台路口西'

# 用户关注公众号时给他推送一条消息
ON_FOLLOW_MESSAGE = {
    'title': '使用说明',
    'description': '',
    'picurl': 'http://doora.qiniudn.com/H9v9n.jpg',
    'url': 'http://t.cn/Rz0J1V6',
}


app = Flask(__name__)
app.config.from_object('config')

weixin = Weixin(app)
app.add_url_rule('/weixin', view_func=weixin.view_func)

if app.config.get('SENTRY_DSN'):
    from raven.contrib.flask import Sentry
    sentry = Sentry(app)


@weixin.register('*')
def query(**kwargs):
    username = kwargs.get('sender')
    sender = kwargs.get('receiver')
    message_type = kwargs.get('type')

    def r(content):
        return weixin.reply(
            username, sender=sender, content=content
        )

    if message_type == 'event' and kwargs.get('event') == 'subscribe':
        return weixin.reply(
            username, type='news', sender=sender, articles=[ON_FOLLOW_MESSAGE]
        )

    content = kwargs.get('content')
    if not content:
        reply = '我好笨笨哦，还不懂你在说什么。\n%s' % QUERY_EXAMPLE
        return r(reply)

    if isinstance(content, unicode):
        content = content.encode('utf-8')

    stations = BeijingBus.extract_stations(content)
    lines = BeijingBus.extract_lines(content)
    if len(stations) < 2:
        reply = '没有结果，可能还不支持这条线路呢~ \n%s' % QUERY_EXAMPLE
        return r(reply)

    from_station, to_station = stations[:2]
    lines = match_stations_with_lines(from_station, to_station, lines)
    if not lines:
        reply = '没有结果，可能还不支持这条线路呢~ \n%s' % QUERY_EXAMPLE
        return r(reply)

    reply = get_realtime_message(lines, from_station)
    return r(reply)


def match_stations_with_lines(from_station, to_station, lines=None):

    def match(a, b, l):
        '''检查l中包含a和b且a比b靠前'''
        try:
            return l.index(a) < l.index(b)
        except ValueError:
            return False

    if not lines:
        lines = BeijingBus.get_all_lines()

    return [
        line for line in lines if match(from_station, to_station, line.stations)
    ]


def get_realtime_message(lines, station):
    realtime_datas = []
    for line in lines:
        for data in line.get_realtime_data(station):
            if data.get('station_arriving_time'):
                realtime_datas.append((line, data))
    realtime_datas.sort(key=lambda d: d[1]['station_arriving_time'])

    if not realtime_datas:
        return '暂时还没有车要来呢 T T'

    reply = ''
    for i, (line, data) in enumerate(realtime_datas[:6]):
        reply += '车辆%s：%s\n' % (i+1, line.short_name)
        reply += '距离%s还有 %s米，' % (station.name, int(data['station_distance']))
        reply += '预计%s到达\n\n' % data['station_arriving_time'].strftime('%H:%M')
    return reply.strip()


@app.route('/list')
def list_supported_lines():
    names = set([
        line.short_name for line in BeijingBus.get_all_lines()
    ])
    names = sorted([n.decode('utf-8') for n in names])
    return render_template('list.html', line_names=names)


if __name__ == '__main__':
    app.run(debug=True, port=8484)
