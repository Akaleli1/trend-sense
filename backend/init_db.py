# backend/init_db.py
from database.db import Database
from etl.data_fetcher import fetch_all_trends_data

def init_application():
    print("--- Veritabanı Başlatılıyor ---")
    db = Database()
    
    # 1. Tabloları oluştur
    print("1. Tablolar kontrol ediliyor...")
    db.create_tables()
    
    # 2. Verileri temizle (İsteğe bağlı, temiz başlangıç için)
    # db.execute("DELETE FROM sentiments") 
    
    # 3. ETL işlemini başlat
    print("2. Mock veriler çekiliyor ve veritabanına yazılıyor...")
    # Not: fetch_all_trends_data fonksiyonu artık veriyi hem çekip hem DB'ye yazmalı
    # Eğer son Cursor güncellemesi bunu yaptıysa, bu fonksiyon yeterli olacaktır.
    data = fetch_all_trends_data()
    
    if data:
        print(f"✅ Başarılı! Toplam {len(data)} adet veri işlendi.")
    else:
        print("⚠️ Uyarı: Hiç veri dönmedi. data_fetcher.py dosyasını kontrol etmeliyiz.")

    print("--- İşlem Tamamlandı ---")

if __name__ == "__main__":
    init_application()