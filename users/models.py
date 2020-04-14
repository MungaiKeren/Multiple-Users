from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
# adding the full name as a reqired field in this case
class UserManager(BaseUserManager):
    def create_user(self, email,full_name, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have email")
        if not password:
            raise ValueError("Users must have password")
        if not full_name:
            raise ValueError("Users must have full names")

        user_obj = self.model(
            email = self.normalize_email(email),
            full_name= full_name,
        )
        user_obj.set_password(password) # change password
        user_obj.staff = is_staff
        user_obj.active = is_active
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj
    
    def create_staffUser(self, email,full_name, password=None):
        user = self.create_user(
            email,
            full_name,
            password=password,
            is_staff=True,
        )
        return user
    
    def create_superuser(self, email,full_name, password=None):
        user = self.create_user(
            email,
            full_name,
            password=password,
            is_staff=True,
            is_admin= True,
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    active = models.BooleanField(default=True) #can login
    staff = models.BooleanField(default=False) # not super user
    admin = models.BooleanField(default=False) #superuser
    timestamp = models.DateTimeField(auto_now_add=True)
    # confirmed_email = models.BooleanField(default=False)
    # confirmed_date = models.DateTimeField()

    USERNAME_FIELD = "email" #username
    # username and password field are required by default
    REQUIRED_FIELDS = ['full_name'] #["full name"] Would appear in python manage.py createsuperuser

    objects = UserManager()
    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email
    
    def get_short_name(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return self.is_admin
    
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active
    
# class Profile(models.Model):
    # user = models.OneToOneField(User)
    # extend extra data