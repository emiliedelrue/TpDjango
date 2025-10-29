from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegistrationForm(UserCreationForm):
    """
    Formulaire d'inscription utilisateur avec validation personnalisée
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre email',
            'autocomplete': 'email'
        })
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choisissez un nom d\'utilisateur',
            'autocomplete': 'username'
        })
    )
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Créez un mot de passe',
            'autocomplete': 'new-password'
        })
    )
    password2 = forms.CharField(
        label='Confirmation du mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmez votre mot de passe',
            'autocomplete': 'new-password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        """
        Vérifie que l'email n'est pas déjà utilisé
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Cet email est déjà utilisé.")
        return email

    def clean_username(self):
        """
        Vérifie que le username respecte les critères et n'est pas déjà pris
        """
        username = self.cleaned_data.get('username')
        
        # Vérifier la longueur minimale
        if len(username) < 3:
            raise ValidationError("Le nom d'utilisateur doit contenir au moins 3 caractères.")
        
        # Vérifier que le username n'est pas déjà pris
        if User.objects.filter(username=username).exists():
            raise ValidationError("Ce nom d'utilisateur est déjà pris.")
        
        return username

    def clean_password2(self):
        """
        Vérifie que les deux mots de passe correspondent
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        
        return password2

    def save(self, commit=True):
        """
        Sauvegarde l'utilisateur avec l'email
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """
    Formulaire de connexion personnalisé
    """
    username = forms.CharField(
        label='Nom d\'utilisateur ou Email',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom d\'utilisateur ou Email',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe',
            'autocomplete': 'current-password'
        })
    )

    def clean_username(self):
        """
        Permet la connexion avec username ou email
        """
        username_or_email = self.cleaned_data.get('username')
        
        # Si c'est un email, on récupère le username associé
        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                return user.username
            except User.DoesNotExist:
                pass
        
        return username_or_email


class UserProfileUpdateForm(forms.ModelForm):
    """
    Formulaire de mise à jour du profil utilisateur
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    first_name = forms.CharField(
        required=False,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prénom (optionnel)'
        })
    )
    last_name = forms.CharField(
        required=False,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom (optionnel)'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom d\'utilisateur',
                'readonly': 'readonly'  # On ne peut pas changer le username
            })
        }

    def clean_email(self):
        """
        Vérifie que l'email n'est pas déjà utilisé par un autre utilisateur
        """
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        
        # Vérifier si un autre utilisateur utilise déjà cet email
        if User.objects.filter(email=email).exclude(username=username).exists():
            raise ValidationError("Cet email est déjà utilisé par un autre utilisateur.")
        
        return email


class PasswordChangeCustomForm(forms.Form):
    """
    Formulaire personnalisé pour changer le mot de passe
    """
    old_password = forms.CharField(
        label='Mot de passe actuel',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe actuel'
        })
    )
    new_password1 = forms.CharField(
        label='Nouveau mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nouveau mot de passe'
        })
    )
    new_password2 = forms.CharField(
        label='Confirmer le nouveau mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe'
        })
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        """
        Vérifie que l'ancien mot de passe est correct
        """
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise ValidationError("Le mot de passe actuel est incorrect.")
        return old_password

    def clean_new_password2(self):
        """
        Vérifie que les deux nouveaux mots de passe correspondent
        """
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les nouveaux mots de passe ne correspondent pas.")
        
        # Vérifier la force du mot de passe
        if len(password1) < 8:
            raise ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        
        return password2

    def save(self, commit=True):
        """
        Change le mot de passe de l'utilisateur
        """
        password = self.cleaned_data['new_password1']
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class AccountDeletionForm(forms.Form):
    """
    Formulaire de confirmation pour la suppression de compte
    """
    password = forms.CharField(
        label='Confirmez votre mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre mot de passe pour confirmer'
        })
    )
    confirm = forms.BooleanField(
        required=True,
        label='Je comprends que cette action est irréversible',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        """
        Vérifie que le mot de passe est correct
        """
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise ValidationError("Mot de passe incorrect.")
        return password