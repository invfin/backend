# Generated by Django 3.2.12 on 2022-03-12 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('escritos', '0005_alter_term_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='term',
            options={'ordering': ['id'], 'verbose_name': 'Término del glosario'},
        ),
    ]
