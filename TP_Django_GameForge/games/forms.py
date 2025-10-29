from django import forms
from .models import Game, Character, Location


class GameCreationForm(forms.ModelForm):
    """
    Formulaire de création de jeu guidée
    """
    keywords = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: boucle temporelle, vengeance, IA rebelle...',
            'rows': 3
        }),
        help_text='Séparez les mots-clés par des virgules'
    )
    
    references = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Zelda, Hollow Knight, Disco Elysium...',
            'rows': 2
        }),
        help_text='Références culturelles optionnelles'
    )
    
    class Meta:
        model = Game
        fields = ['title', 'genre', 'theme', 'keywords', 'references']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Donnez un titre à votre jeu'
            }),
            'genre': forms.Select(attrs={
                'class': 'form-control'
            }),
            'theme': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'title': 'Titre du jeu',
            'genre': 'Genre du jeu',
            'theme': 'Ambiance visuelle et narrative',
        }


class GameUpdateForm(forms.ModelForm):
    """
    Formulaire de mise à jour d'un jeu
    """
    class Meta:
        model = Game
        fields = ['title', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class CharacterForm(forms.ModelForm):
    """
    Formulaire pour créer/éditer un personnage manuellement
    """
    class Meta:
        model = Character
        fields = ['name', 'character_class', 'role', 'background', 'gameplay_description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du personnage'
            }),
            'character_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Guerrier, Mage, Voleur...'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control'
            }),
            'background': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Histoire et background du personnage'
            }),
            'gameplay_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description du gameplay (capacités, style de jeu...)'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }


class LocationForm(forms.ModelForm):
    """
    Formulaire pour créer/éditer un lieu manuellement
    """
    class Meta:
        model = Location
        fields = ['name', 'location_type', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du lieu'
            }),
            'location_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Description détaillée du lieu'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }


class GameSearchForm(forms.Form):
    """
    Formulaire de recherche de jeux
    """
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher un jeu...'
        })
    )
    
    genre = forms.ChoiceField(
        required=False,
        choices=[('', 'Tous les genres')] + Game.GENRE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    theme = forms.ChoiceField(
        required=False,
        choices=[('', 'Tous les thèmes')] + Game.THEME_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Plus récents'),
            ('-views_count', 'Plus vus'),
            ('title', 'Titre (A-Z)'),
            ('-title', 'Titre (Z-A)'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )