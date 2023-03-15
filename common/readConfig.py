"""
@Time ： 2023/2/7 20:08
@Auth ： Kevin-C
@File ：readConfig.py
@IDE ：PyCharm
"""
import json
import requests
import yaml
import os
from common.Log import log


config_file = os.path.join(os.path.dirname(os.getcwd()), r'config/config.yaml')
login_test_data = os.path.join(os.path.dirname(os.getcwd()), r'test_data/login_api_data.yaml')
test = os.path.join(os.path.dirname(os.getcwd()), r'test_data/test_login.yaml')


def read_config(file_path=config_file):
    try:
        log.info('正在读取配置文件中...')
        f = open(file=file_path, mode='r', encoding='utf-8')
        config_data = yaml.load(f, Loader=yaml.FullLoader)
        log.info('配置文件数据读取成功！')
        return config_data

    except FileNotFoundError as e:
        log.error('配置文件读取失败！', exc_info=True)
        print(e)


if __name__ == '__main__':
    t = read_config(test)
    print(t['test_payload']['right_account'][0][0])


