"""
@Time ： 2023/2/8 9:33
@Auth ： Kevin-C
@File ：test_learn_info.py
@IDE ：PyCharm
"""
import os

import allure
import pytest
import requests

file_path = r'C:\Users\lei.chen10\Pictures\hongfa_big.jpg'

# ---------------------------allure--------------------------------


# @allure.title('这是用例标题')
# @allure.story('这是二级标题')
# @allure.step('这是测试步骤标题')
# @allure.description('这是描述信息')
# @allure.issue('https://www.baidu.com', name='点击跳转到问题')
# @allure.severity(allure.severity_level.BLOCKER)  #优先级
# @allure.link('https://www.sohu.com')
# @allure.suite('sdd')
# @allure.feature('哈哈')
# @allure.attach.file(file_path, name='附件名称', attachment_type=allure.attachment_type.JPG) # 附件，可选择文件类型
# @allure.tag
# @allure.testcase('http://www.ifeng.com', name='点击跳转到凤凰网')
#
# def test_xxx():
#     assert 'dfdfdf' == None
#
#
# # ----------------------pytest--------------------------------------
#
#
# if __name__ == '__main__':
#     pytest.main(['-vv', '-s'])


