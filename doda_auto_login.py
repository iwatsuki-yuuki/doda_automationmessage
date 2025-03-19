from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time

def wait_and_click(xpath, description, wait_time=30, scroll=True):
    """
    指定のXPathの要素がクリック可能になるまで待機し、クリックします。
    """
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        if scroll:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)
        element.click()
        print(f"{description}をクリックしました。")
    except Exception as e:
        print(f"{description}のクリックに失敗しました: {e}")

def wait_for_visibility(xpath, description, wait_time=30):
    """
    指定のXPathの要素が表示されるまで待機し、その要素を返します。
    """
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        print(f"{description}が表示されました。")
        return element
    except Exception as e:
        print(f"{description}の表示待機に失敗しました: {e}")
        return None

# ブラウザ起動
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

try:
    # ------------- ログイン処理 -------------
    url = "https://search.doda-x.jp/login/"
    driver.get(url)

    email = "tnakano@masterkey-inc.com"
    password = "Masterkey1322"

    email_xpath = '//input[@placeholder="メールアドレス（半角英数字）"]'
    email_field = wait_for_visibility(email_xpath, "メールアドレス入力欄")
    email_field.send_keys(email)

    password_xpath = '//input[contains(@placeholder,"パスワード（半角英大小文字")]'
    password_field = wait_for_visibility(password_xpath, "パスワード入力欄")
    password_field.send_keys(password)

    login_button_xpath = '//button[contains(text(), "同意してログイン")]'
    wait_and_click(login_button_xpath, "ログインボタン")

    # ------------- 候補者検索画面へ遷移 -------------
    candidate_search_header_xpath = '//nav[@id="g-nav"]//a[@href="/member_search/"]'
    candidate_search_header = wait_for_visibility(candidate_search_header_xpath, "候補者検索ヘッダー")
    ActionChains(driver).move_to_element(candidate_search_header).perform()
    time.sleep(1)

    search_condition_list_xpath = '//li[@class="g-nav-sub-item"]/a[@href="/search_list/"]'
    wait_and_click(search_condition_list_xpath, "検索条件リストリンク")

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "検索条件リスト")]'))
    )
    print("検索条件リスト画面に遷移しました。")

    # ------------- 候補者一覧へ遷移 -------------
    show_button_xpath = '//p[@class="btn-light-s btn-size-l" and normalize-space(text())="表示"]'
    wait_and_click(show_button_xpath, "表示ボタン")

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "候補者検索結果")]'))
    )
    print("候補者一覧ページに遷移しました。")

    # ------------- 候補者詳細画面へ遷移 -------------
    top_company_xpath = '(//div[@id="search-result-list"]//span[@class="company-name"])[1]'
    wait_and_click(top_company_xpath, "一番上の会社名")

    # ------------- スカウト作成画面へ遷移 -------------
    scout_button_xpath = (
        '//button[contains(normalize-space(text()), "スカウトを作成")] | '
        '//a[contains(normalize-space(text()), "スカウトを作成")]'
    )
    wait_and_click(scout_button_xpath, "スカウトを作成ボタン")
    print("『スカウトを作成』ボタンをクリックしました。")
    time.sleep(2)  # モーダル表示待機

    # ------------- 追加処理：テンプレート「【IT向け】」の選択 -------------
    # ① コンボボックス（id="vs4__combobox"）をクリックしてリスト表示を促す
    template_combobox_xpath = "//*[@id='vs4__combobox']"
    wait_and_click(template_combobox_xpath, "テンプレートコンボボックス")

    # ② リストボックス（id="vs4__listbox"）が表示されるまで待機
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "vs4__listbox"))
    )
    time.sleep(1)  # 表示安定のため少し待機

    # ③ リスト内から「【IT向け】」を選択
    it_option_xpath = "//*[@id='vs4__listbox']//li[normalize-space(.)='【IT向け】']"
    wait_and_click(it_option_xpath, "【IT向け】テンプレートオプション")

    # ------------- 追加処理：通常スカウトの選択 -------------
    # ラジオボタンのinputに対応するlabel要素をクリックする
    normal_scout_label_xpath = "//label[@for='mem-status-normal']"
    wait_and_click(normal_scout_label_xpath, "通常スカウトラジオボタンラベル")

    # ------------- 最終確認 -------------
    input("最終確認です。ブラウザを閉じずに表示を続けます。終了するには何かキーを押してください...")

except Exception as e:
    print("エラーが発生しました:", e)
finally:
    driver.quit()
