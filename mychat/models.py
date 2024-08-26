from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.IntegerField()
    pic=models.ImageField(upload_to="img",blank=True,null=True)
    friends=models.ManyToManyField('Friend',related_name="my_friends",null=True,blank=True)


    def __str__(self):
        return self.name

class Friend(models.Model):
    profile=models.OneToOneField(Profile,on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.name
        
class ChatMessage(models.Model):
    body = models.TextField()
    msg_sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="msg_sender")
    msg_recevier = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="msg_recevier")
    seen = models.BooleanField(default=False)
    msg_sender_time = models.DateTimeField(default=timezone.now)  # Time when the message was sent by the sender

    def __str__(self):
        return self.body
