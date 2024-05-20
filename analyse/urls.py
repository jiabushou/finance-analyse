from django.urls import path

from . import views

urlpatterns = [
    path("test", views.test, name="test"),
    path("specific", views.analyseOperateItem, name="analyse"),
    path("add", views.add, name="add")
]