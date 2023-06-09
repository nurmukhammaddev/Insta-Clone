from django.db import models
from PIL import Image

from django.db.models.signals import post_save, post_delete

from apps.common.models import TimeStampedModel
from apps.notification.models import Notification


from apps.common.models import TimeStampedModel
from apps.users.models import User
from apps.profiles.choices import GENDER_CHOICES


class Profile(TimeStampedModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='profile_pics/empty_user.jpg', upload_to='profile_pics/')
    bio = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.user.get_full_name()} | {self.user.username}"

    @property
    def post_count(self):
        return self.user.posts.count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        im = Image.open(self.image.path)

        left = (im.width - im.height) / 2
        right = ((im.width - im.height) / 2) + im.height
        top = 0
        bottom = im.height

        im = im.crop((left, top, right, bottom))
        if im.height > 300:
            newsize = (600, 600)
            img = im.resize(newsize)
            img.save(self.image.path)

    def get_followers(self):
        followers = Profile.objects.filter(followings__followed_to=self)
        return followers

    def get_followings(self):
        followings = Profile.objects.filter(followers__followed_by=self)
        return followings


class Follower(models.Model):
    followed_to = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='followers', null=True
    )
    followed_by = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='followings', null=True
    )

    def __str__(self):
        return f"from {self.followed_by.user} to {self.followed_to.user}"

