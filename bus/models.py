
from django.db import models

class BusStation(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
   
class Bus(models.Model):
    source_station = models.ForeignKey(BusStation, related_name='source_buses', on_delete=models.CASCADE)
    destination_station = models.ForeignKey(BusStation, related_name='destination_buses', on_delete=models.CASCADE)
    bus_number = models.CharField(max_length=10)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    price_per_ticket = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.bus_number} - {self.source_station} to {self.destination_station}"


class Profile(models.Model):
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    number_of_tickets = models.PositiveIntegerField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date_time = models.DateTimeField(auto_now_add=True)
    bus_arrival_time = models.TimeField()
    bus_departure_time = models.TimeField()
    source_station = models.CharField(max_length=255)
    destination_station = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Ticket for {self.bus.bus_number} - {self.booking_date_time}"
        
class OtpRecord(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)




class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name



class Member(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    join_time = models.DateTimeField(auto_now_add=True)




class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

