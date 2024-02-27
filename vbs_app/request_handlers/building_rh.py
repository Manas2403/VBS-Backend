from .. import serializers, validator, response_handler, manager
from ..request_handler import RequestHandler
from enum import Enum


class RequestTypes(Enum):
    GET_ALL_BUILDINGS = 0
    GET_BUILDING_DETAILS = 1
    GET_BUILDINGS_BY_SEARCH = 2
    ADD_NEW_BUILDING = 3
    UPDATE_EXISTING_BUILDING = 4
    REMOVE_EXISTING_BUILDING = 5


class BuildingRequestHandler(RequestHandler):
    def _handle_get_request(self, request_type, request_params):
        if request_type == RequestTypes.GET_ALL_BUILDINGS:
            buildings = manager.get_all_buildings()
            serializer = serializers.BuildingSerializer(buildings, many=True)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestTypes.GET_BUILDING_DETAILS:
            building_id = request_params.get('id')

            is_valid, not_valid_response = validator.validate_building_id(building_id)
            if not is_valid:
                return not_valid_response

            building = manager.get_building_by_id(building_id)
            serializer = serializers.BuildingSerializer(building, many=False)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestTypes.GET_BUILDINGS_BY_SEARCH:
            name = request_params.get('name')

            if name is None:
                return response_handler.get_missing_parameters_response("name")
            if name == "" or not isinstance(name, str):
                return response_handler.get_invalid_parameters_response("name")

            buildings = manager.get_buildings_by_name(name)
            serializer = serializers.BuildingSerializer(buildings, many=True)
            return response_handler.get_success_response(serializer.data)

        return response_handler.get_bad_request_response()

    def _handle_post_request(self, request_type, request_data,headers):
        if request_type == RequestTypes.ADD_NEW_BUILDING:
            # print(request_data)
            name = request_data.get("name")

            if name is None:
                return response_handler.get_missing_parameters_response("name")
            if name == "" or not isinstance(name, str):
                return response_handler.get_invalid_parameters_response("name")

            building = manager.add_building(name)
            serializer = serializers.BuildingSerializer(building, many=False)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestTypes.UPDATE_EXISTING_BUILDING:
            building_id = request_data.get('id')
            name = request_data.get('name')

            is_valid, not_valid_response = validator.validate_building_id(building_id)
            if not is_valid:
                return not_valid_response

            building = manager.get_building_by_id(building_id)

            if name is not None:
                if name == "" or not isinstance(name, str):
                    return response_handler.get_invalid_parameters_response("name")

            building = manager.update_building(building, name)
            serializer = serializers.BuildingSerializer(building, many=False)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestTypes.REMOVE_EXISTING_BUILDING:
            building_id = request_data.get('id')

            is_valid, not_valid_response = validator.validate_building_id(building_id)
            if not is_valid:
                return not_valid_response

            manager.delete_building(building_id)
            return response_handler.get_success_response(None)

        return response_handler.get_bad_request_response()
