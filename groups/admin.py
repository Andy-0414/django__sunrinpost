from django.contrib import admin
from groups.models import Group, Post, Comment

admin.site.register(Group)
admin.site.register(Post)
admin.site.register(Comment)
