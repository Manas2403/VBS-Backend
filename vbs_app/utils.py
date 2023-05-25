import uuid
import re
from datetime import datetime, timedelta, timezone
import pytz
import dateutil


def is_valid_uuid(input_id):
    try:
        uuid.UUID(str(input_id))
        return True
    except ValueError:
        return False


def is_valid_email(email):
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.match(pat, email):
        return False
    domain = re.search(r'@((\w+?\.)+\w+)', email).group(1)
    if domain != "iiita.ac.in":
        return False
    return True


def get_datetime_from_iso(iso_time):
    try:
        event_time = datetime.fromisoformat(str(iso_time))
        return True, event_time
    except ValueError:
        try:
            event_time = datetime.fromisoformat(str(iso_time)[:-1])
            return True, event_time
        except ValueError:
            return False, None


def is_valid_time_and_duration(event_time, duration):
    start_time = event_time
    end_time = event_time + timedelta(minutes=duration)
    return start_time.day == end_time.day and start_time.month == end_time.month and start_time.year == end_time.year


def is_time_overlapping(start_time_1, duration_1, start_time_2, duration_2):
    utc = pytz.UTC

    start_time_1 = start_time_1.replace(tzinfo=utc)
    start_time_2 = start_time_2.replace(tzinfo=utc)

    end_time_1 = start_time_1 + timedelta(minutes=duration_1)
    end_time_2 = start_time_2 + timedelta(minutes=duration_2)

    if start_time_1 < start_time_2:
        if end_time_1 > start_time_2:
            return True
        else:
            return False
    elif start_time_1 == start_time_2:
        return True
    else:
        if start_time_1 < end_time_2:
            return True
        else:
            return False
