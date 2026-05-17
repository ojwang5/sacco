import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sacco_project.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from sacco.models import Member

# Fix the password for the test user
phone = '0781068086'
password = 'user123'

print(f"Fixing password for user: {phone}")

user = User.objects.filter(username=phone).first()
if user:
    user.set_password(password)
    user.save()
    print("✅ Password updated successfully")

    # Test authentication again
    auth_user = authenticate(username=phone, password=password)
    if auth_user:
        print("✅ Authentication now works!")
        print(f"Authenticated user: {auth_user.username}")
    else:
        print("❌ Authentication still failed")
else:
    print("❌ User not found")

print(f"\nLogin credentials:")
print(f"Phone: {phone}")
print(f"Password: {password}")