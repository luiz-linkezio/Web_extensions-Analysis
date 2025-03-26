import json

# Carregar o JSON de permissões usadas
file_path = "data/permissions_usage_report.json"  # Substitua pelo nome correto do arquivo

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Lista para armazenar a taxa de uso de cada extensão
usage_rates = []

# Iterar sobre cada extensão
for ext_id, permissions in data.items():
    total_requested = len(permissions)  # Total de permissões solicitadas
    total_used = sum(1 for perm in permissions.values() if perm)  # Total de permissões realmente usadas

    # Evitar divisão por zero (caso uma extensão não tenha permissões listadas)
    if total_requested > 0:
        usage_rate = total_used / total_requested
        usage_rates.append(usage_rate)

# Calcular a média geral das taxas de uso
average_usage_rate = sum(usage_rates) / len(usage_rates) if usage_rates else 0

# Exibir o resultado
print(f"Taxa média de uso das permissões solicitadas: {average_usage_rate:.2%}")
