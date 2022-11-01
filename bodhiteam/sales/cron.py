from  .models import *
import datetime

def my_scheduled_job():
    #lead = Lead.objects.get(id=9)
    #data=SuccessfullyLead.objects.create(by=request.user.salesexecutive,lead=lead,priceQuoted=10000,extra_requirement=None,datetime=datetime.datetime.now())
    
    temp = Notification.objects.all()
        for i in temp:
            i.is_FirstTime = False
            i.save()
