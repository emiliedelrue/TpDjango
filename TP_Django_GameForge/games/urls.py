from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    # Page d'accueil
    path('', views.home_view, name='home'),
    
    # Tableau de bord
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Création de jeux
    path('create/', views.game_create_view, name='game_create'),
    path('create/random/', views.game_create_random_view, name='game_create_random'),
    
    # Détail, modification, suppression
    path('game/<slug:slug>/', views.game_detail_view, name='game_detail'),
    path('game/<slug:slug>/update/', views.game_update_view, name='game_update'),
    path('game/<slug:slug>/delete/', views.game_delete_view, name='game_delete'),
    
    # Favoris
    path('favorites/', views.favorites_view, name='favorites'),
    path('game/<slug:slug>/favorite/', views.toggle_favorite_view, name='toggle_favorite'),
]