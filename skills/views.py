# skills/views.py

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .forms import SignUpForm, UserEmailUpdateForm, SkillListingForm
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


def _sync_user_email_from_listing(listing_owner_pk, listing_email):
    """If auth User still has empty email, copy the listing email (one-time fill)."""
    listing_email = (listing_email or '').strip().lower()
    if not listing_email:
        return
    owner = User.objects.filter(pk=listing_owner_pk).only('email').first()
    if owner and not (owner.email or '').strip():
        User.objects.filter(pk=listing_owner_pk).update(email=listing_email)


class SkillListingCreate(LoginRequiredMixin, CreateView):
    model = SkillListing
    form_class = SkillListingForm
    template_name = 'skills/skill_listing_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        _sync_user_email_from_listing(
            self.request.user.pk, form.cleaned_data.get('contact_email', '')
        )
        return response


class SkillListingOwnerMixin(UserPassesTestMixin):
    """Only the person who created the row may update or delete it."""

    def test_func(self):
        listing = self.get_object()
        return listing.user_id == self.request.user.pk


class SkillListingUpdate(LoginRequiredMixin, SkillListingOwnerMixin, UpdateView):
    model = SkillListing
    form_class = SkillListingForm
    template_name = 'skills/skill_listing_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        _sync_user_email_from_listing(
            form.instance.user_id, form.cleaned_data.get('contact_email', '')
        )
        return response


class SkillListingDelete(LoginRequiredMixin, SkillListingOwnerMixin, DeleteView):
    model = SkillListing
    template_name = 'skills/skill_listing_confirm_delete.html'
    success_url = reverse_lazy('skill-list')


@login_required
def profile_email(request):
    if request.method == 'POST':
        form = UserEmailUpdateForm(request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your email was saved.')
            return redirect('profile-email')
    else:
        form = UserEmailUpdateForm(instance=request.user, user=request.user)
    return render(request, 'profile_email.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('skill-list')
    else:
        form = SignUpForm()

    return render(
        request,
        'signup.html',
        {
            'form': form,
        },
    )
