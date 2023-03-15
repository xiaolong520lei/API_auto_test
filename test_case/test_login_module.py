"""
@Time ： 2023/2/8 9:34
@Auth ： Kevin-C
@File ：test_login_module.py
@IDE ：PyCharm
"""
import os
from common.readConfig import read_config
from run_main.main import AutoRunBaseInfo
import pytest
import allure
from common.Log import log
from test_case.test_worktop import TestWorkTop


test_data_path = os.path.join(os.path.dirname(os.getcwd()), 'test_case')
# test_data = read_config(test_data_path)['right_account']


# @allure.suite('登录')
# @allure.feature('登录接口验证')
class TestLoginModel:

    # @allure.title('正确用户名密码验证')
    # @allure.description('sdfsdf')
    # @allure.testcase('https://www.baidu.com','sdfsdf')
    # @pytest.mark.dependency(depends=["test_login_wrong_username_password"])
    def test_login_right_username_password(self):
        TestWorkTop.test_01()
        log.info('test..1+1')
        assert 1 == 1



    # # @allure.title('错误用户名密码验证')
    # @pytest.mark.dependy(name='test_login_wrong_username_password')
    # def test_login_wrong_username_password(self):
    #     assert 3 == 3
#
#     @allure.title('验证无网络')
#     def test_login_no_network(self):
#         assert 'c' in 'abc'
#
#     @allure.title('验证正常参数化')
#     # @pytest.mark.parametrize('account,password', [('abc', '1234'), ('nzc', '23sd')])
#     @pytest.mark.parametrize('account,password', test_data)
#     def test_login_canshuhua(self, account, password):
#         assert account == 'abc'
#         assert password == '1234'
#
#     @allure.title('验证叠加相乘参数化')
#     @pytest.mark.parametrize('password', ['234234', 'sdfsdf', '2sdf'])
#     @pytest.mark.parametrize('account', ['admin', 'test'])
#     def test_login_canshuhua2(self, account, password):
#         """
#         result:
#         [nzc-23sd]
#         [admin-234234]
#         [admin-sdfsdf]
#         [admin-2sdf]
#         [test-234234]
#         [test-sdfsdf]
#         [test-2sdf]
#         """
#         print(f'{account}++{password}')
#         assert account == 'abc'
#         assert password == '1234'
#
#
# # 这里的scope支持function、class、module、session四种
# @pytest.fixture(scope='function')
# def test_login_canshuhua3():
#     assert 1 == 'dd'


if __name__ == '__main__':
    pytest.main(['-v','-s',r'C:\Users\Administrator\PycharmProjects\API_auto_test\test_case\test_login_module.py'])