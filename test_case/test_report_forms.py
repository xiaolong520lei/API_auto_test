"""
@Time ： 2023/2/28 14:32
@Auth ： Kevin-C
@File ：test_report_forms.py
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

test_data_path = os.path.join(os.path.dirname(os.getcwd()), r'test_data/test_report_forms.yaml')
test_data = read_config(test_data_path)
res = RequestMethod
host = AutoRunBaseInfo().host
assertion = AssertMethod

robots_report_forms_payload = test_data['robots_report_forms_payload']
devices_report_forms_payload = test_data['devices_report_forms_payload']
skills_report_forms = test_data['skills_report_forms']
tasks_report_forms_payload = test_data['tasks_report_forms_payload']

robots_report_forms_api = test_data['robot_list_request_body']['robots_report_forms_api']
devices_report_forms_api = test_data['robot_list_request_body']['devices_report_forms_api']
skills_report_forms_api = test_data['robot_list_request_body']['skills_report_forms_api']
tasks_report_forms_api = test_data['robot_list_request_body']['tasks_report_forms_api']


@allure.feature('FEATURE:【报表】模块测试')
class TestDispatchTask:
    @allure.title('验证机器人统计接口请求成功')
    def test_robots_report_forms(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        r = res.post_method(url=f'{host}{robots_report_forms_api}', json=robots_report_forms_payload, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证设备统计接口请求成功')
    def test_devices_report_forms(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        r = res.post_method(url=f'{host}{devices_report_forms_api}', json=devices_report_forms_payload,
                            cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证技能统计接口请求成功')
    def test_skill_report_forms(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        r = res.post_method(url=f'{host}{skills_report_forms_api}', json=skills_report_forms,
                            cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证调度任务计接口请求成功')
    def test_dispatch_task_report_forms(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        tasks_report_forms_payload['flag'] = 1
        r = res.post_method(url=f'{host}{tasks_report_forms_api}', json=tasks_report_forms_payload,
                            cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证执行任务计接口请求成功')
    def test_execute_task_report_forms(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        tasks_report_forms_payload['flag'] = 2
        r = res.post_method(url=f'{host}{tasks_report_forms_api}', json=tasks_report_forms_payload,
                            cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')


if __name__ == '__main__':
    print('Python')
