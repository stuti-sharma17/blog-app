from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Tweet(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    text=models.TextField(max_length=240)
    photo=models.ImageField(upload_to='photos/',blank=True,null=True)
    created_At=models.DateTimeField(auto_now_add=True)
    updated_At=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.title if self.title else self.text[:10]}'
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.user.username
    
    def get_profile_picture_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return '/static/images/default.jpg'
