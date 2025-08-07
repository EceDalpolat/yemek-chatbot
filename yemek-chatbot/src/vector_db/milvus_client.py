from pymilvus import Collection, FieldSchema, CollectionSchema, DataType, connections
import logging

class MilvusClient:
    def __init__(self, host="localhost", port="19530"):
        try:
            connections.connect("default", host=host, port=port)
            logging.info(f"Milvus bağlantısı başarılı: {host}:{port}")
        except Exception as e:
            logging.error(f"Milvus bağlantı hatası: {e}")
            raise
    
    def create_recipe_collection(self):
        # Tarif koleksiyonu oluşturma
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="recipe_id", dtype=DataType.VARCHAR, max_length=100),
            FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=500),
            FieldSchema(name="ingredients", dtype=DataType.VARCHAR, max_length=2000),
            FieldSchema(name="instructions", dtype=DataType.VARCHAR, max_length=5000),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384)
        ]
        schema = CollectionSchema(fields, "Yemek tarifleri koleksiyonu")
        collection = Collection("recipes", schema)
        return collection
    
    def get_collection(self, collection_name="recipes"):
        """Koleksiyon al veya oluştur"""
        try:
            collection = Collection(collection_name)
            return collection
        except Exception:
            # Koleksiyon yoksa oluştur
            return self.create_recipe_collection()