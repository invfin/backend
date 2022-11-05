# Generated by Django 3.2.15 on 2022-11-04 22:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('seo', '0001_initial'),
        ('promotions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='users_clicked',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='promotion',
            name='visiteurs_clicked',
            field=models.ManyToManyField(blank=True, to='seo.Visiteur'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='categories',
            field=models.ManyToManyField(blank=True, to='classifications.Category'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='tags',
            field=models.ManyToManyField(blank=True, to='classifications.Tag'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='users_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='campaigns', to='users.userscategory'),
        ),
    ]
