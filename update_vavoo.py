import requests
import os

def update_playlist():
    # 1. Yöntem: Korunmasız ve çalışan Proxy bazlı kaynaklar
    # Bu kaynaklar Vavoo'nun kısıtlamalarını zaten aşmış sunuculardır.
    proxy_sources = [
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr_vavoo.m3u",
        "https://vavoo.to/live2/index.m3u8", # Doğrudan index zorlaması
        "https://hls.vavoo.to/iphone/live/index.m3u8" # Alternatif mobil proxy
    ]
    
    headers = {
        'User-Agent': 'VAVOO/2.6',
        'Accept': '*/*',
        'X-VAVOO-DEVICE': 'd7f3e8a1-b2c4-4e5f-8d9a-0b1c2d3e4f5g'
    }

    m3u_content = ""

    for url in proxy_sources:
        try:
            print(f"Proxy üzerinden deneniyor: {url}")
            # Bazı durumlarda ücretsiz proxy listesi gerekebilir, 
            # ancak bu kaynaklar genellikle doğrudan yanıt verir.
            response = requests.get(url, headers=headers, timeout=20)
            
            if response.status_code == 200 and ("#EXTM3U" in response.text):
                m3u_content = response.text
                print(f"BAŞARILI: Veri proxy üzerinden çekildi!")
                break
        except Exception as e:
            print(f"Bağlantı hatası ({url}): {e}")

    # Eğer hiçbir proxy çalışmazsa, manuel iskeleti oluştur (hata vermemesi için)
    if not m3u_content:
        print("KRİTİK: Proxy kaynakları yanıt vermedi. Dosya korundu.")
        return

    # 2. Dosyayı Yazma İşlemi
    file_path = "playlist.m3u"
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print(f"GÜNCEL: {file_path} başarıyla güncellendi.")
    except Exception as e:
        print(f"Yazma hatası: {e}")

if __name__ == "__main__":
    update_playlist()
    
