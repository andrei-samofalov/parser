from selenium.webdriver.common.by import By

from selenium_version.loader import browser


class CatalogItem:
    def __init__(self, url: str) -> None:
        self._url = url
        self.page_read = False
        self.all_done = False
        self.goods = []

    def parse_page(self):
        self.page_read = False
        while not self.page_read:
            products: list = browser.find_elements(By.CLASS_NAME, 'product__title')
            codes: list = browser.find_elements(By.CLASS_NAME, 'product__footer')
            prices: list = browser.find_elements(By.CLASS_NAME, 'product__price__current')

            amount_of_products = len(products)

            for i in range(amount_of_products):
                element = {
                    'Артикул': codes[i].__getattribute__('text').split(': ')[1],
                    'Наименование': products[i].__getattribute__('text').replace('\n', ' '),
                    'Цена': prices[i].__getattribute__('text')
                }
                self.goods.append(element)
            else:
                self.page_read = True

        return self.goods

    def check_for_end(self):
        return self.all_done

    def page_change(self):
        next_page = browser.find_element(By.CLASS_NAME, 'page-link_next')
        next_page_url = next_page.get_attribute('href')
        if not self.all_done:
            try:
                browser.get(next_page_url)
            except:
                self.all_done = True
                pass




