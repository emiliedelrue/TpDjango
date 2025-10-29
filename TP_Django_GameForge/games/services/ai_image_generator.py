import os
import requests
from typing import Optional
from django.conf import settings
from django.core.files.base import ContentFile
import io
from PIL import Image


class AIImageGenerator:
    """
    Service de génération d'images via l'API Hugging Face (Stable Diffusion)
    """
    
    def __init__(self):
        self.api_key = getattr(settings, 'HUGGINGFACE_API_KEY', os.getenv('HUGGINGFACE_API_KEY'))
        self.api_url = "https://api-inference.huggingface.co/models/"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # Modèle Stable Diffusion
        self.image_model = "stabilityai/stable-diffusion-2-1"
        # Alternatives : "runwayml/stable-diffusion-v1-5" ou "CompVis/stable-diffusion-v1-4"
    
    def generate_image(self, prompt: str, negative_prompt: str = "") -> Optional[bytes]:
        """
        Génère une image à partir d'un prompt
        """
        try:
            payload = {
                "inputs": prompt,
            }
            
            if negative_prompt:
                payload["negative_prompt"] = negative_prompt
            
            response = requests.post(
                f"{self.api_url}{self.image_model}",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.content
            else:
                print(f"Erreur API image: {response.status_code} - {response.text}")
                return self._create_placeholder_image()
                
        except Exception as e:
            print(f"Erreur lors de la génération d'image: {e}")
            return self._create_placeholder_image()
    
    def _create_placeholder_image(self, width: int = 512, height: int = 512) -> bytes:
        """
        Crée une image placeholder en cas d'erreur
        """
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Créer une image avec un fond dégradé
            img = Image.new('RGB', (width, height), color=(30, 30, 50))
            draw = ImageDraw.Draw(img)
            
            # Dessiner un motif
            for i in range(0, width, 50):
                draw.line([(i, 0), (i, height)], fill=(50, 50, 70), width=1)
            for i in range(0, height, 50):
                draw.line([(0, i), (width, i)], fill=(50, 50, 70), width=1)
            
            # Ajouter du texte
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            text = "Image de\nconception"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((width - text_width) / 2, (height - text_height) / 2)
            draw.text(position, text, fill=(200, 200, 220), font=font)
            
            # Convertir en bytes
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            return buffer.getvalue()
            
        except Exception as e:
            print(f"Erreur création placeholder: {e}")
            return b''
    
    def generate_character_image(self, character_name: str, character_description: str, 
                                 art_style: str = "concept art") -> Optional[bytes]:
        """
        Génère une image de personnage
        """
        prompt = f"{art_style}, {character_name}, {character_description}, highly detailed, digital painting, artstation, concept art, sharp focus, illustration"
        
        negative_prompt = "ugly, deformed, noisy, blurry, low contrast, realistic, photographic"
        
        return self.generate_image(prompt, negative_prompt)
    
    def generate_environment_image(self, location_name: str, location_description: str,
                                   art_style: str = "concept art") -> Optional[bytes]:
        """
        Génère une image d'environnement
        """
        prompt = f"{art_style}, {location_name}, {location_description}, landscape, highly detailed, matte painting, artstation, concept art, sharp focus"
        
        negative_prompt = "ugly, deformed, noisy, blurry, low contrast, characters, people"
        
        return self.generate_image(prompt, negative_prompt)
    
    def generate_game_cover(self, game_title: str, genre: str, theme: str) -> Optional[bytes]:
        """
        Génère une image de couverture pour le jeu
        """
        prompt = f"video game cover art, {game_title}, {genre} game, {theme} theme, professional game cover, highly detailed, digital art, trending on artstation"
        
        negative_prompt = "text, watermark, signature, ugly, deformed, noisy, blurry"
        
        return self.generate_image(prompt, negative_prompt)
    
    def save_image_to_model(self, image_bytes: bytes, filename: str) -> ContentFile:
        """
        Convertit les bytes en ContentFile pour Django
        """
        if image_bytes:
            return ContentFile(image_bytes, name=filename)
        return None
    
    def resize_image(self, image_bytes: bytes, max_width: int = 800, max_height: int = 800) -> bytes:
        """
        Redimensionne une image
        """
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            buffer = io.BytesIO()
            img.save(buffer, format=img.format or 'PNG')
            return buffer.getvalue()
        except Exception as e:
            print(f"Erreur redimensionnement: {e}")
            return image_bytes