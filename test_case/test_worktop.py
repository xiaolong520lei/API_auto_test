"""
@Time ： 2023/2/22 17:09
@Auth ： Kevin-C
@File ：test_worktop.py
@IDE ：PyCharm
"""
import os
import sys
import pytest
from common.Assert import AssertMethod
from common.readConfig import read_config
from common.Request import RequestMethod
from run_main.main import AutoRunBaseInfo
import allure
from common.Log import log
import time

test_data_path = os.path.join(os.path.dirname(os.getcwd()), r'test_data/test_worktop.yaml')
test_data = read_config(test_data_path)
res = RequestMethod
host = AutoRunBaseInfo().host
assertion = AssertMethod

query_data_payload = test_data['query_data_payload']
sumExecuteMonthTask_payload = test_data['sumExecuteMonthTask_payload']

robotServiceSkillSumRate_api = test_data['robot_list_request_body']['robotServiceSkillSumRate_api']
sumExecuteTask_api = test_data['robot_list_request_body']['sumExecuteTask_api']
sumTask_api = test_data['robot_list_request_body']['sumTask_api']
queryExeTaskListByCon_api = test_data['robot_list_request_body']['queryExeTaskListByCon_api']
queryDispatchTaskListByCon_api = test_data['robot_list_request_body']['queryDispatchTaskListByCon_api']
sumExecuteMonthTask_api = test_data['robot_list_request_body']['sumExecuteMonthTask_api']


@allure.feature('FEATURE:【工作台】模块测试')
class TestWorkTop:
    @allure.title('验证机器人使用率接口请求成功')
    @pytest.mark.dependency()
    def test_query_skill_rate(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        r = res.post_method(url=f'{host}{robotServiceSkillSumRate_api}', cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证执行任务统计接口请求成功')
    def test_query_count_execute_task(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        r = res.post_method(url=f'{host}{sumExecuteTask_api}', cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证调度任务统计接口请求成功')
    def test_query_count_dispatch_task(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        r = res.post_method(url=f'{host}{sumTask_api}', cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证查询执行任务接口请求成功')
    def test_query_execute_task(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        r = res.post_method(url=f'{host}{queryExeTaskListByCon_api}', json=query_data_payload, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证查询调度任务接口请求成功')
    def test_query_dispatch_task(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        r = res.post_method(url=f'{host}{queryDispatchTaskListByCon_api}', json=query_data_payload, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证查询执行任务趋势接口请求成功')
    def test_query_execute_task_month(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        sumExecuteMonthTask_payload['year'] = time.localtime()[0]
        r = res.post_method(url=f'{host}{sumExecuteMonthTask_api}', data=sumExecuteMonthTask_payload, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')


if __name__ == '__main__':
    pytest.main(['-s', './test_worktop.py'])
    print('Python')
