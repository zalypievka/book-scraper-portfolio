import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# 1. Добавляем "Умные ожидания" (Wait)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

file = open('mystery_full_details.csv', 'w', newline='', encoding='utf-8-sig')
writer = csv.writer(file)
writer.writerow(['Название', 'Цена', 'Описание'])

options = Options()
# Вставляем библиотеку random User-Agent (если установил), или оставляем твою строку
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless")  # Если не нужен браузер на экране

driver = webdriver.Chrome(options=options)
driver.get("http://books.toscrape.com/catalogue/category/books/mystery_3/index.html")

# 2. Ждем, пока прогрузятся ссылки (максимум 10 сек)
# Вместо time.sleep()
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h3/a"))
    )
except:
    print("Страница не загрузилась!")
    driver.quit()

link_elements = driver.find_elements(By.XPATH, "//h3/a")
all_urls = []
for item in link_elements:
    url = item.get_attribute("href")
    all_urls.append(url)

print(f"Собрано ссылок: {len(all_urls)}")

for link in all_urls:
    print(f"Парсим: {link}")
    driver.get(link)
    
    try:
        # 3. Внутри карточки тоже ждем, пока появится заголовок
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1"))
        )

        title = driver.find_element(By.XPATH, "//h1").text
        price = driver.find_element(By.XPATH, ".//p[@class='price_color']").text
        description = driver.find_element(By.XPATH, "//div[@id='product_description']/following-sibling::p").text
        
        writer.writerow([title, price, description])
        
    except Exception as e:
        print(f"Ошибка: {e}")
        continue

driver.quit()
file.close()