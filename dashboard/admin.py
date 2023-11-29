# admin.py
from django.contrib import admin
from .models import *
from django import forms
from django.utils.html import format_html
from django.db.models import OuterRef, Subquery
from django.db.models import Max, F, ExpressionWrapper, fields, Q
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta



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





@admin.register(room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('display_HouseOwner', 'display_RoomNo', 'display_fee', 'status_colored', 'display_remark', 'get_client_name')
    actions = ['make_available', 'make_in_use']
    list_filter = ('status',)

    def display_remark(self, obj):
        return f'{obj.remark}' if obj.remark else ''
    display_remark.short_description = 'Remark / ចំណាំ'

    def display_HouseOwner(self, obj):
        return f'{obj.HouseOwner.name}' if obj.HouseOwner else ''
    display_HouseOwner.short_description = 'House Owner / ម្ចាស់ផ្ទះ'

    def display_RoomNo(self, obj):
        return f'{obj.RoomNo}' if obj.RoomNo else ''
    display_RoomNo.short_description = 'Room Number / លេខបន្ទប់'


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

    def get_client_name(self, obj):
        if obj.status == 'In-use/កំពុង​ប្រើ' and obj.check_in_entries.exists():
            return obj.check_in_entries.last().client_name
        return ''

    get_client_name.short_description = 'Client Name / ឈ្មោះអតិថិជន'




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


class MonthlyRentalFeeForm(forms.ModelForm):
    room_status = forms.CharField(label='Room Status', required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = MonthlyRentalFee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            # Attempt to get the room status
            room_status = self.instance.room.status
        except ObjectDoesNotExist:
            # If room is not associated, set room status to 'N/A'
            room_status = 'N/A'

        self.fields['room_status'].initial = room_status

@admin.register(utilities)
class UtilitiesAdmin(admin.ModelAdmin):
    list_display = ('room', 'get_previous_water', 'other_fee', 'remark')

    def get_previous_water(self, obj):
        return f'{obj.current_water} m³'

    get_previous_water.short_description = 'Previous Water'

@admin.register(WaterUsageHistory)
class WaterUsageHistoryAdmin(admin.ModelAdmin):
    list_display = ('utilities_room', 'formatted_previous_water', 'date')
    list_filter = ('utilities__room__HouseOwner',)

    def utilities_room(self, obj):
        return f'Room {obj.utilities.room.RoomNo}' if obj.utilities and obj.utilities.room else ''

    utilities_room.short_description = 'Utilities Room'

    def formatted_previous_water(self, obj):
        return f'{obj.previous_water} m³'

    formatted_previous_water.short_description = 'Previous Water'

    

@admin.register(MonthlyRentalFee)
class MonthlyRentalFeeAdmin(admin.ModelAdmin):
    list_display = (
        'checkin_client_name',
        'room_no',
        'house_owner',
        'formatted_previous_water',
        'formatted_current_water',
        'formatted_water_fee',
        'formatted_trash_price',
        'formatted_parking_fee',
        'formatted_room_fee',
        'formatted_sub_total',
        'date',
    )

    list_filter = ('checkin__room__HouseOwner',)

    def checkin_client_name(self, obj):
        return obj.checkin.client_name if obj.checkin else ''
    
    checkin_client_name.short_description = 'CheckIn Client Name'

    def room_no(self, obj):
        return obj.checkin.room.RoomNo if obj.checkin and obj.checkin.room else ''
    
    room_no.short_description = 'RoomNo'

    def room_status(self, obj):
        return obj.checkin.room.status if obj.checkin and obj.checkin.room else ''
    
    room_status.short_description = 'Room Status'


    def house_owner(self, obj):
        return obj.checkin.room.HouseOwner.name if obj.checkin and obj.checkin.room and obj.checkin.room.HouseOwner else ''
    
    house_owner.short_description = 'HouseOwner'

    def formatted_previous_water(self, obj):
        if obj.utilities:
            # Fetch the MonthlyRentalFee entry for the month before the current MonthlyRentalFee entry
            previous_month_entry = MonthlyRentalFee.objects.filter(
                utilities=obj.utilities,
                date__lt=obj.date
            ).order_by('-date').first()

            if previous_month_entry:
                return format_html('{} m³', int(float(previous_month_entry.current_water)) if float(previous_month_entry.current_water).is_integer() else float(previous_month_entry.current_water))
            else:
                # If there's no history, display 0 m³
                return format_html('{} m³', 0)

        return format_html('{} m³', 0)



    formatted_previous_water.short_description = 'Previous Water'

    def formatted_current_water(self, obj):
        current_water = obj.current_water
        return format_html('{} m³', int(float(current_water)) if float(current_water).is_integer() else float(current_water))
    
    formatted_current_water.short_description = 'Current Water'

    def formatted_water_fee(self, obj):
        if obj.utilities:
            water_fee = (obj.current_water - obj.utilities.previous_water) * Decimal('0.5')
            return format_html('${}', '{:.0f}'.format(water_fee))
        return ''

    formatted_water_fee.short_description = 'Water Fee'

    def formatted_trash_price(self, obj):
        return format_html('${}', int(float(obj.trash.TrashPrice)) if float(obj.trash.TrashPrice).is_integer() else float(obj.trash.TrashPrice)) if obj.trash else ''
    
    formatted_trash_price.short_description = 'Trash Price'

    def formatted_parking_fee(self, obj):
        return format_html('${}', int(float(obj.parking.ParkingPrice)) if float(obj.parking.ParkingPrice).is_integer() else float(obj.parking.ParkingPrice)) if obj.parking else ''
    
    formatted_parking_fee.short_description = 'Parking Fee'

    def formatted_room_fee(self, obj):
        return format_html('${}', int(float(obj.checkin.room.RoomFee)) if float(obj.checkin.room.RoomFee).is_integer() else float(obj.checkin.room.RoomFee)) if obj.checkin and obj.checkin.room and obj.checkin.room.RoomFee else ''
    
    formatted_room_fee.short_description = 'Room Fee'

    def formatted_sub_total(self, obj):
        total_fee = obj.sub_total
        return format_html('${}', int(float(total_fee)) if float(total_fee).is_integer() else float(total_fee))
    
    formatted_sub_total.short_description = 'Sub Total'
