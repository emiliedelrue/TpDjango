from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    UserRegistrationForm, 
    UserLoginForm, 
    UserProfileUpdateForm,
    PasswordChangeCustomForm,
    AccountDeletionForm
)
from django.contrib.auth.models import User


def register_view(request):
    """
    Vue d'inscription d'un nouvel utilisateur
    """
    if request.user.is_authenticated:
        return redirect('games:dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé avec succès pour {username}! Vous pouvez maintenant vous connecter.')
            login(request, user)
            return redirect('games:dashboard')
        else:
            messages.error(request, 'Erreur lors de la création du compte. Veuillez corriger les erreurs ci-dessous.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Vue de connexion
    """
    if request.user.is_authenticated:
        return redirect('games:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue, {user.username}!')
                
                # Redirection vers la page demandée ou dashboard
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('games:dashboard')
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    Vue de déconnexion
    """
    username = request.user.username
    logout(request)
    messages.info(request, f'Vous êtes maintenant déconnecté. À bientôt {username}!')
    return redirect('home')


@login_required
def profile_view(request):
    """
    Vue du profil utilisateur
    """
    user = request.user
    
    # Compter les statistiques de l'utilisateur
    context = {
        'user': user,
        'total_games': user.games.count() if hasattr(user, 'games') else 0,
        'public_games': user.games.filter(is_public=True).count() if hasattr(user, 'games') else 0,
        'private_games': user.games.filter(is_public=False).count() if hasattr(user, 'games') else 0,
        'total_favorites': user.favorites.count() if hasattr(user, 'favorites') else 0,
    }
    
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_update_view(request):
    """
    Vue de mise à jour du profil
    """
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Erreur lors de la mise à jour du profil.')
    else:
        form = UserProfileUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile_update.html', {'form': form})


@login_required
def password_change_view(request):
    """
    Vue de changement de mot de passe
    """
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important pour ne pas déconnecter l'utilisateur
            messages.success(request, 'Votre mot de passe a été changé avec succès!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = PasswordChangeCustomForm(request.user)
    
    return render(request, 'accounts/password_change.html', {'form': form})


@login_required
def account_delete_view(request):
    """
    Vue de suppression de compte
    """
    if request.method == 'POST':
        form = AccountDeletionForm(request.user, request.POST)
        if form.is_valid():
            user = request.user
            username = user.username
            logout(request)
            user.delete()
            messages.success(request, f'Le compte {username} a été supprimé définitivement.')
            return redirect('home')
        else:
            messages.error(request, 'Erreur lors de la suppression du compte.')
    else:
        form = AccountDeletionForm(request.user)
    
    return render(request, 'accounts/account_delete.html', {'form': form})


@login_required
def settings_view(request):
    """
    Vue de la page des paramètres généraux
    """
    return render(request, 'accounts/settings.html')