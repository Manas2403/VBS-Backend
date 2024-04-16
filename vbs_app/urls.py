from django.urls import path

from vbs_app.request_handlers.building_rh import AddNewBuildingAPIView, UpdateNewBuildingAPIView
from . import views

urlpatterns = [
    path('users/login/', views.login_using_credentials),
    path('users/details/all/', views.get_all_users),
    path('users/details/<str:email>/', views.get_user_details),
    path('users/search/', views.get_users_by_search),
    path('users/add/', views.add_new_user),
    path('users/update/', views.update_existing_user),
    path('users/remove/', views.remove_existing_user),

    path('buildings/details/all/', views.get_all_buildings),
    path('buildings/details/<str:building_id>/', views.get_building_details),
    path('buildings/search/', views.get_building_by_search),
    path('buildings/add/', AddNewBuildingAPIView.as_view(),  name='add-buildings'),
    path('buildings/update/', UpdateNewBuildingAPIView.as_view(),name='update-buildings'),
    path('buildings/remove/', views.remove_existing_building),

    path('venues/details/all/', views.get_all_venues),
    path('venues/details/byBuilding/<str:building_id>/', views.get_venues_by_building),
    path('venues/details/byAuthority/<str:authority_id>/', views.get_venues_by_authority),
    path('venues/details/<str:venue_id>/', views.get_venue_details),
    path('venues/search/', views.get_venues_by_search),
    path('venues/add/', views.add_new_venue),
    path('venues/update/', views.update_existing_venue),
    path('venues/remove/', views.remove_existing_venue),

    path('bookings/details/byUser/<str:user_id>/', views.get_bookings_by_user),
    path('bookings/details/byVenue/<str:venue_id>/', views.get_bookings_by_venue),
    path('bookings/details/byVenue/<str:venue_id>/byDay/', views.get_venue_bookings_by_day),
    path('bookings/details/<str:booking_id>/', views.get_booking_details),
    path('bookings/bookingRequests/byBooking/<str:booking_id>/', views.get_booking_requests_by_booking),
    path('bookings/bookingRequests/byReceiver/<str:receiver_id>/', views.get_booking_requests_by_receiver),
    path('bookings/bookingRequests/details/<str:booking_request_id>/', views.get_booking_request),
    path('bookings/add/', views.add_new_booking),
    path('bookings/update/time/', views.update_booking_time),
    path('bookings/update/details/', views.update_booking),
    path('bookings/cancel/', views.cancel_booking),
    path('bookings/bookingRequests/update/', views.update_booking_request),

    path('comments/byUser/<str:user_id>/', views.get_comments_by_user),
    path('comments/byBooking/<str:booking_id>/', views.get_comments_by_booking),
    path('comments/<str:comment_id>/', views.get_comment),
    path('comments/add/', views.add_new_comment),
]
