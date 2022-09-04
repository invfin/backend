from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin

from .models import Answer, AnswerComment, QuesitonComment, Question



class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
    verbose_name = "Question"
    verbose_name_plural = "Questions"
    fields = [
        "title",
        "content",
        "is_answered",
        "hide_question",
        "has_accepted_answer",
        "upvotes",
        "downvotes",
        "total_votes",
        "total_views",
        "times_shared",
        "category",
        "tags",
    ]
    jazzmin_tab_id = "questions"


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0
    verbose_name = "Answer"
    verbose_name_plural = "Answers"
    fields = [
        "author",
        "content",
        "is_accepted",
        "total_votes",
        "upvotes",
        "downvotes",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    jazzmin_tab_id = "answers"


@admin.register(Question)
class QuestionAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'author',
        "hide_question"
        ]

    list_editable = [
        "hide_question"
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
