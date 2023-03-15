"""
@Time ： 2023/2/10 18:21
@Auth ： Kevin-C
@File ：test_robot_list.py
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
import random

test_data_path = os.path.join(os.path.dirname(os.getcwd()), r'test_data/test_robot_list.yaml')
test_data = read_config(test_data_path)
res = RequestMethod
host = AutoRunBaseInfo().host

json_data = test_data['create_robot']
query_payload = test_data['query_payload']
skill_shop_payload = test_data['skill_shop_payload']
change_state_payload = test_data['change_robot_state']
delete_skill_payload = test_data['delete_skill_payload']

assertion = AssertMethod

create_robot_api = test_data['robot_list_request_body']['create_robot_api']
queryPersona_api = test_data['robot_list_request_body']['queryPersona_api']
queryDepart_api = test_data['robot_list_request_body']['queryDepart_api']
query_api = test_data['robot_list_request_body']['query_api']
change_state_api = test_data['robot_list_request_body']['change_state_api']
delete_robot_api = test_data['robot_list_request_body']['delete_robot_api']
skill_shop_api = test_data['robot_list_request_body']['skill_shop_api']
add_skill_api = test_data['robot_list_request_body']['add_skill_api']
delete_skill_api = test_data['robot_list_request_body']['delete_skill_api']


@allure.feature('FEATURE:【机器人列表】模块测试')
class TestRobotListApi:

    @allure.title('验证机器人创建成功-范围：公开')
    def test_create_robot_public(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        log.info(f'{AutoRunBaseInfo().host}{create_robot_api}')
        json_data['name'] = f'auto_test{random.randint(1000, 9999)}'
        r = res.post_method(url=f'{host}{create_robot_api}', json=json_data, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证机器人创建成功-范围：用户')
    def test_create_robot_user(self, get_cookie):
        cookie = get_cookie
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        log.info(f'{AutoRunBaseInfo().host}{create_robot_api}')
        person_data = res.post_method(url=f'{host}{queryPersona_api}', cookies=cookie)
        for _ in person_data.json()['data']['childrenList']:
            if _.get('userName'):
                if _['userName'] == 'cladmin':
                    json_data['list'].append({'scopeId': _['bid']})
                    json_data['useScopeType'] = 1
                    break
            else:
                pass
        json_data['name'] = f'auto_test{random.randint(1000, 9999)}'
        r = res.post_method(url=f'{host}{create_robot_api}', json=json_data, cookies=cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证机器人创建成功-范围：组织')
    def test_create_robot_organization(self, get_cookie):
        cookie = get_cookie
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        log.info(f'{AutoRunBaseInfo().host}{create_robot_api}')
        depart_data = res.post_method(url=f'{host}{queryDepart_api}', cookies=cookie)
        children_depart = depart_data.json()['data']['sysDepart']['childDepartList']
        if len(children_depart) > 0:
            json_data['list'].append({'scopeId': children_depart[0]['bid']})
            json_data['useScopeType'] = 2
        else:
            pass
        json_data['name'] = f'auto_test{random.randint(1000, 9999)}'
        r = res.post_method(url=f'{host}{create_robot_api}', json=json_data, cookies=cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证机器人列表查询接口请求成功')
    def test_query_all_data(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        r = res.post_method(url=f'{host}{query_api}', data=query_payload, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证修改状态接口请求成功')
    def test_change_robot_state(self, get_cookie):
        cookie = get_cookie
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        query_data = res.post_method(url=f'{host}{query_api}', data=query_payload, cookies=cookie)
        robot_bid = query_data.json()['data']['records'][0]['bid']
        robot_state = query_data.json()['data']['records'][0]['state']
        change_state_payload['bid'] = robot_bid
        change_state_payload['state'] = -1 if robot_state == 0 else 0
        r = res.post_method(url=f'{host}{change_state_api}', data=change_state_payload, cookies=cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证删除机器人接口请求成功')
    def test_delete_robot(self, get_cookie):
        cookie = get_cookie
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        query_data = res.post_method(url=f'{host}{query_api}', data=query_payload, cookies=cookie)
        robot_bid = query_data.json()['data']['records'][0]['bid']
        r = res.post_method(url=f'{host}{delete_robot_api}', json=[robot_bid], cookies=cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证机器人添加技能接口请求成功')
    def test_robot_add_skill(self, get_cookie):
        global skill_bid
        cookie = get_cookie
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        query_data = res.post_method(url=f'{host}{query_api}', data=query_payload, cookies=cookie)
        skill_shop_payload['robotId'] = query_data.json()['data']['records'][0]['bid']
        query_skill_shop = res.post_method(url=f'{host}{skill_shop_api}', data=skill_shop_payload, cookies=cookie)
        for _ in query_skill_shop.json()['data']:
            if _.get('selected') is False:
                skill_bid = _['bid']
                r = res.post_method(url=f'{host}{add_skill_api}{skill_shop_payload["robotId"]}', json=[skill_bid], cookies=cookie)
                assertion.assert_equal(r.json()['code'], 200)
                return
        log.info(f'测试完成！\n')

    @allure.title('验证机器人删除技能接口请求成功')
    def test_robot_delete_skill(self, get_cookie):
        cookie = get_cookie
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        query_data = res.post_method(url=f'{host}{query_api}', data=query_payload, cookies=cookie)
        delete_skill_payload['robotId'] = query_data.json()['data']['records'][0]['bid']
        query_skill_shop = res.post_method(url=f'{host}{skill_shop_api}', data=skill_shop_payload, cookies=cookie)
        for _ in query_skill_shop.json()['data']:
            if _.get('selected') is True:
                delete_skill_payload['serviceId'] = _['bid']
                r = res.post_method(url=f'{host}{delete_skill_api}',
                                    data=delete_skill_payload,
                                    cookies=cookie)
                assertion.assert_equal(r.json()['code'], 200)
                return
        pytest.skip('该机器人未添加技能')
        log.info(f'测试完成！\n')


if __name__ == '__main__':
    pytest.main(['-s', './test_robot_list.py::TestRobotListApi::test_delete_robot'])
    print('Python')
