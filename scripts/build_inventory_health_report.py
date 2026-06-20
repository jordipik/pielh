"""
PIELH FASE 0 - Informe de salud del inventario IoT
Solo lectura. Genera JSON + Markdown a partir del summary de auditoría.
"""

import json
import argparse
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def find_latest_summary(audit_dir: Path) -> Path:
    files = sorted(audit_dir.glob("thethings_activity_summary_*.json"), reverse=True)
    if not files:
        raise FileNotFoundError(f"No se encontró ningún summary en {audit_dir}")
    return files[0]


def _enrich_system_names(summary: dict, audit_dir: Path, summary_path: Path) -> None:
    """Rellena system_name en by_system si el summary no lo trae (versión antigua)."""
    by_sys = summary.get("by_system", {})
    if all(v.get("system_name") for v in by_sys.values()):
        return  # ya tiene nombres

    # Buscar CSV con el mismo timestamp que el summary
    ts = summary_path.stem.replace("thethings_activity_summary_", "")
    csv_path = audit_dir / f"thethings_activity_{ts}.csv"
    if not csv_path.exists():
        return

    import csv as csv_mod
    names: dict = {}
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        for row in csv_mod.DictReader(f):
            sid  = row.get("system_id", "")
            name = row.get("system_name", "")
            if sid and name and sid not in names:
                names[sid] = name

    for sid, info in by_sys.items():
        if not info.get("system_name") and sid in names:
            info["system_name"] = names[sid]


def pct(n: int, total: int) -> str:
    if total == 0:
        return "0.0%"
    return f"{n / total * 100:.1f}%"


def active_count(sys_info: dict) -> int:
    return sys_info.get("active_24h", 0) + sys_info.get("active_7d", 0)


def data_count(sys_info: dict) -> int:
    return (sys_info.get("active_24h", 0) + sys_info.get("active_7d", 0)
            + sys_info.get("stale_30d", 0) + sys_info.get("stale_90d", 0)
            + sys_info.get("inactive_90d", 0) + sys_info.get("data_no_timestamp", 0))


# ---------------------------------------------------------------------------
# Clasificación A / B / C
# ---------------------------------------------------------------------------

def classify_system(sys_id: str, s: dict) -> str:
    """
    A — Inventario operativo real: activos en 24h o 7d.
    B — Inventario recuperable: things válidos, datos existentes o tokens a renovar.
    C — Inventario roto: >80% inválidos, 0 activos, 0 datos.
    """
    total   = s.get("total", 0)
    invalid = s.get("invalid", 0)
    active  = active_count(s)
    has_data = data_count(s)

    if active > 0:
        return "A"
    if total > 0 and invalid / total > 0.8 and has_data == 0:
        return "C"
    return "B"


# ---------------------------------------------------------------------------
# Build report dict
# ---------------------------------------------------------------------------

def build_report(summary: dict, source_file: str) -> dict:
    total   = summary.get("total_sensors", 0)
    valid   = summary.get("valid_things", 0)
    invalid = summary.get("invalid_things", 0)
    a24h    = summary.get("active_24h", 0)
    a7d     = summary.get("active_7d", 0)
    s30d    = summary.get("stale_30d", 0)
    s90d    = summary.get("stale_90d", 0)
    i90d    = summary.get("inactive_90d", 0)
    dnt     = summary.get("data_no_timestamp", 0)
    no_data = summary.get("no_data", 0)
    tok_inv = summary.get("token_or_thing_invalid", 0)
    has_val = summary.get("has_real_value", 0)
    api_err = summary.get("api_errors", 0)

    by_system = summary.get("by_system", {})

    # KPIs demo
    demo_ready_sensors  = a24h + a7d
    demo_ready_systems  = sum(1 for s in by_system.values() if active_count(s) > 0)
    demo_ready_percent  = round(demo_ready_sensors / total * 100, 1) if total else 0.0

    # Clasificación por sistema
    classified: dict = {}
    for sys_id, s in by_system.items():
        classified[sys_id] = classify_system(sys_id, s)

    systems_A = sorted([k for k, v in classified.items() if v == "A"],
                       key=lambda k: -active_count(by_system[k]))
    systems_B = sorted([k for k, v in classified.items() if v == "B"],
                       key=lambda k: -by_system[k].get("valid", 0))
    systems_C = sorted([k for k, v in classified.items() if v == "C"],
                       key=lambda k: -by_system[k].get("total", 0))

    # Sistemas con >50% tokens rotos
    broken_token_systems = [
        sys_id for sys_id, s in by_system.items()
        if s.get("total", 0) > 0
        and s.get("invalid", 0) / s["total"] > 0.5
    ]
    broken_token_systems.sort(key=lambda k: -by_system[k].get("invalid", 0))

    return {
        "generated_at":   datetime.now(timezone.utc).isoformat(),
        "source_summary": source_file,
        "executive_summary": {
            "total_sensors":            total,
            "valid_things":             valid,
            "invalid_things":           invalid,
            "sensors_active":           demo_ready_sensors,
            "sensors_with_data":        has_val,
            "sensors_no_data":          no_data,
            "sensors_token_invalid":    tok_inv,
            "api_errors":               api_err,
        },
        "kpis_demo": {
            "demo_ready_sensors":  demo_ready_sensors,
            "demo_ready_systems":  demo_ready_systems,
            "demo_ready_percent":  demo_ready_percent,
        },
        "classification": {
            "A_operative":    systems_A,
            "B_recoverable":  systems_B,
            "C_broken":       systems_C,
        },
        "broken_token_systems": broken_token_systems,
        "systems_detail": {
            sys_id: {
                **s,
                "class":      classified.get(sys_id, "?"),
                "active":     active_count(s),
                "with_data":  data_count(s),
                "pct_invalid": round(s.get("invalid", 0) / s["total"] * 100, 1)
                               if s.get("total", 0) else 0.0,
            }
            for sys_id, s in sorted(by_system.items())
        },
    }


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------

def build_markdown(report: dict, summary: dict) -> str:
    es   = report["executive_summary"]
    kpis = report["kpis_demo"]
    cls  = report["classification"]
    by_s = summary.get("by_system", {})
    det  = report["systems_detail"]

    def sys_name(sid: str) -> str:
        s = by_s.get(sid, {})
        return s.get("system_name", sid) if isinstance(s, dict) and "system_name" in s else sid

    lines = []
    lines.append("# PIELH — Informe de Salud del Inventario IoT")
    lines.append(f"\n_Generado: {report['generated_at']}_")
    lines.append(f"\n_Fuente: `{Path(report['source_summary']).name}`_\n")

    # 1. Resumen ejecutivo
    lines.append("---\n## 1. Resumen ejecutivo\n")
    lines.append(f"| Métrica | Valor |")
    lines.append(f"|---|---|")
    lines.append(f"| Total sensores | {es['total_sensors']} |")
    lines.append(f"| Things válidos | {es['valid_things']} |")
    lines.append(f"| Things inválidos (token/thing roto) | {es['invalid_things']} |")
    lines.append(f"| Sensores activos (24h + 7d) | {es['sensors_active']} |")
    lines.append(f"| Sensores con datos | {es['sensors_with_data']} |")
    lines.append(f"| Sensores sin datos | {es['sensors_no_data']} |")
    lines.append(f"| TOKEN_OR_THING_INVALID | {es['sensors_token_invalid']} |")
    lines.append(f"| Errores API | {es['api_errors']} |\n")

    # 2. Sistemas recuperables (clase A + B con válidos)
    lines.append("---\n## 2. Sistemas con sensores válidos y datos\n")
    headers = ["Sistema", "Nombre", "Total", "Válidos", "Inválidos", "Activos", "Con datos", "Clase"]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for sid in cls["A_operative"] + [s for s in cls["B_recoverable"]
                                      if det[s].get("valid", 0) > 0]:
        d = det[sid]
        lines.append(
            f"| {sid} | {sys_name(sid)} | {d['total']} | {d['valid']} | {d['invalid']} "
            f"| {d['active']} | {d['with_data']} | **{d['class']}** |"
        )

    # 3. Sistemas con tokens rotos
    lines.append("\n---\n## 3. Sistemas con tokens rotos (>50% inválidos)\n")
    if report["broken_token_systems"]:
        lines.append("| Sistema | Nombre | Total | Inválidos | % inválido |")
        lines.append("|---|---|---|---|---|")
        for sid in report["broken_token_systems"]:
            d = det.get(sid, {})
            lines.append(
                f"| {sid} | {sys_name(sid)} | {d.get('total',0)} "
                f"| {d.get('invalid',0)} | {d.get('pct_invalid',0)}% |"
            )
    else:
        lines.append("_Ningún sistema supera el 50% de tokens inválidos._")

    # 4. Recomendados para demo
    lines.append("\n---\n## 4. Sistemas recomendados para demo\n")
    lines.append("_Criterio: ACTIVE\\_24H + ACTIVE\\_7D > 0, ordenados por sensores activos._\n")
    lines.append("| Sistema | Nombre | Activos | ACTIVE\\_24H | ACTIVE\\_7D | Con datos | Total |")
    lines.append("|---|---|---|---|---|---|---|")
    for sid in cls["A_operative"]:
        s = by_s.get(sid, {})
        lines.append(
            f"| {sid} | {sys_name(sid)} | {active_count(s)} "
            f"| {s.get('active_24h',0)} | {s.get('active_7d',0)} "
            f"| {data_count(s)} | {s.get('total',0)} |"
        )

    # 5. KPIs demo
    lines.append("\n---\n## 5. KPIs demo\n")
    lines.append(f"| KPI | Valor |")
    lines.append(f"|---|---|")
    lines.append(f"| demo\\_ready\\_sensors | {kpis['demo_ready_sensors']} |")
    lines.append(f"| demo\\_ready\\_systems | {kpis['demo_ready_systems']} |")
    lines.append(f"| demo\\_ready\\_percent | {kpis['demo_ready_percent']}% |")

    # 6. Clasificación completa
    lines.append("\n---\n## 6. Clasificación completa A / B / C\n")
    lines.append("| Clase | Criterio |")
    lines.append("|---|---|")
    lines.append("| **A** — Operativo | ACTIVE\\_24H + ACTIVE\\_7D > 0 |")
    lines.append("| **B** — Recuperable | Things válidos existentes, datos o tokens a renovar |")
    lines.append("| **C** — Roto | >80% inválidos, 0 activos, 0 datos |")
    lines.append("")

    all_sids = sorted(det.keys())
    lines.append("| Sistema | Nombre | Clase | Total | Válidos | Inválidos | Activos | Con datos |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for sid in all_sids:
        d = det[sid]
        cls_label = {"A": "**A**", "B": "B", "C": "*C*"}.get(d.get("class", "?"), "?")
        lines.append(
            f"| {sid} | {sys_name(sid)} | {cls_label} "
            f"| {d['total']} | {d['valid']} | {d['invalid']} "
            f"| {d['active']} | {d['with_data']} |"
        )

    lines.append("\n---")
    lines.append("_PIELH Smart City — Auditoría FASE 0 — Solo lectura._")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="PIELH FASE 0 - Informe de salud del inventario IoT"
    )
    parser.add_argument(
        "--summary", type=str, default=None,
        help="Ruta al summary JSON (por defecto: último generado en data/audits/)"
    )
    args = parser.parse_args()

    base_dir  = Path(__file__).resolve().parent.parent
    audit_dir = base_dir / "data" / "audits"

    if args.summary:
        summary_path = Path(args.summary)
    else:
        summary_path = find_latest_summary(audit_dir)

    print(f"[PIELH] Leyendo: {summary_path.name}")
    with open(summary_path, "r", encoding="utf-8") as f:
        summary = json.load(f)
    _enrich_system_names(summary, audit_dir, summary_path)

    report = build_report(summary, str(summary_path))
    md     = build_markdown(report, summary)

    # Guardar JSON
    json_out = audit_dir / "inventory_health_report.json"
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # Guardar Markdown
    md_out = audit_dir / "inventory_health_report.md"
    with open(md_out, "w", encoding="utf-8") as f:
        f.write(md)

    # Imprimir resumen en consola
    es   = report["executive_summary"]
    kpis = report["kpis_demo"]
    sep  = "-" * 52
    print(f"\n[PIELH] INVENTARIO {sep}")
    print(f"  Total sensores:          {es['total_sensors']}")
    print(f"  Things validos:          {es['valid_things']}")
    print(f"  Things invalidos:        {es['invalid_things']}")
    print(f"  Activos (24h+7d):        {es['sensors_active']}")
    print(f"  Con datos:               {es['sensors_with_data']}")
    print(f"  Sin datos:               {es['sensors_no_data']}")
    print(f"")
    print(f"  DEMO KPIs:")
    print(f"    demo_ready_sensors:    {kpis['demo_ready_sensors']}")
    print(f"    demo_ready_systems:    {kpis['demo_ready_systems']}")
    print(f"    demo_ready_percent:    {kpis['demo_ready_percent']}%")
    print(f"")
    cls = report["classification"]
    print(f"  Clase A (operativo):     {cls['A_operative']}")
    print(f"  Clase B (recuperable):   {cls['B_recoverable']}")
    print(f"  Clase C (roto):          {cls['C_broken']}")
    print(sep)
    print(f"  JSON: {json_out}")
    print(f"  MD:   {md_out}")


# ---------------------------------------------------------------------------
# Función reutilizable (importada desde server.py)
# ---------------------------------------------------------------------------

def run_build_report(summary: dict, audit_dir: Path, summary_source: str = "in-memory") -> dict:
    """Genera inventory_health_report.json + .md en audit_dir. Devuelve report dict."""
    audit_dir.mkdir(parents=True, exist_ok=True)
    report = build_report(summary, summary_source)

    json_out = audit_dir / "inventory_health_report.json"
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    md_out = audit_dir / "inventory_health_report.md"
    with open(md_out, "w", encoding="utf-8") as f:
        f.write(build_markdown(report, summary))

    return report


if __name__ == "__main__":
    main()
