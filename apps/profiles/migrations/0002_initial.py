# Generated by Django 3.2.18 on 2023-04-05 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='follower',
            name='followed_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_by', to='profiles.profile'),
        ),
        migrations.AddField(
            model_name='follower',
            name='followed_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_to', to='profiles.profile'),
        ),
    ]
