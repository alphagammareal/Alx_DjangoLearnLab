from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'published_date')
    list_filter = ('author', 'created_at', 'published_date', 'tags')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'active')
    list_filter = ('active', 'created_at', 'author')
    search_fields = ('content', 'author__username')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
