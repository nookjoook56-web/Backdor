import requests
import os
import json

def get_vavoo_token():
    """Resmi el sıkışma ile taze auth token alır."""
    url = "https://www.vavoo.to/live2/check"
    headers = {'User-Agent': 'VAVOO/2.6', 'X-VAVOO-DEVICE': 'd7f3e8a1-b2c4-4e5f-8d9a-0b1c2d3e4f5g'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data[0].get('token') if isinstance(data, list) else data.get('token')
    except:
        return None
    return None

def update_playlist():
    token = get_vavoo_token()
    if not token:
        print("KRİTİK HATA: İmza (token) alınamadı.")
        return

    # Vavoo'nun tüm kanal listesini barındıran JSON veritabanı
    index_url = "https://www.vavoo.to/live2/index.json"
    print("Vavoo veritabanı taranıyor...")

    try:
        response = requests.get(index_url, timeout=20)
        if response.status_code == 200:
            channels = response.json()
            m3u_lines = ["#EXTM3U"]
            
            # Sadece Türkiye kanallarını veya tümünü filtreleyebiliriz
            # Bu örnekte tüm kanalları güncel imzalarla ekliyoruz
            for ch in channels:
                name = ch.get('name', 'Bilinmeyen Kanal')
                group = ch.get('group', 'Genel')
                # Kanal URL yapısını imza ile birleştiriyoruz
                # Vavoo genellikle 'url' veya 'url2' içinde kanal ID barındırır
                base_url = ch.get('url')
                if base_url:
                    m3u_lines.append(f'#EXTINF:-1 group-title="{group}",{name}')
                    # Eğer URL zaten token içermiyorsa, bizim tokenı ekliyoruz
                    final_url = f"{base_url}?auth={token}" if "?auth=" not in base_url else base_url
                    m3u_lines.append(final_url)
            
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write("\n".join(m3u_lines))
            
            print(f"BAŞARILI: {len(channels)} kanal güncel imzalarla listeye eklendi.")
        else:
            print(f"HATA: Veritabanına ulaşılamadı. Kod: {response.status_code}")
    except Exception as e:
        print(f"Sistem hatası: {e}")

if __name__ == "__main__":
    update_playlist()
                      
