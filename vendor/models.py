from django.db import models
from django.conf import settings
from store.models import Products
# Create your models here.
class Seller(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user',on_delete=models.CASCADE)
    shop_name =  models.CharField(max_length=100,unique=True)
    product = models.ForeignKey(Products,related_name='product',on_delete=models.CASCADE)

    def __str__(self):
        return self.shop_name
