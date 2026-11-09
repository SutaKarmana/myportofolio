from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Award, Experience, Project
from main.uploads import store_experience_thumbnail, validate_experience_thumbnail


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


class ExperienceSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    is_ongoing = serializers.BooleanField(read_only=True)
    thumbnail = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=200)
    thumbnail_source = serializers.ChoiceField(choices=["url", "upload"], required=False, write_only=True)
    thumbnail_file = serializers.FileField(
        required=False, write_only=True, validators=[validate_experience_thumbnail],
    )

    class Meta:
        model = Experience
        fields = [
            "id", "title", "description", "category", "category_display", "thumbnail",
            "started_at", "ended_at", "is_ongoing", "star_count", "is_starred",
            "thumbnail_source", "thumbnail_file",
        ]
        read_only_fields = ["id", "started_at"]

    def _clean_text(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Isian tidak boleh kosong atau hanya berisi HTML.")
        return value

    def validate_title(self, value):
        return self._clean_text(value)

    def validate_description(self, value):
        return self._clean_text(value)

    def validate_thumbnail(self, value):
        if not value:
            return value
        # Upload lama disimpan sebagai path lokal. Izinkan hanya nilai lama yang tidak diubah.
        if self.instance and value == self.instance.thumbnail and value.startswith("/static/img/experience-"):
            return value
        value = serializers.URLField().run_validation(value)
        if not value.lower().startswith(("http://", "https://")):
            raise serializers.ValidationError("URL harus menggunakan http:// atau https://.")
        return value

    def validate(self, attrs):
        source = attrs.get("thumbnail_source")
        upload = attrs.get("thumbnail_file")
        if source == "upload" and not upload:
            raise serializers.ValidationError({"thumbnail_file": ["Pilih file gambar untuk di-upload."]})
        if source == "url" and upload:
            raise serializers.ValidationError({"thumbnail_file": ["Pilih sumber Upload untuk mengirim berkas."]})
        return attrs

    def _prepare_thumbnail(self, validated_data):
        validated_data.pop("thumbnail_source", None)
        upload = validated_data.pop("thumbnail_file", None)
        if upload:
            validated_data["thumbnail"] = store_experience_thumbnail(upload)
        return validated_data

    def create(self, validated_data):
        return super().create(self._prepare_thumbnail(validated_data))

    def update(self, instance, validated_data):
        return super().update(instance, self._prepare_thumbnail(validated_data))

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        return bool(request and request.user.is_authenticated and request.user in obj.starred_by.all())


class ExperienceQuerySerializer(serializers.Serializer):
    q = serializers.CharField(required=False, allow_blank=True, default="", max_length=255)
    category = serializers.ChoiceField(choices=Experience.EXPERIENCE_CHOICES, allow_blank=True, default="")
