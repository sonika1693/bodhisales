from django.urls import path
from django.conf.urls import url
from . import views
app_name = 'tech'

urlpatterns = [
    path('profile/',views.Profile,name='Profile'),
    path('create_task/',views.CreateTask,name='CreateTask'),
    path('new_task/',views.NewTask,name='NewTask'),
    path('task_details/',views.TaskDetails,name='TaskDetails'),
    path('assigned_task/',views.AssignedTask,name='AssignedTask'),
    path('ongoing_task/',views.OngoingTask,name='OngoingTask'),
    path('completed_task/',views.CompletedTask,name='CompletedTask'),
    path('accepted_task/',views.AcceptedTask,name='AcceptedTask'),
    path('delete_developer_task/<int:id>/<int:task_id>',views.DeleteDeveloperTask,name='DeleteDeveloperTask'),
    path('delete_created_task/<int:id>',views.DeleteCreatedTask,name='DeleteCreatedTask'),
    path('edit_task/',views.EditTask,name='EditTask'),
    path('add_report/<int:task_id>',views.AddReport,name='AddReport'),
    path('developer_task/',views.DeveloperTask,name='DeveloperTask'),
    path('user_task_details/<int:id>',views.UserTaskDetails,name='UserTaskDetails')
]


