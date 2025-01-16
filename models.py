from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PostModel(models.Model):
    username = models.CharField(max_length=30)
    grade = models.SmallIntegerField()
    text = models.CharField(max_length=2000, blank=True)
    img = models.ImageField(null=True, blank=True, upload_to="post_images/")
    vid = models.FileField(null=True, blank=True, upload_to="post_videos/")
    pfp = models.ImageField()
    time = models.TimeField(blank=True, null=True)
    likes = models.ManyToManyField(User, blank=True, related_name="post_like")
    dislikes = models.ManyToManyField(User, blank=True, related_name="post_dislike")

    def like_count(self):
        return self.likes.count()
    
    def dislike_count(self):
        return self.dislikes.count()

    def __str__(self):
        return self.username
    
class ProfileModel(models.Model):
    username = models.CharField(max_length=300)
    grade = models.SmallIntegerField()
    pfp = models.ImageField(null=True, blank=True, upload_to="profile_picture/")

    def __str__(self):
        return self.username