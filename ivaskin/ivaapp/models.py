from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class App(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField('ivaapp/images/', blank=True, null=True)

    def __str__(self):
        return self.title


class Forclient(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField('ivaapp/images/')
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name



class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    serv = models.ForeignKey('TagForClient', blank=True, null=True, on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"


class TagForClient(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name