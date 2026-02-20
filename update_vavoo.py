import requests
import os

def get_vavoo_token():
    url = "https://www2.vavoo.to/live2/check"
    headers = {'User-Agent': 'VAVOO/2.6', 'Host': 'www2.vavoo.to'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"Token Sorgusu Durumu: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            token = data[0].get('token') if isinstance(data, list) else data.get('token')
            print(f"Token Alındı: {token[:10]}...") # Güvenlik için sadece başını yazdırır
            return token
    except Exception as e:
        print(f"Token alınırken hata oluştu: {e}")
    return None

def update_playlist():
    token = get_vavoo_token()
    if not token:
        print("HATA: Token alınamadığı için işlem durduruldu.")
        return

    # Kendi GitHub linkinizden ham listeyi çekiyoruz
    github_raw_url = "https://raw.githubusercontent.com/nookjoook56-web/Update-m3u/main/playlist.m3u"
    print(f"Liste indiriliyor: {github_raw_url}")
    
    try:
        response = requests.get(github_raw_url)
        if response.status_code == 200:
            lines = response.text.splitlines()
            print(f"Liste indirildi, {len(lines)} satır bulundu.")
            
            new_lines = []
            for line in lines:
                line = line.strip()
                if "vavoo.to" in line and ".m3u8" in line:
                    base_url = line.split('?auth=')[0]
                    new_lines.append(f"{base_url}?auth={token}")
                else:
                    new_lines.append(line)
            
            # DOSYA YAZMA İŞLEMİ
            file_path = "playlist.m3u"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(new_lines))
            
            # Dosyanın oluştuğunu doğrula
            if os.path.exists(file_path):
                print(f"BAŞARILI: {file_path} dosyası oluşturuldu. Boyut: {os.path.getsize(file_path)} byte")
            else:
                print("HATA: Dosya yazıldı dendi ama klasörde bulunamadı!")
                
        else:
            print(f"HATA: Liste indirilemedi! HTTP Kodu: {response.status_code}")
    except Exception as e:
        print(f"Liste güncellenirken hata oluştu: {e}")

if __name__ == "__main__":
    update_playlist()
    
