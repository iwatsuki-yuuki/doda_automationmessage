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

# メールアドレス入力
email_xpath = '//input[@placeholder="メールアドレス（半角英数字）"]'
email_field = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.XPATH, email_xpath))
)
email_field.send_keys(email)

# パスワード入力
password_xpath = '//input[contains(@placeholder,"パスワード（半角英大小文字")]'
password_field = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.XPATH, password_xpath))
)
password_field.send_keys(password)

# ログインボタンをクリック
login_button_xpath = '//button[contains(text(), "同意してログイン")]'
login_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, login_button_xpath))
)
login_button.click()

# ヘッドハンター選択画面が表示されるまで待機
headhunter_screen_xpath = '//h1[contains(text(), "ヘッドハンター選択")]'
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, headhunter_screen_xpath))
)

# XPath: スペースの違いを吸収するために normalize-space() と contains() を併用
headhunter_xpath = (
    '//ul[@class="account-list"]/li['
    '  p[@class="strong-txt"]/span['
    '    contains(normalize-space(text()), "中野") '
    '    and '
    '    contains(normalize-space(text()), "智貴")'
    '  ]'
    ']'
)

# 要素がクリック可能になるまで待機
headhunter_li_element = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, headhunter_xpath))
)

# 念のため画面中央へスクロールしてからJSクリック
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", headhunter_li_element)
time.sleep(1)
driver.execute_script("arguments[0].click();", headhunter_li_element)

# クリック後の画面遷移待ち（例：候補者検索ページへのリンクが表示されるまで）
candidate_search_header_xpath = '//nav[@id="g-nav"]//a[@href="/member_search/"]'
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, candidate_search_header_xpath))
)

print("中野 智貴 を選択し、次のページへ遷移しました。")

# ▼ここで待機させる (好きな方法を選択)

# 方法1: キー入力待ちで停止する
input("ブラウザを閉じずに表示を続けます。終了するには何かキーを押してください...")

# 方法2: 長時間スリープで停止する (例: 1000秒待機)
# time.sleep(1000)