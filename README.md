# AdminPageFinder
自动化查找、验证系统后台登录地址。Python3.5.3环境。

# 使用说明
* 安装依赖库：`pip install -r requirements.txt`
* 用法示例：
```python
from page_finder.finder import AdminPageFinder
import json
if __name__ == '__main__':
    url = "http://zz.oa.haima.com"
    finder = AdminPageFinder()
    if finder.check_host_online(url):
        result = finder.find_admin_page(url)
        print(json.dumps(result, indent=4))
```

结果输出：
```shell
[*]Checking[http://zz.oa.haima.com], [login/], Status[302]
[*]Checking[http://zz.oa.haima.com], [login.jsp], Status[200]
[*]发现后台管理地址：http://zz.oa.haima.com:80/login.jsp,验证状态：True，验证结果：YES
[
    {
        "validate_status": "YES",
        "relative_url": "login.jsp",
        "validated": true,
        "admin_url": "http://zz.oa.haima.com:80/login.jsp",
        "base_url": "http://zz.oa.haima.com",
        "record_time": 1507448255
    }
]
```

