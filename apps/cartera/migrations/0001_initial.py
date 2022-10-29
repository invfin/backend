# Generated by Django 3.2.15 on 2022-10-29 10:51

import apps.general.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('is_stock', models.BooleanField(default=False)),
                ('is_etf', models.BooleanField(default=False)),
                ('is_crypto', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Asset',
                'verbose_name_plural': 'Assets',
                'db_table': 'cartera_assets',
            },
        ),
        migrations.CreateModel(
            name='CashflowMovementCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, verbose_name='Nombre')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Cashflow category',
                'verbose_name_plural': 'Cashflow categories',
                'db_table': 'cartera_cashflow_category',
            },
        ),
        migrations.CreateModel(
            name='FinancialObjectif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, verbose_name='Nombre')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_to_achieve', models.DateTimeField(blank=True, null=True)),
                ('date_achived', models.DateTimeField(blank=True, null=True)),
                ('observation', models.TextField(default='', verbose_name='Observaciones')),
                ('accomplished', models.BooleanField(default=False)),
                ('abandoned', models.BooleanField(default=False)),
                ('percentage', models.DecimalField(decimal_places=2, default=0, max_digits=100, verbose_name='Porcentaje')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=100, verbose_name='Monto')),
                ('is_rule', models.BooleanField(default=False)),
                ('rule_ends', models.BooleanField(default=False)),
                ('requirement', models.JSONField(default=dict)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Objetivo financiero',
                'verbose_name_plural': 'Objetivo financieros',
                'db_table': 'cartera_objectives',
                'ordering': ['date_created'],
            },
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, verbose_name='Nombre')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=100, verbose_name='Monto')),
                ('description', models.TextField(default='', verbose_name='Descripción')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Fecha del movimiento')),
                ('is_recurrent', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Income',
                'verbose_name_plural': 'Incomes',
                'db_table': 'cartera_income',
            },
        ),
        migrations.CreateModel(
            name='Patrimonio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Patrimonio',
                'verbose_name_plural': 'Patrimonios',
                'db_table': 'cartera_patrimoine',
            },
            bases=(models.Model, apps.general.utils.ChartSerializer),
        ),
        migrations.CreateModel(
            name='PositionMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('move_type', models.IntegerField(blank=True, choices=[(1, 'Compra'), (2, 'Venta')], null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=100, verbose_name='Precio')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Fecha del movimiento')),
                ('quantity', models.IntegerField(default=0, verbose_name='Cantidad')),
                ('observacion', models.TextField(default='', verbose_name='Observaciones')),
                ('fee', models.DecimalField(decimal_places=2, default=0, max_digits=100, verbose_name='Comisión')),
            ],
            options={
                'verbose_name': 'Position movement',
                'verbose_name_plural': 'Position movements',
                'db_table': 'cartera_movements',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Spend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, verbose_name='Nombre')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=100, verbose_name='Monto')),
                ('description', models.TextField(default='', verbose_name='Descripción')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Fecha del movimiento')),
                ('is_recurrent', models.BooleanField(default=False)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cartera.cashflowmovementcategory')),
            ],
            options={
                'verbose_name': 'Spend',
                'verbose_name_plural': 'Spends',
                'db_table': 'cartera_spend',
            },
        ),
    ]
