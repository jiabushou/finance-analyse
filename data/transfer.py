from unittest import TestCase

from data import datasource1


# 获取当前市场存在的所有ETF信息
def getAllETFBasicInfo():
    return

# 获取某个ETF的日线数据
def getAllDayDataOfSpecificETF(code):
    originalData = datasource1.getAllDayDataOfSpecificETF(code)
    print(originalData)
    return originalData

