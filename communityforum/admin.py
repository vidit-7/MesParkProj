from django.contrib import admin
from communityforum.models import Topic, ForumPost, ForumComment

# Register your models here.

admin.site.register(Topic)
admin.site.register(ForumPost)
admin.site.register(ForumComment)