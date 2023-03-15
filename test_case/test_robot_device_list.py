"""
@Time ： 2023/2/10 18:21
@Auth ： Kevin-C
@File ：test_robot_device_list.py
@IDE ：PyCharm
"""
import os
import sys
import random
import pytest
from common.Assert import AssertMethod
from common.readConfig import read_config
from common.Request import RequestMethod
from run_main.main import AutoRunBaseInfo
import allure
from common.Log import log

test_data_path = os.path.join(os.path.dirname(os.getcwd()), r'test_data/test_robot_device_list.yaml')
test_data = read_config(test_data_path)
res = RequestMethod
host = AutoRunBaseInfo().host
header = test_data['robot_list_request_body']['request_header']

api = test_data['robot_list_request_body']['api']
device_state_api = test_data['robot_list_request_body']['device_state_api']
device_info_api = test_data['robot_list_request_body']['device_info_api']
update_device_api = test_data['robot_list_request_body']['update_device_api']

payload_data = test_data['test_payload']
change_state_payload = test_data['change_device_state']
update_device_info_payload = test_data['update_device_info']

assertion = AssertMethod


@allure.feature('FEATURE:【机器人设备管理】模块测试')
class TestRobotDeviceListApi:

    @allure.title('验证查询接口请求成功')
    def test_query_data(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        r = res.post_method(url=f'{host}{api}', data=payload_data, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证修改状态接口请求成功')
    def test_change_device_state(self, get_cookie):
        cookie = get_cookie
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        query_data = res.post_method(url=f'{host}{api}', data=payload_data, cookies=cookie)
        device_bid = query_data.json()['data']['records'][0]['bid']
        device_state = query_data.json()['data']['records'][0]['state']
        change_state_payload['bid'] = device_bid
        change_state_payload['state'] = -1 if device_state == 0 else 0
        r = res.post_method(url=f'{host}{device_state_api}', data=change_state_payload, cookies=cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证修改设备名称接口请求成功')
    def test_update_device_info(self, get_cookie):
        cookie = get_cookie
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        query_data = res.post_method(url=f'{host}{api}', data=payload_data, cookies=cookie)
        update_device_info_payload['bid'] = query_data.json()['data']['records'][0]['bid']
        update_device_info_payload['enterpriseId'] = query_data.json()['data']['records'][0]['enterpriseId']
        update_device_info_payload['hostName'] = query_data.json()['data']['records'][0]['hostName']
        update_device_info_payload['name'] = f'auto_test_name{random.randint(1000,9999)}'
        header['Content-Type'] = 'application/json;charset=UTF-8'
        r = res.post_method(url=f'{host}{update_device_api}', json=update_device_info_payload, cookies=cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证修改设备名称重复')
    def test_update_device_name_duplicate(self, get_cookie):
        cookie = get_cookie
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        query_data = res.post_method(url=f'{host}{api}', data=payload_data, cookies=cookie)
        update_device_info_payload['bid'] = query_data.json()['data']['records'][0]['bid']
        update_device_info_payload['enterpriseId'] = query_data.json()['data']['records'][0]['enterpriseId']
        update_device_info_payload['hostName'] = query_data.json()['data']['records'][0]['hostName']
        update_device_info_payload['name'] = query_data.json()['data']['records'][0]['name']
        header['Content-Type'] = 'application/json;charset=UTF-8'
        r = res.post_method(url=f'{host}{update_device_api}', json=update_device_info_payload, cookies=cookie)
        assertion.assert_equal(r.json()['message'], '设备名称已存在')
        log.info(f'测试完成！\n')


if __name__ == '__main__':
    pytest.main(['-s', './test_robot_device_list.py'])
    print('Python')
