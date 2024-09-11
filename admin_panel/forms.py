from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import PredefinedMessage, ChatbotUser, Administrateur, AdministrateurPrincipal

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("password1", "password2")

User = get_user_model()

class PredefinedMessageForm(forms.ModelForm):
    class Meta:
        model = PredefinedMessage
        fields = ['title', 'content']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ChatbotUserForm(forms.ModelForm):
    class Meta:
        model = ChatbotUser
        fields = ['name', 'email', 'password']

class AdministrateurForm(forms.ModelForm):
    class Meta:
        model = Administrateur
        fields = ['id', 'nom', 'prenom', 'email', 'mot_de_passe']

class AdministrateurPrincipalForm(forms.ModelForm):
    class Meta:
        model = AdministrateurPrincipal
        fields = ['id', 'nom', 'prenom', 'email', 'mot_de_passe']

