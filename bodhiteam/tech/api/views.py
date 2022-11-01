
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from membership.models import *
from tech.models import *
from django.db.models import Q
import datetime

# assigned person details
class AssignedUser(APIView):
    def get(self,request):
        get_user = TechPerson.objects.get(typeTech__iexact='Team Leader')
        assign_info = {
            'id':get_user.id,
            'name':get_user.name
        }        
        context = {'status':'Success','message':'Leam Leader Info','assign_info':assign_info}
        return Response(context)

# show list of developer's technology 
class AllTechnology(APIView):
    def get(self,request):
        profile = self.request.user.techperson
        get_user = TechPerson.objects.get(typeTech__iexact='Team Leader')
        technology_list = []
        if(profile==get_user):
            all_technology = Technology.objects.all()
            for technology in all_technology:
                developer_technology = {'id':technology.id,'name':technology.name}
                technology_list.append(developer_technology)
            context = {'status':'Success','technology_list':technology_list}
        else:
            context = {'status':'Failed','message':'not authorized to see technology list'}
        return Response(context)

# show the list of all tech users
class TechUsers(APIView):
    def get(self,request):
        all_developers = TechPerson.objects.all()
        dev_list = []
        for i in all_developers:
            developer = {
                'id':i.id,
                'name':i.name,
                'joiningDate':i.joiningDate,
                'typeTech':i.typeTech,
                'technology':i.technology.all().values()
            }
            dev_list.append(developer)
        context = {'status':'Success','dev_list':dev_list}
        return Response(context)

# sales team create a task and assign to team leader
class CreateTask(APIView):
    def post(self,request):
        data = request.data
        assigned_user          = data['assigned_user']
        institute              = data['institute']
        task_title             = data['task_title']
        task_description       = data['task_description']
        due_date               = data['due_date']

        try:
            tech_person = TechPerson.objects.get(id=assigned_user)
            if due_date:
                due_date = datetime.datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
            else:
                due_date = None  
            Task.objects.create(assignedTo=tech_person,institute=institute,task_title=task_title,task_description=task_description,due_date=due_date)
            context = {'status':'Success','message':'Demo saved'}
        except Exception as e:
            context = {'status':'Failed','message':str(e)}

        return Response(context)

# get list of all tasks to team leader
class GetTasks(APIView):   
    def get(self,request):
        profile = self.request.user.techperson #techperson is model name
        all_task = Task.objects.filter(assignedTo=profile).order_by('-id')
        tasklist = []
        for t in all_task:
            task = {'id':t.id,'title':t.task_title,'create_date':t.create_date,'due_date':t.due_date,'project_status':t.project_status.title}
            tasklist.append(task)
        context = {'status':'Success','tasklist':tasklist}
        return Response(context)

# task related all details
class TaskDetails(APIView):
    def post(self,request):
        profile = self.request.user.techperson
        data = request.data
        task_id = data['task_id']
        if profile:
            task = Task.objects.get(id=task_id)
            all_developers = []
            for developer in task.workedBy.all(): #it will return object
                all_developers.append(developer.name)

            task_details = {
                'workedBy' : all_developers,
                # 'workedBy' : task.workedBy.all().values(),
                'institute' : task.institute,
                'task_title': task.task_title,
                'task_description': task.task_description,
                'create_date': task.create_date,
                'due_date': task.due_date
            }
            
            context = {'status':'success','task_details':task_details}
        else:
            context = {'status':"Failed",'message':"You Can't access data"}
        return Response(context)

# team leader assign task to developers
class AssignTask(APIView):
    def post(self,request):
        data = request.data
        task_id = data['task_id']
        user_id = data['user_id']
        users_list = user_id.strip('][').split(',')

        user_task = Task.objects.get(id=task_id)
        project_status = ProjectStatus.objects.get(title__iexact="Assigned")
        user_task.project_status = project_status
        user_task.save()

        for uid in users_list:
            tech_person = TechPerson.objects.get(id=uid)
            task = user_task.workedBy.add(tech_person)
            developer_task = DeveloperReport.objects.create(developer=tech_person,task=user_task)
               
        context = {'status':'Success','message':'task assigned'}
        return Response(context)

# status list used by team leader to update project status
class ProjectStatusList(APIView):
    def get(self,request):
        allstatus = ProjectStatus.objects.all()
        status_list = []
        for i in allstatus:
            if i.title__iexact=="Created" or i.title__iexact=="Assigned":
                pass
            else:
                status = {'id':i.id,'title':i.title}
                status_list.append(status)

        context = {'status_list':status_list}
        return Response(context)

# team leader can update project status according to progress         
class UpdateProjectStatus(APIView):
    def post(self,request):
        data = request.data
        task_id = data['task_id']
        ps_id = data['ps_id']

        task = Task.objects.get(id=task_id)
        status = ProjectStatus.objects.get(id=ps_id)
        task.project_status = status
        task.save()
        
        context = {'status':'Success','message':'Status updated successfully'}
        return Response(context)

# list of task for developers
class UserTask(APIView):
    def get(self,request):
        profile = self.request.user.techperson
        user_tasks = DeveloperReport.objects.filter(developer=profile).order_by('-id')
            
        task_list = []
        for ut in user_tasks:
            all_task = {'id':ut.id,'task':ut.task.task_title,'status':ut.status.title}
            task_list.append(all_task)

        context = {'status':'Success','user_task_list':task_list}
        return Response(context)

# developer status list
class UserStatusList(APIView):
    def get(self,request):
        allstatus = UserStatus.objects.all()
        status_list = []
        for i in allstatus:
            if i.title=="Unseen" or i.title=="Seen":
                pass
            else:
                status = {'id':i.id,'title':i.title}
                status_list.append(status)
                
        context = {'status_list':status_list}
        return Response(context)

# developer can update their status
class UpdateUserStatus(APIView):
    def post(self,request):
        # profile = self.request.user.techperson
        data = request.data
        user_id = data['user_id']
        task_id = data['task_id']
        feedback = data['feedback']
        user_status_id = data['user_status_id']
        developer = TechPerson.objects.get(id=user_id)
        task = Task.objects.get(id=task_id)
        status = UserStatus.objects.get(id=user_status_id)
        report = DeveloperReport.objects.create(developer=developer,task=task,status=status,developer_issues=feedback)
        
        context = {'status':'Success','message':'User Data updated successfully'}
        return Response(context)

class UserTaskReport(APIView):
    def post(self,request):
        profile = self.request.user.techperson
        get_user = TechPerson.objects.get(typeTech__iexact='Team Leader')
        data = request.data
        user_id = data['user_id']
        task_id = data['task_id']
        if(profile==get_user):
            developer = TechPerson.objects.get(id=user_id)
            task = Task.objects.get(id=task_id)
            reports = DeveloperReport.objects.filter(developer=developer,task=task).order_by('-id')
            report_list = []
            for report in reports:
                all_report = {
                    'id': report.id,
                    'developer' : report.developer.name,
                    'task' : report.task.task_title,
                    'status' : report.status.title,
                    'date' : report.date
                    }
                report_list.append(all_report)  

        context = {'status':'Success','User Report List':report_list}
        return Response(context)

    




         
 


    
        
         