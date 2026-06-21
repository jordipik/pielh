"""
PIELH — Sincronización TAGs HOS con TheThings
Dos modos:
  --pull  Lee TAGs desde TheThings y actualiza hos en el master (TheThings → master)
  --push  Escribe TAGs HOS desde el master hacia TheThings   (master → TheThings)

Flags comunes:
  --dry-run       Simula sin guardar nada
  --limit N       Procesar solo N sensores
  --system S01    Filtrar por system_id
  --hos HOS001    Filtrar por HOS
  --sleep 0.2     Pausa entre peticiones (s)
  --no-ssl-verify Deshabilitar verificación SSL
"""

import csv
import json
import re
import shutil
import ssl
import time
import argparse
import urllib.request
import urllib.error
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

_HOS_PAT = re.compile(r'^HOS\d+$', re.IGNORECASE)

CSV_COLUMNS = [
    "sensor_id", "thing_id", "thing_token", "system_id",
    "hos_master", "hos_tag", "action", "status", "error",
]


# ---------------------------------------------------------------------------
# Config / backup
# ---------------------------------------------------------------------------

def load_config(base_dir: Path) -> dict:
    with open(base_dir / "config.json", encoding="utf-8") as f:
        return json.load(f)


def load_master(cfg: dict, base_dir: Path) -> dict:
    with open(base_dir / cfg["json_file"], encoding="utf-8") as f:
        return json.load(f)


def make_ssl_ctx(verify: bool) -> ssl.SSLContext:
    return ssl._create_unverified_context() if not verify else ssl.create_default_context()


def _backup(master_path: Path, backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = backup_dir / f"pielh_qa_master_{ts}.json"
    shutil.copy2(master_path, dst)
    backups = sorted(backup_dir.glob("pielh_qa_master_*.json"))
    for old in backups[:-20]:
        old.unlink(missing_ok=True)
    return dst


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def get_tags(api_base: str, token: str, thing_token: str,
             ssl_ctx: ssl.SSLContext, timeout: int = 10) -> Tuple[Optional[list], str]:
    """Returns (tags_list, error_msg). tags_list is None on error."""
    url = f"{api_base}/v2/things/{thing_token}/tags"
    req = urllib.request.Request(url, headers={"authorization": token})
    try:
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
            return data.get("tags", []), ""
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except Exception as e:
        return None, str(e)


def post_tag(api_base: str, token: str, thing_token: str, tag_name: str,
             ssl_ctx: ssl.SSLContext, timeout: int = 10) -> Tuple[bool, str]:
    """Returns (success, error_msg)."""
    url  = f"{api_base}/v2/things/{thing_token}/tags"
    body = json.dumps({"name": tag_name}).encode("utf-8")
    req  = urllib.request.Request(url, data=body, headers={
        "authorization":  token,
        "content-type":   "application/json",
    }, method="POST")
    try:
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=timeout) as r:
            json.loads(r.read().decode("utf-8"))
            return True, ""
    except urllib.error.HTTPError as e:
        body_resp = e.read().decode("utf-8", errors="replace")
        return False, f"HTTP {e.code}: {body_resp[:120]}"
    except Exception as e:
        return False, str(e)


def delete_tag(api_base: str, token: str, thing_token: str, tag_id: str,
               ssl_ctx: ssl.SSLContext, timeout: int = 10) -> Tuple[bool, str]:
    """Returns (success, error_msg)."""
    url = f"{api_base}/v2/things/{thing_token}/tags/{tag_id}"
    req = urllib.request.Request(url, headers={"authorization": token}, method="DELETE")
    try:
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=timeout) as r:
            r.read()
            return True, ""
    except urllib.error.HTTPError as e:
        body_resp = e.read().decode("utf-8", errors="replace")
        return False, f"HTTP {e.code}: {body_resp[:120]}"
    except Exception as e:
        return False, str(e)


def _find_hos_tag(tags: list) -> Optional[dict]:
    """Devuelve el primer tag cuyo name encaja con HOS\d+, o None."""
    for t in tags:
        if _HOS_PAT.match(str(t.get("name", ""))):
            return t
    return None


# ---------------------------------------------------------------------------
# PUSH: master → TheThings
# ---------------------------------------------------------------------------

def push_tags(master: dict, api_base: str, token: str, ssl_ctx: ssl.SSLContext,
              dry_run: bool, sleep_secs: float, sensors: list) -> list:
    """
    Para cada sensor con hos en el master:
      - Lee sus TAGs en TheThings
      - Si el TAG HOS está ausente → POST
      - Si el TAG HOS es distinto   → DELETE + POST
      - Si ya coincide              → already_ok
    """
    rows = []
    total = len(sensors)

    for i, sensor in enumerate(sensors, 1):
        sid    = sensor.get("id", "")
        tt     = sensor.get("thing_token", "")
        hos    = sensor.get("hos", "")
        sys_id = sensor.get("system_id", "")
        tid    = sensor.get("thing_id", "")

        row = {
            "sensor_id":   sid,
            "thing_id":    tid,
            "thing_token": tt,
            "system_id":   sys_id,
            "hos_master":  hos,
            "hos_tag":     "",
            "action":      "",
            "status":      "",
            "error":       "",
        }

        print(f"  [{i}/{total}] {sid} ...", end=" ", flush=True)

        if not hos:
            row["action"] = "skipped_no_hos"
            row["status"] = "SKIP"
            print("SKIP (sin HOS en master)")
            rows.append(row)
            continue

        if not tt:
            row["action"] = "skipped_no_token"
            row["status"] = "SKIP"
            print("SKIP (sin thing_token)")
            rows.append(row)
            continue

        tags, err = get_tags(api_base, token, tt, ssl_ctx)
        if tags is None:
            row["action"] = "error"
            row["status"] = "ERROR"
            row["error"]  = err
            print(f"ERROR get_tags: {err}")
            rows.append(row)
            if sleep_secs > 0:
                time.sleep(sleep_secs)
            continue

        existing = _find_hos_tag(tags)
        row["hos_tag"] = existing["name"] if existing else ""

        if existing and existing["name"].upper() == hos.upper():
            row["action"] = "already_ok"
            row["status"] = "OK"
            print("OK (tag ya correcto)")

        elif existing and existing["name"].upper() != hos.upper():
            # Tag HOS distinto: borrar el antiguo y crear el nuevo
            row["action"] = "updated"
            if not dry_run:
                ok_del, err_del = delete_tag(api_base, token, tt, existing["_id"], ssl_ctx)
                if not ok_del:
                    row["status"] = "ERROR"
                    row["error"]  = f"delete: {err_del}"
                    print(f"ERROR delete: {err_del}")
                    rows.append(row)
                    if sleep_secs > 0:
                        time.sleep(sleep_secs)
                    continue
                ok_post, err_post = post_tag(api_base, token, tt, hos, ssl_ctx)
                if ok_post:
                    row["status"] = "OK"
                    print(f"UPDATED {existing['name']} → {hos}")
                else:
                    row["status"] = "ERROR"
                    row["error"]  = f"post: {err_post}"
                    print(f"ERROR post: {err_post}")
            else:
                row["status"] = "DRY_RUN"
                print(f"DRY_RUN update {existing['name']} → {hos}")

        else:
            # Sin tag HOS: crear
            row["action"] = "pushed"
            if not dry_run:
                ok_post, err_post = post_tag(api_base, token, tt, hos, ssl_ctx)
                if ok_post:
                    row["status"] = "OK"
                    print(f"PUSHED {hos}")
                else:
                    row["status"] = "ERROR"
                    row["error"]  = err_post
                    print(f"ERROR post: {err_post}")
            else:
                row["status"] = "DRY_RUN"
                print(f"DRY_RUN push {hos}")

        rows.append(row)
        if sleep_secs > 0:
            time.sleep(sleep_secs)

    return rows


# ---------------------------------------------------------------------------
# PULL: TheThings → master
# ---------------------------------------------------------------------------

def pull_tags(master: dict, api_base: str, token: str, ssl_ctx: ssl.SSLContext,
              dry_run: bool, sleep_secs: float, sensors: list) -> list:
    """
    Para cada sensor:
      - Lee sus TAGs en TheThings
      - Si hay TAG HOS y el sensor no tiene hos en master → actualiza master
      - Si hay TAG HOS y master.hos difiere              → reporta conflict
      - Si ya coincide                                   → already_ok
    """
    rows = []
    total = len(sensors)

    for i, sensor in enumerate(sensors, 1):
        sid    = sensor.get("id", "")
        tt     = sensor.get("thing_token", "")
        hos    = sensor.get("hos", "")
        sys_id = sensor.get("system_id", "")
        tid    = sensor.get("thing_id", "")

        row = {
            "sensor_id":   sid,
            "thing_id":    tid,
            "thing_token": tt,
            "system_id":   sys_id,
            "hos_master":  hos,
            "hos_tag":     "",
            "action":      "",
            "status":      "",
            "error":       "",
        }

        print(f"  [{i}/{total}] {sid} ...", end=" ", flush=True)

        if not tt:
            row["action"] = "skipped_no_token"
            row["status"] = "SKIP"
            print("SKIP (sin thing_token)")
            rows.append(row)
            continue

        tags, err = get_tags(api_base, token, tt, ssl_ctx)
        if tags is None:
            row["action"] = "error"
            row["status"] = "ERROR"
            row["error"]  = err
            print(f"ERROR get_tags: {err}")
            rows.append(row)
            if sleep_secs > 0:
                time.sleep(sleep_secs)
            continue

        existing = _find_hos_tag(tags)
        tag_hos  = existing["name"].upper() if existing else None
        row["hos_tag"] = tag_hos or ""

        if not tag_hos:
            row["action"] = "no_tag"
            row["status"] = "OK"
            print("no_tag (TheThings sin HOS)")

        elif hos and hos.upper() == tag_hos:
            row["action"] = "already_ok"
            row["status"] = "OK"
            print("OK (master ya coincide)")

        elif hos and hos.upper() != tag_hos:
            row["action"] = "conflict"
            row["status"] = "WARN"
            print(f"CONFLICT master={hos} tag={tag_hos}")

        else:
            # master sin hos, tag tiene uno → actualizar master
            row["action"] = "updated"
            if not dry_run:
                sensor["hos"] = tag_hos
            row["status"] = "DRY_RUN" if dry_run else "OK"
            print(f"{'DRY_RUN ' if dry_run else ''}PULL hos={tag_hos}")

        rows.append(row)
        if sleep_secs > 0:
            time.sleep(sleep_secs)

    return rows


# ---------------------------------------------------------------------------
# Salida
# ---------------------------------------------------------------------------

def _stats(rows: list) -> dict:
    by_action = Counter(r["action"] for r in rows)
    by_status = Counter(r["status"] for r in rows)
    errors    = [r for r in rows if r["status"] == "ERROR"]
    return {
        "total":     len(rows),
        "by_action": dict(by_action),
        "by_status": dict(by_status),
        "errors":    errors,
    }


def save_outputs(rows: list, stats: dict, mode: str, out_dir: Path, ts_str: str):
    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = out_dir / f"thethings_tags_{mode}_{ts_str}.json"
    csv_path  = out_dir / f"thethings_tags_{mode}_{ts_str}.csv"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"generated_at": ts_str, "mode": mode, "stats": stats, "rows": rows},
                  f, ensure_ascii=False, indent=2)

    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    return json_path, csv_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="PIELH — Sync TAGs HOS con TheThings")
    mode_grp = parser.add_mutually_exclusive_group(required=True)
    mode_grp.add_argument("--push", action="store_true", help="master → TheThings")
    mode_grp.add_argument("--pull", action="store_true", help="TheThings → master")
    parser.add_argument("--dry-run",       action="store_true", help="Simular sin guardar")
    parser.add_argument("--limit",         type=int,   default=None)
    parser.add_argument("--system",        type=str,   default=None)
    parser.add_argument("--hos",           type=str,   default=None)
    parser.add_argument("--sleep",         type=float, default=0.2)
    parser.add_argument("--no-ssl-verify", action="store_true")
    args = parser.parse_args()

    mode     = "push" if args.push else "pull"
    base_dir = Path(__file__).resolve().parent.parent

    cfg        = load_config(base_dir)
    api_base   = cfg.get("thethings_api", "").rstrip("/")
    token      = cfg.get("thethings_token", "")
    master     = load_master(cfg, base_dir)
    master_path = base_dir / cfg["json_file"]
    backup_dir  = base_dir / "data" / "backups"
    out_dir     = base_dir / "data" / "audits"

    ssl_ctx = make_ssl_ctx(verify=not args.no_ssl_verify)

    sensors = master.get("sensors", [])

    # Filtros
    if args.system:
        sensors = [s for s in sensors if s.get("system_id") == args.system]
        print(f"[PIELH] Filtro sistema: {args.system} ({len(sensors)} sensores)")
    if args.hos:
        sensors = [s for s in sensors if s.get("hos") == args.hos]
        print(f"[PIELH] Filtro HOS: {args.hos} ({len(sensors)} sensores)")
    if mode == "push":
        sensors = [s for s in sensors if s.get("hos")]
        print(f"[PIELH] Sensores con HOS: {len(sensors)}")
    if args.limit:
        sensors = sensors[: args.limit]
        print(f"[PIELH] Límite: {args.limit} sensores")

    print(f"[PIELH] Modo: {mode.upper()} | Total: {len(sensors)} | API: {api_base}")
    if args.dry_run:
        print("[PIELH] DRY RUN — no se guardarán cambios")

    ts_start = datetime.now(timezone.utc)
    ts_str   = ts_start.strftime("%Y%m%d_%H%M%S")

    if mode == "push":
        rows = push_tags(master, api_base, token, ssl_ctx, args.dry_run, args.sleep, sensors)
    else:
        rows = pull_tags(master, api_base, token, ssl_ctx, args.dry_run, args.sleep, sensors)

    # Guardar master si pull + cambios + no dry-run
    if mode == "pull" and not args.dry_run:
        updated = [r for r in rows if r["action"] == "updated" and r["status"] == "OK"]
        if updated:
            backup_path = _backup(master_path, backup_dir)
            print(f"[PIELH] Backup: {backup_path.name}")
            with open(master_path, "w", encoding="utf-8") as f:
                json.dump(master, f, ensure_ascii=False, indent=2)
            print(f"[PIELH] Master guardado ({len(updated)} sensores actualizados).")

    stats    = _stats(rows)
    jp, cp   = save_outputs(rows, stats, mode, out_dir, ts_str)

    sep = "-" * 52
    print(f"\n[PIELH] RESULTADO {mode.upper()} {sep}")
    print(f"  Total procesados: {stats['total']}")
    for action, cnt in sorted(stats["by_action"].items()):
        print(f"  {action}: {cnt}")
    if stats["errors"]:
        print(f"\n  Errores ({len(stats['errors'])}):")
        for r in stats["errors"][:5]:
            print(f"    {r['sensor_id']}: {r['error']}")
    print(sep)
    print(f"  JSON: {jp}")
    print(f"  CSV:  {cp}")


if __name__ == "__main__":
    main()
