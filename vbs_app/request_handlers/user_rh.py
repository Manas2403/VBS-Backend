from .. import serializers, manager, response_handler, validator, google_token_handler
from ..request_handler import RequestHandler
from enum import Enum


class RequestTypes(Enum):
    GET_ALL_USERS = 0
    GET_USER_DETAILS = 1
    LOGIN_USER_USING_CREDENTIALS = 2
    ADD_NEW_USER = 3
    UPDATE_EXISTING_USER = 4
    REMOVE_EXISTING_USER = 5


class UserRequestHandler(RequestHandler):
    def _handle_get_request(self, request_type, request_params):
        if request_type == RequestTypes.GET_ALL_USERS:
            users = manager.get_all_users()
            serializer = serializers.UserSerializer(users, many=True)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestTypes.GET_USER_DETAILS:
            email = request_params.get('email')

            is_valid, not_valid_response = validator.validate_existing_user_email(email)
            if not is_valid:
                return not_valid_response

            user = manager.get_user_by_id(email)
            serializer = serializers.UserSerializer(user, many=False)
            return response_handler.get_success_response(serializer.data)

        return response_handler.get_bad_request_response()

    def _handle_post_request(self, request_type, request_data):
        if request_type == RequestTypes.LOGIN_USER_USING_CREDENTIALS:
            credential = request_data.get('credential')
            is_verified, email = google_token_handler.verify_oauth_token(credential)

            if not is_verified:
                return response_handler.get_invalid_parameters_response("credential")

            if not manager.check_user_exists(email):
                return response_handler.get_not_found_response("User")

            user = manager.get_user_by_id(email)
            serializer = serializers.UserSerializer(user)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestTypes.ADD_NEW_USER:
            email = request_data.get('email')
            name = request_data.get('name')
            parent = request_data.get('parent')
            require_parent_permission = request_data.get('require_parent_permission')
            is_admin = request_data.get('is_admin')
            is_authority = request_data.get('is_authority')

            is_valid, not_valid_response = validator.validate_new_user_email(email)
            if not is_valid:
                return not_valid_response

            if name is None:
                return response_handler.get_missing_parameters_response("name")
            if name == "" or not isinstance(name, str):
                return response_handler.get_invalid_parameters_response("name")

            is_parent_valid, not_valid_response = validator.validate_existing_user_email(parent)
            if not is_parent_valid:
                return not_valid_response

            if require_parent_permission is None:
                return response_handler.get_missing_parameters_response("require_parent_permission")
            if not isinstance(require_parent_permission, bool):
                return response_handler.get_invalid_parameters_response("require_parent_permission")

            if is_admin is None:
                return response_handler.get_missing_parameters_response("is_admin")
            if not isinstance(is_admin, bool):
                return response_handler.get_missing_parameters_response("is_admin")

            if is_authority is None:
                return response_handler.get_missing_parameters_response("is_authority")
            if not isinstance(is_authority, bool):
                return response_handler.get_invalid_parameters_response("is_authority")

            user = manager.add_new_user(email, name, parent, require_parent_permission, is_admin, is_authority)
            serializer = serializers.UserSerializer(user, many=False)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestTypes.UPDATE_EXISTING_USER:
            email = request_data.get('email')
            name = request_data.get('name')
            parent = request_data.get('parent')
            require_parent_permission = request_data.get('require_parent_permission')
            is_admin = request_data.get('is_admin')
            is_authority = request_data.get('is_authority')

            is_valid, not_valid_response = validator.validate_existing_user_email(email)
            if not is_valid:
                return not_valid_response

            user = manager.get_user_by_id(email)

            if parent is not None:
                is_parent_valid, not_valid_response = validator.validate_existing_user_email(parent)
                if not is_parent_valid:
                    return not_valid_response

            if name is not None:
                if name == "" or not isinstance(name, str):
                    return response_handler.get_invalid_parameters_response("name")

            if require_parent_permission is not None:
                if not isinstance(require_parent_permission, bool):
                    return response_handler.get_invalid_parameters_response("require_parent_permission")

            if is_admin is not None:
                if not isinstance(is_admin, bool):
                    return response_handler.get_missing_parameters_response("is_admin")

            if is_authority is not None:
                if not isinstance(is_authority, bool):
                    return response_handler.get_invalid_parameters_response("is_authority")

            user = manager.update_user(user, name, parent, require_parent_permission, is_admin, is_authority)

            serializer = serializers.UserSerializer(user, many=False)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestTypes.REMOVE_EXISTING_USER:
            email = request_data.get('email')

            is_valid, not_valid_response = validator.validate_existing_user_email(email)
            if not is_valid:
                return not_valid_response

            manager.delete_user(email)
            return response_handler.get_success_response(None)

        return response_handler.get_bad_request_response()
