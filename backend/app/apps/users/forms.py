from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data["username"].strip()

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                "A user with this username already exists."
            )

        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "A user with this email address already exists."
            )

        return email


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")


class EmailVerificationForm(forms.Form):
    code = forms.CharField(min_length=6, max_length=6,
        error_messages={
            "required": "Empty your verification code.",
        }
    )

    def clean_code(self):
        code = self.cleaned_data["code"]
        if not code.isdigit():
            raise ValidationError("The code must contain only digits.")
        if len(code) != 6:
            raise ValidationError("Enter the correct confirmation code.")
        else:
            return code

    def __str__(self):
        return self.code



