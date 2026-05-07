from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q

from .models import SkillListing


class EmailLoginForm(AuthenticationForm):
    """Looks like email; checks the same normalized value Django stores as username."""

    username = forms.EmailField(
        label='Email address',
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )

    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': ('Please enter a correct email address and password.'),
    }

    def clean_username(self):
        email = self.cleaned_data.get('username')
        if email:
            return email.strip().lower()
        return email


class SkillListingForm(forms.ModelForm):
    """Listing form — contact email stored on the row so it always shows."""

    class Meta:
        model = SkillListing
        fields = ('title', 'contact_email', 'category', 'description')
        widgets = {
            'contact_email': forms.EmailInput(
                attrs={
                    'placeholder': 'you@example.com',
                    'autocomplete': 'email',
                }
            ),
            'description': forms.Textarea(attrs={'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ce = self.fields['contact_email']
        ce.required = True
        ce.label = 'Your contact email (shown on the listing)'
        ce.help_text = 'Learners will use this to reach you. It appears on your public skill page.'

    def clean_contact_email(self):
        raw = self.cleaned_data.get('contact_email') or ''
        email = raw.strip().lower()
        if not email:
            raise forms.ValidationError('Please enter your contact email.')
        return email


class SignUpForm(UserCreationForm):
    """
    One email field stores both User.username (login key) and User.email.
    HTML5 EmailField validates format before save.
    """

    username = forms.EmailField(
        label='Email address',
        max_length=254,
        help_text='You sign in with this address. Format: name@example.com.',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'you@example.com',
                'autocomplete': 'email',
            }
        ),
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_username(self):
        v = self.cleaned_data['username'].strip().lower()
        self.cleaned_data['username'] = v
        clash = User.objects.filter(
            Q(email__iexact=v) & ~Q(username__iexact=v)
        ).exists()
        if clash:
            raise forms.ValidationError('An account with this email already exists.')
        return super().clean_username()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.username
        if commit:
            user.save()
        return user


class UserEmailUpdateForm(forms.ModelForm):
    """Change sign-in email: keeps username and email identical."""

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, user=None, **kwargs):
        self._account_user = user
        super().__init__(*args, **kwargs)
        fld = self.fields['email']
        fld.required = True
        fld.label = 'Email address'
        fld.widget = forms.EmailInput(
            attrs={'placeholder': 'you@example.com', 'autocomplete': 'email'}
        )

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        qs = User.objects.filter(
            Q(username__iexact=email) | Q(email__iexact=email)
        )
        if self._account_user is not None:
            qs = qs.exclude(pk=self._account_user.pk)
        if qs.exists():
            raise forms.ValidationError('That email is already used by another account.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].strip().lower()
        user.username = user.email
        if commit:
            user.save()
        return user
