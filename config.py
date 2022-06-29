import json

VA_NAME = ""
VA_VER = ""
VA_ALIAS = []
VA_TBR = []
VA_CMD_LIST = {}
VA_ANS_LIST = {}


def load_config(cfg):
    global VA_NAME, VA_VER, VA_CMD_LIST, VA_TBR, VA_ANS_LIST, VA_ALIAS
    with open(cfg, encoding='utf-8') as f:
        data = json.load(f)

    try:
        VA_NAME = data['VA_NAME']
        VA_VER = data['VA_VER']
        VA_ALIAS = tuple(data['VA_ALIAS'])
        VA_TBR = data['VA_TBR']
        VA_CMD_LIST = data['VA_CMD_LIST']
        VA_ANS_LIST = data['VA_ANS_LIST']

    except Exception:
        print('error while loading config.json')
