# Generated by Django 3.2.15 on 2022-09-29 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("business", "0002_initial"),
        ("api", "0002_termrequestapi_search"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("empresas", "0002_initial"),
        ("super_investors", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="termrequestapi",
            name="user",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="superinvestorrequestapi",
            name="key",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="api.key"),
        ),
        migrations.AddField(
            model_name="superinvestorrequestapi",
            name="search",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="super_investors.superinvestor"
            ),
        ),
        migrations.AddField(
            model_name="superinvestorrequestapi",
            name="user",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="reasonkeyrequested",
            name="user",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="key",
            name="subscription",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subscription_related",
                to="business.productsubscriber",
            ),
        ),
        migrations.AddField(
            model_name="key",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="api_key", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="endpoint",
            name="title_related",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="endpoints",
                to="api.endpointscategory",
            ),
        ),
        migrations.AddField(
            model_name="companyrequestapi",
            name="key",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="api.key"),
        ),
        migrations.AddField(
            model_name="companyrequestapi",
            name="search",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="empresas.company"
            ),
        ),
        migrations.AddField(
            model_name="companyrequestapi",
            name="user",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
