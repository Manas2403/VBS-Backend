from . import response_handler, utils, manager, models


def validate_building_id(building_id):
    if building_id is None:
        return False, response_handler.get_missing_parameters_response("building_id")
    if not utils.is_valid_uuid(building_id):
        return False, response_handler.get_invalid_parameters_response("building_id")
    if not manager.check_building_exists(building_id):
        return False, response_handler.get_not_found_response("Building")
    return True, None


def validate_existing_user_email(email):
    if email is None:
        return False, response_handler.get_missing_parameters_response("user")
    if not utils.is_valid_email(email):
        return False, response_handler.get_invalid_parameters_response("user")
    if not manager.check_user_exists(email):
        return False, response_handler.get_not_found_response("User")
    return True, None


def validate_new_user_email(email):
    if email is None:
        return False, response_handler.get_missing_parameters_response("user")
    if not utils.is_valid_email(email):
        return False, response_handler.get_invalid_parameters_response("user")
    if manager.check_user_exists(email):
        return False, response_handler.get_already_exists_response("User")
    return True, None


def validate_venue_id(venue_id):
    if venue_id is None:
        return False, response_handler.get_missing_parameters_response("venue_id")
    if not utils.is_valid_uuid(venue_id):
        return False, response_handler.get_invalid_parameters_response("venue_id")
    if not manager.check_venue_exists(venue_id):
        return False, response_handler.get_not_found_response("Venue")
    return True, None


def validate_venue_type(venue_type):
    if venue_type is None:
        return False, response_handler.get_missing_parameters_response("venue_type")
    if venue_type not in models.Venue.VenueType.names:
        return False, response_handler.get_invalid_parameters_response("venue_type")
    return True, None


def validate_booking_id(booking_id):
    if booking_id is None:
        return False, response_handler.get_missing_parameters_response("booking_id")
    if not utils.is_valid_uuid(booking_id):
        return False, response_handler.get_invalid_parameters_response("booking_id")
    if not manager.check_booking_exists(booking_id):
        return False, response_handler.get_not_found_response("Booking")
    return True, None


def validate_booking_type(booking_type):
    if booking_type is None:
        return False, response_handler.get_missing_parameters_response("booking_type")
    if booking_type not in models.Booking.BookingType.names:
        return False, response_handler.get_invalid_parameters_response("booking_type")
    return True, None


def validate_booking_request_id(booking_request_id):
    if booking_request_id is None:
        return False, response_handler.get_missing_parameters_response("booking_request_id")
    if not utils.is_valid_uuid(booking_request_id):
        return False, response_handler.get_invalid_parameters_response("booking_request_id")
    if not manager.check_booking_request_exists(booking_request_id):
        return False, response_handler.get_not_found_response("Booking Request")
    return True, None


def validate_comment_id(comment_id):
    if comment_id is None:
        return False, response_handler.get_missing_parameters_response("comment_id")
    if not utils.is_valid_uuid(comment_id):
        return False, response_handler.get_invalid_parameters_response("comment_id")
    if not manager.check_comment_exists(comment_id):
        return False, response_handler.get_not_found_response("Comment")
    return True, None
