"""
NOVA/FORM — Custom Forms

Styled forms for registration, login, and checkout.
All forms use CSRF protection and server-side validation.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    """Custom registration form with email and name fields."""
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'First name',
            'autocomplete': 'given-name',
            'id': 'reg-first-name',
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last name',
            'autocomplete': 'family-name',
            'id': 'reg-last-name',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address',
            'autocomplete': 'email',
            'id': 'reg-email',
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'autocomplete': 'new-password',
            'id': 'reg-password',
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm password',
            'autocomplete': 'new-password',
            'id': 'reg-password-confirm',
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Custom login form."""
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address',
            'autocomplete': 'email',
            'id': 'login-email',
        }),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'autocomplete': 'current-password',
            'id': 'login-password',
        })
    )


class CheckoutForm(forms.Form):
    """Checkout form for shipping information."""
    full_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Full name',
            'autocomplete': 'name',
            'id': 'checkout-name',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address',
            'autocomplete': 'email',
            'id': 'checkout-email',
        })
    )
    address = forms.CharField(
        max_length=300,
        widget=forms.TextInput(attrs={
            'placeholder': 'Street address',
            'autocomplete': 'street-address',
            'id': 'checkout-address',
        })
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'City',
            'autocomplete': 'address-level2',
            'id': 'checkout-city',
        })
    )
    state = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'State / Province',
            'autocomplete': 'address-level1',
            'id': 'checkout-state',
        })
    )
    postal_code = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'Postal code',
            'autocomplete': 'postal-code',
            'id': 'checkout-postal',
        })
    )
    country = forms.CharField(
        max_length=100,
        initial='United States',
        widget=forms.TextInput(attrs={
            'placeholder': 'Country',
            'autocomplete': 'country-name',
            'id': 'checkout-country',
        })
    )
