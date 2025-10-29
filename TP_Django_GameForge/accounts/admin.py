from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """
    Inline admin pour afficher le profil dans l'admin User
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profil'
    fields = ('bio', 'avatar', 'date_of_birth', 'website', 'newsletter_subscribed', 
              'email_notifications', 'total_generations')
    readonly_fields = ('total_generations', 'created_at', 'updated_at')


class UserAdmin(BaseUserAdmin):
    """
    Admin personnalisé pour User avec profil inline
    """
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')


# Désenregistrer le User admin par défaut et enregistrer le notre
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin pour UserProfile
    """
    list_display = ('user', 'total_generations', 'newsletter_subscribed', 'created_at')
    list_filter = ('newsletter_subscribed', 'email_notifications', 'created_at')
    search_fields = ('user__username', 'user__email', 'bio')
    readonly_fields = ('created_at', 'updated_at', 'total_generations')
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Informations personnelles', {
            'fields': ('bio', 'avatar', 'date_of_birth', 'website')
        }),
        ('Préférences', {
            'fields': ('newsletter_subscribed', 'email_notifications')
        }),
        ('Statistiques', {
            'fields': ('total_generations', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )