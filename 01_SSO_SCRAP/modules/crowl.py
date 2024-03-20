import pyotp

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC

def crowl(ct_url, email_id, email_pw, otp, account_id, profile_name):
    # 1. common variables.
    mfa = pyotp.TOTP(f'{otp}')

    # 2. set options.
    # set wait time.
    wait_time = 30
    # set pageload strategy.
    caps = DesiredCapabilities().CHROME
    caps['pageLoadStrategy'] = 'none'
    # set driver headless.
    chrome_options = Options()
    chrome_options.headless = True
    
    # 3. execute browser.
    browser = webdriver.Chrome(desired_capabilities = caps, options = chrome_options)
    browser.get(f'{ct_url}')

    # 4. login.
    # id.
    Wait(browser, wait_time).until(EC.presence_of_element_located((By.XPATH, '//*[@id="username-input"]/div/child::input'))).send_keys(f'{email_id}', Keys.ENTER)
    # pw.
    Wait(browser, wait_time).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password-input"]/div/child::input'))).send_keys(f'{email_pw}', Keys.ENTER)
    # mfa.
    Wait(browser, wait_time).until(EC.presence_of_element_located((By.XPATH, '//*[@id="input-0"]/div/child::input'))).send_keys(f'{mfa.now()}', Keys.ENTER)

    # 5. select account.
    Wait(browser, wait_time).until(EC.presence_of_element_located((By.XPATH, '//*[@title="AWS Account"]'))).click()

    account_id_elem = Wait(browser, wait_time).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="instance-metadata"]/span[text()="#{account_id}"]')))
    account_id_elem_up = Wait(account_id_elem, wait_time).until(EC.presence_of_element_located((By.XPATH, '..'))) # p
    account_id_elem_up_up = Wait(account_id_elem_up, wait_time).until(EC.presence_of_element_located((By.XPATH, '..'))) # div
    Wait(account_id_elem_up_up, wait_time).until(EC.presence_of_element_located((By.XPATH, '..'))).click() # flex div

    profile_name_elem = Wait(browser, wait_time).until(EC.presence_of_element_located((By.XPATH, f'//*[@class="desktop-profile"]/span[text()="{profile_name} "]')))
    Wait(profile_name_elem, wait_time).until(EC.presence_of_element_located((By.XPATH, '//child::a[@id="temp-credentials-button"]'))).click()

    # 6. select temp credentials.
    aws_access_key_id = Wait(browser, wait_time).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cli-cred-file-code"]/div[2]'))).text
    aws_secret_access_key = Wait(browser, wait_time).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cli-cred-file-code"]/div[3]'))).text
    aws_session_token = Wait(browser, wait_time).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cli-cred-file-code"]/div[4]'))).text
    # refine temp credentials data.
    aws_access_key_id = aws_access_key_id.split(' = ', 1)[1]
    aws_secret_access_key = aws_secret_access_key.split(' = ', 1)[1]
    aws_session_token = aws_session_token.split(' = ', 1)[1]

    # 7. return.
    return aws_access_key_id, aws_secret_access_key, aws_session_token