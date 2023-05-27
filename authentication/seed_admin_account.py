from django.db import migrations
from .models import User

def create_superuser(apps, schema_editor):
    User = apps.get_model('authentication', 'User')
    User.objects.create_superuser(
        email='douglasmutethia2017@gmail.com.com',
        username='admin',
        password='admin',
        first_name='Douglas',
        last_name='Mutethia'
    )

class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]

   #python manage.py makemigrations --empty authentication --name seed_admin_account
