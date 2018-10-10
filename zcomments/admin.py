# -*- coding: utf-8 -*-
from django.contrib import admin
from zcomments.models import comments


class CommentAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'article__title', 'text')
    list_filter = ('create_time',)
    list_display = ('user', 'article', 'text', 'create_time')
    fields = ('user', 'article', 'parent', 'text')

admin.site.register(comments, CommentAdmin)
