from itertools import chain
from rest_framework.views import APIView
from django.contrib.auth.models import User,Group
from rest_framework.response import Response
from sales.models import *
from membership.models import *
from tech.models import *
import datetime
from django.db.models import Prefetch
from .serializers import *
from django.db.models import Q
from django.utils import timezone 


class GetMyNewLeads(APIView):
    def get(self,request):
        leads = Lead.objects.filter(assignedTo=self.request.user.salesexecutive,lead_status='is_successfull_lead').order_by('-date')
        serializer = LeadSerializer(leads,many=True)
        return Response({'Leads':serializer.data})

# class GetMyNewLeadsDateWise(APIView):
#     def post(self,request,*args,**kwargs):
#         my_profile = self.request.user.salesexecutive
#         data = request.data
#         date= data['date']
#         date = str(date.split('.')[0])
#         date = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
#         main_date = date.date()
#         leads = Lead.objects.filter(assignedTo = my_profile,date__date=main_date).order_by('-date')
#         leads_list = []
#         for lead in leads:
#             lead_dict =\
#             {'name':lead.personName,'instituteName':lead.instituteName,'contactPhone':lead.contactPhone,'email':lead.email,'numberStudents':lead.numberStudents,'location':lead.location,'notes':lead.notes,'source':lead.source,'assignedTo':lead.assignedTo.name}
#             leads_list.append(lead_dict)
#         context = {'leads':leads_list,'date':str(main_date)}
#         return Response(context)

class GetMyNewLeadsDateWise(APIView):
    def post(self,request,*args,**kwargs):
        my_profile = self.request.user.salesexecutive
        data = request.data
        date = data['date']
        date_wise_leads = Lead.objects.filter(assignedTo=my_profile,date__date=date,lead_status='is_successfull_lead').order_by('-id')
        leadsSerializer = LeadSerializer(date_wise_leads,many=True)
        context = {'leads':leadsSerializer.data}
        return Response(context)


class GiveLeadFeedBack(APIView):
    def post(self,request,*args,**kwargs):
        my_profile = self.request.user.salesexecutive
        data = request.data
        lead_id = data['lead_id']
        demo = data['demo']
        executiveId = data['nextCall']
        furtherCall = data['furtherCall']
        nextCallDate = data['nextCallDate']
        demoDate = data['demoDate']

        try:
            numberStudents = data['numberStudents']
        except:
            numberStudents = None
        try:
            freeTime = data['freeTime']
        except:
            freeTime = None

        try:
            try:
                nextCallDate = nextCallDate.strip('"') 
                nextCallDate = datetime.datetime.strptime(nextCallDate,'%Y-%m-%d %H:%M')
            except:
                nextCallDate = None        
            try:
                demoDate = demoDate.strip('"') 
                demoDate = datetime.datetime.strptime(demoDate,'%Y-%m-%d %H:%M')
            except:
                demoDate = None

            try:
                lead = Lead.objects.get(id=lead_id)
            except Lead.DoesNotExist:
                return Response('Incorrect lead id')
            
            feedback = FeedBack(by=my_profile,typeFeedBack=FeedBack.objects.filter(lead=lead_id).count()+1,lead=lead,rating = data['rating'],notes = data['notes'],
                                Cource=data['cource'],instituteType=data['instituteType'],State=data['State'],city=data['city'],
                                callrecording=data['audioUrl'],feedback=data['feedback'],priceQuoted=data['priceQuoted'],numberStudents=numberStudents,freeTime=freeTime)

            if data['Is_wrongLead'] == 'false':
                feedback.Is_wrongLead = False
            else:
                feedback.Is_wrongLead = True
                
            if furtherCall == 'true':
                feedback.furtherCall = True
            else:
                feedback.furtherCall = False

            
            if executiveId == 'None':
                feedback.nextCall = None
            else:
                NextCallerUser = SalesExecutive.objects.get(id=executiveId)
                feedback.nextCall = NextCallerUser
                DemoFeedback_And_LeadFeedback_Notifications.objects.create(notification_user=NextCallerUser,
                sender_user=my_profile,notification_type='LeadFeedbackNotification',lead=lead,
                massage = f"Today is your Feedback schedule of this {lead.personName} lead So remember This", is_FirstTime=True ,nextDate=nextCallDate,datetime=datetime.datetime.now())
            
            if demo == 'true':
                feedback.demo = True
                DemoFeedback_And_LeadFeedback_Notifications.objects.create(notification_user=my_profile,
                sender_user=my_profile,notification_type='DemoNotification',lead=lead,
                massage = f"Today is your demo schedule of this {lead.personName} lead So remember This", is_FirstTime=True ,nextDate=demoDate,datetime=datetime.datetime.now())
            else:
                feedback.demo = False

            feedback.demoDate = demoDate        
            feedback.nextCallDate = nextCallDate
            feedback.save()
            lead.lead_status = 'worked_lead'
            lead.save()
            context = {'status':'Saved','message':'Feedback saved'}
        except Exception as e:
            context = {'status':'Failed','message':str(e)}
        return Response(context)

class FindTypeFeedBack(APIView):
    def post(self,request,*args,**kwargs):
        my_profile = self.request.user.salesexecutive
        data = request.data
        lead_id = data['lead_id']
        lead = Lead.objects.get(id=lead_id)
        feedback = FeedBack.objects.filter(lead=lead)
        feedback_length = len(feedback)
        typeFeedBack = feedback_length + 1
        context = {'typeFeedback':typeFeedBack}
        return Response(context)

class GetAllSalesExecutives(APIView):
    def get(self,request):
        sales_people = SalesExecutive.objects.all()
        sales_list = []
        for sp in sales_people:
            sp_dict = {'id':sp.id,'name':sp.name}
            sales_list.append(sp_dict)
        context = {'salesPeople':sales_list}
        return Response(context)

class GetWorkedLeadsApi(APIView):
    def get(self,request):
        leads = Lead.objects.filter(assignedTo=self.request.user.salesexecutive,lead_status='worked_lead').order_by('-date')
        serializer = LeadSerializer(leads,many=True)
        return Response({'Leads':serializer.data})

class GetFeedbackOrDemosSpecificLeadWiseApi(APIView):
    def post(self,request,*args,**kwargs):
        lead_id = request.data['lead_id']
        feedbackes = FeedBack.objects.filter(lead=lead_id)
        demos = DemoFeedback.objects.filter(lead=lead_id)
        feedbackserializer = FeedBackSerializer(feedbackes,many=True)
        demosserializer = DemoFeedbackSerializer(demos,many=True)
        context = {'feedbacks': feedbackserializer.data,'demosfeedbackes':demosserializer.data}
        return Response(context)

class GiveDemoFeedBackApi(APIView):
    def post(self,request):
        data = request.data
        lead_id = data['lead_id']
        my_profile = self.request.user.salesexecutive
        lead = Lead.objects.get(id=lead_id)
        DemoNextUser = data['demo_nextCall']
        DemoNextDate = data['demo_nextCallDate']
        try:
            demofeedback = DemoFeedback(typedemo=DemoFeedback.objects.filter(lead=lead_id).count()+1, by=my_profile, lead=lead,
            datetime=datetime.datetime.now(),
            demo_rating=data['demo_rating'],
            extra_notes=data['extra_notes'],
            demo_feedback=data['demo_feedback'],
            price_quoted=data['price_quoted'],
            callrecording=data['audioUrl'])
            if not DemoNextDate:
                demofeedback.demo_nextCallDate = None
                DemoNextDate = None
            else:
                demofeedback.demo_nextCallDate = DemoNextDate
            if not DemoNextUser:
                demofeedback.demo_nextCall = None
            else:
                nextcaller = SalesExecutive.objects.get(id=DemoNextUser)
                demofeedback.demo_nextCall = nextcaller
                DemoFeedback_And_LeadFeedback_Notifications.objects.create(notification_user=nextcaller,sender_user=my_profile,notification_type='DemoNotification',lead=lead,
                massage = f"Today is your Demo schedule of this {lead.personName} lead So remember This",is_FirstTime = True,nextDate=DemoNextDate,datetime=datetime.datetime.now())
            demofeedback.save()
            context = {'status':'Saved','message':'Demo saved'}
        except Exception as e:
            context = {'status':'Failed','message':str(e)}
        return Response(context)

class GetMyAssignedLeadsAPI(APIView):
    def get(self,request):
        assignedLeadss = Lead.objects.filter(Q(Q(Q(feeback_lead__nextCall=request.user.salesexecutive) | Q(demo_lead__demo_nextCall=request.user.salesexecutive)) & Q(Q(lead_status='worked_lead') | Q(lead_status='is_successfull_lead'))) & ~Q(Q(feeback_lead__by=request.user.salesexecutive) | Q(demo_lead__by=request.user.salesexecutive))).order_by('-feeback_lead__time')
        serializer = LeadSerializer(assignedLeadss,many=True)
        return Response(serializer.data)    
        
class GetSpecificLeadAndFeedbackAPI(APIView):
    def post(self,request):
        feedback_id = request.data['feedback_id']
        if feedback_id == 'None':
            feedback_id = None
        specific_lead= Lead.objects.get(id=request.data['lead_id'])
        leadserializer = LeadSerializer(specific_lead)
        try:
            specific_feedback = FeedBack.objects.get(id=feedback_id)
            feedbackserializer =  FeedBackSerializer(specific_feedback)
            context = {'lead':leadserializer.data,'feedback':feedbackserializer.data}
            return Response(context)
        except FeedBack.DoesNotExist:
            return Response({'lead':leadserializer.data})
        
class SendMessageToUserAPI(APIView):
    def get(self,request):
        leads = None
        users = SalesExecutive.objects.prefetch_related('lead_assign').all()
        for i in users:
            if i.lead_assign.filter(assignedTo=self.request.user.salesexecutive).exists():
                leads = i.lead_assign.filter(assignedTo=self.request.user.salesexecutive).order_by('-date')
                break
        serializer = LeadSerializer(leads,many=True)
        Userserializer = SalesExecutiveSerializer(users,many=True)
        context = {'AllUsers':Userserializer.data,'leads':serializer.data}
        return Response(context)
    
    def post(self,request):
        data = request.data
        lead_id = data['lead_id']
        Lead_Feedback_Id = data['feedback_id']

        if Lead_Feedback_Id == 'None':
            Lead_Feedback_Id = None
        else:
            Lead_Feedback_Id = FeedBack.objects.get(id=Lead_Feedback_Id) 
        if lead_id == 'None':
            lead_id = None
        else:
            lead_id = Lead.objects.get(id=lead_id)

        Massages.objects.create(senderId=self.request.user.salesexecutive,reciverId=SalesExecutive.objects.get(id=data['reciver']),lead=lead_id,feedback=Lead_Feedback_Id,massage=data['message'],datetime=datetime.datetime.now())
        
        get,create = Notification.objects.get_or_create(notification_user=SalesExecutive.objects.get(id=data['reciver']),sender_user=self.request.user.salesexecutive) 
        get.massage = self.request.user.salesexecutive.name +' '+ self.request.user.salesexecutive.typeExecutive + " send a massage"
        get.is_FirstTime = True
        get.save()
        return Response('Message send successfully')

class GetFeedbackesLeadWiseUsingAjexAPI(APIView):
    def get(self,request):
        feedbackes = FeedBack.objects.filter(lead=request.data['Selected_Lead_id']).order_by('-typeFeedBack')
        feedbackserializer =  FeedBackSerializer(feedbackes,many=True)
        return Response({'feedbackes':feedbackserializer.data})

class MessagesInboxAPI(APIView):
    def get(self,request):
        Allmassages = Massages.objects.filter(reciverId=self.request.user.salesexecutive).order_by('-datetime')
        unread_message_length = Allmassages.filter(massagRead=False).count()
        Notification.objects.filter(notification_user=self.request.user.salesexecutive).delete()
        messageserializer =  MassagesSerializer(Allmassages,many=True)
        context = {'UserAllMessages':messageserializer.data,'unread_message_length':unread_message_length}
        return Response(context)

class GetMySpecificMessageAPI(APIView):
    def post(self,request): 
        specific_user_massages = Massages.objects.filter(reciverId=self.request.user.salesexecutive,senderId=request.data['user_id']).order_by('-datetime')
        specific_user_massages.update(massagRead=True)
        messageserializer =  MassagesSerializer(specific_user_massages,many=True)
        return Response({'messgaes':messageserializer.data})

class SpecificUserNotificationsAPI(APIView):
    def get(self,request):
        myallnotifications = DemoFeedback_And_LeadFeedback_Notifications.objects.filter(notification_user=self.request.user.salesexecutive).order_by('-nextDate')
        serializer = DemoFeedback_And_LeadFeedback_NotificationsSerializer(myallnotifications,many=True)
        return Response({'allnotifications':serializer.data})

class TodayScheduleReminderAPI(APIView):
    def get(self,request):
        from datetime import datetime, timedelta
        me = self.request.user.salesexecutive
        myallSchedule = DemoFeedback_And_LeadFeedback_Notifications.objects.filter(notification_user=me).order_by('-nextDate')
        counter = 0
        dlfns_list = []
        try:
            for i in myallSchedule:
                if str(i.nextDate).split(' ')[0] == str(datetime.now()).split(' ')[0]:
                    counter += 1
                    if i.sender_user == self.request.user.salesexecutive:
                        assignedBy = 'yourself'
                    else:
                        assignedBy = i.sender_user.name
                    dlfn_dict = {'assignedBy':assignedBy,'lead':i.lead.personName,'notification_type':i.notification_type,'massage':i.massage}
                    dlfns_list.append(dlfn_dict)
            context = {'todayTotalSchedule':counter,'TodaySchedule':dlfns_list}
        except Exception as e:
            context = {'status':'Failed','messgae':str(e)}
        return Response(context)

class AddSuccessfullyLeadsAPI(APIView):
    def get(self,request):
        leads = Lead.objects.filter(Q(Q(assignedTo=self.request.user.salesexecutive) | Q(feeback_lead__nextCall=self.request.user.salesexecutive)) & Q(Q(lead_status='is_successfull_lead') | Q(lead_status='worked_lead'))).distinct()
        leadsSerializer = LeadSerializer(leads,many=True)
        return Response({'leads':leadsSerializer.data})
    def post(self,request):
        data = request.data
        lead = Lead.objects.get(id=data['comfirmlead'])
        lead.lead_status = 'successfully_lead'
        lead.save()
        SuccessfullyLead.objects.create(by=self.request.user.salesexecutive,lead=lead,priceQuoted=data['decidedPrice'],extra_requirement=data['extrarequirments'],datetime=datetime.datetime.now())
        return Response('Successfully added')

class SpecificPersonSuccessfullyLeadsAPI(APIView):
    def get(self,request):
        successfullyleads = SuccessfullyLead.objects.filter(by=self.request.user.salesexecutive).order_by('datetime')
        successfullLeadsSerializer = SuccessfullyLeadSerializer(successfullyleads,many=True)
        return Response({'Successfully leads':successfullLeadsSerializer.data})
    def post(self,request):
        from_date = request.data['Fromdate']
        to_date = request.data['Todate']
        successfullyleads = SuccessfullyLead.objects.filter(by=self.request.user.salesexecutive,lead__date__gte=from_date,lead__date__lte=to_date).order_by('datetime')
        successfullLeadsSerializer = SuccessfullyLeadSerializer(successfullyleads,many=True)
        return Response({'datewise successfully leads':successfullLeadsSerializer.data})

class ApplyFilterAndSeacrhAPI(APIView):
    def get(self,request):
        return Response({'FilterAndSearch_html'})
    
    def post(self,request):
        from datetime import datetime, timedelta
        last_month = datetime.today() - timedelta(days=30)
        data = request.data
        searching_value = data['searchingvalue']
        if searching_value:
            leads = Lead.objects.filter(Q(Q(Q(personName__icontains=searching_value) | Q(contactPhone__icontains=searching_value) | Q(email__icontains=searching_value)) & Q(Q(assignedTo=self.request.user.salesexecutive) | Q(feeback_lead__nextCall=self.request.user.salesexecutive))) & Q(Q(lead_status='worked_lead') | Q(lead_status='is_successfull_lead'))).order_by('-date').filter(date__gte=last_month).distinct()
        else: 
            from_date = data['Fromdate']
            To_data = data['Todate']
            selectedvale = data['selected_feedback']
            selectedrating = data['selected_rating']

            if selectedrating:
                selectedrating = selectedrating.strip('][').split(',')
            
            if from_date and selectedvale != 'None':
                selectedvale = selectedvale.strip('][').split(',')
                leads = Lead.objects.filter(Q(Q(Q(Q(feeback_lead__feedback__in=selectedvale) | Q(demo_lead__demo_feedback__in=selectedvale) | Q(feeback_lead__rating__in=selectedrating) | Q(demo_lead__demo_rating__in=selectedrating) ) & (Q(assignedTo=self.request.user.salesexecutive) | Q(feeback_lead__nextCall=self.request.user.salesexecutive) | Q(demo_lead__demo_nextCall=self.request.user.salesexecutive))) & Q(Q(lead_status='worked_lead') | Q(lead_status='is_successfull_lead'))) & Q(date__gte=from_date,date__lte=To_data)).order_by('-date').distinct()
            elif from_date  and data['selected_rating']:
                leads = Lead.objects.filter(Q( Q(Q(Q(feeback_lead__rating__in=selectedrating) | Q(demo_lead__demo_rating__in=selectedrating)) & Q(Q(assignedTo=self.request.user.salesexecutive) | Q(feeback_lead__nextCall=self.request.user.salesexecutive) | Q(demo_lead__demo_nextCall=self.request.user.salesexecutive))) & Q(Q(lead_status='worked_lead') | Q(lead_status='is_successfull_lead'))) & Q(date__gte=from_date,date__lte=To_data)).distinct()
            elif from_date:
                leads = Lead.objects.filter(Q(Q(date__gte=from_date,date__lte=To_data) & Q(Q(assignedTo=self.request.user.salesexecutive) | Q(feeback_lead__nextCall=self.request.user.salesexecutive) | Q(demo_lead__demo_nextCall=self.request.user.salesexecutive))) & Q(Q(lead_status='worked_lead') | Q(lead_status='is_successfull_lead'))).order_by('-date').distinct()
            else:
                selectedvale = selectedvale.strip('][').split(',')
                leads = Lead.objects.filter(Q(Q(Q(Q(feeback_lead__feedback__in=selectedvale) | Q(demo_lead__demo_feedback__in=selectedvale) | Q(feeback_lead__rating__in=selectedrating) | Q(demo_lead__demo_rating__in=selectedrating) ) & (Q(assignedTo=self.request.user.salesexecutive) | Q(feeback_lead__nextCall=self.request.user.salesexecutive) | Q(demo_lead__demo_nextCall=self.request.user.salesexecutive))) & Q(Q(lead_status='worked_lead') | Q(lead_status='is_successfull_lead'))) & Q(date__gte=last_month)).order_by('-date').distinct()
        
        leadsSerializer = LeadSerializer(leads,many=True)
        context = {'filteredLeads':leadsSerializer.data}
        return Response(context)

class SortingApplyAPI(APIView):
    def post(self,request):
        sorting_type = request.data['sorting_type']
        if sorting_type == 'latest':
            leads = Lead.objects.filter(Q(Q(assignedTo=self.request.user.salesexecutive) | Q(feeback_lead__nextCall=self.request.user.salesexecutive)) & Q(Q(lead_status='worked_lead') | Q(lead_status='is_successfull_lead'))).order_by('-date').distinct()
        else:
            leads = Lead.objects.filter(Q(Q(assignedTo=self.request.user.salesexecutive) | Q(feeback_lead__nextCall=self.request.user.salesexecutive)) & Q(Q(lead_status='worked_lead') | Q(lead_status='is_successfull_lead'))).order_by('date').distinct()
        leadsSerializer = LeadSerializer(leads,many=True)
        context = {'SortedLeads':leadsSerializer.data}
        return Response(context)

class SalesUserProfileApi(APIView):
    def get(self,request):
        # write something here
        return Response('get function is called')    
    def post(self,request):
        data = request.data
        currentUser = SalesExecutive.objects.get(id=self.request.user.salesexecutive.id)
        currentUser.name = data['first_name']
        currentUser.contact = data['mobile'] 
        currentUser.email = data['email']
        currentUser.address = data['address'] 
        currentUser.save()
        return Response({'status':'updated successfull'})

class SalesUserChangePasswordApi(APIView):    
    def post(self,request):
        new_password = request.data['newPassword']
        if new_password == request.data['confirmPassword']:
            userobj = User.objects.get(id=request.user.id)
            userobj.set_password(new_password)
            userobj.save()
            return Response({'status':'updated successfull'})
        else:
            return Response({'status':'confirm password does not mached your new password '})


class FilterAndSortForAdminApi(APIView):
    def get(self,request):
        all_leads = Lead.objects.all()  
        leadsSerializer = LeadSerializer(all_leads,many=True)
        context = {'all_leads':leadsSerializer.data}  
        return Response(context)
     
    def post(self,request):
        data = request.data
        selected_feedback_for_filter = data['selected_feedback']
        selected_fromDate_for_filter = data['selected_fromDate']
        selected_toDate_for_filter = data['selected_toDate']
        selected_user = data['selected_user']

        selected_feedback_for_filter = selected_feedback_for_filter.strip('][').split(',')

        if data['selected_feedback'] and selected_fromDate_for_filter:
            Filterd_leads = Lead.objects.filter(Q(Q(feeback_lead__feedback__in=selected_feedback_for_filter) | Q(demo_lead__demo_feedback__in=selected_feedback_for_filter)) & Q(date__date__gte=selected_fromDate_for_filter,date__date__lte=selected_toDate_for_filter)  ).order_by('-date').distinct()

        elif selected_fromDate_for_filter:
            Filterd_leads = Lead.objects.filter(date__date__gte=selected_fromDate_for_filter,date__date__lte=selected_toDate_for_filter).order_by('-date')
        else:
            Filterd_leads = Lead.objects.filter(Q(feeback_lead__feedback__in=selected_feedback_for_filter) | Q(demo_lead__demo_feedback__in=selected_feedback_for_filter)).order_by('-date').distinct()
        
        if Filterd_leads and selected_user:
            user = SalesExecutive.objects.get(id=selected_user)
            Filterd_leads = Filterd_leads.filter(assignedTo=user)

        elif Filterd_leads:
            pass
        else:
            user = SalesExecutive.objects.get(id=selected_user)
            Filterd_leads = Lead.objects.filter(assignedTo=user)
            
    
        leadsSerializer = LeadSerializer(Filterd_leads,many=True)
        context = {'filterd_leads':leadsSerializer.data}  
        return Response(context)


'''

class FilterAndSortForAdminApi(APIView):
    def get(self,request):
        all_leads = Lead.objects.all()  
        leadsSerializer = LeadSerializer(all_leads,many=True)
        context = {'all_leads':leadsSerializer.data}  
        return Response(context)
     
    def post(self,request):
        data = request.data
        selected_feedback_for_filter = data['selected_feedback']
        selected_fromDate_for_filter = data['selected_fromDate']
        selected_toDate_for_filter = data['selected_toDate']
        selected_feedback_for_filter = selected_feedback_for_filter.strip('][').split(',')

        if data['selected_feedback'] and selected_fromDate_for_filter:
            Filterd_leads = Lead.objects.filter(Q(Q(feeback_lead__feedback__in=selected_feedback_for_filter) | Q(demo_lead__demo_feedback__in=selected_feedback_for_filter)) & Q(date__gte=selected_fromDate_for_filter,date__lte=selected_toDate_for_filter)  ).order_by('-date').distinct()
        elif selected_fromDate_for_filter:
            Filterd_leads = Lead.objects.filter(date__gte=selected_fromDate_for_filter,date__lte=selected_toDate_for_filter).order_by('-date')
        else:
            Filterd_leads = Lead.objects.filter(Q(feeback_lead__feedback__in=selected_feedback_for_filter) | Q(demo_lead__demo_feedback__in=selected_feedback_for_filter)).order_by('-date').distinct()
        
        leadsSerializer = LeadSerializer(Filterd_leads,many=True)
        context = {'filterd_leads':leadsSerializer.data}  
        return Response(context)
'''
class AssignLeadToAnotherUserApi(APIView):
    def post(self,request):
        data = request.data
        lead_id = data['lead_id']
        user_id = data['user_id']
        lead = Lead.objects.get(id=lead_id)
        lead.assignedTo = SalesExecutive.objects.get(id=user_id)
        lead.save()
        return Response({'status':'update successfully'})

class LogoutUserApi(APIView):
    def get(self,request):
        try:
            self.request.user.auth_token.delete()
        except Exception as e:
            pass
        return Response('Logout successfully')



class DeleteLeadByAdminApi(APIView):
    def post(self,request):
        lead_id = request.data['lead_id']
        lead = Lead.objects.get(id=lead_id).delete()    
        return Response({'status':'delete successfullt'})

# class GetMyNewLeadsDateWise(APIView):
#     def post(self,request,*args,**kwargs):
#         my_profile = self.request.user.salesexecutive

#         date = request.data['date']
#         date = datetime.datetime.strptime(date,'%Y-%m-%d')
#         date_wise_leads = Lead.objects.filter(assignedTo=my_profile,date__date=date,lead_status='is_successfull_lead').order_by('-id')

#         # date_wise_leads = Lead.objects.filter(assignedTo=self.request.user.salesexecutive,date__date=date.date()).order_by('-date')
#         leadsSerializer = LeadSerializer(date_wise_leads,many=True)
#         context = {'leads':leadsSerializer.data}
#         return Response(context)

class UserGetWorkedLeadsFileterWiseAPI(APIView):
    def post(self,request):
        my_profile = self.request.user.salesexecutive    
        data = request.data
        getDateWise = data['getDateWise']
        getFeedbackWise = data['getFeedbackWise']
        getRatingWise = data['getRatingWise']
        getScheduleLeads = data['getScheduleLeads']

        if getDateWise:
            leads = Lead.objects.filter(date__date=getDateWise,assignedTo=my_profile,lead_status='worked_lead').order_by('-id').distinct()
        
        elif getFeedbackWise:
            leads = Lead.objects.filter(Q(feeback_lead__feedback=getFeedbackWise) | Q(demo_lead__demo_feedback=getFeedbackWise),assignedTo=my_profile,lead_status='worked_lead').order_by('-id').distinct()
        
        elif getRatingWise:
            leads = Lead.objects.filter(Q(feeback_lead__rating=getRatingWise) | Q(demo_lead__demo_rating=getRatingWise),assignedTo=my_profile,lead_status='worked_lead').order_by('-id').distinct()

        else:
            leads = Lead.objects.filter(feeback_lead__demo=True,assignedTo=my_profile,lead_status='worked_lead').order_by('-id').distinct()
     
        # leadsSerializer = LeadSerializer(leads,many=True)

        leads_list = []
        for lead in leads:
            totalFeedback = FeedBack.objects.filter(lead=lead).count()
            lead_dict = {'id':lead.id,'personName':lead.personName,'instituteName':lead.instituteName,'contactPhone':lead.contactPhone,'email':lead.email,'numberStudents':lead.numberStudents,'location':lead.location,'notes':lead.notes,'source':lead.source,'assignedTo':lead.assignedTo.name,'lead_status':lead.lead_status,'totalFeedback':totalFeedback,'totalFeedback':totalFeedback}
            leads_list.append(lead_dict)

        context = {'filteredLeads':leads_list}
        return Response(context)


class GetMyTodayAssignedLeadsAPI(APIView):
    def get(self,request):
        me = request.user.salesexecutive
        today_date = timezone.now().date()

        assignedLeadss = Lead.objects.filter(Q(Q(feeback_lead__nextCall=me) | Q(demo_lead__demo_nextCall=me)) & Q(Q(feeback_lead__nextCallDate__date=today_date) | Q(demo_lead__demo_nextCallDate__date=today_date))).order_by('-feeback_lead__time')
        serializer = LeadSerializer(assignedLeadss,many=True)
        context = {'leads':serializer.data}
        return Response(context)   

class GetMyOldLeadsAPI(APIView):
    def get(self,request):
        leads = Lead.objects.filter(assignedTo=self.request.user.salesexecutive,lead_status='old_lead',is_this_old_lead=True).order_by('-date')
        serializer = LeadSerializer(leads,many=True)
        return Response({'Leads':serializer.data})

class GetOldLeadsFilter(APIView):
    def post(self,request):
        profile = self.request.user.salesexecutive
        data = request.data
        leaddate = data['getDateWise']
        rating = data['getRatingWise']
        feedback = data['getFeedbackWise']
        schedule = data['getScheduleLeads']

        if schedule == 'true':
            schedule = True
        else:
            schedule = False


        if leaddate:
            old_leads = Lead.objects.filter(assignedTo=profile, is_this_old_lead=True, date__date=leaddate)

        elif rating:
            # old_leads = Lead.objects.filter(Q(feeback_lead__rating=rating) | Q(demo_lead__demo_rating=rating),assignedTo=profile, is_this_old_lead=True)

            # lead_user = Lead.objects.filter(assignedTo=profile, is_this_old_lead=True)

            # old_leads = []
            # for lead in lead_user:
            #     feedbackes_count = FeedBack.objects.filter(lead=lead,rating=rating).count()
            #     demo_feedbackes_count = DemoFeedback.objects.filter(lead=lead,demo_rating=rating).count()
                

            #     if feedbackes_count != 0 or demo_feedbackes_count !=0:
            #         old_leads.append(lead)

            feedbacks = FeedBack.objects.filter(rating=rating, by=profile)
            demo = DemoFeedback.objects.filter(demo_rating=rating, by=profile)

            result = list(chain(feedbacks, demo))
            
            old_leads = []
            for f in result:
                lead = f.lead 

                if lead in old_leads:
                    pass
                else:
                    old_leads.append(lead)

        elif feedback:
            # old_leads = Lead.objects.filter(Q(feeback_lead__feedback=feedback) | Q(demo_lead__demo_feedback=feedback),assignedTo=profile, is_this_old_lead=True)
            feedback = FeedBack.objects.filter(feedback=feedback, by=profile)
            dfeedback = DemoFeedback.objects.filter(demo_feedback=feedback, by=profile)
            feedback_result = list(chain(feedback, dfeedback))
            old_leads = []
            for f in feedback_result:
                lead = f.lead 

                if lead in old_leads:
                    pass
                else:
                    old_leads.append(lead)


        else:
            # old_leads = Lead.objects.filter(assignedTo=profile, is_this_old_lead=True, feeback_lead__demo=schedule)
            schedule_lead = FeedBack.objects.filter(demo=schedule, by=profile)
            old_leads = []
            for s in schedule_lead:
                lead = s.lead
                old_leads.append(lead)

        leads_list = []
        for lead in old_leads:
            totalFeedback = FeedBack.objects.filter(lead=lead).count() #count no of feedbacks for a lead
            lead_dict = {'id':lead.id,'personName':lead.personName,'instituteName':lead.instituteName,'contactPhone':lead.contactPhone,'email':lead.email,'numberStudents':lead.numberStudents,'location':lead.location,'notes':lead.notes,'source':lead.source,'assignedTo':lead.assignedTo.name,'lead_status':lead.lead_status,'totalFeedback':totalFeedback,'totalFeedback':totalFeedback}
            leads_list.append(lead_dict)

        context = {'filteredLeads':leads_list}
        return Response(context)
    

        
    
        