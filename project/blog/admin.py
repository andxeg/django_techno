from django.contrib import admin

from blog.models import Post, Category


# class PostAdmin(admin.ModelAdmin):
#     list_display = ('question', 'pub_date', )
#     list_filter = ['pub_date']
#     search_fields = ['question']


admin.site.register(Post) #, PostAdmin)
admin.site.register(Category)
