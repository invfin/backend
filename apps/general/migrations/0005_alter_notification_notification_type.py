# Generated by Django 3.2.15 on 2022-08-30 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0004_alter_period_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('Nuevo blog', 'Nuevo blog'), ('Nuevo comentario', 'Nuevo comentario'), ('Nuevo voto', 'Nuevo voto'), ('Nuevo seguidor', 'Nuevo seguidor'), ('Nueva pregunta', 'Nueva pregunta'), ('Nueva respuesta', 'Nueva respuesta'), ('Respuesta aceptada', 'Respuesta aceptada'), ('Compra efectuada', 'Compra efectuada')], max_length=500),
        ),
    ]
