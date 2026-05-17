import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sacco_project.settings')
django.setup()

from django.contrib.auth import authenticate
from sacco.decorators import get_user_role
from sacco.models import Member

# Test user role detection
phone = '0781068086'
password = 'user123'

user = authenticate(username=phone, password=password)
if user:
    print(f"User: {user.username}")
    role = get_user_role(user)
    print(f"Role: {role}")

    member = Member.objects.filter(user=user).first()
    if member:
        print(f"Member: {member.name}, Role: {member.role}")
    else:
        print("No member found for user")
else:
    print("Authentication failed")