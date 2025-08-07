from pymilvus import Collection, utility
import numpy as np

class VectorOperations:
    def __init__(self, collection):
        self.collection = collection
    
    def insert_recipes(self, recipes_data):
        """Tarifleri vektör veritabanına ekle"""
        try:
            # Veriyi hazırla
            data = [
                recipes_data.get('recipe_ids', []),
                recipes_data.get('titles', []),
                recipes_data.get('ingredients', []),
                recipes_data.get('instructions', []),
                recipes_data.get('embeddings', [])
            ]
            
            # Veri ekleme
            mr = self.collection.insert(data)
            self.collection.flush()
            
            return mr.primary_keys
            
        except Exception as e:
            print(f"Veri ekleme hatası: {e}")
            return None
    
    def search_similar_recipes(self, query_embedding, top_k=5):
        """Benzer tarifleri ara"""
        try:
            search_params = {
                "metric_type": "L2",
                "params": {"nprobe": 10}
            }
            
            results = self.collection.search(
                data=[query_embedding.tolist()],
                anns_field="embedding",
                param=search_params,
                limit=top_k,
                output_fields=["recipe_id", "title", "ingredients", "instructions"]
            )
            
            return results[0] if results else []
            
        except Exception as e:
            print(f"Arama hatası: {e}")
            return []
    
    def create_index(self):
        """Koleksiyon için index oluştur"""
        try:
            index_params = {
                "metric_type": "L2",
                "index_type": "IVF_FLAT",
                "params": {"nlist": 128}
            }
            
            self.collection.create_index("embedding", index_params)
            return True
            
        except Exception as e:
            print(f"Index oluşturma hatası: {e}")
            return False
    
    def load_collection(self):
        """Koleksiyonu belleğe yükle"""
        try:
            self.collection.load()
            return True
        except Exception as e:
            print(f"Koleksiyon yükleme hatası: {e}")
            return False
    
    def get_collection_stats(self):
        """Koleksiyon istatistikleri"""
        try:
            stats = utility.get_query_segment_info(self.collection.name)
            return stats
        except Exception as e:
            print(f"İstatistik alma hatası: {e}")
            return None