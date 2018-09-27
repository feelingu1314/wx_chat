# youdao translation api

import requests
import hashlib
import random
from urllib3.exceptions import InsecureRequestWarning
import warnings
import settings


warnings.filterwarnings(action='ignore', category=InsecureRequestWarning)


class YouDaoTranslation(object):
    def __init__(self, query, lang='ez'):
        self.query = query
        self.from_lang = settings.YouDao_Lang[lang]['from']
        self.to_lang = settings.YouDao_Lang[lang]['to']

        salt = random.randint(1, 65535)
        sign = settings.YouDao_AppKey + self.query + str(salt) + settings.YouDao_SecretKey
        m1 = hashlib.md5()
        m1.update(sign.encode('utf-8'))
        sign = m1.hexdigest()
        self.url = settings.YouDao_URL + '?appKey=' + settings.YouDao_AppKey + '&q=' + self.query + '&from=' + \
                   self.from_lang + '&to=' + self.to_lang + '&salt=' + str(salt) + '&sign=' + sign

    def _request(self):
        response = requests.get(self.url, verify=False)
        response = (response.status_code == 200 and [response.json()] or [None])[0]
        return response

    def wxpy(self):
        result = self._request()
        response = ''
        if result:
            if result['errorCode'] == '0':
                # key: basic在返回字典中
                if 'basic' in result:
                    if 'translation' in result:
                        response = response + result['translation'][0]
                    if 'explains' in result['basic'] and result['basic']['explains']:
                        response = response + '\n\n词典：'
                        for i, element in enumerate(result['basic']['explains'], 1):
                            response = response + '\n{}. {}'.format(i, element)
                    if 'phonetic' in result['basic'] and result['basic']['phonetic']:
                        response = response + '\n\n发音：' + result['basic']['phonetic']
                    if 'web' in result and result['web']:
                        response = response + '\n\n网络释义：'
                        for i, element in enumerate(result['web'], 1):
                            response = response + '\n{0}.{1}：{2}'.format(i, element['key'], element['value'][0])
                else:
                    if 'translation' in result:
                        response = response + '{}'.format(result['translation'][0])
            else:
                return '输入格式有误: %d' % result['errorCode']
        else:
            return result

        return response


# print(YouDaoTranslation('苹果', 'zj').wxpy())