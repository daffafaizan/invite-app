# Generated by Django 4.2.7 on 2023-12-02 07:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UlasanProfil",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("rating", models.PositiveIntegerField(default=0)),
                (
                    "deskripsi_kerja_setim",
                    models.TextField(
                        validators=[
                            django.core.validators.MinLengthValidator(3),
                            django.core.validators.MaxLengthValidator(1000),
                        ]
                    ),
                ),
                (
                    "ulasan",
                    models.TextField(
                        validators=[
                            django.core.validators.MinLengthValidator(15),
                            django.core.validators.MaxLengthValidator(2000),
                        ]
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "diulas",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_diulas",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "pengulas",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_pengulas",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
