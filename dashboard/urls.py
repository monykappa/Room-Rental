from django.urls import path
from django.shortcuts import render 
from . import views
from django.conf import settings 
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView



app_name = 'dashboard'
urlpatterns = [
    path('base/', views.base, name='base'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-room/', views.add_room, name='add_room'),
    path('room_list/', views.room_list, name='room_list'),
    path('client/', views.client, name='client'),
    path('client/list/', views.ClientListView.as_view(), name='client-list-class-based'),
    path('client/<int:pk>/edit/', views.ClientEditView.as_view(), name='client-edit'),
    path('client/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client-delete'),
    path('CheckIn/', views.check_in, name='CheckIn'),
    path('CheckIn/', views.check_in, name='check_in'),
    path('CheckOut/<int:checkin_id>/', views.checkout_view, name='CheckOut'),
    path('CheckIn/form/', views.checkin_form, name='checkin_form'),
    path('CheckOut/', views.check_out, name='CheckOut'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
