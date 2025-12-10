import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("HATA: .env dosyasında GEMINI_API_KEY bulunamadı!")
else:
    genai.configure(api_key=api_key)
    print(f"Anahtar ile bağlanılıyor... (Key: {api_key[:5]}...)")
    
    print("\n--- Kullanılabilir Modeller ---")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"HATA: {e}")