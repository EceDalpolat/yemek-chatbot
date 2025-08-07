from sentence_transformers import SentenceTransformer
import numpy as np
import torch

class EmbeddingGenerator:
    def __init__(self, model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        """Türkçe metinler için uygun model"""
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
    
    def generate_recipe_embedding(self, recipe_dict):
        """Tarif için embedding oluştur"""
        # Tarif metnini birleştir
        combined_text = ""
        
        if 'title' in recipe_dict:
            combined_text += f"Başlık: {recipe_dict['title']} "
        
        if 'description' in recipe_dict:
            combined_text += f"Açıklama: {recipe_dict['description']} "
        
        if 'ingredients' in recipe_dict:
            if isinstance(recipe_dict['ingredients'], list):
                ingredients_text = " ".join(recipe_dict['ingredients'])
            else:
                ingredients_text = recipe_dict['ingredients']
            combined_text += f"Malzemeler: {ingredients_text} "
        
        if 'instructions' in recipe_dict:
            combined_text += f"Yapılışı: {recipe_dict['instructions']}"
        
        # Embedding oluştur
        embedding = self.model.encode(combined_text, convert_to_tensor=True)
        return embedding.cpu().numpy()
    
    def generate_query_embedding(self, query):
        """Sorgu için embedding oluştur"""
        embedding = self.model.encode(query, convert_to_tensor=True)
        return embedding.cpu().numpy()
    
    def batch_generate_embeddings(self, recipe_list):
        """Toplu embedding oluşturma"""
        embeddings = []
        for recipe in recipe_list:
            embedding = self.generate_recipe_embedding(recipe)
            embeddings.append(embedding)
        return np.array(embeddings)