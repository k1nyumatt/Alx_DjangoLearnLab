from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'tag_list')
    list_filter = ('published_date', 'author', 'tags')
    search_fields = ('title', 'content')
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')
    
    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
    
    tag_list.short_description = 'Tags'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'content_preview')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('content', 'author__username', 'post__title')
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    
    content_preview.short_description = 'Content Preview'