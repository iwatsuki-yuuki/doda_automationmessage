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

# 「中野 智貴」をクリック
headhunter_xpath = (
    '//ul[@class="account-list"]/li['
    '  p[@class="strong-txt"]/span['
    '    contains(normalize-space(text()), "中野") '
    '    and '
    '    contains(normalize-space(text()), "智貴")'
    '  ]'
    ']'
)
headhunter_li_element = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, headhunter_xpath))
)
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", headhunter_li_element)
time.sleep(1)
driver.execute_script("arguments[0].click();", headhunter_li_element)

# 候補者検索リンクが表示されるまで待機
candidate_search_header_xpath = '//nav[@id="g-nav"]//a[@href="/member_search/"]'
candidate_search_header = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.XPATH, candidate_search_header_xpath))
)
print("中野 智貴 を選択し、次のページへ遷移しました。")

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
driver.execute_script("arguments[0].scrollIntoView({block: " 
                      "'center'});", show_button)
time.sleep(1)
driver.execute_script("arguments[0].click();", show_button)

# 候補者一覧ページの要素待機 (例: 「候補者検索結果」というタイトルを待つ)
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "候補者検索結果")]'))
)
print("「表示」ボタンをクリックし、候補者一覧ページに遷移しました。")

# 1) 「検索結果リスト」の一番上にある会社名をXPathで特定
#    ※下記は「検索結果リスト(id=search-result-list)の中の span.company-name の先頭要素」を想定。
top_company_xpath = '(//div[@id="search-result-list"]//span[@class="company-name"])[1]'

# 2) 要素がクリック可能になるまで待機
top_company_element = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, top_company_xpath))
)

# 3) 念のため画面中央へスクロールし、JSでクリック
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", top_company_element)
time.sleep(1)
driver.execute_script("arguments[0].click();", top_company_element)

# 4) クリック後の画面遷移やポップアップ表示などがある場合は、適宜待機する
# 例: 次ページに固有の要素があれば、下記のように待機
# WebDriverWait(driver, 30).until(
#     EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "詳細ページ")]'))
# )
print("一番上の会社名をクリックしました。")

# 省略: ここまでのコードは既に書かれていると想定

# -----------------------------
# 一番上の会社名をクリックする部分 (既に書かれている箇所)
# -----------------------------
top_company_xpath = '(//div[@id="search-result-list"]//span[@class="company-name"])[1]'
top_company_element = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, top_company_xpath))
)
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", top_company_element)
time.sleep(1)
driver.execute_script("arguments[0].click();", top_company_element)
print("一番上の会社名をクリックしました。")

# ▼▼▼ ここから「スカウトを作成」ボタンをクリックする例 ▼▼▼

# もし「候補者詳細」ページなどに遷移してからボタンが表示されるなら、その要素が出現するまで待つ
#   例: <h1>に「候補者詳細」など特有の文字があれば待機する
# WebDriverWait(driver, 30).until(
#     EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "候補者詳細")]'))
# )

# 「スカウトを作成」ボタンのXPathを指定 (aタグ or buttonタグなど実際のHTML構造に合わせる)
scout_button_xpath = '//button[contains(normalize-space(text()), "スカウトを作成")] | //a[contains(normalize-space(text()), "スカウトを作成")]'

scout_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, scout_button_xpath))
)

# 念のため画面中央へスクロールし、JSでクリック
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", scout_button)
time.sleep(1)
driver.execute_script("arguments[0].click();", scout_button)

print("『スカウトを作成』ボタンをクリックしました。")

# クリック後に次のページやモーダルが開くのであれば、適宜待機
# 例: モーダルや次画面のタイトルなどを待機
# WebDriverWait(driver, 30).until(
#     EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "スカウト作成画面")]'))
# )

# -----------------------------
# 最後、処理を確認するため一時停止
# -----------------------------
input("ブラウザを閉じずに表示を続けます。終了するには何かキーを押してください...")
print("test")