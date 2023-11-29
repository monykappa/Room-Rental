from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import *

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['ClientName', 'address', 'contact', 'remark']

class RoomForm(forms.ModelForm):
    class Meta:
        model = room
        fields = ['RoomNo', 'HouseOwner', 'RoomFee', 'remark', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'custom-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form'
        self.helper.label_class = 'font-weight-bold'
        self.helper.layout = Layout(
            Field('RoomNo', css_class='form-control mb-2'),
            Field('HouseOwner', css_class='form-control mb-2'),
            Field('RoomFee', css_class='form-control mb-2'),
            Field('remark', css_class='form-control mb-2'),
            Field('status', css_class='custom-select mb-2'),
        )

class CheckInForm(forms.ModelForm):
    class Meta:
        model = CheckIn
        fields = ['client_name', 'client_address', 'client_contact', 'room', 'parking', 'trash', 'date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form'
        self.helper.label_class = 'font-weight-bold'
        self.helper.layout = Layout(
            Field('client_name', css_class='form-control mb-2'),
            Field('client_address', css_class='form-control mb-2'),
            Field('client_contact', css_class='form-control mb-2'),
            Field('room', css_class='form-control mb-2'),
            Field('parking', css_class='form-control mb-2'),
            Field('trash', css_class='form-control mb-2'),
            Field('date', css_class='form-control mb-2'),
        )