from rest_framework import serializers


class ResponseData:
    response_status = ""
    response_message = ""
    response_data = None


class ResponseSerializer(serializers.Serializer):
    response_status = serializers.CharField(max_length=10)
    response_message = serializers.CharField(max_length=200)
    response_data = serializers.JSONField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {k: v for k, v in data.items() if v is not None}
