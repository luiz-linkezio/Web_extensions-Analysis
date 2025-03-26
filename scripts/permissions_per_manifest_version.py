import json
from collections import defaultdict
import statistics

def analyze_permissions(json_file):
    # Carregar o JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Estruturas para análise
    version_stats = defaultdict(list)
    permission_distribution = defaultdict(int)
    top_extensions = []
    
    # Processar cada extensão
    for ext in data['extensions']:
        try:
            # Extrair dados básicos
            manifest_version = str(ext.get('manifest_version', 'unknown'))
            name = ext.get('name', 'unnamed_extension')
            permissions = ext.get('permissions', [])
            num_permissions = len(permissions)
            
            # Atualizar estatísticas
            version_stats[manifest_version].append(num_permissions)
            
            # Contar distribuição de permissões
            for perm in permissions:
                permission_distribution[perm] += 1
                
            # Manter registro das extensões com mais permissões
            top_extensions.append((name, num_permissions, manifest_version))
            
        except Exception as e:
            print(f"Erro ao processar extensão: {e}")
            continue
    
    # Calcular estatísticas
    results = {}
    for version, counts in version_stats.items():
        results[version] = {
            'average': statistics.mean(counts),
            'median': statistics.median(counts),
            'min': min(counts),
            'max': max(counts),
            'count': len(counts)
        }
    
    # Top 5 extensões com mais permissões
    top_extensions.sort(key=lambda x: x[1], reverse=True)
    
    # Permissões mais comuns
    common_permissions = sorted(permission_distribution.items(), 
                               key=lambda x: x[1], reverse=True)[:20]
    
    return {
        'version_stats': results,
        'top_extensions': top_extensions[:5],
        'common_permissions': common_permissions
    }

def print_results(stats):
    print("\n=== Estatísticas por Versão do Manifesto ===")
    for version, data in stats['version_stats'].items():
        print(f"\nManifest V{version}:")
        print(f"  Extensões analisadas: {data['count']}")
        print(f"  Média de permissões: {data['average']:.1f}")
        print(f"  Mediana: {data['median']}")
        print(f"  Mínimo: {data['min']}")
        print(f"  Máximo: {data['max']}")
    
    print("\n=== Top 5 Extensões com Mais Permissões ===")
    for i, (name, count, version) in enumerate(stats['top_extensions'], 1):
        print(f"{i}. {name} (V{version}): {count} permissões")
    
    print("\n=== Permissões Mais Comuns ===")
    for perm, count in stats['common_permissions']:
        print(f"- {perm}: {count} extensões")

# Uso
if __name__ == "__main__":
    stats = analyze_permissions('data/filtered_extensions.json')
    print_results(stats)