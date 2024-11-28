import json
import queue

from django.forms import model_to_dict
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import analyse
from analyse.bo import OperateItem
from analyse.models import OperateRecord
from analyse.service import analyseSpecificBond, addOperateRecord, analyseCostChangeOfSpecificBond



def test(request):
    return HttpResponse("分析模块连通性测试")


# 分析指定证劵的筹码水平
def analyseOperateItem(request):
    bondCode = request.GET.get("bondCode")
    # return HttpResponse(analyseSpecificBond(bondCode))
    result = analyseSpecificBond(bondCode)
    book_list = [
        {'id': 1, 'name': 'ptyhon'},
        {'id': 2, 'name': 'go'},
    ]
    return HttpResponse(json.dumps(book_list), content_type='application/json')




@csrf_exempt
def add(request):
    try:
        fild_obj = request.FILES.get("file")
        result = addOperateRecord(fild_obj)
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        return HttpResponse(json.dumps({"code":500,"msg":"导入错误"}, ensure_ascii=False))


def analyseCostChange(request):
    bondCode = request.GET.get("bondCode")
    result = analyseCostChangeOfSpecificBond(bondCode)
    book_list = [
        {'id': 1, 'name': 'ptyhon'},
        {'id': 2, 'name': 'go'},
    ]
    return HttpResponse(json.dumps(book_list), content_type='application/json')

def xirr_calculate(request):
    bondCode = request.GET.get("bondCode")
    result = analyse.service.xirr_calculate(bondCode)
    book_list = [
        {'id': 1, 'name': 'ptyhon'},
        {'id': 2, 'name': 'go'},
    ]
    return HttpResponse(json.dumps(book_list), content_type='application/json')


# 网格交易模拟
def moni(request):
    bondCode = request.GET.get("bondCode")
    result = analyse.service.grid_moni(bondCode)
    book_list = [
        {'id': 1, 'name': 'ptyhon'},
        {'id': 2, 'name': 'go'},
    ]
    return HttpResponse(json.dumps(book_list), content_type='application/json')

def newTableConnect(request):
    analyse.service.newTableConnect()
    book_list = [
        {'id': 1, 'name': 'ptyhon'},
        {'id': 2, 'name': 'go'},
    ]
    return HttpResponse(json.dumps(book_list), content_type='application/json')

def initializeOuterLeftMatch(request):
    bondCode = request.GET.get("bondCode")
    analyse.service.initialize_outer_left_match(bondCode)
    book_list = [
        {'id': 1, 'name': 'ptyhon'},
        {'id': 2, 'name': 'go'},
    ]
    return HttpResponse(json.dumps(book_list), content_type='application/json')

def outerAnalyse(request):
    bondCode = request.GET.get("bondCode")
    result = analyse.service.outer_analyse(bondCode)
    book_list = [
        {'id': 1, 'name': 'ptyhon'},
        {'id': 2, 'name': 'go'},
    ]
    return HttpResponse(json.dumps(book_list), content_type='application/json')

def renameFile(request):
    result = analyse.service.rename_file()
    book_list = [
        {'id': 1, 'name': 'ptyhon'},
        {'id': 2, 'name': 'go'},
    ]
    return HttpResponse(json.dumps(book_list), content_type='application/json')

def outerOcr(request):
    result = analyse.service.outer_ocr()
    book_list = [
        {'id': 1, 'name': 'ptyhon'},
        {'id': 2, 'name': 'go'},
    ]
    return HttpResponse(json.dumps(book_list), content_type='application/json')