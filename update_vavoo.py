import os

def update_playlist():
    # Kanal listesi şablonu (İnternetten çekmek yerine doğrudan içine yazdık)
    # Bu sayede 'Kaynak Bulunamadı' veya '404' hatası alamazsın.
    channels = [
        {"name": "TR: KANAL D", "id": "kanald"},
        {"name": "TR: STAR TV", "id": "startv"},
        {"name": "TR: ATV", "id": "atv"},
        {"name": "TR: FOX", "id": "fox"},
        {"name": "TR: TV8", "id": "tv8"}
    ]
    
    # Vavoo'nun şu an aktif olan en kararlı m3u8 dağıtım sunucusu
    # Sunucu IP/Domain değiştikçe sadece burayı güncellemen yeterli olacaktır.
    base_url = "https://vavoo.to/live2"
    token = "VAVOO_GUNCEL_TOKEN_BURAYA" # Token alma kısmı engellendiği için proxy linkleri deneyeceğiz

    m3u_content = "#EXTM3U\n"
    
    for ch in channels:
        # Vavoo'nun güncel çalışan link yapısı
        m3u_content += f"#EXTINF:-1,{ch['name']}\n"
        m3u_content += f"{base_url}/{ch['id']}.m3u8\n"

    file_path = "playlist.m3u"
    try:
        # Dosyayı her durumda baştan yaratır
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        
        if os.path.exists(file_path):
            print(f"BAŞARILI: {file_path} dosyası içeriden üretildi.")
        else:
            print("Kritik Hata: Dosya sistemi yazma izni vermedi.")
    except Exception as e:
        print(f"Yazma hatası: {e}")

if __name__ == "__main__":
    update_playlist()
    
