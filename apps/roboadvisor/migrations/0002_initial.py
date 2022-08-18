# Generated by Django 3.2.12 on 2022-08-11 18:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('roboadvisor', '0001_initial'),
        ('general', '0002_initial'),
        ('empresas', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='roboadvisoruserservicestepactivity',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='roboadvisoruserserviceactivity',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='roboadvisor.roboadvisorservice'),
        ),
        migrations.AddField(
            model_name='roboadvisoruserserviceactivity',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='roboadvisorservicestep',
            name='service_related',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='steps', to='roboadvisor.roboadvisorservice'),
        ),
        migrations.AddField(
            model_name='roboadvisorservice',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='general.category'),
        ),
        migrations.AddField(
            model_name='roboadvisorservice',
            name='tags',
            field=models.ManyToManyField(blank=True, to='general.Tag'),
        ),
        migrations.AddField(
            model_name='roboadvisorquestionstocksportfolio',
            name='service_activity',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='roboadvisor.roboadvisoruserserviceactivity'),
        ),
        migrations.AddField(
            model_name='roboadvisorquestionstocksportfolio',
            name='service_step',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='roboadvisor.roboadvisoruserservicestepactivity'),
        ),
        migrations.AddField(
            model_name='roboadvisorquestionstocksportfolio',
            name='stocks',
            field=models.ManyToManyField(to='roboadvisor.RoboAdvisorQuestionPortfolioComposition'),
        ),
        migrations.AddField(
            model_name='roboadvisorquestionstocksportfolio',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='roboadvisorquestionriskaversion',
            name='service_activity',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='roboadvisor.roboadvisoruserserviceactivity'),
        ),
        migrations.AddField(
            model_name='roboadvisorquestionriskaversion',
            name='service_step',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='roboadvisor.roboadvisoruserservicestepactivity'),
        ),
        migrations.AddField(
            model_name='roboadvisorquestionriskaversion',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='roboadvisorquestionportfoliocomposition',
            name='asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='empresas.company'),
        ),
        migrations.AddField(
            model_name='roboadvisorquestionportfoliocomposition',
            name='service_activity',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='roboadvisor.roboadvisoruserserviceactivity'),
        ),
        migrations.AddField(
            model_name='roboadvisorquestionportfoliocomposition',
            name='service_step',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='roboadvisor.roboadvisoruserservicestepactivity'),
        ),
        migrations.AddField(
            model_name='roboadvisorquestionportfoliocomposition',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='roboadvisorquestionportfolioassetsweight',
            name='service_activity',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='roboadvisor.roboadvisoruserserviceactivity'),
        ),
        migrations.AddField(
            model_name='roboadvisorquestionportfolioassetsweight',
            name='service_step',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='roboadvisor.roboadvisoruserservicestepactivity'),
        ),
        migrations.AddField(
            model_name='roboadvisorquestionportfolioassetsweight',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='roboadvisorquestioninvestorexperience',
            name='service_activity',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='roboadvisor.roboadvisoruserserviceactivity'),
        ),
        migrations.AddField(
            model_name='roboadvisorquestioninvestorexperience',
            name='service_step',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='roboadvisor.roboadvisoruserservicestepactivity'),
        ),
        migrations.AddField(
            model_name='roboadvisorquestioninvestorexperience',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='roboadvisorquestionfinancialsituation',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='general.currency'),
        ),
        migrations.AddField(
            model_name='roboadvisorquestionfinancialsituation',
            name='service_activity',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='roboadvisor.roboadvisoruserserviceactivity'),
        ),
        migrations.AddField(
            model_name='roboadvisorquestionfinancialsituation',
            name='service_step',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='roboadvisor.roboadvisoruserservicestepactivity'),
        ),
        migrations.AddField(
            model_name='roboadvisorquestionfinancialsituation',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='roboadvisorquestioncompanyanalysis',
            name='asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='empresas.company'),
        ),
        migrations.AddField(
            model_name='roboadvisorquestioncompanyanalysis',
            name='service_activity',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='roboadvisor.roboadvisoruserserviceactivity'),
        ),
        migrations.AddField(
            model_name='roboadvisorquestioncompanyanalysis',
            name='service_step',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='roboadvisor.roboadvisoruserservicestepactivity'),
        ),
        migrations.AddField(
            model_name='roboadvisorquestioncompanyanalysis',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='investorprofile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_investor_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
