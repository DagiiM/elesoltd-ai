# Generated by Django 4.1.7 on 2023-02-27 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_alter_resume_cover_letter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='contact_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resume',
            name='cover_letter',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resume',
            name='education',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resume',
            name='references',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resume',
            name='work_experience',
            field=models.TextField(blank=True, null=True),
        ),
    ]
