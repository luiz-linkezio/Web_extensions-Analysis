import json

def load_json(file_path):
    """Loads the JSON from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def get_nested_fields(data, prefix=""):
    """Gets all available fields in the JSON, including nested fields, excluding 'id', 'name' and 'downloads'."""
    fields = []
    if isinstance(data, dict):
        for key, value in data.items():
            # Ignores the 'id', 'name' and 'downloads' fields
            if key in ['id', 'name', 'downloads']:
                continue
            new_prefix = f"{prefix}.{key}" if prefix else key
            fields.append(new_prefix)
            fields.extend(get_nested_fields(value, new_prefix))
    elif isinstance(data, list) and data:
        # If it's a list, adds the field with index [0] to represent arrays
        fields.append(f"{prefix}[*]")
        if isinstance(data[0], dict):
            fields.extend(get_nested_fields(data[0], f"{prefix}[0]"))
    return fields

def filter_extensions(extensions, filters):
    """Filter extensions based on the provided filters."""
    filtered_extensions = []
    for extension in extensions:
        match = True
        for field, value in filters.items():
            # Filter for number of downloads
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
                        if key.endswith('[*]'):  # If the field is an array
                            key = key[:-3]  # Remove the [*] to access the field
                            if key in current_data and isinstance(current_data[key], list):
                                # Check if the value is in the array
                                if value not in current_data[key]:
                                    match = False
                                    break
                            else:
                                match = False
                                break
                        else:
                            if '[' in key and ']' in key:  # If it's an array index
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
    file_path = 'data/merged_extensions.json'   # Path to the JSON file
    data = load_json(file_path)
    
    # Filter by minimum number of downloads
    filters = {}
    apply_download_filter = input("Do you want to filter by minimum number of downloads? (y/n): ")
    if apply_download_filter.lower() == 'y':
        min_downloads = input("What is the minimum number of downloads? ")
        try:
            min_downloads = int(min_downloads)
            filters['downloads'] = min_downloads
        except ValueError:
            print("Invalid value for minimum downloads. Continuing without applying the filter.")
    
    # Filter by fields
    apply_field_filter = input("Do you want to use field filtering? (y/n): ")
    if apply_field_filter.lower() == 'y':
        while True:
            print("\nAvailable fields for filtering (except 'id', 'name', 'downloads'):")
            fields = get_nested_fields(data['extensions'][0])
            for idx, field in enumerate(fields, 1):
                print(f"{idx}. {field}")
            
            choice = input("\nEnter the number of the field you want to filter (or 'exit' to finish): ")
            if choice.lower() == 'exit':
                break
            
            try:
                field = fields[int(choice) - 1]
            except (IndexError, ValueError):
                print("Invalid choice. Try again.")
                continue
            
            value = input(f"What value do you want to filter for field '{field}'? ")
            filters[field] = value
            
            more_filters = input("Do you want to add more filters? (y/n): ")
            if more_filters.lower() != 'y':
                break
    
    # Apply the filters
    filtered_extensions = filter_extensions(data['extensions'], filters)
    data['extensions'] = filtered_extensions
    data['extensions_count'] = len(filtered_extensions)
    
    # Save the filtered result
    output_file = 'data/filtered_extensions.json'
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)
    
    print(f"\nFiltered JSON saved in '{output_file}'.")

if __name__ == "__main__":
    main()
