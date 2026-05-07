"""
Root URL routing for SkillSwap Hub.
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from skills.forms import EmailLoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('skills.urls')),
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(authentication_form=EmailLoginForm),
        name='login',
    ),
    path('accounts/', include('django.contrib.auth.urls')),
]
