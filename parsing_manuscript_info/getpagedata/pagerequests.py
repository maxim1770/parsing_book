import os

import requests

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Is-Ajax-Request": "X-Is-Ajax-Request",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
}


class PageRequests:

    def __init__(self, url, headers=None):
        self.requests = None

        self.url = url
        self.headers = headers

        self.create_requests()

    def create_requests(self):
        self.requests = requests.get(url=self.url, headers=self.headers)

    def get_src(self):
        return self.requests.text

    def get_src_to_file(self, path):
        """тут скорее всего ошибка, почему этот класс должен это делать?
        Нарушается принцып единственной ответсвеностии
        """
        with open(f'{path}', "w", encoding="utf-8") as file:
            file.write(self.get_src())

    def exception_handling(self):
        if self.requests.status_code != 200:
            pass


def main():
    req = PageRequests(url="https://kp.rusneb.ru/item/material/evangelie-uchitelnoe-licevoe",
                       )

    print(req.get_src())

    if not os.path.exists("../data"):
        os.mkdir("../data")

    req.get_src_to_file("data/index_copy_second.html")


if __name__ == "__main__":
    main()
