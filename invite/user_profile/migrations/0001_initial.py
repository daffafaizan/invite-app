# Generated by Django 4.2.7 on 2023-12-01 13:33

from django.conf import settings
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
            name='UlasanProfil',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('rating', models.PositiveIntegerField(default=0)),
                ('deskripsi_kerja_setim', models.TextField()),
                ('ulasan', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('diulas', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='diulas', to=settings.AUTH_USER_MODEL)),
                ('pengulas', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pengulas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
