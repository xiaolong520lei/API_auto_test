"""
@Time ： 2023/2/28 16:12
@Auth ： Kevin-C
@File ：test_settings_enterprise.py
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

test_data_path = os.path.join(os.path.dirname(os.getcwd()), r'test_data/test_settings_enterprise.yaml')
test_data = read_config(test_data_path)
res = RequestMethod
host = AutoRunBaseInfo().host
assertion = AssertMethod

update_data_payload = test_data['update_data_payload']

query_data_api = test_data['robot_list_request_body']['query_data_api']
update_data_api = test_data['robot_list_request_body']['update_data_api']


@allure.feature('FEATURE:【设置】【企业】模块测试')
class TestSettingsEnterprise:

    @allure.title('验证获取企业信息接口请求成功')
    def test_query_skill_rate(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        r = res.post_method(url=f'{host}{query_data_api}', cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')

    @allure.title('验证修改企业信息接口请求成功')
    def test_query_skill_rate(self, get_cookie):
        def_name = sys._getframe().f_code.co_name
        log.warning(f'开始测试：{def_name}')
        update_data_payload['updateTime'] = int(time.time())*1000
        update_data_payload['introduction'] = 'AUTO-TEST'
        r = res.post_method(url=f'{host}{update_data_api}', json=update_data_payload, cookies=get_cookie)
        assertion.assert_equal(r.json()['code'], 200)
        log.info(f'测试完成！\n')


if __name__ == '__main__':
    print('Python')
