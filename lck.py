from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

class IDUnlockAutomation:
    def __init__(self, url, username, business_id):
        self.url = url
        self.username = username
        self.business_id = business_id

        options = Options()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 90)

    def switch_to_iframe_containing_input(self, input_id):
        self.driver.switch_to.default_content()
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            try:
                self.driver.switch_to.frame(iframe)
                self.driver.find_element(By.ID, input_id)
                print(f"✅ Switched to iframe: {iframe.get_attribute('id') or 'no-id'}")
                return True
            except:
                self.driver.switch_to.default_content()
        return False

    def login_and_submit(self):
        try:
            self.driver.get(self.url)
            sso_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.infaButton.infaButton-toolbar-icon")))
            sso_button.click()
            print("✅ SSO button clicked.")

            widget = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-draggable")))
            print("✅ SSO widget loaded.")

            username_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'samlUserName') or contains(@name, 'username') or contains(@placeholder, 'Username')]")))
            username_field.clear()
            username_field.send_keys(self.username)
            print("✅ Username entered.")

            try:
                continue_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' or @type='button'][contains(@value, 'Continue')]")))
                continue_button.click()
            except:
                continue_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Continue')]")))
                continue_button.click()
            print("✅ Continue button clicked.")

            self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Select Organization')]")))
            print("✅ Organization selection widget loaded.")

            grs_prod_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'GRS-Prod') and contains(text(), 'hDYxJ4CSgmEefLG7Cahz6l')]")))
            grs_prod_option.click()
            print("✅ GRS-Prod organization selected.")
            time.sleep(2)

            confirm_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' or @type='button'][contains(@value, 'Continue')] | //button[contains(text(), 'Continue')] | //*[contains(text(), 'Continue')]")))
            confirm_button.click()
            print("✅ Organization selection confirmed.")

            self.driver.execute_script(f"window.open('{self.url}', '_blank');")
            self.driver.switch_to.window(self.driver.window_handles[1])
            print("✅ Lock/Unlock portal opened in new tab.")

            input_id = "ae_sf_string_renderer1"
            print("🔍 Searching for Business ID input field in iframes...")
            found = self.switch_to_iframe_containing_input(input_id)
            if not found:
                print("❌ Could not locate input field in any iframe.")
                self.driver.save_screenshot("error_screenshot_final.png")
                self.driver.quit()
                return

            self.driver.save_screenshot("before_entering_business_id.png")
            business_id_input = self.wait.until(EC.presence_of_element_located((By.ID, input_id)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", business_id_input)
            time.sleep(1)
            business_id_input.click()
            time.sleep(0.5)

            print(f"📌 Entering Business ID: {self.business_id}")
            self.driver.execute_script("""
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, business_id_input, self.business_id)

            time.sleep(1)
            entered_value = business_id_input.get_attribute("value")
            print(f"🔎 Business ID field value after input: {entered_value}")
            self.driver.save_screenshot("after_entering_business_id.png")

            if entered_value != self.business_id:
                print("❌ Business ID was not set correctly. Retrying...")
                business_id_input.clear()
                business_id_input.send_keys(self.business_id)
                time.sleep(1)
                entered_value = business_id_input.get_attribute("value")
                print(f"🔁 Retried value: {entered_value}")
                if entered_value != self.business_id:
                    print("❌ Retry failed.")
                    self.driver.save_screenshot("error_screenshot_final.png")
                    self.driver.quit()
                    return

            self.driver.switch_to.default_content()
            dropdown_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select#ae_sf-picklist_renderer2.ae-sf-screen-simpledataitem-value.ae-sf-screen-simpledataitem-inputcontrol.ae-sf-screen-renderer-datavalue")))
            dropdown = Select(dropdown_element)
            dropdown.select_by_visible_text("Lock/Unlock")
            print("✅ Dropdown option selected.")

            continue_container = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#ae_sf_rt_screen_prompt_actions_wrapper")))
            continue_button = continue_container.find_element(By.XPATH, ".//*[contains(text(), 'Continue')]")
            continue_button.click()
            print("✅ Continue clicked.")

        except Exception as e:
            print("❌ Automation failed:", e)
            self.driver.save_screenshot("error_screenshot_final.png")
            self.driver.quit()

    def close(self):
        print("Closing browser...")
        self.driver.quit()

# Example usage
if __name__ == "__main__":
    IDMC_URL = "https://usw5-cai.dm-us.informaticacloud.com/activevos-central/hDYxJ4CSgmEefLG7Cahz6l/app/aesf-screenflow?avsf_sflow_uri=project%3A%2Fsf.lockUnlockBusinessEntity%2FlockUnlockBusinessEntity.xml&_sfMode=runtime&_sfGuideName=lockUnlockBusinessEntity&_aedev=false"
    USERNAME = "NaveenSaiKrishna.Polisetty@libertymutual.com"
    BUSINESS_ID = "5416458"

    automation = IDUnlockAutomation(IDMC_URL, USERNAME, BUSINESS_ID)
    automation.login_and_submit()
    time.sleep(5)
    automation.close()