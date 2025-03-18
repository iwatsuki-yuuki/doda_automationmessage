from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
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

# クリック後の画面遷移待ち（候補者検索リンクが表示されるまで）
candidate_search_header_xpath = '//nav[@id="g-nav"]//a[@href="/member_search/"]'
candidate_search_header = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.XPATH, candidate_search_header_xpath))
)

print("中野 智貴 を選択し、次のページへ遷移しました。")

# -------------------------------------------------
# ▼【重要】「候補者検索」にマウスをホバーし、サブメニュー「検索条件リスト」をクリック
# -------------------------------------------------

# 1) ActionChainsで「候補者検索」にマウスをホバー
ActionChains(driver).move_to_element(candidate_search_header).perform()
time.sleep(1)  # サブメニューが表示されるのを待つ

# 2) 「検索条件リスト」のリンク要素をXPathで特定
search_condition_list_xpath = '//li[@class="g-nav-sub-item"]/a[@href="/search_list/"]'
search_condition_list_link = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, search_condition_list_xpath))
)

# 3) クリック
search_condition_list_link.click()

# 4) 画面遷移を待機（検索条件リスト特有の要素を待つ）
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "検索条件リスト")]'))
)

print("検索条件リスト画面に遷移しました。")

# ▼ここで待機させる (好きな方法を選択)
input("ブラウザを閉じずに表示を続けます。終了するには何かキーを押してください...")
# time.sleep(1000)