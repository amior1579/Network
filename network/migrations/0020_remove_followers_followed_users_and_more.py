# Generated by Django 4.0.5 on 2022-09-10 05:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0019_remove_followers_user_followers_followed_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followers',
            name='followed_users',
        ),
        migrations.AddField(
            model_name='followers',
            name='followed_users',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='followed_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
