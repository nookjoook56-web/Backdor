import requests
import os

def update_playlist():
    # Vavoo'nun korumasını aşmış, hazır ve güncel tokenlı linkler sunan kaynak
    source_url = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr_vavoo.m3u"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        print("Güncel kanallar ve çalışan tokenlar toplanıyor...")
        response = requests.get(source_url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            content = response.text
            # Gelen içeriği senin playlist.m3u dosyana yazıyoruz
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write(content)
            print("BAŞARILI: Yüzlerce güncel kanal ve çalışan tokenlar eklendi!")
        else:
            print(f"Kaynak yanıt vermedi (Kod: {response.status_code}). Yedek liste korunuyor.")

    except Exception as e:
        print(f"Bağlantı hatası: {e}")

if __name__ == "__main__":
    update_playlist()
    
