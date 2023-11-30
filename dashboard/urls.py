from django.urls import path
from django.shortcuts import render 
from . import views
from django.conf import settings 
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView



app_name = 'dashboard'
urlpatterns = [
    # dashboard
    path('base/', views.base, name='base'),
    path('dashboard/', views.dashboard, name='dashboard'),
    #room
    path('add-room/', views.add_room, name='add_room'),
    path('room_list/', views.room_list, name='room_list'),

    #house owner
    path('house_owner/', views.house_owner, name='house_owner'),
    path('house_owner/<int:pk>/edit/', views.HouseOwnerEditView.as_view(), name='house_owner_edit'),
    
    #client
    path('client/', views.client, name='client'),
    path('client/list/', views.ClientListView.as_view(), name='client-list-class-based'),
    path('client/<int:pk>/edit/', views.ClientEditView.as_view(), name='client-edit'),
    path('client/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client-delete'),
    #check-in
    path('CheckIn/', views.check_in, name='CheckIn'),
    path('CheckIn/form/', views.checkin_form, name='checkin_form'),
    #check-out
    path('checkout/', views.checkout_form_view, name='checkout_form_view'),
    path('CheckOut/', views.check_out, name='CheckOut'),


    #other fee
    path('other_fee/', views.other_fee, name='other_fee'),
    path('edit_trash/<int:trash_id>/', views.edit_trash, name='edit_trash'),
    path('edit_parking/<int:parking_id>/', views.edit_parking, name='edit_parking'),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
