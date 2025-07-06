from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options for better compatibility
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Set up the webdriver (Chrome)
driver = webdriver.Chrome(options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

try:
    # Navigate to a website
    driver.get("https://www.google.com")
    
    # Wait a moment for page to fully load
    time.sleep(2)
    
    # Try to dismiss any cookie banners or overlays
    try:
        # Look for common cookie banner dismiss buttons
        cookie_buttons = driver.find_elements(By.CSS_SELECTOR, 
            "button[id*='accept'], button[id*='agree'], button[class*='accept'], button[class*='agree']")
        for button in cookie_buttons:
            if button.is_displayed():
                button.click()
                time.sleep(1)
                break
    except:
        pass
    
    # Wait for search box to be clickable (not just present)
    search_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "q"))
    )
    
    # Click on the search box first to ensure it's focused
    search_box.click()
    
    # Type in search box
    search_box.send_keys("selenium python")
    search_box.send_keys(Keys.RETURN)
    
    # Wait for results and print page title
    WebDriverWait(driver, 10).until(
        EC.title_contains("selenium python")
    )
    
    print(f"Page title: {driver.title}")
    
except Exception as e:
    print(f"An error occurred: {e}")
    
finally:
    # Close the browser
    driver.quit()