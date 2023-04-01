from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=200, primary_key=True)
    name = models.CharField(max_length=50)
    parent = models.CharField(max_length=100, null=True)
    require_parent_permission = models.BooleanField(default=False)
    is_admin = models.BooleanField()
    is_authority = models.BooleanField()


class Building(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Venue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

    building_id = models.ForeignKey(Building, on_delete=models.SET_NULL, null=True)
    floor_number = models.IntegerField()

    is_accessible = models.BooleanField()

    seating_capacity = models.IntegerField()
    has_air_conditioner = models.BooleanField()
    has_projectors = models.BooleanField()
    has_speakers = models.BooleanField()
    has_whiteboard = models.BooleanField()

    authority_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    class BookingStatus(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        APPROVED = 'APPROVED', _('Approved')
        REJECTED = 'REJECTED', _('Rejected')
        CANCELLED = 'CANCELLED', _('Cancelled')
        AUTOMATICALLY_DECLINED = 'AUTOMATICALLY_DECLINED', _('Automatically Declined')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    venue_id = models.ForeignKey(Venue, on_delete=models.CASCADE)

    booking_time = models.DateTimeField()
    event_time = models.DateTimeField()
    last_updated_time = models.DateTimeField()

    booking_status = models.CharField(
        max_length=60,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
    )

    event_duration = models.IntegerField()
    expected_strength = models.IntegerField()
    description = models.TextField()


class BookingRequest(models.Model):
    class RequestStatus(models.TextChoices):
        PENDING_RECEIVE = 'PENDING_RECEIVE', _('Receive Pending')
        RECEIVED = 'RECEIVED', _('Received')
        REJECTED = 'REJECTED', _('Rejected')
        APPROVED = 'APPROVED', _('Approved')
        CANCELLED = 'CANCELLED', _('Cancelled')
        AUTOMATICALLY_DECLINED = 'AUTOMATICALLY_DECLINED', _('Automatically Declined')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    receiver_id = models.ForeignKey(User, on_delete=models.CASCADE)

    request_status = models.CharField(
        max_length=60,
        choices=RequestStatus.choices,
        default=RequestStatus.PENDING_RECEIVE,
    )

    last_updated_time = models.DateTimeField()


class Comments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment_time = models.DateTimeField()
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    comment_content = models.TextField()
