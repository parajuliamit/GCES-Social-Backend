from typing import Set
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_DEFAULT, SET_NULL

# Create your models here.

class Batch(models.Model):
    name = models.CharField(max_length=10,primary_key=True)
        
    def __str__(self):
        return self.name

class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT,null=False,default=1)
    title = models.CharField(max_length = 200)
    content = models.TextField()
    image = models.ImageField(null = True,blank = True)
    createdAt = models.DateTimeField(auto_now_add=True)
    category =  models.CharField(max_length = 200,choices=[('general','general'),('exam','exam'),('events','events')])
    batch = models.ManyToManyField(Batch,blank=True)
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
    likes = models.ManyToManyField(User,related_name='blog_posts',blank=True)
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
        return str(self.comment)

class Suggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)


class Routine(models.Model):
    day =  models.CharField(max_length = 20,default='Sunday',choices=[('Sunday','Sunday'),('Monday','Monday'),('Tuesday','Tuesday'),('Wednesday','Wednesday'),('Thursday','Thursday'),('Friday','Friday')])
    time =  models.CharField(max_length = 20)
   
    def __str__(self):
        return self.day +' '+ self.time

class Subject(models.Model):
    name = models.CharField(max_length = 100)
    teacher = models.CharField(max_length = 100)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    routine = models.ManyToManyField(Routine,blank=True)
    def __str__(self):
        return self.name

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    submissionDate = models.DateField()
    user = models.ForeignKey(User, on_delete=SET_DEFAULT, default=1)
    batch = models.ForeignKey(Batch, on_delete=SET_DEFAULT, default='All')
    file = models.URLField( max_length=200,null=True, blank= True)
    def __str__(self):
        return self.title

class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField()
    createdAt = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(null=True,blank=True)
    teacher_comment = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return str(self.assignment) +' - ' + self.user.first_name


class VerifyPin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)

    def __str__(self):
        return self.user.first_name

class Event(models.Model):
    title = models.CharField(max_length = 200)
    batch = models.ManyToManyField(Batch,blank=True)
    date = models.DateField()

    def __str__(self):
        return self.title