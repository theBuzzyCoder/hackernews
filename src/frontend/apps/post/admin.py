import os
from django.contrib import admin
from django.utils.safestring import mark_safe
from frontend.apps.post.models import Post, Extractor


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'getSubject', 'upvotes', 'post_age', 'comments', 'is_read', 'is_deleted')

    # fieldsets basically organises the edit view with panels.
    # the first item is panel name and second item in the tuple is a dict with key as field.
    fieldsets = (
        ('Primary', {  # Panel-1
            'fields': ('subject', 'hacker_news_url')
        }),
        ('Analytics', {  # Panel-2
            # Making tuple allows both fields come inline while displaying in frontend.
            'fields': (('post_age', 'comments', 'upvotes', 'is_read', 'is_deleted'), )
        }),
        ('Timestamp', {  # Panel-3
            'fields': (('created_at', 'modified_at'), )
        })
    )

    # Order by created_at desc
    ordering = ['-post_age', 'id']
    search_fields = ['subject']

    def getSubject(self, instance):
        return mark_safe(f'<a href="{instance.hacker_news_url}" alt="{instance.subject}"> {instance.subject} </a>')

    getSubject.short_description = 'Subject'


class ExtractorAdmin(admin.ModelAdmin):
    list_display = ('id', 'getFilePath', 'pagination', 'is_parsed', 'created_at')
    fieldsets = (
        ('Primary', {  # Panel-1
            'fields': ('file_path', 'pagination', 'created_at')
        }),
    )
    ordering = ['-created_at']
    search_fields = ['file_path']

    def getFilePath(self, instance):
        basename = os.path.basename(instance.file_path)
        return mark_safe(f'<a href="/post/html/{basename}" alt="{instance.file_path}"> {instance.file_path} </a>')

    getFilePath.short_description = "Html Path"

admin.site.register(Post, PostAdmin)
admin.site.register(Extractor, ExtractorAdmin)
