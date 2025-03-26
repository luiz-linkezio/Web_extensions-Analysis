import os
import json
import logging
import time
from datetime import datetime, timezone
from collections import defaultdict

# Diretórios e paths
LOG_DIR = "exploit_permissions/logs/merge_data"
DUMP_DIR = "exploit_permissions/data/raw_json_manifests/"
OUTPUT_FILE = "exploit_permissions/data/merged_extensions.json"

# Criar diretórios se não existirem
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DUMP_DIR, exist_ok=True)

# Função para configurar o logger
def setup_logger():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = os.path.join(LOG_DIR, f"{timestamp}.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_filename),  # Log em arquivo
            logging.StreamHandler()  # Log no console
        ]
    )
    return logging.getLogger()

logger = setup_logger()

# Lista de paths
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

def merge_json_files():
    start_time = time.time()
    extensions_dict = {}
    extension_paths = defaultdict(set)
    duplicate_count = 0  # Contador para extensões duplicadas
    
    logger.info(f"Iniciando a merge dos arquivos JSON... Total de categorias: {len(PATHS)}")

    for path in PATHS:
        if path == "":
            path = "/root"

        formatted_path = path.replace('/', '_')
        file_path = os.path.join(DUMP_DIR, f"extensions{formatted_path}.json")

        if not os.path.exists(file_path):
            logger.warning(f"Arquivo não encontrado: {file_path}")
            continue
        
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                extensions_list = data.get("extensions", [])

                logger.info("-" * 100)  # Linha de divisão
                
                logger.info(f"Carregando {len(extensions_list)} extensões de {file_path}")

                for ext in extensions_list:
                    ext_id = ext["id"]
                    
                    if ext.get("downloads"):
                        ext["downloads"] = int(ext["downloads"])  # Converte para inteiro
                    else:
                        ext["downloads"] = -1  # Se não houver valor, define como -1

                    
                    if ext_id in extensions_dict:
                        logger.info(f"Extensão duplicada encontrada: {ext_id} (adicionando novo caminho)")
                        extension_paths[ext_id].add(path)
                        duplicate_count += 1
                    else:
                        extensions_dict[ext_id] = ext
                        extension_paths[ext_id] = {path}

        except Exception as e:
            logger.error(f"Erro ao processar {file_path}: {str(e)}")

    logger.info("-" * 100)  # Linha de divisão
    logger.info("Finalizando o merge dos dados e adicionando caminhos às extensões...")

    # Atualizar a lista de paths nas extensões
    for ext_id, paths in extension_paths.items():
        ext = extensions_dict[ext_id]
        ext["paths"] = list(paths)
        extensions_dict[ext_id] = {"id": ext["id"], "paths": ext["paths"], **{k: v for k, v in ext.items() if k not in ["id", "paths"]}}
    
    logger.info("Ordenando extensões por número de downloads...")
    
    # Ordenar por número de downloads (decrescente)
    sorted_extensions = sorted(extensions_dict.values(), key=lambda x: x["downloads"], reverse=True)
    
    # Criar estrutura final
    merged_data = {
        "extensions_count": len(sorted_extensions),
        "extraction_date": datetime.now().isoformat(),
        "extensions": sorted_extensions
    }
    
    # Salvar no arquivo final
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
            json.dump(merged_data, output_file, indent=4, ensure_ascii=False)
        logger.info(f"Arquivo de saída gerado com sucesso: {OUTPUT_FILE}")
    except Exception as e:
        logger.error(f"Erro ao salvar {OUTPUT_FILE}: {str(e)}")
    
    # Tempo de execução
    elapsed_time = time.time() - start_time
    logger.info(f"Tempo de execução: {elapsed_time:.2f} segundos")

    # Adicionando contagem de extensões duplicadas e únicas
    logger.info(f"Extensões únicas: {len(sorted_extensions)}")
    logger.info(f"Extensões duplicadas: {duplicate_count}")

if __name__ == "__main__":
    merge_json_files()
