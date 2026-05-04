from django.urls import path
from . import views  # wires URLs to views

urlpatterns = [
    path('', views.landing, name='home'),
    path('about/', views.about, name='about'),
    path('skills/', views.SkillListingList.as_view(), name='skill-list'),
    path('skills/<int:pk>/', views.SkillListingDetail.as_view(), name='skill-detail'),
    path('skills/create/', views.SkillListingCreate.as_view(), name='skill-create'),
    path('skills/<int:pk>/update/', views.SkillListingUpdate.as_view(), name='skill-update'),
    path('skills/<int:pk>/delete/', views.SkillListingDelete.as_view(), name='skill-delete'),
    path('accounts/signup/', views.signup, name='signup'),
]
