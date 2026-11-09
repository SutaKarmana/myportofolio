from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_experience_thumbnail(file):
    """Aturan upload yang sama untuk form lama dan serializer API Experience."""
    if not file:
        return
    header = file.read(12)
    file.seek(0)
    allowed = (
        header.startswith(b"\x89PNG\r\n\x1a\n")
        or header.startswith(b"\xff\xd8\xff")
        or header.startswith((b"GIF87a", b"GIF89a"))
        or (header.startswith(b"RIFF") and header[8:12] == b"WEBP")
    )
    extension = Path(file.name).suffix.lower()
    if not allowed or extension not in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
        raise ValidationError("Upload hanya menerima gambar PNG, JPG, GIF, atau WebP.")
    if file.size > 5 * 1024 * 1024:
        raise ValidationError("Ukuran gambar maksimal 5 MB.")


def store_experience_thumbnail(file):
    """Pertahankan lokasi upload lama; nama acak menghindari benturan nama berkas."""
    directory = Path(settings.BASE_DIR) / "static" / "img"
    directory.mkdir(parents=True, exist_ok=True)
    name = f"experience-{uuid4().hex}{Path(file.name).suffix.lower()}"
    with (directory / name).open("wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return f"/static/img/{name}"
