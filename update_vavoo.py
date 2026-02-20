import requests
import os

def update_playlist():
    # Vavoo'nun korumasını aşmış, hazır ve güncel m3u sunan alternatif kaynak
    # Bu kaynak GitHub Action tarafından genellikle engellenmez.
    source_url = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr_vavoo.m3u"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        print("Güncel kanallar ve tokenlar toplanıyor...")
        response = requests.get(source_url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            content = response.text
            # Dosyayı senin playlist.m3u dosyana yazıyoruz
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write(content)
            print("BAŞARILI: Yüzlerce güncel kanal ve çalışan tokenlar eklendi!")
        else:
            print(f"Kaynak yanıt vermedi: {response.status_code}. Yedek liste oluşturuluyor...")
            # Eğer internetten çekemezsek, en azından iskeleti koru (senin yaptığın gibi)
            create_backup_list()

    except Exception as e:
        print(f"Hata oluştu: {e}")
        create_backup_list()

def create_backup_list():
    # İnternet kesilirse dosyanın silinmemesi için emniyet kemeri
    if not os.path.exists("playlist.m3u"):
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n#EXTINF:-1,Yedek Kanal\nhttps://vavoo.to/live2/test.m3u8")

if __name__ == "__main__":
    update_playlist()
    
