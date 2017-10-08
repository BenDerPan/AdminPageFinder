from utils.web_tools import *
import http.client
from pyquery import PyQuery
import json
import datetime


class AdminPageFinder(object):
    '''
    业务后台管理地址查找实现类
    '''

    def __init__(self):
        pass

    def make_web_connection(self, proto, host, port, timeout=5):
        '''
        构建WEB请求连接对象
        :param proto: 协议类型，[http,https]
        :param host: 目标主机
        :param port: 目标端口
        :param timeout: 超时时间，单位秒
        :return: http协议对应http.client.HTTPConnection对象，https协议对应http.client.HTTPSConnection
        '''
        if proto.lower() == "http":
            return http.client.HTTPConnection(host=host, port=port, timeout=timeout)
        else:
            return http.client.HTTPSConnection(host=host, port=port, timeout=timeout)

    def get_response(self, url, append="", timeout=5):
        '''
        获取WEB请求响应对象
        :param url: 需要请求的地址URL
        :param append: 请求地址URL需要追加的相对路径
        :param timeout: 超时时间，单位秒
        :return: WEB请求响应对象
        '''
        try:
            proto, host, port, rest = split_url(url, append)
            connection = self.make_web_connection(proto, host, port, timeout)

            connection.request("GET", rest)
            return connection.getresponse()
        except Exception as e:
            print("[!]请求[{0} + {1}]失败:{2}".format(url, append, e))
            return None

    def get_full_url(self, url, append=''):
        '''
        根据根URL和相对URL地址获取完整URL地址
        :param url: 根URL地址
        :param append: 相对URL路径
        :return: 完整的URL地址
        '''
        try:
            proto, host, port, rest = split_url(url, append)
            if rest.startswith("/"):
                return "{0}://{1}:{2}{3}".format(proto, host, port, rest)
            return "{0}://{1}:{2}/{3}".format(proto, host, port, rest)
        except Exception as e:
            return None

    def check_host_online(self, url):
        '''
        监测目标主机是否在线
        :param url: 需要检测的URL地址
        :return: True-在线，False-不在线
        '''
        try:
            proto, host, port, rest = split_url(url)
            connection = self.make_web_connection(proto, host, port)

            connection.connect()
            return True
        except Exception as e:
            print("[!]检查目标URL主机是否在线失败:", e)
            return False

    def find_admin_page(self, url, validate_html=True, stop_when_found_one=True, dict=None):
        '''
        通过跑字典的方式查找指定URL对应的业务后台登录地址
        :param url: 需要查找后台管理地址的URL，一般为业务系统WEB根地址
        :param validate_html: 是否通过HTML标签验证登录组件的存在
        :param stop_when_found_one: 是否在查找到一个符合要求的后台管理地址后停止查找
        :param dict: 后台管理地址相对URL地址字典文件，None则使用默认字典
        :return: 查找结果集合对象，具体格式如下：
        ```[
                {
                    #检测到的时间戳
                    "record_time": 1507447094,
                    #检测的根URL地址
                    "base_url": "http://zz.oa.haima.com",
                    #检测的相对URL路径
                    "relative_url": "login.jsp",
                    #HTML组件验证结果，YES-验证通过，NO-验证不存在，FAILED-验证过程出现异常，UNKNOWN-未知
                    "validate_status": "YES",
                    #是否经过了HTML组件验证，true-是，false-否
                    "validated": true,
                    #管理后台地址URL
                    "admin_url": "http://zz.oa.haima.com:80/login.jsp"
                }
        ```]
        '''
        page_url = []
        if not dict:
            dict = get_default_dict()
        if self.check_host_online(url):
            with open(dict, 'r') as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == '':
                        continue
                    response = self.get_response(url, line)
                    # 若可以访问，则进一步分析
                    if response:
                        print("[*]Checking[{0}], [{1}], Status[{2}]".format(url, line, response.status))
                        # 返回200认为初步查找成功
                        if response.status == 200:
                            result = {}
                            result['base_url'] = url
                            result['relative_url'] = line
                            result['admin_url'] = None
                            result['validated'] = False
                            result['validate_status'] = "UNKNOWN"
                            result['record_time'] = int(datetime.datetime.now().timestamp())

                            fullURL = self.get_full_url(url, line)
                            result['admin_url'] = fullURL
                            if validate_html:
                                try:
                                    pageHtml = PyQuery(fullURL)
                                    inputHtmls = pageHtml('input')
                                    password = False
                                    for p in inputHtmls:
                                        if 'type' in p.attrib and p.attrib['type'] == "password":
                                            password = True
                                            break
                                    if inputHtmls.length > 1 and password:
                                        result['validated'] = True
                                        result['validate_status'] = "YES"
                                    else:
                                        result['validated'] = True
                                        result['validate_status'] = "NO"
                                except Exception as e:
                                    result['validated'] = True
                                    result['validate_status'] = "FAILED"
                            else:
                                result['validated'] = False

                            page_url.append(result)
                            print("[*]发现后台管理地址：{0},验证状态：{1}，验证结果：{2}".format(fullURL, result['validated'],
                                                                             result['validate_status']))
                            if stop_when_found_one:
                                break
        return page_url


if __name__ == '__main__':
    url = "http://zz.oa.haima.com"
    finder = AdminPageFinder()
    if finder.check_host_online(url):
        result = finder.find_admin_page(url)
        print(json.dumps(result, indent=4))
