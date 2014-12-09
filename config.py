#-*-coding:utf-8-*-

WEIXIN_TOKEN = ''
SENTRY_DSN = ''

ON_FOLLOW_MESSAGE = {
   'title': '',
   'description': '',
   'picurl': '',
   'url': '',
}


try:
    from local_config import *
except:
    pass
