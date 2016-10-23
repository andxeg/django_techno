from django.contrib import admin
from polls.models import Poll, Choice, Answer
# from comment.models import Comment


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

#
# class CommentInline(admin.TabularInline):
#     model = Comment
#     extra = 2


class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Author', {'fields': ['author']}),
        (None, {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),

    ]

    list_display = ('author', 'question', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question']
    inlines = [ChoiceInline] #, CommentInline]


class AnswerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Author', {'fields': ['author']}),
        ('Choice', {'fields': ['choice']}),
    ]
    list_display = ('author', 'choice',)
    search_fields = ['author']

admin.site.register(Poll, PollAdmin)
admin.site.register(Answer, AnswerAdmin)

