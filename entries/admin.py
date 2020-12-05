from django.contrib import admin
from .models import Entry, Comment

# Register your models here.

admin.site.register(Entry)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('commenter', 'comment_content', 'entry', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('commenter', 'comment_content')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


#admin.site.register(Comment)