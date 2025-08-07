from sentence_transformers import SentenceTransformer
import openai
from pymilvus import Collection

class RAGPipeline:
    def __init__(self, milvus_collection, openai_key):
        self.collection = milvus_collection
        self.encoder = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        openai.api_key = openai_key
    

    def retrieve_recipes(self, query, top_k=3):
        # Sorguyu vektöre çevir
        query_embedding = self.encoder.encode(query).tolist()
        
        # Benzer tarifleri bul
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        results = self.collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            output_fields=["title", "ingredients", "instructions"]
        )
        
        return results[0]
    
    def generate_response(self, query, retrieved_recipes):
        # Context oluştur
        context = "İlgili yemek tarifleri:\n"
        for recipe in retrieved_recipes:
            context += f"Tarif: {recipe.entity.get('title')}\n"
            context += f"Malzemeler: {recipe.entity.get('ingredients')}\n"
            context += f"Yapılışı: {recipe.entity.get('instructions')}\n\n"
        
        # GPT'ye gönder
        prompt = f"""Sen bir yemek uzmanısın. Aşağıdaki tarif bilgilerini kullanarak kullanıcının sorusunu cevapla.

{context}

Kullanıcı sorusu: {query}

Cevap:"""
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content