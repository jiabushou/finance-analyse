import efinance as ef

def getAllDayDataOfSpecificETF(code):
    return ef.stock.get_quote_history(code)