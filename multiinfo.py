import os, requests, warnings

from requests.exceptions import RequestException
from pyquery import PyQuery as pq
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning
from splinter.browser import Browser
from settings import BROWSER


class GetInfo(object):

    def __init__(self, text):
        self.text = text # string / generator

    @staticmethod
    def request_url(url, headers):
        try:
            #去除链接https时不使用证书认证而产生的warning
            warnings.filterwarnings(action='ignore', category=InsecureRequestWarning)
            response = requests.get(url, headers=headers, verify=False)
            if response.status_code == 200:
                res_text = response.text
                # res_json = response.json()
                # res_content = response.content
                return res_text
            else:
                return None
        except RequestException as e:
            raise e

    def smzdm(self):
        raw = self.text.split('&')
        if raw[0] == '':
            num = 5
        elif isinstance(int(raw[0]), int):
            num = int(raw[0])
        else:
            raise ValueError('incorrect arguments: %s' % self.text)
        url = 'https://post.smzdm.com/'
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }
        response = self.request_url(url, headers)  # text
        content = '值得买原创文：\n'
        count = 0

        def parse_smzdm(html):
            doc = pq(response)
            for item in doc('#feed-main-list > li.feed-row-wide > div > div.z-feed-content > h5 > a').items():
                yield {
                    'title': '\n'+item.text(),
                    'link': item.attr('href'),
                }

        for item in parse_smzdm(response):
            if count < num:
                for v in item.values():
                    content += '%s\n' % v
            else:
                break
            count += 1
        return content


    def enterprise(self):
        driver = Browser(driver_name=BROWSER['SPLINTER']['NAME'], executable_path=BROWSER['SPLINTER']['PATH'], headless=True)
        driver.visit(self.text)
        fiscal = False
        n = 0

        items = driver.find_by_tag('strong')
        for seq, item in enumerate(items):
            n += 1
            if not item.text == '财报信息':
                if seq == 0:
                    content = '全球企业动态[%s]\n\n' % datetime.now().date()
                elif seq == 1:
                    content += '概要：\n%s\n' % item.text
                else:
                    content += '\n%d. %s\n' % (seq-1, item.text)
            else:
                fiscal = True
                break
        if fiscal:
            content += '\n财报信息:\n' + driver.find_by_xpath('//*[@id="js_content"]/p[%s]' % str(n*2)).text
        
        content += '\n\n' + self.text
        return content

