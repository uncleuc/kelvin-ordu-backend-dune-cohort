from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=150, required=True, label='Name')
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        # map `name` into first_name for simplicity
        user.first_name = self.cleaned_data.get('name', '')
        if commit:
            user.save()
        return user
