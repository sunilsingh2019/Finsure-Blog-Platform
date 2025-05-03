from django.contrib import admin
from .models import Post, Comment, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'likes', 'dislikes')
    search_fields = ('title', 'content', 'author')
    list_filter = ('created_at', 'updated_at', 'categories')
    filter_horizontal = ('categories',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'updated_at')
    search_fields = ('content', 'author')
    list_filter = ('created_at', 'updated_at')
