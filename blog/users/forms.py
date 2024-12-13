from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, AbstractBaseUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from .models import Profile

class RegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True, help_text="exx@gmail.com")
    class Meta:
        model=User
        fields=['email', 'username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user: AbstractBaseUser) -> None:
        if not user.profile.activated:
            raise forms.ValidationError(f"Check your email: {user.email} and confirm your acccount first!")
        return super().confirm_login_allowed(user)
    
class ChangeImageForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image']
        