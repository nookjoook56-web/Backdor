import requests
import os
import random
import re

def get_vavoo_token():
    """Vavoo'nun o anki yetki anahtarını (auth token) yakalar."""
    # Token almak için en kararlı uç noktalar
    endpoints = [
        "https://www.vavoo.to/live2/check",
        "https://vavoo.to/live2/check"
    ]
    headers = {'User-Agent': 'VAVOO/2.6'}
    
    for url in endpoints:
        try:
            # Token alırken bazen proxy gerekebilir, doğrudan deniyoruz
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                token = data[0].get('token') if isinstance(data, list) else data.get('token')
                if token:
                    return token
        except:
            continue
    return None

def update_playlist():
    token = get_vavoo_token()
    if not token:
        print("HATA: Güncel token alınamadı. İşlem durduruldu.")
        return

    # Korumayı aşmış ana kanal listesi kaynağı
    source_url = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr_vavoo.m3u"
    
    try:
        print(f"Token Yakalandı: {token[:10]}... Liste güncelleniyor.")
        response = requests.get(source_url, timeout=20)
        
        if response.status_code == 200:
            lines = response.text.splitlines()
            new_m3u = []
            
            for line in lines:
                # Link satırlarını bul ve token ekle/güncelle
                if "vavoo.to" in line:
                    # Mevcut auth parametresini temizle ve yenisini ekle
                    clean_url = line.split('?auth=')[0].split('?key=')[0].strip()
                    new_m3u.append(f"{clean_url}?auth={token}")
                else:
                    new_m3u.append(line)
            
            # Dosyayı yaz
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write("\n".join(new_m3u))
            
            print(f"BAŞARILI: playlist.m3u dosyası {len(new_m3u)} satır ve taze token ile güncellendi.")
        else:
            print(f"HATA: Liste kaynağına ulaşılamadı (Kod: {response.status_code})")
            
    except Exception as e:
        print(f"Sistem hatası: {e}")

if __name__ == "__main__":
    update_playlist()
    
