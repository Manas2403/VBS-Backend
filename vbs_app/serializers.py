from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'email',
            'name',
            'parent',
            'require_parent_permission',
            'is_admin',
            'is_authority',
        )


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Building
        fields = (
            'id',
            'name',
            'building_picture',
        )


class VenueSerializer(serializers.ModelSerializer):
    building_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    authority_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = models.Venue
        fields = (
            'id',
            'name',
            'building_id',
            'floor_number',
            'venue_type',
            'is_accessible',
            'seating_capacity',
            'has_air_conditioner',
            'has_projectors',
            'has_speakers',
            'has_whiteboard',
            'authority_id',
        )


class BookingSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    venue_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = models.Booking
        fields = (
            'id',
            'user_id',
            'venue_id',
            'booking_time',
            'event_time',
            'last_updated_time',
            'booking_status',
            'booking_type',
            'event_duration',
            'expected_strength',
            'title',
            'description',
        )


class BookingRequestSerializer(serializers.ModelSerializer):
    booking_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    receiver_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = models.BookingRequest
        fields = (
            'id',
            'booking_id',
            'receiver_id',
            'request_status',
            'last_updated_time',
        )


class CommentsSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    booking_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = models.Comments
        fields = (
            'id',
            'comment_time',
            'user_id',
            'booking_id',
            'comment_content',
        )
class VHVenueSerializer(serializers.ModelSerializer):
    building_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    authority_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    
    class Meta:
        model = models.VHVenue    
        fields = (
            'id',
            'name',
            'floor_number',
            'building_id',
            'accomodation_type',
            'authority_id',
        )
class VHBookingSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    venue_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    class Meta:
        model = models.VHBooking
        fields = (
            'id',
            'user_id',
            'venue_id',
            'booking_time',
            'last_updated_time',
            'user_address',
            'user_contact',
            'arrival_time',
            'departure_time',
            'rooms_required',
            'booking_purpose',
            'booking_status',
            'booking_type',
            'requestby',
            'id_proof',
        )    

class VHBookingRequestSerializer(serializers.ModelSerializer):
    booking_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    receiver_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = models.VHBookingRequest
        fields = (
            'id',
            'booking_id',
            'receiver_id',
            'request_status',
            'last_updated_time',
        )

