"""
@Time ： 2023/2/28 17:13
@Auth ： Kevin-C
@File ：test_settings_department.py
@IDE ：PyCharm
"""
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
import time

test_data_path = os.path.join(os.path.dirname(os.getcwd()), r'test_data/test_settings_department.yaml')
test_data = read_config(test_data_path)
res = RequestMethod
host = AutoRunBaseInfo().host
assertion = AssertMethod

add_depart_payload = test_data['add_depart_payload']
up_down_payload = test_data['up_down_payload']

department_tree_api = test_data['robot_list_request_body']['department_tree_api']
up_down_depart_api = test_data['robot_list_request_body']['up_down_depart_api']
add_depart_api = test_data['robot_list_request_body']['add_depart_api']
delete_depart_api = test_data['robot_list_request_body']['delete_depart_api']


@allure.feature('FEATURE:【设置】【部门】模块测试')
class TestSettingsEnterprise:

    @allure.title('验证获取部门信息接口请求成功')
    def test_query_skill_rate(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        r = res.post_method(url=f'{host}{department_tree_api}', cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证上移下移接口请求成功')
    def test_up_down(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        department_data = res.post_method(url=f'{host}{department_tree_api}', cookies=get_cookie)
        up_down_payload['departId'] = department_data.json()['data'][0]['childDepartList'][0]['bid']
        with allure.step('向上移动'):
            up_down_payload['action'] = 'up'
            r = res.post_method(url=f'{host}{up_down_depart_api}', data=up_down_payload, cookies=get_cookie)
            assertion.assert_equal(r.json()['code'], 200)
        with allure.step('向下移动'):
            up_down_payload['action'] = 'down'
            r = res.post_method(url=f'{host}{up_down_depart_api}', data=up_down_payload, cookies=get_cookie)
            assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证添加部门接口请求成功')
    def test_add_department(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        department_data = res.post_method(url=f'{host}{department_tree_api}', cookies=get_cookie)
        add_depart_payload['parentId'] = department_data.json()['data'][0]['childDepartList'][0]['bid']
        add_depart_payload['departName'] = f'auto_test_department{random.randint(1000, 9999)}'
        r = res.post_method(url=f'{host}{add_depart_api}', json=add_depart_payload, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证删除部门接口请求成功')
    def test_delete_department(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        department_data = res.post_method(url=f'{host}{department_tree_api}', cookies=get_cookie)
        depart_bid = [i['bid'] for i in department_data.json()['data'][0]['childDepartList'][0]['childDepartList'] if 'auto_test' in i['departName']]
        r = res.post_method(url=f'{host}{delete_depart_api}', data={'departId': depart_bid[0]}, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')


if __name__ == '__main__':
    print('Python')
