"""bodhiteam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sales/',include('sales.urls',namespace='sales')),
    path('api/sales/',include('sales.api.urls')),
    path('',include('membership.urls')),
    path('api/membership/',include('membership.api.urls')),
    path('tech/',include('tech.urls',namespace='tech')),
    path('api/tech/',include('tech.api.urls')),
    # path('crm/',include('crm.urls',namespace='crm')),
    path('api/crm/',include('crm.api.urls')),
    path('silk/',include('silk.urls',namespace='silk'))   
]

