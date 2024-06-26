from django.db import models
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField
import uuid
from decimal import Decimal
from django.utils import timezone
import os
from dal import autocomplete
from datetime import datetime, date




def validate_file_extension(value): 
    ext = os.path.splitext(value.name)[1]  
    valid_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')


def images_directory_path(instance, filename):
    unique_id = str(uuid.uuid4())
    directory_path = f'content/{unique_id}/'
    return os.path.join(directory_path, filename)




class provinces(models.Model):
    PROVINCE_CHOICES = [
        ('Banteay Meanchey', 'Banteay Meanchey'),
        ('Battambang', 'Battambang'),
        ('Kampong Cham', 'Kampong Cham'),
        ('Kampong Chhnang', 'Kampong Chhnang'),
        ('Kampong Speu', 'Kampong Speu'),
        ('Kampong Thom', 'Kampong Thom'),
        ('Kampot', 'Kampot'),
        ('Kandal', 'Kandal'),
        ('Kep', 'Kep'),
        ('Koh Kong', 'Koh Kong'),
        ('Kratié', 'Kratié'),
        ('Mondulkiri', 'Mondulkiri'),
        ('Oddar Meanchey', 'Oddar Meanchey'),
        ('Pailin', 'Pailin'),
        ('Phnom Penh', 'Phnom Penh'),
        ('Preah Sihanouk', 'Preah Sihanouk'),
        ('Preah Vihear', 'Preah Vihear'),
        ('Pursat', 'Pursat'),
        ('Ratanakiri', 'Ratanakiri'),
        ('Siem Reap', 'Siem Reap'),
        ('Prey Veng', 'Prey Veng'),
        ('Stung Treng', 'Stung Treng'),
        ('Svay Rieng', 'Svay Rieng'),
        ('Takeo', 'Takeo'),
        ('Tbong Khmum', 'Tbong Khmum'),
    ]


class Person(models.Model):
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

class Client(models.Model):
    ClientName = models.CharField(max_length=200)
    sex = models.CharField(max_length=1, choices=Person.SEX_CHOICES, null=True, blank=True)
    address = models.CharField(max_length=500, choices=provinces.PROVINCE_CHOICES)
    contact = models.CharField(max_length=200)
    remark = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.ClientName

    def save(self, *args, **kwargs):
        super(Client, self).save(*args, **kwargs)
        # Update associated CheckIn entries
        self.checkin_set.update(client_name=self.ClientName)

        
    def update_checkin_entries(self):
        checkin_entries = CheckIn.objects.filter(client=self)
        checkin_entries.update(client_name=self.ClientName)




class parking(models.Model):
    ParkingPrice = models.DecimalField(max_digits=10, decimal_places=2)
    remark = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'${self.ParkingPrice}'


class Trash(models.Model):
    TrashPrice = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'${self.TrashPrice}'

class HouseOwner(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class room(models.Model):
    AVAILABLE = 'Available/ទំនេរ'
    IN_USE = 'In-use/កំពុង​ប្រើ'

    STATUS_CHOICES = [
        (AVAILABLE, 'Available/ទំនេរ'),
        (IN_USE, 'In-use/កំពុង​ប្រើ'),
    ]

    HouseOwner = models.ForeignKey(HouseOwner, on_delete=models.CASCADE)
    RoomNo = models.CharField(max_length=200)
    RoomFee = models.DecimalField(max_digits=10, decimal_places=2)
    remark = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AVAILABLE)

    def __str__(self):
        return f'Room/បន្ទប់លេខ: {self.RoomNo} - {self.HouseOwner.name} - {self.status}'


class CheckOut(models.Model):
    ClientName = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='checkouts')
    room = models.ForeignKey(room, on_delete=models.CASCADE, related_name='checkouts', null=True)
    date = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.room and hasattr(self.room, 'status'):
            self.room.status = 'Available/ទំនេរ'
            self.room.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.ClientName} - Checked out from Room: {self.room.RoomNo}' if self.room else f'{self.ClientName} - Checked out'



class CheckIn(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    client_name = models.CharField(max_length=200, null=True)
    client_address = models.CharField(max_length=500, choices=provinces.PROVINCE_CHOICES, null=True)
    client_contact = models.CharField(max_length=200, null=True)
    room = models.ForeignKey('room', on_delete=models.CASCADE, related_name='check_in_entries')
    date = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Create or get the client
        client, created = Client.objects.get_or_create(
            ClientName=self.client_name,
            address=self.client_address,
            contact=self.client_contact
        )

        # Update the client information in the CheckIn instance
        self.client_name = client.ClientName
        self.client_address = client.address
        self.client_contact = client.contact

        # Save the room status and other changes
        self.room.status = 'In-use/កំពុង​ប្រើ'
        self.room.save()
        self.client = client

        super().save(*args, **kwargs)
    
    def has_checked_out(self):
        return self.client.checkouts.exists() 
    
    def __str__(self):
        return f'{self.client_name} - Room: {self.room.RoomNo} - Fee: ${self.room.RoomFee}'

    


class WaterRate(models.Model):
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.rate}'

class Utilities(models.Model):
    room = models.OneToOneField('room', on_delete=models.CASCADE, related_name='utilities')
    previous_water = models.PositiveIntegerField(default=0)
    current_water = models.PositiveIntegerField(default=0)
    water_rate = models.ForeignKey(WaterRate, on_delete=models.SET_NULL, null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'Utilities for {self.room}'

class WaterUsage(models.Model):
    room = models.ForeignKey('room', on_delete=models.CASCADE, related_name='water_usage')
    house_owner = models.ForeignKey(HouseOwner, on_delete=models.CASCADE)
    water_quantity = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'Water Usage for Room {self.room.RoomNo} - {self.date}'

class MonthlyRentalFee(models.Model):
    room = models.ForeignKey('room', on_delete=models.CASCADE, related_name='monthly_fees')
    date = models.DateField(default=timezone.now)
    water_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_water = models.PositiveIntegerField(null=True, blank=True)
    previous_water = models.PositiveIntegerField(default=0)  # New field for tracking previous water usage
    trash_fee = models.DecimalField(max_digits=10, decimal_places=2)
    park_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def calculate_water_cost(self):
        # Ensure self.room.utilities.water_rate.rate is not None
        if self.room.utilities.water_rate and self.room.utilities.water_rate.rate is not None:
            water_quantity_difference = self.current_water - self.previous_water
            return water_quantity_difference * self.room.utilities.water_rate.rate
        else:
            # Handle the case when water_rate or its rate is None
            return 0 
    
    def calculate_total(self):
        # Ensure none of the values are None before performing the addition
        room_fee = self.room.RoomFee if self.room.RoomFee is not None else 0
        water_fee = self.water_fee if self.water_fee is not None else 0
        trash_fee = self.trash_fee if self.trash_fee is not None else 0
        self.trash_fee = trash_fee
        park_fee = self.park_fee if self.park_fee is not None else 0
        self.park_fee = park_fee

        return room_fee + water_fee + trash_fee + park_fee

    def save(self, *args, **kwargs):
        if not self.id:
            self.previous_water = self.current_water

        utilities, created = Utilities.objects.get_or_create(room=self.room)
        utilities.previous_water = utilities.current_water
        utilities.current_water = self.current_water
        self.previous_water = utilities.previous_water

        self.water_fee = self.calculate_water_cost()
        self.total = self.calculate_total()

        utilities.save()

        if isinstance(utilities.date, datetime):
            utilities.date = utilities.date.date()
        elif isinstance(utilities.date, date):
            pass

        if self.date > utilities.date:
            utilities.date = self.date
            utilities.save()



        water_quantity = self.current_water if self.current_water is not None else 0
        water_usage = WaterUsage.objects.create(
            room=self.room,
            house_owner=self.room.HouseOwner,
            water_quantity=water_quantity,
            date=self.date
        )

        water_usage.save()

        super().save(*args, **kwargs)




# class utilities(models.Model):
#     room = models.ForeignKey(room, on_delete=models.CASCADE, related_name='utilities')
#     previous_water = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))
#     current_water = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     other_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     remark = models.CharField(max_length=200, null=True, blank=True)

#     def __str__(self):
#         return f'Room {self.room.RoomNo}, Previous Water: {self.current_water} m³'


# class WaterUsageHistory(models.Model):
#     utilities = models.ForeignKey(utilities, on_delete=models.CASCADE, related_name='water_usage_history')
#     previous_water = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))
#     date = models.DateTimeField(auto_now_add=True)

# class MonthlyRentalFee(models.Model):
#     utilities = models.ForeignKey(utilities, on_delete=models.CASCADE)
#     current_water = models.DecimalField(max_digits=10, decimal_places=2)
#     parking = models.ForeignKey(parking, on_delete=models.CASCADE)
#     trash = models.ForeignKey(Trash, on_delete=models.CASCADE)
#     sub_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
#     water_fee = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True)
#     water_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.5)
#     date = models.DateTimeField(auto_now_add=True, null=True)  

#     def save(self, *args, **kwargs):
#         # Fetch the latest WaterUsageHistory entry for the same utilities
#         previous_water_entry = WaterUsageHistory.objects.filter(
#             utilities=self.utilities
#         ).order_by('-date').first()

#         if previous_water_entry:
#             # Use previous_water from WaterUsageHistory
#             previous_water = previous_water_entry.previous_water
#         else:
#             # Use the initial value if no previous_water_entry
#             previous_water = Decimal('0')

#         # Calculate the difference between current and previous water
#         water_difference = Decimal(str(self.current_water)) - self.utilities.previous_water



#         # Use the water_rate from the MonthlyRentalFee model
#         water_rate = self.water_rate
#         water_fee = max(0, water_difference) * water_rate  # Calculate water_fee, ensuring it's not negative

#         # Update the attribute to water_fee
#         self.water_fee = water_fee

#         # Update the utilities model's previous_water and current_water
#         if self.utilities:
#             self.utilities.previous_water = self.current_water
#             self.utilities.current_water = self.current_water
#             self.utilities.save()

#             # Create a new WaterUsageHistory record
#             WaterUsageHistory.objects.create(utilities=self.utilities, previous_water=self.current_water)

#         # Calculate sub_total based on the positive difference between current_water and previous_water
#         if self.utilities:
#             # Assuming the rate for other fees is 1, you can adjust it accordingly
#             self.sub_total = self.water_fee + Decimal(str(self.trash.TrashPrice)) + Decimal(str(self.parking.ParkingPrice))

#         super().save(*args, **kwargs)


# class Invoice(models.Model):
#     monthly_rental_fee = models.ForeignKey(MonthlyRentalFee, on_delete=models.CASCADE)
#     invoice_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     issue_date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"Invoice for {self.monthly_rental_fee.utilities.room.RoomNo} - {self.issue_date}"