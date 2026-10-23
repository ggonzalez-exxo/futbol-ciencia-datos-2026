#!/usr/bin/env python3
"""
export_hf_data.py
-----------------
Exporta los datos de las animaciones a archivos JS que consumen las
composiciones de HyperFrames (video/hyperframes/assets/data/*.js).

Genera:
  - counter.js  : total de eventos
  - xt.js       : grilla xT por iteración
  - heatmap.js  : grillas 12x16 muestreadas de la figura VAEP de P3
  - umap.js     : embedding UMAP por jugador y cluster

Uso:
    .venv-video/bin/python video/scripts/export_hf_data.py
    # o con el entorno temporal de pruebas:
    /tmp/opencode/videoenv/bin/python video/scripts/export_hf_data.py
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
VIDEO = ROOT / "video"
OUT = VIDEO / "hyperframes" / "assets" / "data"

SPADL = ROOT / "notebooks" / "spadl_curado_PL_2017.parquet"
RANKINGS = ROOT / "notebooks" / "rankings_jugadores_PL_2017.csv"
VAEP_HEATMAP = VIDEO / "graficos" / "esc05" / "esc05_heatmap_vaep_messi_cr_dybala.png"
UMAP_CSV = VIDEO / "animaciones" / "umap_embedding.csv"

TOTAL_EVENTS = 3_251_294

# Paneles de Messi y Cristiano dentro de la figura VAEP de 3 paneles.
PANEL_BOXES = [
    (0.005, 0.350, 0.244, 0.872),
    (0.355, 0.350, 0.594, 0.872),
]
PLAYERS = [
    {"name": "L. Messi", "stat": "VAEP/partido: 0.972"},
    {"name": "Cristiano Ronaldo", "stat": "VAEP/partido: 0.581"},
]

M, N = 16, 12


def write_js(name: str, payload: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.js"
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    path.write_text(
        "window.HF_DATA = window.HF_DATA || {};\n"
        f"window.HF_DATA.{name} = {body};\n",
        encoding="utf-8",
    )
    print(f"  ✓ {path.relative_to(ROOT)} ({path.stat().st_size/1024:.0f} KB)")


# ---------------------------------------------------------------------------
# xT
# ---------------------------------------------------------------------------

def compute_xt(df: pd.DataFrame, max_iter: int = 30):
    x = df["start_x"].to_numpy()
    y = df["start_y"].to_numpy()
    ex = df["end_x"].to_numpy()
    ey = df["end_y"].to_numpy()

    xi = np.clip((x / 105 * M).astype(int), 0, M - 1)
    yi = np.clip((y / 68 * N).astype(int), 0, N - 1)
    z = xi * N + yi

    xe = np.clip((ex / 105 * M).astype(int), 0, M - 1)
    ye = np.clip((ey / 68 * N).astype(int), 0, N - 1)
    ze = xe * N + ye

    is_shot = df["type_name"].isin(["shot", "shot_freekick", "shot_penalty"]).to_numpy()
    is_goal = (df["result_name"] == "success").to_numpy() & is_shot

    dx = ex - x
    dy = ey - y
    moved = (np.abs(dx) + np.abs(dy)) > 1e-6
    is_move = (~is_shot) & moved

    n_actions = np.bincount(z, minlength=M * N)
    n_shots = np.bincount(z[is_shot], minlength=M * N)
    n_goals = np.bincount(z[is_goal], minlength=M * N)
    n_moves = np.bincount(z[is_move], minlength=M * N)

    T = np.zeros((M * N, M * N))
    np.add.at(T, (z[is_move], ze[is_move]), 1.0)
    with np.errstate(invalid="ignore", divide="ignore"):
        T = T / n_moves[:, None]

    shot_p = np.divide(n_shots, n_actions, out=np.zeros_like(n_shots, dtype=float), where=n_actions > 0)
    goal_p = np.divide(n_goals, n_shots, out=np.zeros_like(n_goals, dtype=float), where=n_shots > 0)
    move_p = np.divide(n_moves, n_actions, out=np.zeros_like(n_moves, dtype=float), where=n_actions > 0)

    xt = np.zeros(M * N)
    rows = []
    for it in range(max_iter):
        new = shot_p * goal_p + move_p * (T @ xt)
        dmax = float(np.max(np.abs(new - xt)))
        xt = new
        rows.append({"iter": it + 1, "dmax": round(dmax, 6), "values": xt.reshape(M, N).T.tolist()})
        if dmax < 1e-6:
            break
    return rows, float(xt.max())


def export_xt() -> None:
    print("xT...")
    df = pd.read_parquet(
        SPADL,
        columns=["type_name", "result_name", "start_x", "start_y", "end_x", "end_y"],
    )
    rows, vmax = compute_xt(df)
    rows = rows[:12]
    write_js(
        "xt",
        {
            "grid": {"m": M, "n": N},
            "iterations": rows,
            "max": round(vmax, 6),
            "source": "La Liga 2017/18 · 1.454.478 acciones SPADL",
        },
    )


# ---------------------------------------------------------------------------
# Heatmap VAEP (muestreada de la figura de P3)
# ---------------------------------------------------------------------------

def _crop_panel(img: Image.Image, box, size=(820, 540)) -> np.ndarray:
    w, h = img.size
    x0, y0, x1, y1 = box
    crop = img.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))
    return np.asarray(crop.resize(size, Image.Resampling.LANCZOS)).astype(np.float32)


def _luminance_grid(panel: np.ndarray) -> list[list[float]]:
    h, w, _ = panel.shape
    grid = np.zeros((N, M), dtype=np.float32)
    for j in range(N):
        for i in range(M):
            x0, x1 = int(i * w / M), int((i + 1) * w / M)
            y0, y1 = int(j * h / N), int((j + 1) * h / N)
            cell = panel[y0:y1, x0:x1].reshape(-1, 3)
            mn = cell.min(axis=1)
            mx = cell.max(axis=1)
            is_line = (mn > 150) & ((mx - mn) < 45)
            c = cell[~is_line] if (~is_line).sum() > 10 else cell
            med = np.median(c, axis=0)
            grid[j, i] = 0.2126 * med[0] + 0.7152 * med[1] + 0.0722 * med[2]
    return grid


def export_heatmap() -> None:
    print("heatmap...")
    if not VAEP_HEATMAP.exists():
        print(f"  ! falta {VAEP_HEATMAP.relative_to(ROOT)}; corré extraer_figuras.py")
        return
    img = Image.open(VAEP_HEATMAP).convert("RGB")
    panels = [_crop_panel(img, box) for box in PANEL_BOXES]
    grids = [_luminance_grid(p) for p in panels]
    vmax = max(float(np.percentile(g, 99.5)) for g in grids)
    norm = [np.clip(g / max(vmax, 1e-6), 0, 1) for g in grids]

    write_js(
        "heatmap",
        {
            "grid": {"m": M, "n": N},
            "players": PLAYERS,
            "panels": [
                {"name": PLAYERS[k]["name"], "stat": PLAYERS[k]["stat"], "values": norm[k].round(4).tolist()}
                for k in range(2)
            ],
            "source": "VAEP ofensivo por zona · P3 · DiploDatos 2026",
        },
    )


# ---------------------------------------------------------------------------
# UMAP
# ---------------------------------------------------------------------------

CLUSTERS = {
    0: {"name": "Finalizadores", "color": "#F59E0B"},
    1: {"name": "Defensores / volantes", "color": "#22D3EE"},
    2: {"name": "Arqueros", "color": "#94A3B8"},
    3: {"name": "Creadores", "color": "#22C55E"},
}


def export_umap() -> None:
    print("umap...")
    if not UMAP_CSV.exists():
        print(f"  ! falta {UMAP_CSV.relative_to(ROOT)}; corré generar_animaciones.py --solo umap")
        return
    players = []
    with UMAP_CSV.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            players.append(
                {
                    "id": int(row["player_id"]),
                    "name": row["jugador"],
                    "cluster": int(row["cluster"]),
                    "x": round(float(row["umap_x"]), 4),
                    "y": round(float(row["umap_y"]), 4),
                    "vaep": round(float(row["vaep_p90"]), 4),
                }
            )
    write_js(
        "umap",
        {
            "players": players,
            "clusters": {str(k): v for k, v in CLUSTERS.items()},
            "count": len(players),
            "source": "1.201 jugadores · K-Means (k=4) · 21 features",
        },
    )


def export_counter() -> None:
    print("counter...")
    write_js(
        "counter",
        {
            "total": TOTAL_EVENTS,
            "source": "Temporada 2017/18 · Wyscout",
            "caption": "eventos de juego registrados",
        },
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    export_counter()
    export_xt()
    export_heatmap()
    export_umap()
    print(f"\nListo: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
