from .. import serializers, validator, response_handler, manager
from ..request_handler import FileUploadRequestHandler, RequestHandler
from enum import Enum
import cloudinary.uploader


class RequestTypes(Enum):
    GET_ALL_BUILDINGS = 0
    GET_BUILDING_DETAILS = 1
    GET_BUILDINGS_BY_SEARCH = 2
    ADD_NEW_BUILDING = 3
    UPDATE_EXISTING_BUILDING = 4
    REMOVE_EXISTING_BUILDING = 5


class AddNewBuildingAPIView(FileUploadRequestHandler):
     def _handle_post_request(self, request_data, request_files):
        name = request_data.get("name")
        building_picture=request_data.get('building_picture')
        if name is None:
            return response_handler.get_missing_parameters_response("name")
        if name == "" or not isinstance(name, str):
            return response_handler.get_invalid_parameters_response("name")
        if building_picture:
            try:
                result = cloudinary.uploader.upload(building_picture)
                image_url = result.get('secure_url')
            except Exception as e:
                return response_handler.get_internal_server_error_response("Failed to upload image")
        else:
            image_url = None
        building = manager.add_building(name,image_url)
        serializer = serializers.BuildingSerializer(building, many=False)
        return response_handler.get_success_response(serializer.data)

class UpdateNewBuildingAPIView(FileUploadRequestHandler):
    def _handle_post_request(self, request_data, request_files):
            building_id = request_data.get('id')
            name = request_data.get('name')
            building_picture=request_data.get('building_picture')
            is_valid, not_valid_response = validator.validate_building_id(building_id)
            if not is_valid:
                return not_valid_response

            building = manager.get_building_by_id(building_id)

            if name is not None:
                if name == "" or not isinstance(name, str):
                    return response_handler.get_invalid_parameters_response("name")
            if building_picture:
                try:
                    result = cloudinary.uploader.upload(building_picture)
                    previous_image_public_id = building.building_picture.split('/')[-1].split('.')[0]
                    building.building_picture = result.get('secure_url')
                    if previous_image_public_id:
                        cloudinary.uploader.destroy(previous_image_public_id)
                except Exception as e:
                    return response_handler.get_internal_server_error_response("Failed to upload new building image")
            building = manager.update_building(building, name)
            serializer = serializers.BuildingSerializer(building, many=False)
            return response_handler.get_success_response(serializer.data)

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
            print(request_data)
            name = request_data.get("name")
            building_picture=request_data.get('building_picture')
            if name is None:
                return response_handler.get_missing_parameters_response("name")
            if name == "" or not isinstance(name, str):
                return response_handler.get_invalid_parameters_response("name")
            if building_picture:
                try:
                    result = cloudinary.uploader.upload(building_picture)
                    image_url = result.get('secure_url')
                except Exception as e:
                    return response_handler.get_internal_server_error_response("Failed to upload image")
            else:
                image_url = None
            building = manager.add_building(name,image_url)
            serializer = serializers.BuildingSerializer(building, many=False)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestTypes.UPDATE_EXISTING_BUILDING:
            building_id = request_data.get('id')
            name = request_data.get('name')
            building_picture=request_data.get('building_picture')
            is_valid, not_valid_response = validator.validate_building_id(building_id)
            if not is_valid:
                return not_valid_response

            building = manager.get_building_by_id(building_id)

            if name is not None:
                if name == "" or not isinstance(name, str):
                    return response_handler.get_invalid_parameters_response("name")
            if building_picture:
                try:
                    result = cloudinary.uploader.upload(building_picture)
                    previous_image_public_id = building.building_picture.split('/')[-1].split('.')[0]
                    building.building_picture = result.get('secure_url')
                    if previous_image_public_id:
                        cloudinary.uploader.destroy(previous_image_public_id)
                except Exception as e:
                    return response_handler.get_internal_server_error_response("Failed to upload new building image")
            building = manager.update_building(building, name)
            serializer = serializers.BuildingSerializer(building, many=False)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestTypes.REMOVE_EXISTING_BUILDING:
            building_id = request_data.get('id')
            is_valid, not_valid_response = validator.validate_building_id(building_id)
            if not is_valid:
                return not_valid_response
         
            building = manager.get_building_by_id(building_id)
            if building.building_picture:
                try:
                    public_id = building.building_picture.split('/')[-1].split('.')[0]
                    cloudinary.uploader.destroy(public_id)
                except Exception as e:
                    return response_handler.get_internal_server_error_response("Failed to delete building image")
            
            manager.delete_building(building_id)
            return response_handler.get_success_response(None)

        return response_handler.get_bad_request_response()
