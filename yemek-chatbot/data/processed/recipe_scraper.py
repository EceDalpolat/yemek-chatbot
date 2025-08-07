import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

class RecipeScraper:
    def __init__(self):
        self.recipes = []
    
    def scrape_nefis_yemekler(self, max_page=100):
        base_url = "https://www.nefisyemektarifleri.com/tarifler/yeni-tarifler/"
        for page in range(1, max_page + 1):
            try:
                url = f"{base_url}?page={page}"
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                recipes = soup.find_all("div", class_="recipe-card")
                
                for recipe in recipes:
                    try:
                        title_elem = recipe.find("h3", class_="recipe-title")
                        desc_elem = recipe.find("p", class_="recipe-description")
                        
                        if title_elem and desc_elem:
                            title = title_elem.text.strip()
                            description = desc_elem.text.strip()
                            self.recipes.append({
                                "title": title,
                                "description": description,
                                "source": "nefisyemektarifleri.com"
                            })
                    except Exception as e:
                        print(f"Tarif işlenirken hata: {e}")
                        continue
            except Exception as e:
                print(f"Sayfa {page} yüklenirken hata: {e}")
                continue
    
    def scrape_yemekcom(self, max_page=100):
        base_url = "https://www.yemek.com/tarifler/yeni-tarifler/"
        for page in range(1, max_page + 1):
            try:
                url = f"{base_url}?page={page}"
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                recipes = soup.find_all("div", class_="recipe-card")
                
                for recipe in recipes:
                    try:
                        title_elem = recipe.find("h3", class_="recipe-title")
                        if title_elem:
                            title = title_elem.text.strip()
                            self.recipes.append({
                                "title": title,
                                "description": "",
                                "source": "yemek.com"
                            })
                    except Exception as e:
                        print(f"Tarif işlenirken hata: {e}")
                        continue
            except Exception as e:
                print(f"Sayfa {page} yüklenirken hata: {e}")
                continue
    
    def save_recipes(self, filename):
        df = pd.DataFrame(self.recipes)
        df.to_json(filename, orient='records', ensure_ascii=False)

