# 🍳 AI-Powered Cooking Assistant | Yapay Zeka Destekli Yemek Asistanı

A multilingual AI chatbot that provides cooking recipes, dietary advice, and culinary guidance. Built with Streamlit, OpenAI, and vector database technology.

[English](#english) | [Türkçe](#türkçe)

---

## English

### ✨ Features

- 🌍 **Multilingual Support**: Automatic language detection with Turkish and English support
- 🍽️ **Recipe Recommendations**: Personalized cooking suggestions based on available ingredients
- 🥗 **Dietary Restrictions**: Specialized support for gluten-free, lactose-free, vegan, keto diets
- 🧠 **Memory System**: Remembers user preferences using Mem0
- 🔍 **Vector Search**: Fast recipe retrieval using Milvus vector database
- 🤖 **RAG Pipeline**: Retrieval-Augmented Generation for accurate responses
- 📱 **Modern UI**: Clean, responsive Streamlit interface
- 🔧 **Fine-tuning Ready**: Prepared for custom model training

### 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/EceDalpolat/yemek-chatbot.git
   cd yemek-chatbot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   cd yemek-chatbot
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env file with your API keys:
   # OPENAI_API_KEY=your_openai_key
   # MEM0_API_KEY=your_mem0_key (optional)
   ```

5. **Run the application**
   ```bash
   streamlit run src/chatbot/main.py
   ```

### 🐳 Docker Setup

```bash
# Start Milvus vector database
docker compose up -d

# Access the application
# Streamlit: http://localhost:8501
# Milvus: http://localhost:19530
```

### 📁 Project Structure

```
yemek-chatbot/
├── data/                    # Data storage
│   ├── recipes/             # Raw recipe data
│   ├── processed/           # Processed data
│   └── embeddings/          # Vector embeddings
├── src/
│   ├── data_processing/     # Data processing modules
│   ├── vector_db/          # Milvus operations
│   ├── rag/                # RAG pipeline
│   ├── memory/             # Memory management (Mem0)
│   ├── fine_tuning/        # Model fine-tuning
│   └── chatbot/            # Main application
├── configs/                # Configuration files
├── requirements.txt        # Python dependencies
└── docker-compose.yml     # Docker services
```

### 🎯 Usage Examples

```python
# Ask for recipes
"Give me a pasta recipe"
"I have chicken and rice, what can I cook?"

# Dietary restrictions
"Gluten-free bread recipe"
"Vegan protein sources"
"Lactose-free dessert ideas"

# Cooking techniques
"How to properly season meat?"
"Best way to cook vegetables?"
```

### 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Model**: OpenAI GPT-3.5/4, OpenRouter support
- **Vector DB**: Milvus
- **Memory**: Mem0
- **Data Processing**: Pandas, NumPy
- **ML**: Sentence Transformers, PyTorch
- **Deployment**: Docker, Docker Compose

### 🔧 Configuration

Edit configuration files in `configs/`:
- `milvus_config.yaml` - Vector database settings
- `model_config.yaml` - AI model parameters
- `mem0_config.yaml` - Memory system settings

### 📊 Fine-tuning

Train the model with your own recipe data:

```bash
python fine_tuning_example.py
```

### 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Türkçe

### ✨ Özellikler

- 🌍 **Çok Dil Desteği**: Otomatik dil algılama ile Türkçe ve İngilizce desteği
- 🍽️ **Tarif Önerileri**: Mevcut malzemelere göre kişiselleştirilmiş yemek önerileri
- 🥗 **Diyet Kısıtlamaları**: Glutensiz, laktozsuz, vegan, keto diyetler için özel destek
- 🧠 **Hafıza Sistemi**: Mem0 kullanarak kullanıcı tercihlerini hatırlama
- 🔍 **Vektör Arama**: Milvus vektör veritabanı ile hızlı tarif arama
- 🤖 **RAG Pipeline**: Doğru yanıtlar için Retrieval-Augmented Generation
- 📱 **Modern Arayüz**: Temiz, responsive Streamlit arayüzü
- 🔧 **Fine-tuning Hazır**: Özel model eğitimi için hazır altyapı

### 🚀 Hızlı Başlangıç

1. **Repository'yi klonlayın**
   ```bash
   git clone https://github.com/EceDalpolat/yemek-chatbot.git
   cd yemek-chatbot
   ```

2. **Virtual environment oluşturun**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate
   ```

3. **Bağımlılıkları yükleyin**
   ```bash
   cd yemek-chatbot
   pip install -r requirements.txt
   ```

4. **Environment variables ayarlayın**
   ```bash
   cp env.example .env
   # .env dosyasını API key'lerinizle düzenleyin:
   # OPENAI_API_KEY=openai_anahtarınız
   # MEM0_API_KEY=mem0_anahtarınız (opsiyonel)
   ```

5. **Uygulamayı çalıştırın**
   ```bash
   streamlit run src/chatbot/main.py
   ```

### 🎯 Kullanım Örnekleri

```python
# Tarif sorma
"Makarna tarifi ver"
"Elimde tavuk ve pirinç var, ne yapabilirim?"

# Diyet kısıtlamaları
"Glutensiz ekmek tarifi"
"Vegan protein kaynakları"
"Laktozsuz tatlı önerileri"

# Pişirme teknikleri
"Et nasıl baharatlanır?"
"Sebze pişirmenin en iyi yolu?"
```

### 📈 Geliştirme Planı

- [ ] Sesli komut desteği
- [ ] Görsel tarif tanıma
- [ ] Beslenme değeri hesaplama
- [ ] Sosyal medya entegrasyonu
- [ ] Mobil uygulama

### 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

### 📞 İletişim

- 🐛 Issues: [GitHub Issues](https://github.com/EceDalpolat/yemek-chatbot/issues)
- 📖 Wiki: [Project Wiki](https://github.com/EceDalpolat/yemek-chatbot/wiki)

---

### ⭐ Star the project if you find it useful!

Made with ❤️ by Ece DalPolat
