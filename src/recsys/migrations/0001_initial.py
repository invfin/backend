# Generated by Django 3.2.15 on 2022-12-31 14:33

from django.db import migrations, models
import django.db.models.deletion
import src.general.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('escritos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCompanyRecommended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(choices=[('side', 'Side'), ('top', 'Top'), ('middle', 'Middle'), ('bottom', 'Bottom'), ('in_between', 'In between')], default='side', max_length=150)),
                ('location', models.CharField(choices=[('all-web', 'Toda la web'), ('web-inicio', 'Web Inicio'), ('screener-inicio', 'Screener Inicio'), ('screener-market', 'Screener Market'), ('screener-company', 'Screener Company'), ('cartera-inicio', 'Cartera Inicio'), ('cartera-financials', 'Cartera Financials'), ('cartera-balance', 'Cartera Balance'), ('private-profile', 'Private Profile'), ('public-profile', 'Public Profile'), ('question-inicio', 'Question Inicio'), ('question-details', 'Question Details'), ('term-inicio', 'Term Inicio'), ('term-details', 'Term Details'), ('blog-inicio', 'Blog Inicio'), ('blog-details', 'Blog Details')], default='all-web', max_length=150)),
                ('style', models.CharField(choices=[('pop_up', 'Pop up'), ('banner', 'Big Banner'), ('lista', 'List'), ('solo', 'Solo')], default='solo', max_length=150)),
                ('clicked', models.BooleanField(default=False)),
                ('recommendation_personalized', models.BooleanField(default=False)),
                ('recommendation_explained', models.JSONField(default=dict)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Company recommended for user',
                'db_table': 'recsys_companies_recommended_users',
            },
            bases=(models.Model, src.general.mixins.BaseToAllMixin),
        ),
        migrations.CreateModel(
            name='UserProductComplementaryRecommended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(choices=[('side', 'Side'), ('top', 'Top'), ('middle', 'Middle'), ('bottom', 'Bottom'), ('in_between', 'In between')], default='side', max_length=150)),
                ('location', models.CharField(choices=[('all-web', 'Toda la web'), ('web-inicio', 'Web Inicio'), ('screener-inicio', 'Screener Inicio'), ('screener-market', 'Screener Market'), ('screener-company', 'Screener Company'), ('cartera-inicio', 'Cartera Inicio'), ('cartera-financials', 'Cartera Financials'), ('cartera-balance', 'Cartera Balance'), ('private-profile', 'Private Profile'), ('public-profile', 'Public Profile'), ('question-inicio', 'Question Inicio'), ('question-details', 'Question Details'), ('term-inicio', 'Term Inicio'), ('term-details', 'Term Details'), ('blog-inicio', 'Blog Inicio'), ('blog-details', 'Blog Details')], default='all-web', max_length=150)),
                ('style', models.CharField(choices=[('pop_up', 'Pop up'), ('banner', 'Big Banner'), ('lista', 'List'), ('solo', 'Solo')], default='solo', max_length=150)),
                ('clicked', models.BooleanField(default=False)),
                ('recommendation_personalized', models.BooleanField(default=False)),
                ('recommendation_explained', models.JSONField(default=dict)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Term recommended for user',
                'db_table': 'recsys_product_complementary_recommended_users',
            },
            bases=(models.Model, src.general.mixins.BaseToAllMixin),
        ),
        migrations.CreateModel(
            name='UserPromotionRecommended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(choices=[('side', 'Side'), ('top', 'Top'), ('middle', 'Middle'), ('bottom', 'Bottom'), ('in_between', 'In between')], default='side', max_length=150)),
                ('location', models.CharField(choices=[('all-web', 'Toda la web'), ('web-inicio', 'Web Inicio'), ('screener-inicio', 'Screener Inicio'), ('screener-market', 'Screener Market'), ('screener-company', 'Screener Company'), ('cartera-inicio', 'Cartera Inicio'), ('cartera-financials', 'Cartera Financials'), ('cartera-balance', 'Cartera Balance'), ('private-profile', 'Private Profile'), ('public-profile', 'Public Profile'), ('question-inicio', 'Question Inicio'), ('question-details', 'Question Details'), ('term-inicio', 'Term Inicio'), ('term-details', 'Term Details'), ('blog-inicio', 'Blog Inicio'), ('blog-details', 'Blog Details')], default='all-web', max_length=150)),
                ('style', models.CharField(choices=[('pop_up', 'Pop up'), ('banner', 'Big Banner'), ('lista', 'List'), ('solo', 'Solo')], default='solo', max_length=150)),
                ('clicked', models.BooleanField(default=False)),
                ('recommendation_personalized', models.BooleanField(default=False)),
                ('recommendation_explained', models.JSONField(default=dict)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Term recommended for user',
                'db_table': 'recsys_promotion_recommended_users',
            },
            bases=(models.Model, src.general.mixins.BaseToAllMixin),
        ),
        migrations.CreateModel(
            name='UserPublicBlogRecommended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(choices=[('side', 'Side'), ('top', 'Top'), ('middle', 'Middle'), ('bottom', 'Bottom'), ('in_between', 'In between')], default='side', max_length=150)),
                ('location', models.CharField(choices=[('all-web', 'Toda la web'), ('web-inicio', 'Web Inicio'), ('screener-inicio', 'Screener Inicio'), ('screener-market', 'Screener Market'), ('screener-company', 'Screener Company'), ('cartera-inicio', 'Cartera Inicio'), ('cartera-financials', 'Cartera Financials'), ('cartera-balance', 'Cartera Balance'), ('private-profile', 'Private Profile'), ('public-profile', 'Public Profile'), ('question-inicio', 'Question Inicio'), ('question-details', 'Question Details'), ('term-inicio', 'Term Inicio'), ('term-details', 'Term Details'), ('blog-inicio', 'Blog Inicio'), ('blog-details', 'Blog Details')], default='all-web', max_length=150)),
                ('style', models.CharField(choices=[('pop_up', 'Pop up'), ('banner', 'Big Banner'), ('lista', 'List'), ('solo', 'Solo')], default='solo', max_length=150)),
                ('clicked', models.BooleanField(default=False)),
                ('recommendation_personalized', models.BooleanField(default=False)),
                ('recommendation_explained', models.JSONField(default=dict)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'PublicBlog recommended for user',
                'db_table': 'recsys_public_blogs_recommended_users',
            },
            bases=(models.Model, src.general.mixins.BaseToAllMixin),
        ),
        migrations.CreateModel(
            name='UserQuestionRecommended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(choices=[('side', 'Side'), ('top', 'Top'), ('middle', 'Middle'), ('bottom', 'Bottom'), ('in_between', 'In between')], default='side', max_length=150)),
                ('location', models.CharField(choices=[('all-web', 'Toda la web'), ('web-inicio', 'Web Inicio'), ('screener-inicio', 'Screener Inicio'), ('screener-market', 'Screener Market'), ('screener-company', 'Screener Company'), ('cartera-inicio', 'Cartera Inicio'), ('cartera-financials', 'Cartera Financials'), ('cartera-balance', 'Cartera Balance'), ('private-profile', 'Private Profile'), ('public-profile', 'Public Profile'), ('question-inicio', 'Question Inicio'), ('question-details', 'Question Details'), ('term-inicio', 'Term Inicio'), ('term-details', 'Term Details'), ('blog-inicio', 'Blog Inicio'), ('blog-details', 'Blog Details')], default='all-web', max_length=150)),
                ('style', models.CharField(choices=[('pop_up', 'Pop up'), ('banner', 'Big Banner'), ('lista', 'List'), ('solo', 'Solo')], default='solo', max_length=150)),
                ('clicked', models.BooleanField(default=False)),
                ('recommendation_personalized', models.BooleanField(default=False)),
                ('recommendation_explained', models.JSONField(default=dict)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Question recommended for user',
                'db_table': 'recsys_questions_recommended_users',
            },
            bases=(models.Model, src.general.mixins.BaseToAllMixin),
        ),
        migrations.CreateModel(
            name='UserTermRecommended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(choices=[('side', 'Side'), ('top', 'Top'), ('middle', 'Middle'), ('bottom', 'Bottom'), ('in_between', 'In between')], default='side', max_length=150)),
                ('location', models.CharField(choices=[('all-web', 'Toda la web'), ('web-inicio', 'Web Inicio'), ('screener-inicio', 'Screener Inicio'), ('screener-market', 'Screener Market'), ('screener-company', 'Screener Company'), ('cartera-inicio', 'Cartera Inicio'), ('cartera-financials', 'Cartera Financials'), ('cartera-balance', 'Cartera Balance'), ('private-profile', 'Private Profile'), ('public-profile', 'Public Profile'), ('question-inicio', 'Question Inicio'), ('question-details', 'Question Details'), ('term-inicio', 'Term Inicio'), ('term-details', 'Term Details'), ('blog-inicio', 'Blog Inicio'), ('blog-details', 'Blog Details')], default='all-web', max_length=150)),
                ('style', models.CharField(choices=[('pop_up', 'Pop up'), ('banner', 'Big Banner'), ('lista', 'List'), ('solo', 'Solo')], default='solo', max_length=150)),
                ('clicked', models.BooleanField(default=False)),
                ('recommendation_personalized', models.BooleanField(default=False)),
                ('recommendation_explained', models.JSONField(default=dict)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Term recommended for user',
                'db_table': 'recsys_terms_recommended_users',
            },
            bases=(models.Model, src.general.mixins.BaseToAllMixin),
        ),
        migrations.CreateModel(
            name='VisiteurCompanyRecommended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(choices=[('side', 'Side'), ('top', 'Top'), ('middle', 'Middle'), ('bottom', 'Bottom'), ('in_between', 'In between')], default='side', max_length=150)),
                ('location', models.CharField(choices=[('all-web', 'Toda la web'), ('web-inicio', 'Web Inicio'), ('screener-inicio', 'Screener Inicio'), ('screener-market', 'Screener Market'), ('screener-company', 'Screener Company'), ('cartera-inicio', 'Cartera Inicio'), ('cartera-financials', 'Cartera Financials'), ('cartera-balance', 'Cartera Balance'), ('private-profile', 'Private Profile'), ('public-profile', 'Public Profile'), ('question-inicio', 'Question Inicio'), ('question-details', 'Question Details'), ('term-inicio', 'Term Inicio'), ('term-details', 'Term Details'), ('blog-inicio', 'Blog Inicio'), ('blog-details', 'Blog Details')], default='all-web', max_length=150)),
                ('style', models.CharField(choices=[('pop_up', 'Pop up'), ('banner', 'Big Banner'), ('lista', 'List'), ('solo', 'Solo')], default='solo', max_length=150)),
                ('clicked', models.BooleanField(default=False)),
                ('recommendation_personalized', models.BooleanField(default=False)),
                ('recommendation_explained', models.JSONField(default=dict)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Company recommended for visiteur',
                'db_table': 'recsys_companies_recommended_visiteurs',
            },
            bases=(models.Model, src.general.mixins.BaseToAllMixin),
        ),
        migrations.CreateModel(
            name='VisiteurProductComplementaryRecommended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(choices=[('side', 'Side'), ('top', 'Top'), ('middle', 'Middle'), ('bottom', 'Bottom'), ('in_between', 'In between')], default='side', max_length=150)),
                ('location', models.CharField(choices=[('all-web', 'Toda la web'), ('web-inicio', 'Web Inicio'), ('screener-inicio', 'Screener Inicio'), ('screener-market', 'Screener Market'), ('screener-company', 'Screener Company'), ('cartera-inicio', 'Cartera Inicio'), ('cartera-financials', 'Cartera Financials'), ('cartera-balance', 'Cartera Balance'), ('private-profile', 'Private Profile'), ('public-profile', 'Public Profile'), ('question-inicio', 'Question Inicio'), ('question-details', 'Question Details'), ('term-inicio', 'Term Inicio'), ('term-details', 'Term Details'), ('blog-inicio', 'Blog Inicio'), ('blog-details', 'Blog Details')], default='all-web', max_length=150)),
                ('style', models.CharField(choices=[('pop_up', 'Pop up'), ('banner', 'Big Banner'), ('lista', 'List'), ('solo', 'Solo')], default='solo', max_length=150)),
                ('clicked', models.BooleanField(default=False)),
                ('recommendation_personalized', models.BooleanField(default=False)),
                ('recommendation_explained', models.JSONField(default=dict)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Term recommended for visiteur',
                'db_table': 'recsys_product_complementary_recommended_visiteurs',
            },
            bases=(models.Model, src.general.mixins.BaseToAllMixin),
        ),
        migrations.CreateModel(
            name='VisiteurPromotionRecommended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(choices=[('side', 'Side'), ('top', 'Top'), ('middle', 'Middle'), ('bottom', 'Bottom'), ('in_between', 'In between')], default='side', max_length=150)),
                ('location', models.CharField(choices=[('all-web', 'Toda la web'), ('web-inicio', 'Web Inicio'), ('screener-inicio', 'Screener Inicio'), ('screener-market', 'Screener Market'), ('screener-company', 'Screener Company'), ('cartera-inicio', 'Cartera Inicio'), ('cartera-financials', 'Cartera Financials'), ('cartera-balance', 'Cartera Balance'), ('private-profile', 'Private Profile'), ('public-profile', 'Public Profile'), ('question-inicio', 'Question Inicio'), ('question-details', 'Question Details'), ('term-inicio', 'Term Inicio'), ('term-details', 'Term Details'), ('blog-inicio', 'Blog Inicio'), ('blog-details', 'Blog Details')], default='all-web', max_length=150)),
                ('style', models.CharField(choices=[('pop_up', 'Pop up'), ('banner', 'Big Banner'), ('lista', 'List'), ('solo', 'Solo')], default='solo', max_length=150)),
                ('clicked', models.BooleanField(default=False)),
                ('recommendation_personalized', models.BooleanField(default=False)),
                ('recommendation_explained', models.JSONField(default=dict)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Term recommended for visiteur',
                'db_table': 'recsys_promotion_recommended_visiteurs',
            },
            bases=(models.Model, src.general.mixins.BaseToAllMixin),
        ),
        migrations.CreateModel(
            name='VisiteurPublicBlogRecommended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(choices=[('side', 'Side'), ('top', 'Top'), ('middle', 'Middle'), ('bottom', 'Bottom'), ('in_between', 'In between')], default='side', max_length=150)),
                ('location', models.CharField(choices=[('all-web', 'Toda la web'), ('web-inicio', 'Web Inicio'), ('screener-inicio', 'Screener Inicio'), ('screener-market', 'Screener Market'), ('screener-company', 'Screener Company'), ('cartera-inicio', 'Cartera Inicio'), ('cartera-financials', 'Cartera Financials'), ('cartera-balance', 'Cartera Balance'), ('private-profile', 'Private Profile'), ('public-profile', 'Public Profile'), ('question-inicio', 'Question Inicio'), ('question-details', 'Question Details'), ('term-inicio', 'Term Inicio'), ('term-details', 'Term Details'), ('blog-inicio', 'Blog Inicio'), ('blog-details', 'Blog Details')], default='all-web', max_length=150)),
                ('style', models.CharField(choices=[('pop_up', 'Pop up'), ('banner', 'Big Banner'), ('lista', 'List'), ('solo', 'Solo')], default='solo', max_length=150)),
                ('clicked', models.BooleanField(default=False)),
                ('recommendation_personalized', models.BooleanField(default=False)),
                ('recommendation_explained', models.JSONField(default=dict)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'PublicBlog recommended for visiteur',
                'db_table': 'recsys_public_blogs_recommended_visiteurs',
            },
            bases=(models.Model, src.general.mixins.BaseToAllMixin),
        ),
        migrations.CreateModel(
            name='VisiteurQuestionRecommended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(choices=[('side', 'Side'), ('top', 'Top'), ('middle', 'Middle'), ('bottom', 'Bottom'), ('in_between', 'In between')], default='side', max_length=150)),
                ('location', models.CharField(choices=[('all-web', 'Toda la web'), ('web-inicio', 'Web Inicio'), ('screener-inicio', 'Screener Inicio'), ('screener-market', 'Screener Market'), ('screener-company', 'Screener Company'), ('cartera-inicio', 'Cartera Inicio'), ('cartera-financials', 'Cartera Financials'), ('cartera-balance', 'Cartera Balance'), ('private-profile', 'Private Profile'), ('public-profile', 'Public Profile'), ('question-inicio', 'Question Inicio'), ('question-details', 'Question Details'), ('term-inicio', 'Term Inicio'), ('term-details', 'Term Details'), ('blog-inicio', 'Blog Inicio'), ('blog-details', 'Blog Details')], default='all-web', max_length=150)),
                ('style', models.CharField(choices=[('pop_up', 'Pop up'), ('banner', 'Big Banner'), ('lista', 'List'), ('solo', 'Solo')], default='solo', max_length=150)),
                ('clicked', models.BooleanField(default=False)),
                ('recommendation_personalized', models.BooleanField(default=False)),
                ('recommendation_explained', models.JSONField(default=dict)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Question recommended for visiteur',
                'db_table': 'recsys_questions_recommended_visiteurs',
            },
            bases=(models.Model, src.general.mixins.BaseToAllMixin),
        ),
        migrations.CreateModel(
            name='VisiteurTermRecommended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(choices=[('side', 'Side'), ('top', 'Top'), ('middle', 'Middle'), ('bottom', 'Bottom'), ('in_between', 'In between')], default='side', max_length=150)),
                ('location', models.CharField(choices=[('all-web', 'Toda la web'), ('web-inicio', 'Web Inicio'), ('screener-inicio', 'Screener Inicio'), ('screener-market', 'Screener Market'), ('screener-company', 'Screener Company'), ('cartera-inicio', 'Cartera Inicio'), ('cartera-financials', 'Cartera Financials'), ('cartera-balance', 'Cartera Balance'), ('private-profile', 'Private Profile'), ('public-profile', 'Public Profile'), ('question-inicio', 'Question Inicio'), ('question-details', 'Question Details'), ('term-inicio', 'Term Inicio'), ('term-details', 'Term Details'), ('blog-inicio', 'Blog Inicio'), ('blog-details', 'Blog Details')], default='all-web', max_length=150)),
                ('style', models.CharField(choices=[('pop_up', 'Pop up'), ('banner', 'Big Banner'), ('lista', 'List'), ('solo', 'Solo')], default='solo', max_length=150)),
                ('clicked', models.BooleanField(default=False)),
                ('recommendation_personalized', models.BooleanField(default=False)),
                ('recommendation_explained', models.JSONField(default=dict)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('model_recommended', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='escritos.term')),
            ],
            options={
                'verbose_name': 'Term recommended for visiteur',
                'db_table': 'recsys_terms_recommended_visiteurs',
            },
            bases=(models.Model, src.general.mixins.BaseToAllMixin),
        ),
    ]
