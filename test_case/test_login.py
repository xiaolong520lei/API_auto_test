"""
@Time ： 2023/2/8 15:17
@Auth ： Kevin-C
@File ：test_login.py
@IDE ：PyCharm
"""
import os
import sys
from common.Assert import AssertMethod
from common.readConfig import read_config
from common.Request import RequestMethod
from run_main.main import AutoRunBaseInfo
import pytest
import allure
from common.Log import log
import base64
import ddddocr

test_data_path = os.path.join(os.path.dirname(os.getcwd()), r'test_data/test_login.yaml')
test_data = read_config(test_data_path)
res = RequestMethod
host = AutoRunBaseInfo().host
api = test_data['login_request_body']['api']
menu_api = test_data['login_request_body']['menu']
permission_api = test_data['login_request_body']['permission']
headers = test_data['login_request_body']['request_header']
payload_data = test_data['test_payload']
assertion = AssertMethod


@allure.feature('FEATURE:【管理平台登录】模块测试')
class TestLoginApi:

    @allure.story('STORY:用户名密码正确验证')
    @allure.step('STEP:用户名密码正确验证')
    @pytest.mark.parametrize('username,password', payload_data['right_account'])
    def test_right_account(self, username, password):
        def_name = sys._getframe().f_code.co_name
        log.info(f'开始测试：{def_name}')
        get_image = res.get_method(url=f'{host}/plat/api/sys/getImageCode?userName={username}')
        big_pic = get_image.json()['data']['bigImageBase64']
        small_pic = get_image.json()['data']['smallImageBase64']
        big_pic_path = os.path.join(os.path.dirname(os.getcwd()), r'temp\big.png')
        small_pic_path = os.path.join(os.path.dirname(os.getcwd()), r'temp\small.png')
        save_image(big_pic_path, big_pic)
        save_image(small_pic_path, small_pic)
        log.info('验证图保存成功！')
        moveposx = get_location(big_pic_path, small_pic_path)
        log.info('获取拖图坐标成功')
        json_data = {"movePosX": moveposx, "username": username, "password": password}
        r = res.post_method(url=f'{host}{api}', headers=headers, json=json_data)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.story('STORY:错误用户名密码验证')
    @allure.step('STEP:错误用户名密码验证')
    @pytest.mark.parametrize('username,password', payload_data['wrong_account'])
    def test_wrong_account(self, username, password):
        def_name = sys._getframe().f_code.co_name
        log.info(f'开始测试：{def_name}')
        get_image = res.get_method(url=f'{host}/plat/api/sys/getImageCode?userName={username}')
        big_pic = get_image.json()['data']['bigImageBase64']
        small_pic = get_image.json()['data']['smallImageBase64']
        big_pic_path = os.path.join(os.path.dirname(os.getcwd()), r'temp\big.png')
        small_pic_path = os.path.join(os.path.dirname(os.getcwd()), r'temp\small.png')
        save_image(big_pic_path, big_pic)
        save_image(small_pic_path, small_pic)
        log.info('验证图保存成功！')
        moveposx = get_location(big_pic_path, small_pic_path)
        log.info('获取拖图坐标成功')
        json_data = {"movePosX": moveposx, "username": username, "password": password}
        r = res.post_method(url=f'{host}{api}', headers=headers, json=json_data)
        assertion.assert_equal(r.json()['message'], '用户名或密码错误')
        log.info(f'测试完成！\n')

    @allure.story('STORY:滑块验证不通过')
    @allure.step('STEP:正确用户名密码验证')
    @pytest.mark.parametrize('movePosX,username,password', payload_data['wrong_place'])
    def test_wrong_slide(self, movePosX, username, password):
        def_name = sys._getframe().f_code.co_name
        log.info(f'开始测试：{def_name}')
        json_data = {"movePosX": movePosX, "username": username, "password": password}
        res.get_method(url=f'{host}/plat/api/sys/getImageCode?userName={username}')
        log.info('请求slide picture 成功！')
        r = res.post_method(url=f'{host}{api}', headers=headers, json=json_data)
        assertion.assert_equal(r.json()['message'], '验证不通过')
        log.info(f'测试完成！\n')

    @allure.step('STEP:滑块移动距离参数缺失')
    @pytest.mark.parametrize('movePosX,username,password', payload_data['wrong_place'])
    def test_miss_slide_params(self, movePosX, username, password):
        def_name = sys._getframe().f_code.co_name
        log.info(f'开始测试：{def_name}')
        json_data = {"movePosX": movePosX, "username": username, "password": password}
        r = res.post_method(url=f'{host}{api}', headers=headers, json=json_data)
        assertion.assert_equal(r.json()['message'], '滑块移动距离参数缺失')
        log.info(f'测试完成！\n')

    @allure.step('STEP:菜单接口获取成功')
    def test_get_menu(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.info(f'开始测试：{def_name}')
        r = res.get_method(url=f'{host}{menu_api}', params={'menuType': 0}, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.step('STEP:权限接口获取成功')
    def test_get_permission(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.info(f'开始测试：{def_name}')
        r = res.get_method(url=f'{host}{permission_api}', cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')


def save_image(filename, image_base64):
    image_data = base64.b64decode(image_base64)
    with open(filename, 'wb') as f:
        f.write(image_data)


def get_location(big_pic_path, small_pic_path):
    det = ddddocr.DdddOcr(det=False, ocr=False)
    with open(small_pic_path, 'rb') as f:
        target_bytes = f.read()
    with open(big_pic_path, 'rb') as f:
        background_bytes = f.read()
    location = det.slide_match(target_bytes, background_bytes, simple_target=True)
    x_location = location['target'][0]
    return x_location


if __name__ == '__main__':
    pytest.main(['-s', './test_login.py::TestLoginApi::test_get_menu'])
    print(test_data_path)
