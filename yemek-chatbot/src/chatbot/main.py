import streamlit as st
import os
from dotenv import load_dotenv
import openai

# Environment variables yükle
load_dotenv()

def test_openai_connection():
    """OpenAI/OpenRouter bağlantısını test et"""
    try:
        # OpenRouter kullanıyorsanız
        if os.getenv("USE_OPENROUTER") == "true":
            from openai import OpenAI
            client = OpenAI(
                api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1",
            )
            model = "openai/gpt-3.5-turbo"
        else:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            model = "gpt-3.5-turbo"
        
        # Test mesajı
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Merhaba, bu bir test mesajıdır."}],
            max_tokens=50
        )
        return True, response.choices[0].message.content
    except Exception as e:
        return False, str(e)

def is_food_related(query):
    """Sorunun yemek ile ilgili olup olmadığını kontrol et"""
    food_keywords = [
        # Yemek türleri
        'tarif', 'yemek', 'pişirmek', 'yapmak', 'çorba', 'et', 'tavuk', 'balık', 'sebze',
        'makarna', 'pilav', 'börek', 'pasta', 'kek', 'kurabiye', 'tatlı', 'salata',
        'kahvaltı', 'öğle', 'akşam', 'yemeği', 'içecek', 'çay', 'kahve', 'meze',
        
        # Malzemeler
        'malzeme', 'içindekiler', 'un', 'yumurta', 'süt', 'tereyağı', 'peynir',
        'domates', 'soğan', 'sarımsak', 'biber', 'tuz', 'karabiber', 'baharat',
        'zeytinyağı', 'limon', 'patates', 'havuç', 'bulgur', 'pirinç',
        
        # Pişirme yöntemleri
        'fırın', 'tavada', 'haşlama', 'kavurma', 'kızartma', 'sotele', 'marine',
        'pişirme', 'hazırlama', 'karıştır', 'ekle', 'dök', 'beklet',
        
        # Mutfak araçları
        'tencere', 'tava', 'fırın', 'blender', 'mikser', 'spatula',
        
        # Türk mutfağı
        'menemen', 'lahmacun', 'döner', 'köfte', 'mantı', 'dolma', 'sarma',
        'baklava', 'künefe', 'lokum', 'ayran', 'çorba', 'pide', 'kebap',
        
        # Diyet ve beslenme
        'gluten', 'glutensiz', 'çölyak', 'laktoz', 'laktozsuz', 'vegan', 'vejetaryen',
        'diyet', 'beslenme', 'kalori', 'sağlıklı', 'organik', 'doğal',
        'intolerans', 'alerjik', 'alerji', 'hassasiyet', 'keto', 'paleo',
        'şekersiz', 'tuzsuz', 'yağsız', 'protein', 'karbonhidrat', 'vitamin',
        'mineral', 'lif', 'detoks', 'fit', 'zayıflama', 'kilo', 'rejim',
        'diyabetik', 'şeker hastalığı', 'tansiyon', 'kolesterol', 'kalp dostu',
        'prebiyotik', 'probiyotik', 'antioksidan', 'süt ürünü', 'et yemem',
        'tavuk yemem', 'balık yemem', 'yumurta yemem', 'fındık alerjim',
        'yer fıstığı', 'susam', 'bezelye', 'soya', 'buğday', 'arpa', 'çavdar'
    ]
    
    query_lower = query.lower()
    
    # Malzeme bazlı sorular
    ingredient_phrases = ['elimde', 'evde var', 'malzemelerim', 'ile ne yapabilirim']
    if any(phrase in query_lower for phrase in ingredient_phrases):
        return True
    
    # Yemek kelimeleri kontrolü
    if any(keyword in query_lower for keyword in food_keywords):
        return True
    
    # Soru kalıpları
    food_patterns = ['nasıl yapılır', 'tarifi nedir', 'ne pişirebilirim', 'yemek öner']
    if any(pattern in query_lower for pattern in food_patterns):
        return True
    
    return False

def simple_recipe_response(query, selected_language="Türkçe"):
    """Sadece yemek konularında cevap veren fonksiyon"""
    
    # Önce sorunun yemek ile ilgili olup olmadığını kontrol et
    if not is_food_related(query):
        # Dil tespiti yap
        query_lower = query.lower()
        
        # İngilizce anahtar kelimeler
        english_keywords = [
            'what', 'how', 'can', 'please', 'give', 'tell', 'show', 'help', 'recipe', 'food',
            'cooking', 'make', 'cook', 'ingredients', 'dish', 'meal', 'breakfast', 'lunch', 'dinner',
            'chicken', 'beef', 'fish', 'vegetable', 'pasta', 'rice', 'bread', 'dessert', 'cake',
            'gluten', 'lactose', 'vegan', 'vegetarian', 'diet', 'healthy', 'sugar', 'salt'
        ]
        is_english = any(word in query_lower for word in english_keywords)
        
        # Seçilen dile göre red mesajı ver
        if selected_language == "English":
            return """
🍳 **Sorry, I can only help with cooking and food topics!**

I can help you with:
• 🥘 Recipe suggestions
• 🥗 What to cook with your ingredients
• 👨‍🍳 Cooking techniques
• 🍯 Food recommendations

**Example questions:**
- "Pasta recipe"
- "I have chicken, what can I cook?"
- "Easy dessert recipe"
- "How to make scrambled eggs?"

Please ask a food-related question! 😊
            """
        else:
            return """
🍳 **Üzgünüm, ben sadece yemek konularında yardımcı olabilirim!**

Size şunlarda yardımcı olabilirim:
• 🥘 Yemek tarifleri
• 🥗 Malzemelerle ne yapabileceğiniz
• 👨‍🍳 Pişirme teknikleri
• 🍯 Yemek önerileri

**Örnek sorular:**
- "Makarna tarifi"
- "Elimde tavuk var, ne yapabilirim?"
- "Kolay tatlı tarifi"
- "Menemen nasıl yapılır?"

Lütfen yemek ile ilgili bir soru sorun! 😊
            """
    
    try:
        # OpenRouter kullanıyorsanız
        if os.getenv("USE_OPENROUTER") == "true":
            from openai import OpenAI
            client = OpenAI(
                api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1",
            )
            model = "openai/gpt-3.5-turbo"
        else:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            model = "gpt-3.5-turbo"
        
        # Seçilen dile göre prompt oluştur
        if selected_language == "English":
            prompt = f"""
You are an expert chef and nutrition specialist who ONLY helps with cooking and food topics.

IMPORTANT RULES:
1. Only discuss recipes, ingredients, and cooking techniques
2. You care deeply about special dietary needs (gluten-free, lactose-free, vegan, keto, etc.)
3. Always include in your response: Ingredients, Cooking steps, Tips
4. RESPOND IN ENGLISH ONLY
5. Use warm, friendly English
6. State what dish you're suggesting before giving the recipe

ESPECIALLY PAY ATTENTION TO:
- Gluten intolerance = Give gluten-free recipe (no wheat, barley, rye, regular flour!)
- Lactose intolerance = Give lactose-free recipe (no dairy products!)
- Vegan = No animal products (no meat, dairy, eggs, honey!)
- Vegetarian = No meat but dairy is okay
- Take allergies very seriously

User question: {query}

Your response should be ONLY about food/cooking and consider special dietary needs. RESPOND IN ENGLISH:"""
        else:
            prompt = f"""
Sen uzman bir Türk mutfağı şefi ve beslenme uzmanısın. SADECE yemek ve mutfak konularında yardım ediyorsun.

ÖNEMLI KURALLAR:
1. Sadece yemek tarifleri, malzemeler ve pişirme teknikleri hakkında konuş
2. Özel diyet ihtiyaçlarını (glutensiz, laktozsuz, vegan, keto vb.) çok önemsiyorsun
3. Her cevabında: Malzemeler, Yapılış adımları, İpuçları ver
4. SADECE TÜRKÇE CEVAP VER
5. Türkçe ve samimi bir dille yanıt ver
6. Tarif vermeden önce hangi yemek olduğunu belirt

ÖZELLİKLE DİKKAT ET:
- Gluten intoleransı = Glutensiz tarif ver (buğday, arpa, çavdar, normal un yok!)
- Laktoz intoleransı = Laktozsuz tarif ver (süt ürünü yok!)
- Vegan = Hayvansal ürün yok (et, süt, yumurta, bal yok!)
- Vejetaryen = Et yok ama süt ürünü olabilir
- Alerji durumlarını çok ciddiye al

Kullanıcı sorusu: {query}

Yanıtın sadece yemek konusunda olmalı ve özel diyet ihtiyaçlarını dikkate almalı. TÜRKÇE CEVAP VER:"""
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"You are a chef and nutrition expert who ONLY helps with cooking and food topics. You understand special dietary needs very well. ALWAYS respond in {'ENGLISH' if selected_language == 'English' else 'TURKISH'} regardless of the question language."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Hata oluştu: {str(e)}"

# Streamlit arayüzü
def main():
    st.set_page_config(
        page_title="Cooking Recipes Chatbot / Yemek Tarifleri Chatbot",
        page_icon="🍳",
        layout="wide"
    )
    
    # Dil seçimi - EN ÜST SAĞDA
    with st.container():
        col1, col2, col3 = st.columns([6, 1, 1])
        with col3:
            language = st.selectbox("🌍", ["Türkçe", "English"], index=0, key="main_language")
    
    # Dil bazlı başlık ve açıklamalar
    if language == "English":
        st.title("🍳 Cooking Recipes Assistant")
        st.markdown("### 👨‍🍳 Your personal cooking and recipe expert!")
        st.write("Ask me anything about cooking and recipes!")
        
        # API bağlantı testi
        st.sidebar.header("🔧 System Status")
    else:
        st.title("🍳 Yemek Tarifleri Asistanı")
        st.markdown("### 👨‍🍳 Size özel yemek tarifleri ve pişirme uzmanınız!")
        st.write("Yemek tarifleri hakkında sorularınızı sorabilirsiniz!")
        
        # API bağlantı testi
        st.sidebar.header("🔧 Sistem Durumu")
    
    if language == "English":
        if st.sidebar.button("Test API Connection"):
            with st.spinner("Testing..."):
                success, message = test_openai_connection()
                if success:
                    st.sidebar.success("✅ API connection successful!")
                    st.sidebar.info(f"Test response: {message}")
                else:
                    st.sidebar.error(f"❌ API connection error: {message}")
        
        # Environment variables kontrolü
        st.sidebar.subheader("📋 Configuration")
        openai_key = os.getenv("OPENAI_API_KEY")
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        use_openrouter = os.getenv("USE_OPENROUTER")
        
        if use_openrouter == "true":
            st.sidebar.info("🔄 Using OpenRouter")
            if openrouter_key:
                st.sidebar.success("✅ OpenRouter API key found")
            else:
                st.sidebar.error("❌ OpenRouter API key not found")
        else:
            st.sidebar.info("🤖 Using OpenAI")
            if openai_key:
                st.sidebar.success("✅ OpenAI API key found")
            else:
                st.sidebar.error("❌ OpenAI API key not found")
    else:
        if st.sidebar.button("API Bağlantısını Test Et"):
            with st.spinner("Test ediliyor..."):
                success, message = test_openai_connection()
                if success:
                    st.sidebar.success("✅ API bağlantısı başarılı!")
                    st.sidebar.info(f"Test yanıtı: {message}")
                else:
                    st.sidebar.error(f"❌ API bağlantı hatası: {message}")
        
        # Environment variables kontrolü
        st.sidebar.subheader("📋 Konfigürasyon")
        openai_key = os.getenv("OPENAI_API_KEY")
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        use_openrouter = os.getenv("USE_OPENROUTER")
        
        if use_openrouter == "true":
            st.sidebar.info("🔄 OpenRouter kullanılıyor")
            if openrouter_key:
                st.sidebar.success("✅ OpenRouter API key bulundu")
            else:
                st.sidebar.error("❌ OpenRouter API key bulunamadı")
        else:
            st.sidebar.info("🤖 OpenAI kullanılıyor")
            if openai_key:
                st.sidebar.success("✅ OpenAI API key bulundu")
            else:
                st.sidebar.error("❌ OpenAI API key bulunamadı")
    
    # Ana chat arayüzü
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if language == "English":
            st.subheader("💬 Chat")
        else:
            st.subheader("💬 Sohbet")
        
        # Chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        placeholder_text = "Ask me about cooking and recipes..." if language == "English" else "Yemek hakkında soru sorabilirsiniz..."
        if prompt := st.chat_input(placeholder_text):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get bot response
            with st.chat_message("assistant"):
                spinner_text = "Preparing answer..." if language == "English" else "Cevap hazırlanıyor..."
                with st.spinner(spinner_text):
                    response = simple_recipe_response(prompt, language)
                    st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    with col2:
        if language == "English":
            st.subheader("🎯 Quick Actions")
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        else:
            st.subheader("🎯 Hızlı Aksiyonlar")
            if st.button("🗑️ Sohbeti Temizle", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        
        st.markdown("---")


        
        if language == "English":
            # İngilizce örnek sorular
            st.subheader("💡 Example Food Questions")
            example_questions = [
                "🍝 Easy pasta recipe",
                "🥚 Vegetable omelet recipe", 
                "☕ Quick breakfast ideas",
                "🍪 Chocolate cookie recipe",
                "🍲 Lentil soup recipe"
            ]
            
            st.markdown("**🧅 Ingredient-based questions:**")
            ingredient_questions = [
                "🥩 I have chicken, what can I cook?",
                "🥔 What can I make with potatoes and onions?",
                "🧀 Easy cheese recipe please"
            ]
            
            st.markdown("**🥗 Special diet questions:**")
            diet_questions = [
                "🌾 Gluten-free pasta recipe",
                "🥛 Lactose-free dessert recipe",
                "🌱 Vegan meatball recipe",
                "🥑 Keto breakfast ideas",
                "🍯 Sugar-free cookies"
            ]
        else:
            # Türkçe örnek sorular
            st.subheader("💡 Örnek Yemek Soruları")
            example_questions = [
                "🍝 Kolay makarna tarifi",
                "🥚 Sebzeli omlet yapımı", 
                "☕ Hızlı kahvaltı tarifleri",
                "🍪 Çikolatalı kurabiye",
                "🍲 Mercimek çorbası"
            ]
            
            st.markdown("**🧅 Malzeme bazlı sorular:**")
            ingredient_questions = [
                "🥩 Elimde tavuk var, ne yapabilirim?",
                "🥔 Patates ve soğanla ne pişirebilirim?",
                "🧀 Peynirli kolay tarif öner"
            ]
            
            st.markdown("**🥗 Özel diyet soruları:**")
            diet_questions = [
                "🌾 Glutensiz makarna tarifi",
                "🥛 Laktozsuz tatlı tarifi",
                "🌱 Vegan köfte tarifi",
                "🥑 Keto uyumlu kahvaltı",
                "🍯 Şekersiz kurabiye"
            ]
        
        for i, question in enumerate(example_questions):
            if st.button(question, use_container_width=True, key=f"example_{language}_{i}"):
                # Add to chat
                st.session_state.messages.append({"role": "user", "content": question})
                spinner_text = "Preparing answer..." if language == "English" else "Cevap hazırlanıyor..."
                with st.spinner(spinner_text):
                    response = simple_recipe_response(question, language)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
        
        for i, question in enumerate(ingredient_questions):
            if st.button(question, use_container_width=True, key=f"ingredient_{language}_{i}"):
                # Add to chat
                st.session_state.messages.append({"role": "user", "content": question})
                spinner_text = "Preparing answer..." if language == "English" else "Cevap hazırlanıyor..."
                with st.spinner(spinner_text):
                    response = simple_recipe_response(question, language)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
        
        for i, question in enumerate(diet_questions):
            if st.button(question, use_container_width=True, key=f"diet_{language}_{i}"):
                # Add to chat
                st.session_state.messages.append({"role": "user", "content": question})
                spinner_text = "Preparing answer..." if language == "English" else "Cevap hazırlanıyor..."
                with st.spinner(spinner_text):
                    response = simple_recipe_response(question, language)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
    


if __name__ == "__main__":
    main()