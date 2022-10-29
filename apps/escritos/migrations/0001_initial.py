# Generated by Django 3.2.15 on 2022-10-29 10:51

import apps.general.bases
import apps.general.mixins
import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FavoritesTermsHistorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('added', models.BooleanField(default=False)),
                ('removed', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Término favorito',
                'verbose_name_plural': 'Términos favoritos',
                'db_table': 'favorites_terms_historial',
            },
        ),
        migrations.CreateModel(
            name='FavoritesTermsList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Lista de términos favoritos',
                'verbose_name_plural': 'Lista de términos favoritos',
                'db_table': 'favorites_terms_list',
            },
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.CharField(blank=True, max_length=500, null=True)),
                ('total_votes', models.IntegerField(default=0)),
                ('total_views', models.PositiveIntegerField(default=0)),
                ('times_shared', models.PositiveIntegerField(default=0)),
                ('checkings', models.JSONField(default=apps.general.bases.default_dict)),
                ('resume', models.TextField(default='')),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField(blank=True, choices=[(1, 'Publicado'), (2, 'Borrador'), (3, 'Programado'), (4, 'Necesita revisión')], default=2)),
                ('thumbnail', models.ImageField(blank=True, height_field='image_height', null=True, upload_to='', verbose_name='image', width_field='image_width')),
                ('non_thumbnail_url', models.CharField(blank=True, max_length=500, null=True)),
                ('in_text_image', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Término del glosario',
                'db_table': 'term',
                'ordering': ['id'],
            },
            bases=(models.Model, apps.general.mixins.CommonMixin, apps.general.mixins.BaseEscritosMixins),
        ),
        migrations.CreateModel(
            name='TermContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=3000)),
                ('order', models.PositiveIntegerField(default=0)),
                ('content', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'Partes del término',
                'db_table': 'term_content',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='TermCorrection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=3000, null=True)),
                ('date_suggested', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_approved', models.BooleanField(default=False)),
                ('date_approved', models.DateTimeField(blank=True, null=True)),
                ('content', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'Corrections terms',
                'db_table': 'term_content_correction',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TermsComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('content', models.TextField()),
            ],
            options={
                'verbose_name': "Term's comment",
                'db_table': 'term_comments',
            },
            bases=(models.Model, apps.general.mixins.BaseToAllMixin),
        ),
        migrations.CreateModel(
            name='TermsRelatedToResume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term_to_delete', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='term_to_delete', to='escritos.term')),
                ('term_to_keep', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='term_to_keep', to='escritos.term')),
            ],
            options={
                'verbose_name': 'Terms to resume',
                'db_table': 'terms_to_resume',
            },
        ),
    ]
