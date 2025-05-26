from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
import time
from datetime import datetime, timedelta

def login_to_twitter(driver, user_id, password):
    driver.get("https://twitter.com/login")
    time.sleep(3)

    user_input = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "text")))
    user_input.send_keys(user_id)
    user_input.send_keys(Keys.ENTER)
    time.sleep(2)

    pass_input = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "password")))
    pass_input.send_keys(password)
    pass_input.send_keys(Keys.ENTER)
    time.sleep(5)

def count_replies(username, target_date, login_id, login_pass):
    chromedriver_autoinstaller.install()

    next_date = (datetime.strptime(target_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    query = f"from:{username} filter:replies since:{target_date} until:{next_date}"
    url = f"https://twitter.com/search?q={query}&src=typed_query&f=live"

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    login_to_twitter(driver, login_id, login_pass)

    driver.get(url)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='cellInnerDiv']"))
        )
    except:
        driver.quit()
        return 0

    tweet_urls = set()
    scroll_attempts = 0
    max_scrolls = 30
    unchanged_scrolls = 0
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        time.sleep(3)
        anchors = driver.find_elements(By.XPATH, "//a/time/parent::a")
        for a in anchors:
            href = a.get_attribute("href")
            if href and '/status/' in href:
                tweet_urls.add(href)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            unchanged_scrolls += 1
        else:
            unchanged_scrolls = 0

        if unchanged_scrolls >= 3 or scroll_attempts >= max_scrolls:
            break

        scroll_attempts += 1
        last_height = new_height

    driver.quit()
    return len(tweet_urls)
