"""
@Time ： 2023/2/7 21:07
@Auth ： Kevin-C
@File ：Log.py
@IDE ：PyCharm
"""

import logging
import os
import colorlog
from logging.handlers import RotatingFileHandler
from datetime import datetime

'''
使用方法：
1：其他文件输出日志时如需要带执行文件名则直接from common.Log import log即可，但error中默认不带Trackback 详细信息,如需Trackback 信息在
   调用error方法时加入exc_info=True 即可
2：如果需要默认输入error Trackback信息则直接 from common.Log import my_handler as log 即可,但执行路径默认为Log.py，如需对各infor、
    error等方法定制可在HandleLog类最下方进行开发
'''

# 当前日期,用于创建每日文件夹和日志文件
now_date = datetime.now().strftime('%Y-%m-%d')


# 配置日志文件名称及路径，如果不存在则自动创建
def log_save_path():
    """
    :return: log_path 输入日志的存储路径，以当前日期做为文件夹
    """
    cur_path = os.path.dirname(os.getcwd())  # 当前项目路径
    log_path = os.path.join(cur_path, 'logs/' + now_date)  # log_path为存放日志的路径
    os.makedirs(log_path, exist_ok=True)  # 判断如果路径不存在则创建
    return log_path


log_colors_config = {
    # 终端输出日志颜色配置
    'DEBUG': 'white',
    'INFO': 'cyan',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

default_formats = {
    # 终端输出格式
    'color_format': '%(log_color)s[%(asctime)s]-[%(name)s]-[%(filename)s]-[line:%(lineno)d]-%(levelname)s: %(message)s',
    # 日志输出格式
    'log_format': '[%(asctime)s]-[%(filename)s]-[line:%(lineno)d]-%(levelname)s: %(message)s'
}


# logger是创建日志记录器，同时设置日志记录器输出级别
logger = logging.getLogger(os.path.split(__file__)[-1].split(".")[0])
logger.setLevel(logging.DEBUG)


class HandleLog:

    def __init__(self):
        """
        初始化创建日志记录器和文件保存路径、记录器日志输出级别
        cur_file 为传入的文件名称，用于打印日志格式中的 %(name)s的名称
        log_path 为保存文件的路径
        info_log_path和error_log_path 为存储日志文件的绝对文件路径和日志名称
        """
        self.cur_file = os.path.split(__file__)[-1].split(".")[0]
        self.log_path = log_save_path()
        self.info_log_path = os.path.join(self.log_path, now_date + "-INFO" + ".log")
        self.error_log_path = os.path.join(self.log_path, now_date + "-ERROR" + ".log")

    def init_all_handles(self):
        """
        console_stream_handler 设置控制台日志输入流
        info_file_handler 设置info日志文件回滚处理器用于存储文件，maxBytes参数可设置文件大小，backupCount为设置的输出日志数量
        error_file_handler 设置info日志文件回滚处理器用于存储文件，maxBytes参数可设置文件大小，backupCount为设置的输出日志数量
        """
        logger.handlers.clear()
        console_stream_handler = colorlog.StreamHandler()
        info_file_handler = RotatingFileHandler(filename=self.info_log_path, maxBytes=1 * 1024 * 1024, backupCount=5,
                                                encoding='utf-8')
        error_file_handler = RotatingFileHandler(filename=self.error_log_path, maxBytes=1 * 1024 * 1024, backupCount=5,
                                                 encoding='utf-8')
        return console_stream_handler, info_file_handler, error_file_handler

    @staticmethod
    def init_all_format():
        """
        定义控制台和日志存储的格式
        :return:
        """
        console_format = colorlog.ColoredFormatter(default_formats['color_format'], log_colors=log_colors_config)
        log_format = logging.Formatter(default_formats['log_format'])
        return console_format, log_format

    @staticmethod
    def set_all_handles(console_stream_handler, info_file_handler, error_file_handler):
        """
        将logger添加到控制台处理器和info，error处理器中
        :param console_stream_handler:控制台处理器
        :param info_file_handler:info日志处理器
        :param error_file_handler:error日志处理
        :return:
        """
        console_stream_handler.setLevel(logging.DEBUG)
        info_file_handler.setLevel(logging.DEBUG)
        error_file_handler.setLevel(logging.ERROR)
        logger.addHandler(console_stream_handler)
        logger.addHandler(info_file_handler)
        logger.addHandler(error_file_handler)

    def set_all_format(self, console_stream_handler, info_file_handler, error_file_handler):
        """
        设置控制台处理和info,error处理器日志格式
        :param console_stream_handler:
        :param info_file_handler:
        :param error_file_handler:
        :return:
        """
        console_format, log_format = self.init_all_format()
        console_stream_handler.setFormatter(console_format)
        info_file_handler.setFormatter(log_format)
        error_file_handler.setFormatter(log_format)

    @staticmethod
    def remove_handles(console_stream_handler, info_file_handler, error_file_handler):
        """
        移除处理器
        :param console_stream_handler:
        :param info_file_handler:
        :param error_file_handler:
        :return:
        """
        logger.removeHandler(console_stream_handler)
        logger.removeHandler(info_file_handler)
        logger.removeHandler(error_file_handler)

    @staticmethod
    def close_handles(info_file_handler, error_file_handler):
        """
        关闭处理器
        :param info_file_handler:
        :param error_file_handler:
        :return:
        """
        info_file_handler.close()
        error_file_handler.close()

    def pack_log(self):
        """
        封装控制器，用于在其他文个中引用
        :return:
        """
        console_stream_handler, info_file_handler, error_file_handler = self.init_all_handles()
        self.set_all_format(console_stream_handler, info_file_handler, error_file_handler)
        self.set_all_handles(console_stream_handler, info_file_handler, error_file_handler)
        self.close_handles(info_file_handler, error_file_handler)
        return logger

    # -------如下可用于自定义log的内容-------------------------------------------------------------
    @staticmethod
    def info(msg):
        logger.info(msg)

    @staticmethod
    def error(msg):
        logger.error(msg, exc_info=True)

    @staticmethod
    def warning(msg):
        logger.warning(msg)

    @staticmethod
    def debug(msg):
        logger.debug(msg)

    @staticmethod
    def critical(msg):
        logger.critical(msg)


# -----带执行文件，直接引用log------
my_handler = HandleLog()
log = my_handler.pack_log()

if __name__ == '__main__':
    loger = HandleLog()
    # logger = log.log()
    # logger.info('test info')
    # logger.debug('test debug')
    # logger.critical('test critical')
    # logger.error('test error',exc_info=True)
    # logger.warning('test warning')
    loger.info('sdfsdf')
    loger.error('sdfsd')
    print(os.path.dirname(os.getcwd()))