from mem0 import Memory
import os

class MemoryManager:
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = os.getenv("MEM0_API_KEY")
        self.memory = Memory(api_key=api_key)
    
    def add_user_preference(self,user_id,preference):
        """Kullanıcı tercihlerini kaydet"""
        self.memory.add(
            messages=[{"role": "user", "content": preference}],
            user_id=user_id
        )
    
    def get_user_context(self, user_id):
        """Kullanıcı geçmişini getir"""
        memories = self.memory.get_all(user_id=user_id)
        return memories
    
    def personalize_response(self, query, user_id):
        """Kişiselleştirilmiş yanıt için context ekle"""
        user_memories = self.get_user_context(user_id)
        context = ""
        if user_memories:
            context = "Kullanıcı tercihleri: " + "; ".join([m['memory'] for m in user_memories])
        
        return f"{context}\nSoru: {query}"



"""
from mem0 import MemoryClient

client = MemoryClient(api_key="m0-3FPdJaGCFz7WPBiotn9X1qZpiOkpx2O7PllMn6D8")

"""