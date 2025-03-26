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

# Função para configurar o logger
def setup_logger():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = os.path.join(LOGS_DIR, f"{timestamp}.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        handlers=[
            logging.FileHandler(log_filename),  # Log em arquivo
            logging.StreamHandler()  # Log no console
        ]
    )
    return logging.getLogger()

# Função para configurar o driver do Selenium
def setup_driver():
    """Configura o driver do Selenium."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Execute em modo headless, sem abrir a janela do navegador
    driver = webdriver.Chrome(options=options)
    return driver

# Função para carregar todas as extensões
def load_all_extensions(driver, path, logger):
    """Carrega todas as extensões até que o botão 'Carregar mais' não esteja mais disponível."""
    logger.info(f"[NAVEGAÇÃO] Acessando: {path}")
    driver.get(path)  # Acesse a URL específica do caminho
    time.sleep(2)  # Aguarda um pouco para que a página carregue

    while True:
        try:
            # Aguarda até que o botão "Carregar mais" esteja visível usando o novo XPath
            load_more_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//button[@jsname='t6Kl7b']//span[contains(text(), 'Carregar mais')]"))
            )
            driver.execute_script("arguments[0].click();", load_more_button)
            logger.info(f"[NAVEGAÇÃO] Clicou em 'Carregar mais' em: {path}")
            time.sleep(2)  # Aguarda um pouco para que novas extensões sejam carregadas
            
            # Conta as tags 'a' que possuem './detail/' no href
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            a_tags = soup.find_all('a', href=True)
            detail_links = [link for link in a_tags if './detail/' in link['href']]
            logger.info(f"[INFO] Quantidade de extensões carregadas em tela: {len(detail_links)}")

            if len(detail_links) >= 1568:
                break

        except Exception as e:
            logger.warning(f"[NAVEGAÇÃO] Não há mais extensões para carregar ou erro ao clicar em 'Carregar mais' em {path}")
            break

# Função para extrair os IDs das extensões
def get_extension_ids(driver, logger):
    """Extrai os IDs das extensões da página atual."""
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    extension_ids = []
    for link in soup.find_all('a', href=True):
        if './detail/' in link['href']:
            extension_id = link['href'].split('/')[-1]
            extension_ids.append(extension_id)
    
    return list(set(extension_ids))

# Função para baixar a extensão
def download_extension(extension_id, logger):
    """Baixa a extensão no formato CRX."""
    logger.info("-" * 100)  # Linha de divisão
    logger.info(f"[DOWNLOAD] Baixando extensão: {extension_id}")
    url = f"https://clients2.google.com/service/update2/crx?response=redirect&prodversion=91.0&acceptformat=crx2,crx3&x=id%3D{extension_id}%26uc"
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            crx_path = os.path.join(DOWNLOAD_DIR, f"{extension_id}.crx")
            with open(crx_path, 'wb') as file:
                file.write(response.content)
            logger.info(f"[DOWNLOAD] Extensão {extension_id} baixada com sucesso.")
            return crx_path
        else:
            logger.error(f"[DOWNLOAD] Erro ao baixar a extensão {extension_id}: Status {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"[DOWNLOAD] Erro de requisição ao baixar a extensão {extension_id}: {e}")
        return None

# Função para extrair o manifest
def extract_manifest(crx_path, logger):
    """Extrai o manifest.json de um arquivo CRX."""
    logger.info(f"[EXTRAÇÃO] Extraindo manifest de: {crx_path}")
    
    try:
        with zipfile.ZipFile(crx_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if 'manifest.json' in file:
                    with zip_ref.open(file) as manifest_file:
                        return json.load(manifest_file)
                    
    except json.JSONDecodeError as e:
        logger.error(f"[EXTRAÇÃO] Erro ao decodificar o JSON do manifest")
    except Exception as e:
        logger.error(f"[EXTRAÇÃO] Erro ao extrair o manifest de {crx_path}")

    return None

# Função para salvar todas as informações das extensões em um único arquivo JSON
def save_all_manifests(manifests, logger):
    """Salva todas as informações das extensões em um único arquivo JSON."""
    json_path = os.path.join(DOWNLOAD_DIR, "extensions_info.json")
    
    # Criar o dicionário com as informações
    data_to_save = {
        "extensions_count": len(manifests),
        "extraction_date": datetime.now().isoformat(),
        "extensions": manifests
    }
    
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data_to_save, file, indent=4, ensure_ascii=False)
    
    logger.info(f"[SALVAR] Dados salvos em: {json_path}")

# Função para extrair o número de downloads da página de detalhes
def get_downloads_count(driver, extension_id, logger):
    """Extrai o número de downloads da página de detalhes da extensão."""
    try:
        logger.info(f"[EXTRAÇÃO] Extraindo o número de downloads/usuários da extensão: {extension_id}")

        detail_url = f"https://chrome.google.com/webstore/detail/{extension_id}"
        driver.execute_script(f"window.open('{detail_url}', '_blank');")  # Abre a página da extensão em uma nova aba
        driver.switch_to.window(driver.window_handles[1])  # Muda para a nova aba
        
        # Aguarda a página carregar completamente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'F9iKBc'))
        )
        
        # Extrai o número de downloads
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        downloads_div = soup.find('div', class_='F9iKBc')
        downloads_text = downloads_div.get_text(strip=True) if downloads_div else None
        downloads_count = None
        if downloads_text:
            # Extraímos apenas a parte numérica
            downloads_count = ''.join(filter(str.isdigit, downloads_text))
        
        driver.close()  # Fecha a aba da extensão
        driver.switch_to.window(driver.window_handles[0])  # Volta para a aba original

        return downloads_count

    except Exception as e:
        logger.error(f"[EXTRAÇÃO] Erro ao extrair número de downloads da extensão: {extension_id}:")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])  # Volta para a aba original
        return None


# Função para salvar os manifestos em JSON por categoria
def save_manifests_by_path(path, manifests, logger):
    """Salva as informações das extensões em um JSON separado por path."""
    category = path.strip("/").replace("/", "_") or "root"
    json_filename = f"extensions_{category}.json"
    json_path = os.path.join(EXTENSIONS_JSON_DIR, json_filename)

    data_to_save = {
        "path": path,
        "extensions_count": len(manifests),
        "extraction_date": datetime.now().isoformat(),
        "extensions": manifests
    }

    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data_to_save, file, indent=4, ensure_ascii=False)
    
    logger.info(f"[SALVAR] Dados salvos em: {json_path}")

def process_extensions(driver, extension_ids, logger):
    """Processa as extensões, coleta os manifests e os números de downloads."""
    manifests = []
    for ext_id in extension_ids:
        crx_path = download_extension(ext_id, logger)
        
        if crx_path:
            manifest = extract_manifest(crx_path, logger)
            if manifest:
                downloads_count = get_downloads_count(driver, ext_id, logger)  # Obtém o número de downloads
                manifests.append({
                    "id": ext_id,
                    "downloads": downloads_count,
                    "name": manifest.get("name", "unknown_extension"),
                    "manifest_version": manifest.get("manifest_version", "unknown"),
                    "permissions": manifest.get("permissions", []),
                    "host_permissions": manifest.get("host_permissions", []),
                    "content_scripts": manifest.get("content_scripts", []),
                    "content_security_policy": manifest.get("content_security_policy", {}),
                    "externally_connectable": manifest.get("externally_connectable", {}),
                    "storage": manifest.get("storage", {}),
                })
            os.remove(crx_path)  # Remove o arquivo CRX após o processamento

    return manifests

# Execução principal do script
if __name__ == "__main__":
    logger = setup_logger()  # Configura o logger
    start_time = datetime.now()  # Marca o início da execução
    driver = setup_driver()

    for path in PATHS:
        full_path = BASE_URL + path
        load_all_extensions(driver, full_path, logger)
        extension_ids = get_extension_ids(driver, logger)
        
        # Processa as extensões e salva os manifests com o número de downloads
        manifests = process_extensions(driver, extension_ids, logger)

        save_manifests_by_path(path, manifests, logger)

        logger.info("-" * 100)  # Linha de divisão

    driver.quit()  # Fecha o navegador após a execução
    
    end_time = datetime.now()  # Marca o fim da execução
    total_duration = end_time - start_time
    logger.info(f"Tempo total de execução: {str(total_duration).split('.')[0]}")