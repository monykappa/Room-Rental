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
from django.http import HttpResponse
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist



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
            return redirect('dashboard:CheckIn')
    else:
        form = CheckInForm()

    return render(request, 'dashboard/checkin_form.html', {'form': form})


def checkout_view(request, checkin_id):
    checkin = get_object_or_404(CheckIn, pk=checkin_id)

    # Create a CheckOut entry
    CheckOut.objects.create(ClientName=checkin.client, room=checkin.room)

    # Update room status
    checkin.room.status = 'Available/ទំនេរ'
    checkin.room.save()

    return redirect('dashboard:check_in') 


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


def checkout_form_view(request):
    if request.method == 'POST':
        form = check_out_form(request.POST)
        if form.is_valid():
            checkout_instance = form.save(commit=False)
            
            # Update the room status and save the checkout entry
            checkout_instance.room.status = 'Available/ទំនេរ'
            checkout_instance.room.save()
            
            # Automatically get the associated client of the selected room during check-in
            checkin_entry = checkout_instance.room.check_in_entries.last()
            
            if checkin_entry and hasattr(checkin_entry, 'client_name'):
                client_name = checkin_entry.client_name
                # Assuming 'Client' has a field 'ClientName', modify if needed
                client_instance, created = Client.objects.get_or_create(ClientName=client_name)
                checkout_instance.ClientName = client_instance

            checkout_instance.save()
            return redirect('dashboard:CheckOut')
    else:
        form = check_out_form()

    return render(request, 'dashboard/checkout_form.html', {'form': form})


def other_fee(request):
    trashes = Trash.objects.all()
    parkings = parking.objects.all()

    return render(request, 'dashboard/other_fee.html', {'trashes': trashes, 'parkings': parkings})


def edit_trash(request, trash_id):
    trash_instance = get_object_or_404(Trash, id=trash_id)
    success_message = None

    if request.method == 'POST':
        new_price = request.POST.get('new_price')
        trash_instance.TrashPrice = new_price
        trash_instance.save()
        success_message = "Trash price updated successfully"

        # Redirect to the same page to fetch the updated data
        return redirect('dashboard:other_fee')

    return render(request, 'dashboard/other_fee.html', {'success_message': success_message})

def edit_parking(request, parking_id):
    parking_instance = get_object_or_404(parking, id=parking_id)
    success_message = None

    if request.method == 'POST':
        new_price = request.POST.get('new_price')
        parking_instance.ParkingPrice = new_price
        parking_instance.save()
        success_message = "Parking price updated successfully"

        # Redirect to the same page to fetch the updated data
        return redirect('dashboard:other_fee')

    return render(request, 'dashboard/other_fee.html', {'success_message': success_message})