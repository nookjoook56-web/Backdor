import requests

def get_vavoo_token():
    url = "https://www2.vavoo.to/live2/check"
    headers = {'User-Agent': 'VAVOO/2.6', 'Host': 'www2.vavoo.to'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data[0].get('token') if isinstance(data, list) else data.get('token')
    except: return None
    return None

def update_playlist():
    token = get_vavoo_token()
    if not token: return

    # Mevcut playlist.m3u dosyasını oku
    try:
        with open("playlist.m3u", "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            line = line.strip()
            if "vavoo.to" in line and ".m3u8" in line:
                # Eski auth'u temizle ve yenisini ekle
                base_url = line.split('?auth=')[0]
                new_lines.append(f"{base_url}?auth={token}")
            else:
                new_lines.append(line)
        
        # Dosyayı güncelle
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines))
        print(f"Token güncellendi: {token}")
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    update_playlist()
  
