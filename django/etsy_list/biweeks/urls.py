from django.urls import path
from biweeks.views import Allview

urlpatterns = [
    path("", Allview.as_view()),
]
