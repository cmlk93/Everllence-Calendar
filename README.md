# Modern Android Takvim Uygulaması

Bu uygulama, Python ve Kivy framework'ü kullanılarak geliştirilmiş modern bir takvim uygulamasıdır.

## Özellikler

✅ **Bugünkü tarihle açılır**: Uygulama açıldığında mevcut ay gösterilir
✅ **Bugün belirgin şekilde işaretli**: Mavi arka planla vurgulanır
✅ **Pazartesi başlangıçlı hafta**: Takvim Pazartesi gününden başlar
✅ **Renkli hafta gösterimi**: 
   - 2 Mart 2026 Pazartesi'den başlayarak hafta aşırı kırmızı/yeşil renk
   - Kırmızı haftalar: Hafif kırmızı ton (#FFD9D9)
   - Yeşil haftalar: Hafif yeşil ton (#D9FFD9)
✅ **2030 yılına kadar**: 2030 yılına kadar olan tarihleri gösterir
✅ **Modern ve şık tasarım**: Yuvarlatılmış köşeler, temiz hatlar
✅ **Türkçe dil desteği**: Ay isimleri ve gün kısaltmaları Türkçe

## Gereksinimler

### Geliştirme Ortamı
- Python 3.8 veya üzeri
- pip paket yöneticisi

### Bilgisayarda Test Etmek İçin

```bash
# Gerekli paketleri yükle
pip install -r requirements.txt

# Uygulamayı çalıştır
python calendar_app.py
```

## Android APK Oluşturma

### 🪟 Windows Kullanıcıları İçin

**Detaylı Windows rehberi için**: `WINDOWS_APK_GUIDE.md` dosyasına bakın

**En kolay yöntem - GitHub Actions (Önerilen)**:
1. GitHub hesabı oluşturun
2. Repository oluşturun ve dosyaları yükleyin
3. `.github/workflows/` klasöründe `build.yml` dosyasını oluşturun
4. Otomatik olarak APK oluşturulacak ve indirebileceksiniz

**Alternatif - WSL2**:
```powershell
# PowerShell'de (Yönetici olarak)
wsl --install
# Sonra Ubuntu terminalinde buildozer komutlarını çalıştırın
```

### Linux/Ubuntu için:

```bash
# Sistem gereksinimlerini yükle
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Buildozer'ı yükle
pip install buildozer

# Cython'u yükle
pip install cython

# APK oluştur
buildozer android debug

# APK dosyası şu konumda oluşacak:
# bin/moderncalendar-1.0-arm64-v8a-debug.apk
```

### Windows için:

Windows'ta direkt APK oluşturmak yerine şunları yapabilirsiniz:
1. **WSL2 (Windows Subsystem for Linux)** kullanarak yukarıdaki Linux komutlarını çalıştırın
2. **Google Colab** veya **GitHub Actions** üzerinde build işlemi yapın
3. **Linux sanal makine** kullanın

### macOS için:

```bash
# Homebrew ile gerekli paketleri yükle
brew install python@3.11
brew install autoconf automake libtool pkg-config
brew install cmake

# Buildozer'ı yükle
pip3 install buildozer cython

# APK oluştur
buildozer android debug
```

## APK'yı Android'e Yükleme

APK oluştuktan sonra:

1. APK dosyasını Android cihazınıza kopyalayın
2. Cihazınızda "Bilinmeyen kaynaklardan yükleme" iznini aktifleştirin:
   - Ayarlar → Güvenlik → Bilinmeyen Kaynaklar (etkinleştir)
3. APK dosyasına dokunun ve yükleyin

## Uygulama Kullanımı

- **< ve > butonları**: Önceki/sonraki aya geçiş
- **Mavi arka planlı gün**: Bugünkü tarih (beyaz yazı ile)
- **Renkli günler**: Mevcut ayın günleri
- **Gri günler**: Önceki/sonraki ayın günleri
- **Kırmızı arka plan**: Hafta aşırı haftalar (2 Mart 2026'dan başlayarak)
- **Yeşil arka plan**: Normal haftalar

## Teknik Detaylar

- **Framework**: Kivy 2.3.0
- **Build Tool**: Buildozer 1.5.0
- **Target SDK**: Android API 31
- **Minimum SDK**: Android API 21 (Android 5.0+)
- **Desteklenen Mimariler**: ARM64-v8a, ARMeabi-v7a

## Renk Şeması

- **Bugün**: RGB(51, 102, 204) - #3366CC (Koyu mavi arka plan, beyaz yazı)
- Kırmızı hafta: RGB(255, 217, 217) - #FFD9D9
- Yeşil hafta: RGB(217, 255, 217) - #D9FFD9
- Arka plan: RGB(245, 245, 245) - #F5F5F5
- Mavi butonlar: RGB(77, 153, 230) - #4D99E6

## Sorun Giderme

### APK oluşturma hatası alıyorsanız:
```bash
# Buildozer cache'ini temizle
buildozer android clean

# Tekrar deneyin
buildozer android debug
```

### İlk build çok uzun sürüyor:
- İlk build işlemi Android SDK ve NDK'yı indirdiği için 30-60 dakika sürebilir
- Sonraki build'ler çok daha hızlı olacaktır

## Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## Katkıda Bulunma

Geliştirmeler için pull request gönderebilirsiniz.

---

**Not**: Bu uygulama 2026-2030 yılları arasında çalışacak şekilde tasarlanmıştır. 2 Mart 2026 Pazartesi günü referans tarih olarak kullanılmaktadır.
