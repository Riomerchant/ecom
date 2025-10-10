from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User,AbstractUser,AbstractBaseUser
from userprofile.models import *

# Create your models here.  
class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

class Seller(models.Model):
        user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name='user',on_delete=models.CASCADE)
        shop_name =  models.CharField(max_length=100,blank=True,null=True)

        def __str__(self):
            return self.user.username

class Products(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products',null=True,blank=True)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    img = models.ImageField(upload_to="products" ,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True )

    class Meta:
        ordering = ("-created_at",)



    def __str__(self):
        return self.title
    

class CartItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} X {self.product.title}'
    
class WishlistItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}list'
    

