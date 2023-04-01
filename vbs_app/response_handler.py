from rest_framework import status
from rest_framework.response import Response

from . import response


def get_bad_request_response():
    return get_error_response(status.HTTP_400_BAD_REQUEST, "Invalid Request")


def get_missing_parameters_response(parameter_name):
    return get_error_response(status.HTTP_400_BAD_REQUEST, f"Required Parameter ({parameter_name}) not found")


def get_invalid_parameters_response(parameter_name):
    return get_error_response(status.HTTP_400_BAD_REQUEST, f"Parameter provided ({parameter_name}) is invalid")


def get_not_found_response(model_type):
    return get_error_response(status.HTTP_404_NOT_FOUND, f"Given {model_type} not Found")


def get_already_exists_response(model_type):
    return get_error_response(status.HTTP_403_FORBIDDEN, f"{model_type} already exists!")


def get_serializer_error_response(serializer):
    return get_error_response(status.HTTP_400_BAD_REQUEST, "Invalid Request Type", serializer.errors)


def get_error_response(status_code, status_message, response_data=None):
    error_response = response.ResponseData()

    error_response.response_status = "FAILED"
    error_response.response_message = status_message
    error_response.response_data = response_data

    serializer = response.ResponseSerializer(error_response)
    return Response(serializer.data, status=status_code)


def get_success_response(response_data, response_message="Request processed successfully"):
    success_response = response.ResponseData()

    success_response.response_status = "SUCCESS"
    success_response.response_message = response_message
    success_response.response_data = response_data

    serializer = response.ResponseSerializer(success_response)
    return Response(serializer.data, status=status.HTTP_200_OK)
