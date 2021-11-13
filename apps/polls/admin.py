from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

    fieldsets = (
        (
            'Question information',
            dict(
                fields=['question_text'],
                classes=['collapse']
            )
        ),

        (
            'Date information',
            dict(
                fields=['pub_date'],
                classes=['collapse']
            )
        ),
    )

    inlines = (ChoiceInline,)


admin.site.register(Question, QuestionAdmin)
