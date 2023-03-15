"""
@Time ： 2023/2/7 20:07
@Auth ： Kevin-C
@File ：Request.py
@IDE ：PyCharm
"""
import os
from common.readConfig import read_config
import requests
from common.Log import log
import json
from run_main.main import AutoRunBaseInfo


class RequestMethod:
    @staticmethod
    def get_method(url, params=None, **kwargs):
        try:
            response = requests.get(url=url, params=params, **kwargs)
            log.info(f'GET请求接口：{url} 成功!')
            if params is None:
                pass
            else:
                log.info(f'GET请求参数为：{params}')
            log.info(f'GET接口返回数据为:{response.json()}')
        except Exception as e:
            log.error(f'GET请求接口：{url} 出错! {e}', exc_info=True)
        else:
            return response

    @staticmethod
    def post_method(url, data=None, json=None, **kwargs):
        try:
            response = requests.post(url=url, data=data, json=json, **kwargs)
            log.info(f'POST请求接口：{url} 成功!')
            if data is None:
                if json is None:
                    pass
                else:
                    log.info(f'POST请求参数为：{json}')
            else:
                log.info(f'POST请求参数为：{data}')
            log.info(f'POST接口返回数据为:{response.json()}')
        except Exception as e:
            log.error(f'Post请求接口：{url}出错! {e}', exc_info=True)
        else:
            return response

    def other_method(self, method, url, pamars=None, data=None, json=None, **kwargs):
        method = str(method).lower()
        try:
            if method == 'get':
                self.get_method(url=url, pamars=pamars, **kwargs)
            elif method == 'post':
                self.post_method(url=url, data=data, json=json, **kwargs)
            else:
                response = requests.request(method, url=url, params=pamars, data=data, json=json, **kwargs)
                log.info(f'{method}请求接口：{url} 成功!')
                if data is None:
                    if json is None:
                        if pamars is None:
                            pass
                        else:
                            log.info(f'{method.upper()}请求参数为：{pamars}')
                    else:
                        log.info(f'{method.upper()}请求参数为：{json}')
                else:
                    log.info(f'{method.upper()}请求参数为：{data}')
                log.info(f'{method.upper()}接口返回数据为:{response.json()}')
                return response
        except Exception as e:
            print(e)
            log.error(f'{method}请求接口：{url}出错! {e}', exc_info=True)


res = RequestMethod()
if __name__ == '__main__':
    f = res.get_method('https://mrpa-test.ai-rtc.com:8082/plat/api/project/listNoPage',params={'type':1})


