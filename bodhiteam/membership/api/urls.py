from django.conf.urls import url
from django.urls import path
from membership.models import *
from membership.api import views



urlpatterns = [
    url(r'login/$',views.Login.as_view(),name='login'),
    url(r'register_upload_user/$',views.RegisterUploadUser.as_view(),name='RegisterUploadUser'),
    url(r'get_user_ip/$',views.GetUserIpAddress.as_view(),name='GetUserIpAddress'),

]
