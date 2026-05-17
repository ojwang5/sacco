import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sacco_project.settings')
django.setup()

from django.conf import settings
settings.DEBUG = True

from django.test import Client
c = Client()
for path in ['/login/', '/withdrawals/']:
    r = c.get(path)
    print(f"{path} => {r.status_code}")
    if r.status_code == 500:
        print(r.content.decode('utf-8', errors='replace'))
        break
else:
    print('No 500')
