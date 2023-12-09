from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import *
from django.utils.html import format_html
from django.forms import inlineformset_factory
from django.forms import formset_factory



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
    class Meta:
        model = CheckIn
        fields = ['client_name', 'client_address', 'client_contact', 'room', 'date']
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
            Field('client_address', css_class='form-control mb-2'),
            Field('client_contact', css_class='form-control mb-2'),
            Field('room', css_class='form-control mb-2'), 
            Field('date', css_class='form-control mb-2'),
        )


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
