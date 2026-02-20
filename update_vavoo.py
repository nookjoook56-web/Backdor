import requests
import os
import random

def update_playlist():
    # 1. Korumayı aşmış ana kaynak
    source_url = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr_vavoo.m3u"
    
    # 2. Ücretsiz ve hızlı Proxy listesi (Statik olarak tanımlandı)
    # Eğer bu proxylerden biri çalışmazsa sistem diğerini dener.
    proxy_list = [
        "167.172.191.246:80",   # Örnek Statik Proxy 1
        "178.62.193.19:8080",   # Örnek Statik Proxy 2
        "159.203.116.148:80"    # Örnek Statik Proxy 3
    ]
    
    selected_proxy = random.choice(proxy_list)
    proxies_dict = {
        "http": f"http://{selected_proxy}",
        "https": f"http://{selected_proxy}"
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': '*/*'
    }

    try:
        print(f"Statik Proxy Tüneli Aktif: {selected_proxy}")
        
        # İsteği tünel üzerinden gönder
        response = requests.get(source_url, headers=headers, proxies=proxies_dict, timeout=30)
        
        if response.status_code == 200 and "#EXTM3U" in response.text:
            file_path = "playlist.m3u"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            
            size = os.path.getsize(file_path)
            print(f"BAŞARILI: {size} byte veri tünel üzerinden güvenle yazıldı.")
        else:
            print(f"HATA: Proxy yanıt verdi ancak veri alınamadı. Kod: {response.status_code}")
            # Proxy başarısız olursa doğrudan bağlantıyı dene (B planı)
            print("Proxy başarısız, doğrudan bağlantı deneniyor...")
            fallback = requests.get(source_url, headers=headers, timeout=20)
            if fallback.status_code == 200:
                with open("playlist.m3u", "w", encoding="utf-8") as f:
                    f.write(fallback.text)
                print("BAŞARILI: Veri doğrudan bağlantı ile kurtarıldı.")
            
    except Exception as e:
        print(f"Tünel hatası: {e}. Dosya oluşturulamadı.")

if __name__ == "__main__":
    update_playlist()
    
