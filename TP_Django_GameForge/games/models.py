from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Game(models.Model):
    """
    Modèle principal pour un jeu vidéo généré
    """
    GENRE_CHOICES = [
        ('RPG', 'RPG'),
        ('FPS', 'FPS'),
        ('METROIDVANIA', 'Metroidvania'),
        ('VISUAL_NOVEL', 'Visual Novel'),
        ('PUZZLE', 'Puzzle'),
        ('ACTION_ADVENTURE', 'Action-Adventure'),
        ('PLATFORMER', 'Platformer'),
        ('STRATEGY', 'Strategy'),
        ('SIMULATION', 'Simulation'),
        ('HORROR', 'Horror'),
    ]
    
    THEME_CHOICES = [
        ('POST_APOCALYPTIC', 'Post-apocalyptique'),
        ('CYBERPUNK', 'Cyberpunk'),
        ('DARK_FANTASY', 'Dark Fantasy'),
        ('ONIRIC', 'Onirique'),
        ('STEAMPUNK', 'Steampunk'),
        ('SPACE', 'Spatial'),
        ('MEDIEVAL', 'Médiéval'),
        ('MODERN', 'Moderne'),
        ('FUTURISTIC', 'Futuriste'),
    ]
    
    # Informations de base
    title = models.CharField(max_length=200, verbose_name='Titre du jeu')
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games', verbose_name='Créateur')
    
    # Paramètres de génération
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, verbose_name='Genre')
    theme = models.CharField(max_length=50, choices=THEME_CHOICES, verbose_name='Thème')
    keywords = models.TextField(max_length=500, verbose_name='Mots-clés', help_text='Séparés par des virgules')
    references = models.TextField(max_length=500, blank=True, null=True, verbose_name='Références culturelles')
    
    # Contenu généré - Univers
    universe_description = models.TextField(verbose_name='Description de l\'univers')
    
    # Contenu généré - Histoire (3 actes)
    story_act1 = models.TextField(verbose_name='Histoire - Acte 1')
    story_act2 = models.TextField(verbose_name='Histoire - Acte 2')
    story_act3 = models.TextField(verbose_name='Histoire - Acte 3')
    
    # Image principale
    main_image = models.ImageField(upload_to='games/covers/', blank=True, null=True, verbose_name='Image de couverture')
    
    # Paramètres
    is_public = models.BooleanField(default=True, verbose_name='Projet public')
    is_featured = models.BooleanField(default=False, verbose_name='Mis en avant')
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Dernière modification')
    views_count = models.IntegerField(default=0, verbose_name='Nombre de vues')
    
    class Meta:
        verbose_name = 'Jeu'
        verbose_name_plural = 'Jeux'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['slug']),
            models.Index(fields=['is_public']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # S'assurer de l'unicité
            original_slug = self.slug
            counter = 1
            while Game.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('games:game_detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        """Incrémente le compteur de vues"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    @property
    def favorites_count(self):
        """Retourne le nombre de fois que le jeu a été mis en favori"""
        return self.favorited_by.count()


class Character(models.Model):
    """
    Personnage d'un jeu
    """
    ROLE_CHOICES = [
        ('PROTAGONIST', 'Protagoniste'),
        ('ANTAGONIST', 'Antagoniste'),
        ('MENTOR', 'Mentor'),
        ('ALLY', 'Allié'),
        ('NEUTRAL', 'Neutre'),
        ('RIVAL', 'Rival'),
    ]
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='characters', verbose_name='Jeu')
    name = models.CharField(max_length=200, verbose_name='Nom')
    character_class = models.CharField(max_length=100, verbose_name='Classe/Archétype')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, verbose_name='Rôle')
    background = models.TextField(verbose_name='Background/Histoire')
    gameplay_description = models.TextField(verbose_name='Description du gameplay')
    
    # Image du personnage
    image = models.ImageField(upload_to='games/characters/', blank=True, null=True, verbose_name='Image')
    
    # Ordre d'affichage
    order = models.IntegerField(default=0, verbose_name='Ordre')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    
    class Meta:
        verbose_name = 'Personnage'
        verbose_name_plural = 'Personnages'
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.name} - {self.game.title}"


class Location(models.Model):
    """
    Lieu emblématique d'un jeu
    """
    LOCATION_TYPE_CHOICES = [
        ('CITY', 'Ville'),
        ('DUNGEON', 'Donjon'),
        ('SANCTUARY', 'Sanctuaire'),
        ('RUINS', 'Ruines'),
        ('FOREST', 'Forêt'),
        ('DESERT', 'Désert'),
        ('CASTLE', 'Château'),
        ('SPACE_STATION', 'Station spatiale'),
    ]
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='locations', verbose_name='Jeu')
    name = models.CharField(max_length=200, verbose_name='Nom du lieu')
    location_type = models.CharField(max_length=50, choices=LOCATION_TYPE_CHOICES, verbose_name='Type de lieu')
    description = models.TextField(verbose_name='Description')
    
    # Image du lieu
    image = models.ImageField(upload_to='games/locations/', blank=True, null=True, verbose_name='Image')
    
    # Ordre d'affichage
    order = models.IntegerField(default=0, verbose_name='Ordre')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    
    class Meta:
        verbose_name = 'Lieu'
        verbose_name_plural = 'Lieux'
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.name} - {self.game.title}"


class Favorite(models.Model):
    """
    Système de favoris pour les jeux
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='Utilisateur')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='favorited_by', verbose_name='Jeu')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date d\'ajout')
    
    class Meta:
        verbose_name = 'Favori'
        verbose_name_plural = 'Favoris'
        unique_together = ['user', 'game']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.game.title}"


class GenerationHistory(models.Model):
    """
    Historique des générations d'IA (pour tracking et limitation)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generation_history', verbose_name='Utilisateur')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Jeu')
    generation_type = models.CharField(max_length=50, verbose_name='Type de génération')
    tokens_used = models.IntegerField(default=0, verbose_name='Tokens utilisés')
    success = models.BooleanField(default=True, verbose_name='Succès')
    error_message = models.TextField(blank=True, null=True, verbose_name='Message d\'erreur')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date')
    
    class Meta:
        verbose_name = 'Historique de génération'
        verbose_name_plural = 'Historiques de génération'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.generation_type} - {self.created_at}"