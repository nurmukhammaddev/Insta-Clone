# Generated by Django 4.1.7 on 2023-03-31 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_postmedia_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='allow_commentary',
            field=models.BooleanField(default=True, verbose_name='allow commentary'),
        ),
    ]