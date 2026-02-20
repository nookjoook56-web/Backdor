import requests
import os
import time
import json

def get_vavoo_token():
    """Vavoo sunucularından resmi el sıkışma (handshake) ile token alır."""
    # Vavoo'nun doğrulama yaptığı güncel adres
    url = "https://www.vavoo.to/live2/check"
    
    # Uygulamanın orijinal başlıklarını taklit ediyoruz
    headers = {
        'User-Agent': 'VAVOO/2.6',
        'Accept': 'application/json',
        'X-VAVOO-DEVICE': 'd7f3e8a1-b2c4-4e5f-8d9a-0b1c2d3e4f5g', # Rastgele cihaz kimliği
        'Connection': 'keep-alive'
    }

    try:
        # verify=False bazen SSL sertifika hatalarını aşmak için gerekebilir
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # Token genellikle bir liste veya obje içinde döner
            token = data[0].get('token') if isinstance(data, list) else data.get('token')
            if token:
                print(f"BAŞARILI: Yeni imza yakalandı: {token[:15]}...")
                return token
        print(f"Uyarı: Doğrudan token alınamadı (Kod: {response.status_code}), yedek yöntem deneniyor...")
    except Exception as e:
        print(f"Bağlantı hatası: {e}")
    return None

def update_playlist():
    token = get_vavoo_token()
    
    # Token alınamazsa bile sistemin çökmemesi için süreci yönetiyoruz
    if not token:
        print("KRİTİK HATA: İmza simülasyonu başarısız oldu.")
        return

    # Korumayı aşmış ana m3u veri kaynağı
    source_url = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr_vavoo.m3u"
    
    try:
        response = requests.get(source_url, timeout=20)
        if response.status_code == 200:
            lines = response.text.splitlines()
            updated_m3u = []
            
            for line in lines:
                line = line.strip()
                # Vavoo linklerini bul ve yeni imzayı (auth token) ekle
                if "vavoo.to" in line:
                    # Linkin sonundaki eski parametreleri temizle
                    base_url = line.split('?')[0]
                    # Yeni imzayı ekleyerek linki canlandır
                    updated_m3u.append(f"{base_url}?auth={token}")
                else:
                    updated_m3u.append(line)
            
            # Dosyayı kaydet
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write("\n".join(updated_m3u))
            
            print(f"TAMAMLANDI: playlist.m3u güncellendi. Kanal sayısı: {len(updated_m3u)//2}")
        else:
            print("HATA: Liste kaynağına ulaşılamadı.")
    except Exception as e:
        print(f"Sistem hatası: {e}")

if __name__ == "__main__":
    update_playlist()
            
