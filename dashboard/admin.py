# admin.py
from django.contrib import admin
from .models import *
from django import forms
from django.utils.html import format_html
from django.db.models import OuterRef, Subquery
from django.db.models import Max, F, ExpressionWrapper, fields, Q


class ClientInline(admin.TabularInline):
    model = Client
    fields = ['ClientName', 'address', 'contact', 'remark']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('ClientName', 'address', 'contact', 'remark')
    search_fields = ('ClientName', 'contact')

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



from django.db.models import OuterRef, Subquery

@admin.register(room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('HouseOwner_colored', 'RoomNo_colored', 'display_fee', 'status_colored', 'remark_colored')
    actions = ['make_available', 'make_in_use']

    def display_fee(self, obj):
        return f'${obj.RoomFee:.0f}'

    display_fee.short_description = 'Room Fee / ថ្លៃបន្ទប់'

    def status_colored(self, obj):
        if obj.status == 'Available/ទំនេរ':
            color = 'green'
        elif obj.status == 'In-use/កំពុង​ប្រើ':
            color = 'red'
        else:
            color = 'black'  # You can customize the color for other statuses

        return format_html(
            '<span style="display: inline-block; width: 120px; text-align:center; background-color: {}; padding: 10px; color: white; border-radius: 5px;">{}</span>',
            color,
            obj.status,
        )

    status_colored.short_description = 'Status / ស្ថានភាព'

    def make_available(modeladmin, request, queryset):
        queryset.update(status='Available/ទំនេរ')

    def make_in_use(modeladmin, request, queryset):
        queryset.update(status='In-use/កំពុង​ប្រើ')

    make_available.short_description = 'Set selected rooms as Available/ទំនេរ'
    make_in_use.short_description = 'Set selected rooms as In-use/កំពុង​ប្រើ'

    def HouseOwner_colored(self, obj):
        # Replace 'HouseOwner' with the actual field name in your model
        return format_html(
            '<span style="display: inline-block; width: 130px; text-align:center;">{}</span>',
            obj.HouseOwner,
        )

    HouseOwner_colored.short_description = 'House Owner / ម្ចាស់ផ្ទះ'

    def RoomNo_colored(self, obj):
        # Replace 'RoomNo' with the actual field name in your model
        return format_html(
            '<span style="display: inline-block; width: 130px; text-align:center;">{}</span>',
            obj.RoomNo,
        )

    RoomNo_colored.short_description = 'Room Number / លេខបន្ទប់'

    def remark_colored(self, obj):
        # Replace 'remark' with the actual field name in your model
        return format_html(
            '<span style="display: inline-block; width: 130px; text-align:center;">{}</span>',
            obj.remark,
        )

    remark_colored.short_description = 'Remark / សំគាល់'









@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'room_owner_name', 'RoomNo', 'RoomFee', 'date')
    list_filter = ('room__status',)  # Adds a filter for room status

    def client_name(self, obj):
        return obj.client.ClientName if obj.client else ''
    
    client_name.short_description = 'Client Name'

    def room_owner_name(self, obj):
        return obj.room.HouseOwner.name if obj.room and obj.room.HouseOwner else ''
    
    room_owner_name.short_description = 'Owner Name'

    def RoomNo(self, obj):
        return obj.room.RoomNo if obj.room else ''

    def RoomFee(self, obj):
        return f'${obj.room.RoomFee:.0f}' if obj.room else ''

    def status(self, obj):
        return obj.room.status if obj.room else ''

    RoomNo.short_description = 'Room No'
    RoomFee.short_description = 'Room Fee'
    status.short_description = 'Status'

@admin.register(CheckOut)
class CheckOutAdmin(admin.ModelAdmin):
    list_display = ('ClientName', 'room_owner_name', 'RoomNo', 'date')
    search_fields = ['ClientName__name']

    def room_owner_name(self, obj):
        return obj.room.HouseOwner.name if obj.room and obj.room.HouseOwner else ''

    room_owner_name.short_description = 'Owner Name'

    def RoomNo(self, obj):
        return obj.room.RoomNo if obj.room else ''

    def status(self, obj):
        return obj.room.status if obj.room else ''

    RoomNo.short_description = 'Room No'
    status.short_description = 'Status'
