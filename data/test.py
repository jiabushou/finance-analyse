import warnings
from collections import defaultdict
from unittest import TestCase

import calmap
import matplotlib.pyplot as plt
from urllib3.exceptions import InsecureRequestWarning

from analyse.models import OperateRecord
from data.datasource1 import getAllETFBasicInfo
from data.transfer import getAllDayDataOfSpecificETF
import numpy as np
import pandas as pd

class test(TestCase):
    # 测试获取ETF所有日线数据
    def test_for(self):
        # 510500
        originalData = getAllDayDataOfSpecificETF('512660')
        if originalData is None:
            return
        # 取出收盘价
        kanzhangtunmo_analyse = []
        close_prices = originalData.iloc[:,4]
        open_prices = originalData.iloc[:,3]
        fund_date = originalData.iloc[:,2]
        slopes = [0, 0, 0, 0]
        kanzhangtunmo = []
        invalid_count = 0
        after_day_consider = 10
        # 遍历这列数据，每5个数据点为一组
        for i in range(0, len(close_prices)):
            # 取出当前组的5个数据点
            y = close_prices[i:i + 5]
            # 如果不足5个点，则跳过
            if len(y) < 5:
                break
            # 生成对应的x值（0, 1, 2, 3, 4）
            x = np.arange(len(y))
            # 进行线性回归计算
            slope, intercept = np.polyfit(x, y, 1)
            # 将计算得到的斜率添加到列表中
            slopes.append(slope)
            # 取出第6个元素开盘价,收盘价  第5个元素开盘价,收盘价
            six_open_price = None
            six_close_price = None
            if i+5 <= len(open_prices) - 1:
                six_open_price = open_prices[i+5]
                six_close_price = close_prices[i+5]
            five_open_price = open_prices[i+4]
            five_close_price = close_prices[i+4]
            # 获取小于0的斜率
            if slope < 0:
                # 判断第6天数据是否存在
                if six_open_price is not None and six_close_price is not None:
                    if six_open_price < five_open_price and \
                            six_open_price < five_close_price and \
                            six_close_price > five_open_price and \
                            six_close_price > five_close_price:
                        kanzhangtunmo.append(fund_date[i+5])
                        # 从当前日期的下一个日期开始,如果10天内达到止损,则记录-1,如果未达到止损,记录最高值
                        # zhisun_price = six_open_price
                        zhisun_price = six_close_price
                        max_price = -1
                        if i+after_day_consider < len(close_prices):
                            consider_after_date_prices = close_prices[i+6:i+after_day_consider]
                            for temp in consider_after_date_prices:
                                if temp <= zhisun_price:
                                    kanzhangtunmo_analyse.append(-1)
                                    invalid_count += 1
                                    break
                                max_price = temp if temp > max_price else max_price
                            if len(kanzhangtunmo_analyse) != len(kanzhangtunmo):
                                kanzhangtunmo_analyse.append(max_price)
        mingzhong_percetage = (len(kanzhangtunmo)-invalid_count)/len(kanzhangtunmo)

        # kanzhangtunmo_by_years_defaultdict = defaultdict(list)
        # for temp in kanzhangtunmo:
        #     year = temp.split('-')[0]  # 从日期字符串中提取年份
        #     kanzhangtunmo_by_years_defaultdict[year].append(temp)
        # kanzhangtunmo_by_years_normaldict = dict(kanzhangtunmo_by_years_defaultdict)
        #
        # for year, dates in kanzhangtunmo_by_years_normaldict.items():
        #     # dates = ['2013-04-19', '2013-06-27', '2013-08-20', '2013-09-04', '2013-11-06', '2013-11-28', '2013-12-16']
        #     values = [1] * len(dates)  # 假设每个日期的数值为1
        #     # # 将日期字符串转换为pandas的DateTime对象
        #     dates = pd.to_datetime(dates)
        #     # # 创建一个pandas Series，索引为日期，值为对应的数值
        #     data = pd.Series(values, index=dates)
        #     # # 使用calmap绘制日历热图
        #     # plt.figure(figsize=(16, 10))
        #     calmap.calendarplot(data, cmap='YlGn', fillcolor='red', linewidth=0.5, fig_kws=dict(figsize=(16, 8)))
        #     plt.show()
        # print(slopes)

    # 测试获取所有ETF基础信息
    def test_for_etf_basic_info(self):
        dataa = getAllETFBasicInfo()
        print("finish")

    def test_all(self):
        warnings.filterwarnings("ignore", category=FutureWarning)
        warnings.filterwarnings("ignore", category=InsecureRequestWarning)
        all_etf = getAllETFBasicInfo()
        # 前63行是一些国外的ETF,不考虑
        etf_infos = all_etf.iloc[63:, [0, 1]]

        for index, row in etf_infos.iterrows():
            code = row[0]
            name = row[1]

            if code != '510300':
                continue

            originalData = getAllDayDataOfSpecificETF(code)
            if originalData is None:
                print(name, "无数据")
                continue
            # 取出收盘价
            kanzhangtunmo_analyse = []
            close_prices = originalData.iloc[:, 4]
            open_prices = originalData.iloc[:, 3]
            highest_prices = originalData.iloc[:,5]
            fund_date = originalData.iloc[:, 2]
            slopes = [0, 0, 0, 0]
            kanzhangtunmo = []
            kanzhangtunmo_first_below = []
            kanzhangtunmo_first_below_day = []
            kanzhangtunmo_zhisun_jia = []
            kanzhangtunmo_kuisun_jia = []
            kanzhangtunmo_zuihao_jia = []
            kanzhangtunmo_zuihao_jia_percentage = []
            invalid_count = 0
            after_day_consider = 10
            # 遍历这列数据，每5个数据点为一组
            for i in range(0, len(close_prices)):
                # 取出当前组的5个数据点
                y = close_prices[i:i + 5]
                # 如果不足5个点，则跳过
                if len(y) < 5:
                    break
                # 生成对应的x值（0, 1, 2, 3, 4）
                x = np.arange(len(y))
                # 进行线性回归计算
                slope, intercept = np.polyfit(x, y, 1)
                # 将计算得到的斜率添加到列表中
                slopes.append(slope)
                # 取出第6个元素开盘价,收盘价  第5个元素开盘价,收盘价
                six_open_price = None
                six_close_price = None
                if i + 5 <= len(open_prices) - 1:
                    six_open_price = open_prices[i + 5]
                    six_close_price = close_prices[i + 5]
                five_open_price = open_prices[i + 4]
                five_close_price = close_prices[i + 4]
                # 触发信号
                if slope < 0:
                    # 判断第6天数据是否存在
                    if six_open_price is not None and six_close_price is not None:
                        if six_open_price < five_open_price and \
                                six_open_price < five_close_price and \
                                six_close_price > five_open_price and \
                                six_close_price > five_close_price:
                            kanzhangtunmo.append(fund_date[i + 5])
                            zhisun_price = six_open_price
                            kanzhangtunmo_zhisun_jia.append(zhisun_price)
                            max_price_but_higher_than_zhisun_price = zhisun_price

                            # 从当前日期的下一个日期开始,取出首次收盘价低于止损线的价格,计算该收盘价相比于止损线的亏损率
                            # 取出最高价
                            for index, temp in enumerate(close_prices[i+6:], start=i+6):
                                if highest_prices[index] > max_price_but_higher_than_zhisun_price:
                                    max_price_but_higher_than_zhisun_price = highest_prices[index]
                                if temp < zhisun_price:
                                    kanzhangtunmo_first_below.append(round((zhisun_price-temp)/zhisun_price, 4))
                                    kanzhangtunmo_first_below_day.append(index - i - 5)
                                    kanzhangtunmo_kuisun_jia.append(temp)
                                    kanzhangtunmo_zuihao_jia.append(max_price_but_higher_than_zhisun_price)
                                    kanzhangtunmo_zuihao_jia_percentage.append(round((max_price_but_higher_than_zhisun_price-zhisun_price)/zhisun_price, 4))
                                    break
                            if len(kanzhangtunmo) != len(kanzhangtunmo_first_below):
                                kanzhangtunmo_first_below.append("not below")
                                kanzhangtunmo_first_below_day.append("not below")
                                kanzhangtunmo_kuisun_jia.append("not below")
                                kanzhangtunmo_zuihao_jia.append(max_price_but_higher_than_zhisun_price)
                                kanzhangtunmo_zuihao_jia_percentage.append(round((max_price_but_higher_than_zhisun_price - zhisun_price) / zhisun_price, 4))

                            # 从当前日期的下一个日期开始,如果10天内达到止损,则记录-1,如果未达到止损,记录最高值
                            # max_price = -1
                            # if i + after_day_consider < len(close_prices):
                            #     consider_after_date_prices = close_prices[i + 6:i + after_day_consider]
                            #     for temp in consider_after_date_prices:
                            #         if temp <= zhisun_price:
                            #             kanzhangtunmo_analyse.append(-1)
                            #             invalid_count += 1
                            #             break
                            #         max_price = temp if temp > max_price else max_price
                            #     if len(kanzhangtunmo_analyse) != len(kanzhangtunmo):
                            #         kanzhangtunmo_analyse.append(max_price)
            # if len(kanzhangtunmo) != 0:
            #     mingzhong_percetage = round((len(kanzhangtunmo) - invalid_count) / len(kanzhangtunmo), 2)
            # else:
            #     mingzhong_percetage = 0

            # print(name, mingzhong_percetage, len(kanzhangtunmo) - invalid_count, len(kanzhangtunmo))
            plt.hist(kanzhangtunmo_zuihao_jia_percentage, bins=130, alpha=0.7, rwidth=0.85)
            plt.show()
            print(name)
        print("finish")


    def test_for(self):
        bondCode = "510300"
        operateRecordList = OperateRecord.objects.filter(bond_code=bondCode).order_by('bargain_time')
        print("f")