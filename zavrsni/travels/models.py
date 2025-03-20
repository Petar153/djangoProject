from django.db import models
from django.contrib.auth.models import User
from django.forms import DateTimeField

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    organization = models.BooleanField()

    def __str__(self):
        return f"{self.id} - {self.name}"

class Travels(models.Model):

    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date = models.DateField(auto_now=False, auto_now_add=False) 
    photo = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default="available")


    def __str__(self):
        return f"{self.user.account.name} - {self.title}"

class Messages(models.Model):

    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    reciever_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciever')
    text= models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.sender_id.account.name} -> {self.reciever_id.account.name} - {self.text[:20]}"

    

class Trips(models.Model):

    travel=models.ForeignKey(Travels, on_delete=models.CASCADE)
    traveler = models.ForeignKey(User, on_delete=models.CASCADE)    
    rating=models.IntegerField(default=0)
    def __str__(self):
        return f"{self.travel.title} - {self.traveler.account.name}"