from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")
        

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")


class EmailVerificationForm(forms.Form):
    code = forms.CharField(min_length=6, max_length=6,
        error_messages={
        "required": "Enter the confirmation code.",
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



