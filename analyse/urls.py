from django.urls import path

from . import views

urlpatterns = [
    # 测试连通性
    path("test", views.test, name="test"),
    # 分析指定证劵的筹码水平
    path("specific", views.analyseOperateItem, name="analyse"),
    # 导入交易记录
    path("add", views.add, name="add"),
    # 分析持仓成本变化
    path("cost", views.analyseCostChange, name="costAnalyse"),
    # 分析XIRR
    path("xirr", views.xirr_calculate, name="xirrCalculate"),
    # 模拟网格交易
    path("moni", views.moni, name="moni"),
    # 测试新表连通性
    path("testAnalyse", views.newTableConnect, name="newTableConnect"),
    # 场外基金筹码水平分析
    path("outerAnalyse", views.outerAnalyse, name="outerAnalyse"),
    # 场外基金交易记录ocr识别并存储
    path("outerOcr", views.outerOcr, name="outerOcr"),
    # 文件重命名
    path("renameFile", views.renameFile, name="renameFile"),
    # 初始化待匹配记录
    path("initializeOuterLeftMatch", views.initializeOuterLeftMatch, name="initializeOuterLeftMatch"),
]