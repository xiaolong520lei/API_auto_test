"""
@Time ： 2023/2/7 20:08
@Auth ： Kevin-C
@File ：sendEmail.py
@IDE ：PyCharm
"""

import yagmail
from common.readConfig import read_config

login_info = read_config()
email_host = login_info['email']['email_host']
account = login_info['email']['email_account']
password = login_info['email']['email_password']


def send_mail():
    try:
        yag = yagmail.SMTP(user=account, password=password, host=email_host)
        return yag
    except BaseException as e:
        print(e)


if __name__ == '__main__':
    f = send_mail()
    f.send(to='32223840@qq.com',subject='py_test', contents='test')


if __name__ == '__main__':
    print('Python')
