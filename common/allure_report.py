"""
@Time ： 2023/2/7 20:07
@Auth ： Kevin-C
@File ：allure_report.py
@IDE ：PyCharm
"""
import os
from common.Log import log

allure_bin_path = os.path.abspath(os.path.join(os.path.dirname(os.getcwd()), r'common/allure-2.19.0/bin'))
allure_report_data_path = os.path.join(os.path.dirname(os.getcwd()), r'report/report_data')
allure_report_path = os.path.join(os.path.dirname(os.getcwd()), r'report/report_html')


def generate_report():
    try:
        log.info('正在生成报告中...')
        os.chdir(allure_bin_path)
        log.info(f'生成报告的数据路径为：{allure_report_data_path}')
        os.system(f'allure generate --clean {allure_report_data_path} -o {allure_report_path}')
        log.info(f'生成报告html路径为：{allure_report_path}')
        log.info('报告生成成功！')
    except Exception as e:
        log.error('报告生成失败', exc_info=True)
        print(e)


if __name__ == '__main__':
    # print(allure_bin_path)
    print(allure_report_data_path)
    print(allure_report_path)
    # os.chdir(allure_bin_path)
