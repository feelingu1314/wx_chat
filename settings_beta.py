"""
MP_FWD::forward msg from MP
FRI_FWD::forward msg to friends
GRP_FWD::forward msg to groups
GRP_IGN::ignore msg from groups
SYMBOL::reply sender by symbol

BROWSER::parameters for web driver
"""
CONTACT = {
    'MP_FWD': {
        # 'mp_global': '全球企业动态',
        'mp_coder': '进击的coder',
        # 'mp_infra': '聊聊架构',
        'mp_shanghai': '上海发布',
        # 'mp_cn': '中华元智库',
        # 'mp_devops': 'DevOps时代',
        'mp_dba': 'DBAplus社群',
        # 'mp_python_cn': 'Python中文社区',
        # 'mp_f5': 'F5Networks',
        'mp_kjmx': '科技美学官方',
        'mp_zhihuDaily': '知乎日报',
        # 'mp_me': 'feelingu1314',
    },
    'FRI_FWD': {
        'fri_me': '🚀',
    },
    'GRP_FWD': {
        'grp_game': '坑',
    },
}

BROWSER = {
    'SPLINTER': {
        'NAME': 'chrome',
        'PATH': '<YOUR>\\<PC>\\<PATH>\\chromedriver_win32\\chromedriver.exe',
    },
}


"""
mongo connection Parameters
redis connection Parameters
"""
MONGO = {
    'WECHAT': {
        'URI': 'mongodb://192.168.1.59:27017',
        'DB': 'wechat',
        'COLLECTION_1': 'info',
        'COLLECTION_2': 'msg_mp_global',
        'COLLECTION_3': 'user_stock_info',
    },
}

REDIS = {
    'WECHAT': {
        'URI': 'redis://192.168.1.59:6379/3',
    },
}

# YouDao API Parameters
YouDao_AppKey = '<YOUR APP ID>'
YouDao_SecretKey = '<YOUR APP SECRET KEY>'
YouDao_URL = 'http://openapi.youdao.com/api'
YouDao_Lang = {
    'ze':{
        'from':'zh-CHS',
        'to':'EN'
    },
    'ez':{
        'from':'EN',
        'to':'zh-CHS'
    },
    'zj':{
            'from':'zh-CHS',
            'to':'ja'
        },
    'jz':{
            'from':'ja',
            'to':'zh-CHS'
        },
    'zf':{
            'from':'zh-CHS',
            'to':'fr'
        },
    'fz':{
            'from':'fr',
            'to':'zh-CHS'
        },
    'zk':{
            'from':'zh-CHS',
            'to':'ko'
        },
    'kz':{
            'from':'ko',
            'to':'zh-CHS'
        },
    'zr':{
            'from':'zh-CHS',
            'to':'ru'
        },
    'rz':{
            'from':'ru',
            'to':'zh-CHS'
        },
    'zp':{
            'from':'zh-CHS',
            'to':'pt'
        },
    'pz':{
            'from':'pt',
            'to':'zh-CHS'
        },
    'zs':{
            'from':'zh-CHS',
            'to':'es'
        },
    'sz':{
            'from':'es',
            'to':'zh-CHS'
        }
}


"""
baidu api NLP-wechat
"""
BAIDU = {
    'NLP': {
        'WECHAT': {
            'APP_ID': '<YOUR APP_ID>',
            'API_KEY': '<YOUR API_KEY>',
            'SECRET_KEY': '<YOUR SECRET_KEY>',
        },
    },
    'IMAGE': {
        'WECHAT': {
            'APP_ID': '<YOUR APP_ID>',
            'API_KEY': '<YOUR API_KEY>',
            'SECRET_KEY': '<YOUR SECRET_KEY>',
        }
    },
}

