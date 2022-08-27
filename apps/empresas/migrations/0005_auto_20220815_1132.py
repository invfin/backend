# Generated by Django 3.2.15 on 2022-08-15 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0004_auto_20220814_1717'),
    ]

    operations = [
        migrations.RenameField(
            model_name='balancesheetfinprep',
            old_name='common_stocks',
            new_name='common_stock',
        ),
        migrations.RenameField(
            model_name='balancesheetfinprep',
            old_name='property_plant_equipment',
            new_name='total_liabilities_and_stockholders_equity',
        ),
        migrations.RenameField(
            model_name='cashflowstatementfinprep',
            old_name='accounts_payable',
            new_name='accounts_payables',
        ),
        migrations.RenameField(
            model_name='cashflowstatementfinprep',
            old_name='capex',
            new_name='capital_expenditure',
        ),
        migrations.RenameField(
            model_name='cashflowstatementfinprep',
            old_name='cash_beginning_period',
            new_name='cash_at_beginning_of_period',
        ),
        migrations.RenameField(
            model_name='cashflowstatementfinprep',
            old_name='cash_end_period',
            new_name='cash_at_end_of_period',
        ),
        migrations.RenameField(
            model_name='cashflowstatementfinprep',
            old_name='depreciation_amortization',
            new_name='depreciation_and_amortization',
        ),
        migrations.RenameField(
            model_name='cashflowstatementfinprep',
            old_name='effect_forex_exchange',
            new_name='effect_of_forex_changes_on_cash',
        ),
        migrations.RenameField(
            model_name='cashflowstatementfinprep',
            old_name='fcf',
            new_name='free_cash_flow',
        ),
        migrations.RenameField(
            model_name='cashflowstatementfinprep',
            old_name='financing_activities_cf',
            new_name='investments_in_property_plant_and_equipment',
        ),
        migrations.RenameField(
            model_name='cashflowstatementfinprep',
            old_name='investing_activities_cf',
            new_name='net_cash_provided_by_operating_activities',
        ),
        migrations.RenameField(
            model_name='cashflowstatementfinprep',
            old_name='investments_property_plant_equipment',
            new_name='net_cash_used_for_investing_activites',
        ),
        migrations.RenameField(
            model_name='cashflowstatementfinprep',
            old_name='net_change_cash',
            new_name='net_cash_used_provided_by_financing_activities',
        ),
        migrations.RenameField(
            model_name='cashflowstatementfinprep',
            old_name='operating_activities_cf',
            new_name='net_change_in_cash',
        ),
        migrations.RenameField(
            model_name='cashflowstatementfinprep',
            old_name='operating_cf',
            new_name='operating_cash_flow',
        ),
        migrations.RenameField(
            model_name='cashflowstatementfinprep',
            old_name='other_financing_activities',
            new_name='other_financing_activites',
        ),
        migrations.RenameField(
            model_name='cashflowstatementfinprep',
            old_name='purchases_investments',
            new_name='purchases_of_investments',
        ),
        migrations.RenameField(
            model_name='cashflowstatementfinprep',
            old_name='sales_maturities_investments',
            new_name='sales_maturities_of_investments',
        ),
        migrations.RenameField(
            model_name='cashflowstatementfinprep',
            old_name='stock_based_compesation',
            new_name='stock_based_compensation',
        ),
        migrations.RenameField(
            model_name='incomestatementfinprep',
            old_name='depreciation_amortization',
            new_name='depreciation_and_amortization',
        ),
        migrations.RenameField(
            model_name='incomestatementfinprep',
            old_name='general_administrative_expenses',
            new_name='general_and_administrative_expenses',
        ),
        migrations.RenameField(
            model_name='incomestatementfinprep',
            old_name='income_tax_expenses',
            new_name='income_tax_expense',
        ),
        migrations.RenameField(
            model_name='incomestatementfinprep',
            old_name='net_total_other_income_expenses',
            new_name='interest_income',
        ),
        migrations.RenameField(
            model_name='incomestatementfinprep',
            old_name='rd_expenses',
            new_name='research_and_development_expenses',
        ),
        migrations.RenameField(
            model_name='incomestatementfinprep',
            old_name='selling_marketing_expenses',
            new_name='selling_and_marketing_expenses',
        ),
        migrations.RenameField(
            model_name='incomestatementfinprep',
            old_name='sga_expenses',
            new_name='selling_general_and_administrative_expenses',
        ),
        migrations.RenameField(
            model_name='incomestatementfinprep',
            old_name='weighted_average_diluated_shares_outstanding',
            new_name='total_other_income_expenses_net',
        ),
        migrations.RenameField(
            model_name='incomestatementfinprep',
            old_name='weighted_average_shares_outstanding',
            new_name='weighted_average_shs_out',
        ),
        migrations.AddField(
            model_name='balancesheetfinprep',
            name='calendar_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='balancesheetfinprep',
            name='cik',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='balancesheetfinprep',
            name='symbol',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='cashflowstatementfinprep',
            name='calendar_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cashflowstatementfinprep',
            name='cik',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cashflowstatementfinprep',
            name='symbol',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='incomestatementfinprep',
            name='calendar_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='incomestatementfinprep',
            name='cik',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='incomestatementfinprep',
            name='symbol',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='incomestatementfinprep',
            name='weighted_average_shs_out_dil',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
