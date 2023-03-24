"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from Pokemon import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import staticfiles

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('mainpage/', views.mainpage),
    path('resalepage/', views.resalepage),
    path('logout/', views.logout),
    path('signup/', views.signup),
    path('mypokemon/', views.mypokemon),
    path('boxhistory/', views.boxhistory),
    path('resalehistory/', views.resalehistory),
    path('buyonebox/', views.buyonebox),
    path('modifycard/', views.modifycard),
    path('buyonecard/', views.buyonecard),
    path('showpricetrend/', views.showpricetrend),
    path('checkbox/', views.checkbox),
    path('deleteboxhistory/', views.deleteboxhistory),
    path('pricecheck/', views.pricecheck),
    path('adminpage/', views.adminpage),
    path('adminsearch/', views.adminsearch),
    path('searchbox/', views.searchbox),
    path('checkmycard/', views.checkmycard),
    path('checkresalecard/', views.checkresalecard),
    path('checkavg/', views.checkavg),
    path('searchresalecard/', views.searchresalecard),
    path('searchcard/', views.searchcard),
    path('sendcard/', views.sendcard),
    path('dashboard/', views.dashboard),
    path('sendbonus/', views.sendbonus),
]

urlpatterns += staticfiles_urlpatterns()
