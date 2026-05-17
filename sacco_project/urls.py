from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # include sacco app at root or under /sacco/ depending on your dashboard links
    # If your templates use {% url 'sacco:members_list' %} and expect /sacco/... use the second option.
    path('', include(('sacco.urls', 'sacco'), namespace='sacco')),   # root (http://127.0.0.1:8000/)
    # OR use this if you want sacco pages under /sacco/:
    # path('sacco/', include(('sacco.urls', 'sacco'), namespace='sacco')),
]
