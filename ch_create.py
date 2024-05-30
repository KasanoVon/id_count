# ch_create.py

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import ch_url  # ch_url モジュールをインポート

def process_href_attributes_list(href_attributes_list):
    href_ends_with_1_list = []
    results = []

    if not href_attributes_list:
        total = 0
    else:
        href_a = len(href_attributes_list[0:-1])
        total = 0

        for i in range(href_a):
            url = href_attributes_list[i]
            
            while True:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                tables = soup.find_all("table")
                
                try:
                    target_table = tables[5]
                except IndexError:
                    print("テーブルが見つかりませんでした")
                    break

                td_tags = target_table.find_all("a")

                for a_tag in td_tags:
                    href_value = a_tag.get('href')
                    print(f'URL: {url}, Href: {href_value}')
                    
                    if href_value and href_value.endswith("/1"):
                        href_value = href_value[:-2]
                        href_ends_with_1_list.append(href_value)
                        print(f'URL: {url}, スレ立てフラグ: {href_value}') 
                        total += 1

                next_page_a_tag = soup.find("a", string="次へ>>")
                if next_page_a_tag:
                    print("次へリンクがみつかりました")  
                    next_page_href = next_page_a_tag.get('href')
                    url = urljoin(url, next_page_href)
                    print(next_page_href)
                else:
                    print("次へリンクはありませんでした")
                    break

    print("スレ立て数：", total)
    print("hrefが'/1'で終わるリスト：", href_ends_with_1_list)

    for url in href_ends_with_1_list:
        thread_titles = []
        unique_ids = set()
        total_res = 0

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        thread_title_tag = soup.find(id="threadtitle")
        if thread_title_tag:
            thread_title = thread_title_tag.text.strip()
            thread_titles.append(thread_title)

        id_tags = soup.find_all(class_="uid")
        for tag in id_tags:
            unique_ids.add(tag.text.strip())

        res_tags = soup.find_all(class_="postid")
        total_res += len(res_tags)

        print("URL：", url)
        print("スレタイ：", thread_titles)
        print("ID数：", len(unique_ids))
        print("レス数：", total_res)
        print()

        results.append((url, thread_titles, len(unique_ids), total_res))

    return results

if __name__ == "__main__":
    href_attributes_list = ch_url.process_data("example_url", "example_id", "example_keyword", "20230501")
    process_href_attributes_list(href_attributes_list)
