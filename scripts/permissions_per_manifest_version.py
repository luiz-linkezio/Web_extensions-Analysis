import json
from collections import defaultdict
import statistics

def analyze_permissions(json_file):
    # Load the JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Structures for analysis
    version_stats = defaultdict(list)
    permission_distribution = defaultdict(int)
    top_extensions = []
    
    # Process each extension
    for ext in data['extensions']:
        try:
            # Extract basic data
            manifest_version = str(ext.get('manifest_version', 'unknown'))
            name = ext.get('name', 'unnamed_extension')
            permissions = ext.get('permissions', [])
            num_permissions = len(permissions)
            
            # Update statistics
            version_stats[manifest_version].append(num_permissions)
            
            # Count permission distribution
            for perm in permissions:
                permission_distribution[perm] += 1
                
            # Keep track of extensions with more permissions
            top_extensions.append((name, num_permissions, manifest_version))
            
        except Exception as e:
            print(f"Error processing extension: {e}")
            continue
    
    # Calculate statistics
    results = {}
    for version, counts in version_stats.items():
        results[version] = {
            'average': statistics.mean(counts),
            'median': statistics.median(counts),
            'min': min(counts),
            'max': max(counts),
            'count': len(counts)
        }
    
    # Top 5 extensions with most permissions
    top_extensions.sort(key=lambda x: x[1], reverse=True)
    
    # Most common permissions
    common_permissions = sorted(permission_distribution.items(), 
                               key=lambda x: x[1], reverse=True)[:20]
    
    return {
        'version_stats': results,
        'top_extensions': top_extensions[:5],
        'common_permissions': common_permissions
    }

def print_results(stats):
    print("\n=== Statistics by Manifest Version ===")
    for version, data in stats['version_stats'].items():
        print(f"\nManifest V{version}:")
        print(f"  Extensions analyzed: {data['count']}")
        print(f"  Average permissions: {data['average']:.1f}")
        print(f"  Median: {data['median']}")
        print(f"  Minimum: {data['min']}")
        print(f"  Maximum: {data['max']}")
    
    print("\n=== Top 5 Extensions with Most Permissions ===")
    for i, (name, count, version) in enumerate(stats['top_extensions'], 1):
        print(f"{i}. {name} (V{version}): {count} permissions")
    
    print("\n=== Most Common Permissions ===")
    for perm, count in stats['common_permissions']:
        print(f"- {perm}: {count} extensions")

# Usage
if __name__ == "__main__":
    stats = analyze_permissions('data/filtered_extensions.json')
    print_results(stats)