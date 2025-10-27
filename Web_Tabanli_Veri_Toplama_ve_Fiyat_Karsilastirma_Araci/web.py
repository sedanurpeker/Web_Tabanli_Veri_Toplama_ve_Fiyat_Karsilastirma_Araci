import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_dynamic_html_content(url):
    """
    Selenium kullanarak dinamik HTML içeriğini çeker ve döndürür.
    "Diğer Satıcıları Göster" butonunu tıklayarak modalı açmaya çalışır.
    """
    driver = None
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        print("INFO: Chrome driver başarıyla başlatıldı.")
        print(f"INFO: URL'ye erişiliyor: {url}")
        
        driver.get(url)
        wait = WebDriverWait(driver, 20)
        
        button_clicked = False
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-title")))
            
            print("INFO: 'Tüm Satıcıları Göster' butonunu bulmaya çalışıyor...")
            
            # Farklı buton varyasyonlarını dene
            button_selectors = [
                (By.XPATH, "//button[contains(@data-testid, 'show-more-button')]"),
                (By.XPATH, "//div[contains(text(), 'TÜM SATICILARI GÖSTER')]/ancestor::button"),
                (By.XPATH, "//div[contains(text(), 'TÜMÜNÜ GÖR')]/ancestor::button"),
                (By.XPATH, "//a[contains(text(), 'Tüm Satıcıları Gör')]")
            ]
            
            for selector_type, selector_value in button_selectors:
                try:
                    all_sellers_button = wait.until(EC.element_to_be_clickable((selector_type, selector_value)))
                    driver.execute_script("arguments[0].click();", all_sellers_button)
                    print("INFO: 'Tüm Satıcıları Göster' butonu başarıyla tıklandı.")
                    button_clicked = True
                    break
                except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
                    continue
        
        except Exception as e:
            print(f"Hata: Buton arama veya tıklama sırasında bir hata oluştu: {e}")
        
        if button_clicked:
            try:
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_modal-body_366d7ce")))
                print("INFO: 'Diğer Satıcılar' modalı başarıyla yüklendi.")
            except TimeoutException:
                print("Uyarı: Modal yüklenemedi. Sayfa yapısı değişmiş olabilir.")
        else:
            print("Uyarı: Hiçbir butona tıklanamadı. Sadece sayfadaki satıcı bilgileri toplanacak.")
            
        time.sleep(3)
        html_content = driver.page_source
        return html_content
    except Exception as e:
        print(f"URL'ye erişim hatası: {e}")
        return None
    finally:
        if driver:
            print("INFO: Driver kapatıldı.")
            driver.quit()

def parse_trendyol(soup):
    """
    Trendyol ürün sayfasından satıcı bilgilerini ayrıştırır.
    Farklı sayfa yapılarını (modal veya doğrudan sayfa listesi) dikkate alır.
    """
    sellers_data = []

    # Ürünün genel puanını çek
    product_rating_elem = soup.find('span', class_='reviews-summary-average-rating')
    product_rating = product_rating_elem.text.strip() if product_rating_elem else "Puan yok"

    # --- ANA SATICI ---
    try:
        main_price_elem = soup.find('span', class_='discounted') or soup.find('span', class_='prc-dsc') or soup.find('div', class_='prc-box-prc-dsc') or soup.find('div', class_='price-current-price')
        main_price = main_price_elem.text.strip() if main_price_elem else "0 TL"
        
        main_seller_name_elem = soup.find('div', class_='merchant-name') or soup.find('a', class_='seller-container-info-name')
        main_seller_name = main_seller_name_elem.text.strip() if main_seller_name_elem else "Bilinmeyen Satıcı"
        
        main_seller_rating_elem = soup.find('div', class_='score-badge') or soup.find('span', class_='seller-container-info-score-text')
        main_seller_rating = main_seller_rating_elem.text.strip() if main_seller_rating_elem else "Puan yok"

        cargo_info_elem = soup.find('div', class_='title', attrs={'data-testid': 'promotion-title'})
        cargo_info = cargo_info_elem.text.strip() if cargo_info_elem else "Kargo bilgisi yok"

        sellers_data.append({
            "Satıcı Adı": main_seller_name,
            "Fiyat": main_price,
            "Kargo Bilgisi": cargo_info,
            "Satıcı Puanı": main_seller_rating,
            "Ürün Puanı": product_rating
        })
    except Exception as e:
        print(f"Ana satıcı verisi çekilirken hata oluştu: {e}")

    # --- DİĞER SATICILAR - MODAL VEYA SAYFA İÇİ LİSTE ---
    found_sellers = False
    
    # Strateji 1: Modal içindeki satıcılar
    modal_container = soup.find('div', class_='_modal-body_366d7ce')
    if modal_container:
        seller_items = modal_container.find_all('div', class_='other-merchant-item-box') or modal_container.find_all('div', class_='seller-card')
        for item in seller_items:
            found_sellers = True
            try:
                seller_name = (item.find('a', class_='merchant-header-name') or item.find('div', class_='merchant-header-name') or item.find('div', class_='merchant-name')).text.strip()
                price = (item.find('div', class_='price-current-price') or item.find('div', class_='price-box-price-box')).text.strip()
                cargo_info = (item.find('div', class_='other-merchant-delivery-container') or item.find('div', class_='delivery-detail')).text.strip()
                rating = (item.find('span', class_='seller-score') or item.find('div', class_='merchant-header-seller-score') or item.find('div', class_='score-badge')).text.strip()
                
                sellers_data.append({"Satıcı Adı": seller_name, "Fiyat": price, "Kargo Bilgisi": cargo_info, "Satıcı Puanı": rating, "Ürün Puanı": product_rating})
            except:
                continue

    # Strateji 2: Sayfa içindeki dikey liste
    side_sellers_section = soup.find('div', class_='side-other-seller-container')
    if side_sellers_section:
        seller_items = side_sellers_section.find_all('div', class_='other-seller-item-total-container')
        for item in seller_items:
            found_sellers = True
            try:
                seller_name = (item.find('a', class_='other-seller-header-merchant-name') or item.find('div', class_='other-seller-header-merchant-name')).text.strip()
                price = (item.find('div', class_='price-current-price') or item.find('span', class_='prc-dsc')).text.strip()
                cargo_info = (item.find('div', class_='side-other-seller-delivery-container') or item.find('div', class_='other-merchant-delivery-container')).text.strip()
                rating = (item.find('div', class_='other-seller-header-seller-score')).text.strip()
                
                sellers_data.append({"Satıcı Adı": seller_name, "Fiyat": price, "Kargo Bilgisi": cargo_info, "Satıcı Puanı": rating, "Ürün Puanı": product_rating})
            except:
                continue

    # Strateji 3: Sayfa içindeki yatay (slider) liste
    slider_sellers_section = soup.find('div', class_='other-merchants')
    if slider_sellers_section:
        seller_items = slider_sellers_section.find_all('div', class_='other-merchant-item-box')
        for item in seller_items:
            found_sellers = True
            try:
                seller_name = (item.find('a', class_='merchant-header-name') or item.find('div', class_='merchant-header-name')).text.strip()
                price = (item.find('div', class_='price-current-price') or item.find('span', class_='prc-dsc')).text.strip()
                cargo_info = (item.find('div', class_='other-merchant-delivery-container')).text.strip()
                rating = (item.find('div', class_='merchant-header-seller-score')).text.strip()
                
                sellers_data.append({"Satıcı Adı": seller_name, "Fiyat": price, "Kargo Bilgisi": cargo_info, "Satıcı Puanı": rating, "Ürün Puanı": product_rating})
            except:
                continue

    if not found_sellers and len(sellers_data) <= 1:
        print("Uyarı: Sayfada veya modalda satıcı listesi bulunamadı. Sınıf adları değişmiş olabilir.")
            
    return sellers_data

def process_data(data):
    """
    Toplanan veriyi temizler ve analiz için hazırlar.
    """
    df = pd.DataFrame(data)
    df['Fiyat'] = df['Fiyat'].str.replace(' TL', '').str.replace('₺', '').str.replace('.', '').str.replace(',', '.').astype(float)
    df['Satıcı Puanı'] = df['Satıcı Puanı'].str.replace(' ', '').str.replace(',', '.')
    df['Satıcı Puanı'] = pd.to_numeric(df['Satıcı Puanı'].apply(
        lambda x: x.split('/')[0] if '/' in str(x) else x
    ), errors='coerce').fillna(0)
    df['Ürün Puanı'] = pd.to_numeric(df['Ürün Puanı'].str.replace(',', '.'), errors='coerce').fillna(0)
    return df

def analyze_and_report(df, output_filename='urun_fiyat_karsilastirma.csv'):
    """
    Veriyi analiz eder, raporlar ve CSV olarak kaydeder.
    """
    if df.empty:
        print("Analiz edilecek veri bulunamadı.")
        return
    
    df = df.drop_duplicates(subset=['Satıcı Adı', 'Fiyat']).reset_index(drop=True)
    df.to_csv(output_filename, index=False, encoding='utf-8-sig')
    print(f"Veriler '{output_filename}' dosyasına kaydedildi.")
    
    print("\n" + "="*50)
    
    if len(df) <= 1:
        print("Sadece bir satıcı bilgisi bulundu.")
        print("="*50)
        print(df.to_string(index=False))
    else:
        print("--- En Ucuz 5 Ürün ---")
        print("="*50)
        cheapest_products = df.sort_values(by='Fiyat', ascending=True).head(5)
        print(cheapest_products.to_string(index=False))
        
        print("\n" + "="*50)
        print("--- En Pahalı 5 Ürün ---")
        print("="*50)
        most_expensive_products = df.sort_values(by='Fiyat', ascending=False).head(5)
        print(most_expensive_products.to_string(index=False))

def main():
    """
    Ana fonksiyon: Kullanıcıdan URL alır ve tüm süreci yönetir.
    """
    print("🛒 GELİŞMİŞ WEB TABANLI VERİ TOPLAMA VE FİYAT KARŞILAŞTIRMA ARACI")
    print("="*80)
    
    url = input("Lütfen Trendyol ürün URL'sini girin: ").strip()
    
    if not url:
        print("URL girmediniz. Program sonlandırılıyor.")
        return
    
    html_content = get_dynamic_html_content(url)
    if not html_content:
        return
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    product_name_elem = soup.find('h1', class_='product-title')
    product_name = product_name_elem.text.strip() if product_name_elem else "Bilinmeyen Ürün"
    
    scraped_data = parse_trendyol(soup)

    if not scraped_data:
        print("Veri toplama başarısız oldu. Lütfen URL'yi kontrol edin veya sitenin yapısı değişmiş olabilir.")
        return
    
    for item in scraped_data:
        item['Ürün Adı'] = product_name
    
    df_processed = process_data(scraped_data)
    df_processed = df_processed[['Ürün Adı', 'Satıcı Adı', 'Fiyat', 'Kargo Bilgisi', 'Satıcı Puanı', 'Ürün Puanı']]
    
    analyze_and_report(df_processed)

if __name__ == "__main__":
    main()