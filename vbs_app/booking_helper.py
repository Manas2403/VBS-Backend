from . import manager, utils
import os
from dotenv import load_dotenv
load_dotenv()

def create_booking_requests(booking):
    if not is_slot_available(booking.venue_id, booking.event_time, booking.event_duration):
        manager.update_booking_status(booking, "AUTOMATICALLY_DECLINED")
        return

    user_id = booking.user_id
    authority_id = booking.venue_id.authority_id

    users_list = get_users_list_for_booking_requests(user_id, authority_id)
    for user in users_list:
        manager.add_booking_request(booking, user)

    update_booking_requests(booking)

def create_vh_booking_requests(booking):
    user_id=booking.user_id
    authority_mail=os.getenv("VH_AUTHORITY_MAIL")
    authority_id=manager.get_user_by_id(authority_mail)
    users_list=get_users_list_for_booking_requests(user_id,authority_id)
    for user in users_list:
        manager.add_vh_booking_request(booking,user)
    return

def update_booking_requests(booking):
    total_requests = manager.get_booking_request_by_booking(booking)

    approved_requests = total_requests.filter(
        request_status=manager.get_booking_request_status_from_str("APPROVED")
    )
    pending_requests = total_requests.filter(
        request_status=manager.get_booking_request_status_from_str("PENDING_RECEIVE")
    )
    rejected_requests = total_requests.filter(
        request_status=manager.get_booking_request_status_from_str("REJECTED")
    )

    print(pending_requests)

    if len(total_requests) == 0 or len(total_requests) == len(approved_requests):
        manager.update_booking_status(booking, "APPROVED")
        automatically_decline_other_bookings(booking, booking.event_time, booking.event_duration)
        return

    if len(rejected_requests) > 0:
        manager.update_booking_status(booking, "REJECTED")
        automatically_decline_remaining_requests(booking)
        return

    if len(pending_requests) > 0:
        new_request = pending_requests[0]
        send_request(new_request)


def update_booking_time(booking_id, event_time, event_duration):
    booking = manager.get_booking_by_id(booking_id)

    if not is_slot_available(booking.venue_id, event_time, event_duration):
        manager.update_booking_status(booking, "AUTOMATICALLY_DECLINED")
        return manager.get_booking_by_id(booking_id)

    booking = manager.update_booking_time(booking, event_time, event_duration)
    update_booking_requests_for_updated_time(booking)
    return booking

def update_vh_booking_time(booking_id, arrival_time, departure_time):
    booking = manager.get_vh_booking_by_id(booking_id)
    if not is_slot_available(booking.venue_id, arrival_time,departure_time):
        manager.update_vh_booking_status(booking, "AUTOMATICALLY_DECLINED")
        return manager.get_vh_booking_by_id(booking_id)

    booking = manager.update_vh_booking_time(booking,arrival_time, departure_time)
    update_vh_booking_requests_for_updated_time(booking)
    return booking


def cancel_booking(booking_id):
    booking = manager.get_booking_by_id(booking_id)
    booking = manager.cancel_booking(booking)
    cancel_booking_requests(booking)
    return booking

def cancel_vh_booking(booking_id):
    booking=manager.get_vh_booking_by_id(booking_id)
    booking=manager.cancel_vh_booking(booking)
    cancel_vh_booking_requests(booking)
    return booking

def get_users_list_for_booking_requests(requester_user, authority_user):
    if requester_user == authority_user:
        return list()
    if not requester_user.require_parent_permission:
        return [authority_user]

    user_list = list()
    user = requester_user
    while user.require_parent_permission:
        user = manager.get_user_by_id(user.parent)
        if user == authority_user:
            break
        user_list.append(user)

    user_list.append(authority_user)
    return user_list


def send_request(booking_request):
    manager.update_booking_request(booking_request, "RECEIVED")



def send_vh_request(booking_request):
    manager.update_vh_booking_request(booking_request, "RECEIVED")

def is_slot_available(venue_id, start_time, duration):
    approved_bookings = manager.get_approved_bookings_by_venue(venue_id, start_time)
    for booking in approved_bookings:
        if utils.is_time_overlapping(start_time, duration, booking.event_time, booking.event_duration):
            return False
    return True


def automatically_decline_other_bookings(booking, start_time, duration):
    other_bookings = manager.get_pending_bookings_by_venue(booking.venue_id, start_time)

    for other_booking in other_bookings:
        if utils.is_time_overlapping(start_time, duration, other_booking.event_time, other_booking.event_duration):
            automatically_decline_all_requests(other_booking)

def automatically_decline_other_vh_bookings(booking, start_time, duration):
    other_bookings = manager.get_pending_vh_bookings_by_venue(booking.venue_id, start_time)

    for other_booking in other_bookings:
        if utils.is_time_overlapping(start_time, duration, other_booking.event_time, other_booking.event_duration):
            automatically_decline_all_vh_requests(other_booking)

def cancel_booking_requests(booking):
    booking_requests = manager.get_booking_request_by_booking(booking)
    for booking_request in booking_requests:
        manager.update_booking_request(booking_request, "CANCELLED")


def cancel_vh_booking_requests(booking):
    booking_requests = manager.get_vh_booking_request_by_booking(booking)
    for booking_request in booking_requests:
        manager.update_vh_booking_request(booking_request, "CANCELLED")

def automatically_decline_all_requests(booking):
    manager.update_booking_status(booking, "AUTOMATICALLY_DECLINED")
    total_requests = manager.get_booking_request_by_booking(booking)
    for booking_request in total_requests:
        manager.update_booking_request(booking_request, "AUTOMATICALLY_DECLINED")

def automatically_decline_all_vh_requests(booking):
    manager.update_vh_booking_status(booking, "AUTOMATICALLY_DECLINED")
    total_requests = manager.get_vh_booking_request_by_booking(booking)
    for booking_request in total_requests:
        manager.update_vh_booking_request(booking_request, "AUTOMATICALLY_DECLINED")


def automatically_decline_remaining_requests(booking):
    total_requests = manager.get_booking_request_by_booking(booking)
    pending_requests = total_requests.filter(
        request_status=manager.get_booking_request_status_from_str("PENDING_RECEIVE")
    )
    for pending_request in pending_requests:
        manager.update_booking_request(pending_request, "AUTOMATICALLY_DECLINED")

def automatically_decline_remaining_vh_requests(booking):
    total_requests = manager.get_vh_booking_request_by_booking(booking)
    pending_requests = total_requests.filter(
        request_status=manager.get_vh_booking_request_status_from_str("PENDING_RECEIVE")
    )
    for pending_request in pending_requests:
        manager.update_vh_booking_request(pending_request, "AUTOMATICALLY_DECLINED")

def update_booking_requests_for_updated_time(booking):
    booking_requests = manager.get_booking_request_by_booking(booking)
    for booking_request in booking_requests:
        manager.update_booking_request(booking_request, "PENDING_RECEIVE")
    if len(booking_requests) > 0:
        send_request(booking_requests[0])
    return

def update_vh_booking_requests_for_updated_time(booking):
    booking_requests = manager.get_vh_booking_request_by_booking(booking)
    for booking_request in booking_requests:
        manager.update_vh_booking_request(booking_request, "PENDING_RECEIVE")
    if len(booking_requests) > 0:
        send_vh_request(booking_requests[0])
    return

def update_vh_booking_requests(booking):
    total_requests = manager.get_vh_booking_request_by_booking(booking)

    approved_requests = total_requests.filter(
        request_status=manager.get_vh_booking_request_status_from_str("APPROVED")
    )
    pending_requests = total_requests.filter(
        request_status=manager.get_vh_booking_request_status_from_str("PENDING_RECEIVE")
    )
    rejected_requests = total_requests.filter(
        request_status=manager.get_vh_booking_request_status_from_str("REJECTED")
    )

    print(pending_requests)

    if len(total_requests) == 0 or len(total_requests) == len(approved_requests):
        manager.update_vh_booking_status(booking, "APPROVED")
        # automatically_decline_other_vh_bookings(booking, booking.event_time, booking.event_duration)
        return

    if len(rejected_requests) > 0:
        manager.update_vh_booking_status(booking, "REJECTED")
        automatically_decline_remaining_vh_requests(booking)
        return

    if len(pending_requests) > 0:
        new_request = pending_requests[0]
        send_vh_request(new_request)
