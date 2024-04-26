import email

from flask import request
from .. import serializers, utils, manager, validator, response_handler, booking_helper,email_rh
from ..request_handler import RequestHandler
from enum import Enum


class RequestType(Enum):
    GET_VH_BOOKINGS_BY_USER = 0
    GET_VH_BOOKINGS_BY_VENUE = 1
    GET_VH_BOOKING_DETAILS = 2
    GET_VH_VENUE_BOOKINGS_BY_DAY = 3
    GET_VH_BOOKING_REQUESTS_BY_BOOKING = 4
    GET_VH_BOOKING_REQUESTS_BY_RECEIVER = 5
    GET_VH_BOOKING_REQUEST = 6
    ADD_NEW_VH_BOOKING = 7
    UPDATE_VH_BOOKING_TIME = 8
    UPDATE_VH_BOOKING = 9
    CANCEL_VH_BOOKING = 10
    UPDATE_VH_BOOKING_REQUEST = 11
    
class VHBookingRequestHandler(RequestHandler):
     def _handle_get_request(self, request_type, request_params):
         if request_type == RequestType.GET_VH_BOOKINGS_BY_USER:
            user_id = request_params.get('user_id')
            is_valid, not_valid_response = validator.validate_existing_user_email(user_id)
            if not is_valid:
                return not_valid_response
            bookings = manager.get_vh_booking_by_user(user_id)
            serializer = serializers.VHBookingSerializer(bookings, many=True)
            return response_handler.get_success_response(serializer.data)
        
         if request_type == RequestType.GET_VH_BOOKINGS_BY_VENUE:
            venue_id = request_params.get('venue_id')

            is_valid, not_valid_response = validator.validate_vh_venue_id(venue_id)
            if not is_valid:
                return not_valid_response

            bookings = manager.get_vh_booking_by_venue(venue_id)
            serializer = serializers.VHBookingSerializer(bookings, many=True)
            return response_handler.get_success_response(serializer.data)
        
         if request_type == RequestType.GET_VH_BOOKING_DETAILS:
            booking_id = request_params.get('booking_id')
            is_valid, not_valid_response = validator.validate_vh_booking_id(booking_id)
            if not is_valid:
                return not_valid_response

            booking = manager.get_vh_booking_by_id(booking_id)
            serializer = serializers.VHBookingSerializer(booking, many=False)
            return response_handler.get_success_response(serializer.data)

         if request_type == RequestType.GET_VH_VENUE_BOOKINGS_BY_DAY:
            venue_id = request_params.get("venue_id")
            query_time = request_params.get("query_time")

            is_valid, not_valid_response = validator.validate_venue_id(venue_id)
            if not is_valid:
                return not_valid_response

            if query_time is None:
                return response_handler.get_missing_parameters_response("query_time")
            is_valid_time, query_time = utils.get_datetime_from_iso(query_time)
            if not is_valid_time:
                return response_handler.get_invalid_parameters_response("query_time")

            bookings = manager.get_approved_vh_bookings_by_venue_id(venue_id, query_time)
            serializer = serializers.VHBookingSerializer(bookings, many=True)
            return response_handler.get_success_response(serializer.data)

         if request_type == RequestType.GET_VH_BOOKING_REQUESTS_BY_BOOKING:
            booking_id = request_params.get("booking_id")

            is_valid, not_valid_response = validator.validate_vh_booking_id(booking_id)
            if not is_valid:
                return not_valid_response

            booking_requests = manager.get_vh_booking_request_by_booking(booking_id)
            serializer = serializers.VHBookingRequestSerializer(booking_requests, many=True)
            return response_handler.get_success_response(serializer.data)

         if request_type == RequestType.GET_VH_BOOKING_REQUESTS_BY_RECEIVER:
            receiver_id = request_params.get("receiver_id")

            is_valid, not_valid_response = validator.validate_existing_user_email(receiver_id)
            if not is_valid:
                return not_valid_response

            booking_requests = manager.get_vh_booking_request_by_receiver(receiver_id)
            serializer = serializers.VHBookingRequestSerializer(booking_requests, many=True)
            return response_handler.get_success_response(serializer.data)

         if request_type == RequestType.GET_VH_BOOKING_REQUEST:
            booking_request_id = request_params.get("booking_request_id")

            is_valid, not_valid_response = validator.validate_vh_booking_request_id(booking_request_id)
            if not is_valid:
                return not_valid_response

            booking_request = manager.get_vh_booking_request_by_id(booking_request_id)
            serializer = serializers.VHBookingRequestSerializer(booking_request, many=False)
            return response_handler.get_success_response(serializer.data)
        
         return response_handler.get_bad_request_response()
             