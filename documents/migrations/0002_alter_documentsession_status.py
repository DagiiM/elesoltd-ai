# Generated by Django 4.1.7 on 2023-02-26 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentsession',
            name='status',
            field=models.CharField(default='draft', max_length=50),
        ),
    ]