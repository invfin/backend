# Generated by Django 3.2.15 on 2022-12-31 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('empresas', '0001_initial'),
        ('escritos', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('preguntas_respuestas', '0002_initial'),
        ('seo', '0001_initial'),
        ('public_blog', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='visiteuruserrelation',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='visiteuruserrelation',
            name='visiteur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='seo.visiteur'),
        ),
        migrations.AddField(
            model_name='visiteurtermvisited',
            name='model_visited',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='escritos.term'),
        ),
        migrations.AddField(
            model_name='visiteurtermvisited',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seo.visiteur'),
        ),
        migrations.AddField(
            model_name='visiteurtermvisited',
            name='visit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seo.visiteurjourney'),
        ),
        migrations.AddField(
            model_name='visiteurquestionvisited',
            name='model_visited',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='preguntas_respuestas.question'),
        ),
        migrations.AddField(
            model_name='visiteurquestionvisited',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seo.visiteur'),
        ),
        migrations.AddField(
            model_name='visiteurquestionvisited',
            name='visit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seo.visiteurjourney'),
        ),
        migrations.AddField(
            model_name='visiteurpublicblogvisited',
            name='model_visited',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='public_blog.publicblog'),
        ),
        migrations.AddField(
            model_name='visiteurpublicblogvisited',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seo.visiteur'),
        ),
        migrations.AddField(
            model_name='visiteurpublicblogvisited',
            name='visit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seo.visiteurjourney'),
        ),
        migrations.AddField(
            model_name='visiteurjourney',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='journeys', to='seo.visiteur'),
        ),
        migrations.AddField(
            model_name='visiteurcompanyvisited',
            name='model_visited',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='empresas.company'),
        ),
        migrations.AddField(
            model_name='visiteurcompanyvisited',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seo.visiteur'),
        ),
        migrations.AddField(
            model_name='visiteurcompanyvisited',
            name='visit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seo.visiteurjourney'),
        ),
        migrations.AddField(
            model_name='usertermvisited',
            name='model_visited',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='escritos.term'),
        ),
        migrations.AddField(
            model_name='usertermvisited',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usertermvisited',
            name='visit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seo.userjourney'),
        ),
        migrations.AddField(
            model_name='userquestionvisited',
            name='model_visited',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='preguntas_respuestas.question'),
        ),
        migrations.AddField(
            model_name='userquestionvisited',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userquestionvisited',
            name='visit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seo.userjourney'),
        ),
        migrations.AddField(
            model_name='userpublicblogvisited',
            name='model_visited',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='public_blog.publicblog'),
        ),
        migrations.AddField(
            model_name='userpublicblogvisited',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userpublicblogvisited',
            name='visit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seo.userjourney'),
        ),
        migrations.AddField(
            model_name='userjourney',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='journeys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usercompanyvisited',
            name='model_visited',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='empresas.company'),
        ),
        migrations.AddField(
            model_name='usercompanyvisited',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usercompanyvisited',
            name='visit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seo.userjourney'),
        ),
        migrations.AddField(
            model_name='metaparametershistorial',
            name='parameter_settings',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='seo.metaparameters'),
        ),
        migrations.AddField(
            model_name='metaparameters',
            name='meta_author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
