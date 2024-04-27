import email

from flask import request
from .. import serializers, utils, manager, validator, response_handler, booking_helper,email_rh
from ..request_handler import FileUploadRequestHandler,RequestHandler
from enum import Enum
import cloudinary.uploader
import os
from dotenv import load_dotenv
load_dotenv()

class RequestType(Enum):
    GET_VH_BOOKINGS_BY_USER = 0
    GET_VH_BOOKINGS_BY_VENUE = 1
    GET_VH_BOOKING_DETAILS = 2
    GET_VH_VENUE_BOOKINGS_BY_DAY = 3
    GET_VH_BOOKING_REQUESTS_BY_BOOKING = 4
    GET_VH_BOOKING_REQUESTS_BY_RECEIVER = 5
    GET_VH_BOOKING_REQUEST = 6
    UPDATE_VH_BOOKING_TIME = 7
    CANCEL_VH_BOOKING = 8
    UPDATE_VH_BOOKING_REQUEST = 9
 
class AddNewVHBookingAPIView(FileUploadRequestHandler):
     def _handle_post_request(self, request_data, request_files):
         user_id = request_data.get("user_id")
         booking_type = request_data.get("booking_type")
         arrival_time = request_data.get("arrival_time")
         departure_time = request_data.get("departure_time")
         rooms_required = request_data.get("rooms_required")
         booking_purpose = request_data.get("booking_purpose") 
         requestby = request_data.get("requestby")
         user_address = request_data.get("user_address")
         user_contact = request_data.get("user_contact")
         id_proof = request_data.get("id_proof")  

         is_valid, not_valid_response = validator.validate_existing_user_email(user_id)
         if not is_valid:
                return not_valid_response

         is_valid, not_valid_response = validator.validate_vh_booking_type(booking_type)
         if not is_valid:
                return not_valid_response
        
         is_valid, not_valid_response = validator.validate_vh_request_by_type(requestby)
         if not is_valid:
                return not_valid_response
            
         if arrival_time is None:
             return response_handler.get_missing_parameters_response("arrival_time")
         is_valid_time, arrival_time = utils.get_datetime_from_iso(arrival_time)
         if not is_valid_time:
            return response_handler.get_invalid_parameters_response("arrival_time")
        
         if departure_time is None:
             return response_handler.get_missing_parameters_response("departure_time")
         is_valid_time, departure_time = utils.get_datetime_from_iso(departure_time)
         if not is_valid_time:
            return response_handler.get_invalid_parameters_response("departure_time")
        
         if rooms_required is None:
            return response_handler.get_missing_parameters_response("rooms_required")
         if booking_purpose is None:
            return response_handler.get_missing_parameters_response("booking_purpose")
         if booking_purpose == "":
            return response_handler.get_invalid_parameters_response("booking_purpose")
         
         if user_address is None:
            return response_handler.get_missing_parameters_response("user_address")
         if user_address == "":
            return response_handler.get_invalid_parameters_response("user_address")
         
         if user_contact is None:
             return response_handler.get_missing_parameters_response("user_contact")
         if not utils.is_valid_phone_number(user_contact):
            return response_handler.get_invalid_parameters_response("user_contact")
        
         if id_proof is not None:
            try:
                result = cloudinary.uploader.upload(id_proof)
                image_url = result.get('secure_url')
            except Exception as e:
                return response_handler.get_internal_server_error_response("Failed to upload image")
         else:
            image_url = None
         booking = manager.add_new_vh_booking(user_id, booking_type, arrival_time, departure_time, rooms_required, booking_purpose, requestby, user_address, user_contact, image_url)
         booking_helper.create_vh_booking_requests(booking)
         email_rh.send_email_view(self,user_id,"Your booking has been successfully created! You will receive an email update when there are changes to your booking status.")
         authority_id=os.getenv("VH_AUTHORITY_MAIL")
         email_rh.send_email_view(self,authority_id,"A new booking request has been generated. Please visit the website to update the status of the request.")       
         serializer = serializers.VHBookingSerializer(booking, many=False)
         return response_handler.get_success_response(serializer.data)              
    
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

        
        
     def _handle_post_request(self, request_type, request_data,headers):
         if request_type == RequestType.UPDATE_VH_BOOKING_TIME:
            booking_id = request_data.get('booking_id')
            arrival_time = request_data.get("arrival_time")
            departure_time = request_data.get("departure_time")

            is_valid, not_valid_response = validator.validate_vh_booking_id(booking_id)
            if not is_valid:
                return not_valid_response
            if arrival_time is None:
                return response_handler.get_missing_parameters_response("arrival_time")
            is_valid_time, arrival_time = utils.get_datetime_from_iso(arrival_time)
            if not is_valid_time:
                return response_handler.get_invalid_parameters_response("arrival_time")

            if departure_time is None:
                return response_handler.get_missing_parameters_response("departure_time")
            is_valid_time, departure_time = utils.get_datetime_from_iso(departure_time)
            if not is_valid_time:
                return response_handler.get_invalid_parameters_response("departure_time")

            booking = booking_helper.update_vh_booking_time(booking_id, arrival_time, departure_time)
            serializer = serializers.VHBookingSerializer(booking, many=False)
            serialized_data=serializer.data
            return response_handler.get_success_response(serialized_data)     
        
         if request_type == RequestType.CANCEL_VH_BOOKING:
            booking_id = request_data.get('booking_id')
            is_valid, not_valid_response = validator.validate_vh_booking_id(booking_id)
            if not is_valid:
                return not_valid_response
            booking = booking_helper.cancel_vh_booking(booking_id)
            serializer = serializers.VHBookingSerializer(booking, many=False)
            return response_handler.get_success_response(serializer.data)


         if request_type == RequestType.UPDATE_VH_BOOKING_REQUEST:
            booking_request_id = request_data.get("id")
            request_status = request_data.get("request_status")      
            is_valid, not_valid_response = validator.validate_vh_booking_request_id(booking_request_id)
            if not is_valid:
                return not_valid_response

            if request_status is None:
                return response_handler.get_missing_parameters_response("request_status")
            if request_status not in ["REJECTED", "APPROVED"]:
                return response_handler.get_invalid_parameters_response("request_status")

            booking_request = manager.get_vh_booking_request_by_id(booking_request_id)
            manager.update_vh_booking_request(booking_request, request_status)
            booking_helper.update_vh_booking_requests(booking_request.booking_id)
            booking=manager.get_vh_booking_by_id(booking_request.booking_id.id)
            email_rh.send_email_view(self,booking.user_id.email,"Your booking request has been {}".format(request_status))
            serializer = serializers.VHBookingRequestSerializer(booking_request, many=False)
            return response_handler.get_success_response(serializer.data)

         return response_handler.get_bad_request_response()
             