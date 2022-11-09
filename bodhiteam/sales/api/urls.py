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
    url(r'applyFilterAndSearch/$', views.ApplyFilterAndSeacrhAPI.as_view(), name='applyFilterAndSearch'),
    url(r'applysorting/$', views.SortingApplyAPI.as_view(), name='applysorting'),
    url(r'salesUserProfile/$', views.SalesUserProfileApi.as_view(), name='salesUserProfile'),
    url(r'salesUser_changePassword/$', views.SalesUserChangePasswordApi.as_view(), name='salesUser_changePassword'),
    url(r'filterAndSortForAdmin/$', views.FilterAndSortForAdminApi.as_view(), name='filterAndSortForAdmin'),
    url(r'assignLeadToAnotherUser/$', views.AssignLeadToAnotherUserApi.as_view(), name='assignLeadToAnotherUser'),
    url(r'deleteLead/$', views.DeleteLeadByAdminApi.as_view(), name='deleteLead'),

    url(r'logout/$', views.LogoutUserApi.as_view(), name='logout'),

    url(r'get_worked_leads_fileterwise/$', views.UserGetWorkedLeadsFileterWiseAPI.as_view(), name='UserGetWorkedLeadsFileterWiseAPI'),
    url(r'get_my_today_assigned_leads/$', views.GetMyTodayAssignedLeadsAPI.as_view(), name='GetMyTodayAssignedLeadsAPI'),
    url(r'get_my_old_leads/$', views.GetMyOldLeadsAPI.as_view(), name='GetMyOldLeadsAPI'),
    url(r'see_datewise_salesuser_details/$', views.SeeDatewiseSalesUserDetails.as_view(), name='see_datewise_salesuser_details'),
    url(r'admin_searching/$', views.AdminSearchingAPI.as_view(), name='admin_searching'),
    url(r'leaderboard_list/$', views.LeaderboardList.as_view(), name='leaderboard_list'),

    url(r'get_last_feedback_lead_wise/$', views.GetLastFeedbackLeadWiseApi.as_view(), name='get_last_feedback_lead_wise'),


]
