from pagerequests import PageRequests
from pageparsing import PageParsing
import os


def main():
    # req = PageRequests(url="https://kp.rusneb.ru/item/material/evangelie-uchitelnoe-licevoe",
    #                    )
    #
    # print(req.get_src())
    #
    # if not os.path.exists("data"):
    #     os.mkdir("data")
    #
    # req.get_src_to_file("data/index_copy_second.html")

    with open("../data/index_copy_second.html", encoding="utf-8") as file:
        src = file.read()

    parsing = PageParsing(src=src)

    parsing.collect_data()
    data = parsing.get_data()

    print(data)

if __name__ == "__main__":
    main()