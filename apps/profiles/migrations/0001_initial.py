# Generated by Django 4.1.7 on 2023-04-07 11:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('image', models.ImageField(default='profile_pics/empty_user.jpg', upload_to='profile_pics/')),
                ('bio', models.CharField(blank=True, max_length=200)),
                ('gender', models.CharField(choices=[('Male', 'male'), ('Female', 'female')], max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_by', to='profiles.profile')),
                ('followed_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_to', to='profiles.profile')),
            ],
        ),
    ]
