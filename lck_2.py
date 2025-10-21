from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Configuration ---
IDMC_URL = "https://usw5-cai.dm-us.informaticacloud.com/activevos-central/hDYxJ4CSgmEefLG7Cahz6l/app/aesf-screenflow?avsf_sflow_uri=project%3A%2Fsf.lockUnlockBusinessEntity%2FlockUnlockBusinessEntity.xml&_sfMode=runtime&_sfGuideName=lockUnlockBusinessEntity&_aedev=false"
LOCK_UNLOCK_URL = IDMC_URL
USERNAME = "NaveenSaiKrishna.Polisetty@libertymutual.com"
BUSINESS_ID = "5416458"

# --- Setup Chrome Options ---
options = Options()
options.add_argument("--start-maximized")

# --- Launch Chrome ---
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 90)

# --- Helper: Switch to iframe containing the input field ---
def switch_to_iframe_containing_input(driver, input_id):
    driver.switch_to.default_content()
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    for iframe in iframes:
        try:
            driver.switch_to.frame(iframe)
            driver.find_element(By.ID, input_id)
            print(f"✅ Switched to iframe: {iframe.get_attribute('id') or 'no-id'}")
            return True
        except:
            driver.switch_to.default_content()
    return False

# --- Function to Fill Business ID and Submit ---
def fill_business_id_and_submit(driver, business_id):
    try:
        driver.switch_to.window(driver.window_handles[1])
        wait = WebDriverWait(driver, 90)

        input_id = "ae_sf_string_renderer1"

        print("🔍 Searching for Business ID input field in iframes...")
        found = switch_to_iframe_containing_input(driver, input_id)
        if not found:
            print("❌ Could not locate input field in any iframe.")
            driver.save_screenshot("error_screenshot_final.png")
            driver.quit()
            exit()

        print("📸 Screenshot before entering Business ID...")
        driver.save_screenshot("before_entering_business_id.png")

        business_id_input = wait.until(EC.presence_of_element_located((By.ID, input_id)))

        driver.execute_script("arguments[0].scrollIntoView(true);", business_id_input)
        time.sleep(1)
        business_id_input.click()
        time.sleep(0.5)

        print(f"📌 Entering Business ID: {business_id}")
        driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, business_id_input, business_id)

        time.sleep(1)
        entered_value = business_id_input.get_attribute("value")
        print(f"🔎 Business ID field value after input: {entered_value}")
        driver.save_screenshot("after_entering_business_id.png")

        if entered_value != business_id:
            print("❌ Business ID was not set correctly. Retrying...")
            business_id_input.clear()
            business_id_input.send_keys(business_id)
            time.sleep(1)
            entered_value = business_id_input.get_attribute("value")
            print(f"🔁 Retried value: {entered_value}")
            if entered_value != business_id:
                print("❌ Retry failed.")
                driver.save_screenshot("error_screenshot_final.png")
                driver.quit()
                exit()

        print("🔍 Waiting for dropdown...")
        driver.switch_to.default_content()
        dropdown_element = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "select#ae_sf-picklist_renderer2.ae-sf-screen-simpledataitem-value.ae-sf-screen-simpledataitem-inputcontrol.ae-sf-screen-renderer-datavalue")
        ))
        dropdown = Select(dropdown_element)
        dropdown.select_by_visible_text("Lock/Unlock")
        print("✅ Dropdown option selected.")

        print("🔍 Waiting for Continue button...")
        continue_container = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div#ae_sf_rt_screen_prompt_actions_wrapper")
        ))
        continue_button = continue_container.find_element(By.XPATH, ".//*[contains(text(), 'Continue')]")
        continue_button.click()
        print("✅ Continue clicked.")
    except Exception as e:
        print("❌ Failed to complete Business ID flow:", e)
        driver.save_screenshot("error_screenshot_final.png")
        driver.quit()
        exit()

# --- Step 1: Open IDMC Login Page ---
driver.get(IDMC_URL)

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
    widget = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-draggable")
    ))
    print("✅ SSO widget loaded.")
except Exception as e:
    print("❌ Failed to locate SSO widget:", e)
    driver.quit()
    exit()

# --- Step 4: Enter Username ---
try:
    username_field = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[contains(@id, 'samlUserName') or contains(@name, 'username') or contains(@placeholder, 'Username')]")
    ))
    username_field.clear()
    username_field.send_keys(USERNAME)
    print("✅ Username entered.")
except Exception as e:
    print("❌ Failed to enter username:", e)
    driver.quit()
    exit()

# --- Step 5: Click Continue Button ---
try:
    continue_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@type='submit' or @type='button'][contains(@value, 'Continue')]")
    ))
    continue_button.click()
    print("✅ Continue button clicked.")
except Exception:
    try:
        continue_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(text(), 'Continue')]")
        ))
        continue_button.click()
        print("✅ Continue button clicked (fallback).")
    except Exception as e:
        print("❌ Failed to click Continue button:", e)
        driver.quit()
        exit()

# --- Step 6: Wait for Organization Selection Widget ---
try:
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//*[contains(text(), 'Select Organization')]")
    ))
    print("✅ Organization selection widget loaded.")
except Exception as e:
    print("❌ Failed to load organization selection widget:", e)
    driver.quit()
    exit()

# --- Step 7: Select GRS-Prod Organization ---
try:
    grs_prod_option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//*[contains(text(), 'GRS-Prod') and contains(text(), 'hDYxJ4CSgmEefLG7Cahz6l')]")
    ))
    grs_prod_option.click()
    print("✅ GRS-Prod organization selected.")
    time.sleep(2)
except Exception as e:
    print("❌ Failed to select GRS-Prod organization:", e)
    driver.quit()
    exit()

# --- Step 8: Confirm Selection ---
try:
    confirm_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@type='submit' or @type='button'][contains(@value, 'Continue')] | //button[contains(text(), 'Continue')] | //*[contains(text(), 'Continue')]")
    ))
    confirm_button.click()
    print("✅ Organization selection confirmed.")
except Exception as e:
    print("❌ Failed to confirm organization selection:", e)
    driver.quit()
    exit()

# --- Step 9: Open Lock/Unlock Portal in New Tab ---
try:
    driver.execute_script(f"window.open('{LOCK_UNLOCK_URL}', '_blank');")
    driver.switch_to.window(driver.window_handles[1])
    print("✅ Lock/Unlock portal opened in new tab.")
except Exception as e:
    print("❌ Failed to open second tab:", e)
    driver.quit()
    exit()

# --- Step 10: Call the Business ID Function ---
print(f"🚀 Submitting Business ID: {BUSINESS_ID}")
fill_business_id_and_submit(driver, BUSINESS_ID)

# --- Step 11: Optional Wait ---
time.sleep(100)

# --- Step 12: Close Browser ---
# driver.quit()