from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os, time, traceback, logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

is_render = os.getenv("RENDER", "false").lower() == "true"
env_file = ".env.production" if is_render else ".env.development"
load_dotenv(env_file)

CHROME_BIN_PATH = "/opt/render/project/src/.chrome/chromium/chrome"
CHROMEDRIVER_PATH = "/opt/render/project/src/.chromedriver/chromedriver"

def login_and_fetch_data(username, password):
    options = Options()
    options.binary_location = CHROME_BIN_PATH
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    logging.info(f"Chrome binary exists: {os.path.exists(CHROME_BIN_PATH)}")
    logging.info(f"ChromeDriver exists: {os.path.exists(CHROMEDRIVER_PATH)}")

    driver = None
    try:
        service = Service(executable_path=CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("Chrome driver launched successfully.")

        driver.get("https://gecgudlavalleruonlinepayments.com/")
        time.sleep(1)

        driver.find_element(By.ID, "txtId2").send_keys(username)
        driver.find_element(By.ID, "txtPwd2").send_keys(password)
        driver.find_element(By.ID, "imgBtn2").click()
        time.sleep(3)

        driver.get("https://gecgudlavalleruonlinepayments.com/Academics/StudentProfile.aspx")
        time.sleep(3)

        try:
            WebDriverWait(driver, 5).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "capIframeId"))
            )
        except:
            pass

        perf_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//h1[contains(text(), 'PERFORMANCE (Present)')]"))
        )
        perf_tab.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "divProfile_Present"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        div_perf = soup.find("div", {"id": "divProfile_Present"})

        return {
            "status": "success",
            "tableHTML": str(div_perf)
        }

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        logging.debug(f"Stack trace: {traceback.format_exc()}")
        return {
            "status": "error",
            "message": str(e),
            "stack": traceback.format_exc()
        }

    finally:
        if driver:
            try:
                driver.quit()
                logging.info("Chrome driver quit successfully.")
            except Exception as quit_error:
                logging.error(f"Error while quitting driver: {quit_error}")
