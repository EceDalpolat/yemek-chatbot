import openai
import json
import time

class ModelTrainer:
    def __init__(self, openai_api_key):
        openai.api_key = openai_api_key
    
    def upload_training_file(self, file_path):
        """Eğitim dosyasını OpenAI'ye yükle"""
        try:
            with open(file_path, 'rb') as f:
                response = openai.files.create(
                    file=f,
                    purpose='fine-tune'
                )
            return response.id
        except Exception as e:
            print(f"Dosya yükleme hatası: {e}")
            return None
    
    def create_fine_tune_job(self, training_file_id, model="gpt-3.5-turbo"):
        """Fine-tuning işi oluştur"""
        try:
            response = openai.fine_tuning.jobs.create(
                training_file=training_file_id,
                model=model
            )
            return response.id
        except Exception as e:
            print(f"Fine-tuning işi oluşturma hatası: {e}")
            return None
    
    def check_job_status(self, job_id):
        """İş durumunu kontrol et"""
        try:
            response = openai.fine_tuning.jobs.retrieve(job_id)
            return response.status
        except Exception as e:
            print(f"Durum kontrol hatası: {e}")
            return None
    
    def wait_for_completion(self, job_id, check_interval=30):
        """İşin tamamlanmasını bekle"""
        while True:
            status = self.check_job_status(job_id)
            print(f"İş durumu: {status}")
            
            if status in ['succeeded', 'failed', 'cancelled']:
                break
            
            time.sleep(check_interval)
        
        return status
    
    def get_fine_tuned_model(self, job_id):
        """Fine-tune edilmiş modeli al"""
        try:
            job = openai.fine_tuning.jobs.retrieve(job_id)
            return job.fine_tuned_model
        except Exception as e:
            print(f"Model alma hatası: {e}")
            return None