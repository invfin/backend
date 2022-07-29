from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin

from .models import Answer, AnswerComment, QuesitonComment, Question


@admin.register(Question)
class QuestionAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'author'
        ]
    
    list_editable = [
        'author'
    ]

    search_fields = ['author_username']


@admin.register(QuesitonComment)
class QuesitonCommentAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = [
        'id',
        'author',
        'created_at']
    
    search_fields = ['author_username']


@admin.register(Answer)
class AnswerAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = [
        'id',
        'author'
        ]
    
    list_editable = [
        'author'
    ]
    search_fields = ['author_username']


@admin.register(AnswerComment)
class AnswerCommentAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = [
        'id',
        'author',
        'created_at']
    
    search_fields = ['author_username']
