from rest_framework import status
from rest_framework.response import Response

from . import response


def get_bad_request_response():
    return get_error_response(status.HTTP_400_BAD_REQUEST, "Invalid Request")


def get_invalid_token_response():
    return get_error_response(status.HTTP_401_UNAUTHORIZED, "Unauthorized Access")


def get_missing_parameters_response(parameter_name):
    return get_error_response(status.HTTP_400_BAD_REQUEST, f"Required Parameter ({parameter_name}) not found")

def get_out_of_college_email_response(parameter_name):
    return get_error_response(status.HTTP_400_BAD_REQUEST, f"Email provided ({parameter_name}) is not a college email")

def get_invalid_parameters_response(parameter_name):
    return get_error_response(status.HTTP_400_BAD_REQUEST, f"Parameter provided ({parameter_name}) is invalid")


def get_not_found_response(model_type):
    return get_error_response(status.HTTP_404_NOT_FOUND, f"Given {model_type} not Found")


def get_already_exists_response(model_type):
    return get_error_response(status.HTTP_403_FORBIDDEN, f"{model_type} already exists!")


def get_error_response(status_code, status_message):
    error_response = response.ResponseData()

    error_response.response_message = status_message

    serializer = response.ResponseSerializer(error_response)
    return Response(serializer.data, status=status_code)


def get_success_response(response_data):
    success_response = response.ResponseData()

    success_response.response_data = response_data

    serializer = response.ResponseSerializer(success_response)
    return Response(serializer.data, status=status.HTTP_200_OK)

def get_internal_server_error_response(message="Internal Server Error"):
    return get_error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, message)
