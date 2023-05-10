"""
@Time ： 2023/2/8 9:33
@Auth ： Kevin-C
@File ：conftest.py
@IDE ：PyCharm
"""
import sys

import pytest
import requests.utils
from common.Request import RequestMethod
import ddddocr
import os
import base64

from common.md5_encode import pwd_md5_encode
from run_main.main import AutoRunBaseInfo
from common.Log import log
from common.readConfig import read_config

config_info = os.path.join(os.path.dirname(os.getcwd()), r'config/config.yaml')
test_data = read_config(config_info)
res = RequestMethod
host = AutoRunBaseInfo().host
login_api = test_data['login_api']
account_info = test_data['account']
login_header = test_data['request_header']
'''
scope参数为session：所有测试.py文件执行前执行一次
scope参数为module：每一个测试.py文件执行前都会执行一次conftest文件中的fixture
scope参数为class：每一个测试文件中的测试类执行前都会执行一次conftest文件中的
scope参数为function：所有文件的测试用例执行前都会执行一次conftest文件中的fixture
'''


@pytest.fixture(scope='function')
def get_token():
    token = '123345345'
    print('这是Fixture：开始了')
    return token


# 用 fixture 实现 teardown 并不是一个独立的函数，而是用 yield 关键字来开启 teardown 操作。
# autouser 设置为Ture 则不需要在测试用例中传入函数名，设置为否是则需要在用例中传入函数名。
@pytest.fixture(scope='function')
def get_num():
    num = 'ccc'
    print('这是set_up开始执行...')
    yield num
    print('这是tear_down结束执行!!!')


@pytest.fixture(scope='module')
def get_cookie():
    while True:
        get_image = res.get_method(url=f'{host}/plat/api/sys/getImageCode?userName={account_info["username"]}')
        big_pic = get_image.json()['data']['bigImageBase64']
        small_pic = get_image.json()['data']['smallImageBase64']
        big_pic_path = os.path.join(os.path.dirname(os.getcwd()),r'temp/big.png')
        small_pic_path = os.path.join(os.path.dirname(os.getcwd()),r'temp/small.png')
        save_image(big_pic_path, big_pic)
        save_image(small_pic_path, small_pic)
        moveposx = get_location(big_pic_path,small_pic_path)
        encode_password = pwd_md5_encode(account_info['password'])
        json_data = {"movePosX": moveposx, "username": account_info['username'], "password": encode_password}
        r = res.post_method(url=f'{host}{login_api}', headers=login_header, json=json_data)
        if r.json()['code'] == 200:
            cookies = r.cookies
            cookie = requests.utils.dict_from_cookiejar(cookies)
            log.info(f'获取Cookie成功！')
            return cookie
        elif r.json()['code'] == 500 and r.json()['message'] == '验证不通过':
            continue
        else:
            log.error(f'获取cookie失败')
            raise Exception(f'服务器可能异常:{r.json()}')


def save_image(filename,image_base64):
    image_data = base64.b64decode(image_base64)
    with open(filename,'wb') as f:
        f.write(image_data)


def get_location(big_pic_path,small_pic_path):
    det = ddddocr.DdddOcr(det=False, ocr=False)
    with open(small_pic_path, 'rb') as f:
        target_bytes = f.read()
    with open(big_pic_path, 'rb') as f:
        background_bytes = f.read()
    location = det.slide_match(target_bytes, background_bytes,simple_target=True)
    x_location = location['target'][0]
    return x_location


if __name__ == '__main__':

    print(host)


