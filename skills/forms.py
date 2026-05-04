from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """Same as Django's sign-up plus email, actually stored on User.email."""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        # One account per email so contact info stays unambiguous on listings.
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError('An account with that email already exists.')
        return email
