# Generated by Django 5.0.6 on 2024-08-26 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mychat', '0002_alter_profile_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(blank=True, null=True, related_name='my_friends', to='mychat.friend'),
        ),
    ]
