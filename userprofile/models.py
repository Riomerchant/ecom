from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from datetime import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not password:
            raise ValueError('Users must have a password')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(username, email, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    class Status(models.TextChoices):
        ADMIN = "admin", "Admin"
        SELLER = "seller", "Seller"
        BUYER = "buyer", "Buyer"
    
    class Genc(models.TextChoices):
        MALE = "Male","male"
        FEMALE = "Female","female"

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone = PhoneNumberField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(blank=True,null=True,choices=Genc.choices)
    img = models.ImageField(upload_to="profile", blank=True,null=True,default="")
    role = models.CharField(max_length=20, choices=Status.choices, default=Status.BUYER)
    
    # Required fields
    is_vendor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        return self.first_name
    
class AddressD(models.Model):
    user = models.ForeignKey(UserProfile,related_name="address",on_delete=models.CASCADE)
    Title = models.CharField(max_length=20)
    flatno=models.CharField(max_length=20)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=30)
    pincode = models.IntegerField(max_length=6)


    def get_address(self):
        return f"{self.flatno}, {self.street}, {self.city}, {self.state}, {self.country}, {self.pincode}"



class Orders(models.Model):
    buyer = models.ForeignKey(UserProfile,related_name='orders',on_delete=models.CASCADE)
    seller = models.ForeignKey(UserProfile,related_name='orderb',on_delete=models.CASCADE)
    address = models.ForeignKey(AddressD,related_name="address",on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)







