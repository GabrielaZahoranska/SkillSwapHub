# skills/views.py

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import SkillListing


def landing(request):
    # Home page anyone can see: short intro plus newest listings
    recent_skills = SkillListing.objects.select_related('category', 'user').order_by('-created_at')[:6]
    return render(request, 'landing.html', {'recent_skills': recent_skills})


def about(request):
    return render(request, 'about.html')


class SkillListingList(ListView):
    model = SkillListing
    template_name = 'skills/skill_listing_list.html'
    context_object_name = 'skill_listings'

    def get_queryset(self):
        return SkillListing.objects.select_related('category', 'user').all()


class SkillListingDetail(DetailView):
    model = SkillListing
    template_name = 'skills/skill_listing_detail.html'


class SkillListingCreate(LoginRequiredMixin, CreateView):
    model = SkillListing
    fields = ['title', 'category', 'description']
    template_name = 'skills/skill_listing_form.html'

    def form_valid(self, form):
        # Tie the listing to whoever is logged in
        form.instance.user = self.request.user
        return super().form_valid(form)


class SkillListingOwnerMixin(UserPassesTestMixin):
    """Only the person who created the row may update or delete it."""

    def test_func(self):
        listing = self.get_object()
        return listing.user_id == self.request.user.pk


class SkillListingUpdate(LoginRequiredMixin, SkillListingOwnerMixin, UpdateView):
    model = SkillListing
    fields = ['title', 'category', 'description']
    template_name = 'skills/skill_listing_form.html'


class SkillListingDelete(LoginRequiredMixin, SkillListingOwnerMixin, DeleteView):
    model = SkillListing
    template_name = 'skills/skill_listing_confirm_delete.html'
    success_url = reverse_lazy('skill-list')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('skill-list')
        else:
            error_message = 'Invalid sign up - try again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
