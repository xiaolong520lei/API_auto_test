"""
@Time ： 2023/2/8 16:09
@Auth ： Kevin-C
@File ：md5_encode.py
@IDE ：PyCharm
"""
import hashlib


def pwd_md5_encode(pwd) -> str:
    md = hashlib.md5()
    md.update(pwd.encode('utf-8'))
    pwd = md.hexdigest()
    return pwd


if __name__ == '__main__':
    print(pwd_md5_encode('Aa13579.'))
