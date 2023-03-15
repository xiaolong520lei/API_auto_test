"""
@Time ： 2023/2/27 10:40
@Auth ： Kevin-C
@File ：test_execute_task_list.py
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

test_data_path = os.path.join(os.path.dirname(os.getcwd()), r'test_data/test_execute_task_list.yaml')
test_data = read_config(test_data_path)
res = RequestMethod
host = AutoRunBaseInfo().host
assertion = AssertMethod
login_info = os.path.join(os.path.dirname(os.getcwd()), r'test_data/test_login.yaml')

query_data_payload = test_data['query_data_payload']

query_execute_task_api = test_data['robot_list_request_body']['query_execute_task_api']
query_execute_task_info_api = test_data['robot_list_request_body']['query_execute_task_info_api']
query_execute_task_log_api = test_data['robot_list_request_body']['query_execute_task_log_api']


@allure.feature('FEATURE:【执行任务列表】模块测试')
class TestExecuteTask:
    @allure.title('验证查询执行任务接口请求成功')
    def test_query_execute_task(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        r = res.post_method(url=f'{host}{query_execute_task_api}',json=query_data_payload, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证执行任务详情接口请求成功')
    def test_execute_task_info(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        list_data = res.post_method(url=f'{host}{query_execute_task_api}', json=query_data_payload, cookies=get_cookie)
        task_bid = list_data.json()['data']['pagedItems'][0]['bid']
        r = res.post_method(url=f'{host}{query_execute_task_info_api}', json={'bid': task_bid}, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证执行任务轨迹接口请求成功')
    def test_execute_task_log(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        list_data = res.post_method(url=f'{host}{query_execute_task_api}', json=query_data_payload, cookies=get_cookie)
        task_bid = list_data.json()['data']['pagedItems'][0]['bid']
        r = res.get_method(url=f'{host}{query_execute_task_log_api}{task_bid}', params={'pageNo': 1}, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')


if __name__ == '__main__':
    print('Python')
