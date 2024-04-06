from core.user.models import User
from rest_framework import serializers
from .models import Repository, Category
from core.user.serializers import UserSerializer
from rest_framework.exceptions import ValidationError
from core.abstract.serializers import AbstractSerializer


class CategorySerializer(AbstractSerializer):
    class Meta:
        model = Category
        fields = ["name", "created_at", "updated_at"]


class RepositorySerializer(AbstractSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    creator_details = serializers.SerializerMethodField()

    class Meta:
        model = Repository
        fields = [
            "id",
            "title",
            "edited",
            "author",
            "creator",
            "category",
            "is_public",
            "created_at",
            "updated_at",
            "description",
            "creator_details",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "edited"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["category"] = CategorySerializer(instance.category).data
        return representation

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().update(instance, validated_data)

    def get_creator_details(self, instance):
        creator = instance.creator
        return UserSerializer(creator).data


# class RepositorySerializerV2(AbstractSerializer):
#     creator = serializers.SlugRelatedField(
#             queryset=User.objects.all(), slug_field="public_id"
#     )
#     creator = serializers.HiddenField(
#         default=serializers.CurrentUserDefault()
#     )
#     creator_details = serializers.SerializerMethodField()

#     class Meta:
#         model = Repository
#         fields = [
#             "id",
#             "title",
#             "edited",
#             "author",
#             "creator",
#             "creator_details",
#             "category",
#             "is_public",
#             "created_at",
#             "updated_at",
#             "description",
#         ]
#         read_only_fields = ["id", "created_at", "updated_at"]

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         creator = User.objects.get(public_id=representation["creator"])
#         representation["creator"] = UserSerializer(creator).data
#         representation["category"] = CategorySerializer(instance.category).data
#         return representation

#     def create(self, validated_data):
#         validated_data["creator"] = self.context["request"].user
#         return super().create(validated_data)

#     def get_creator_details(self, instance):
#         creator = instance.creator
#         return UserSerializer(creator).data
