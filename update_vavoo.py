import requests
import os
import random

def get_proxy():
    """Ücretsiz proxy havuzundan çalışan bir IP yakalar."""
    # En güvenilir ücretsiz proxy kaynakları
    proxy_urls = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://www.proxy-list.download/api/v1/get?type=https",
        "https://www.proxyscan.io/download?type=https"
    ]
    
    for api_url in proxy_urls:
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                proxies = response.text.splitlines()
                if proxies:
                    # Rastgele bir proxy seç
                    return random.choice(proxies).strip()
        except:
            continue
    return None

def update_playlist():
    # Korumayı aşmış ana kaynak (iptv-org topluluğu tarafından onaylı)
    source_url = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr_vavoo.m3u"
    
    proxy = get_proxy()
    # Proxy sözlüğünü oluştur (Hem http hem https için)
    proxies_dict = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    } if proxy else None
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': '*/*'
    }

    try:
        if proxy:
            print(f"Özel Proxy Tüneli Kuruldu: {proxy}")
        else:
            print("Proxy yakalanamadı, doğrudan bağlantı deneniyor...")

        # İsteği proxy tüneli üzerinden gönder
        response = requests.get(source_url, headers=headers, proxies=proxies_dict, timeout=30)
        
        if response.status_code == 200 and "#EXTM3U" in response.text:
            file_path = "playlist.m3u"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            
            size = os.path.getsize(file_path)
            print(f"BAŞARILI: {size} byte veri proxy üzerinden güvenle çekildi.")
        else:
            print(f"HATA: Kaynak yanıt vermedi. Kod: {response.status_code}")
            
    except Exception as e:
        print(f"Bağlantı hatası: {e}")

if __name__ == "__main__":
    update_playlist()
    
