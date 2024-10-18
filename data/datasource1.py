import adata
import efinance as ef
from adata import fund


def getAllDayDataOfSpecificETF(code):
    return ef.stock.get_quote_history(code)

def getAllETFBasicInfo():
    # adata.proxy(is_proxy=True, ip='60.167.21.27:1133')
    res_df = fund.info.all_etf_exchange_traded_info()
    # print(res_df)
    return res_df