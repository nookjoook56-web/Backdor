import requests

def get_vavoo_token():
    url = "https://www2.vavoo.to/live2/check"
    headers = {'User-Agent': 'VAVOO/2.6', 'Host': 'www2.vavoo.to'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data[0].get('token') if isinstance(data, list) else data.get('token')
    except:
        return None
    return None

def update_playlist():
    token = get_vavoo_token()
    if not token:
        print("Token alınamadı, işlem iptal.")
        return

    # Dosyayı önce internetten çekiyoruz (Yerelde yoksa hata almamak için)
    github_raw_url = "https://raw.githubusercontent.com/nookjoook56-web/Update-m3u/main/playlist.m3u"
    
    try:
        response = requests.get(github_raw_url)
        if response.status_code == 200:
            lines = response.text.splitlines()
            new_lines = []
            
            for line in lines:
                line = line.strip()
                if "vavoo.to" in line and ".m3u8" in line:
                    # Mevcut auth parametresini temizle ve yenisini ekle
                    base_url = line.split('?auth=')[0]
                    new_lines.append(f"{base_url}?auth={token}")
                else:
                    new_lines.append(line)
            
            # Sonuçları 'playlist.m3u' adıyla kaydet (Git'in bulması için)
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write("\n".join(new_lines))
            print(f"Başarılı! Yeni token uygulandı: {token}")
        else:
            print(f"Liste çekilemedi. HTTP Kodu: {response.status_code}")
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    update_playlist()
    
