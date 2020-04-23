from django.contrib import admin

# Register your models here.
from .models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','body','publish','created','updated','status']
    list_filter = ('status','author',)
    prepopulated_fields = {'slug':('title',)}

# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['post','name','email','body','created','updated','active']
#     list_filter = ('active','created','updated')
#     search_fields = ('name','email','body')

admin.site.register(Post,PostAdmin)
# admin.site.register(Comment,CommentAdmin)