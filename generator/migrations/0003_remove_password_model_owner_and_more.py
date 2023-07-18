# Generated by Django 4.2.1 on 2023-05-09 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0002_password_model_delete_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='password_model',
            name='owner',
        ),
        migrations.AddField(
            model_name='password_model',
            name='email_address',
            field=models.EmailField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]