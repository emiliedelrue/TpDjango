import os
import requests
from typing import Dict, List
from django.conf import settings


class AITextGenerator:
    """
    Service de génération de texte via l'API Hugging Face
    """
    
    def __init__(self):
        self.api_key = getattr(settings, 'HUGGINGFACE_API_KEY', os.getenv('HUGGINGFACE_API_KEY'))
        self.api_url = "https://api-inference.huggingface.co/models/"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # Modèles recommandés
        self.text_model = "mistralai/Mistral-7B-Instruct-v0.2"
        # Alternative si le modèle ci-dessus ne fonctionne pas : "gpt2" ou "facebook/opt-1.3b"
    
    def _make_request(self, model_name: str, prompt: str, max_length: int = 500) -> str:
        """
        Fait une requête à l'API Hugging Face
        """
        try:
            response = requests.post(
                f"{self.api_url}{model_name}",
                headers=self.headers,
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": max_length,
                        "temperature": 0.8,
                        "top_p": 0.95,
                        "do_sample": True,
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '').replace(prompt, '').strip()
                return str(result)
            else:
                print(f"Erreur API: {response.status_code} - {response.text}")
                return self._get_fallback_text(prompt)
                
        except Exception as e:
            print(f"Erreur lors de la génération: {e}")
            return self._get_fallback_text(prompt)
    
    def _get_fallback_text(self, prompt: str) -> str:
        """
        Texte de secours si l'API ne répond pas
        """
        return "Contenu généré automatiquement. [En mode démo - API non disponible]"
    
    def generate_universe(self, genre: str, theme: str, keywords: List[str], references: str = "") -> Dict[str, str]:
        """
        Génère la description de l'univers du jeu
        """
        keywords_str = ", ".join(keywords) if keywords else "aventure, mystère"
        
        prompt = f"""Crée un univers de jeu vidéo {genre} avec une ambiance {theme}.
Mots-clés: {keywords_str}
Références: {references}

Décris cet univers en détail (contexte, époque, règles du monde, particularités):"""

        description = self._make_request(self.text_model, prompt, max_length=400)
        
        return {
            'type': genre,
            'ambiance': theme,
            'description': description,
            'keywords': keywords_str
        }
    
    def generate_story(self, universe_description: str, genre: str) -> Dict[str, str]:
        """
        Génère une histoire en 3 actes avec un retournement narratif
        """
        # Acte 1
        prompt_act1 = f"""Dans un jeu {genre}, voici l'univers: {universe_description[:200]}

Écris l'Acte 1 de l'histoire (introduction, présentation du héros, déclencheur de l'aventure):"""
        act1 = self._make_request(self.text_model, prompt_act1, max_length=300)
        
        # Acte 2
        prompt_act2 = f"""Suite de l'histoire. Acte 1: {act1[:150]}

Écris l'Acte 2 (quête principale, obstacles, développement des enjeux):"""
        act2 = self._make_request(self.text_model, prompt_act2, max_length=300)
        
        # Acte 3
        prompt_act3 = f"""Fin de l'histoire. Contexte: {act2[:150]}

Écris l'Acte 3 avec un retournement narratif surprenant et une conclusion épique:"""
        act3 = self._make_request(self.text_model, prompt_act3, max_length=300)
        
        return {
            'act1': act1 or "Le héros découvre un monde en danger et reçoit un appel à l'aventure.",
            'act2': act2 or "Le héros affronte de nombreux défis et découvre la véritable nature de sa quête.",
            'act3': act3 or "Un retournement majeur révèle la vérité, le héros accomplit son destin."
        }
    
    def generate_character(self, universe_description: str, role: str, character_number: int) -> Dict[str, str]:
        """
        Génère un personnage avec ses caractéristiques
        """
        roles_list = ["protagoniste", "antagoniste", "mentor", "allié"]
        actual_role = role if role else roles_list[min(character_number, len(roles_list) - 1)]
        
        prompt = f"""Univers du jeu: {universe_description[:200]}

Crée un personnage de type {actual_role} pour ce jeu.
Donne: son nom, sa classe/archétype, son rôle dans l'histoire, son background, et son style de gameplay:"""

        character_text = self._make_request(self.text_model, prompt, max_length=350)
        
        # Parser le texte (simpliste)
        lines = character_text.split('\n')
        
        return {
            'name': self._extract_value(character_text, 'nom') or f"Personnage {character_number + 1}",
            'character_class': self._extract_value(character_text, 'classe') or 'Guerrier',
            'role': actual_role,
            'background': character_text[:200] or "Un mystérieux personnage avec un passé trouble.",
            'gameplay_description': self._extract_value(character_text, 'gameplay') or "Combat rapproché et compétences spéciales."
        }
    
    def generate_location(self, universe_description: str, location_number: int) -> Dict[str, str]:
        """
        Génère un lieu emblématique
        """
        location_types = ["ville principale", "donjon dangereux", "sanctuaire mystique", "ruines anciennes"]
        location_type = location_types[min(location_number, len(location_types) - 1)]
        
        prompt = f"""Univers: {universe_description[:200]}

Décris un lieu emblématique de type "{location_type}".
Inclus: nom du lieu, description visuelle détaillée, atmosphère, importance dans le jeu:"""

        location_text = self._make_request(self.text_model, prompt, max_length=300)
        
        return {
            'name': self._extract_value(location_text, 'nom') or f"Lieu {location_number + 1}",
            'description': location_text or "Un lieu mystérieux rempli de secrets et de dangers.",
            'type': location_type
        }
    
    def _extract_value(self, text: str, key: str) -> str:
        """
        Extrait une valeur d'un texte généré (méthode simple)
        """
        key_lower = key.lower()
        lines = text.split('\n')
        
        for line in lines:
            if key_lower in line.lower():
                parts = line.split(':')
                if len(parts) > 1:
                    return parts[1].strip()
        
        return ""
    
    def generate_random_concept(self) -> Dict[str, any]:
        """
        Génère un concept de jeu complètement aléatoire
        """
        import random
        
        genres = ["RPG", "FPS", "Metroidvania", "Visual Novel", "Puzzle", "Action-Adventure"]
        themes = ["Post-apocalyptique", "Cyberpunk", "Dark Fantasy", "Onirique", "Steampunk", "Spatial"]
        keywords_pool = [
            "boucle temporelle", "vengeance", "IA rebelle", "prophétie", "corruption",
            "révolution", "mémoire perdue", "réalité virtuelle", "portails dimensionnels"
        ]
        
        genre = random.choice(genres)
        theme = random.choice(themes)
        keywords = random.sample(keywords_pool, 3)
        
        return {
            'genre': genre,
            'theme': theme,
            'keywords': keywords,
            'references': "Surprise moi !"
        }