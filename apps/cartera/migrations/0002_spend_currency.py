# Generated by Django 3.2.15 on 2022-09-29 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('general', '0001_initial'),
        ('cartera', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='spend',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='general.currency'),
        ),
    ]
