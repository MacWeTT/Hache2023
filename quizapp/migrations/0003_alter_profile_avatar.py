# Generated by Django 4.1.7 on 2023-03-01 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0002_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='avatar.svg', null=True, upload_to='user_data'),
        ),
    ]
