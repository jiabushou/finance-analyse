from unittest import TestCase

from data.transfer import getAllDayDataOfSpecificETF


class test(TestCase):
    # 测试获取ETF所有日线数据
    def test_for(self):
        getAllDayDataOfSpecificETF('510500')