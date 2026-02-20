import requests
import os

def get_vavoo_token():
    # Birkaç farklı endpoint deneyelim
    urls = [
        "https://www.vavoo.to/live2/check",
        "https://vavoo.to/live2/check",
        "https://www2.vavoo.to/live2/check"
    ]
    
    headers = {
        'User-Agent': 'VAVOO/2.6',
        'Accept': 'application/json',
        'X-VAVOO-DEVICE': '1234567890' # Bazı durumlarda cihaz kimliği ister
    }

    for url in urls:
        try:
            print(f"Deneniyor: {url}")
            # SSL doğrulamasını devre dışı bırakmak (verify=False) bazen işe yarar
            response = requests.get(url, headers=headers, timeout=10, verify=True)
            if response.status_code == 200:
                data = response.json()
                token = data[0].get('token') if isinstance(data, list) else data.get('token')
                if token:
                    print(f"BAŞARILI! Token bulundu: {token[:10]}...")
                    return token
            else:
                print(f"Durum Kodu: {response.status_code}")
        except Exception as e:
            print(f"Hata: {e}")
            
    return None

def update_playlist():
    token = get_vavoo_token()
    if not token:
        print("KRİTİK HATA: Hiçbir adresten token alınamadı. Vavoo erişimi engellemiş olabilir.")
        return

    github_url = "https://raw.githubusercontent.com/nookjoook56-web/Update-m3u/main/playlist.m3u"
    
    try:
        res = requests.get(github_url)
        if res.status_code == 200:
            lines = res.text.splitlines()
            new_lines = []
            for line in lines:
                if "vavoo.to" in line and ".m3u8" in line:
                    base = line.split('?auth=')[0]
                    new_lines.append(f"{base}?auth={token}")
                else:
                    new_lines.append(line)
            
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write("\n".join(new_lines))
            print("Dosya başarıyla güncellendi.")
        else:
            print(f"GitHub listesi alınamadı: {res.status_code}")
    except Exception as e:
        print(f"Güncelleme hatası: {e}")

if __name__ == "__main__":
    update_playlist()
              
