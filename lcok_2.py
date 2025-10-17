from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Configuration ---
LOGIN_URL = "https://usw5-cai.dm-us.informaticacloud.com/activevos-central/hDYxJ4CSgmEefLG7Cahz6l/app/aesf-screenflow?avsf_sflow_uri=project%3A%2Fsf.lockUnlockBusinessEntity%2FlockUnlockBusinessEntity.xml&_sfMode=runtime&_sfGuideName=lockUnlockBusinessEntity&_aedev=false"
USERNAME = "NaveenSaiKrishna.Polisetty@libertymutual.com"

# --- Setup Chrome Options ---
options = Options()
options.add_argument("--start-maximized")

# --- Launch Chrome ---
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 40)

# --- Step 1: Open Login Page ---
driver.get(LOGIN_URL)

# --- Step 2: Click SSO Button ---
try:
    sso_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button.infaButton.infaButton-toolbar-icon")
    ))
    sso_button.click()
    print("✅ SSO button clicked.")
except Exception as e:
    print("❌ Failed to click SSO button:", e)

# --- Step 3: Wait for SSO Widget ---
try:
    time.sleep(5)  # Give time for widget to load
    widget = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-draggable")
    ))
    print("✅ SSO widget loaded.")
except Exception as e:
    print("❌ Failed to locate SSO widget:", e)
    print("🔍 Dumping page source for debugging...")
    with open("sso_debug.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    driver.save_screenshot("sso_debug.png")
    driver.quit()
    exit()

# --- Step 4: Enter Username ---
try:
    username_field = wait.until(EC.presence_of_element_located(
        (By.ID, "ifrm2_samlUserName_label-for-id")
    ))
    username_field.clear()
    username_field.send_keys(USERNAME)
    print("✅ Username entered.")
except Exception as e:
    print("❌ Failed to enter username:", e)
    print("🔍 Dumping page source for debugging...")
    with open("username_debug.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    driver.save_screenshot("username_debug.png")
    driver.quit()
    exit()

# --- Step 5: Click Continue Button ---
try:
    continue_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix button")
    ))
    continue_button.click()
    print("✅ Continue button clicked.")
except Exception as e:
    print("❌ Failed to click Continue button:", e)

# --- Step 6: Optional Wait for Confirmation ---
time.sleep(5)

# --- Step 7: Close Browser ---
driver.quit()