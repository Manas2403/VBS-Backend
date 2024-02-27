from .. import serializers, utils, manager, validator, response_handler, booking_helper
from ..request_handler import RequestHandler
from enum import Enum


class RequestType(Enum):
    GET_BOOKINGS_BY_USER = 0
    GET_BOOKINGS_BY_VENUE = 1
    GET_BOOKING_DETAILS = 2
    GET_VENUE_BOOKINGS_BY_DAY = 3
    GET_BOOKING_REQUESTS_BY_BOOKING = 4
    GET_BOOKING_REQUESTS_BY_RECEIVER = 5
    GET_BOOKING_REQUEST = 6
    ADD_NEW_BOOKING = 7
    UPDATE_BOOKING_TIME = 8
    UPDATE_BOOKING = 9
    CANCEL_BOOKING = 10
    UPDATE_BOOKING_REQUEST = 11


class BookingRequestHandler(RequestHandler):
    def _handle_get_request(self, request_type, request_params):
        if request_type == RequestType.GET_BOOKINGS_BY_USER:
            user_id = request_params.get('user_id')

            is_valid, not_valid_response = validator.validate_existing_user_email(user_id)
            if not is_valid:
                return not_valid_response

            bookings = manager.get_booking_by_user(user_id)
            serializer = serializers.BookingSerializer(bookings, many=True)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestType.GET_BOOKINGS_BY_VENUE:
            venue_id = request_params.get('venue_id')

            is_valid, not_valid_response = validator.validate_venue_id(venue_id)
            if not is_valid:
                return not_valid_response

            bookings = manager.get_booking_by_venue(venue_id)
            serializer = serializers.BookingSerializer(bookings, many=True)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestType.GET_BOOKING_DETAILS:
            booking_id = request_params.get('booking_id')

            is_valid, not_valid_response = validator.validate_booking_id(booking_id)
            if not is_valid:
                return not_valid_response

            booking = manager.get_booking_by_id(booking_id)
            serializer = serializers.BookingSerializer(booking, many=False)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestType.GET_VENUE_BOOKINGS_BY_DAY:
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

            bookings = manager.get_approved_bookings_by_venue_id(venue_id, query_time)
            serializer = serializers.BookingSerializer(bookings, many=True)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestType.GET_BOOKING_REQUESTS_BY_BOOKING:
            booking_id = request_params.get("booking_id")

            is_valid, not_valid_response = validator.validate_booking_id(booking_id)
            if not is_valid:
                return not_valid_response

            booking_requests = manager.get_booking_request_by_booking(booking_id)
            serializer = serializers.BookingRequestSerializer(booking_requests, many=True)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestType.GET_BOOKING_REQUESTS_BY_RECEIVER:
            receiver_id = request_params.get("receiver_id")

            is_valid, not_valid_response = validator.validate_existing_user_email(receiver_id)
            if not is_valid:
                return not_valid_response

            booking_requests = manager.get_booking_request_by_receiver(receiver_id)
            serializer = serializers.BookingRequestSerializer(booking_requests, many=True)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestType.GET_BOOKING_REQUEST:
            booking_request_id = request_params.get("booking_request_id")

            is_valid, not_valid_response = validator.validate_booking_request_id(booking_request_id)
            if not is_valid:
                return not_valid_response

            booking_request = manager.get_booking_request_by_id(booking_request_id)
            serializer = serializers.BookingRequestSerializer(booking_request, many=False)
            return response_handler.get_success_response(serializer.data)

        return response_handler.get_bad_request_response()

    def _handle_post_request(self, request_type, request_data,headers):
        if request_type == RequestType.ADD_NEW_BOOKING:
            user_id = request_data.get("user_id")
            venue_id = request_data.get("venue_id")
            booking_type = request_data.get("booking_type")
            event_time = request_data.get("event_time")
            event_duration = request_data.get("event_duration")
            expected_strength = request_data.get("expected_strength")
            title = request_data.get("title")
            description = request_data.get("description")

            is_valid, not_valid_response = validator.validate_existing_user_email(user_id)
            if not is_valid:
                return not_valid_response

            is_valid, not_valid_response = validator.validate_venue_id(venue_id)
            if not is_valid:
                return not_valid_response

            is_valid, not_valid_response = validator.validate_booking_type(booking_type)
            if not is_valid:
                return not_valid_response

            if event_time is None:
                return response_handler.get_missing_parameters_response("event_time")
            is_valid_time, event_time = utils.get_datetime_from_iso(event_time)
            if not is_valid_time:
                return response_handler.get_invalid_parameters_response("event_time")

            if event_duration is None:
                return response_handler.get_missing_parameters_response("event_duration")
            if event_duration <= 0 or not isinstance(event_duration, int):
                return response_handler.get_invalid_parameters_response("event_duration")

            if expected_strength is None:
                return response_handler.get_missing_parameters_response("expected_strength")
            if expected_strength <= 0 or not isinstance(expected_strength, int):
                return response_handler.get_invalid_parameters_response("expected_strength")

            if title is None:
                return response_handler.get_missing_parameters_response("title")
            if title == "" or not isinstance(title, str):
                return response_handler.get_invalid_parameters_response("title")

            if description is None:
                return response_handler.get_missing_parameters_response("description")
            if description == "" or not isinstance(description, str):
                return response_handler.get_invalid_parameters_response("description")

            if not utils.is_valid_time_and_duration(event_time, event_duration):
                return response_handler.get_invalid_parameters_response("event_time, event_duration")

            booking = manager.add_new_booking(user_id, venue_id, booking_type, event_time, event_duration, expected_strength,
                                              title, description)

            booking_helper.create_booking_requests(booking)

            serializer = serializers.BookingSerializer(booking, many=False)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestType.UPDATE_BOOKING_TIME:
            booking_id = request_data.get('booking_id')
            event_time = request_data.get("event_time")
            event_duration = request_data.get("event_duration")

            is_valid, not_valid_response = validator.validate_booking_id(booking_id)
            if not is_valid:
                return not_valid_response

            if event_time is None:
                return response_handler.get_missing_parameters_response("event_time")
            is_valid_time, event_time = utils.get_datetime_from_iso(event_time)
            if not is_valid_time:
                return response_handler.get_invalid_parameters_response("event_time")

            if event_duration is None:
                return response_handler.get_missing_parameters_response("event_duration")
            if event_duration <= 0 or not isinstance(event_duration, int):
                return response_handler.get_invalid_parameters_response("event_duration")

            if not utils.is_valid_time_and_duration(event_time, event_duration):
                return response_handler.get_invalid_parameters_response("event_time, event_duration")

            booking = booking_helper.update_booking_time(booking_id, event_time, event_duration)
            serializer = serializers.BookingSerializer(booking, many=False)
            return response_handler.get_success_response(serializer)

        if request_type == RequestType.UPDATE_BOOKING:
            booking_id = request_data.get('booking_id')
            booking_type = request_data.get("booking_type")
            expected_strength = request_data.get("expected_strength")
            title = request_data.get("title")
            description = request_data.get("description")

            is_valid, not_valid_response = validator.validate_booking_id(booking_id)
            if not is_valid:
                return not_valid_response

            if booking_type is not None:
                is_valid, not_valid_response = validator.validate_booking_type(booking_type)
                if not is_valid:
                    return not_valid_response

            if expected_strength is not None:
                if expected_strength <= 0 or not isinstance(expected_strength, int):
                    return response_handler.get_invalid_parameters_response("expected_strength")

            if title is not None:
                if title == "" or not isinstance(title, str):
                    return response_handler.get_invalid_parameters_response("title")

            if description is not None:
                if description == "" or not isinstance(description, str):
                    return response_handler.get_invalid_parameters_response("description")

            booking = manager.update_booking(booking_id, booking_type, expected_strength, title, description)
            serializer = serializers.BookingSerializer(booking, many=False)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestType.CANCEL_BOOKING:
            booking_id = request_data.get('booking_id')

            is_valid, not_valid_response = validator.validate_booking_id(booking_id)
            if not is_valid:
                return not_valid_response

            booking = booking_helper.cancel_booking(booking_id)
            serializer = serializers.BookingSerializer(booking, many=False)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestType.UPDATE_BOOKING_REQUEST:
            booking_request_id = request_data.get("id")
            request_status = request_data.get("request_status")

            is_valid, not_valid_response = validator.validate_booking_request_id(booking_request_id)
            if not is_valid:
                return not_valid_response

            if request_status is None:
                return response_handler.get_missing_parameters_response("request_status")
            if request_status not in ["REJECTED", "APPROVED"]:
                return response_handler.get_invalid_parameters_response("request_status")

            booking_request = manager.get_booking_request_by_id(booking_request_id)
            manager.update_booking_request(booking_request, request_status)
            booking_helper.update_booking_requests(booking_request.booking_id)

            serializer = serializers.BookingRequestSerializer(booking_request, many=False)
            return response_handler.get_success_response(serializer.data)

        return response_handler.get_bad_request_response()
