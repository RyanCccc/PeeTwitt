from django.db import models
from django import forms
from django.contrib.auth.models import User as Auth_User
import string
import random

class PeeUserManager(models.Manager):
    def create_user(
        self,
        email,
        password,
        firstname,
        lastname,
    ):
        user = Auth_User.objects.create_user(
                email,
                email,
                password,
                first_name=firstname,
                last_name=lastname,
            )
        user.is_active = False
        user.save()
        active_key = key_generator()
        pee_user = self.create(
                user=user,
                pwd=password,
                active_key=active_key,
            )
        return pee_user

# Create your models here.
class PeeUser(models.Model):
    user = models.OneToOneField(Auth_User, primary_key=True)
    pwd = models.CharField(max_length=100)
    active_key = models.CharField(max_length=100, unique=True)
    followings = models.ManyToManyField("self", related_name="followers")
    avatar = models.ImageField(upload_to='avatars', default = 'avatars/default.jpg')
    objects = PeeUserManager()

    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)


# class ImageUploadForm(forms.Form):
#     """Image upload form."""
#     image = forms.ImageField()


def key_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
