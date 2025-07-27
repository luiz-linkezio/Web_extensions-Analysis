import os
import json
import requests
import zipfile
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

# Diretório de download das extensões
DOWNLOAD_DIR = "exploit_permissions/data"
LOGS_DIR = "exploit_permissions/logs/dump"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Diretório para armazenar os JSONs de cada path
EXTENSIONS_JSON_DIR = os.path.join(DOWNLOAD_DIR, "extensions_json")
os.makedirs(EXTENSIONS_JSON_DIR, exist_ok=True)

# Diretório para logs
os.makedirs(LOGS_DIR, exist_ok=True)

# URL base do Chrome Web Store
BASE_URL = "https://chrome.google.com/webstore/category/extensions"
PATHS = [
    "",
    "/productivity/communication",
    "/productivity/education",
    "/productivity/tools",
    "/productivity/developer",
    "/productivity/workflow",
    "/lifestyle/art",
    "/lifestyle/well_being",
    "/lifestyle/shopping",
    "/lifestyle/entertainment",
    "/lifestyle/household",
    "/lifestyle/games",
    "/lifestyle/news",
    "/lifestyle/fun",
    "/lifestyle/social",
    "/lifestyle/travel",
    "/make_chrome_yours/accessibility",
    "/make_chrome_yours/functionality",
    "/make_chrome_yours/privacy",
]

# Function to configure the logger
def setup_logger():
    """Configure and return a logger instance."""
    logger = logging.getLogger('extension_dumper')
    logger.setLevel(logging.INFO)
    
    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(os.path.join(LOGS_DIR, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"))
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.INFO)
    
    # Create formatters and add it to handlers
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(log_format)
    f_handler.setFormatter(log_format)
    
    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    
    return logger

# Function to configure the Selenium driver
def setup_driver():
    """Configure and return a Chrome WebDriver instance."""
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")  # Run in headless mode, without opening browser window
    driver = webdriver.Chrome(options=options)
    return driver

# Function to load all extensions
def load_all_extensions(driver, path, logger):
    """Loads all extensions until the 'Load more' button is no longer available."""
    logger.info(f"[NAVIGATION] Accessing: {path}")
    driver.get(path)  # Access the specific URL path
    time.sleep(2)  # Wait a bit for the page to load

    while True:
        try:
            # Wait until the "Load more" button is visible using the new XPath
            load_more_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//button[@jsname='t6Kl7b']//span[contains(text(), 'Carregar mais')]"))
            )
            driver.execute_script("arguments[0].click();", load_more_button)
            logger.info(f"[NAVIGATION] Clicked 'Load more' in: {path}")
            time.sleep(2)  # Wait a bit for new extensions to load
            
            # Count the 'a' tags that have './detail/' in the href
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            a_tags = soup.find_all('a', href=True)
            detail_links = [link for link in a_tags if './detail/' in link['href']]
            logger.info(f"[INFO] Number of extensions loaded on screen: {len(detail_links)}")

            if len(detail_links) >= 1568:
                break

        except Exception as e:
            logger.warning(f"[NAVIGATION] No more extensions to load or error clicking 'Load more' in {path}")
            break

# Function to extract extension IDs
def get_extension_ids(driver, logger):
    """Extracts extension IDs from the current page."""
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    extension_ids = []
    for link in soup.find_all('a', href=True):
        if './detail/' in link['href']:
            extension_id = link['href'].split('/')[-1]
            extension_ids.append(extension_id)
    
    return list(set(extension_ids))

# Function to download extension
def download_extension(extension_id, logger):
    """Downloads the extension in CRX format."""
    logger.info("-" * 100)  # Division line
    logger.info(f"[DOWNLOAD] Downloading extension: {extension_id}")
    url = f"https://clients2.google.com/service/update2/crx?response=redirect&prodversion=91.0&acceptformat=crx2,crx3&x=id%3D{extension_id}%26uc"
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            crx_path = os.path.join(DOWNLOAD_DIR, f"{extension_id}.crx")
            with open(crx_path, 'wb') as file:
                file.write(response.content)
            logger.info(f"[DOWNLOAD] Extension {extension_id} downloaded successfully.")
            return crx_path
        else:
            logger.error(f"[DOWNLOAD] Error downloading extension {extension_id}: Status {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"[DOWNLOAD] Request error downloading extension {extension_id}: {e}")
        return None

# Function to extract manifest
def extract_manifest(crx_path, logger):
    """Extracts manifest.json from a CRX file."""
    logger.info(f"[EXTRACTION] Extracting manifest from: {crx_path}")
    
    try:
        with zipfile.ZipFile(crx_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if 'manifest.json' in file:
                    with zip_ref.open(file) as manifest_file:
                        return json.load(manifest_file)
                    
    except json.JSONDecodeError as e:
        logger.error(f"[EXTRACTION] Error decoding manifest JSON")
    except Exception as e:
        logger.error(f"[EXTRACTION] Error extracting manifest from {crx_path}")

    return None

# Function to save all extension information in a single JSON file
def save_all_manifests(manifests, logger):
    """Saves all extension information in a single JSON file."""
    json_path = os.path.join(DOWNLOAD_DIR, "extensions_info.json")
    
    # Create the dictionary with the information
    data_to_save = {
        "extensions_count": len(manifests),
        "extraction_date": datetime.now().isoformat(),
        "extensions": manifests
    }
    
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data_to_save, file, indent=4, ensure_ascii=False)
    
    logger.info(f"[SAVING] Data saved to: {json_path}")

# Function to extract download count from details page
def get_downloads_count(driver, extension_id, logger):
    """Extracts the number of downloads from the extension details page."""
    try:
        logger.info(f"[EXTRACTION] Extracting the number of downloads/users for the extension: {extension_id}")

        detail_url = f"https://chrome.google.com/webstore/detail/{extension_id}"
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(detail_url)
        
        # Wait for the page to load completely
        time.sleep(3)
        
        # Extract the number of downloads
        try:
            downloads_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'users') or contains(text(), 'usuários')]"))
            )
            downloads_text = downloads_element.text
            # Extract only the numeric part
            downloads = ''.join(filter(str.isdigit, downloads_text))
            return int(downloads) if downloads else 0
        except:
            return 0

    except Exception as e:
        logger.error(f"[EXTRACTION] Error extracting number of downloads for extension: {extension_id}:")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])  # Return to original tab
        return 0
    finally:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])  # Return to original tab

# Function to save manifests in JSON by category
def save_manifests_by_path(path, manifests, logger):
    """Saves extension information in a separate JSON by path."""
    formatted_path = path.replace('/', '_')
    json_path = os.path.join(DOWNLOAD_DIR, f"extensions{formatted_path}.json")
    
    data_to_save = {
        "extensions_count": len(manifests),
        "extraction_date": datetime.now().isoformat(),
        "extensions": manifests
    }
    
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data_to_save, file, indent=4, ensure_ascii=False)
    
    logger.info(f"[SAVING] Data saved to: {json_path}")

def process_extensions(driver, extension_ids, logger):
    """Processes extensions, collects manifests and download counts."""
    manifests = []
    for ext_id in extension_ids:
        try:
            # Download the extension
            crx_path = download_extension(ext_id, logger)
            if not crx_path:
                continue
            
            # Extract manifest
            manifest = extract_manifest(crx_path, logger)
            if not manifest:
                continue
            
            # Get download count
            downloads = get_downloads_count(driver, ext_id, logger)
            
            # Add metadata
            manifest['id'] = ext_id
            manifest['downloads'] = downloads
            
            manifests.append(manifest)
            
            # Clean up
            os.remove(crx_path)  # Remove the CRX file after processing
            
        except Exception as e:
            logger.error(f"Error processing extension {ext_id}: {e}")
            continue
    
    return manifests

def main():
    start_time = datetime.now()  # Mark the start of execution
    
    logger = setup_logger()
    driver = setup_driver()
    
    # Process extensions and save manifests with download counts
    for path in PATHS:
        try:
            load_all_extensions(driver, path, logger)
            extension_ids = get_extension_ids(driver, logger)
            manifests = process_extensions(driver, extension_ids, logger)
            save_manifests_by_path(path, manifests, logger)
        except Exception as e:
            logger.error(f"Error processing path {path}: {e}")
    
    driver.quit()
    
    end_time = datetime.now()  # Mark the end of execution
    total_duration = end_time - start_time
    logger.info(f"Total execution time: {str(total_duration).split('.')[0]}")

# Execução principal do script
if __name__ == "__main__":
    main()