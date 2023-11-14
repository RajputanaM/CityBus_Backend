from rest_framework import serializers
from .models import *

class BusStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStation
        fields = '__all__'
    


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class BusStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStation
        fields = '__all__'
    
class BusCountSerializer(serializers.Serializer):
    source_station = serializers.CharField()
    destination_station = serializers.CharField()
    bus_count = serializers.IntegerField()




class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
