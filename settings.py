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
        'fri_ds': '邓爽',
        'fri_wd': '韦东',
    },
    'GRP_FWD': {
        # 'grp_guys': 'Guys',  # 805b0cca
        'grp_god': '一神看二傻',  # 0567b03e
        # 'grp_game': '坑',  # 3aae1bfc
    },
}

BROWSER = {
    'SPLINTER': {
        'NAME': 'chrome',
        'PATH': 'C:\\Users\\Agodabkk\\Downloads\\chromedriver_win32\\chromedriver.exe',  # JXMW2M2
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
YouDao_AppKey = '6c9dc5b3d5feb395'  # app id
YouDao_SecretKey = 'ag0rT1g83119oLzlC4r4n6X8TM300F7B'  # app secret key
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
            'APP_ID': '11731276',
            'API_KEY': 'q1uuofq0d3PC86eRiMr9GX7f',
            'SECRET_KEY': 'HiczI8lC98MD8oPg5hTCPzFDPSGs3hQO',
        },
    },
    'IMAGE': {
        'WECHAT': {
            'APP_ID': '11726146',
            'API_KEY': '38Behfba1DDzbMDC5ArspKi4',
            'SECRET_KEY': 'Ej5vBZTqa7SEMBvm3TMudCxIZ1WfG0oz',
        }
    },
}

