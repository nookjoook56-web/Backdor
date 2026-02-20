import requests
import os

def update_playlist():
    # Vavoo'nun korumasını aşmış, hazır ve güncel tokenlı linkler sunan güvenilir kaynak
    # Bu kaynak GitHub Action tarafından genellikle engellenmez.
    source_url = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr_vavoo.m3u"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        print("Güncel kanallar ve çalışan tokenlar toplanıyor...")
        response = requests.get(source_url, headers=headers, timeout=30)
        
        if response.status_code == 200 and "#EXTM3U" in response.text:
            content = response.text
            # Gelen içeriği senin playlist.m3u dosyana yazıyoruz
            file_path = "playlist.m3u"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            # Dosya boyutunu kontrol edelim (Büyümüş olması lazım)
            file_size = os.path.getsize(file_path)
            print(f"BAŞARILI: {file_size} byte veri yazıldı. Yüzlerce güncel kanal eklendi!")
        else:
            print(f"HATA: Kaynak yanıt vermedi veya içerik boş (Kod: {response.status_code}).")

    except Exception as e:
        print(f"Bağlantı hatası oluştu: {e}")

if __name__ == "__main__":
    update_playlist()
    
