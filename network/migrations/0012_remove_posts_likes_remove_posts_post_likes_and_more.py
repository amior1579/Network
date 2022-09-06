# Generated by Django 4.0.5 on 2022-09-06 10:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_posts_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='post_likes',
        ),
        migrations.AddField(
            model_name='posts',
            name='post_likes',
            field=models.ManyToManyField(blank=True, default=None, related_name='post_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
