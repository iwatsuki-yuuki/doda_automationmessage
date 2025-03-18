from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

url = "https://search.doda-x.jp/login/"
driver.get(url)

email = "tnakano@masterkey-inc.com"
password = "Masterkey1322"

# メールアドレス入力欄（確実に要素を待機）
email_xpath = '//input[@placeholder="メールアドレス（半角英数字）"]'
email_field = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.XPATH, email_xpath))
)
email_field.send_keys(email)

# パスワード入力欄（確実に要素を待機）
password_xpath = '//input[contains(@placeholder,"パスワード（半角英大小文字")]'
password_field = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.XPATH, password_xpath))
)
password_field.send_keys(password)

# 同意してログインボタンをクリック
login_button_xpath = '//button[contains(text(), "同意してログイン")]'
login_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, login_button_xpath))
)
login_button.click()

# 次画面（ヘッドハンター選択）を待つ
headhunter_xpath = '//div[contains(text(), "ヘッドハンターを選択")]'
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, headhunter_xpath))
)

# ヘッドハンター「中野智貴」を選択する
headhunter_name = "中野智貴"
headhunter_select_xpath = f'//div[contains(text(), "{headhunter_name}")]'
headhunter_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, headhunter_select_xpath))
)
headhunter_button.click()

time.sleep(3)