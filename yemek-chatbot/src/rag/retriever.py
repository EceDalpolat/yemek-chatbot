from sentence_transformers import SentenceTransformer
import numpy as np

class Retriever:
    def __init__(self, vector_operations, embedding_generator):
        self.vector_ops = vector_operations
        self.embedding_gen = embedding_generator
    
    def retrieve(self, query, top_k=3):
        """Sorguya göre en benzer tarifleri getir"""
        try:
            # Sorgu embedding'i oluştur
            query_embedding = self.embedding_gen.generate_query_embedding(query)
            
            # Benzer tarifleri ara
            results = self.vector_ops.search_similar_recipes(query_embedding, top_k)
            
            # Sonuçları formatla
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'recipe_id': result.entity.get('recipe_id'),
                    'title': result.entity.get('title'),
                    'ingredients': result.entity.get('ingredients'),
                    'instructions': result.entity.get('instructions'),
                    'similarity_score': result.distance
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"Retrieval hatası: {e}")
            return []
    
    def retrieve_by_ingredients(self, ingredients_list, top_k=3):
        """Malzeme listesine göre tarif öner"""
        # Malzeme listesini query'ye çevir
        query = "Bu malzemelerle yapılabilecek yemekler: " + ", ".join(ingredients_list)
        return self.retrieve(query, top_k)
    
    def retrieve_by_cuisine_type(self, cuisine_type, top_k=5):
        """Mutfak türüne göre tarif öner"""
        query = f"{cuisine_type} mutfağı yemekleri"
        return self.retrieve(query, top_k)