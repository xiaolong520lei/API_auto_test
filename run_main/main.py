import os
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
    pytest.main(['-vv', '-s', case_path, '--alluredir', allure_report_data_path])
    allure_report.generate_report()

