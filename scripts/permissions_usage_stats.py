import json
from collections import defaultdict

def generate_permission_stats(permission_data):
    permission_stats = defaultdict(lambda: {'used': 0, 'unused': 0, 'requested': 0})
    extensions_all_used = 0
    extensions_with_unused = 0
    critical_permissions = ["<all_urls>", "nativeMessaging", "debugger", "tabs", "webRequest", "webRequestBlocking"]
    critical_unused = defaultdict(int)
    extensions_unused_counts = []

    # Processa cada extensão
    for ext_id, permissions in permission_data.items():
        unused_count = 0
        has_unused = False

        for perm, used in permissions.items():
            permission_stats[perm]['requested'] += 1
            if used:
                permission_stats[perm]['used'] += 1
            else:
                permission_stats[perm]['unused'] += 1
                unused_count += 1
                has_unused = True
                if perm in critical_permissions:
                    critical_unused[perm] += 1

        if has_unused:
            extensions_with_unused += 1
            extensions_unused_counts.append({
                "id": ext_id,
                "unused_permissions": unused_count,
                "total_permissions": len(permissions)
            })
        else:
            extensions_all_used += 1

    # Calcula métricas adicionais
    top_requested = sorted(
        permission_stats.items(),
        key=lambda x: x[1]['requested'],
        reverse=True
    )[:10]

    top_wasted = sorted(
        permission_stats.items(),
        key=lambda x: (x[1]['unused'] / x[1]['requested']) if x[1]['requested'] > 0 else 0,
        reverse=True
    )[:100]

    top_extensions_unused = sorted(
        extensions_unused_counts,
        key=lambda x: x["unused_permissions"],
        reverse=True
    )[:10]

    # Formata o relatório
    report = {
        "permission_usage": {
            perm: {
                "used": stats['used'],
                "unused": stats['unused'],
                "requested": stats['requested'],
                "ratio": f"{stats['used']}/{stats['requested']}"
            } for perm, stats in permission_stats.items()
        },
        "extensions_summary": {
            "all_permissions_used": extensions_all_used,
            "with_unused_permissions": extensions_with_unused,
            "ratio": f"{extensions_all_used}/{len(permission_data)}"
        },
        "top_requested_permissions": [
            {"permission": perm, "requested": stats['requested']}
            for perm, stats in top_requested
        ],
        "top_wasted_permissions": [
            {
                "permission": perm,
                "unused_ratio": f"{stats['unused']}/{stats['requested']}",
                "percentage_unused": round((stats['unused'] / stats['requested']) * 100, 2)
            }
            for perm, stats in top_wasted
        ],
        "critical_permissions_unused": {
            perm: {
                "total_requested": permission_stats[perm]['requested'],
                "total_unused": critical_unused.get(perm, 0),
                "ratio": f"{critical_unused.get(perm, 0)}/{permission_stats[perm]['requested']}"
            }
            for perm in critical_permissions if perm in permission_stats
        },
        "top_extensions_with_unused_permissions": top_extensions_unused
    }
    return report

# Carrega o JSON de entrada
with open("data/permissions_usage_report.json", "r") as file:
    permission_data = json.load(file)

# Gera o relatório
report = generate_permission_stats(permission_data)

# Salva o relatório
with open("data/permission_analysis_report.json", "w") as file:
    json.dump(report, file, indent=4)

print("Análise concluída! Verifique 'permission_analysis_report.json'.")