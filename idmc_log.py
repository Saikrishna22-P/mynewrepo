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
