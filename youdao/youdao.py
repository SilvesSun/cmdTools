import hashlib
import time
import uuid

import click
import requests
import yaml
import json

YOUDAO_URL = 'http://openapi.youdao.com/api'
CONF_FILE = r'D:\projects\pytools\youdao\conf.yaml'

with open(CONF_FILE) as f:
    data = f.read()
    conf_dic = yaml.load(data, Loader=yaml.FullLoader)

app_key = conf_dic['app_key']
app_secert = conf_dic['app_secret']


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


@click.command()
@click.argument('from_to', default='ez')
@click.argument('text_to_translate')
def translate(from_to, text_to_translate):
    """COMMAND: ez|ze"""
    data = {}
    if from_to == 'ez':
        data['from'] = 'EN'
        data['to'] = 'zh-CHS'
    else:
        data['from'] = 'zh-CHS'
        data['to'] = 'EN'

    q = text_to_translate

    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = app_key + truncate(q) + salt + curtime + app_secert
    sign = encrypt(signStr)
    data['appKey'] = app_key
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign

    response = do_request(data)
    content = response.content.decode('utf-8')
    content_json = json.loads(content)
    try:
        explains = content_json['basic']['explains']
        fromat_exp = '\n'.join(explains)
        print(fromat_exp)
    except:
        print('no result found')


if __name__ == '__main__':
    translate()
