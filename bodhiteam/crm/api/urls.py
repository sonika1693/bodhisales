from django.urls import path
from . import views

urlpatterns = [
    path('institute/create/', views.CreateInstitute.as_view(),
         name='create-institute'),
    path('institute/status/', views.InstituteStatusAPI.as_view(),
         name='status-of-institute'),
    path('institute/requirements/create/', views.CreateInstituteRequirementsAPI.as_view(),
         name='institute-requirements-create'),
    path('institute/requirements/status/', views.InstituteRequirementsStatusAPI.as_view(),
         name='institute-requirements-status'),
    path('institute/convert_by/list/', views.GetInstituteDetailAPI.as_view(),
         name='converted_by_list'),
    path('institute/get/', views.GetInstituteDetailAPI.as_view(),
         name='get-institute'),
    path('institute/get/all/', views.GetInstituteAPI.as_view(),
         name='get-all-institute'),
    path('institute/update/', views.UpdateInstitute.as_view(),
         name='update-institute'),
    path('institute/requirements/update/', views.UpdateInstituteRequirementsAPI.as_view(),
         name='institute-requirements-update'),

]
