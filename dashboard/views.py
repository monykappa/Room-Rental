from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User 
from django.contrib.auth import logout
from .models import *
from django.utils import timezone
from django.contrib.auth.views import LogoutView
from django.db.models import Q
from decimal import Decimal
from django.views.generic import ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from .forms import *
from .models import CheckIn as CheckInModel
from django.urls import reverse
from django.db.models import Max
from datetime import timedelta



def base(request):
    template = 'base.html'  
    return render(request, template)

def dashboard(request):
    template = 'dashboard/dashboard.html'
    return render(request, template)

def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('dashboard:room_list'))  # Use the correct name here
        else:
            # Handle form errors if needed
            pass
    else:
        form = RoomForm()

    house_owners = HouseOwner.objects.all()
    return render(request, 'dashboard/add_room.html', {'house_owners': house_owners, 'form': form})

def room_list(request):
    rooms = room.objects.annotate(latest_checkin=Max('check_in_entries__date')).order_by('-latest_checkin')
    house_owners = HouseOwner.objects.all()
    return render(request, 'dashboard/room_list.html', {'rooms': rooms, 'house_owners': house_owners})


def client(request):
    clients = Client.objects.all()
    return render(request, 'dashboard/client.html', {'clients': clients})

class ClientListView(ListView):
    model = Client
    template_name = 'dashboard/client.html'
    context_object_name = 'clients'

class ClientEditView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'dashboard/client_edit_form.html'
    success_url = reverse_lazy('dashboard:client-list-class-based')
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object, form=self.get_form())
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'dashboard/client_confirm_delete.html'
    success_url = reverse_lazy('dashboard:client-list-class-based')

def check_in(request):
    check_ins = CheckInModel.objects.all()
    return render(request, 'dashboard/check_in.html', {'CheckIn': check_ins})


def checkin_form(request):
    if request.method == 'POST':
        form = CheckInForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the check-in list page or any other page
            return redirect('checkin_list')
    else:
        form = CheckInForm()

    return render(request, 'dashboard/checkin_form.html', {'form': form})

def check_out(request):
    check_outs = CheckOut.objects.all()

    for checkout in check_outs:
        try:
            checkin = CheckIn.objects.get(client_name=checkout.ClientName.ClientName)
            checkout.total_stay = (checkout.date - checkin.date).days
            checkout.checkin_date = checkin.date
        except CheckIn.DoesNotExist:
            checkout.total_stay = None
            checkout.checkin_date = None

    return render(request, 'dashboard/check_out.html', {'CheckOut': check_outs})