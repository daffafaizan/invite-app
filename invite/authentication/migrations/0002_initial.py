# Generated by Django 4.2.7 on 2023-12-11 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("authentication", "0001_initial"),
        ("find_members", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="registereduser",
            name="bookmarked_lowongans",
            field=models.ManyToManyField(blank=True, to="find_members.lowonganregu"),
        ),
        migrations.AddField(
            model_name="registereduser",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                related_name="user_set",
                related_query_name="user",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="registereduser",
            name="profile_details",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="authentication.profiledetails",
            ),
        ),
        migrations.AddField(
            model_name="registereduser",
            name="tautan_media_sosial",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="authentication.tautanmediasosial",
            ),
        ),
        migrations.AddField(
            model_name="registereduser",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
    ]
