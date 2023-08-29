from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Items(models.Model):
    uid = models.CharField(max_length=255, default='No data')
    name = models.CharField(max_length=255, default='No data')

    def __str__(self):
        return self.name


class Referrar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    refer_url = models.CharField(max_length=255, blank=True)
    referred_user = models.ManyToManyField(User, related_name='referred_users', blank=True)

    def __str__(self):
        return self.user.username

class Payment_detail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    card_number = models.CharField(max_length=255, default="000000000000000")
    card_name = models.CharField(max_length=255, default="John Doe", )
    cvv = models.CharField(max_length=3, default="000")
    exp_date = models.CharField(max_length=255, default="00-00")

