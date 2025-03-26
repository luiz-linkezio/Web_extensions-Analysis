import os
import json
import requests
import zipfile
import re
from typing import Dict, List, Set

# Configurações
DOWNLOAD_DIR = "extensions_crx"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Função para baixar o CRX (igual à sua versão anterior)
def download_extension(extension_id: str) -> str:
    url = f"https://clients2.google.com/service/update2/crx?response=redirect&prodversion=91.0&acceptformat=crx2,crx3&x=id%3D{extension_id}%26uc"
    crx_path = os.path.join(DOWNLOAD_DIR, f"{extension_id}.crx")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(crx_path, 'wb') as file:
            file.write(response.content)
        return crx_path
    return None

# Função para extrair JS do CRX
def extract_js_files(crx_path: str, extraction_dir: str) -> List[str]:
    js_files = []
    with zipfile.ZipFile(crx_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_dir)
        for root, _, files in os.walk(extraction_dir):
            for file in files:
                if file.endswith('.js'):
                    js_files.append(os.path.join(root, file))
    return js_files

# Função para verificar o uso de permissões nos JS
def check_permissions_usage(js_files: List[str], permissions: List[str]) -> Dict[str, bool]:
    permission_usage = {perm: False for perm in permissions}
    
    for js_file in js_files:
        try:
            with open(js_file, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                for perm in permissions:
                    # Padrões de busca (ex: chrome.permissions, chrome.tabs, etc.)
                    patterns = [
                        f"chrome.{perm.split('.')[-1]}",  # chrome.tabs
                        f"chrome\\['{perm.split('.')[-1]}'\\]",  # chrome['tabs']
                        f"chrome\\.{perm.split('.')[-1]}\\s*\\(",  # chrome.tabs.query(
                    ]
                    if any(re.search(pattern, content) for pattern in patterns):
                        permission_usage[perm] = True
        except Exception as e:
            print(f"Erro ao ler {js_file}: {e}")
    
    return permission_usage

# Função principal para processar uma extensão
def process_extension(extension_id: str, permissions: List[str]) -> Dict[str, Dict[str, bool]]:
    crx_path = download_extension(extension_id)
    if not crx_path:
        return None
    
    extraction_dir = os.path.join(DOWNLOAD_DIR, f"extracted_{extension_id}")
    os.makedirs(extraction_dir, exist_ok=True)
    
    js_files = extract_js_files(crx_path, extraction_dir)
    permission_usage = check_permissions_usage(js_files, permissions)
    
    # Limpa os arquivos extraídos (opcional)
    for root, _, files in os.walk(extraction_dir, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        os.rmdir(root)
    os.remove(crx_path)
    
    return {extension_id: permission_usage}

# Exemplo de uso:
if __name__ == "__main__":
    # Carrega seu JSON filtrado
    with open("data/filtered_extensions.json", "r") as file:
        data = json.load(file)
    
    results = {}
    for ext in data["extensions"]:
        ext_id = ext["id"]
        permissions = ext["permissions"]
        print(f"Processando {ext_id}...")
        
        usage_data = process_extension(ext_id, permissions)
        if usage_data:
            results.update(usage_data)
    
    # Salva os resultados
    with open("permissions_usage_report.json", "w") as file:
        json.dump(results, file, indent=4)