"""
@Time ： 2023/2/9 10:04
@Auth ： Kevin-C
@File ：Assert.py
@IDE ：PyCharm
"""
from common.Log import log


class AssertMethod:
    @staticmethod
    def assert_equal(value_1, value_2):
        try:
            assert value_1 == value_2
            log.info(f"断言成功----验证值为： {value_1}, 结果为：{value_2} ")
        except AssertionError:
            log.error(f"断言失败----验证值为： {value_1}, 结果为：{value_2} ", exc_info=True)
            raise

    @staticmethod
    def assert_in(value_1, value_2):
        try:
            assert value_1 in value_2
            log.info(f"断言成功----验证值为： {value_1}, 结果为：{value_2} ")
        except AssertionError:
            log.error(f"断言失败----验证值为： {value_1}, 结果为：{value_2} ", exc_info=True)
            raise

    @staticmethod
    def assert_greater_than(value_1, value2):
        try:
            assert value_1 > value2
            log.info(f"断言成功----验证值为： {value_1}, 结果为：{value2} ")
        except AssertionError:
            log.error(f"断言失败----验证值为： {value_1}, 结果为：{value2} ", exc_info=True)
            raise

    @staticmethod
    def assert_less_than(value_1, value2):
        try:
            assert value_1 < value2
            log.info(f"断言成功----验证值为： {value_1}, 结果为：{value2} ")
        except AssertionError:
            log.error(f"断言失败----验证值为： {value_1}, 结果为：{value2} ", exc_info=True)
            raise


def assert_less_than(value_1, value2):
    try:
        assert value_1 < value2
        log.info(f"断言成功----验证值为： {value_1}, 结果为：{value2} ")
    except AssertionError:
        log.error(f"验证失败, 验证值为： {value_1}, 结果为：{value2} ", exc_info=True)
        raise


if __name__ == '__main__':
    print('Python')
