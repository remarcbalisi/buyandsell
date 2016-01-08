from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from time import time
from django.utils import timezone

from django.contrib.auth.models import BaseUserManager

# CUSTOM USER AUTH
###############################################################################

class UserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            is_admin=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return UserManager

class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    contact_number = models.CharField(max_length=30, null=True, blank=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def get_full_name(self):
        return self.email
    def get_short_name(self):
        return self.email

    objects = UserManager()

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class Type(models.Model):
	name = models.CharField(max_length = 10)

	def __str__(self):
		return self.name

#############################################################################
#------- importing images---
def generate_filename(instance, filename):
    ext = filename.split('.')[-1]
    return 'uploads/' + str(int(time())) + '.' + ext

class Image(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    stuff_image = models.ImageField(upload_to=generate_filename)
    item_id = models.ForeignKey('Item', null=True, blank=True)

    def __unicode__(self):
	   return "%s" %(self.title)
        
    class Meta:
        ordering = ['title']
#----------------------------

##############################################################################

class Category(models.Model):
	name = models.CharField(max_length = 50)

	def __str__(self):
		return self.name

class Comment(models.Model):
    comment = models.TextField(null=True)
    item_id = models.ForeignKey('Item', blank=True, null=True)
    user_id = models.ForeignKey('User', blank=True, null=True)
    post_comment = models.DateTimeField(blank = True, null = True)

    def publish(self):
        self.post_comment = timezone.now()
        self.save()


    def __str__(self):
        return self.user_id


class Item(models.Model):
    name = models.CharField(max_length = 70)
    description = models.TextField()
    price = models.IntegerField()
    category_id = models.ForeignKey('Category')
    type_id = models.ForeignKey('Type', null=True, blank=True)
    user_id = models.ForeignKey('User', null=True, blank=True)
    post_date = models.DateTimeField(blank = True, null = True)
    ranking_id = models.ForeignKey('Ranking', blank=True, null=True)

    def __str__(self):
        return self.name

    # %Y for year
    def date_posted(self):
        return self.post_date.strftime("%d")

    def month_posted(self):
        return self.post_date.strftime("%b")

class Ranking(models.Model):
    item_rank = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return "%s" %(self.item_rank)

    def init(self):
        self.item_rank = timezone.now()
        self.save()

    def __unicode__(self):
       return self.item_rank

class Message(models.Model):
    text_message = models.TextField()
    message_created = models.DateTimeField(auto_now_add=True)
    #user_id is the sender of the message
    user_id = models.ForeignKey('User', blank=True, null=True)
    recipient_id = models.ForeignKey('Recipient', blank=True, null=True)
    thread_id = models.ForeignKey('Thread', blank=True, null=True)
    has_read = models.BooleanField(default=False)
    read_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "%s %s" %(self.user_id, self.message_created)

    def seen(self):
        self.has_read = True
        self.read_time = timezone.now()
        self.save()

class Recipient(models.Model):
    user_id = models.ForeignKey('User', blank=True, null=True)

    def __str__(self):
        return self.user_id

class Thread(models.Model):
    #user_id is the sender
    user_id = models.ForeignKey('User', blank=True, null=True)
    recipient_id = models.ForeignKey('Recipient', blank=True, null=True)
    thread_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" %(self.user_id, self.thread_created)