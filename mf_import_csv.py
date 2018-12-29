import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

from datetime import datetime

url = "https://moneyforward.com/accounts/show_manual/xxxxxxxxxxxxxxxxxxxxxx" #銀行のURL
user = "user" #自分のアカウント
password = "password" #自分のパスワード


if len(sys.argv) != 2:
    print("No input_file!")
    print("usage: python mf_import_csv.py data_file.csv")
    sys.exit()
input_file = str(sys.argv[1])

try:
    print("Start :" + input_file)

    #Chromeブラウザを立ち上げる
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)   #wait

    #マネーフォワードの銀行ページに遷移
    driver.get(url)

    #アカウント入力
    elem = driver.find_element_by_id("sign_in_session_service_email")
    elem.clear()
    elem.send_keys(user)

    #パスワード入力
    elem = driver.find_element_by_id("sign_in_session_service_password")
    elem.clear()
    elem.send_keys(password)

    #ログインボダン押す
    elem = driver.find_element_by_id("login-btn-sumit")
    elem.click()


    #CSVファイルを開く、文字コードはUTF-8 sig
    f = open(input_file, mode='r', encoding='utf_8_sig')

    reader = csv.reader(f)
    n = 1;
    for row in reader:
        #input button click
        elem = driver.find_element_by_class_name("cf-new-btn")
        elem.click()

        if int(row[2]) > 0:
            print("[" + str(n) + "] " + "Plus! :")
            print(row)
            amount = int(row[2])

            #click Plus
            elem = driver.find_element_by_class_name("plus-payment")
            elem.click()

        elif int(row[3]) > 0:
            print("[" + str(n) + "] " + "Minus! :")
            print(row)
            amount = int(row[3])

            #click Minus
        else:
            print ("Error row num = " + str(n) + "\n")

        #string to date
        dt = row[0].split(" ")[0]
        dt = datetime.strptime(dt,'%d-%b-%Y')
        str_dt = dt.strftime('%Y/%m/%d')
        elem = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "updated-at"))
        )
        elem.clear()
        elem.send_keys(str_dt)

        #amount
        elem = driver.find_element_by_id("appendedPrependedInput")
        elem.clear()
        elem.send_keys(amount)

        #content with 51 charactor
        content = row[1][0:50]
        elem = driver.find_element_by_id("js-content-field")
        elem.clear()
        elem.send_keys(content)

        #click
        elem = driver.find_element_by_id("submit-button")
        elem.click()

        driver.implicitly_wait(8)   #wait
        driver.get(url)
        driver.implicitly_wait(3)   #wait

        n+=1

    f.close()



finally:
    print("End :" + input_file)
    #driver.quit()

