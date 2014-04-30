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
    relationships = models.ManyToManyField('self', through='Relationship', 
                                           symmetrical=False, 
                                           related_name='related_to')
    avatar = models.ImageField(upload_to='avatars', default = 'avatars/default.jpg')
    objects = PeeUserManager()

    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

    def add_relationship(self, person, status):
        relationship, created = Relationship.objects.get_or_create(
            from_person=self,
            to_person=person,
            status=status)
        return relationship

    def remove_relationship(self, person, status):
        Relationship.objects.filter(
            from_person=self, 
            to_person=person,
            status=status).delete()
        return

    def get_relationships(self, status):
        return self.relationships.filter(
            to_people__status=status, 
            to_people__from_person=self)

    def get_related_to(self, status):
        return self.related_to.filter(
            from_people__status=status, 
            from_people__to_person=self)

    def get_following(self):
        return self.get_relationships(RELATIONSHIP_FOLLOWING)

    def get_followers(self):
        return self.get_related_to(RELATIONSHIP_FOLLOWING)


# class ImageUploadForm(forms.Form):
#     """Image upload form."""
#     image = forms.ImageField()

RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
)

class Relationship(models.Model):
    from_person = models.ForeignKey(PeeUser, related_name='from_people')
    to_person = models.ForeignKey(PeeUser, related_name='to_people')
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)


def key_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
