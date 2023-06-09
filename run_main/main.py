import os
import sys
import shutil

object_path = os.path.abspath(os.path.join(os.getcwd(), '../'))
if object_path not in sys.path:
    sys.path.append(object_path)

import pytest
from common.readConfig import read_config
from common import allure_report



environment_info = read_config()['environment']
case_path = os.path.join(os.path.dirname(os.getcwd()), 'test_case')
allure_report_data_path = os.path.join(os.path.dirname(os.getcwd()), r'report/report_data')


class AutoRunBaseInfo:
    def __init__(self):
        self.host = environment_info['host']['test']

    def setup_class(self):
        self.host = environment_info['host']['test']
        print('SETUP,,,,,,,')


if __name__ == '__main__':
    # print(object_path)
    # pytest.main(['-vv', '-s', case_path, '--alluredir', allure_report_data_path]) #本地运行方式
    pytest.main(['-vv', '-s', case_path + '/test_login.py','--alluredir', allure_report_data_path, '--clean-alluredir']) #临时测试jenkins
    shutil.copy(object_path + '/temp/environment.properties', allure_report_data_path)
    # allure_report.generate_report() #生成allure报告

