import requests
import os

def get_vavoo_token():
    # 404 hatasını önlemek için güncellenmiş URL
    url = "https://www.vavoo.to/live2/check" 
    headers = {
        'User-Agent': 'VAVOO/2.6',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }
    try:
        # verify=False ekleyerek SSL sertifika hatalarını geçebiliriz
        response = requests.get(url, headers=headers, timeout=15)
        print(f"Token Sorgusu Durumu: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            # Vavoo bazen liste bazen obje döndürür
            token = data[0].get('token') if isinstance(data, list) else data.get('token')
            if token:
                print(f"Token Başarıyla Alındı: {token[:10]}...")
                return token
        elif response.status_code == 404:
            print("HATA: Vavoo API adresi değişmiş (404).")
    except Exception as e:
        print(f"Bağlantı hatası: {e}")
    return None

def update_playlist():
    token = get_vavoo_token()
    if not token:
        print("HATA: Token alınamadığı için işlem durduruldu.")
        return

    # Kayıtlı GitHub linkin
    github_raw_url = "https://raw.githubusercontent.com/nookjoook56-web/Update-m3u/main/playlist.m3u"
    
    try:
        response = requests.get(github_raw_url)
        if response.status_code == 200:
            lines = response.text.splitlines()
            new_lines = []
            
            for line in lines:
                line = line.strip()
                # Vavoo linklerini bul ve token ekle
                if "vavoo.to" in line and ".m3u8" in line:
                    base_url = line.split('?auth=')[0]
                    new_lines.append(f"{base_url}?auth={token}")
                else:
                    new_lines.append(line)
            
            # Dosyayı yerel dizine yaz
            file_path = "playlist.m3u"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(new_lines))
            
            if os.path.exists(file_path):
                print(f"BAŞARILI: {file_path} güncellendi.")
            else:
                print("HATA: Dosya oluşturulamadı.")
        else:
            print(f"HATA: Liste indirilemedi (HTTP {response.status_code}).")
    except Exception as e:
        print(f"Liste işleme hatası: {e}")

if __name__ == "__main__":
    update_playlist()
    
