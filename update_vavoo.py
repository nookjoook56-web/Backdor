import requests
import os
import random

def get_proxy():
    """Ücretsiz proxy listesinden rastgele bir proxy çeker."""
    try:
        # Ücretsiz proxy sağlayan bir API (PubProxy veya benzeri)
        proxy_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
        response = requests.get(proxy_url, timeout=10)
        if response.status_code == 200:
            proxies = response.text.splitlines()
            return random.choice(proxies)
    except:
        return None
    return None

def update_playlist():
    # Vavoo'nun korumasını aşmış, hazır tokenlı kaynak
    source_url = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr_vavoo.m3u"
    
    proxy = get_proxy()
    proxies_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        if proxy:
            print(f"Özel Proxy kullanılıyor: {proxy}")
        else:
            print("Proxy alınamadı, doğrudan bağlanılıyor...")

        # İsteği proxy üzerinden gönder
        response = requests.get(source_url, headers=headers, proxies=proxies_dict, timeout=30)
        
        if response.status_code == 200 and "#EXTM3U" in response.text:
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"BAŞARILI: Veri çekildi ve playlist.m3u güncellendi.")
        else:
            print(f"HATA: Kaynak yanıt vermedi (Kod: {response.status_code})")
            
    except Exception as e:
        print(f"Bağlantı hatası: {e}")

if __name__ == "__main__":
    update_playlist()
    
