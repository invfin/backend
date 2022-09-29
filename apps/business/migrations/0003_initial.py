<<<<<<< HEAD
# Generated by Django 3.2.15 on 2022-09-29 15:29
=======
# Generated by Django 3.2.15 on 2022-09-29 15:33
>>>>>>> 3f643cc69432aef628d5b1cec721aaa8492f8a8d

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
<<<<<<< HEAD
        ('business', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0001_initial'),
=======
>>>>>>> 3f643cc69432aef628d5b1cec721aaa8492f8a8d
        ('general', '0001_initial'),
        ('web', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsubscriber',
            name='subscriber',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productdiscount',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.product'),
        ),
        migrations.AddField(
            model_name='productdiscount',
            name='product_complementary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.productcomplementary'),
        ),
        migrations.AddField(
            model_name='productdiscount',
            name='promotion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='promotion_discount', to='web.promotion'),
        ),
        migrations.AddField(
            model_name='productcomplementarypaymentlink',
            name='product_complementary',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_links', to='business.productcomplementary'),
        ),
        migrations.AddField(
            model_name='productcomplementarypaymentlink',
            name='promotion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='promotion_link_payment', to='web.promotion'),
        ),
        migrations.AddField(
            model_name='productcomplementary',
            name='currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='general.currency'),
        ),
        migrations.AddField(
            model_name='productcomplementary',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='complementary', to='business.product'),
        ),
        migrations.AddField(
            model_name='productcomment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productcomment',
            name='content_related',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_related', to='business.product'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
