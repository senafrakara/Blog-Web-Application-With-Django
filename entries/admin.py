from django.contrib import admin
from .models import Entry, Comment, Profile

# Register your models here.

#in this page we defined models which are presented to admin panel. If we want to change the view of the data to the admin,
#we set this in below codes
admin.site.register(Profile)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('entry_title', 'entry_author', 'entry_date')
    list_filter = ('entry_title', 'entry_author', 'entry_date')
    search_fields = ('entry_title', 'entry_author')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('commenter', 'comment_content', 'entry', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('commenter', 'comment_content')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user','profile_pic',)
#     list_filter = ('user',)
#     search_fields = ('user',)
#
