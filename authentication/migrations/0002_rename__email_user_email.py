# Generated by Django 4.1.7 on 2023-03-19 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='_email',
            new_name='email',
        ),
    ]
