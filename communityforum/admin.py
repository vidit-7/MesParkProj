from django.contrib import admin
from communityforum.models import Topic, ForumPost, ForumComment, ForumCommentReply

# Register your models here.

admin.site.register(Topic)
admin.site.register(ForumPost)
admin.site.register(ForumComment)
admin.site.register(ForumCommentReply)