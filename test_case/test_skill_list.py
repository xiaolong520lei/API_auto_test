"""
@Time ： 2023/2/23 10:15
@Auth ： Kevin-C
@File ：test_skill_list.py
@IDE ：PyCharm
"""
import json
import os
import random
import sys
import pytest
from requests_toolbelt import MultipartEncoder
from common.Assert import AssertMethod
from common.readConfig import read_config
from common.Request import RequestMethod
from run_main.main import AutoRunBaseInfo
import allure
from common.Log import log

test_data_path = os.path.join(os.path.dirname(os.getcwd()), r'test_data/test_skill_list.yaml')
test_data = read_config(test_data_path)
res = RequestMethod
host = AutoRunBaseInfo().host

create_skill_payload = test_data['create_skill_payload']
query_payload = test_data['query_payload']
change_state_payload = test_data['change_skill_state']
delete_skill_payload = test_data['delete_skill_payload']
component_sql_payload = test_data['component_sql_payload']
process_json = test_data['process_json']
assertion = AssertMethod

header = test_data['robot_list_request_body']['request_header']

query_list_api = test_data['robot_list_request_body']['query_api']
change_state_api = test_data['robot_list_request_body']['change_state_api']
create_skill_api = test_data['robot_list_request_body']['create_skill_api']
delete_skill_api = test_data['robot_list_request_body']['delete_skill_api']
component_api = test_data['robot_list_request_body']['component_api']
save_skill_api = test_data['robot_list_request_body']['save_skill_api']
query_skill_version_api = test_data['robot_list_request_body']['query_skill_version_api']
query_skill_version_handbook_api = test_data['robot_list_request_body']['query_skill_version_handbook_api']
skill_push_api = test_data['robot_list_request_body']['skill_push_api']


@allure.feature('FEATURE:【技能】模块测试')
class TestRobotDeviceListApi:

    @allure.title('验证查询接口请求成功')
    def test_query_data(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        r = res.post_method(url=f'{host}{query_list_api}', data=query_payload, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证创建技能接口请求成功')
    def test_create_skill(self, get_cookie):
        cookie = get_cookie
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        create_skill_payload['name'] = f'auto_test_skill{random.randint(1000, 9999)}'
        r = res.post_method(url=f'{host}{create_skill_api}', data=create_skill_payload, cookies=cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证修改状态接口请求成功')
    def test_change_skill_state(self, get_cookie):
        cookie = get_cookie
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        query_data = res.post_method(url=f'{host}{query_list_api}', data=query_payload, cookies=get_cookie)
        skill_bid = query_data.json()['data']['records'][0]['bid']
        skill_state = query_data.json()['data']['records'][0]['state']
        change_state_payload['skillId'] = skill_bid
        change_state_payload['state'] = 1 if skill_state == 0 or -1 else 0
        r = res.post_method(url=f'{host}{change_state_api}', data=change_state_payload, cookies=cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证WEB编辑器接口请求成功')
    @pytest.mark.parametrize('sql', component_sql_payload)
    def test_get_webedit_component(self, sql, get_cookie):
        cookie = get_cookie
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        r = res.post_method(url=f'{host}{component_api}', json={'sql': sql}, cookies=cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证WEB编辑器保存接口请求成功')
    def test_save_edit_skill(self, get_cookie):
        cookie = get_cookie
        def_name = sys._getframe().f_code.co_name
        query_data = res.post_method(url=f'{host}{query_list_api}', data=query_payload, cookies=get_cookie)
        skill_version_id = query_data.json()['data']['records'][0]['versionId']
        fields = {
            'versionId': (None, skill_version_id),
            'processJson': ('blob', json.dumps(process_json), 'application/octet-stream')
        }
        multipart_encode = MultipartEncoder(fields=fields)
        header['Content-Type'] = multipart_encode.content_type
        log.warning(f'开始测试：{def_name}')
        r = res.post_method(url=f'{host}{save_skill_api}',headers=header, data=multipart_encode, cookies=cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证WEB编辑器发布接口请求成功')
    def test_push_skill(self, get_cookie):
        cookie = get_cookie
        def_name = sys._getframe().f_code.co_name
        with allure.step('查询技能列表数据'):
            query_data = res.post_method(url=f'{host}{query_list_api}', data=query_payload, cookies=get_cookie)
            assertion.assert_equal(query_data.json()['code'], 200)
        skill_version_id = query_data.json()['data']['records'][0]['versionId']
        skill_bid = query_data.json()['data']['records'][0]['bid']
        skill_version_no = query_data.json()['data']['records'][0]['version']
        skill_name = query_data.json()['data']['records'][0]['name']
        with allure.step('查询技能数据'):
            query_skill_version_data = res.get_method(url=f'{host}{query_skill_version_api}{skill_bid}', cookies=get_cookie)
            assertion.assert_equal(query_skill_version_data.json()['code'], 200)
        with allure.step('查询技能版本数据'):
            query_skill_version_handbook_data = res.get_method(url=f'{host}{query_skill_version_handbook_api}{skill_version_id}', cookies=get_cookie)
            assertion.assert_equal(query_skill_version_handbook_data.json()['code'], 200)
        fields = {
            'zipFileName': (None,'V'+ str(float(skill_version_no)+0.1)),
            'processJson': ('blob', json.dumps(process_json), 'application/octet-stream'),
            'skillName': (None,skill_name),
            'skillClassifyCode': (None,'5'),
            'publishSysType': (None,'0'),
            'versionNum':(None,str(float(skill_version_no)+0.1)),
            'description': (None,'auto test'),
            'state': (None,'0'),
            'skillId': (None,str(skill_bid)),
            'handbookCoverImage': (None,''),
            'handbookTitle': (None,''),
            'handbookSimpleContent': (None,''),
            'handbookContent': (None,'')
        }
        multipart_encode = MultipartEncoder(fields=fields)
        header['Content-Type'] = multipart_encode.content_type
        log.warning(f'开始测试：{def_name}')
        with allure.step('测试发布'):
            r = res.post_method(url=f'{host}{skill_push_api}', headers=header, data=multipart_encode, cookies=cookie)
            assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证删除技能接口请求成功')
    def test_delete_skill(self, get_cookie):
        cookie = get_cookie
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        query_data = res.post_method(url=f'{host}{query_list_api}', data=query_payload, cookies=get_cookie)
        skill_bid = query_data.json()['data']['records'][0]['bid']
        delete_skill_payload['skillId'] = skill_bid
        r = res.post_method(url=f'{host}{delete_skill_api}', data=delete_skill_payload, cookies=cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')


if __name__ == '__main__':
    pytest.main(['-s', './test_skill_list.py'])
    print('Python')
