from django.contrib import admin

from .models import Comment, Essay

admin.site.register(Essay)
admin.site.register(Comment)
