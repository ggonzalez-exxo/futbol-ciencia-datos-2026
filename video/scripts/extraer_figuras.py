#!/usr/bin/env python3
"""
extraer_figuras.py
------------------
Extrae todas las figuras (PNG/SVG) incrustadas en los notebooks del proyecto
y las guarda en video/graficos/ con nombres listos para importar en Kdenlive.

Uso:
    python video/scripts/extraer_figuras.py
    python video/scripts/extraer_figuras.py --out video/graficos

No necesita pandas ni matplotlib: solo la librería estándar de Python.
"""

from __future__ import annotations

import argparse
import base64
import csv
import json
import re
import unicodedata
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

NOTEBOOKS = {
    "p1": "P1_Analisis_Visualizacion.ipynb",
    "p2": "P2_EDA_Curacion_SPADL.ipynb",
    "p3": "P3_Supervisado_NoSupervisado.ipynb",
}

# Figuras clave: (notebook, celda) -> nombre amigable.
# El prefijo escNN indica la escena del guion a la que pertenece.
ALIASES: dict[tuple[str, int], str] = {
    # --- Escena 3: TP1 -----------------------------------------------------
    ("p1", 24): "esc03_shotmap",
    ("p1", 26): "esc03_heatmap_densidad",
    ("p1", 29): "esc03_heatmap_equipos",
    ("p1", 32): "esc03_xg_curva",
    ("p1", 38): "esc03_red_pases_barcelona",
    ("p1", 45): "esc03_radar_kroos",
    ("p1", 46): "esc03_radar_cristiano",
    ("p1", 50): "esc03_pases_progresivos",
    ("p1", 58): "esc03_shotmap_barca_vs_madrid",
    ("p1", 65): "esc03_xg_acumulado",
    ("p1", 72): "esc03_red_pases_villarreal",
    ("p1", 74): "esc03_red_pases_villarreal_mitades",
    ("p1", 79): "esc03_radar_mediocampistas",
    ("p1", 80): "esc03_radar_mediocampistas_2",
    ("p1", 81): "esc03_radar_mediocampistas_3",
    ("p1", 82): "esc03_radar_mediocampistas_4",
    ("p1", 87): "esc03_pressing_equipos",
    ("p1", 89): "esc03_pressing_barras",
    ("p1", 91): "esc03_pressing_heatmaps",
    # --- Escena 4: TP2 -----------------------------------------------------
    ("p2", 31): "esc04_heatmap_eventos",
    ("p2", 99): "esc04_distribucion_temporal",
    ("p2", 100): "esc04_distribucion_temporal_2",
    ("p2", 110): "esc04_features",
    ("p2", 119): "esc04_sesgo_posicional",
    # --- Escena 5: TP3 -----------------------------------------------------
    ("p3", 9): "esc05_xt_grilla",
    ("p3", 20): "esc05_vaep_distribucion",
    ("p3", 22): "esc05_shap_1",
    ("p3", 23): "esc05_shap_2",
    ("p3", 24): "esc05_shap_3",
    ("p3", 27): "esc05_vaep_vs_xt",
    ("p3", 31): "esc05_clustering_codo",
    ("p3", 33): "esc05_clusters_perfiles",
    ("p3", 35): "esc05_umap",
    ("p3", 38): "esc05_scouting_messi",
    ("p3", 45): "esc05_xt_grilla_32x24",
    ("p3", 60): "esc05_heatmap_vaep_messi_cr_dybala",
    ("p3", 61): "esc05_flujo_vaep",
    ("p3", 62): "esc05_tiros_pases_top",
    ("p3", 63): "esc05_flujo_vaep_2",
    ("p3", 64): "esc05_flujo_vaep_3",
    ("p3", 68): "esc05_clusters_por_liga",
    ("p3", 69): "esc05_clusters_por_liga_perfiles",
    ("p3", 77): "esc05_scouting_iniesta",
    ("p3", 78): "esc05_scouting_messi_2",
}


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def slugify(text: str, max_len: int = 60) -> str:
    """Convierte un título en un nombre de archivo seguro."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_").lower()
    return text[:max_len] or "figura"


def decode_image(data) -> bytes:
    """Decodifica el campo image/png (str o lista de str) a bytes."""
    if isinstance(data, list):
        data = "".join(data)
    return base64.b64decode(data)


def last_heading(cells: list, idx: int) -> str:
    """Busca el último encabezado markdown antes de la celda idx."""
    for j in range(idx, -1, -1):
        cell = cells[j]
        if cell.get("cell_type") != "markdown":
            continue
        lines = "".join(cell.get("source", [])).strip().splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith("#"):
                return line.lstrip("#").strip()
    return ""


def scene_from_alias(alias: str | None) -> str:
    if alias and alias.startswith("esc"):
        return alias[:5]
    return "otros"


# ---------------------------------------------------------------------------
# Extracción
# ---------------------------------------------------------------------------

def extract(repo: Path, out_root: Path) -> list[dict]:
    rows: list[dict] = []

    for nb_key, nb_name in NOTEBOOKS.items():
        nb_path = repo / "notebooks" / nb_name
        if not nb_path.exists():
            print(f"  ! No existe {nb_path}")
            continue

        nb = json.loads(nb_path.read_text(encoding="utf-8"))
        cells = nb.get("cells", [])
        print(f"\n[{nb_key}] {nb_name} — {len(cells)} celdas")

        for idx, cell in enumerate(cells):
            if cell.get("cell_type") != "code":
                continue

            images: list[tuple[str, bytes]] = []
            for output in cell.get("outputs", []):
                data = output.get("data", {})
                if "image/png" in data:
                    images.append(("png", decode_image(data["image/png"])))
                elif "image/svg+xml" in data:
                    svg = data["image/svg+xml"]
                    if isinstance(svg, list):
                        svg = "".join(svg)
                    images.append(("svg", svg.encode("utf-8")))

            if not images:
                continue

            heading = last_heading(cells, idx)
            alias = ALIASES.get((nb_key, idx))
            scene = scene_from_alias(alias)
            dest_dir = out_root / scene
            dest_dir.mkdir(parents=True, exist_ok=True)

            for j, (ext, blob) in enumerate(images, start=1):
                if alias:
                    base = alias
                    if len(images) > 1:
                        base = f"{base}_{j}"
                else:
                    base = f"{nb_key}_cell{idx:03d}_{slugify(heading or 'figura')}"
                    if len(images) > 1:
                        base = f"{base}_{j}"

                dest = dest_dir / f"{base}.{ext}"
                dest.write_bytes(blob)

                rows.append(
                    {
                        "notebook": nb_key,
                        "cell": idx,
                        "image_index": j,
                        "scene": scene,
                        "filename": dest.relative_to(out_root).as_posix(),
                        "heading": heading,
                        "bytes": len(blob),
                    }
                )
                print(f"  ✓ {dest.relative_to(out_root)} ({len(blob)/1024:.0f} KB)")

    return rows


def write_manifest(rows: list[dict], out_root: Path) -> None:
    manifest = out_root / "manifest.csv"
    with manifest.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["notebook", "cell", "image_index", "scene", "filename", "heading", "bytes"],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nManifiesto: {manifest} ({len(rows)} figuras)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extrae figuras de los notebooks.")
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Raíz del repositorio (por defecto: dos niveles arriba de este script).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Carpeta de salida (por defecto: <repo>/video/graficos).",
    )
    args = parser.parse_args()

    repo = args.repo.resolve()
    out_root = (args.out or repo / "video" / "graficos").resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    print(f"Repositorio : {repo}")
    print(f"Salida      : {out_root}")

    rows = extract(repo, out_root)
    write_manifest(rows, out_root)

    if not rows:
        raise SystemExit("No se encontraron imágenes en los notebooks.")


if __name__ == "__main__":
    main()
