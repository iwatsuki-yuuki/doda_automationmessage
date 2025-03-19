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

# ★【修正】以下の「ヘッドハンター選択」待機・クリック処理は削除
# （ヘッドハンター選択画面がなくなったため）

# 代わりに、ログイン後にすぐ表示されるメイン画面の要素を待機
candidate_search_header_xpath = '//nav[@id="g-nav"]//a[@href="/member_search/"]'
candidate_search_header = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.XPATH, candidate_search_header_xpath))
)
print("ログイン後のメイン画面に遷移しました。")

# 「候補者検索」にマウスをホバーしてサブメニュー「検索条件リスト」をクリック
ActionChains(driver).move_to_element(candidate_search_header).perform()
time.sleep(1)

search_condition_list_xpath = '//li[@class="g-nav-sub-item"]/a[@href="/search_list/"]'
search_condition_list_link = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, search_condition_list_xpath))
)
search_condition_list_link.click()

# 「検索条件リスト」ページを待機
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "検索条件リスト")]'))
)
print("検索条件リスト画面に遷移しました。")

# ▼【追加】「表示」ボタンをクリックして候補者一覧ページへ遷移
show_button_xpath = '//p[@class="btn-light-s btn-size-l" and normalize-space(text())="表示"]'
show_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, show_button_xpath))
)

# 念のためスクロールしてクリック
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", show_button)
time.sleep(1)
driver.execute_script("arguments[0].click();", show_button)

# 候補者一覧ページの要素待機 (例: 「候補者検索結果」というタイトルを待つ)
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "候補者検索結果")]'))
)
print("「表示」ボタンをクリックし、候補者一覧ページに遷移しました。")

# 一番上の会社名をクリック
top_company_xpath = '(//div[@id="search-result-list"]//span[@class="company-name"])[1]'
top_company_element = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, top_company_xpath))
)
driver.execute_script("arguments[0].scrollIntoView({block: " 
                      "'center'});", top_company_element)
time.sleep(1)
driver.execute_script("arguments[0].click();", top_company_element)
print("一番上の会社名をクリックしました。")

# 「スカウトを作成」ボタンをクリック
scout_button_xpath = '//button[contains(normalize-space(text()), "スカウトを作成")] | //a[contains(normalize-space(text()), "スカウトを作成")]'
scout_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, scout_button_xpath))
)
driver.execute_script("arguments[0].scrollIntoView({block: " 
                      "'center'});", scout_button)
time.sleep(1)
driver.execute_script("arguments[0].click();", scout_button)
print("『スカウトを作成』ボタンをクリックしました。")

# 必要に応じて次の画面の要素待機などを追加

# -----------------------------
# 最後、処理を確認するため一時停止
# -----------------------------
input("ブラウザを閉じずに表示を続けます。終了するには何かキーを押してください...")
