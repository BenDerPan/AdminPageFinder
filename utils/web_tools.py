import urllib
import os

INVALIDE_FILE_CHARACTERS = '/ \ ? * : " < >'.split(' ')


def replace_invalid_chars(sourceStr,replace=''):
    '''
    替换文件名中不合法的字符
    :param sourceStr: 原始文件名字符串
    :param replace: 替换字符
    :return: 替换后的文件名字符串
    '''
    for c in INVALIDE_FILE_CHARACTERS:
        sourceStr = sourceStr.replace(c, replace)
    return sourceStr


def split_url(url, append=''):
    '''
    拆分URL，并根据相对URL路径生成对应的协议，主机，端口和相对地址
    :param url: 需要拆分的URL路径
    :param append: 需要拼接的相对URL地址
    :return: （proto,host,port,rest）原组，对应（协议，主机，端口，URL相对路径）
    '''
    proto, rest = urllib.parse.splittype(url)
    host, rest = urllib.parse.splithost(rest)
    host, port = urllib.parse.splitport(host)
    if port is None:
        if proto == "http":
            port = 80
        elif proto == "https":
            port = 443
    if rest.endswith('/'):
        rest = rest[:-1]
    if append.startswith('/'):
        append = append[1:]
    rest = "{0}/{1}".format(rest, append)
    return proto, host, port, rest


def get_default_dict():
    '''
    获取默认字典文件路径
    :return: 默认字典文件路径
    '''
    path = os.path.split(os.path.abspath(__file__))[0]
    path = path.rsplit("/", maxsplit=1)[0]
    path = os.path.join(path, "page_finder/dicts/admin_page_url_dict.txt")
    return path
