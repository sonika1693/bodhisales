from django.conf.urls import url
from django.urls import path
from sales.api import views


urlpatterns = [
    url(r'get_my_new_leads/$',views.GetMyNewLeads.as_view(),name='GetMyNewLeads'),
    url(r'get_my_datewise_leads/$',views.GetMyNewLeadsDateWise.as_view(),name='salesExecutiveGetDateWiseLeads'),
    url(r'give_feedback_lead/$',views.GiveLeadFeedBack.as_view(),name='giveLeadFeedBack'),
    url(r'find_type_feedback/$',views.FindTypeFeedBack.as_view(),name='findTypeFeedBack'),
    url(r'get_all_sales_people/$',views.GetAllSalesExecutives.as_view(),name='getAllSalesExecutive'),
    # url(r'get_leads_datewise/$',views.GetMyNewLeadsDateWise.as_view(),name='getMyNewLeadsDateWise'),
    url(r'get_my_worked_leads/$', views.GetWorkedLeadsApi.as_view(), name='get_my_all_leads'),
    url(r'get_feedback_demos_specificlead/$', views.GetFeedbackOrDemosSpecificLeadWiseApi.as_view(), name='GetFeedbackOrDemosSpecificLeadWiseApi'),
    url(r'give_demo_feedback/$', views.GiveDemoFeedBackApi.as_view(), name='give_demo_feedback'),
    url(r'get_my_assignedleads/$', views.GetMyAssignedLeadsAPI.as_view(), name='GetMyAssignedLeadsAPI'),
    url(r'get_specific_lead_andfeedback/$', views.GetSpecificLeadAndFeedbackAPI.as_view(), name='GetSpecificLeadAndFeedbackAPI'),
    url(r'send_message_to_user/$', views.SendMessageToUserAPI.as_view(), name='SendMessageToUserAPI'),
    url(r'get_feedbackes_listleadwise/$', views.GetFeedbackesLeadWiseUsingAjexAPI.as_view(), name='GetFeedbackesLeadWiseUsingAjexAPI'),
    url(r'get_my_all_message/$', views.MessagesInboxAPI.as_view(), name='MessagesInboxAPI'),
    url(r'get_specific_massages/$', views.GetMySpecificMessageAPI.as_view(), name='GetMySpecificMessageAPI'),
    url(r'specific_user_notifications/$', views.SpecificUserNotificationsAPI.as_view(), name='specific_user_notifications'),
    url(r'get_today_schedule/$', views.TodayScheduleReminderAPI.as_view(), name='TodayScheduleReminderAPI'),
    url(r'add_successfull_lead/$', views.AddSuccessfullyLeadsAPI.as_view(), name='add_successfull_lead'),
    url(r'get_my_successfully_leads/$', views.SpecificPersonSuccessfullyLeadsAPI.as_view(), name='get_my_successfully_leads'),
    url(r'apply_filter_search/$', views.ApplyFilterAndSeacrhAPI.as_view(), name='ApplyFilterAndSeacrhAPI'),
    url(r'applysorting/$', views.SortingApplyAPI.as_view(), name='SortingApplyAPI'),
    url(r'sales_user_profile/$', views.SalesUserProfileApi.as_view(), name='SalesUserProfileApi'),
    url(r'salesuser_changepassword/$', views.SalesUserChangePasswordApi.as_view(), name='SalesUserChangePasswordApi'),
    url(r'admin_filter_sort_leads/$', views.FilterAndSortForAdminApi.as_view(), name='filterAndSortForAdmin'),
    url(r'assign_lead_to_anotheruser/$', views.AssignLeadToAnotherUserApi.as_view(), name='AssignLeadToAnotherUserApi'),
    url(r'delete_lead/$', views.DeleteLeadByAdminApi.as_view(), name='DeleteLeadByAdminApi'),
    url(r'logout/$', views.LogoutUserApi.as_view(), name='logout'),

    url(r'get_worked_leads_fileterwise/$', views.UserGetWorkedLeadsFileterWiseAPI.as_view(), name='UserGetWorkedLeadsFileterWiseAPI'),
    url(r'get_my_today_assigned_leads/$', views.GetMyTodayAssignedLeadsAPI.as_view(), name='GetMyTodayAssignedLeadsAPI'),
    url(r'get_my_old_leads/$', views.GetMyOldLeadsAPI.as_view(), name='GetMyOldLeadsAPI'),
    url(r'get_old_leads_filterwise/$', views.GetOldLeadsFilter.as_view(), name='GetOldLeadsFilter'),

]
