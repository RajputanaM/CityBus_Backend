from rest_framework import generics,status,viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response 
import json
import random
import smtplib
from email.mime.text import MIMEText
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt


# List all buses and create a new bus
class BusListCreateView(generics.ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

# Retrieve, update, or delete a specific bus
class BusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class TicketListByUserView(generics.ListAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id:
            return Ticket.objects.filter(user_id=user_id)
        return Ticket.objects.none()

# List all tickets and create a new ticket
class TicketListCreateView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    # Override the perform_create method to customize ticket creation
    def perform_create(self, serializer):
        # You can customize the behavior here if needed
        serializer.save()
# Retrieve, update, or delete a specific ticket
class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

# Custom view to search for buses from source to destination
class BusSearchView(generics.ListAPIView):
    serializer_class = BusSerializer

    def get_queryset(self):
        source_station = self.request.query_params.get('source_station')
        destination_station = self.request.query_params.get('destination_station')
        
        if source_station and destination_station:
            return Bus.objects.filter(
                source_station__name=source_station,
                destination_station__name=destination_station
            )
        return Bus.objects.all()

# List all bus stations and create a new bus station
class BusStationListCreateView(generics.ListCreateAPIView):
    queryset = BusStation.objects.all()
    serializer_class = BusStationSerializer
    
class UserListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

# Retrieve, update, or delete a specific bus station
class BusStationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BusStation.objects.all()
    serializer_class = BusStationSerializer
class search_buses(generics.ListAPIView):
    serializer_class = BusSerializer

    def get_queryset(self):
        source_station_name = self.request.query_params.get('source_station')
        destination_station_name = self.request.query_params.get('destination_station')
        
        queryset = Bus.objects.all()
        
        if source_station_name:
            queryset = queryset.filter(source_station__name=source_station_name)
        
        if destination_station_name:
            queryset = queryset.filter(destination_station__name=destination_station_name)
        
        return queryset


class UserProfileDetailView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'  # Use 'id' as the lookup field

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        # Parse the JSON data from the request
        data = json.loads(request.body.decode('utf-8'))

        email = data.get('email')
        password = data.get('password')

        if email and password:
            # Authenticate the user
            user = authenticate(request, username=email, password=password)

            if user is not None:
                # Log the user in
                login(request, user)
                return JsonResponse({'message': 'Login successful'},status=200)
            else:
                return JsonResponse({'message': 'Invalid email or password'}, status=401)
        else:
            return JsonResponse({'message': 'Email and password are required'}, status=400)

    return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def registration_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print("Received data:", data) 
        # name = name.get('name')
        email = data.get('email')
        mobile = data.get('mobile')
        password = data.get('password')
        
        # Generate and send OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        otp_record, created = OtpRecord.objects.get_or_create(email=email)
        otp_record.otp = otp
        otp_record.save()

        send_otp_to_user(email, otp)  # Custom function to send OTP via email      
        return JsonResponse({'message': 'OTP generated'}, status=200)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    
    
def send_otp_to_user(email, otp):
        # Send OTP via email
    message = f"Hello Dear,\n\n" \
                  f"Thank you for choosing CityBus! To complete your registration and secure your account, please use the following One-Time Password (OTP):\n\n" \
                  f"OTP: {otp}\n\n" \
                  f"This OTP will expire in [2 minutes], so please make sure to use it promptly. If you didn't request this OTP, please ignore this message.\n\n" \
                  f"For any assistance or questions, feel free to contact our support team by replying this message.\n\n" \
                  f"Best Regards,\n" \
                  f"CityBus"

    msg = MIMEText(message)
    msg['Subject'] = 'OTP for Login'
    msg['From'] = 'offcampushelp@gmail.com'
    msg['To'] = email

    # Replace these credentials with your actual SMTP server credentials
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login('offcampushelp@gmail.com', 'itxdzhieaaerqxrc')
    smtp_server.send_message(msg)
    smtp_server.quit()

@csrf_exempt
def verify_otp_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            user_otp = data.get('otp')
            password = data.get('password')
            name = data.get('name')
            mobile = data.get('mobile')
            
            print(mobile)
            print(password)
            
            print(request.session)
            # Fetch the actual OTP generated and sent
            actual_otp = get_stored_otp(email)
            print(actual_otp)
            if user_otp == actual_otp:  # Compare the user's OTP with the actual OTP
               
               Profile.objects.create(name=name, email=email, mobile=mobile, password=password)
               print("user tk aaya")
               user = User.objects.create_user(username=email, email=email, password=password)
               print("isme bhi aaya")
               user.save()
               return JsonResponse({'message': 'User registered successfully'}, status=200)
            else:
                print("invalid otp")
                return JsonResponse({'error': 'Invalid OTP.'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

def get_stored_otp(email):
    try:
        otp_record = OtpRecord.objects.get(email=email)
        return otp_record.otp
    except OtpRecord.DoesNotExist:
        return None
    
class GetUserByEmail(APIView):
    def get(self, request, email):
        try:
            user = Profile.objects.get(email=email)
            serializer = UserSerializer(user)  # Serialize the user object
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



class UserProfileUpdateView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        new_password = request.data.get('password')  # Assuming you send the new password in the request
        if new_password:
            user = User.objects.get(username=instance.email)
            user.set_password(new_password)
            user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    


@csrf_exempt
def verify_otp_view2(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            user_otp = data.get('otp')
            print(request.session)
            # Fetch the actual OTP generated and sent
            actual_otp = get_stored_otp(email)
            print(actual_otp)
            if user_otp == actual_otp:  # Compare the user's OTP with the actual OTP
               return JsonResponse({'message': 'OTP verified'}, status=200)
            else:
                print("invalid otp")
                return JsonResponse({'error': 'Invalid OTP.'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)



from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ChatRoomSerializer, MemberSerializer, MessageSerializer

class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        chat_room = self.get_object()
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(room=chat_room)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    lookup_field = 'room'
    @action(detail=True, methods=['post'])
    def add_message(self, request, pk=None):
        chat_room = self.get_object()
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(room=chat_room, sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def room_messages(self, request):
        room_id = request.query_params.get('room_id')
        if room_id is not None:
            chat_room = get_object_or_404(ChatRoom, id=room_id)
            messages = Message.objects.filter(room=chat_room)
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'room_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)



class MessageViewSet1(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(detail=False, methods=['get'])
    def messages_by_room(self, request, room_id=None):
        if room_id is not None:
            messages = Message.objects.filter(room__id=room_id)
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'room_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
