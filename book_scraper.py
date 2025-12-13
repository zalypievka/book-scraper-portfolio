import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options



file=open('mystery_books.csv', 'w', newline='', encoding='utf-8-sig')
writer=csv.writer(file)
writer.writerow(['Название книги','Цена','Наличие'])

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)
driver.get("http://books.toscrape.com/catalogue/category/books/mystery_3/index.html")

books=driver.find_elements(By.XPATH,".//article[@class='product_pod']")
for i, book in enumerate(books, 1):
    full_title = "Нет названия"
    price = "Нет цены"
    availability = "Нет статуса"
    try:
        link = book.find_element(By.XPATH, ".//h3/a")
        full_title = link.get_attribute("title")
    except Exception:
        print(f"Книга №{i}: Не нашел название")
    try:
        price = book.find_element(By.XPATH, ".//p[@class='price_color']").text
    except Exception:
        print(f"Книга №{i} ({full_title}): Не нашел цену")
    try:
        availability = book.find_element(By.XPATH, ".//p[@class='instock availability']").text
    except Exception:
        print(f"Книга №{i} ({full_title}): Не нашел наличие")
    writer.writerow([full_title, price, availability])

driver.quit()
file.close()