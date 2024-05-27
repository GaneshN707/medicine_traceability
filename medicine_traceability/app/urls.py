
from django.contrib import admin
from django.urls import path,re_path
from  app import views
from django.conf.urls import handler404
from django.shortcuts import render

urlpatterns = [
    path('', views.index, name='index'),
    path('registration/<str:user_type>', views.registration , name='registration'),
    path('log_in', views.log_in , name='log_in'),
    path('sidebar', views.sidebar , name='sidebar'),
    path('admedicine', views.admedicine , name='admedicine'),
    path('scaned_qr/<str:qr_value>/', views.scaned_qr, name='scaned_qr'),
    path('scan_qr/', views.scan_qr, name='scan_qr'),
    path('tracemedicine/', views.tracemedicine, name='tracemedicine'),
    path('trace_qr/<str:qr_value>/', views.trace_qr, name='trace_qr'),
    path('Show_data', views.Show_data , name='Show_data'),
    path('log_out', views.log_out , name='log_out'),
    # re_path(r'^.*\.*', views.pages, name='pages'),

]

