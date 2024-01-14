from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import *
from django.utils.html import format_html
from django.forms import inlineformset_factory
from django.forms import formset_factory
from datetime import datetime



class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['ClientName', 'sex', 'address', 'contact', 'remark']


class HouseOwnerForm(forms.ModelForm):
    class Meta:
        model = HouseOwner
        fields = ['name']
    
    

class RoomForm(forms.ModelForm):
    class Meta:
        model = room
        fields = ['RoomNo', 'HouseOwner', 'client_name', 'RoomFee', 'remark', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'custom-select'}),
        }

    client_name = forms.CharField(
        label='Client Name / ឈ្មោះអតិថិជន',
        widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'readonly': 'readonly'}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form'
        self.helper.label_class = 'font-weight-bold'
        self.helper.layout = Layout(
            Field('RoomNo', css_class='form-control mb-2', placeholder='Enter Room Number'),
            Field('HouseOwner', css_class='form-control mb-2', placeholder='Enter House Owner'),
            Field('RoomFee', css_class='form-control mb-2', placeholder='Enter Room Fee'),
            Field('remark', css_class='form-control mb-2', placeholder='Enter Remark'),
            Field('status', css_class='custom-select mb-2', placeholder='Select Status'),
            Field('ClientName', css_class='form-control mb-2', placeholder='Client Name'),
        )


class CheckInForm(forms.ModelForm):
    sex = forms.ChoiceField(choices=Person.SEX_CHOICES, required=False, label='Sex / ភេទ', initial='')

    class Meta:
        model = CheckIn
        fields = ['client_name', 'sex', 'client_address', 'client_contact', 'room', 'date']
        labels = {
            'client_name': 'Client name / ឈ្មោះអតិថិជន',
            'client_address': 'Client address / អាសយដ្ឋានអតិថិជន',
            'client_contact': 'Client contact / ទំនាក់ទំនងអតិថិជន',
            'room': 'Room / បន្ទប់',
            'date': 'Date / កាលបរិច្ឆេទ',
        }
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['room'].queryset = room.objects.filter(status=room.AVAILABLE)

            self.helper = FormHelper()
            self.helper.form_class = 'form'
            self.helper.label_class = 'font-weight-bold'
            self.helper.layout = Layout(
                Field('client_name', css_class='form-control mb-2'),
                Field('sex', css_class='form-control mb-2'),
                Field('client_address', css_class='form-control mb-2'),
                Field('client_contact', css_class='form-control mb-2'),
                Field('room', css_class='form-control mb-2'), 
                Field('date', css_class='form-control mb-2'),
            )
            
    def save(self, commit=True):
        instance = super(CheckInForm, self).save(commit=False)
        
        # Get the associated Client instance
        client_instance, created = Client.objects.get_or_create(ClientName=instance.client_name)
        
        # Update the 'sex' field in the Client instance
        client_instance.sex = self.cleaned_data.get('sex', None)
        client_instance.save()

        if commit:
            instance.save()
        return instance



class check_out_form(forms.ModelForm):
    class Meta:
        model = CheckOut
        fields = ['room', 'date']

    def __init__(self, *args, **kwargs):
        super(check_out_form, self).__init__(*args, **kwargs)
        self.fields['room'].queryset = room.objects.filter(status=room.IN_USE)

        self.helper = FormHelper()
        self.helper.form_class = 'form'
        self.helper.label_class = 'font-weight-bold'
        self.helper.layout = Layout(
            Field('room', css_class='form-control mb-2', data_url='/room-search/'),  # Add data_url for AJAX room search
            Field('date', css_class='form-control mb-2'),
        )



class MonthlyRentalFeeForm(forms.ModelForm):
    class Meta:
        model = MonthlyRentalFee
        fields = ['current_water', 'trash_fee', 'park_fee', 'date']

    def __init__(self, room, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['date'].initial = timezone.now().date()  # Set initial value to the current date
        self.room = room  # Store the room in the form

        # Set a default value for the trash_fee field
        self.fields['trash_fee'].initial = 1  # Change this value to your desired default

        # Set default value for the park_fee field
        last_month_fee = self.get_last_month_park_fee()
        self.fields['park_fee'].initial = int(last_month_fee) if int(last_month_fee) == last_month_fee else last_month_fee

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.room = self.room

        # Calculate water fee using the provided calculate_water_cost method
        instance.water_fee = instance.calculate_water_cost()

        if commit:
            instance.save()

            # Update or create Utilities
            utilities, created = Utilities.objects.get_or_create(room=self.room)
            utilities.previous_water = utilities.current_water
            utilities.current_water = instance.current_water
            utilities.save()

        return instance

    def get_current_water(self):
        # Retrieve current water from Utilities
        utilities = Utilities.objects.get(room=self.room)
        return utilities.current_water

    def get_last_month_park_fee(self):
        # Retrieve the park fee from the last month
        last_month_instance = MonthlyRentalFee.objects.filter(room=self.room).order_by('-date').first()
        return last_month_instance.park_fee if last_month_instance else 0


class MonthFilterForm(forms.Form):
    MONTH_CHOICES = [
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    ]

    YEAR_CHOICES = [(year, str(year)) for year in range(2023, datetime.now().year + 5)]

    selected_month = forms.ChoiceField(choices=MONTH_CHOICES, label='Select Month', required=False)
    selected_year = forms.ChoiceField(choices=YEAR_CHOICES, label='Select Year', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set initial values to the current month and year
        self.fields['selected_month'].initial = datetime.now().month
        self.fields['selected_year'].initial = datetime.now().year
        
        
class MonthYearForm(forms.Form):
    selected_month = forms.ChoiceField(choices=[(i, i) for i in range(1, 13)], label='Select Month')
    selected_year = forms.IntegerField(label='Enter Year')