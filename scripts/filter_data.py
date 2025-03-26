import json

def load_json(file_path):
    """Carrega o JSON de um arquivo."""
    with open(file_path, 'r') as file:
        return json.load(file)

def get_nested_fields(data, prefix=""):
    """Obtém todos os campos disponíveis no JSON, incluindo campos aninhados, excluindo 'id', 'name' e 'downloads'."""
    fields = []
    if isinstance(data, dict):
        for key, value in data.items():
            # Ignora os campos 'id', 'name' e 'downloads'
            if key in ['id', 'name', 'downloads']:
                continue
            new_prefix = f"{prefix}.{key}" if prefix else key
            fields.append(new_prefix)
            fields.extend(get_nested_fields(value, new_prefix))
    elif isinstance(data, list) and data:
        # Se for uma lista, adiciona o campo com índice [0] para representar arrays
        fields.append(f"{prefix}[*]")
        if isinstance(data[0], dict):
            fields.extend(get_nested_fields(data[0], f"{prefix}[0]"))
    return fields

def filter_extensions(extensions, filters):
    """Filtra as extensões com base nos filtros fornecidos."""
    filtered_extensions = []
    for extension in extensions:
        match = True
        for field, value in filters.items():
            # Filtro para o número de downloads
            if field == 'downloads':
                try:
                    if extension.get('downloads', 0) < value:
                        match = False
                except ValueError:
                    match = False
            else:
                keys = field.split('.')
                current_data = extension
                try:
                    for key in keys:
                        if key.endswith('[*]'):  # Se o campo for um array
                            key = key[:-3]  # Remove o [*] para acessar o campo
                            if key in current_data and isinstance(current_data[key], list):
                                # Verifica se o valor está no array
                                if value not in current_data[key]:
                                    match = False
                                    break
                            else:
                                match = False
                                break
                        else:
                            if '[' in key and ']' in key:  # Se for um índice de array
                                key = int(key.split('[')[1].split(']')[0])
                            current_data = current_data[key]
                    else:
                        if isinstance(current_data, list):
                            if value not in current_data:
                                match = False
                        elif str(current_data) != value:
                            match = False
                except (KeyError, IndexError, TypeError):
                    match = False
                    break
        if match:
            filtered_extensions.append(extension)
    return filtered_extensions

def main():
    file_path = 'data/merged_extensions.json'   # Caminho para o arquivo JSON
    data = load_json(file_path)
    
    # Filtro por número mínimo de downloads
    filters = {}
    apply_download_filter = input("Deseja filtrar por número mínimo de downloads? (s/n): ")
    if apply_download_filter.lower() == 's':
        min_downloads = input("Qual é o número mínimo de downloads? ")
        try:
            min_downloads = int(min_downloads)
            filters['downloads'] = min_downloads
        except ValueError:
            print("Valor inválido para o número mínimo de downloads. Continuando sem aplicar o filtro.")
    
    # Filtro por campos
    apply_field_filter = input("Deseja usar o filtro de campos? (s/n): ")
    if apply_field_filter.lower() == 's':
        while True:
            print("\nCampos disponíveis para filtro (exceto 'id', 'name', 'downloads'):")
            fields = get_nested_fields(data['extensions'][0])
            for idx, field in enumerate(fields, 1):
                print(f"{idx}. {field}")
            
            choice = input("\nDigite o número do campo que você deseja filtrar (ou 'sair' para finalizar): ")
            if choice.lower() == 'sair':
                break
            
            try:
                field = fields[int(choice) - 1]
            except (IndexError, ValueError):
                print("Escolha inválida. Tente novamente.")
                continue
            
            value = input(f"Qual valor você deseja filtrar para o campo '{field}'? ")
            filters[field] = value
            
            more_filters = input("Deseja adicionar mais filtros? (s/n): ")
            if more_filters.lower() != 's':
                break
    
    # Aplicar os filtros
    filtered_extensions = filter_extensions(data['extensions'], filters)
    data['extensions'] = filtered_extensions
    data['extensions_count'] = len(filtered_extensions)
    
    # Salvar o resultado filtrado
    output_file = 'data/filtered_extensions.json'
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)
    
    print(f"\nJSON filtrado salvo em '{output_file}'.")

if __name__ == "__main__":
    main()
