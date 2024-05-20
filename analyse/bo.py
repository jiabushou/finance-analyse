



# 交易记录
class OperateItem:
    def __init__(self, operateKind, operateTime, unitPrice, share, fee):
        self.operateKind = operateKind
        self.operateTime = operateTime
        self.unitPrice = unitPrice
        self.share = share
        self.fee = fee

# 筹码水平
class CostOfLevelInfo:
    def __init__(self, unitPrice, share):
        self.unitPrice = unitPrice
        self.share = share