import openai

class Generator:
    def __init__(self, openai_api_key):
        openai.api_key = openai_api_key
    
    def generate_response(self, query, retrieved_recipes, user_context=""):
        """Alınan tariflere göre yanıt oluştur"""
        
        # Context oluştur
        context = self._build_context(retrieved_recipes)
        
        # Prompt hazırla
        prompt = self._create_prompt(query, context, user_context)
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sen bir yemek uzmanısın ve kullanıcılara yemek tarifleri konusunda yardımcı oluyorsun. Türkçe yanıt ver."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Yanıt oluşturulurken hata oluştu: {str(e)}"
    
    def _build_context(self, recipes):
        """Tarif listesinden context oluştur"""
        if not recipes:
            return "İlgili tarif bulunamadı."
        
        context = "İlgili yemek tarifleri:\n\n"
        
        for i, recipe in enumerate(recipes, 1):
            context += f"{i}. {recipe.get('title', 'Başlık yok')}\n"
            
            if recipe.get('ingredients'):
                context += f"   Malzemeler: {recipe['ingredients']}\n"
            
            if recipe.get('instructions'):
                instructions = recipe['instructions'][:200] + "..." if len(recipe['instructions']) > 200 else recipe['instructions']
                context += f"   Yapılışı: {instructions}\n"
            
            context += "\n"
        
        return context
    
    def _create_prompt(self, query, context, user_context):
        """Prompt oluştur"""
        prompt = f"""
Aşağıdaki tarif bilgilerini kullanarak kullanıcının sorusunu cevapla:

{context}

{user_context}

Kullanıcı sorusu: {query}

Lütfen:
1. Soruyla ilgili en uygun tarifleri öner
2. Malzeme listelerini net bir şekilde belirt
3. Yapılış adımlarını açık bir şekilde anlat
4. Varsa ipuçları ve püf noktaları paylaş
5. Türkçe ve samimi bir dille yanıtla

Yanıt:"""
        
        return prompt
    
    def generate_recipe_summary(self, recipe):
        """Tek tarif için özet oluştur"""
        try:
            prompt = f"""
Aşağıdaki tarifi özetle:

Başlık: {recipe.get('title', '')}
Malzemeler: {recipe.get('ingredients', '')}
Yapılışı: {recipe.get('instructions', '')}

Kısa ve öz bir özet hazırla.
"""
            
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.5
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Özet oluşturulamadı: {str(e)}"