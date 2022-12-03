# Generated by Django 3.2.15 on 2022-11-04 22:43

import src.general.mixins
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmailNotification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("date_sent", models.DateTimeField(auto_now_add=True)),
                ("opened", models.BooleanField(default=False)),
                ("date_opened", models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                "verbose_name": "Email from notifications",
                "db_table": "emails_notifications",
            },
            bases=(models.Model, src.general.mixins.BaseToAllMixin),
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("object_id", models.PositiveIntegerField()),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "notification_type",
                    models.CharField(
                        choices=[
                            ("Nuevo blog", "Nuevo blog"),
                            ("Nuevo comentario", "Nuevo comentario"),
                            ("Nuevo voto", "Nuevo voto"),
                            ("Nuevo seguidor", "Nuevo seguidor"),
                            ("Nueva pregunta", "Nueva pregunta"),
                            ("Nueva respuesta", "Nueva respuesta"),
                            ("Respuesta aceptada", "Respuesta aceptada"),
                            ("Compra efectuada", "Compra efectuada"),
                        ],
                        max_length=500,
                    ),
                ),
                ("is_seen", models.BooleanField(default=False)),
                (
                    "content_type",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="contenttypes.contenttype"),
                ),
            ],
            options={
                "verbose_name": "Notification",
                "db_table": "notifications",
            },
            bases=(models.Model, src.general.mixins.BaseToAllMixin),
        ),
    ]
