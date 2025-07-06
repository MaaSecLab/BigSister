from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

class ImageSearchIRIS:
    def __init__(self):
        """Initialize the Image Retrieval and Identification Script"""
        self.driver = None
        self.max_results = 10
        self.search_timeout = 30
        self.setup_driver()
    
    def setup_driver(self):
        """Set up Chrome webdriver with stealth options"""
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option("prefs", {"intl.accept_languages": "en-US,en"})
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    def reverse_image_search(self, image_path):
        """Perform reverse image search using Google Images"""
        if not os.path.exists(image_path):
            print(f"❌ Error: Image file not found: {image_path}")
            return False
        
        try:
            print(f"🔍 Starting reverse image search for: {image_path}")
            
            # Navigate to Google Images
            self.driver.get("https://images.google.com?hl=en&gl=us")
            time.sleep(3)
            
            # Handle cookie consent if present
            self._handle_cookie_consent()
            
            # Click on the camera icon for reverse image search
            camera_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label*='Search by image']"))
            )
            camera_button.click()
            
            # Wait for upload dialog and click "Upload a file"
            upload_tab = None
            upload_selectors = [
                "//div[contains(text(), 'Upload a file')]",
                "//div[contains(text(), 'upload a file')]", 
                "//div[contains(text(), 'Upload an image')]",
                "//span[contains(text(), 'Upload a file')]",
                "//span[contains(text(), 'upload a file')]",
                "//button[contains(text(), 'Upload')]",
                "//div[@role='tab'][contains(., 'Upload')]",
                "//div[contains(@class, 'upload')]",
                "[data-bucket='upload']",
                "input[type='file']"
            ]
            
            for selector in upload_selectors:
                try:
                    if selector.startswith("//"):
                        upload_tab = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        upload_tab = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    print(f"✅ Found upload element with selector: {selector}")
                    break
                except:
                    continue
            
            if upload_tab:
                upload_tab.click()
            else:
                print("❌ Could not find upload button, trying alternative approach...")
            
            # Find and click the file input
            file_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
            
            # Upload the image file
            file_input.send_keys(os.path.abspath(image_path))
            
            # Wait for search results to load
            print("⏳ Waiting for search results...")
            WebDriverWait(self.driver, self.search_timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-ved]"))
            )
            
            time.sleep(3)  # Additional wait for full page load
            
            print("✅ Search completed! Results are now visible in the browser.")
            print("🌐 You can browse the results directly in the opened browser window.")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during reverse image search: {e}")
            return False
    
    def _handle_cookie_consent(self):
        """Handle Google's cookie consent dialog"""
        try:
            # Look for various cookie consent buttons
            consent_selectors = [
                "button[id*='accept']",
                "button[id*='agree']",
                "button[id*='Accept all']" 
                "button[class*='accept']",
                "button[class*='agree']",
                "div[role='button'][jsaction*='accept']"
            ]
            
            for selector in consent_selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for button in buttons:
                        if button.is_displayed() and button.is_enabled():
                            button.click()
                            time.sleep(1)
                            return
                except:
                    continue
        except Exception as e:
            print(f"Note: Could not handle cookie consent: {e}")
    
    def close(self):
        """Close the webdriver"""
        if self.driver:
            self.driver.quit()
            print("🔒 Browser closed")

def main():
    """Main function to demonstrate reverse image search"""
    # Initialize IRIS
    iris = ImageSearchIRIS()
    
    try:
        # Test image path
        test_image = "/home/lambda/Downloads/photo-1526779259212-939e64788e3c.jpeg"
        
        # Perform reverse image search
        success = iris.reverse_image_search(test_image)
        
        if success:
            print("\n" + "="*60)
            print("🎯 REVERSE IMAGE SEARCH COMPLETED!")
            print("="*60)
            print("📋 The search results are now displayed in your browser.")
            print("🔍 You can:")
            print("   • Browse through visually similar images")
            print("   • Check pages that contain matching images")
            print("   • Click on any result to explore further")
            print("   • Use browser tools to save or analyze results")
            print("="*60)
            
            # Keep browser open for user interaction
            input("\n⏸️  Press Enter when you're done viewing the results to close the browser...")
        
    except KeyboardInterrupt:
        print("\n⚠️  Search interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        iris.close()

if __name__ == "__main__":
    main()