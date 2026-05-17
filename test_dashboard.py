import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sacco_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import authenticate
from sacco.models import Member

# Test dashboard access
client = Client()

# Login first
phone = '0781068086'
password = 'user123'

# Authenticate user
user = authenticate(username=phone, password=password)
if user:
    print(f"✅ User authenticated: {user.username}")

    # Login via client
    login_success = client.login(username=phone, password=password)
    if login_success:
        print("✅ Client login successful")

        # Try to access dashboard
        response = client.get('/')

        print(f"Dashboard response status: {response.status_code}")

        if response.status_code == 200:
            print("✅ Dashboard loaded successfully")
        else:
            print("❌ Dashboard failed")
            print("Response content preview:")
            print(response.content.decode('utf-8', errors='replace')[:1000])

    else:
        print("❌ Client login failed")
else:
    print("❌ Authentication failed")