# Generated by Django 3.2.15 on 2022-10-29 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('super_investors', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='favoritessuperinvestorslist',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='favorites_superinvestors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='favoritessuperinvestorshistorial',
            name='superinvestor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='super_investors.superinvestor'),
        ),
        migrations.AddField(
            model_name='favoritessuperinvestorshistorial',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
