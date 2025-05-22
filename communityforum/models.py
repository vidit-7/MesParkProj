from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class ForumPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic) #,null=True , blank=True) #topics__name==
    title = models.CharField(max_length=150)
    content = models.TextField()
    image = models.ImageField(upload_to='forumpost_pics',null=True,blank=True)
    # video = models.FileField(upload_to='forumpost_videos',null=True,blank=True)
    video_url = models.URLField(null=True, blank=True)
    posted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.user} - {self.title}"
    
    def isEdited(self):
        if self.posted.replace(microsecond=0) != self.updated.replace(microsecond=0):
            return True
        return False
    
    def contentShort(self):
        if len(self.content) > 250:
            return self.content[:250]+"..."
        return self.content

class ForumComment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    forumpost = models.ForeignKey(ForumPost, on_delete=models.CASCADE)
    comment = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.user} - {self.shortComment()}"

    def shortComment(self):
        if len(self.comment)>25:
            return self.comment[0:25] + '...'
        else:
            return self.comment