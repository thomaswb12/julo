from rest_framework import serializers

class SignInSerializer(serializers.Serializer):
    customer_xid = serializers.UUIDField(required=True)