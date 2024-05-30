import os
import math
import time
import datetime
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

def process_data(url, id_value, keyword_value, date):
    # 入力された情報を表示
    print(f"URL:{url}")
    print(f"ID:{id_value}")
    print(f"トリップ: {keyword_value}")
    print(f"日付: {date}")
    
    # 日付文字列を日付オブジェクトに変換
    dateget = datetime.strptime(date, "%Y%m%d").date()
    
    # 現在の日付を取得
    current_date = datetime.now().date()
    
    # 日数の差分を計算
    datediff = (current_date - dateget).days
    print(f"日数の差分: {datediff} 日")

    ## URL指定
    URL = url

    ## headless モードでChrome起動
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--hide-scrollbars')
    options.add_argument('--window-size=760,1055')
    options.add_argument('--log-level=3') # コンソールログ非表示
    options.add_argument('--ignore-certificate-errors') ## 他では使用しない
    driver = webdriver.Chrome(options=options) 

    ## 指定URLに画面遷移
    driver.get(URL)

    # ドロップダウンメニューの操作
    dropdown = driver.find_elements(By.NAME, "date")
    if dropdown:  # リストが空でない場合
        select_dropdown = dropdown[1]
        select = Select(select_dropdown)
        select.select_by_index(datediff)

    # 検索ボックスへの入力
    search_box = driver.find_element(By.NAME, "Trip")
    search_box.send_keys(keyword_value)

    # 検索ボタンの操作
    search_btn = driver.find_element(By.XPATH,"/html/body/table/tbody/tr/td/table/tbody/tr[3]/td[2]/form/input[3]")
    value_attribute = search_btn.get_attribute("value")
    print("検索ボタン名：", value_attribute)
    time.sleep(10)
    search_btn.click()

    # 現在のページの URL 取得
    current_url = driver.current_url
    print("現在のページのURL:", current_url)

    # ページ内のリンクのリスト取得
    href_attributes_list = []
    search_links = driver.find_elements(By.TAG_NAME,"a")
    number_of_links = len(search_links)
    print("number：", number_of_links)
    if number_of_links == 1:
        print("書き込みなし")
        print("取得したhref属性のリスト:", href_attributes_list)
    else:
        for link in search_links:
            href_attribute = link.get_attribute("href")
            href_attributes_list.append(href_attribute)
            print("現在のページのリンク先URL", href_attribute)
        print("取得したhref属性のリスト:", href_attributes_list[0:number_of_links-1])

    ## 10秒待機
    time.sleep(10)

    ## ブラウザを閉じる
    driver.quit() 

    return href_attributes_list