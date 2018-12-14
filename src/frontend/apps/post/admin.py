from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post


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
    ordering = ['-created_at']
    search_fields = ['subject']
    read_only = True

    def getSubject(self, instance):
        return mark_safe(f'<a href="{instance.hacker_news_url}" alt="{instance.subject}"> {instance.subject} </a>')

    getSubject.short_description = 'Subject'

admin.site.register(Post, PostAdmin)
