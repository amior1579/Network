# Generated by Django 4.0.5 on 2022-09-06 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='post_likes',
            field=models.IntegerField(default=0),
        ),
    ]
