import os
import datetime
import time
import json
import csv
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 Safari/537.36"
}


def get_first_page_with_selenium():
    if not os.path.exists("data_rusneb/elizavetgradskoe-evangelie-licevoe/index_with_selenium.html"):

        options = webdriver.ChromeOptions()

        options.add_argument(f"user-agent={headers}")

        try:
            driver = webdriver.Chrome(
                executable_path=r"C:\Users\MaxDroN\Desktop\python_projects\python_selenium_learn\learn_1\сhromedriver\chromedriver.exe",
                options=options
            )

            driver.get(
                url="https://kp.rusneb.ru/item/reader/elizavetgradskoe-evangelie-licevoe")

            time.sleep(20)

            with open("data_rusneb/elizavetgradskoe-evangelie-licevoe/index_with_selenium.html", "w", encoding="utf-8") as file:
                file.write(driver.page_source)


        except Exception as ex:
            print(ex)

        finally:
            driver.close()
            driver.quit()


def get_images_links_with_selenium():
    with open("data_rusneb/elizavetgradskoe-evangelie-licevoe/index_with_selenium.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    items_data_images_links = soup.find('div', class_="main-right-side").find('div', class_="panel").find_all('div',
                                                                                                              class_='preview')

    data_images_links = []

    for item_image_link in items_data_images_links:
        image_thumb_size_link = 'https://kp.rusneb.ru' + item_image_link.find("img")["data-src"]

        image_preview_size_link = image_thumb_size_link.replace('thumb', 'preview')

        image_number = int(item_image_link.text)

        data_images_links.append((image_number, image_preview_size_link))

    return data_images_links


def collect_all_data(data_images_links: list):
    if not os.path.exists("data_rusneb/elizavetgradskoe-evangelie-licevoe/images_rusneb_elizavetgradskoe-evangelie-licevoe"):
        os.mkdir("data_rusneb/elizavetgradskoe-evangelie-licevoe/images_rusneb_elizavetgradskoe-evangelie-licevoe")

    for image_link in data_images_links:

        time.sleep(1)

        req = requests.get(image_link[1], headers, stream=True)

        if req.status_code != 200:
            print(f'[Error {req.status_code}] Страница № {image_link[0]}, url: {image_link[1]}')
            continue

        else:

            if not os.path.exists(
                    f"data_rusneb/elizavetgradskoe-evangelie-licevoe/images_rusneb_elizavetgradskoe-evangelie-licevoe/image_rusneb_{image_link[0]}.jpg"):

                # download_image
                with open(
                        f"data_rusneb/elizavetgradskoe-evangelie-licevoe/images_rusneb_elizavetgradskoe-evangelie-licevoe/image_rusneb_{image_link[0]}.jpg",
                        'wb') as file:
                    for chunk in req.iter_content(chunk_size=1024):  # 1 байт
                        if chunk:
                            file.write(chunk)
                        else:
                            print('error chunk in:', image_link[0])
                            print(f'url: {image_link[1]}')
                            print('-' * 10)

                print(f"Страница {image_link[0]} загружена")
            else:
                print(f"Страница {image_link[0]} уже была загружена")


def main():
    if not os.path.exists("data_rusneb"):
        os.mkdir("data_rusneb")

    if not os.path.exists("data_rusneb/elizavetgradskoe-evangelie-licevoe"):
        os.mkdir("data_rusneb/elizavetgradskoe-evangelie-licevoe")

    get_first_page_with_selenium()

    data_images_links = get_images_links_with_selenium()

    collect_all_data(data_images_links)


if __name__ == "__main__":
    main()
