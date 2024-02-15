from rest_framework import serializers


class AbstractSerializer(serializers.ModelSerializer):
    """Every serializer contains id, created and updated fields."""
    id = serializers.UUIDField(source="public_id", read_only=True, format="hex")
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
