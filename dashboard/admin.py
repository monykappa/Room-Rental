# admin.py
from django.contrib import admin
from .models import *
from django import forms

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('ClientName', 'address', 'contact', 'remark')

@admin.register(HouseOwner)
class HouseOwnerAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ('display_price',)

    def display_price(self, obj):
        return str(obj)
    display_price.short_description = 'Parking Price'

@admin.register(Trash)
class TrashAdmin(admin.ModelAdmin):
    list_display = ('display_price',)

    def display_price(self, obj):
        return str(obj)
    display_price.short_description = 'Trash Price'


@admin.register(room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('HouseOwner', 'RoomNo', 'display_fee', 'status', 'remark')

    def display_fee(self, obj):
        return f'${obj.RoomFee:.0f}'

    display_fee.short_description = 'Room Fee'



@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ('ClientName', 'room_owner_name', 'RoomNo', 'RoomFee', 'date')

    def room_owner_name(self, obj):
        return obj.room.HouseOwner.name if obj.room.HouseOwner else ''
    
    room_owner_name.short_description = 'OwnerName'

    def RoomNo(self, obj):
        return obj.room.RoomNo if obj.room else ''

    def RoomFee(self, obj):
        return f'${obj.room.RoomFee:.0f}' if obj.room else ''

    def status(self, obj):
        return obj.room.status if obj.room else ''

    RoomNo.short_description = 'RoomNo'
    RoomFee.short_description = 'RoomFee'
    status.short_description = 'Status'





@admin.register(CheckOut)
class CheckOutAdmin(admin.ModelAdmin):
    list_display = ('ClientName', 'room_owner_name', 'RoomNo', 'date')
    search_fields = ['ClientName__name']

    def room_owner_name(self, obj):
        return obj.room.HouseOwner.name if obj.room.HouseOwner else ''

    room_owner_name.short_description = 'OwnerName'

    def RoomNo(self, obj):
        return obj.room.RoomNo if obj.room else ''

    def status(self, obj):
        return obj.room.status if obj.room else ''

    RoomNo.short_description = 'RoomNo'
    status.short_description = 'Status'
