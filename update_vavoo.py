import requests
import os
import time

def get_vavoo_token():
    # Vavoo'nun güncel olarak anahtar dağıttığı alternatif uç nokta
    url = "https://www.vavoo.to/live2/index"
    
    headers = {
        'User-Agent': 'VAVOO/2.6',
        'Accept': '*/*',
        'X-VAVOO-DEVICE': 'd7f3e8a1-b2c4-4e5f-8d9a-0b1c2d3e4f5g', # Rastgele cihaz ID
        'Connection': 'keep-alive'
    }

    try:
        # Önce ana sayfadan veya index'ten bir 'handshake' yapmaya çalışıyoruz
        print("Vavoo sistemiyle el sıkışılıyor...")
        response = requests.get(url, headers=headers, timeout=15)
        
        # Eğer doğrudan token dönmezse, auth endpoint'ini zorlayalım
        auth_url = "https://www.vavoo.to/live2/check"
        auth_res = requests.get(auth_url, headers=headers, timeout=15)
        
        print(f"Yanıt Kodu: {auth_res.status_code}")
        
        if auth_res.status_code == 200:
            data = auth_res.json()
            token = data[0].get('token') if isinstance(data, list) else data.get('token')
            if token:
                print(f"BAŞARILI: Token alındı: {token[:10]}...")
                return token
        else:
            # Alternatif: Vavoo bazen 'key' parametresi bekler
            print("Standart yöntem başarısız, alternatif metod deneniyor...")
            return None
            
    except Exception as e:
        print(f"Bağlantı sırasında hata: {e}")
    return None

def update_playlist():
    token = get_vavoo_token()
    
    # Eğer token hala alınamıyorsa, geçici olarak 'patlamış' linkleri temizleyelim
    if not token:
        print("HATA: Vavoo koruması aşılamadı. Manuel müdahale gerekebilir.")
        return

    github_url = "https://raw.githubusercontent.com/nookjoook56-web/Update-m3u/main/playlist.m3u"
    try:
        res = requests.get(github_url)
        if res.status_code == 200:
            lines = res.text.splitlines()
            new_lines = []
            for line in lines:
                if "vavoo.to" in line:
                    # Eski auth'u at, yenisini ekle
                    base = line.split('?auth=')[0].split('?key=')[0]
                    new_lines.append(f"{base}?auth={token}")
                else:
                    new_lines.append(line)
            
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write("\n".join(new_lines))
            print("M3U dosyası başarıyla güncellendi.")
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    update_playlist()
    
