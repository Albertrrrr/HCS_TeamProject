"""HCS_TeamProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from portal.views import LoginView,SurveyView,FormDataSubmissionView,Quiz
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/index/', permanent=False)),
    path('admin/', admin.site.urls),
    path('index/', LoginView.as_view(), name='login'),
    path('form/<int:page>/', SurveyView.as_view(), name='form'),
    path('submit-form/', FormDataSubmissionView.as_view(), name='submit_form'),
    path('quiz/', Quiz.as_view(), name='quiz')

]
