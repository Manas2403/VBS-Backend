from rest_framework.parsers import JSONParser
from . import response_handler, google_token_handler


class RequestHandler:

    def handle_request(self, request, request_type, request_params=None):
        auth_token = request.headers.get('Authorization')
        is_verified, email = google_token_handler.verify_id_token(auth_token)

        if not is_verified:
            return response_handler.get_invalid_token_response()

        if request.method == 'GET':
            return self._handle_get_request(request_type, request_params)

        if request.method == 'POST':
            request_data = JSONParser().parse(request)
            if request_data is None:
                return response_handler.get_bad_request_response()
            return self._handle_post_request(request_type, request_data,request.headers)

    def handle_login_request(self, request, request_type):
        request_data = JSONParser().parse(request)
        if request_data is None:
            return response_handler.get_bad_request_response()
        return self._handle_post_request(request_type, request_data, request.headers)

    def _handle_get_request(self, request_type, request_params):
        return response_handler.get_bad_request_response()

    def _handle_post_request(self, request_type, request_data):
        return response_handler.get_bad_request_response()
