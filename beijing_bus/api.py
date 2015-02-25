#-*-coding:utf-8-*-

import logging
import requests
import xmltodict 

from requests.exceptions import ConnectionError


API_ENDPOINT = 'http://mc.aibang.com/aiguang/bjgj.c'
REALTIME_ENDPOINT = 'http://bjgj.aibang.com:8899/bus.php'


def request_api(url, params):
    for _ in range(3):
        try:
            r = requests.get(url, params=params, headers={'cid':1024})
        except (ConnectionError, requests.exceptions.Timeout) as e:
            continue
        else:
            return xmltodict.parse(r.text)
    raise e


def get_line_update_state():
    logging.debug('Getting all lines')
    params = {'m': 'checkUpdate', 'version': '1'}
    return request_api(API_ENDPOINT, params)


def get_bus_offline_data(line_id):
    logging.debug('Fetching line: %s' % line_id)
    params = {'m': 'update', 'id': line_id}
    return request_api(API_ENDPOINT, params)


def get_realtime_data(line_id, station_num):
    params = {
        'city': '北京',
        'id': line_id,
        'no': station_num,
        'type': 2,
        'encrpt': 1,
        'versionid': 2
    }
    return request_api(REALTIME_ENDPOINT, params)
