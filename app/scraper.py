import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os, time, traceback, logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
is_render = os.getenv("RENDER", "false").lower() == "true"
env_file = ".env.production" if is_render else ".env.development"
load_dotenv(env_file)

CHROME_BIN_PATH = "/opt/render/project/src/.chrome/chromium/chrome"

def login_and_fetch_data(username, password):
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    if is_render:
        options.binary_location = CHROME_BIN_PATH

    logging.info(f"Chrome binary exists: {os.path.exists(CHROME_BIN_PATH)}")
    driver = None

    try:
        driver = uc.Chrome(options=options, browser_executable_path=CHROME_BIN_PATH)
        logging.info("Chrome driver launched successfully.")

        driver.get("https://gecgudlavalleruonlinepayments.com/")
        time.sleep(1)

        driver.find_element(By.ID, "txtId2").send_keys(username)
        driver.find_element(By.ID, "txtPwd2").send_keys(password)
        driver.find_element(By.ID, "imgBtn2").click()
        time.sleep(3)

        driver.get("https://gecgudlavalleruonlinepayments.com/Academics/StudentProfile.aspx")
        time.sleep(3)

        # Switch to CAPTCHA iframe if available
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
                logging.info("Quitting driver and stopping service.")
                driver.quit()  # Normal quit
                if hasattr(driver, 'service'):
                    driver.service.stop()  # Explicitly stop the service if available
            except Exception as quit_error:
                logging.error(f"Error while quitting driver: {quit_error}")
