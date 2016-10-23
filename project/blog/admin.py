from django.contrib import admin

from blog.models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'created_date',)
    list_filter = ['created_date']
    search_fields = ['title']


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
