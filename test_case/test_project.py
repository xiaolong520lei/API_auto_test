"""
@Time ： 2023/2/24 18:06
@Auth ： Kevin-C
@File ：test_project.py
@IDE ：PyCharm
"""
import datetime
import json
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
sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])
test_data_path = os.path.join(os.path.dirname(os.getcwd()), r'test_data/test_project.yaml')
test_data = read_config(test_data_path)
res = RequestMethod
host = AutoRunBaseInfo().host

query_data_payload = test_data['query_data_payload']
create_project_payload = test_data['create_project_payload']
update_project_payload = test_data['update_project_payload']
delete_project_payload = test_data['delete_project_payload']
assertion = AssertMethod

query_data_api = test_data['robot_list_request_body']['query_data_api']
create_project_api = test_data['robot_list_request_body']['create_project_api']
update_project_api = test_data['robot_list_request_body']['update_project_api']
delete_project_api = test_data['robot_list_request_body']['delete_project_api']


@allure.feature('FEATURE:【项目】模块测试')
class TestRobotDeviceListApi:

    @allure.title('验证查询接口请求成功')
    def test_query_data(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        r = res.post_method(url=f'{host}{query_data_api}', json=query_data_payload, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证创建项目接口请求成功')
    def test_create_project(self, get_cookie):
        cookie = get_cookie
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        get_start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        get_end_time = (datetime.datetime.now()+datetime.timedelta(days=10)).strftime('%Y-%m-%d %H:%M:%S')
        create_project_payload['projectName'] = f'auto_test_project{random.randint(1000, 9999)}'
        create_project_payload['planStartTime'] = get_start_time
        create_project_payload['planEndTime'] = get_end_time
        r = res.post_method(url=f'{host}{create_project_api}', json=create_project_payload, cookies=cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证修改项目接口请求成功')
    def test_update_project(self, get_cookie):
        cookie = get_cookie
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        get_start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        get_end_time = (datetime.datetime.now() + datetime.timedelta(days=15)).strftime('%Y-%m-%d %H:%M:%S')
        query_data = res.post_method(url=f'{host}{query_data_api}', json=query_data_payload, cookies=get_cookie)
        update_project_payload['projectName'] = f'auto_test_project{random.randint(1000, 9999)}'
        update_project_payload['bid'] = query_data.json()['data']['pagedItems'][0]['bid']
        update_project_payload['projectNum'] = query_data.json()['data']['pagedItems'][0]['projectNum']
        update_project_payload['planStartTime'] = get_start_time
        update_project_payload['planEndTime'] = get_end_time
        r = res.post_method(url=f'{host}{update_project_api}', json=update_project_payload, cookies=cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证删除项目接口请求成功')
    def test_delete_project(self, get_cookie):
        cookie = get_cookie
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        query_data = res.post_method(url=f'{host}{query_data_api}', json=query_data_payload, cookies=get_cookie)
        delete_project_payload['bid'] = query_data.json()['data']['pagedItems'][0]['bid']
        r = res.post_method(url=f'{host}{delete_project_api}', json=delete_project_payload, cookies=cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')


if __name__ == '__main__':
    # pytest.main(['-s', './test_project.py'])

    print('Python')
