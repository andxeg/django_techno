from django.contrib import admin

from blog.models import Post, Category
from comment.models import Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 2


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'created_date',)
    list_filter = ['created_date']
    search_fields = ['title']
    inlines = [CommentInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
