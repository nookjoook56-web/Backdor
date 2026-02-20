import requests
import os

def update_playlist():
    # Engellenen API yerine, topluluk tarafından güncellenen güncel ham veri kaynağı
    # Bu kaynak genellikle çalışan auth tokenları önceden eklenmiş linkler sunar
    backup_sources = [
        "https://raw.githubusercontent.com/De-Y/vavoo/main/vavoo.m3u",
        "https://archive.org/download/vavoo-turk/vavoo.m3u"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': '*/*'
    }

    m3u_content = None

    for source in backup_sources:
        try:
            print(f"Kaynak deneniyor: {source}")
            response = requests.get(source, headers=headers, timeout=15)
            if response.status_code == 200 and "#EXTM3U" in response.text:
                m3u_content = response.text
                print(f"BAŞARILI: {source} üzerinden güncel liste alındı.")
                break
        except Exception as e:
            print(f"Kaynak hatası: {e}")

    if not m3u_content:
        print("KRİTİK HATA: Hiçbir kaynaktan güncel liste alınamadı.")
        return

    # Dosyayı yerel dizine (playlist.m3u) kaydet
    file_path = "playlist.m3u"
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        
        if os.path.exists(file_path):
            print(f"TAMAMLANDI: {file_path} dosyası yeni verilerle oluşturuldu.")
        else:
            print("HATA: Dosya yazımı başarısız.")
    except Exception as e:
        print(f"Yazma hatası: {e}")

if __name__ == "__main__":
    update_playlist()
    
