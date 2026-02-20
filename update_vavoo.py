import requests
import os
import json

# Merkezi Domain Yönetimi
DOMAINS = {
    "vavoo": "vavoo.to",
    "animesaturn": "animesaturn.cx",
    "vixsrc": "vixsrc.to",
    "animeunity": "animeunity.so"
}

def get_vavoo_token():
    # Domain sözlüğünden adresi çekiyoruz
    base_domain = DOMAINS["vavoo"]
    url = f"https://www.{base_domain}/live2/check"
    
    headers = {
        'User-Agent': 'VAVOO/2.6',
        'X-VAVOO-DEVICE': 'd7f3e8a1-b2c4-4e5f-8d9a-0b1c2d3e4f5g'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            token = data[0].get('token') if isinstance(data, list) else data.get('token')
            print(f"Token başarıyla alındı (Domain: {base_domain})")
            return token
    except Exception as e:
        print(f"Token alınırken hata: {e}")
    return None

def update_playlist():
    token = get_vavoo_token()
    if not token:
        print("HATA: Token alınamadı, işlem durduruldu.")
        return

    # Dinamik URL oluşturma
    index_url = f"https://www.{DOMAINS['vavoo']}/live2/index.json"
    
    try:
        print(f"Vavoo veritabanı taranıyor: {index_url}")
        response = requests.get(index_url, timeout=20)
        
        if response.status_code == 200:
            channels = response.json()
            m3u_lines = ["#EXTM3U"]
            
            for ch in channels:
                name = ch.get('name', 'Bilinmeyen Kanal')
                group = ch.get('group', 'Genel')
                base_url = ch.get('url')
                
                if base_url:
                    # Link yapısını oluştur ve token ekle
                    m3u_lines.append(f'#EXTINF:-1 group-title="{group}",{name}')
                    # URL zaten parametre içeriyorsa & yoksa ? kullanır
                    separator = "&" if "?" in base_url else "?"
                    m3u_lines.append(f"{base_url}{separator}auth={token}")
            
            # Dosyayı kaydet
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write("\n".join(m3u_lines))
            
            print(f"BAŞARILI: {len(channels)} kanal güncel domain ve token ile kaydedildi.")
        else:
            print(f"Veritabanı hatası: {response.status_code}")
            
    except Exception as e:
        print(f"Sistem hatası: {e}")

if __name__ == "__main__":
    update_playlist()
    
