from django.contrib import admin
from django.contrib.auth.models import Group

from comments.models import Comment
from posts.models import Post

admin.site.unregister(Group)


class CommentAdmin(admin.TabularInline):
    model = Comment
    extra = 1
    ordering = ('created', )
    readonly_fields = ('created', )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'text', 'image', 'created', 'author')
    readonly_fields = ('created', )
    list_display = ('title', 'created', 'author')
    list_filter = ('created', )
    search_fields = ('title', 'description', 'text', 'author')
    ordering = ('title', 'created')
    inlines = (CommentAdmin, )
