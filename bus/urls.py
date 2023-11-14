from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('buses/', views.BusListCreateView.as_view(), name='bus-list-create'),
    path('buses/<int:pk>/', views.BusDetailView.as_view(), name='bus-detail'),

    # URLs for listing and creating tickets
    path('tickets/', views.TicketListCreateView.as_view(), name='ticket-list-create'),
    path('ticket/<int:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/<int:user_id>/', views.TicketListByUserView.as_view(), name='ticket-list-by-user'),

    # Custom URL for searching buses
    path('buses/search/', views.BusSearchView.as_view(), name='bus-search'),
    path('bus-stations/', views.BusStationListCreateView.as_view(), name='bus-station-list-create'),
    path('bus-stations/<int:pk>/', views.BusStationDetailView.as_view(), name='bus-station-detail'),
    path('search/', views.search_buses.as_view()),
    
    path('users/', views.UserListCreateView.as_view()),
    path('users/<str:email>/', views.UserProfileDetailView.as_view(), name='user-profile-detail'),

    path('login/', views.login_view),
    path('verifyOtp/',views.verify_otp_view),
    path('registration/',views.registration_view, name = 'registration'),
    
    path('userByEmail/<str:email>', views.GetUserByEmail.as_view()),
    path('updateuser/<str:email>', views.UserProfileUpdateView.as_view()),
    path('otpPassword/',views.verify_otp_view2),








    #chat room


    path('rooms/', views.ChatRoomViewSet.as_view({'get': 'list', 'post': 'create'}), name='chat-room-list'),
    path('chat-rooms/<int:pk>/', views.ChatRoomViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='chat-room-detail'),
    path('chat-rooms/<int:pk>/add-member/', views.ChatRoomViewSet.as_view({'post': 'add_member'}), name='chat-room-add-member'),

    # Member URLs
    path('members/', views.MemberViewSet.as_view({'get': 'list', 'post': 'create'}), name='member-list'),
    path('members/<int:pk>/', views.MemberViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='member-detail'),

    # Message URLs
    path('messages/', views.MessageViewSet.as_view({'get': 'list', 'post': 'create'}), name='message-list'),
    path('messages/<int:pk>/add-message/', views.MessageViewSet.as_view({'post': 'add_message'}), name='message-add-message'),
    path('messages/<int:room_id>/', views.MessageViewSet1.as_view({'get': 'messages_by_room'}), name='messages-by-room'),
]
