from rest_framework.decorators import api_view

from .request_handlers import user_rh
from .request_handlers import building_rh
from .request_handlers import venue_rh
from .request_handlers import booking_rh
from .request_handlers import comment_rh


@api_view(['GET', 'POST'])
def login_using_credentials(request):
    return user_rh.UserRequestHandler().handle_login_request(request, user_rh.RequestTypes.LOGIN_USER_USING_CREDENTIALS)


@api_view(['GET', 'POST'])
def get_all_users(request):
    return user_rh.UserRequestHandler().handle_request(request, user_rh.RequestTypes.GET_ALL_USERS)


@api_view(['GET', 'POST'])
def get_user_details(request, email):
    return user_rh.UserRequestHandler().handle_request(request, user_rh.RequestTypes.GET_USER_DETAILS, {
        'email': email
    })


@api_view(['GET', 'POST'])
def get_users_by_search(request):
    return user_rh.UserRequestHandler().handle_request(request, user_rh.RequestTypes.GET_USERS_BY_SEARCH, {
        'name': request.GET.get('name', '')
    })


@api_view(['GET', 'POST'])
def add_new_user(request):
    return user_rh.UserRequestHandler().handle_request(request, user_rh.RequestTypes.ADD_NEW_USER)


@api_view(['GET', 'POST'])
def update_existing_user(request):
    return user_rh.UserRequestHandler().handle_request(request, user_rh.RequestTypes.UPDATE_EXISTING_USER)


@api_view(['GET', 'POST'])
def remove_existing_user(request):
    return user_rh.UserRequestHandler().handle_request(request, user_rh.RequestTypes.REMOVE_EXISTING_USER)


@api_view(['GET', 'POST'])
def get_all_buildings(request):
    return building_rh.BuildingRequestHandler().handle_request(request, building_rh.RequestTypes.GET_ALL_BUILDINGS)


@api_view(['GET', 'POST'])
def get_building_details(request, building_id):
    return building_rh.BuildingRequestHandler().handle_request(request, building_rh.RequestTypes.GET_BUILDING_DETAILS, {
        'id': building_id
    })


@api_view(['GET', 'POST'])
def get_building_by_search(request):
    return building_rh.BuildingRequestHandler().handle_request(request, building_rh.RequestTypes.GET_BUILDINGS_BY_SEARCH, {
        'name': request.GET.get('name', '')
    })


# @api_view(['GET', 'POST'])
# def add_new_building(request):
#     return building_rh.BuildingRequestHandler().handle_request(request, building_rh.RequestTypes.ADD_NEW_BUILDING)


@api_view(['GET', 'POST'])
def update_existing_building(request):
    return building_rh.BuildingRequestHandler().handle_request(request, building_rh.RequestTypes.UPDATE_EXISTING_BUILDING)


@api_view(['GET', 'POST'])
def remove_existing_building(request):
    return building_rh.BuildingRequestHandler().handle_request(request, building_rh.RequestTypes.REMOVE_EXISTING_BUILDING)


@api_view(['GET', 'POST'])
def get_all_venues(request):
    return venue_rh.VenueRequestHandler().handle_request(request, venue_rh.RequestTypes.GET_ALL_VENUES)


@api_view(['GET', 'POST'])
def get_venues_by_building(request, building_id):
    return venue_rh.VenueRequestHandler().handle_request(request, venue_rh.RequestTypes.GET_VENUES_BY_BUILDING, {
        'building_id': building_id
    })


@api_view(['GET', 'POST'])
def get_venues_by_authority(request, authority_id):
    return venue_rh.VenueRequestHandler().handle_request(request, venue_rh.RequestTypes.GET_VENUES_BY_AUTHORITY, {
        'authority_id': authority_id
    })


@api_view(['GET', 'POST'])
def get_venues_by_search(request):
    return venue_rh.VenueRequestHandler().handle_request(request, venue_rh.RequestTypes.GET_VENUES_BY_SEARCH, {
        'name': request.GET.get('name', '')
    })


@api_view(['GET', 'POST'])
def get_venue_details(request, venue_id):
    return venue_rh.VenueRequestHandler().handle_request(request, venue_rh.RequestTypes.GET_VENUE_DETAILS, {
        'venue_id': venue_id
    })


@api_view(['GET', 'POST'])
def add_new_venue(request):
    return venue_rh.VenueRequestHandler().handle_request(request, venue_rh.RequestTypes.ADD_NEW_VENUE)


@api_view(['GET', 'POST'])
def update_existing_venue(request):
    return venue_rh.VenueRequestHandler().handle_request(request, venue_rh.RequestTypes.UPDATE_EXISTING_VENUE)


@api_view(['GET', 'POST'])
def remove_existing_venue(request):
    return venue_rh.VenueRequestHandler().handle_request(request, venue_rh.RequestTypes.REMOVE_EXISTING_VENUE)


@api_view(['GET', 'POST'])
def get_bookings_by_user(request, user_id):
    return booking_rh.BookingRequestHandler().handle_request(request, booking_rh.RequestType.GET_BOOKINGS_BY_USER, {
        'user_id': user_id
    })


@api_view(['GET', 'POST'])
def get_bookings_by_venue(request, venue_id):
    return booking_rh.BookingRequestHandler().handle_request(request, booking_rh.RequestType.GET_BOOKINGS_BY_VENUE, {
        'venue_id': venue_id
    })


@api_view(['GET', 'POST'])
def get_booking_details(request, booking_id):
    return booking_rh.BookingRequestHandler().handle_request(request, booking_rh.RequestType.GET_BOOKING_DETAILS, {
        'booking_id': booking_id
    })


@api_view(['GET', 'POST'])
def get_venue_bookings_by_day(request, venue_id):
    return booking_rh.BookingRequestHandler().handle_request(request, booking_rh.RequestType.GET_VENUE_BOOKINGS_BY_DAY, {
        'venue_id': venue_id,
        'query_time': request.GET.get('query_time', '')
    })


@api_view(['GET', 'POST'])
def get_booking_requests_by_booking(request, booking_id):
    return booking_rh.BookingRequestHandler().handle_request(request, booking_rh.RequestType.GET_BOOKING_REQUESTS_BY_BOOKING, {
        'booking_id': booking_id
    })


@api_view(['GET', 'POST'])
def get_booking_requests_by_receiver(request, receiver_id):
    return booking_rh.BookingRequestHandler().handle_request(request, booking_rh.RequestType.GET_BOOKING_REQUESTS_BY_RECEIVER, {
        'receiver_id': receiver_id
    })


@api_view(['GET', 'POST'])
def get_booking_request(request, booking_request_id):
    return booking_rh.BookingRequestHandler().handle_request(request, booking_rh.RequestType.GET_BOOKING_REQUEST, {
        'booking_request_id': booking_request_id
    })


@api_view(['GET', 'POST'])
def add_new_booking(request):
    return booking_rh.BookingRequestHandler().handle_request(request, booking_rh.RequestType.ADD_NEW_BOOKING)


@api_view(['GET', 'POST'])
def update_booking_time(request):
    return booking_rh.BookingRequestHandler().handle_request(request, booking_rh.RequestType.UPDATE_BOOKING_TIME)


@api_view(['GET', 'POST'])
def update_booking(request):
    return booking_rh.BookingRequestHandler().handle_request(request, booking_rh.RequestType.UPDATE_BOOKING)


@api_view(['GET', 'POST'])
def cancel_booking(request):
    return booking_rh.BookingRequestHandler().handle_request(request, booking_rh.RequestType.CANCEL_BOOKING)


@api_view(['GET', 'POST'])
def update_booking_request(request):
    return booking_rh.BookingRequestHandler().handle_request(request, booking_rh.RequestType.UPDATE_BOOKING_REQUEST)


@api_view(['GET', 'POST'])
def get_comments_by_user(request, user_id):
    return comment_rh.CommentsRequestHandler().handle_request(request, comment_rh.RequestType.GET_COMMENTS_BY_USER, {
        'user_id': user_id
    })


@api_view(['GET', 'POST'])
def get_comments_by_booking(request, booking_id):
    return comment_rh.CommentsRequestHandler().handle_request(request, comment_rh.RequestType.GET_COMMENTS_BY_BOOKING, {
        'booking_id': booking_id
    })


# @api_view(['GET', 'POST'])
# def get_comment(request, comment_id):
#     return comment_rh.CommentsRequestHandler().handle_request(request, comment_rh.RequestType.GET_COMMENT, {
#         'comment_id': comment_id
#     })


@api_view(['GET', 'POST'])
def add_new_comment(request):
    return comment_rh.CommentsRequestHandler().handle_request(request, comment_rh.RequestType.ADD_NEW_COMMENT)
