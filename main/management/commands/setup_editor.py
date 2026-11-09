from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = "Menyiapkan permission grup Editor untuk Awards dan Experience."

    @transaction.atomic
    def handle(self, *args, **options):
        permissions = list(Permission.objects.filter(
            content_type__app_label="main",
            codename__in=["change_award", "change_experience"],
        ))
        if len(permissions) != 2:
            raise CommandError("Permission belum tersedia. Jalankan migrate terlebih dahulu.")

        group, _ = Group.objects.get_or_create(name="Editor")
        # Tambahkan izin edit tanpa menghapus permission lama atau mengubah anggota grup.
        group.permissions.add(*permissions)
        self.stdout.write(self.style.SUCCESS("Permission Editor untuk Awards dan Experience siap."))
