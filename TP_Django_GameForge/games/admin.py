from django.contrib import admin
from .models import Game, Character, Location, Favorite, GenerationHistory


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """
    Administration des jeux
    """
    list_display = ('title', 'creator', 'genre', 'theme', 'is_public', 'views_count', 'created_at')
    list_filter = ('genre', 'theme', 'is_public', 'is_featured', 'created_at')
    search_fields = ('title', 'creator__username', 'keywords', 'universe_description')
    readonly_fields = ('slug', 'created_at', 'updated_at', 'views_count')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('title', 'slug', 'creator', 'is_public', 'is_featured')
        }),
        ('Paramètres de génération', {
            'fields': ('genre', 'theme', 'keywords', 'references')
        }),
        ('Contenu généré - Univers', {
            'fields': ('universe_description',),
            'classes': ('collapse',)
        }),
        ('Contenu généré - Histoire', {
            'fields': ('story_act1', 'story_act2', 'story_act3'),
            'classes': ('collapse',)
        }),
        ('Médias', {
            'fields': ('main_image',)
        }),
        ('Métadonnées', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('creator')


class CharacterInline(admin.TabularInline):
    """
    Inline pour les personnages dans l'admin Game
    """
    model = Character
    extra = 0
    fields = ('name', 'character_class', 'role', 'order')


class LocationInline(admin.TabularInline):
    """
    Inline pour les lieux dans l'admin Game
    """
    model = Location
    extra = 0
    fields = ('name', 'location_type', 'order')


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    """
    Administration des personnages
    """
    list_display = ('name', 'game', 'character_class', 'role', 'order', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('name', 'game__title', 'background')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('game', 'name', 'character_class', 'role', 'order')
        }),
        ('Description', {
            'fields': ('background', 'gameplay_description')
        }),
        ('Médias', {
            'fields': ('image',)
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """
    Administration des lieux
    """
    list_display = ('name', 'game', 'location_type', 'order', 'created_at')
    list_filter = ('location_type', 'created_at')
    search_fields = ('name', 'game__title', 'description')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('game', 'name', 'location_type', 'order')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Médias', {
            'fields': ('image',)
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """
    Administration des favoris
    """
    list_display = ('user', 'game', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'game__title')
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'game')


@admin.register(GenerationHistory)
class GenerationHistoryAdmin(admin.ModelAdmin):
    """
    Administration de l'historique des générations
    """
    list_display = ('user', 'game', 'generation_type', 'success', 'tokens_used', 'created_at')
    list_filter = ('success', 'generation_type', 'created_at')
    search_fields = ('user__username', 'game__title')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Informations', {
            'fields': ('user', 'game', 'generation_type', 'success')
        }),
        ('Détails', {
            'fields': ('tokens_used', 'error_message')
        }),
        ('Métadonnées', {
            'fields': ('created_at',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'game')