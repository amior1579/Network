# Generated by Django 4.0.5 on 2022-09-10 06:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0020_remove_followers_followed_users_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followers',
            name='followed_users',
        ),
        migrations.AddField(
            model_name='followers',
            name='followed_users',
            field=models.ManyToManyField(blank=True, default=None, related_name='followed_users', to=settings.AUTH_USER_MODEL),
        ),
    ]