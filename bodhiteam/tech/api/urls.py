from django.conf.urls import url
from tech.api import views

urlpatterns = [
    url(r'all_technology/$',views.AllTechnology.as_view(),name='AllTechnology'),
    url(r'tech_users/$',views.TechUsers.as_view(),name='TechUsers'),
    url(r'create_task/$',views.CreateTask.as_view(),name='CreateTask'),
    url(r'get_tasks/$',views.GetTasks.as_view(),name='GetTasks'),
    url(r'task_details/$',views.TaskDetails.as_view(),name='TaskDetails'),
    url(r'assign_task/$',views.AssignTask.as_view(),name='AssignTask'),
    url(r'project_status_list/$',views.ProjectStatusList.as_view(),name='ProjectStatusList'),
    url(r'update_project_status/$',views.UpdateProjectStatus.as_view(),name='UpdateProjectStatus'),
    url(r'user_task/$',views.UserTask.as_view(),name='UserTask'),
    url(r'user_status_list/$',views.UserStatusList.as_view(),name='UserStatusList'),
    url(r'update_user_status/$',views.UpdateUserStatus.as_view(),name='UpdateUserStatus'),
    url(r'user_task_report/$',views.UserTaskReport.as_view(),name='UserTaskReport'),
]