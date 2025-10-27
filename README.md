# Trendyol Fiyat Karşılaştırma Uygulaması

Bu proje, **Trendyol** üzerindeki ürünlerin fiyatlarını otomatik olarak toplayan ve karşılaştırmalı bir tablo şeklinde gösteren web tabanlı bir uygulamadır.  
Kullanıcıdan alınan ürün linki aracılığıyla **tüm satıcıların fiyat, kargo bilgisi ve puanları** dinamik olarak analiz edilir.  
Sonuçlar web arayüzünde görüntülenir ve CSV olarak indirilebilir.

---

## Özellikler
-  **Otomatik Veri Toplama (Web Scraping):**  
  Selenium ile dinamik sayfa içeriğini çeker, BeautifulSoup ile satıcı verilerini ayrıştırır.  
-  **Fiyat Karşılaştırması:**  
  Tüm satıcıların fiyat, puan ve kargo bilgilerini tablo halinde gösterir.  
-  **CSV Dışa Aktarma:**  
  Kullanıcı, tek tuşla tabloyu `urunler.csv` olarak indirebilir.  
-  **Web Arayüzü:**  
  Flask tabanlı, sade ve mobil uyumlu bir arayüz (Bootstrap 5).

---

##  Kullanılan Teknolojiler
- **Python 3.9+**
- **Flask** – Web arayüzü için  
- **Selenium** – Dinamik içerik çekimi  
- **BeautifulSoup4 (bs4)** – HTML ayrıştırma  
- **Pandas** – Veri işleme ve CSV kaydı  
- **Bootstrap 5** – Arayüz tasarımı  

---

##  Kurulum ve Çalıştırma

### 1️. Gerekli kütüphaneleri yükle
```bash
pip install flask selenium beautifulsoup4 pandas webdriver-manager
```

### 2️. Proje dizin yapısı
```
trendyol-fiyat-karsilastirma
 ┣  app.py                   # Flask web uygulaması
 ┣  web.py                   # Veri çekme ve analiz kodları
 ┣  urun_fiyat_karsilastirma.csv   # Örnek çıktı dosyası
 ┗  templates / static (opsiyonel)  # Web sayfa içeriği
```

### 3️. Uygulamayı başlat
```bash
python app.py
```
Tarayıcıda şu adresi aç: http://127.0.0.1:5000
 
## Kullanım

- Uygulamayı çalıştır.
- Açılan sayfada Trendyol ürün linkini gir.
- “Verileri Getir” butonuna tıkla.
- Tüm satıcıların fiyatları tablo olarak listelenecek.
-İstersen tabloyu CSV olarak indirebilirsin.

| Satıcı Adı     | Fiyat   | Kargo Bilgisi  | Satıcı Puanı | Ürün Puanı |
| -------------- | ------- | -------------- | ------------ | ---------- |
| Trendyol       | 999.90  | Ücretsiz Kargo | 9.8          | 4.7        |
| ABC Elektronik | 1015.00 | 1 Gün İçinde   | 9.4          | 4.7        |
| XYZ Store      | 1029.99 | Ücretsiz Kargo | 9.6          | 4.7        |


Developer: Sedanur Peker
