import pandas as pd
import json
from typing import List, Dict

class FineTuningDataPrep:
    def __init__(self):
        self.training_data = []
    
    def prepare_conversation_data(self, recipes_data: List[Dict]):
        """Tarif verilerini fine-tuning için hazırla"""
        
        for recipe in recipes_data:
            # Soru-cevap çiftleri oluştur
            qa_pairs = self._generate_qa_pairs(recipe)
            self.training_data.extend(qa_pairs)
    
    def _generate_qa_pairs(self, recipe: Dict):
        """Bir tarif için soru-cevap çiftleri oluştur"""
        qa_pairs = []
        
        title = recipe.get('title', '')
        ingredients = recipe.get('ingredients', '')
        instructions = recipe.get('instructions', '')
        
        # Farklı soru türleri
        questions = [
            f"{title} nasıl yapılır?",
            f"{title} tarifi nedir?",
            f"{title} için hangi malzemeler gerekli?",
            f"{title} yapımı nasıl?",
        ]
        
        for question in questions:
            answer = f"""
{title} tarifi:

Malzemeler:
{ingredients}

Yapılışı:
{instructions}
"""
            
            qa_pairs.append({
                "messages": [
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": answer}
                ]
            })
        
        return qa_pairs
    
    def save_training_data(self, filename: str):
        """Eğitim verisini dosyaya kaydet"""
        with open(filename, 'w', encoding='utf-8') as f:
            for item in self.training_data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    def create_validation_set(self, validation_ratio: float = 0.2):
        """Doğrulama seti oluştur"""
        total_size = len(self.training_data)
        val_size = int(total_size * validation_ratio)
        
        validation_data = self.training_data[:val_size]
        training_data = self.training_data[val_size:]
        
        return training_data, validation_data