from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Game, Character, Location, Favorite, GenerationHistory
from .forms import GameCreationForm, GameUpdateForm, GameSearchForm
from .services import AITextGenerator, AIImageGenerator
import json


def home_view(request):
    """
    Page d'accueil avec tous les jeux publics
    """
    games = Game.objects.filter(is_public=True).select_related('creator').annotate(
        favorites_count=Count('favorited_by')
    ).order_by('-created_at')
    
    # Recherche et filtres
    search_form = GameSearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        genre = search_form.cleaned_data.get('genre')
        theme = search_form.cleaned_data.get('theme')
        sort_by = search_form.cleaned_data.get('sort_by')
        
        if query:
            games = games.filter(
                Q(title__icontains=query) | 
                Q(keywords__icontains=query) |
                Q(creator__username__icontains=query)
            )
        
        if genre:
            games = games.filter(genre=genre)
        
        if theme:
            games = games.filter(theme=theme)
        
        if sort_by:
            games = games.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(games, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_games': Game.objects.filter(is_public=True).count(),
    }
    
    return render(request, 'games/home.html', context)


@login_required
def dashboard_view(request):
    """
    Tableau de bord personnel de l'utilisateur
    """
    user_games = Game.objects.filter(creator=request.user).annotate(
        favorites_count=Count('favorited_by')
    ).order_by('-created_at')
    
    context = {
        'games': user_games,
        'total_games': user_games.count(),
        'public_games': user_games.filter(is_public=True).count(),
        'private_games': user_games.filter(is_public=False).count(),
    }
    
    return render(request, 'games/dashboard.html', context)


@login_required
def game_create_view(request):
    """
    Vue de création d'un nouveau jeu
    """
    if request.method == 'POST':
        form = GameCreationForm(request.POST)
        if form.is_valid():
            try:
                # Créer le jeu sans le sauvegarder encore
                game = form.save(commit=False)
                game.creator = request.user
                
                # Initialiser les générateurs IA
                text_generator = AITextGenerator()
                image_generator = AIImageGenerator()
                
                # Convertir les keywords en liste
                keywords_list = [k.strip() for k in game.keywords.split(',')]
                
                # Générer l'univers
                universe_data = text_generator.generate_universe(
                    genre=game.get_genre_display(),
                    theme=game.get_theme_display(),
                    keywords=keywords_list,
                    references=game.references or ""
                )
                game.universe_description = universe_data['description']
                
                # Générer l'histoire
                story_data = text_generator.generate_story(
                    universe_description=game.universe_description,
                    genre=game.get_genre_display()
                )
                game.story_act1 = story_data['act1']
                game.story_act2 = story_data['act2']
                game.story_act3 = story_data['act3']
                
                # Sauvegarder le jeu
                game.save()
                
                # Générer les personnages (2 à 4)
                num_characters = 3
                for i in range(num_characters):
                    role = ['PROTAGONIST', 'ANTAGONIST', 'ALLY'][i] if i < 3 else 'NEUTRAL'
                    
                    character_data = text_generator.generate_character(
                        universe_description=game.universe_description,
                        role=role,
                        character_number=i
                    )
                    
                    character = Character.objects.create(
                        game=game,
                        name=character_data['name'],
                        character_class=character_data['character_class'],
                        role=role,
                        background=character_data['background'],
                        gameplay_description=character_data['gameplay_description'],
                        order=i
                    )
                    
                    # Générer une image pour le personnage (optionnel)
                    if i == 0:  # Seulement pour le protagoniste pour économiser les API calls
                        try:
                            image_bytes = image_generator.generate_character_image(
                                character_name=character_data['name'],
                                character_description=character_data['background'][:200],
                                art_style=game.get_theme_display()
                            )
                            if image_bytes:
                                character.image.save(
                                    f"{character.name.replace(' ', '_')}.png",
                                    image_generator.save_image_to_model(image_bytes, f"{character.name}.png"),
                                    save=True
                                )
                        except Exception as e:
                            print(f"Erreur génération image personnage: {e}")
                
                # Générer les lieux (2 à 3)
                num_locations = 2
                for i in range(num_locations):
                    location_data = text_generator.generate_location(
                        universe_description=game.universe_description,
                        location_number=i
                    )
                    
                    Location.objects.create(
                        game=game,
                        name=location_data['name'],
                        location_type=location_data.get('type', 'CITY').upper().replace(' ', '_'),
                        description=location_data['description'],
                        order=i
                    )
                
                # Générer une image de couverture
                try:
                    cover_image_bytes = image_generator.generate_game_cover(
                        game_title=game.title,
                        genre=game.get_genre_display(),
                        theme=game.get_theme_display()
                    )
                    if cover_image_bytes:
                        game.main_image.save(
                            f"{game.slug}_cover.png",
                            image_generator.save_image_to_model(cover_image_bytes, f"{game.slug}_cover.png"),
                            save=True
                        )
                except Exception as e:
                    print(f"Erreur génération image couverture: {e}")
                
                # Enregistrer dans l'historique
                GenerationHistory.objects.create(
                    user=request.user,
                    game=game,
                    generation_type='FULL_GAME',
                    success=True
                )
                
                # Incrémenter le compteur de l'utilisateur
                if hasattr(request.user, 'profile'):
                    request.user.profile.increment_generations()
                
                messages.success(request, f'Le jeu "{game.title}" a été créé avec succès!')
                return redirect('games:game_detail', slug=game.slug)
                
            except Exception as e:
                messages.error(request, f'Erreur lors de la génération du jeu: {str(e)}')
                if 'game' in locals() and game.pk:
                    game.delete()
        else:
            messages.error(request, 'Erreur dans le formulaire. Veuillez corriger les erreurs.')
    else:
        form = GameCreationForm()
    
    return render(request, 'games/game_create.html', {'form': form})


@login_required
def game_create_random_view(request):
    """
    Vue de création d'un jeu aléatoire (exploration libre)
    """
    try:
        text_generator = AITextGenerator()
        concept = text_generator.generate_random_concept()
        
        # Pré-remplir le formulaire avec le concept aléatoire
        initial_data = {
            'title': f"Jeu Aléatoire {Game.objects.count() + 1}",
            'genre': concept['genre'],
            'theme': concept['theme'],
            'keywords': ', '.join(concept['keywords']),
            'references': concept['references']
        }
        
        form = GameCreationForm(initial=initial_data)
        
        messages.info(request, 'Concept aléatoire généré! Vous pouvez le modifier avant de créer le jeu.')
        
        return render(request, 'games/game_create.html', {
            'form': form,
            'is_random': True
        })
        
    except Exception as e:
        messages.error(request, f'Erreur lors de la génération du concept: {str(e)}')
        return redirect('games:game_create')


def game_detail_view(request, slug):
    """
    Vue de détail d'un jeu
    """
    game = get_object_or_404(Game, slug=slug)
    
    # Vérifier les permissions
    if not game.is_public and game.creator != request.user:
        messages.error(request, 'Ce jeu est privé.')
        return redirect('games:home')
    
    # Incrémenter le compteur de vues
    game.increment_views()
    
    # Vérifier si l'utilisateur a mis ce jeu en favori
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, game=game).exists()
    
    # Récupérer les personnages et lieux
    characters = game.characters.all()
    locations = game.locations.all()
    
    context = {
        'game': game,
        'characters': characters,
        'locations': locations,
        'is_favorited': is_favorited,
        'favorites_count': game.favorited_by.count(),
    }
    
    return render(request, 'games/game_detail.html', context)


@login_required
def game_update_view(request, slug):
    """
    Vue de mise à jour d'un jeu
    """
    game = get_object_or_404(Game, slug=slug, creator=request.user)
    
    if request.method == 'POST':
        form = GameUpdateForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le jeu a été mis à jour avec succès!')
            return redirect('games:game_detail', slug=game.slug)
    else:
        form = GameUpdateForm(instance=game)
    
    return render(request, 'games/game_update.html', {
        'form': form,
        'game': game
    })


@login_required
def game_delete_view(request, slug):
    """
    Vue de suppression d'un jeu
    """
    game = get_object_or_404(Game, slug=slug, creator=request.user)
    
    if request.method == 'POST':
        game_title = game.title
        game.delete()
        messages.success(request, f'Le jeu "{game_title}" a été supprimé.')
        return redirect('games:dashboard')
    
    return render(request, 'games/game_delete.html', {'game': game})


@login_required
def favorites_view(request):
    """
    Vue de la page des favoris
    """
    favorites = Favorite.objects.filter(user=request.user).select_related('game', 'game__creator')
    
    # Pagination
    paginator = Paginator(favorites, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_favorites': favorites.count(),
    }
    
    return render(request, 'games/favorites.html', context)


@login_required
def toggle_favorite_view(request, slug):
    """
    Vue AJAX pour ajouter/retirer un jeu des favoris
    """
    if request.method == 'POST':
        game = get_object_or_404(Game, slug=slug)
        
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            game=game
        )
        
        if not created:
            # Le favori existe déjà, on le supprime
            favorite.delete()
            is_favorited = False
            message = 'Retiré des favoris'
        else:
            is_favorited = True
            message = 'Ajouté aux favoris'
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'is_favorited': is_favorited,
                'favorites_count': game.favorited_by.count(),
                'message': message
            })
        else:
            messages.success(request, message)
            return redirect('games:game_detail', slug=slug)
    
    return redirect('games:home')