from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import *
from django.utils.html import format_html

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
        labels = {
            'client_name': 'Client name / ឈ្មោះអតិថិជន',
            'client_address': 'Client address / អាសយដ្ឋានអតិថិជន',
            'client_contact': 'Client contact / ទំនាក់ទំនងអតិថិជន',
            'room': 'Room / បន្ទប់',
            'parking': 'Parking / ទីតាំងដំឡូង',
            'trash': 'Trash / ធាតុសករាជ',
            'date': 'Date / កាលបរិច្ឆេទ',
            # Add labels for other fields as needed
        }

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



class check_out_form(forms.ModelForm):
    class Meta:
        model = CheckOut
        fields = ['room', 'date']

    def __init__(self, *args, **kwargs):
        super(check_out_form, self).__init__(*args, **kwargs)

        # Set the queryset for the 'room' field and order by status
        if 'instance' in kwargs and kwargs['instance']:
            # If the form is for an existing instance (edit mode), set the queryset based on the instance
            self.fields['room'].queryset = room.objects.filter(pk=kwargs['instance'].room.pk)
        else:
            # If the form is for a new instance (create mode), set the queryset for all rooms and order by status
            self.fields['room'].queryset = room.objects.all().order_by('status')

        # Add a class to the 'room' field widget based on the room status
        room_status = self.fields['room'].queryset.first().status if self.fields['room'].queryset.exists() else None
        if room_status == 'In-use/កំពុង​ប្រើ':
            self.fields['room'].widget.attrs['class'] = 'in-use-room'
        elif room_status == 'Available/ទំនេរ':
            self.fields['room'].widget.attrs['class'] = 'available-room'
