from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from core.models import Bb, AdvUser
from api.models import Outfit


class OutfitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outfit
        fields = ("id", "title", "price", "image", "author", "likes")


class BbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bb
        fields = "__all__"


class HistorySerializer(serializers.Serializer):
    changed_field = serializers.CharField(read_only=True)
    old = serializers.CharField(read_only=True)
    new = serializers.CharField(read_only=True)
    change_by = serializers.CharField(read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        last_change = instance.order_by("history_date").last()
        delta = last_change.diff_against(last_change.prev_record)
        for change in delta.changes:
            ret.update(
                {
                    "changed_field": change.field,
                    "old": change.old,
                    "new": change.new,
                    "change_by": last_change.history_user.username
                    if last_change.history_user
                    else None,
                }
            )

        return ret


class BbDetailSerializer(serializers.ModelSerializer):
    change_history = HistorySerializer(many=True, read_only=True)

    class Meta:
        model = Bb
        fields = (
            "id",
            "category",
            "title",
            "content",
            "price",
            "contacts",
            "image",
            "author",
            "is_active",
            "created_at",
            "change_history",
            "views",
        )
        depth = 1

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["change_history"] = HistorySerializer(instance=instance.history.all()).data
        return ret


class ListBbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bb
        fields = (
            "id",
            "title",
            "content",
            "price",
            "created_at",
            "contacts",
            "image",
            "owner_last_login",
        )

    owner_last_login = serializers.DateTimeField()


class AdvUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = AdvUser
        fields = ("old_password", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def validate_old_password(self, value):
        user = self.instance
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def update(self, instance, validated_data, *args, **kwargs):

        instance.set_password(validated_data["password"])
        instance.save()

        return instance
