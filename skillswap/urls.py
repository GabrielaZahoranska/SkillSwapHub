"""
Root URL routing for SkillSwap Hub.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('skills.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
