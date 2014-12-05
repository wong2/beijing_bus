#-*-coding:utf-8-*-

import time
import click
from datetime import datetime
from beijing_bus import BeijingBus


@click.group()
def cli():
    pass


@click.command(help='build or re-build the cache')
def build_cache():
    import logging
    logging.basicConfig(level=logging.DEBUG)
    BeijingBus.build_cache()
    click.secho('Done!', fg='green')


def echo_realtime_data(line, station_num):
    station = line.stations[station_num-1]
    realtime_data = line.get_realtime_data(station_num)
    click.clear()
    now = datetime.now().strftime('%H:%M:%S')
    title = '实时数据 [%s]  线路：%s  (每5秒自动刷新，更新于%s)' % (station.name, line.name, now)
    click.secho(title, fg='green', bold=True)
    click.echo()
    realtime_data = filter(lambda d: d['station_arriving_time'], realtime_data)
    realtime_data.sort(key=lambda d: d['station_arriving_time'])
    for i, data in enumerate(realtime_data):
        click.secho('公交%s：' % (i+1), bold=True, underline=True)
        click.echo('距离 %s 还有%s米' % (station.name, data['station_distance']))
        click.echo('预计 %s 到达' % data['station_arriving_time'].strftime('%H:%M'))
        click.echo()


@click.command()
def query():
    q = click.prompt('请输入线路名', value_proc=str)
    lines = BeijingBus.search_lines(q)
    for index, line in enumerate(lines):
        click.echo()
        click.secho('[%s] %s' % (index+1, line.name), bold=True, underline=True)
        station_names = [s.name for s in line.stations]
        click.echo()
        click.echo('站点列表：%s' % ','.join(station_names))

    click.echo()
    q = click.prompt('请从结果中选择线路编号', type=int)

    line = lines[q-1]
    click.clear()
    click.echo('你选择了 %s，下面请选择站点' % line.name)
    click.echo()
    for index, station in enumerate(line.stations):
        click.echo('[%s] %s' % (index+1, station.name))

    click.echo()
    q = click.prompt('请从结果中选择线路编号', type=int)

    while True:
        echo_realtime_data(line, q)
        time.sleep(5)
    

cli.add_command(build_cache)
cli.add_command(query)


if __name__ == '__main__':
    cli()
