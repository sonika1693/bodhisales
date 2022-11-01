from django.shortcuts import render,redirect
import csv, io
import pandas as pd
from .models import *
from membership.models import *
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import auth ,User
from django.views.generic.base import View
from django.contrib import messages
import datetime
from django.db.models import Prefetch
from rest_framework.authtoken.models import Token
from django.db.models import Q
# Create your views here.

def UploadCSV(request):
    if request.method == 'GET':
        return render(request,'sales/lead_upload.html')
    else:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv') and not csv_file.name.endswith('.xlsx'):
            messages.error(request,'This is not csv or xlsx file')
            return redirect('/sales/upload_new_csv')        
        elif csv_file.name.endswith('.csv'):
            df = pd.read_csv(csv_file)
        else:
            df = pd.read_excel(csv_file)
        name = df['Name']
        notes = df['Notes']
        phone = df['Phone']
        salesAssigned = df['Code']
        is_this_old_lead = df['is_this_old_lead']

        final_list = list(zip(name,phone,notes,salesAssigned,is_this_old_lead))
        count = 0
        for nm,ph,no,sa,isol in final_list:
            count += 1 
            lead = Lead.objects.filter(contactPhone=ph)
            if len(lead) > 0:
                continue
            else:
                try:
                    salesMan = SalesExecutive.objects.get(salesNumber=sa)
                    educator_type = None
                    mail = None
                    source = None
                    name_coaching = None
                    det = no
                    if 'Educator type' in det:
                        type_educator = det.split('\n')[0]
                        educator_type = type_educator.split(':')[1]
                    if 'Coaching Name' in det:
                        coaching_name = det.split('\n')[1]
                        name_coaching = coaching_name.split(':')[1]
                    if 'Email' in det:
                        mail = det.split('\n')[2]
                        mail = mail.split(':')[1]
                    if 'Lead Source' in det:
                        source=det.split('\n')[3]
                        source=source.split(':')[1]
                    
                    leads=Lead(personName=nm,source=source,instituteName=name_coaching,contactPhone=ph,email=mail,notes=educator_type,assignedTo=salesMan,date=datetime.datetime.now())
                    leads.save()

                    if isol == 'yes':
                        leads.is_this_old_lead = True
                        leads.lead_status = 'old_lead'
                        leads.save()

                except Exception as e:
                    error = str(e)
                    messages.error(request,f'Till now leads {count-1} add successfully but error found at lead no.{count} please check lead {count} ------- {error}')
                    return redirect('/sales/upload_new_csv')
        messages.success(request,'lead uploaded successfully')      
        return redirect('/sales/upload_new_csv')


def loginView(request):
    if request.method == 'GET':
        return render(request,'sales/login.html')
    else:
        username = request.POST.get("UserName")
        password = request.POST.get("Password")
        user = None
        user = auth.authenticate(request, username=username, password=password)
        if user:
            token,created = Token.objects.get_or_create(user=user)
            auth.login(request, user)
            return redirect('/')
        else:
            try:
                User.objects.get(username=username)
                messages.error(request, 'Incorrect Password')
                return redirect('/sales/login')
            except User.DoesNotExist:
                messages.error(request, 'Incorrect Username')
                return redirect('/sales/login')

def GetMyNewLeadView(request):
    leads = Lead.objects.filter(assignedTo=request.user.salesexecutive,lead_status='is_successfull_lead').order_by('-id')
    return render(request,'sales/lead.html',{"leads":leads})

def GetMyWorkedLeadsView(request):
    leads = Lead.objects.filter(assignedTo=request.user.salesexecutive,lead_status='worked_lead').order_by('-date')
    return render(request, 'sales/Workedleads.html', {'allworkedleads': leads})
    
class FeedbackCreateView(View):
    def get(self,request):
        users = SalesExecutive.objects.all()
        typefeedback = FeedBack.objects.filter(lead=request.GET['lead_id']).count() + 1
        return render(request,'sales/Feedback.html',{'SalesExecutiveUser':users,'feedbacktype':typefeedback})

    def post(self,request):
        demo = request.POST.get("demo")
        iswronglead = request.POST.get("iswronglead")
        furthercall = request.POST.get("furthercall")
        lead_id = request.POST.get('lead_id')
        NextCallUser = request.POST.get("nextcalluser")
        NextCallDate = request.POST.get("nextcalldate")
        demo_next_date = request.POST.get("demodate")
        my_profile = self.request.user.salesexecutive
        
        lead = Lead.objects.get(id=lead_id)
        lead.lead_status = 'worked_lead'
        lead.save()
        feedback = FeedBack(typeFeedBack=FeedBack.objects.filter(lead=lead_id).count() + 1,by=my_profile,lead=lead,time= datetime.datetime.now(),
                            rating=request.POST.get("rating"),notes=request.POST.get("notes"),Cource=request.POST.get("Course"),
                            instituteType=request.POST.get("instituteType"),State=request.POST.get("state"),city=request.POST.get("city"))
        if NextCallDate:
            feedback.nextCallDate = NextCallDate
        else:
            feedback.nextCallDate = None
            NextCallDate = None
        if NextCallUser:
            executive = SalesExecutive.objects.get(id=NextCallUser)
            feedback.nextCall = executive
            DemoFeedback_And_LeadFeedback_Notifications.objects.create(notification_user=executive,
            sender_user=self.request.user.salesexecutive,notification_type='LeadFeedbackNotification',lead=lead,
            massage = f"Today is your Feedback schedule of this {lead.personName} lead So remember This", is_FirstTime=True ,nextDate=NextCallDate,datetime=datetime.datetime.now())
        else:
            feedback.nextCall = None
        if demo_next_date:
            feedback.demoDate = demo_next_date
        else:
            feedback.demoDate = None
            demo_next_date = None

        if demo == 'on':
            feedback.demo = True
            DemoFeedback_And_LeadFeedback_Notifications.objects.create(notification_user=my_profile,
            sender_user=my_profile,notification_type='DemoNotification',lead=lead,
            massage = f"Today is your demo schedule of this {lead.personName} lead So remember This", is_FirstTime=True ,nextDate=demo_next_date,datetime=datetime.datetime.now())
        else:
            feedback.demo = False

        if iswronglead == 'on':
            feedback.Is_wrongLead = True
        else:
            feedback.Is_wrongLead = False
        feedback.feedback = request.POST.get("feedback")
        if furthercall == 'on':
            feedback.furtherCall = True
        else:
            feedback.furtherCall = False
        feedback.priceQuoted = request.POST.get("pricequoted")
        feedback.save()
        messages.success(request, 'Feedback saved successfully')
        return redirect('/sales/feedback_creating/?lead_id='+lead_id)

class DemoCreatingView(View):
    def get(self,request):
        users = SalesExecutive.objects.all()
        typedemo = DemoFeedback.objects.filter(lead=request.GET['lead_id']).count() + 1
        return  render(request,'sales/DemoCreating.html',{'SalesExecutiveUser':users,'typedemo':typedemo})
    
    def post(self,request):
        lead_id = request.POST.get('lead_id')
        my_profile = self.request.user.salesexecutive
        lead = Lead.objects.get(id=lead_id)
        DemoNextUser = request.POST.get("demo_nextCall")
        DemoNextDate = request.POST.get("demo_nextCallDate")
        demofeedback = DemoFeedback(typedemo=DemoFeedback.objects.filter(lead=lead_id).count()+1, by=my_profile, lead=lead,
                            datetime=datetime.datetime.now(),demo_rating=request.POST.get("demo_rating"), 
                            extra_notes=request.POST.get("extra_notes"),demo_feedback=request.POST.get("demo_feedback"),
                            price_quoted = request.POST.get("price_quoted"))
        if DemoNextDate:
            demofeedback.demo_nextCallDate = DemoNextDate
        else:
            demofeedback.demo_nextCallDate = None
            DemoNextDate = None
        if DemoNextUser:
            nextcaller = SalesExecutive.objects.get(id=DemoNextUser)
            demofeedback.demo_nextCall = nextcaller
            DemoFeedback_And_LeadFeedback_Notifications.objects.create(notification_user=nextcaller,sender_user=self.request.user.salesexecutive,notification_type='DemoNotification',lead=lead,
            massage = f"Today is your Demo schedule of this {lead.personName} lead So remember This",is_FirstTime = True,nextDate=DemoNextDate,datetime=datetime.datetime.now())
        else:
            demofeedback.demo_nextCall = None
        demofeedback.save()
        messages.success(request, 'demofeedback saved successfully')
        return redirect('/sales/demo_creating/?lead_id='+lead_id)

class SendMassageToUserView(View):
    def get(self,request):
        leads = None
        users = SalesExecutive.objects.prefetch_related('lead_assign').all()
        for i in users:
            if i.lead_assign.filter(assignedTo=self.request.user.salesexecutive).exists():
                leads = i.lead_assign.filter(assignedTo=self.request.user.salesexecutive).order_by('-date')
                break
        context = {'SalesExecutiveUser':users,'leads':leads}
        return render(request,'sales/MassageForm.html',context)
    
    def post(self,request):
        lead_id = request.POST.get('sendinglead')
        Lead_Feedback_Id = request.POST.get('feedback')
        if Lead_Feedback_Id:
            Lead_Feedback_Id = FeedBack.objects.get(id=Lead_Feedback_Id) 
        else:
            Lead_Feedback_Id = None
        if lead_id:
            lead_id = Lead.objects.get(id=lead_id)
        else:
            lead_id = None
        Massages.objects.create(senderId=self.request.user.salesexecutive,reciverId=SalesExecutive.objects.get(id=request.POST.get('reciver')),lead=lead_id,feedback=Lead_Feedback_Id,massage=request.POST.get('massage'),datetime=datetime.datetime.now())

        get,create = Notification.objects.get_or_create(notification_user=SalesExecutive.objects.get(id=request.POST.get('reciver')),sender_user=self.request.user.salesexecutive) 
        get.massage = self.request.user.salesexecutive.name +' '+ self.request.user.salesexecutive.typeExecutive + " send a massage"
        get.is_FirstTime = True
        get.save()
        messages.success(request,'massage send successfully')
        return redirect('/sales/Sendmassage/')

def GetFeedbackesLeadWiseUsingAjexView(request):
    feedbackes = FeedBack.objects.filter(lead=request.GET.get('Selected_lead_id')).order_by('-typeFeedBack').values()
    return JsonResponse(list(feedbackes),safe=False)

def GetMyAssignedLeadsView(request):
    assignedLeadss = Lead.objects.filter(Q(Q(Q(feeback_lead__nextCall=request.user.salesexecutive) | Q(demo_lead__demo_nextCall=request.user.salesexecutive)) & Q(Q(lead_status='worked_lead') | Q(lead_status='is_successfull_lead'))) & ~Q(Q(feeback_lead__by=request.user.salesexecutive) | Q(demo_lead__by=request.user.salesexecutive))).order_by('-feeback_lead__time')    
    return render(request,'sales/AssignedLeads.html',{'assignedLeadss':assignedLeadss})

def MessagesInboxView(request):
    Allmassages = Massages.objects.filter(reciverId=request.user.salesexecutive).order_by('-datetime')
    list1 = []
    list2 = []
    for i in Allmassages:
        if i.senderId.id not in list1:
            list1.append(i.senderId.id)
            list2.append(i)
    unread_massage_length = Allmassages.filter(massagRead=False).count()
    Notification.objects.filter(notification_user=request.user.salesexecutive).delete()
    context = {'usermassages':list2,'unread_massage_length':unread_massage_length}
    return render(request,'sales/MessagesInbox.html',context)

def GetSpecificUserMessageView(request,user_id):
    specific_user_massages = Massages.objects.filter(reciverId=request.user.salesexecutive,senderId=user_id).order_by('-datetime')
    specific_user_massages.update(massagRead=True)
    return render(request,'sales/SpecificMessagesInbox.html',{'specific_user_massages':specific_user_massages})

def GetFeedbackesAndDemos_A_SpecificLeadWiseView(request):
    lead_id = request.GET['lead_id']
    feedbackes_SpecificLeadWise = FeedBack.objects.filter(lead=lead_id).order_by('-time')
    demos_SpecificLeadWise = DemoFeedback.objects.filter(lead=lead_id).order_by('-datetime')
    context = {'feedbackes_SpecificLeadWise':feedbackes_SpecificLeadWise,'demos_SpecificLeadWise':demos_SpecificLeadWise}
    return render(request,'sales/AllFeedbackAndDemo_A_SpecificLead.html',context)

def GetSpecificLeadAndFeedbackView(request,lead_id=None,feedback_id=None):
    specific_lead_and_feedback = Lead.objects.filter(id=lead_id).prefetch_related(
        Prefetch(
            "feeback_lead",
            queryset=FeedBack.objects.filter(id=feedback_id),
            to_attr="recieved_feedback"
        )
    )
    return render(request,'sales/SpecificLeadAndFeedback.html',{'specific_lead_and_feedback':specific_lead_and_feedback})
    
def GetMyAllNotificationsView(request):
    myallnotifications = DemoFeedback_And_LeadFeedback_Notifications.objects.filter(notification_user=request.user.salesexecutive).order_by('-nextDate')
    return render(request,'sales/Allnotification.html',{'myallnotifications':myallnotifications})   

class AddSuccessfullyLeadView(View):
    def get(self,request):
        leads = Lead.objects.filter(Q(Q(assignedTo=self.request.user.salesexecutive) | Q(feeback_lead__nextCall=self.request.user.salesexecutive)) & Q(Q(lead_status='is_successfull_lead') | Q(lead_status='worked_lead'))).distinct()
        return render(request,'sales/AddSuccessfullyLead.html',{'leads':leads})

    def post(self,request):
        lead = Lead.objects.get(id=request.POST.get('comfirmlead'))
        lead.lead_status = 'successfully_lead'
        lead.save()
        SuccessfullyLead.objects.create(by=self.request.user.salesexecutive,lead=lead,priceQuoted=request.POST.get('decidedPrice'),extra_requirement=request.POST.get('extrarequirments'),datetime=datetime.datetime.now())
        messages.success(request,'successfully added')
        return redirect('/sales/add_comfirmLead/')

def SpecificPersonSuccessfullyLeadsView(request):
    if request.method == 'GET':
        successfullyleads = SuccessfullyLead.objects.filter(by=request.user.salesexecutive).order_by('datetime')
    else:
        from_date = request.POST.get('Fromdate')
        to_date = request.POST.get('Todate')
        successfullyleads = SuccessfullyLead.objects.filter(by=request.user.salesexecutive,lead__date__gte=from_date,lead__date__lte=to_date).order_by('datetime')
    return render(request,'sales/SuccessfullyLeads.html',{'successfullyleads':successfullyleads})

class ApplyFilterAndSeacrhView(View):
    def get(self,request):
        return render(request,'sales/LeadFilterAndSearch.html')
    
    def post(self,request):
        from datetime import datetime, timedelta
        last_month = datetime.today() - timedelta(days=60)
        searching_value = request.POST.get('searchingvalue')
        selectedvale = request.POST.getlist('feedbackesfilter')
        selectedrating = request.POST.getlist('filterByRating')
        if searching_value:
            leads = Lead.objects.filter(Q(Q(Q(personName__icontains=searching_value) | Q(contactPhone__icontains=searching_value) | Q(email__icontains=searching_value)) & Q(Q(assignedTo=self.request.user.salesexecutive) | Q(feeback_lead__nextCall=self.request.user.salesexecutive))) & Q(Q(lead_status='worked_lead') | Q(lead_status='is_successfull_lead'))).order_by('-date').filter(date__gte=last_month).distinct()
        else:
            from_date = request.POST.get('Fromdate')
            To_data = request.POST.get('Todate')
            
            if from_date and selectedvale:
                leads = Lead.objects.filter(Q(Q(Q(Q(feeback_lead__feedback__in=selectedvale) | Q(demo_lead__demo_feedback__in=selectedvale) | Q(feeback_lead__rating__in=selectedrating) | Q(demo_lead__demo_rating__in=selectedrating) ) & (Q(assignedTo=self.request.user.salesexecutive) | Q(feeback_lead__nextCall=self.request.user.salesexecutive) | Q(demo_lead__demo_nextCall=self.request.user.salesexecutive))) & Q(Q(lead_status='worked_lead') | Q(lead_status='is_successfull_lead'))) & Q(date__gte=from_date,date__lte=To_data)).order_by('-date').distinct()
            elif from_date and selectedrating:
                leads = Lead.objects.filter(Q( Q(Q(Q(feeback_lead__rating__in=selectedrating) | Q(demo_lead__demo_rating__in=selectedrating)) & Q(Q(assignedTo=self.request.user.salesexecutive) | Q(feeback_lead__nextCall=self.request.user.salesexecutive) | Q(demo_lead__demo_nextCall=self.request.user.salesexecutive))) & Q(Q(lead_status='worked_lead') | Q(lead_status='is_successfull_lead'))) & Q(date__gte=from_date,date__lte=To_data)).distinct()
            elif from_date:
                leads = Lead.objects.filter(Q(Q(date__gte=from_date,date__lte=To_data) & Q(Q(assignedTo=self.request.user.salesexecutive) | Q(feeback_lead__nextCall=self.request.user.salesexecutive) | Q(demo_lead__demo_nextCall=self.request.user.salesexecutive))) & Q(Q(lead_status='worked_lead') | Q(lead_status='is_successfull_lead'))).order_by('-date').distinct()
            else:
                leads = Lead.objects.filter(Q(Q(Q(Q(feeback_lead__feedback__in=selectedvale) | Q(demo_lead__demo_feedback__in=selectedvale) | Q(feeback_lead__rating__in=selectedrating) | Q(demo_lead__demo_rating__in=selectedrating) ) & (Q(assignedTo=self.request.user.salesexecutive) | Q(feeback_lead__nextCall=self.request.user.salesexecutive)  | Q(demo_lead__demo_nextCall=self.request.user.salesexecutive) )) & Q(Q(lead_status='worked_lead') | Q(lead_status='is_successfull_lead'))) & Q(date__gte=last_month)).order_by('-date').distinct()

        feedback_list = []
        for i in leads:
            feedback = i.feeback_lead.filter(Q(feedback__in=selectedvale) | Q(rating__in=selectedrating))
            feedback_list.append(feedback)        
        context = {'filteredLeads':leads,'searching_value':searching_value,'feedback_list':feedback_list}
        return render(request,'sales/LeadFilterAndSearch.html',context)

def SortingApplyView(request,sorting_type):
    if sorting_type == 'latest':
        leads = Lead.objects.filter(Q(Q(assignedTo=request.user.salesexecutive) | Q(feeback_lead__nextCall=request.user.salesexecutive)) & Q(Q(lead_status='worked_lead') | Q(lead_status='is_successfull_lead'))).order_by('-date').distinct()
    else:
        leads = Lead.objects.filter(Q(Q(assignedTo=request.user.salesexecutive) | Q(feeback_lead__nextCall=request.user.salesexecutive)) & Q(Q(lead_status='worked_lead') | Q(lead_status='is_successfull_lead'))).order_by('date').distinct()
    return render(request,'sales/LeadFilterAndSearch.html',{'filteredLeads':leads,'sorting_type':sorting_type})

def SalesUserProfileView(request):
    if request.method == 'GET':
        currentUser = SalesExecutive.objects.get(executiveUser=request.user.id)
        new_leads_length = currentUser.lead_assign.filter(lead_status='is_successfull_lead').count()
        worked_leads_length = currentUser.lead_assign.filter(lead_status='worked_lead').count()
        successfully_leads_length = currentUser.successfull_lead_user.count()
        assignedleads = Lead.objects.filter(Q(Q(Q(feeback_lead__nextCall=request.user.salesexecutive) | Q(demo_lead__demo_nextCall=request.user.salesexecutive)) & Q(Q(lead_status='worked_lead') | Q(lead_status='is_successfull_lead'))) & ~Q(Q(feeback_lead__by=request.user.salesexecutive) | Q(demo_lead__by=request.user.salesexecutive))).count()
        context = {'assignedleads':assignedleads,'NewleadsLenght':new_leads_length,'WorkedLeadsLenght':worked_leads_length,'successfully_leads_length':successfully_leads_length}
        return render(request,'sales/salesUserProfile.html',context)
    else:
        currentUser = SalesExecutive.objects.get(id=request.user.salesexecutive.id)
        currentUser.name = request.POST.get('first_name')
        currentUser.contact = request.POST.get('mobile') 
        currentUser.email = request.POST.get('email')
        currentUser.address = request.POST.get('address') 
        currentUser.save()
        messages.success(request,'updated successfull')
        return redirect('/sales/salesUser_profile')

def SalesUserChangePasswordView(request):
    if request.method == 'POST':
        new_password = request.POST.get('newPassword')
        if new_password == request.POST.get('confirmPassword'):
            userobj = User.objects.get(id=request.user.id)
            userobj.set_password(new_password)
            userobj.save()
            messages.success(request,'password update successfully')
            return redirect('/')
        else:
            messages.error(request,'confirm password does not mached your new password ')
            return redirect('/sales/salesUser_profile')
    
def logoutview(request):
    try:
        request.user.auth_token.delete()
    except Exception as e:
        pass
    auth.logout(request)
    messages.success(request, 'Logged Out Successfully')
    return redirect('/sales/login')
