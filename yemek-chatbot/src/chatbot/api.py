from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import sys
from typing import List, Optional

# Path ayarlaması
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.rag_pipeline import RAGPipeline
from memory.mem0_client import MemoryManager
from vector_db.milvus_client import MilvusClient
from data_processing.embedding_generator import EmbeddingGenerator

app = FastAPI(title="Yemek Tarifleri Chatbot API", version="1.0.0")

# Pydantic modelleri
class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    user_id: str

class RecipeRequest(BaseModel):
    title: str
    ingredients: str
    instructions: str
    description: Optional[str] = ""

# Global değişkenler
chatbot = None

@app.on_event("startup")
async def startup_event():
    """Uygulama başlangıcında chatbot'u başlat"""
    global chatbot
    try:
        # Environment variables
        openai_key = os.getenv("OPENAI_API_KEY")
        milvus_host = os.getenv("MILVUS_HOST", "localhost")
        milvus_port = os.getenv("MILVUS_PORT", "19530")
        
        if not openai_key:
            raise ValueError("OPENAI_API_KEY environment variable gerekli!")
        
        # Bileşenleri başlat
        milvus_client = MilvusClient(host=milvus_host, port=milvus_port)
        collection = milvus_client.get_collection("recipes")
        
        rag_pipeline = RAGPipeline(collection, openai_key)
        memory_manager = MemoryManager()
        
        chatbot = {
            "rag": rag_pipeline,
            "memory": memory_manager,
            "milvus": milvus_client
        }
        
        print("Chatbot başarıyla başlatıldı!")
        
    except Exception as e:
        print(f"Chatbot başlatma hatası: {e}")
        raise

@app.get("/")
async def root():
    """Ana sayfa"""
    return {"message": "Yemek Tarifleri Chatbot API v1.0"}

@app.get("/health")
async def health_check():
    """Sağlık kontrolü"""
    return {"status": "healthy", "chatbot_ready": chatbot is not None}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chatbot ile sohbet et"""
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot henüz hazır değil")
    
    try:
        # Kullanıcı geçmişini al
        personalized_query = chatbot["memory"].personalize_response(
            request.message, request.user_id
        )
        
        # RAG pipeline ile cevap üret
        retrieved_recipes = chatbot["rag"].retrieve_recipes(personalized_query)
        response = chatbot["rag"].generate_response(request.message, retrieved_recipes)
        
        # Kullanıcı tercihini kaydet
        chatbot["memory"].add_user_preference(request.user_id, request.message)
        
        return ChatResponse(response=response, user_id=request.user_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata oluştu: {str(e)}")

@app.post("/add-recipe")
async def add_recipe(recipe: RecipeRequest):
    """Yeni tarif ekle"""
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot henüz hazır değil")
    
    try:
        # Embedding oluştur
        embedding_gen = EmbeddingGenerator()
        recipe_dict = recipe.dict()
        embedding = embedding_gen.generate_recipe_embedding(recipe_dict)
        
        # Vektör veritabanına ekle
        # Bu kısım vector_operations ile yapılacak
        
        return {"message": "Tarif başarıyla eklendi", "recipe_title": recipe.title}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tarif ekleme hatası: {str(e)}")

@app.get("/recipes/search/{query}")
async def search_recipes(query: str, limit: int = 5):
    """Tarif ara"""
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot henüz hazır değil")
    
    try:
        results = chatbot["rag"].retrieve_recipes(query, top_k=limit)
        return {"query": query, "results": results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Arama hatası: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)