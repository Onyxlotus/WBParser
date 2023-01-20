from bs4 import BeautifulSoup
import undetected_chromedriver
import pandas as pd
import json
import time


def wildberries(url):
    options = undetected_chromedriver.ChromeOptions()

    driver = undetected_chromedriver.Chrome(
        executable_path="./config/chromedriver",
        options=options
    )

    try:
        driver.get(url)
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        html = driver.page_source
        with open("main.html", "w", encoding='utf-8') as f:
            f.write(html)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def my_soup():
    save_product = {}
    with open("main.html", "r", encoding='utf-8') as f:
        file = f.read()
    soup = BeautifulSoup(file, "lxml")
    all_product = soup.find_all(class_="market_row")

    for t, i in enumerate(all_product):
        name = i.find('div', class_="market_row_name").get_text()
        brand = i.find('span', class_="market-item-price").get_text()
        link = i.find("img", class_="market_row_img")['src']

        save_product[t] = {
            "цена": brand,
            "Название": name,

            "Ссылка на фото": link,

        }

    with open('data.json', 'w', encoding='utf8') as outfile:
        json.dump(save_product, outfile, indent=4, ensure_ascii=False)


def parse():
    result_list = {'Название': [], 'Цена': [], 'Ссылка на фото': []}
    with open("main.html", "r", encoding='utf-8') as f:
        file = f.read()
    soup = BeautifulSoup(file, "lxml")
    xname = soup.find_all(class_="market_row_name")
    brand = soup.find_all(class_="market-item-price")
    link = soup.find("img", class_="market_row_img")['src']

    for name in xname:
        result_list['Название'].append(name.text)
    for name in brand:
        result_list['Цена'].append(name.text)
    for name in link:
        result_list['Ссылка на фото'].append(name.text)
    return result_list


if __name__ == '__main__':
    my_url = "https://vk.com/market-202261956"
    wildberries(my_url)
    df = pd.DataFrame(data=parse())
    df.to_excel("data.xlsx")
    my_soup()

