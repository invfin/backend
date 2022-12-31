# Generated by Django 3.2.15 on 2022-12-31 14:33

import ckeditor.fields
from django.db import migrations, models
import src.emailing.extensions
import src.escritos.abstracts
import src.general.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FollowingHistorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_following', models.BooleanField(default=False)),
                ('stop_following', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Users following historial',
                'db_table': 'writer_followers_historial',
            },
        ),
        migrations.CreateModel(
            name='NewsletterFollowers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Base de seguidores del blog',
                'db_table': 'writer_followers_newsletters',
            },
        ),
        migrations.CreateModel(
            name='PublicBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, max_length=800, null=True)),
                ('slug', models.SlugField(blank=True, max_length=800, null=True)),
                ('checkings', models.JSONField(default=src.escritos.abstracts.default_dict)),
                ('total_votes', models.IntegerField(default=0)),
                ('total_views', models.PositiveIntegerField(default=0)),
                ('times_shared', models.PositiveIntegerField(default=0)),
                ('resume', models.TextField(default='')),
                ('published_at', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField(blank=True, choices=[(1, 'Publicado'), (2, 'Borrador'), (3, 'Programado'), (4, 'Necesita revisión')], default=2)),
                ('thumbnail', models.ImageField(blank=True, height_field='image_height', null=True, upload_to='', verbose_name='image', width_field='image_width')),
                ('non_thumbnail_url', models.CharField(blank=True, max_length=500, null=True)),
                ('in_text_image', models.BooleanField(default=False)),
                ('send_as_newsletter', models.BooleanField(default=False)),
                ('content', ckeditor.fields.RichTextField()),
                ('published_correctly', models.BooleanField(default=False)),
                ('date_to_publish', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Public blog post',
                'db_table': 'blog_post',
                'ordering': ['total_views'],
            },
            bases=(models.Model, src.general.mixins.BaseToAllMixin, src.general.mixins.CommentsMixin, src.general.mixins.VotesMixin, src.general.mixins.CheckingsMixin),
        ),
        migrations.CreateModel(
            name='PublicBlogAsNewsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=500)),
                ('content', ckeditor.fields.RichTextField()),
                ('sent', models.BooleanField(default=False)),
                ('date_to_send', models.DateTimeField(blank=True, null=True)),
                ('call_to_action', models.CharField(blank=True, max_length=500, null=True)),
                ('call_to_action_url', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, src.general.mixins.BaseToAllMixin, src.emailing.extensions.EmailExtension),
        ),
        migrations.CreateModel(
            name='PublicBlogComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
            ],
            options={
                'verbose_name': "Blog's comment",
                'db_table': 'blog_comments',
            },
            bases=(models.Model, src.general.mixins.BaseToAllMixin),
        ),
        migrations.CreateModel(
            name='WriterProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('host_name', models.CharField(blank=True, max_length=500, null=True, unique=True)),
                ('long_description', ckeditor.fields.RichTextField(blank=True, default='')),
                ('facebook', models.CharField(blank=True, max_length=500, null=True)),
                ('twitter', models.CharField(blank=True, max_length=500, null=True)),
                ('instagram', models.CharField(blank=True, max_length=500, null=True)),
                ('youtube', models.CharField(blank=True, max_length=500, null=True)),
                ('linkedin', models.CharField(blank=True, max_length=500, null=True)),
                ('tiktok', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'verbose_name': 'User writer profile',
                'db_table': 'writer_profile',
            },
        ),
    ]
