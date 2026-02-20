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
    base_domain = DOMAINS["vavoo"]
    url = f"https://www.{base_domain}/live2/check"
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
        print("HATA: Token alınamadı.")
        return

    index_url = f"https://www.{DOMAINS['vavoo']}/live2/index.json"
    
    try:
        response = requests.get(index_url, timeout=20)
        if response.status_code == 200:
            channels = response.json()
            m3u_lines = ["#EXTM3U"]
            count = 0
            
            for ch in channels:
                name = ch.get('name', '').upper()
                group = ch.get('group', '').upper()
                base_url = ch.get('url')
                
                # --- AKILLI FİLTRELEME BURADA ---
                # Sadece Türkiye kanallarını ve ortak grupları alıyoruz
                is_turkish = "TURK" in group or "TURK" in name or "TR:" in name
                
                if is_turkish and base_url:
                    m3u_lines.append(f'#EXTINF:-1 group-title="{group}",{ch.get("name")}')
                    separator = "&" if "?" in base_url else "?"
                    m3u_lines.append(f"{base_url}{separator}auth={token}")
                    count += 1
            
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write("\n".join(m3u_lines))
            
            print(f"FİLTRELEME BAŞARILI: {count} adet Türkiye kanalı listelendi.")
        else:
            print(f"HATA: Veritabanına ulaşılamadı.")
            
    except Exception as e:
        print(f"Sistem hatası: {e}")

if __name__ == "__main__":
    update_playlist()
    
