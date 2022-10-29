# Generated by Django 3.2.15 on 2022-10-29 10:51

import apps.general.bases
import apps.general.mixins
import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content', ckeditor.fields.RichTextField()),
                ('is_accepted', models.BooleanField(default=False)),
                ('total_votes', models.IntegerField(default=0)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Answer',
                'db_table': 'answers',
                'ordering': ['-id'],
            },
            bases=(models.Model, apps.general.mixins.CommonMixin),
        ),
        migrations.CreateModel(
            name='AnswerComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('content', models.TextField()),
            ],
            options={
                'verbose_name': "Answer's comment",
                'db_table': 'answer_comments',
            },
            bases=(models.Model, apps.general.mixins.BaseToAllMixin),
        ),
        migrations.CreateModel(
            name='QuesitonComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('content', models.TextField()),
            ],
            options={
                'verbose_name': "Question's comment",
                'db_table': 'question_comments',
            },
            bases=(models.Model, apps.general.mixins.BaseToAllMixin),
        ),
        migrations.CreateModel(
            name='Question',
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
                ('content', ckeditor.fields.RichTextField()),
                ('is_answered', models.BooleanField(default=False)),
                ('hide_question', models.BooleanField(default=False)),
                ('has_accepted_answer', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Question',
                'db_table': 'questions',
                'ordering': ['-created_at'],
            },
            bases=(models.Model, apps.general.mixins.CommonMixin),
        ),
    ]
