from django.urls import path,re_path
from django.conf import settings
from servers import views


urlpatterns = [
        path(r'index',views.index,name="index"),
]


