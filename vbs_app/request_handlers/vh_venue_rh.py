from .. import serializers, manager, validator, response_handler
from ..request_handler import RequestHandler
from enum import Enum


class RequestTypes(Enum):
    GET_ALL_VH_VENUES = 0
    GET_VH_VENUES_BY_BUILDING = 1
    GET_VH_VENUES_BY_AUTHORITY = 2
    GET_VH_VENUES_BY_SEARCH = 3
    GET_VH_VENUE_DETAILS = 4
    ADD_NEW_VH_VENUE = 5
    UPDATE_EXISTING_VH_VENUE = 6
    REMOVE_EXISTING_VH_VENUE = 7
    
class VHVenueRequestHandler(RequestHandler):
     def _handle_get_request(self, request_type, request_params):
         if request_type == RequestTypes.GET_ALL_VH_VENUES:
            venues = manager.get_all_vh_venues()
            serializer = serializers.VHVenueSerializer(venues, many=True)
            return response_handler.get_success_response(serializer.data)
        
         if request_type == RequestTypes.GET_VH_VENUES_BY_BUILDING:
            building_id = request_params.get('building_id')

            is_building_valid, not_valid_response = validator.validate_building_id(building_id)
            if not is_building_valid:
                return not_valid_response

            venues = manager.get_vh_venue_by_building(building_id)
            serializer = serializers.VHVenueSerializer(venues, many=True)
            return response_handler.get_success_response(serializer.data)
        
         if request_type == RequestTypes.GET_VH_VENUES_BY_AUTHORITY:
            authority_id = request_params.get('authority_id')
            is_authority_valid, not_valid_response = validator.validate_existing_user_email(authority_id)
            if not is_authority_valid:
                return not_valid_response

            venues = manager.get_vh_venue_by_authority(authority_id)
            serializer = serializers.VHVenueSerializer(venues, many=True)
            return response_handler.get_success_response(serializer.data)
        
         if request_type == RequestTypes.GET_VH_VENUES_BY_SEARCH:
            name = request_params.get('name')
            if name is None:
                return response_handler.get_missing_parameters_response("name")
            if not isinstance(name, str):
                return response_handler.get_invalid_parameters_response("name")

            venues = manager.get_vh_venue_by_name(name)
            serializer = serializers.VHVenueSerializer(venues, many=True)
            return response_handler.get_success_response(serializer.data)
        
         if request_type == RequestTypes.GET_VH_VENUE_DETAILS:
            venue_id = request_params.get('venue_id')

            is_valid, not_valid_response = validator.validate_vh_venue_id(venue_id)
            if not is_valid:
                return not_valid_response

            venue = manager.get_vh_venue_by_id(venue_id)
            serializer = serializers.VHVenueSerializer(venue, many=False)
            return response_handler.get_success_response(serializer.data)

         return response_handler.get_bad_request_response()
     
     def _handle_post_request(self, request_type, request_data,headers):
         if request_type == RequestTypes.ADD_NEW_VH_VENUE:
            building_id = request_data.get('building_id')
            authority_id = request_data.get('authority_id')
            name = request_data.get("name")
            floor_number = request_data.get("floor_number")
            accomodation_type = request_data.get("accomodation_type")
            
            is_valid, not_valid_response = validator.validate_building_id(building_id)
            if not is_valid:
                return not_valid_response
            
            is_valid, not_valid_response = validator.validate_existing_user_email(authority_id)
            if not is_valid:
                return not_valid_response
            
            is_valid, not_valid_response = validator.validate_accomodation_type(accomodation_type)
            if not is_valid:
                return not_valid_response
            
            if name is None:
                return response_handler.get_missing_parameters_response("name")
            if floor_number is None:
                return response_handler.get_missing_parameters_response("floor_number")
            
            if name == "" or not isinstance(name, str):
                return response_handler.get_invalid_parameters_response("name")
            if floor_number < 0 or not isinstance(floor_number, int):
                return response_handler.get_invalid_parameters_response("floor_number")
            
            venue = manager.add_vh_venue(building_id,authority_id,name,floor_number,accomodation_type)

            serializer = serializers.VHVenueSerializer(venue, many=False)
            return response_handler.get_success_response(serializer.data)
        
         if request_type == RequestTypes.UPDATE_EXISTING_VH_VENUE:
            venue_id = request_data.get('id')
            building_id = request_data.get("building_id")
            authority_id = request_data.get("authority_id")
            name = request_data.get("name")
            floor_number = request_data.get("floor_number")
            accomodation_type = request_data.get("accomodation_type")

            is_valid, not_valid_response = validator.validate_vh_venue_id(venue_id)
            if not is_valid:
                return not_valid_response

            venue = manager.get_vh_venue_by_id(venue_id)

            if building_id is not None:
                is_valid, not_valid_response = validator.validate_building_id(building_id)
                if not is_valid:
                    return not_valid_response

            if authority_id is not None:
                is_valid, not_valid_response = validator.validate_existing_user_email(authority_id)
                if not is_valid:
                    return not_valid_response

            if name is not None:
                if name == "" or not isinstance(name, str):
                    return response_handler.get_invalid_parameters_response("name")

            if floor_number is not None:
                if floor_number < 0 or not isinstance(floor_number, int):
                    return response_handler.get_invalid_parameters_response("floor_number")

            if accomodation_type is not None:
                is_valid, not_valid_response = validator.validate_accomodation_type(accomodation_type)
                if not is_valid:
                    return not_valid_response


            venue = manager.update_vh_venue(venue, name, building_id, floor_number,accomodation_type,authority_id)

            serializer = serializers.VHVenueSerializer(venue, many=False)
            return response_handler.get_success_response(serializer.data)
        
         if request_type == RequestTypes.REMOVE_EXISTING_VH_VENUE:
            venue_id = request_data.get('id')
            is_valid, not_valid_response = validator.validate_vh_venue_id(venue_id)
            if not is_valid:
                return not_valid_response

            manager.delete_vh_venue(venue_id)
            return response_handler.get_success_response(None)

         return response_handler.get_bad_request_response()

            
         
          
