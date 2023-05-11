from .. import serializers, manager, validator, response_handler
from ..request_handler import RequestHandler
from enum import Enum


class RequestTypes(Enum):
    GET_ALL_VENUES = 0
    GET_VENUES_BY_BUILDING = 1
    GET_VENUES_BY_AUTHORITY = 2
    GET_VENUES_BY_SEARCH = 3
    GET_VENUE_DETAILS = 4
    ADD_NEW_VENUE = 5
    UPDATE_EXISTING_VENUE = 6
    REMOVE_EXISTING_VENUE = 7


class VenueRequestHandler(RequestHandler):
    def _handle_get_request(self, request_type, request_params):
        if request_type == RequestTypes.GET_ALL_VENUES:
            venues = manager.get_all_venues()
            serializer = serializers.VenueSerializer(venues, many=True)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestTypes.GET_VENUES_BY_BUILDING:
            building_id = request_params.get('building_id')

            is_building_valid, not_valid_response = validator.validate_building_id(building_id)
            if not is_building_valid:
                return not_valid_response

            venues = manager.get_venue_by_building(building_id)
            serializer = serializers.VenueSerializer(venues, many=True)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestTypes.GET_VENUES_BY_AUTHORITY:
            authority_id = request_params.get('authority_id')

            is_authority_valid, not_valid_response = validator.validate_existing_user_email(authority_id)
            if not is_authority_valid:
                return not_valid_response

            venues = manager.get_venue_by_authority(authority_id)
            serializer = serializers.VenueSerializer(venues, many=True)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestTypes.GET_VENUES_BY_SEARCH:
            name = request_params.get('name')

            if name is None:
                return response_handler.get_missing_parameters_response("name")
            if not isinstance(name, str):
                return response_handler.get_invalid_parameters_response("name")

            venues = manager.get_venue_by_name(name)
            serializer = serializers.VenueSerializer(venues, many=True)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestTypes.GET_VENUE_DETAILS:
            venue_id = request_params.get('venue_id')

            is_valid, not_valid_response = validator.validate_venue_id(venue_id)
            if not is_valid:
                return not_valid_response

            venue = manager.get_venue_by_id(venue_id)
            serializer = serializers.VenueSerializer(venue, many=False)
            return response_handler.get_success_response(serializer.data)

        return response_handler.get_bad_request_response()

    def _handle_post_request(self, request_type, request_data):
        if request_type == RequestTypes.ADD_NEW_VENUE:
            building_id = request_data.get('building_id')
            authority_id = request_data.get('authority_id')
            name = request_data.get("name")
            floor_number = request_data.get("floor_number")
            venue_type = request_data.get("venue_type")
            is_accessible = request_data.get("is_accessible")
            seating_capacity = request_data.get("seating_capacity")
            has_air_conditioner = request_data.get("has_air_conditioner")
            has_projectors = request_data.get("has_projectors")
            has_speakers = request_data.get("has_speakers")
            has_whiteboard = request_data.get("has_whiteboard")

            is_valid, not_valid_response = validator.validate_building_id(building_id)
            if not is_valid:
                return not_valid_response

            is_valid, not_valid_response = validator.validate_existing_user_email(authority_id)
            if not is_valid:
                return not_valid_response

            is_valid, not_valid_response = validator.validate_venue_type(venue_type)
            if not is_valid:
                return not_valid_response

            if name is None:
                return response_handler.get_missing_parameters_response("name")
            if floor_number is None:
                return response_handler.get_missing_parameters_response("floor_number")
            if is_accessible is None:
                return response_handler.get_missing_parameters_response("is_accessible")
            if seating_capacity is None:
                return response_handler.get_missing_parameters_response("seating_capacity")
            if has_air_conditioner is None:
                return response_handler.get_missing_parameters_response("has_air_conditioner")
            if has_projectors is None:
                return response_handler.get_missing_parameters_response("has_projectors")
            if has_speakers is None:
                return response_handler.get_missing_parameters_response("has_speakers")
            if has_whiteboard is None:
                return response_handler.get_missing_parameters_response("has_whiteboard")

            if name == "" or not isinstance(name, str):
                return response_handler.get_invalid_parameters_response("name")
            if floor_number < 0 or not isinstance(floor_number, int):
                return response_handler.get_invalid_parameters_response("floor_number")
            if not isinstance(is_accessible, building_id):
                return response_handler.get_invalid_parameters_response("is_accessible")
            if seating_capacity <= 0 or not isinstance(seating_capacity, int):
                return response_handler.get_invalid_parameters_response("seating_capacity")
            if not isinstance(has_air_conditioner, bool):
                return response_handler.get_invalid_parameters_response("has_air_conditioner")
            if not isinstance(has_projectors, bool):
                return response_handler.get_invalid_parameters_response("has_projectors")
            if not isinstance(has_speakers, bool):
                return response_handler.get_invalid_parameters_response("has_speakers")
            if not isinstance(has_whiteboard, bool):
                return response_handler.get_invalid_parameters_response("has_whiteboard")

            venue = manager.add_venue(name, building_id, floor_number, venue_type, is_accessible, seating_capacity,
                                      has_air_conditioner, has_projectors, has_speakers, has_whiteboard, authority_id)

            serializer = serializers.VenueSerializer(venue, many=False)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestTypes.UPDATE_EXISTING_VENUE:
            venue_id = request_data.get('venue_id')
            building_id = request_data.get("building_id")
            authority_id = request_data.get("authority_id")
            name = request_data.get("name")
            floor_number = request_data.get("floor_number")
            venue_type = request_data.get("venue_type")
            is_accessible = request_data.get("is_accessible")
            seating_capacity = request_data.get("seating_capacity")
            has_air_conditioner = request_data.get("has_air_conditioner")
            has_projectors = request_data.get("has_projectors")
            has_speakers = request_data.get("has_speakers")
            has_whiteboard = request_data.get("has_whiteboard")

            is_valid, not_valid_response = validator.validate_venue_id(venue_id)
            if not is_valid:
                return not_valid_response

            venue = manager.get_venue_by_id(venue_id)

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

            if venue_type is not None:
                is_valid, not_valid_response = validator.validate_venue_type(venue_type)
                if not is_valid:
                    return not_valid_response

            if is_accessible is not None:
                if not isinstance(is_accessible, building_id):
                    return response_handler.get_invalid_parameters_response("is_accessible")

            if seating_capacity is not None:
                if seating_capacity <= 0 or not isinstance(seating_capacity, int):
                    return response_handler.get_invalid_parameters_response("seating_capacity")

            if has_air_conditioner is not None:
                if not isinstance(has_air_conditioner, bool):
                    return response_handler.get_invalid_parameters_response("has_air_conditioner")

            if has_projectors is not None:
                if not isinstance(has_projectors, bool):
                    return response_handler.get_invalid_parameters_response("has_projectors")

            if has_speakers is not None:
                if not isinstance(has_speakers, bool):
                    return response_handler.get_invalid_parameters_response("has_speakers")

            if has_whiteboard is not None:
                if not isinstance(has_whiteboard, bool):
                    return response_handler.get_invalid_parameters_response("has_whiteboard")

            venue = manager.update_venue(venue, name, building_id, floor_number, is_accessible, seating_capacity,
                                         has_air_conditioner, has_projectors, has_speakers, has_whiteboard,
                                         authority_id)

            serializer = serializers.VenueSerializer(venue, many=False)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestTypes.REMOVE_EXISTING_VENUE:
            venue_id = request_data.get('venue_id')

            is_valid, not_valid_response = validator.validate_venue_id(venue_id)
            if not is_valid:
                return not_valid_response

            manager.delete_venue(venue_id)
            return response_handler.get_success_response(None)

        return response_handler.get_bad_request_response()
