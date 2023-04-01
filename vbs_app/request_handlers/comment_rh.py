from .. import serializers, manager, response_handler, validator
from ..request_handler import RequestHandler
from enum import Enum


class RequestType(Enum):
    GET_COMMENTS_BY_USER = 0
    GET_COMMENTS_BY_BOOKING = 1
    GET_COMMENT = 2
    ADD_NEW_COMMENT = 3


class CommentsRequestHandler(RequestHandler):
    def _handle_get_request(self, request_type, request_params):
        if request_type == RequestType.GET_COMMENTS_BY_USER:
            user_id = request_params.get("user_id")

            is_valid, not_valid_response = validator.validate_existing_user_email(user_id)
            if not is_valid:
                return not_valid_response

            comments = manager.get_comments_by_user(user_id)
            serializer = serializers.CommentsSerializer(comments, many=True)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestType.GET_COMMENTS_BY_BOOKING:
            booking_id = request_params.get("booking_id")

            is_valid, not_valid_response = validator.validate_booking_id(booking_id)
            if not is_valid:
                return not_valid_response

            comments = manager.get_comments_by_booking(booking_id)
            serializer = serializers.CommentsSerializer(comments, many=True)
            return response_handler.get_success_response(serializer.data)

        if request_type == RequestType.GET_COMMENT:
            comment_id = request_params.get("comment_id")

            is_valid, not_valid_response = validator.validate_comment_id(comment_id)
            if not is_valid:
                return not_valid_response

            comment = manager.get_comment_by_id(comment_id)
            serializer = serializers.CommentsSerializer(comment, many=False)
            return response_handler.get_success_response(serializer.data)

        return response_handler.get_bad_request_response()

    def _handle_post_request(self, request_type, request_data):
        if request_type == RequestType.ADD_NEW_COMMENT:
            user_id = request_data.get("user_id")
            booking_id = request_data.get("booking_id")
            comment_content = request_data.get("comment_content")

            is_valid, not_valid_response = validator.validate_existing_user_email(user_id)
            if not is_valid:
                return not_valid_response

            is_valid, not_valid_response = validator.validate_booking_id(booking_id)
            if not is_valid:
                return not_valid_response

            if comment_content is None:
                return response_handler.get_missing_parameters_response("comment_content")
            if comment_content == "" or not isinstance(comment_content, str):
                return response_handler.get_invalid_parameters_response("comment_content")

            comment = manager.add_comment(user_id, booking_id, comment_content)
            serializer = serializers.CommentsSerializer(comment, many=False)
            return response_handler.get_success_response(serializer.data, "Comment added successfully")

        return response_handler.get_bad_request_response()
