from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import traceback
from dotenv import load_dotenv
import os

# for Render.com deployment and local development
is_render = os.getenv("RENDER", "false").lower() == "true"
env_file = ".env.production" if is_render else ".env.development"
load_dotenv(env_file)

driver_path = os.getenv("CHROMEDRIVER_PATH")

def login_and_fetch_data(username, password):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://gecgudlavalleruonlinepayments.com/")
        time.sleep(1)

        driver.find_element(By.ID, "txtId2").send_keys(username)
        driver.find_element(By.ID, "txtPwd2").send_keys(password)
        driver.find_element(By.ID, "imgBtn2").click()
        time.sleep(3)

        driver.get("https://gecgudlavalleruonlinepayments.com/Academics/StudentProfile.aspx")
        time.sleep(3)

        # Log all iframes
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"Found {len(iframes)} iframes")
        for iframe in iframes:
            print(f"Iframe ID: {iframe.get_attribute('id')}")

        # Try switching to iframe only if it's found
        try:
            WebDriverWait(driver, 5).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "capIframeId"))
            )
            print("Switched to iframe")
        except:
            print("Iframe not found or not switchable, continuing in main page...")

        # ✅ Updated block starts here
        perf_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//h1[contains(text(), 'PERFORMANCE (Present)')]"))
        )
        perf_tab.click()
        print("Clicked performance tab")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "divProfile_Present"))
        )
        print("Performance content loaded")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        div_perf = soup.find("div", {"id": "divProfile_Present"})

        return {
            "status": "success",
            "tableHTML": str(div_perf)
        }
        # ✅ Updated block ends here

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "stack": traceback.format_exc()
        }
    finally:
        driver.quit()
