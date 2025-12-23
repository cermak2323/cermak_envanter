"""
Bu script PC'nin ağ IP adresini gösterir.
Telefon ve diğer cihazlardan erişim için bu IP'yi kullan.
"""

import socket
import subprocess
import platform

def get_local_ip():
    """Yerel ağ IP adresini al"""
    try:
        # Geçici bir socket oluştur (gerçekten bağlanmaz)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return None

def get_all_ips_windows():
    """Windows'ta tüm network interface IP'lerini göster"""
    try:
        result = subprocess.run(
            ['ipconfig'], 
            capture_output=True, 
            text=True,
            encoding='cp1254'  # Türkçe karakterler için
        )
        return result.stdout
    except Exception as e:
        return f"Hata: {e}"

def main():
    print("=" * 70)
    print("🌐 NETWORK IP ADRESİ - TELEFON BAĞLANTISI İÇİN")
    print("=" * 70)
    print()
    
    # Ana IP adresini göster
    local_ip = get_local_ip()
    
    if local_ip:
        print(f"✅ Telefondan/Diğer Cihazlardan Bağlanmak İçin:")
        print()
        print(f"   🔗 http://{local_ip}:5002")
        print()
        print(f"📱 TELEFON AYARLARI:")
        print(f"   1. Telefonu WiFi'ye bağla (PC ile aynı ağ)")
        print(f"   2. Tarayıcıda aç: http://{local_ip}:5002")
        print(f"   3. Giriş yap ve QR okut!")
        print()
    else:
        print("⚠️  IP adresi otomatik bulunamadı.")
        print()
    
    # Windows'ta detaylı bilgi
    if platform.system() == "Windows":
        print("=" * 70)
        print("📋 TÜM NETWORK AYARLARI (IPv4 Adreslerine Bakın):")
        print("=" * 70)
        print()
        ipconfig_output = get_all_ips_windows()
        
        # IPv4 satırlarını highlight et
        lines = ipconfig_output.split('\n')
        for line in lines:
            if 'IPv4' in line or 'IP Address' in line:
                print(f">>> {line.strip()}")
            elif line.strip() and not line.startswith(' ' * 6):
                print(line)
        print()
    
    # Firewall uyarısı
    print("=" * 70)
    print("🔥 FIREWALL AYARI GEREKLİ!")
    print("=" * 70)
    print()
    print("PowerShell'i YÖNETİCİ OLARAK aç ve çalıştır:")
    print()
    print('New-NetFirewallRule -DisplayName "Flask EnvanterQR" -Direction Inbound -Protocol TCP -LocalPort 5002 -Action Allow -Profile Private,Domain')
    print()
    print("=" * 70)
    print()
    
    # QR Kod öneri
    if local_ip:
        print("💡 İPUCU: QR Kod Oluştur!")
        print()
        print(f"   URL: http://{local_ip}:5002")
        print(f"   Site: https://www.qr-code-generator.com")
        print(f"   QR'u yazdır ve depoya as, telefonla okut → direkt giriş!")
        print()
    
    print("✅ Flask'ı başlat: python app.py")
    print()

if __name__ == "__main__":
    main()
