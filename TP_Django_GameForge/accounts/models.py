from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Extension du modèle User pour ajouter des informations supplémentaires
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name='Biographie')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Date de naissance')
    website = models.URLField(max_length=200, blank=True, null=True, verbose_name='Site web')
    
    # Préférences
    newsletter_subscribed = models.BooleanField(default=True, verbose_name='Abonné à la newsletter')
    email_notifications = models.BooleanField(default=True, verbose_name='Notifications par email')
    
    # Statistiques
    total_generations = models.IntegerField(default=0, verbose_name='Nombre total de générations')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Dernière modification')

    class Meta:
        verbose_name = 'Profil utilisateur'
        verbose_name_plural = 'Profils utilisateurs'

    def __str__(self):
        return f"Profil de {self.user.username}"

    def increment_generations(self):
        """Incrémente le compteur de générations"""
        self.total_generations += 1
        self.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal pour créer automatiquement un profil lors de la création d'un utilisateur
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal pour sauvegarder automatiquement le profil lors de la sauvegarde d'un utilisateur
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()