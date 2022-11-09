from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views.generic.base import View
from django.contrib import messages
from .models import * 
# Create your views here.

def Profile(request):
    user = request.user.techperson
    return render(request,'tech/Profile.html')

def CreateTask(request):
    if request.method == "GET":
        team_leader = TechPerson.objects.filter(typeTech="Team Leader")
        return render(request,'tech/CreateTask.html',{'team_leader':team_leader})

    else:
        # team_leader = TechPerson.objects.filter(typeTech="Team Leader")
        assigned_to = request.POST.get('assigned_to')
        institute = request.POST.get('institute')
        task_title = request.POST.get('task_title')
        task_description = request.POST.get('task_description')
        due_date = request.POST.get('due_date')
        if due_date:
            due_date = due_date
        else:
            due_date = None
        
        assigned_user = TechPerson.objects.get(id=assigned_to)
        Task.objects.create(assignedTo=assigned_user,institute=institute,task_title=task_title,task_description=task_description,due_date=due_date)
        messages.success(request, 'Create Task Successfully')
        # return render(request,'tech/CreateTask.html',{'team_leader':team_leader})
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def NewTask(request):
    profile = request.user.techperson
    get_user = TechPerson.objects.get(typeTech__iexact='Team Leader')
    if(profile==get_user):
        tasks = Task.objects.filter(assignedTo=get_user, project_status__title__iexact="Created").order_by('-id')
        task_count = tasks.count()
    else:
        tasks = DeveloperReport.objects.filter(developer=profile,task_status__title__iexact="Created").order_by('-id')
        task_count = tasks.count()
    return render(request,'tech/NewTask.html',{'tasks':tasks,'task_count':task_count,'get_user':get_user})

def AssignedTask(request):
    profile = request.user.techperson
    get_user = TechPerson.objects.get(typeTech__iexact='Team Leader')
    if(profile==get_user): 
        tasks = Task.objects.filter(assignedTo=profile, project_status__title__iexact="Assigned").order_by('-id')

    return render(request,'tech/AssignedTask.html',{'tasks':tasks})

def OngoingTask(request):
    profile = request.user.techperson
    get_user = TechPerson.objects.get(typeTech__iexact='Team Leader')
    if(profile==get_user): 
        tasks = Task.objects.filter(assignedTo=profile,project_status__title__iexact="Ongoing").order_by('-id')
    else:
        tasks = DeveloperReport.objects.filter(developer=profile, task_status__title__iexact="Ongoing").order_by('-id')

    return render(request,'tech/OngoingTask.html',{'tasks':tasks})

def CompletedTask(request):
    profile = request.user.techperson
    get_user = TechPerson.objects.get(typeTech__iexact='Team Leader')
    if(profile==get_user): 
        tasks = Task.objects.filter(assignedTo=profile,project_status__title__iexact="Completed").order_by('-id')
    else:
        tasks = DeveloperReport.objects.filter(developer=profile, task_status__title__iexact="Completed").order_by('-id')

    return render(request,'tech/CompletedTask.html',{'tasks':tasks})

def AcceptedTask(request):
    profile = request.user.techperson
    tasks = DeveloperReport.objects.filter(developer=profile,status__title__iexact="Accept").order_by('-id')
    return render(request,'tech/AcceptedTask.html',{'tasks':tasks})

def TaskDetails(request): 
    if request.method == "GET":
        task_id = request.GET.get('task_id')
        task = Task.objects.filter(id=task_id).first()
        users_list = task.workedBy.all()
        assigned_developer_report = DeveloperReport.objects.filter(developer__in = users_list, task = task).order_by('-id')
        individual_developer_report = DeveloperReport.objects.filter(developer = request.user.techperson, task = task).order_by('-id')
        user_status = UserStatus.objects.exclude(title__iexact='Unseen')
        hide_status_from_list = ['Assigned','Created']
        task_status = ProjectStatus.objects.exclude(title__in=hide_status_from_list)

        context = {
            'task':task,
            'developers':users_list,
            'assigned_developer_report':assigned_developer_report,
            'individual_developer_report':individual_developer_report,
            'user_status':user_status,
            'task_status':task_status
        }
    else:
        task_id = request.POST.get('task_id')
        developer_id = request.POST.get('developer_id')
        task = Task.objects.filter(id=task_id).first()
        users_list = task.workedBy.all()
        if developer_id == 'all':
            assigned_developer_report = DeveloperReport.objects.filter(task = task).order_by('-id')
        else:
            assigned_developer_report = DeveloperReport.objects.filter(developer__id=developer_id,task = task).order_by('-id')

        individual_developer_report = DeveloperReport.objects.filter(developer = request.user.techperson, task = task).order_by('-id')
        user_status = UserStatus.objects.exclude(title__iexact='Unseen')
        hide_status_from_list = ['Assigned','Created']
        task_status = ProjectStatus.objects.exclude(title__in=hide_status_from_list)

        context = {
            'task':task,
            'developers':users_list,
            'assigned_developer_report':assigned_developer_report,
            'individual_developer_report':individual_developer_report,
            'user_status':user_status,
            'task_status':task_status
        }

    return render(request,'tech/TaskDetails.html',context)

def DeleteDeveloperTask(request,id,task_id):
    report = DeveloperReport.objects.get(id=id)
    report.delete()
    all_reports = DeveloperReport.objects.filter(task__id=task_id,developer=report.developer).count()
    if all_reports==0:
        report.task.workedBy.remove(report.developer)

    messages.success(request, 'Delete Successfully')
    return redirect(f"/tech/task_details/?task_id={task_id}")

def EditTask(request):
    if request.method == "POST": 
        task_id = request.POST.get('task_id')
        users_list = request.POST.getlist('worked_by')
        projectStatus = request.POST.get('projectStatus')
        additional_details = request.POST.get('additional_details')
        due_date = request.POST.get('due_date')

        task = Task.objects.get(id=task_id)
        if users_list:
            project_status = ProjectStatus.objects.all()
            if task.project_status.title == 'Created':
                status = project_status.get(title='Assigned')
                task.project_status = status
            else:
                status = project_status.get(id=projectStatus)
                task.project_status = status

        task.additional_details = additional_details
        task.due_date = due_date
        task.save()

        worked_by = task.workedBy.all().values_list('id',flat=True)
        for userid in users_list:
            if int(userid) not in worked_by:
                tech_person = TechPerson.objects.get(id=userid)
                add_tech_person = task.workedBy.add(tech_person)
                # entry for developer report table
                developer_task = DeveloperReport.objects.create(developer=tech_person,task=task)
        
        messages.success(request, 'Update Successfully')
        return redirect("/tech/edit_task/?task_id="+str(task_id)) 
    else: 
        hide_status_from_user_list = ['Assigned','Created']
        all_status = ProjectStatus.objects.exclude(title__in=hide_status_from_user_list)
        
        # technology = Technology.objects.exclude(name="All")
        developer_list = TechPerson.objects.exclude(typeTech="Team Leader")
        get_task = Task.objects.get(id=request.GET['task_id'])
        workedBy = get_task.workedBy.all().values_list('id',flat=True)#return list not list of tuples

        return render(request,'tech/EditTask.html',{'get_task':get_task,'developer_list':developer_list,'status_list':all_status,'workedBy':workedBy})

def DeveloperTask(request):
    profile = request.user.techperson
    get_user = TechPerson.objects.get(typeTech__iexact='Team Leader')
    if profile==get_user:
        user_tasks = DeveloperReport.objects.all().order_by('-id')
    else:
        user_tasks = DeveloperReport.objects.filter(developer=profile).order_by('-id')

    return render(request,'tech/DeveloperTask.html',{'user_tasks':user_tasks})

def UserTaskDetails(request,id):
    report = DeveloperReport.objects.get(id=id)
    return render(request,'tech/UserTaskDetails.html',{'report':report})

def AddReport(request,task_id):
    if request.method == "POST":
        profile = request.user.techperson
        task = Task.objects.get(id=task_id)
        user_status_id = request.POST.get('user_status')
        task_status_id = request.POST.get('task_status')
        user_query = request.POST.get('user_query')
        if user_status_id:
            userStatus = UserStatus.objects.get(id=user_status_id)
        if task_status_id:
            taskStatus = ProjectStatus.objects.get(id=task_status_id)
        developer_task = DeveloperReport.objects.create(developer=profile,task=task,status=userStatus,task_status=taskStatus,developer_issues=user_query)

    messages.success(request, 'New Report Added Successfully')
    return redirect("/tech/task_details/?task_id="+str(task_id))

def DeleteCreatedTask(request,id):
    task = Task.objects.get(id=id)
    task.delete()
    messages.success(request, 'Delete Task Successfully')
    return redirect("/tech/new_task/")

# def DeleteDeveloperTask(request,id,task_id):
#     report = DeveloperReport.objects.get(id=id)
#     all_reports = DeveloperReport.objects.filter(task__id=task_id,developer=report.developer)
#     if len(all_reports) == 1:
#         task = report.task
#         user = report.developer
#         report.delete()
#         assigned_users = task.workedBy.remove(user)
#     else:
#         report.delete()