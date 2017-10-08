from page_finder.finder import AdminPageFinder
import json
if __name__ == '__main__':
    url = "http://zz.oa.haima.com"
    finder = AdminPageFinder()
    if finder.check_host_online(url):
        result = finder.find_admin_page(url)
        print(json.dumps(result, indent=4))
