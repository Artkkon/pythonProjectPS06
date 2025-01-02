import scrapy
import csv


class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/novosibirsk/category/svet"]

    def __init__(self):
        # Открываем CSV файл для записи и создаем объект writer
        self.file = open("hh.csv", "w", newline="", encoding="utf-8")
        self.writer = csv.writer(self.file)
        # Записываем заголовок файла
        self.writer.writerow(["Название", "Цена", "Ссылка"])

    def parse(self, response):
        svets = response.css("div._Ud0k")
        for svet in svets:
            item = {
                "name": svet.css("div.lsooF span::text").get(),
                "price": svet.css("div.q5Uds span::text").get(),
                "link": response.urljoin(svet.css("a").attrib["href"]),
            }
            # Записываем строку в CSV
            self.writer.writerow([item["name"], item["price"], item["link"]])
            yield item

    def close(self, reason):
        # Закрываем файл при завершении работы паука
        self.file.close()
