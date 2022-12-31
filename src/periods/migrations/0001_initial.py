# Generated by Django 3.2.15 on 2022-12-31 14:33

from django.db import migrations, models
import src.general.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('period', models.IntegerField(blank=True, choices=[(1, '1 Quarter'), (2, '2 Quarter'), (3, '3 Quarter'), (4, '4 Quarter'), (5, 'For Year')], null=True)),
            ],
            options={
                'verbose_name': 'Period',
                'verbose_name_plural': 'Periods',
                'db_table': 'assets_periods',
                'ordering': ['-year', '-period'],
                'get_latest_by': ['-year', '-period'],
            },
            bases=(models.Model, src.general.mixins.BaseToAllMixin),
        ),
    ]
