<<<<<<< HEAD
# Generated by Django 3.2.15 on 2022-09-29 15:29
=======
# Generated by Django 3.2.15 on 2022-09-29 15:33
>>>>>>> 3f643cc69432aef628d5b1cec721aaa8492f8a8d

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('escritos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogSharedHistorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_shared', models.DateTimeField(auto_now_add=True)),
                ('post_type', models.PositiveIntegerField(choices=[(1, 'Video'), (2, 'Image'), (3, 'Text'), (4, 'Repost'), (5, 'Text and video'), (6, 'Text and image'), (7, 'Shorts'), (8, 'Thread')])),
                ('platform_shared', models.CharField(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('reddit', 'Reddit'), ('whatsapp', 'Whatsapp'), ('linkedin', 'Linkedin'), ('pinterest', 'Pinterest'), ('tumblr', 'Tumblr'), ('youtube', 'Youtube'), ('instagram', 'Instagram')], max_length=500)),
                ('social_id', models.CharField(max_length=500)),
                ('title', ckeditor.fields.RichTextField(blank=True)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('extra_description', ckeditor.fields.RichTextField(blank=True)),
                ('inside_information', ckeditor.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'Blog shared',
                'db_table': 'shared_blogs',
            },
        ),
        migrations.CreateModel(
            name='CompanySharedHistorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_shared', models.DateTimeField(auto_now_add=True)),
                ('post_type', models.PositiveIntegerField(choices=[(1, 'Video'), (2, 'Image'), (3, 'Text'), (4, 'Repost'), (5, 'Text and video'), (6, 'Text and image'), (7, 'Shorts'), (8, 'Thread')])),
                ('platform_shared', models.CharField(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('reddit', 'Reddit'), ('whatsapp', 'Whatsapp'), ('linkedin', 'Linkedin'), ('pinterest', 'Pinterest'), ('tumblr', 'Tumblr'), ('youtube', 'Youtube'), ('instagram', 'Instagram')], max_length=500)),
                ('social_id', models.CharField(max_length=500)),
                ('title', ckeditor.fields.RichTextField(blank=True)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('extra_description', ckeditor.fields.RichTextField(blank=True)),
                ('inside_information', ckeditor.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'Company shared',
                'db_table': 'shared_companies',
            },
        ),
        migrations.CreateModel(
            name='DefaultContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('for_content', models.PositiveIntegerField(blank=True, choices=[(0, 'All'), (1, 'Question'), (2, 'News'), (3, 'Term'), (4, 'Blog'), (5, 'Company'), (6, 'Web')], default=0)),
                ('purpose', models.CharField(blank=True, choices=[('promotion', 'Promotion'), ('suggestion', 'Suggestion'), ('announcement', 'Announcement'), ('welcome', 'Welcome'), ('engagement', 'Engagement'), ('engagement-user-no-active', 'Engagement user no active'), ('engagement-user-little-active', 'Engagement user little active'), ('engagement-user-first-call', 'Engagement user first call')], max_length=500, null=True)),
                ('content', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'Default content',
                'db_table': 'socialmedia_content',
            },
        ),
        migrations.CreateModel(
            name='DefaultTilte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='')),
                ('for_content', models.PositiveIntegerField(blank=True, choices=[(0, 'All'), (1, 'Question'), (2, 'News'), (3, 'Term'), (4, 'Blog'), (5, 'Company'), (6, 'Web')], default=0)),
                ('purpose', models.CharField(blank=True, choices=[('promotion', 'Promotion'), ('suggestion', 'Suggestion'), ('announcement', 'Announcement'), ('welcome', 'Welcome'), ('engagement', 'Engagement'), ('engagement-user-no-active', 'Engagement user no active'), ('engagement-user-little-active', 'Engagement user little active'), ('engagement-user-first-call', 'Engagement user first call')], max_length=500, null=True)),
            ],
            options={
                'verbose_name': 'Default titles',
                'db_table': 'socialmedia_titles',
            },
        ),
        migrations.CreateModel(
            name='Emoji',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emoji', models.CharField(max_length=500)),
            ],
            options={
                'verbose_name': 'Default emojis',
                'db_table': 'socialmedia_emojis',
            },
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='')),
                ('platform', models.CharField(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('reddit', 'Reddit'), ('whatsapp', 'Whatsapp'), ('linkedin', 'Linkedin'), ('pinterest', 'Pinterest'), ('tumblr', 'Tumblr'), ('youtube', 'Youtube'), ('instagram', 'Instagram')], max_length=500)),
                ('is_trending', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Default hashtags',
                'db_table': 'socialmedia_hashtags',
            },
        ),
        migrations.CreateModel(
            name='NewsSharedHistorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_shared', models.DateTimeField(auto_now_add=True)),
                ('post_type', models.PositiveIntegerField(choices=[(1, 'Video'), (2, 'Image'), (3, 'Text'), (4, 'Repost'), (5, 'Text and video'), (6, 'Text and image'), (7, 'Shorts'), (8, 'Thread')])),
                ('platform_shared', models.CharField(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('reddit', 'Reddit'), ('whatsapp', 'Whatsapp'), ('linkedin', 'Linkedin'), ('pinterest', 'Pinterest'), ('tumblr', 'Tumblr'), ('youtube', 'Youtube'), ('instagram', 'Instagram')], max_length=500)),
                ('social_id', models.CharField(max_length=500)),
                ('title', ckeditor.fields.RichTextField(blank=True)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('extra_description', ckeditor.fields.RichTextField(blank=True)),
                ('inside_information', ckeditor.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'Company news shared',
                'db_table': 'shared_news',
            },
        ),
        migrations.CreateModel(
            name='ProfileSharedHistorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_shared', models.DateTimeField(auto_now_add=True)),
                ('post_type', models.PositiveIntegerField(choices=[(1, 'Video'), (2, 'Image'), (3, 'Text'), (4, 'Repost'), (5, 'Text and video'), (6, 'Text and image'), (7, 'Shorts'), (8, 'Thread')])),
                ('platform_shared', models.CharField(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('reddit', 'Reddit'), ('whatsapp', 'Whatsapp'), ('linkedin', 'Linkedin'), ('pinterest', 'Pinterest'), ('tumblr', 'Tumblr'), ('youtube', 'Youtube'), ('instagram', 'Instagram')], max_length=500)),
                ('social_id', models.CharField(max_length=500)),
                ('title', ckeditor.fields.RichTextField(blank=True)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('extra_description', ckeditor.fields.RichTextField(blank=True)),
                ('inside_information', ckeditor.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'Profile shared',
                'db_table': 'shared_profiles',
            },
        ),
        migrations.CreateModel(
            name='QuestionSharedHistorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_shared', models.DateTimeField(auto_now_add=True)),
                ('post_type', models.PositiveIntegerField(choices=[(1, 'Video'), (2, 'Image'), (3, 'Text'), (4, 'Repost'), (5, 'Text and video'), (6, 'Text and image'), (7, 'Shorts'), (8, 'Thread')])),
                ('platform_shared', models.CharField(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('reddit', 'Reddit'), ('whatsapp', 'Whatsapp'), ('linkedin', 'Linkedin'), ('pinterest', 'Pinterest'), ('tumblr', 'Tumblr'), ('youtube', 'Youtube'), ('instagram', 'Instagram')], max_length=500)),
                ('social_id', models.CharField(max_length=500)),
                ('title', ckeditor.fields.RichTextField(blank=True)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('extra_description', ckeditor.fields.RichTextField(blank=True)),
                ('inside_information', ckeditor.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'Question shared',
                'db_table': 'shared_questions',
            },
        ),
        migrations.CreateModel(
            name='TermSharedHistorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_shared', models.DateTimeField(auto_now_add=True)),
                ('post_type', models.PositiveIntegerField(choices=[(1, 'Video'), (2, 'Image'), (3, 'Text'), (4, 'Repost'), (5, 'Text and video'), (6, 'Text and image'), (7, 'Shorts'), (8, 'Thread')])),
                ('platform_shared', models.CharField(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('reddit', 'Reddit'), ('whatsapp', 'Whatsapp'), ('linkedin', 'Linkedin'), ('pinterest', 'Pinterest'), ('tumblr', 'Tumblr'), ('youtube', 'Youtube'), ('instagram', 'Instagram')], max_length=500)),
                ('social_id', models.CharField(max_length=500)),
                ('title', ckeditor.fields.RichTextField(blank=True)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('extra_description', ckeditor.fields.RichTextField(blank=True)),
                ('inside_information', ckeditor.fields.RichTextField(blank=True)),
                ('content_shared', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='terms_shared', to='escritos.term')),
            ],
            options={
                'verbose_name': 'Term shared',
                'db_table': 'shared_terms',
            },
        ),
    ]
