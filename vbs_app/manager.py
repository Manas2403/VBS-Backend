from datetime import datetime, timedelta

from .models import Building, User, Venue, Booking, BookingRequest, Comments


def check_user_exists(user_id):
    return User.objects.filter(email=user_id).exists()


def get_user_by_id(email):
    return User.objects.get(email=email)


def get_all_users():
    return User.objects.all().order_by('name')


def get_users_by_name(name):
    return User.objects.filter(name__contains=name).order_by('name')


def add_new_user(email, name, parent, require_parent_permission, is_admin, is_authority):
    user = User(
        email=email,
        name=name,
        parent=parent,
        require_parent_permission=require_parent_permission,
        is_admin=is_admin,
        is_authority=is_authority
    )
    user.save()
    return user


def update_user(user, name, parent, require_parent_permission, is_admin, is_authority):
    if name is not None:
        user.name = name
    if parent is not None:
        user.parent = parent
    if require_parent_permission is not None:
        user.require_parent_permission = require_parent_permission
    if is_admin is None:
        user.is_admin = is_admin
    if is_authority is not None:
        user.is_authority = is_authority
    user.save()
    return user


def delete_user(email):
    user = get_user_by_id(email)
    user.delete()


def check_building_exists(building_id):
    return Building.objects.filter(id=building_id).exists()


def get_building_by_id(building_id):
    return Building.objects.get(id=building_id)


def get_all_buildings():
    return Building.objects.all().order_by('name')


def get_buildings_by_name(name):
    return Building.objects.filter(name__contains=name).order_by('name')


def add_building(name):
    building = Building(name=name)
    building.save()
    return building


def update_building(building, name):
    building.name = name
    building.save()
    return building


def delete_building(building_id):
    building = get_building_by_id(building_id)
    building.delete()


def check_venue_exists(venue_id):
    return Venue.objects.filter(id=venue_id).exists()


def get_venue_by_id(venue_id):
    return Venue.objects.get(id=venue_id)


def get_venue_by_building(building_id):
    return Venue.objects.filter(building_id=building_id).order_by('name')


def get_venue_by_authority(authority_id):
    return Venue.objects.filter(authority_id=authority_id).order_by('name')


def get_venue_by_name(name):
    return Venue.objects.filter(name__contains=name)


def get_all_venues():
    return Venue.objects.all()


def add_venue(name, building_id, floor_number, venue_type, is_accessible, seating_capacity, has_air_conditioner,
              has_projectors, has_speakers, has_whiteboard, authority_id):
    venue = Venue(
        name=name,
        building_id=get_building_by_id(building_id),
        venue_type=venue_type,
        floor_number=floor_number,
        is_accessible=is_accessible,
        seating_capacity=seating_capacity,
        has_air_conditioner=has_air_conditioner,
        has_projectors=has_projectors,
        has_speakers=has_speakers,
        has_whiteboard=has_whiteboard,
        authority_id=get_user_by_id(authority_id)
    )
    venue.save()
    return venue


def update_venue(venue, name, building_id, floor_number, venue_type, is_accessible, seating_capacity, has_air_conditioner,
                 has_projectors, has_speakers, has_whiteboard, authority_id):
    if name is not None:
        venue.name = name
    if building_id is not None:
        venue.building_id = get_building_by_id(building_id)
    if floor_number is not None:
        venue.floor_number = floor_number
    if venue_type is not None:
        venue.venue_type = venue_type
    if is_accessible is not None:
        venue.is_accessible = is_accessible
    if seating_capacity is not None:
        venue.seating_capacity = seating_capacity
    if has_air_conditioner is not None:
        venue.has_air_conditioner = has_air_conditioner
    if has_projectors is not None:
        venue.has_projectors = has_projectors
    if has_speakers is not None:
        venue.has_speakers = has_speakers
    if has_whiteboard is not None:
        venue.has_whiteboard = has_whiteboard
    if authority_id is not None:
        venue.authority_id = get_user_by_id(authority_id)
    venue.save()
    return venue


def delete_venue(venue_id):
    venue = get_venue_by_id(venue_id)
    venue.delete()


def get_authority_by_venue(venue_id):
    return get_venue_by_id(venue_id).authority_id


def check_booking_exists(booking_id):
    return Booking.objects.filter(id=booking_id).exists()


def get_booking_by_id(booking_id):
    return Booking.objects.get(id=booking_id)


def get_booking_by_user(user_id):
    return Booking.objects.filter(user_id=user_id).order_by('booking_time')


def get_booking_by_venue(venue_id):
    return Booking.objects.filter(venue_id=venue_id).order_by('event_time')


def get_approved_bookings_by_venue(venue_id, event_time):
    bookings = get_booking_by_venue(venue_id)
    start_time = datetime(year=event_time.year, month=event_time.month, day=event_time.day)
    end_time = start_time + timedelta(days=1)
    return bookings.filter(booking_status=Booking.BookingStatus.APPROVED, event_time__range=(start_time, end_time))


def get_pending_bookings_by_venue(venue_id, event_time):
    bookings = get_booking_by_venue(venue_id)
    start_time = datetime(year=event_time.year, month=event_time.month, day=event_time.day)
    end_time = start_time + timedelta(days=1)
    return bookings.filter(booking_status=Booking.BookingStatus.PENDING, event_time__range=(start_time, end_time))


def get_approved_bookings_by_venue_id(venue_id, event_time):
    return get_approved_bookings_by_venue(get_venue_by_id(venue_id), event_time)


def get_all_bookings():
    return Booking.objects.all()


def add_new_booking(user_id, venue_id, booking_type, event_time, event_duration, expected_strength, title, description):
    booking = Booking(
        user_id=get_user_by_id(user_id),
        venue_id=get_venue_by_id(venue_id),
        booking_type=booking_type,
        booking_time=datetime.now(),
        event_time=event_time,
        last_updated_time=datetime.now(),
        event_duration=event_duration,
        expected_strength=expected_strength,
        title=title,
        description=description
    )
    booking.save()
    return booking


def update_booking(booking_id, booking_type, expected_strength, title, description):
    booking = get_booking_by_id(booking_id)
    if booking_type is not None:
        booking.booking_type = booking_type
    if expected_strength is not None:
        booking.expected_strength = expected_strength
    if title is not None:
        booking.title = title
    if description is not None:
        booking.description = description
    booking.last_updated_time = datetime.now()
    booking.save()
    return booking


def update_booking_time(booking, event_time, duration):
    booking.event_time = event_time
    booking.event_duration = duration
    booking.save()
    return booking


def update_booking_status(booking, booking_status):
    booking.booking_status = get_booking_status_from_str(booking_status)
    booking.last_updated_time = datetime.now()
    booking.save()


def cancel_booking(booking):
    booking.booking_status = get_booking_status_from_str("CANCELLED")
    booking.save()
    return booking


def get_booking_status_from_str(request_status):
    if request_status == "PENDING":
        return Booking.BookingStatus.PENDING
    if request_status == "REJECTED":
        return Booking.BookingStatus.REJECTED
    if request_status == "APPROVED":
        return Booking.BookingStatus.APPROVED
    if request_status == "CANCELLED":
        return Booking.BookingStatus.CANCELLED
    if request_status == "AUTOMATICALLY_DECLINED":
        return Booking.BookingStatus.AUTOMATICALLY_DECLINED


def check_booking_request_exists(booking_request_id):
    return BookingRequest.objects.filter(id=booking_request_id).exists()


def get_booking_request_by_id(booking_request_id):
    return BookingRequest.objects.get(id=booking_request_id)


def get_booking_request_by_venue(venue_id):
    booking_requests = list()
    bookings = Booking.objects.filter(venue_id=venue_id)
    for booking in bookings:
        booking_requests.append(BookingRequest.objects.filter(booking_id=booking.id))
    return booking_requests


def get_booking_request_by_booking(booking_id):
    return BookingRequest.objects.filter(booking_id=booking_id)


def get_booking_request_by_receiver(receiver_id):
    return BookingRequest.objects.filter(receiver_id=receiver_id)


def get_all_booking_requests():
    return BookingRequest.objects.all()


def add_booking_request(booking, user):
    booking_request = BookingRequest(
        booking_id=booking,
        receiver_id=user,
        last_updated_time=datetime.now()
    )
    booking_request.save()


def update_booking_request(booking_request, request_status):
    booking_request.request_status = get_booking_request_status_from_str(request_status)
    booking_request.last_updated_time = datetime.now()
    booking_request.save()


def get_booking_request_status_from_str(request_status):
    if request_status == "PENDING_RECEIVE":
        return BookingRequest.RequestStatus.PENDING_RECEIVE
    if request_status == "RECEIVED":
        return BookingRequest.RequestStatus.RECEIVED
    if request_status == "REJECTED":
        return BookingRequest.RequestStatus.REJECTED
    if request_status == "APPROVED":
        return BookingRequest.RequestStatus.APPROVED
    if request_status == "CANCELLED":
        return BookingRequest.RequestStatus.CANCELLED
    if request_status == "AUTOMATICALLY_DECLINED":
        return BookingRequest.RequestStatus.AUTOMATICALLY_DECLINED


def check_comment_exists(comment_id):
    return Comments.objects.filter(id=comment_id).exists()


def get_comment_by_id(comment_id):
    return Comments.objects.get(id=comment_id)


def get_comments_by_user(user_id):
    return Comments.objects.filter(user_id=user_id)


def get_comments_by_booking(booking_id):
    return Comments.objects.filter(booking_id=booking_id)


def get_all_comments():
    return Comments.objects.all()


def add_comment(user_id, booking_id, comment_content):
    comment = Comments(
        user_id=get_user_by_id(user_id),
        booking_id=get_booking_by_id(booking_id),
        comment_content=comment_content,
        comment_time=datetime.now()
    )
    comment.save()
    return comment
