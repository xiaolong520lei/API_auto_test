"""
@Time ： 2023/2/27 10:40
@Auth ： Kevin-C
@File ：test_dispatch_task_list.py
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

test_data_path = os.path.join(os.path.dirname(os.getcwd()), r'test_data/test_dispatch_task_list.yaml')
login_data_info_path = os.path.join(os.path.dirname(os.getcwd()), r'test_data/test_login.yaml')
test_data = read_config(test_data_path)
user_info_data = read_config(login_data_info_path)
res = RequestMethod
host = AutoRunBaseInfo().host
assertion = AssertMethod
login_info = os.path.join(os.path.dirname(os.getcwd()), r'test_data/test_login.yaml')

query_data_payload = test_data['query_data_payload']
skill_list_payload = test_data['skill_list_payload']
save_dispatch_strategy_payload = test_data['save_dispatch_strategy_payload']
save_dispatch_task_payload = test_data['save_dispatch_task_payload']
delete_dispatch_task_payload = test_data['delete_dispatch_task_payload']

query_dispatch_task_api = test_data['robot_list_request_body']['query_dispatch_task_api']
owner_list_api = test_data['robot_list_request_body']['owner_list_api']
owner_robot_list_api = test_data['robot_list_request_body']['owner_robot_list_api']
device_skill_list_api = test_data['robot_list_request_body']['device_skill_list_api']
skill_tree_robot_api = test_data['robot_list_request_body']['skill_tree_robot_api']
save_dispatch_strategy_api = test_data['robot_list_request_body']['save_dispatch_strategy_api']
save_dispatch_task_api = test_data['robot_list_request_body']['save_dispatch_stask_api']
query_project_list_api = test_data['robot_list_request_body']['query_project_list_api']
query_dispatch_task_info_api = test_data['robot_list_request_body']['query_dispatch_task_info_api']
query_dispatch_task_log_api = test_data['robot_list_request_body']['query_dispatch_task_log_api']
delete_dispatch_task_api = test_data['robot_list_request_body']['delete_dispatch_task_api']


@allure.feature('FEATURE:【调度任务列表】模块测试')
class TestDispatchTask:
    @allure.title('验证查询调度任务接口请求成功')
    def test_query_dispatch_task(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        r = res.post_method(url=f'{host}{query_dispatch_task_api}',json=query_data_payload, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证新建调度任务接口请求成功')
    def test_create_dispatch_task(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        with allure.step('查询项目数据'):
            project_data = res.post_method(url=f'{host}{query_project_list_api}', params={'type': 1}, cookies=get_cookie)
        with allure.step('查询用户数据'):
            owner_list_data = res.get_method(url=f'{host}{owner_list_api}', cookies=get_cookie)
        owner_list = owner_list_data.json()['data']
        user_id = [_['bid'] for _ in owner_list if _['userName'] == user_info_data['test_payload']['right_account'][0][0] ][0]
        with allure.step('查询机器人数据'):
            user_owner_robot_data = res.get_method(url=f'{host}{owner_robot_list_api}{user_id}', cookies=get_cookie)
        robot_id = user_owner_robot_data.json()['data'][0]['bid']
        skill_list_payload['robotId'] = robot_id
        skill_list_payload['userId'] = user_id
        with allure.step('查询设备数据'):
            device_skill_list_data = res.post_method(url=f'{host}{device_skill_list_api}', data=skill_list_payload, cookies=get_cookie)
        skill_bid = device_skill_list_data.json()['data']['skills'][0]['bid']
        device_bid = device_skill_list_data.json()['data']['devices'][0]['bid']
        skill_version = device_skill_list_data.json()['data']['skills'][0]['version']
        with allure.step('查询机器人技能数据'):
            skill_tree_robot_data = res.post_method(url=f'{host}{skill_tree_robot_api}', data={f'robotId': {robot_id}}, cookies=get_cookie)
        skill_version_id = skill_tree_robot_data.json()['data'][0]['skillVersionId']
        strategy_start_time = (datetime.datetime.now() + datetime.timedelta(days=15)).strftime('%Y-%m-%d %H:%M:%S')
        end_date = '2099-12-31'
        start_date = strategy_start_time.split(' ')[0]
        save_dispatch_strategy_payload['endTime'] = end_date
        save_dispatch_strategy_payload['startTime'] = start_date
        save_dispatch_strategy_payload['timePoint'] = strategy_start_time.split(' ')[1]
        save_dispatch_strategy_payload['planEndTime'] = end_date + ' ' + strategy_start_time.split(' ')[1]
        save_dispatch_strategy_payload['firstStartTime'] = strategy_start_time
        save_dispatch_strategy_payload['newPlanStartTime'] = strategy_start_time
        with allure.step('验证保存调度策略'):
            res.post_method(url=f'{host}{save_dispatch_strategy_api}', json=save_dispatch_strategy_payload, cookies=get_cookie)
        save_dispatch_task_payload['deviceId'] = device_bid
        save_dispatch_task_payload['msTimeDto'] = {'year': int(start_date.split('-')[0]), 'month': start_date.split('-')[1], 'day': int(start_date.split('-')[2])}
        save_dispatch_task_payload['name'] = f'autoTestDispatch{random.randint(1000, 9999)}'
        save_dispatch_task_payload['planStartTime'] = strategy_start_time
        save_dispatch_task_payload['projectId'] = project_data.json()['data'][0]['bid']
        save_dispatch_task_payload['robotId'] = robot_id
        save_dispatch_task_payload['robotOwnerBid'] = user_id
        save_dispatch_task_payload['skillId'] = skill_bid
        save_dispatch_task_payload['skillVersionId'] = skill_version_id
        save_dispatch_task_payload['strategy'] = save_dispatch_strategy_payload
        with allure.step('验证保存调度任务'):
            save_dispatch_data = res.post_method(url=f'{host}{save_dispatch_task_api}',
                                                 json=save_dispatch_task_payload, cookies=get_cookie)
        assertion.assert_equal(save_dispatch_data.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证调度任务详情接口请求成功')
    def test_dispatch_task_info(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        list_data = res.post_method(url=f'{host}{query_dispatch_task_api}', json=query_data_payload, cookies=get_cookie)
        task_bid = list_data.json()['data']['pagedItems'][0]['bid']
        r = res.post_method(url=f'{host}{query_dispatch_task_info_api}', json={'bid': task_bid}, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证调度任务轨迹接口请求成功')
    def test_dispatch_task_log(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        list_data = res.post_method(url=f'{host}{query_dispatch_task_api}', json=query_data_payload, cookies=get_cookie)
        task_bid = list_data.json()['data']['pagedItems'][0]['bid']
        r = res.get_method(url=f'{host}{query_dispatch_task_log_api}{task_bid}', params={'pageNo': 1}, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证删除调度任务接口请求成功')
    def test_delete_dispatch_task(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        list_data = res.post_method(url=f'{host}{query_dispatch_task_api}', json=query_data_payload, cookies=get_cookie)
        for _ in list_data.json()['data']['pagedItems']:
            if _['state'] == 4 or _['state'] == 3:
                delete_dispatch_task_payload['bid'] = _['bid']
                delete_dispatch_task_payload['deviceId'] = _['deviceId']
                delete_dispatch_task_payload['dispatchTaskId'] = _['bid']
                delete_dispatch_task_payload['id'] = _['id']
                delete_dispatch_task_payload['robotId'] = _['robotId']
                delete_dispatch_task_payload['taskName'] = _['taskName']
                break
        r = res.post_method(url=f'{host}{delete_dispatch_task_api}', json=delete_dispatch_task_payload, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')


if __name__ == '__main__':
    print('Python')
