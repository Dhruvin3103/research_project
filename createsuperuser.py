import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def create_superuser():
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin',  'admin')
        print('Superuser created successfully.')
    else:
        print('Superuser already exists.')


if __name__ == '__main__':
    create_superuser()
