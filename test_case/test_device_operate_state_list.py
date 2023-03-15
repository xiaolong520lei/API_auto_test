"""
@Time ： 2023/2/28 11:35
@Auth ： Kevin-C
@File ：test_device_operate_state_list.py
@IDE ：PyCharm
"""
import datetime
import os
import random
import sys
import pytest
from common.Assert import AssertMethod
from common.readConfig import read_config
from common.Request import RequestMethod
from run_main.main import AutoRunBaseInfo
import allure
from common.Log import log

test_data_path = os.path.join(os.path.dirname(os.getcwd()), r'test_data/test_device_operate_state.yaml')
test_data = read_config(test_data_path)
res = RequestMethod
host = AutoRunBaseInfo().host
assertion = AssertMethod

query_data_payload = test_data['query_data_payload']
query_device_robot_list_payload = test_data['query_device_robot_list_payload']

query_robots_api = test_data['robot_list_request_body']['query_robots_api']
get_state_api = test_data['robot_list_request_body']['get_state_api']
query_device_robot_list_api = test_data['robot_list_request_body']['query_device_robot_list_api']


@allure.feature('FEATURE:【设备运行状态】模块测试')
class TestDispatchTask:
    @allure.title('验证查询设备运行状态接口请求成功')
    def test_query_devices_state(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        res.post_method(url=f'{host}{query_robots_api}', cookies=get_cookie)
        r = res.post_method(url=f'{host}{get_state_api}', json=query_data_payload, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证绑定机器人接口请求成功')
    def test_query_device_robot_list(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        devices_data = res.post_method(url=f'{host}{get_state_api}', json=query_data_payload, cookies=get_cookie)
        device_id = devices_data.json()['data']['serviceStateList']['records'][0]['deviceId']
        query_device_robot_list_payload['deviceId'] = device_id
        r = res.post_method(url=f'{host}{query_device_robot_list_api}', json=query_device_robot_list_payload, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')


if __name__ == '__main__':
    print('Python')
