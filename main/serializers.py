from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Award, Project


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "tech_stack",
            "project_url", "project_image_url",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_tech_stack(self, value):
        return strip_tags(value)

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class AwardSerializer(serializers.ModelSerializer):
    """Like adalah padanan star Awards; identitas pemberinya tidak diekspos."""

    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Award
        fields = [
            "id", "title", "issuer", "year", "thumbnail", "certificate_url",
            "like_count", "is_liked",
        ]
        read_only_fields = ["id"]

    def _clean_text(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Isian tidak boleh kosong atau hanya berisi HTML.")
        return value

    def validate_title(self, value):
        return self._clean_text(value)

    def validate_issuer(self, value):
        return self._clean_text(value)

    def _validate_web_url(self, value):
        # URLField memeriksa struktur URL; batasi juga skema yang boleh ditampilkan.
        if value and not value.lower().startswith(("https://", "http://")):
            raise serializers.ValidationError("URL harus menggunakan http:// atau https://.")
        return value

    def validate_thumbnail(self, value):
        return self._validate_web_url(value)

    def validate_certificate_url(self, value):
        return self._validate_web_url(value)

    def get_like_count(self, obj):
        return obj.liked_by.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.liked_by.all()


class AwardQuerySerializer(serializers.Serializer):
    """Validasi query string memakai aturan yang sama untuk semua klien API."""

    q = serializers.CharField(required=False, allow_blank=True, default="", max_length=255)
    year = serializers.IntegerField(required=False, min_value=0, max_value=2147483647)
    ordering = serializers.ChoiceField(
        choices=["-year", "year", "title"], default="-year",
    )
