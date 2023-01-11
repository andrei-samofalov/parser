import json
import time

from selenium_version.misc.catalog import CatalogItem
from selenium_version.misc.url import CATALOG, URL


def load(bro):
    start_time = time.time()

    with bro as bro:
        final_list = []
        for key in CATALOG.keys():
            current_url = URL.replace('{category}', CATALOG[key])
            print(f'Каталог {key}')
            bro.get(url=current_url)
            catalog_item = CatalogItem(url=current_url)

            page_count = 0
            while not catalog_item.check_for_end():
                page_count += 1
                print(f'  Обрабатывается страница №{page_count}', end='')

                current_time = time.time()
                page_data = catalog_item.parse_page()
                parse_time = time.time()
                print(f'...parse: {round(parse_time - current_time, 3)} сек', end='')

                catalog_item.page_change()
                print(f'...page change: {round(time.time() - parse_time, 3)} сек')
            else:
                data_dict = {key: page_data}
                final_list.append(data_dict)
                with open('log.txt', 'a', encoding='utf-8') as file:
                    file.write(f'Группа {key}; Страниц {page_count}\n')
                    count = 0
                    for elem in page_data:
                        count += 1
                        file.write(f'{count} ')
                        for i, j in elem.items():
                            file.write(f'{i}: {j}; ')
                        else:
                            file.write('\n')
        else:
            with open('data.json', 'w') as file:
                json.dump(final_list, file, indent=4)
    end_time = time.time()

    print(f'Скрипт работал {round((end_time - start_time) / 60, 3)} минут')
