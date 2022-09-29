<<<<<<< HEAD
# Generated by Django 3.2.15 on 2022-09-29 15:29
=======
# Generated by Django 3.2.15 on 2022-09-29 15:33
>>>>>>> 3f643cc69432aef628d5b1cec721aaa8492f8a8d

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('general', '0001_initial'),
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionhistorial',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='general.currency'),
        ),
        migrations.AddField(
            model_name='transactionhistorial',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.customer'),
        ),
        migrations.AddField(
            model_name='transactionhistorial',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.productdiscount'),
        ),
        migrations.AddField(
            model_name='transactionhistorial',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.product'),
        ),
        migrations.AddField(
            model_name='transactionhistorial',
            name='product_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.productcomment'),
        ),
        migrations.AddField(
            model_name='transactionhistorial',
            name='product_complementary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.productcomplementary'),
        ),
        migrations.AddField(
            model_name='stripewebhookresponse',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.customer'),
        ),
        migrations.AddField(
            model_name='stripewebhookresponse',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.product'),
        ),
        migrations.AddField(
            model_name='stripewebhookresponse',
            name='product_complementary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.productcomplementary'),
        ),
        migrations.AddField(
            model_name='productsubscriber',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscribers', to='business.product'),
        ),
        migrations.AddField(
            model_name='productsubscriber',
            name='product_complementary',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='complementary_subs', to='business.productcomplementary'),
        ),
    ]
