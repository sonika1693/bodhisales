from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from membership.models import *
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
import datetime

class Login(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        username = data['username']
        password = data['password']
        typeUser = data['typeUser']
        try:
            user = authenticate(username=username,password=password)           
            token,created = Token.objects.get_or_create(user=user)
            if typeUser =='admin':
                try:
                    finalUser = User.objects.get(is_superuser=True,username=user)
                    context={'status':'Success','token':token.key,'username':username,'name':finalUser.username,'typeUser':'admin'}
                except Exception as e:
                    context = {'status':'Failed','hint':'Choose CorrectUser Type','message':str(e)}

            elif typeUser == 'sales':
                finalUser = SalesExecutive.objects.get(executiveUser=user)
                context = {'status':'Success','token':token.key,'username':username,'name':finalUser.name,'typeUser':typeUser}
            elif typeUser == 'tech':
                finalUser = TechPerson.objects.get(executiveUser=user)
                context = {'status':'Success','token':token.key,'username':username,'name':finalUser.name,'typeUser':typeUser}
            elif typeUser == 'uploaduser':
                finalUser = UploadUser.objects.get(uploaduser=user)
                context = {'status':'Success','token':token.key,'username':username,'name':finalUser.name,'typeUser':typeUser}
            else:
                context={'status':'Failed','message':'Choose CorrectUser Type'}
            
        except Exception as e:
            context = {'status':'Failed','message':str(e)}
        return Response(context)

'''
class Login(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        username = data['username']
        password = data['password']
        typeUser = data['typeUser']
        try:
            user = authenticate(username=username,password=password)           
            token,created = Token.objects.get_or_create(user=user)
            if typeUser == 'sales':
                finalUser = SalesExecutive.objects.get(executiveUser=user)
                context = {'status':'Success','token':token.key,'username':username,'name':finalUser.name,'typeUser':typeUser}
            elif typeUser == 'tech':
                finalUser = TechPerson.objects.get(executiveUser=user)
                context = {'status':'Success','token':token.key,'username':username,'name':finalUser.name,'typeUser':typeUser}
            elif typeUser == 'admin':
                finalUser = User.objects.get(is_superuser=True,username=user)
                context = {'status':'Success','token':token.key,'username':username,'name':finalUser.username,'typeUser':typeUser}
        except Exception as e:
            context = {'status':'Failed','message':str(e)}
        return Response(context)
''' 

class RegisterUploadUser(APIView):
    def post(self,request):
        data = request.data
        username = data['username']
        name = data['name']
        password = data['password']
        try:
            user = User.objects.get(username=username)
            context = {'status':'Failed','message':'user already exists'}
        except User.DoesNotExist:
            user = User.objects.create_user(username=username,password=password) 
            uploaduser = UploadUser()
            uploaduser.name = name
            uploaduser.uploaduser = user
            joininig_date = datetime.datetime.now()
            uploaduser.jdate=joininig_date
            uploaduser.save()
            token,created = Token.objects.get_or_create(user=user)
            context = {'status':'Success','token':token.key,'username':username,'name':uploaduser.name,'typeUser':'uploaduser'}
        return Response(context)

class GetUserIpAddress(APIView):
    def get(self,request):
        me = self.request.user.salesexecutive
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')  
        me.ipAddress = ip
        me.save()
        context = {'status':'success'}
        return Response(context)