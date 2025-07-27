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
    duplicate_count = 0  # Counter for duplicate extensions
    
    logger.info(f"Starting JSON files merge... Total categories: {len(PATHS)}")

    for path in PATHS:
        if path == "":
            path = "/root"

        formatted_path = path.replace('/', '_')
        file_path = os.path.join(DUMP_DIR, f"extensions{formatted_path}.json")

        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            continue
        
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                extensions_list = data.get("extensions", [])

                logger.info("-" * 100)  # Division line
                
                logger.info(f"Loading {len(extensions_list)} extensions from {file_path}")

                for ext in extensions_list:
                    ext_id = ext["id"]
                    
                    if ext.get("downloads"):
                        ext["downloads"] = int(ext["downloads"])  # Convert to integer
                    else:
                        ext["downloads"] = -1  # If there's no value, set as -1

                    
                    if ext_id in extensions_dict:
                        logger.info(f"Duplicate extension found: {ext_id} (adding new path)")
                        extension_paths[ext_id].add(path)
                        duplicate_count += 1
                    else:
                        extensions_dict[ext_id] = ext
                        extension_paths[ext_id] = {path}

        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")

    logger.info("-" * 100)  # Division line
    logger.info("Finalizing data merge and adding paths to extensions...")

    # Update the paths list in extensions
    for ext_id, paths in extension_paths.items():
        ext = extensions_dict[ext_id]
        ext["paths"] = list(paths)
        extensions_dict[ext_id] = {"id": ext["id"], "paths": ext["paths"], **{k: v for k, v in ext.items() if k not in ["id", "paths"]}}
    
    logger.info("Sorting extensions by number of downloads...")
    
    # Sort by number of downloads (descending)
    sorted_extensions = sorted(extensions_dict.values(), key=lambda x: x["downloads"], reverse=True)
    
    # Create final structure
    merged_data = {
        "extensions_count": len(sorted_extensions),
        "extraction_date": datetime.now().isoformat(),
        "extensions": sorted_extensions
    }
    
    # Save to final file
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
            json.dump(merged_data, output_file, indent=4, ensure_ascii=False)
        logger.info(f"Output file generated successfully: {OUTPUT_FILE}")
    except Exception as e:
        logger.error(f"Error saving {OUTPUT_FILE}: {str(e)}")
    
    # Execution time
    elapsed_time = time.time() - start_time
    logger.info(f"Execution time: {elapsed_time:.2f} seconds")

    # Adding count of duplicate and unique extensions
    logger.info(f"Unique extensions: {len(sorted_extensions)}")
    logger.info(f"Duplicate extensions: {duplicate_count}")

if __name__ == "__main__":
    merge_json_files()
