from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    title = models.CharField(max_length = 200)
    content = models.TextField()
    image = models.ImageField(null = True,blank = True)
    createdAt = models.DateTimeField(auto_now_add=True)
    category =  models.CharField(max_length = 200,choices=[('general','general'),('exam','exam'),('events','events')])
    # name = models.TextField(blank=True, null = True)

    def __str__(self):
        return self.title
    
    # def save(self,*args, **kwargs):
    #     self.name = self.user.username
    #     super(Announcement,self).save(*args, **kwargs)


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,related_name='blog_posts')
    # likes = models.IntegerField(null=True,blank=True,default=0)
    is_approved = models.BooleanField(default=False)
    # liked = models.BooleanField(default=False)

    @property
    def total_likes(self):
        return self.likes.count

    def __str__(self):
        return self.title

    @property
    def comment_count(self):
        return self.comment_set.count()

class Comment(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)
    