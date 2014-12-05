## 北京实时公交

该项目是北京实时公交查询接口的Python绑定，接口逆向自其[安卓客户端](http://www.bjjtw.gov.cn/topic/bjssgj/)

### Quick Start

* `pip install -r requirements.txt` 安装依赖
* `python manage.py build_cache` 获取离线数据，建立本地缓存

项目自带了一个终端中的查询工具作为例子，运行： `python manage.py query`

### Roadmap

- [x] 实现 beijing_bus 模块，提供需要的Python接口
- [x] 终端中的查询工具
- [ ] webapp
- [ ] 微信公众号
