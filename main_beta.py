import queue, re, requests, json
from multiprocessing.managers import BaseManager
from aip import AipNlp, AipImageClassify
from uuid import uuid1
from wxpy import *
from wechat_sender import *
from settings_beta import YouDao_Lang, BAIDU, CONTACT


bot = Bot(cache_path=True, qr_path="<YOUR>\\<PC>\\<PATH>wxpy.jpg")
bot.enable_puid("wxpy_puid.pkl")
me = bot.self
helper = bot.file_helper

fri_fwd = list(map(lambda x: ensure_one(bot.friends().search(x)), [v for v in CONTACT['FRI_FWD'].values()]))
grp_fwd = list(map(lambda x: ensure_one(bot.groups().search(x)), [v for v in CONTACT['GRP_FWD'].values()]))
mp_fwd = list(map(lambda x: ensure_one(bot.mps().search(x)), [v for v in CONTACT['MP_FWD'].values()]))
print('activate friends => %s\nactivate groups => %s\nactivate mp => %s' % (fri_fwd, grp_fwd, mp_fwd))

class QueueManager(BaseManager):
    pass

# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')
server_addr = '127.0.0.1'


def connect_queue(param):
    print('Connect to server %s...' % server_addr)
    # 端口和验证码注意保持与task_master.py设置的完全一致:
    m = QueueManager(address=(server_addr, 5000), authkey=b'abc')
    m.connect()
    # 获取Queue的对象:
    task = m.get_task_queue()
    result = m.get_result_queue()
    try:
        result.put(param)
    except Queue.Empty:
        print('task queue is empty.')
    print('worker exit.')


def set_flag(messages, messages_type):
    """
    :param messages: @bot.register => reply_fri() => msg.text, msg.type
    :return: dict() => type:boolean => trans, lang, symbol
    """
    # print(messages_type)
    flag = {
        'trans': False,
        'kw': False,
        'query_mp_global': None,
        'news_global': False,
    }

    pattern_words = re.compile('[A-Za-z\d\W]+', re.S)
    pattern_nonWords = re.compile('[\d\W]+', re.S)
    pattern_kw = re.compile('^#(.*?)', re.S)  # [大盘，天气, 买， 动态]

    if messages_type == 'Text':
        if re.fullmatch(pattern_kw, messages):
            flag['kw'] = True
        elif (re.fullmatch(pattern_words, messages) and not re.fullmatch(pattern_nonWords, messages)) or (messages.split(' ', 1)[0] in YouDao_Lang.keys()):
            flag['trans'] = True
            flag['kw'] = True
        else:
            pass
    elif messages_type == 'Sharing':
        if messages == '昨夜今晨全球大公司动态':
            flag['news_global'] = True
    else:
        pass

    return flag


def baidu_image(image_path):
    # content = ''
    options = dict()
    options['baike_num'] = 1
    client = AipImageClassify(BAIDU['IMAGE']['WECHAT']['APP_ID'], BAIDU['IMAGE']['WECHAT']['API_KEY'],
                              BAIDU['IMAGE']['WECHAT']['SECRET_KEY'])
    
    def get_file_content(file_path):
        with open(file_path, 'rb') as fb:
            return fb.read()

    image = get_file_content(image_path)
    response = client.advancedGeneral(image, options)
    # print(response)
    if 'error_code' not in response:
        if response['result'][0]['baike_info'] and response['result'][0]['root'] != '非自然图像-屏幕截图':
            keyword = response['result'][0]['keyword']
            description = response['result'][0]['baike_info']['description']
            image_url = response['result'][0]['baike_info']['image_url']
            reply_image_path = ".\\grp_img\\reply_%s.jpg" % image_path.split('\\')[2][:-4]
            with open(reply_image_path, 'wb') as f:
                f.write(requests.get(image_url).content)
            content = '%s\n%s' % (keyword, description)
            return content, reply_image_path
        else:
            return None


def baidu_nlp(title=None):
    client = AipNlp(BAIDU['NLP']['WECHAT']['APP_ID'], BAIDU['NLP']['WECHAT']['API_KEY'],
                    BAIDU['NLP']['WECHAT']['SECRET_KEY'])

    if title:
        keywords = ''
        tag = []
        result_lexer = client.lexer(title)

        # step1::lexer() => keywords
        for i in result_lexer['items']:
            if i['ne'] in ['PER', 'LOC', 'ORG', 'TIME'] or i['pos'] in ['n', 'nr', 'nz', 'ns', 'nt', 'nw']:
                keywords += i['item']

        # step2::topic() => category
        topics = client.topic(keywords, result_lexer['text'])
        try:
            if 'error_code' not in topics:
                for i in topics['item']['lv1_tag_list']:
                    tag.append(i['tag'])
            else:
                print('baidu_nlp() => client() => error_code: %s | error_msg: %s' % (topics['error_code'], topics['error_msg']))
                tag.append('其他')
        except Exception as e:
            print('baidu_nlp() Exception: %s' % e)
        finally:
            pass

        return tag


# reply friends
@bot.register(fri_fwd, except_self=False)
def reply_fri(msg):
    flag = set_flag(msg.text, msg.type)

    if flag['kw']:
        if msg.sender.puid != msg.receiver.puid:
            if msg.sender.puid == me.puid:
                receiver = msg.receiver.name
                puid = msg.receiver.puid
            else:
                receiver = msg.sender.name
                puid = msg.sender.puid
        else:
            receiver = msg.sender.name
            puid = msg.sender.puid
        connect_queue('&'.join(('#翻译%s' % msg.text if flag['trans'] else msg.text, puid, receiver)))
    elif flag['news_global']:
        connect_queue('@'.join(('#动态%s' % msg.url, msg.sender.puid, msg.sender.name)))

    print('fri_msg: {}->{}| {} | {} | {} | {}'.format(msg.sender.name, msg.receiver.name, msg.text, msg.type, msg.receive_time, msg.url))


# reply groups
@bot.register(grp_fwd, except_self=False)
def reply_grp(msg):
    flag = set_flag(msg.text, msg.type)
    if flag['kw']:
        connect_queue('&'.join(('#翻译%s' % msg.text if flag['trans'] else msg.text, msg.chat.puid, msg.chat.name)))

    print('grp_msg: {}->{}| {} | {} | {}'.format(msg.member.name, msg.chat.name, msg.text, msg.type, msg.receive_time))


# forward msg from <MP_FWD>
@bot.register(mp_fwd)
def forward_mp(msg):
    flag = set_flag(msg.text, msg.type)
    
    if flag['news_global']:
        for member in fri_fwd:
            connect_queue('@'.join(('#动态%s' % msg.url, msg.sender.puid, member.name)))
        for group in grp_fwd:
            connect_queue('@'.join(('#动态%s' % msg.url, msg.sender.puid, group.name)))
    else:
        print('msg: {} | {} | {} | {}'.format(msg.sender, msg.text, msg.type, msg.receive_time))
        return


listen(bot, token='houwei2018', port=10245)
bot.join()
# embed()