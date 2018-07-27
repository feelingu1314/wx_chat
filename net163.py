# 网易移动端API接口
import os
import requests


class Net163(object):
    def __init__(self):
        # self.type = type
        self.url_headline = 'http://c.m.163.com/nc/article/headline/T1348647853363/0-10.html'
        self.url_sports = 'http://c.m.163.com/nc/article/list/T1348649079062/0-10.html'

    def get_page(self):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
        resp = requests.get(self.url_sports, headers=header)
        # print(resp.text)
        return (resp.status_code == 200 and [resp.json()] or [None])[0]

    def download_img(self, img_src, img_sign):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
        resp = requests.get(img_src, headers=header)
        return (resp.status_code == 200 and [self.save_img(resp.content, img_sign)] or [None])[0]

    def save_img(self, content, img_path):
        img_path = '{0}/{1}'.format(os.getcwd(), img_path)
        with open(img_path, 'wb') as f:
            f.write(content)

    def wxpy(self):
        result = self.get_page()['T1348649079062']
        # content = ''

        # format detail info
        if result:
            for item in result:
                if item.get('url', 'na') == 'na':
                    continue
                else:
                    img_src = item['imgsrc']
                    img_sign = item['imgsrc'][7:].split('/')[-1]
                    # content += item['title'] + '\n' + item['url'] + '\n' + img_sign + '\n\n'
                    self.download_img(img_src, img_sign)

                    yield {
                        'title': item['title'],
                        'url': item['url'],
                        'img_sign': img_sign
                    }

# for i in Net163().wxpy():
#     print(i)