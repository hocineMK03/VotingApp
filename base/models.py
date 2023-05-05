from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class login_user(models.Model):
    username=models.TextField(max_length=30)
    password=models.TextField(max_length=30)

class Polls_details(models.Model):
    Question=models.TextField(max_length=20,null=False)
    Desc=models.TextField(max_length=20,null=True)
    Date_created=models.DateTimeField(auto_now_add=True)
    Date_end=models.DateTimeField()
    Is_active=models.BooleanField(default=True)

    Created_by=models.ForeignKey(User,on_delete=models.CASCADE)

class Choice_poll(models.Model):
    choices=models.CharField(max_length=10)
    poll_belongsto=models.ForeignKey(Polls_details,on_delete=models.DO_NOTHING)
    count = models.IntegerField(default=0)
    
class User_choices(models.Model):
    the_poll=models.ForeignKey(Polls_details,on_delete=models.CASCADE)
    the_choice=models.ForeignKey(Choice_poll,on_delete=models.CASCADE)
    the_voter=models.ForeignKey(User,on_delete=models.CASCADE)
    is_voted=models.BooleanField(default=False)