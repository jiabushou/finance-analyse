from datetime import date

from django.test import TestCase
from pyxirr import xirr

from analyse.models import OperateRecord
import numpy as np

from analyse.service import grid_moni


# Create your tests here.
class tests(TestCase):

    def test_for(self):
        # bondCode = "510300"
        # operateRecordList = OperateRecord.objects.filter(bond_code=bondCode).order_by('bargain_time')
        # print("f")

        dates = [date(2020, 1, 1), date(2021, 1, 1), date(2022, 1, 1)]
        amounts = [-1000, 1000, 1000]

        # feed columnar data
        c = xirr(dates, amounts)

        # feed tuples
        b = xirr(zip(dates, amounts))

        # feed DataFrame
        import pandas as pd
        a = xirr(pd.DataFrame({"dates": dates, "amounts": amounts}))
        print("d")

    def test_for2(self):
        grid_moni(510500)