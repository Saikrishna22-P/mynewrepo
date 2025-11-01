import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Configuration ---
IDMC_URL = "https://usw5-cai.dm-us.informaticacloud.com/activevos-central/hDYxJ4CSgmEefLG7Cahz6l/app/aesf-screenflow?avsf_sflow_uri=project%3A%2Fsf.lockUnlockBusinessEntity%2FlockUnlockBusinessEntity.xml&_sfMode=runtime&_sfGuideName=lockUnlockBusinessEntity&_aedev=false"
USERNAME = "NaveenSaiKrishna.Polisetty@libertymutual.com"

# --- Setup Chrome Options ---
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# --- Launch Chrome ---
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 40)

# --- Ask user for hierarchy name ---
hierarchy_name = input("Enter the name for the new hierarchy: ")

# --- Login Flow ---
def login_to_idmc():
    driver.get(IDMC_URL)

    try:
        sso_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.infaButton.infaButton-toolbar-icon")))
        sso_button.click()
    except:
        print("SSO button not found or already bypassed.")

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-draggable")))
    except:
        print("Login dialog not found.")
        driver.quit()
        return

    try:
        username_field = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[contains(@id, 'samlUserName') or contains(@name, 'username') or contains(@placeholder, 'Username')]")
        ))
        username_field.clear()
        username_field.send_keys(USERNAME)
    except:
        print("Username field not found.")
        driver.quit()
        return

    try:
        continue_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@type='submit' or @type='button'][contains(@value, 'Continue')]")
        ))
        continue_button.click()
    except:
        try:
            continue_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'Continue')]")
            ))
            continue_button.click()
        except:
            print("Continue button not found.")
            driver.quit()
            return

    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Select Organization')]")))
    except:
        print("Organization selection not found.")
        driver.quit()
        return

    try:
        grs_prod_option = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(text(), 'GRS-Prod') and contains(text(), 'hDYxJ4CSgmEefLG7Cahz6l')]")
        ))
        grs_prod_option.click()
        time.sleep(2)
    except:
        print("GRS-Prod option not found.")
        driver.quit()
        return

    try:
        confirm_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@type='submit' or @type='button'][contains(@value, 'Continue')] | //button[contains(text(), 'Continue')] | //*[contains(text(), 'Continue')]")
        ))
        confirm_button.click()
    except:
        print("Final Continue button not found.")
        driver.quit()
        return

    print("✅ Login successful!")

# --- Add First Level Nodes ---
def click_add_first_level_nodes():
    try:
        # 1. Click 'Add First Level Nodes' button
        add_node_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[data-testid='add-root-record-button']")
        ))
        driver.execute_script("arguments[0].scrollIntoView(true);", add_node_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", add_node_button)
        print("✅ Clicked 'Add First Level Nodes' button using JS.")
        time.sleep(3)

        # 2. Wait for modal to appear
        modal = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div[data-testid='mdm-bui-search-modal']")
        ))

        # 3. Locate the search input inside the modal
        search_input = modal.find_element(By.CSS_SELECTOR, "input[data-testid='mdm-bui-search-input']")
        driver.execute_script("arguments[0].value = '';", search_input)  # Clear field
        search_input.send_keys("24128677")  # Enter your mstr_prty_id
        print("✅ Entered ID into modal search input.")

        # 4. Click the search icon inside the modal
        search_icon = modal.find_element(By.CSS_SELECTOR, "button[data-testid='mdm-bui-search-icon']")
        driver.execute_script("arguments[0].click();", search_icon)
        print("✅ Clicked search icon inside modal.")

    except Exception as e:
        print(f"❌ Error during modal search: {e}")
        driver.save_screenshot("error_modal_search.png")

# --- Click 'Customer 360', Hierarchies Tab, Add Entity, Create, Fill Form, Submit ---
def click_customer_360_and_hierarchies():
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.app-switcher-container")))
        time.sleep(3)

        customer_360_card = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='Customer 360']/ancestor::a[contains(@class, 'app-switcher-card')]")
        ))
        customer_360_card.click()
        print("✅ Clicked 'Customer 360' card.")
        time.sleep(10)

        hierarchies_tab = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@href, '/ui-x360-app/app/c360/hierarchy-list')]")
        ))
        hierarchies_tab.click()
        print("✅ Clicked 'Hierarchies' tab.")
        time.sleep(5)

        add_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.btn_add_hierarchy[data-testid='btn_add_hierarchy'][aria-label='Add Hierarchy']")
        ))
        add_button.click()
        print("✅ Clicked '+' icon to add hierarchy.")
        time.sleep(2)

        account_entity = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'hierarchy-list')]//span[contains(text(), 'Account to Account Business Entity')]")
        ))
        account_entity.click()
        print("✅ Clicked 'Account to Account Business Entity' item.")
        time.sleep(2)

        create_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.d-button--primary[data-testid='btn-create-new-record']")
        ))
        create_button.click()
        print("✅ Clicked 'Create' button to open form.")
        time.sleep(3)

        name_label = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//label[contains(text(), 'Name')]")
        ))
        name_input_id = name_label.get_attribute("for")
        name_field = wait.until(EC.element_to_be_clickable((By.ID, name_input_id)))
        name_field.clear()
        name_field.send_keys(hierarchy_name)
        print(f"✅ Filled 'Name' field with '{hierarchy_name}'.")

        final_create_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'd-button--primary') and span[text()='Create']]")
        ))
        driver.execute_script("arguments[0].scrollIntoView(true);", final_create_button)
        time.sleep(1)
        final_create_button.click()
        print("✅ Clicked 'Create' to proceed to submission.")

        submit_button = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button[data-testid='hier-submit-btn']")
        ))
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='hier-submit-btn']"))).click()
        print("✅ Clicked 'Submit' to finalize hierarchy creation.")

        # Add First Level Nodes
        click_add_first_level_nodes()

    except Exception as e:
        print(f"❌ Error during hierarchy interaction or form submission: {e}")
        driver.save_screenshot("form_submission_error.png")

# --- Execute Flow ---
login_to_idmc()
click_customer_360_and_hierarchies()

# --- Keep Tab Open ---
print("⏳ Keeping tab open for 5 minutes...")
time.sleep(300)

# --- Optional: Close Browser ---
# driver.quit()
