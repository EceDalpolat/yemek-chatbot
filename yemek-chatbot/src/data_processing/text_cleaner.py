import re
import string

class TextCleaner:
    def __init__(self):
        self.turkish_chars = "çğıöşüÇĞIİÖŞÜ"
    
    def clean_text(self, text):
        """Metni temizle ve normalize et"""
        if not text:
            return ""
        
        # HTML taglerini kaldır
        text = re.sub(r'<[^>]+>', '', text)
        
        # Fazla boşlukları temizle
        text = re.sub(r'\s+', ' ', text)
        
        # Başındaki ve sonundaki boşlukları kaldır
        text = text.strip()
        
        return text
    
    def normalize_recipe_text(self, recipe_dict):
        """Tarif metnini normalize et"""
        cleaned_recipe = {}
        
        for key, value in recipe_dict.items():
            if isinstance(value, str):
                cleaned_recipe[key] = self.clean_text(value)
            else:
                cleaned_recipe[key] = value
        
        return cleaned_recipe
    
    def extract_ingredients(self, text):
        """Malzeme listesini çıkar"""
        # Basit malzeme çıkarma logic'i
        lines = text.split('\n')
        ingredients = []
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or 
                        re.match(r'^\d+\.', line)):
                ingredients.append(self.clean_text(line))
        
        return ingredients