#!/usr/bin/env python3
"""
generar_animaciones.py
----------------------
Genera las animaciones del video final a partir de los datos del proyecto:

  1. Contador de eventos (escena 0).
  2. Grilla xT iterando (escena 5).
  3. Heat maps de Messi y Cristiano iluminándose por escala (escena 5),
     a partir de la figura VAEP extraída del notebook P3.
  4. UMAP de jugadores por arquetipo (escena 5).

Salidas: video/animaciones/*.mp4 y algunos PNG de referencia.

Uso:
    # Requiere haber corrido antes: video/scripts/extraer_figuras.py
    python video/scripts/generar_animaciones.py
    python video/scripts/generar_animaciones.py --solo xt,heatmap
    python video/scripts/generar_animaciones.py --solo umap

Dependencias: numpy, pandas, pyarrow, matplotlib, mplsoccer,
              scikit-learn, umap-learn, pillow (ver requirements.txt).
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap
from mplsoccer import Pitch
from PIL import Image, ImageDraw, ImageFont

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# Rutas y estilo
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]
VIDEO = ROOT / "video"
OUT = VIDEO / "animaciones"
GRAF = VIDEO / "graficos"

SPADL_PATH = ROOT / "notebooks" / "spadl_curado_PL_2017.parquet"
RANKINGS_PATH = ROOT / "notebooks" / "rankings_jugadores_PL_2017.csv"
VAEP_HEATMAP = GRAF / "esc05" / "esc05_heatmap_vaep_messi_cr_dybala.png"

FPS = 30
W, H = 1920, 1080

BG = "#0E1116"
PANEL_BG = "#111820"
LINE = "#3A4656"
TEXT = "#E5E7EB"
MUTED = "#9AA3AD"

CLUSTER_COLORS = {
    0: "#F59E0B",  # finalizadores
    1: "#22D3EE",  # defensores / volantes
    2: "#94A3B8",  # arqueros
    3: "#22C55E",  # creadores
}
CLUSTER_NAMES = {
    0: "Finalizadores",
    1: "Defensores / volantes",
    2: "Arqueros",
    3: "Creadores",
}

# Fuente para las composiciones con PIL
def _font_path(bold: bool = False) -> str:
    return font_manager.findfont(
        font_manager.FontProperties(family="DejaVu Sans", weight="bold" if bold else "normal")
    )


FONT_BOLD = _font_path(True)
FONT_REG = _font_path(False)

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "text.color": TEXT,
        "axes.labelcolor": TEXT,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "figure.facecolor": BG,
        "axes.facecolor": BG,
        "savefig.facecolor": BG,
        "savefig.bbox": "standard",
        "savefig.pad_inches": 0,
    }
)


# ---------------------------------------------------------------------------
# Helpers de video
# ---------------------------------------------------------------------------

def encode_frames(frames_dir: Path, out: Path, fps: int = FPS) -> None:
    """Codifica frame_0001.png ... en un MP4 H.264."""
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-framerate", str(fps),
        "-i", str(frames_dir / "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "medium",
        "-movflags", "+faststart",
        str(out),
    ]
    subprocess.run(cmd, check=True)
    print(f"  → {out.relative_to(ROOT)}")


def save_frame(fig, path: Path, dpi: int = 120) -> None:
    fig.savefig(path, dpi=dpi, facecolor=fig.get_facecolor())
    plt.close(fig)


def ease_in_out(t: float) -> float:
    """Suaviza una progresión 0→1."""
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------------------
# 1. Contador de eventos
# ---------------------------------------------------------------------------

def animar_contador(out_dir: Path, total: int = 3_251_294, fps: int = FPS) -> None:
    print("\n[1/4] Contador de eventos")
    frames = 90
    with tempfile.TemporaryDirectory(prefix="frames_contador_") as tmp:
        tmp = Path(tmp)
        f_num = ImageFont.truetype(FONT_BOLD, 190)
        f_sub = ImageFont.truetype(FONT_REG, 38)
        f_tag = ImageFont.truetype(FONT_REG, 28)

        for i in range(frames):
            t = i / (frames - 1)
            value = int(total * (1 - (1 - t) ** 3))
            img = Image.new("RGB", (W, H), BG)
            d = ImageDraw.Draw(img)

            # Barra de progreso inferior
            d.rectangle([160, 930, W - 160, 936], fill="#1F2937")
            d.rectangle([160, 930, 160 + int((W - 320) * t), 936], fill="#22C55E")

            txt = f"{value:,}".replace(",", ".")
            bbox = d.textbbox((0, 0), txt, font=f_num)
            d.text(((W - (bbox[2] - bbox[0])) / 2, 390), txt, font=f_num, fill=TEXT)

            sub = "eventos de juego registrados"
            bbox = d.textbbox((0, 0), sub, font=f_sub)
            d.text(((W - (bbox[2] - bbox[0])) / 2, 620), sub, font=f_sub, fill=MUTED)

            tag = "Temporada 2017/18  ·  Wyscout"
            bbox = d.textbbox((0, 0), tag, font=f_tag)
            d.text(((W - (bbox[2] - bbox[0])) / 2, 690), tag, font=f_tag, fill="#4B5563")

            img.save(tmp / f"frame_{i + 1:04d}.png")

        encode_frames(tmp, out_dir / "esc00_contador_eventos.mp4", fps)


# ---------------------------------------------------------------------------
# 2. Grilla xT iterando
# ---------------------------------------------------------------------------

def compute_xt(df: pd.DataFrame, M: int = 16, N: int = 12, max_iter: int = 30):
    """Calcula la grilla xT y devuelve el historial de iteraciones."""
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
    history = [xt.reshape(M, N).T.copy()]
    dmaxs = []
    for _ in range(max_iter):
        new = shot_p * goal_p + move_p * (T @ xt)
        dmax = float(np.max(np.abs(new - xt)))
        xt = new
        dmaxs.append(dmax)
        history.append(xt.reshape(M, N).T.copy())
        if dmax < 1e-6:
            break

    return history, dmaxs


def animar_xt(df: pd.DataFrame, out_dir: Path, fps: int = FPS) -> None:
    print("\n[2/4] Grilla xT iterando")
    M, N = 16, 12
    history, dmaxs = compute_xt(df, M=M, N=N)

    # Nos quedamos con las primeras 12 iteraciones (las que muestran la convergencia)
    n_iter = min(12, len(history) - 1)
    history = history[1 : n_iter + 1]
    dmaxs = dmaxs[:n_iter]
    vmax = max(float(np.max(g)) for g in history)

    pitch = Pitch(
        pitch_type="custom",
        pitch_length=105,
        pitch_width=68,
        pitch_color=PANEL_BG,
        line_color="#C7D2DE",
        linewidth=1.2,
    )

    with tempfile.TemporaryDirectory(prefix="frames_xt_") as tmp:
        tmp = Path(tmp)
        frame_id = 1
        hold = 7

        for k, grid in enumerate(history, start=1):
            for _ in range(hold):
                fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
                fig.patch.set_facecolor(BG)
                ax.set_facecolor(BG)
                pitch.draw(ax=ax)

                im = ax.imshow(
                    grid,
                    extent=(0, 105, 0, 68),
                    origin="lower",
                    cmap="viridis",
                    vmin=0,
                    vmax=vmax,
                    alpha=0.92,
                    interpolation="nearest",
                    zorder=1,
                )
                pitch.draw(ax=ax)

                # Retícula tenue
                for gx in np.linspace(0, 105, M + 1):
                    ax.axvline(gx, color="white", alpha=0.10, lw=0.6, zorder=2)
                for gy in np.linspace(0, 68, N + 1):
                    ax.axhline(gy, color="white", alpha=0.10, lw=0.6, zorder=2)

                ax.set_xlim(-2, 107)
                ax.set_ylim(-2, 70)
                ax.axis("off")

                fig.text(0.5, 0.94, "Expected Threat (xT)", ha="center", va="center",
                         fontsize=34, fontweight="bold", color=TEXT)
                fig.text(0.5, 0.885, f"Grilla {M} × {N} · iteración {k} de {n_iter}",
                         ha="center", va="center", fontsize=19, color=MUTED)
                fig.text(0.5, 0.06, f"Δmax = {dmaxs[k-1]:.4f}", ha="center", va="center",
                         fontsize=16, color=MUTED, family="monospace")

                cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.01)
                cbar.set_label("Amenaza esperada", color=TEXT, fontsize=13)
                cbar.ax.yaxis.set_tick_params(color=MUTED, labelcolor=MUTED)

                fig.subplots_adjust(left=0.04, right=0.90, top=0.84, bottom=0.10)
                fig.savefig(tmp / f"frame_{frame_id:04d}.png", dpi=120, facecolor=BG)
                plt.close(fig)
                frame_id += 1

        # Frame final con más contraste
        fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
        fig.patch.set_facecolor(BG)
        ax.set_facecolor(BG)
        pitch.draw(ax=ax)
        im = ax.imshow(history[-1], extent=(0, 105, 0, 68), origin="lower",
                       cmap="viridis", vmin=0, vmax=vmax, alpha=0.95,
                       interpolation="nearest", zorder=1)
        pitch.draw(ax=ax)
        for gx in np.linspace(0, 105, M + 1):
            ax.axvline(gx, color="white", alpha=0.10, lw=0.6, zorder=2)
        for gy in np.linspace(0, 68, N + 1):
            ax.axhline(gy, color="white", alpha=0.10, lw=0.6, zorder=2)
        ax.set_xlim(-2, 107); ax.set_ylim(-2, 70); ax.axis("off")
        fig.text(0.5, 0.94, "Expected Threat (xT)", ha="center", va="center",
                 fontsize=34, fontweight="bold", color=TEXT)
        fig.text(0.5, 0.885, "Grilla final 16 × 12 · convergencia",
                 ha="center", va="center", fontsize=19, color=MUTED)
        cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.01)
        cbar.set_label("Amenaza esperada", color=TEXT, fontsize=13)
        cbar.ax.yaxis.set_tick_params(color=MUTED, labelcolor=MUTED)
        fig.subplots_adjust(left=0.04, right=0.90, top=0.84, bottom=0.10)
        fig.savefig(tmp / f"frame_{frame_id:04d}.png", dpi=120, facecolor=BG)
        fig.savefig(GRAF / "esc05" / "esc05_xt_grilla_final.png", dpi=120, facecolor=BG)
        plt.close(fig)
        for _ in range(30):
            shutil.copy(tmp / f"frame_{frame_id:04d}.png", tmp / f"frame_{frame_id + 1:04d}.png")
            frame_id += 1

        encode_frames(tmp, out_dir / "esc05_xt_grilla.mp4", fps)


# ---------------------------------------------------------------------------
# 3. Heat maps VAEP de Messi y Cristiano, iluminándose
# ---------------------------------------------------------------------------

# Fracciones (x0, y0, x1, y1) de los paneles de Messi y Cristiano dentro de la
# figura de 3 paneles exportada por el notebook P3.
PANEL_BOXES = [
    (0.005, 0.350, 0.244, 0.872),  # Messi
    (0.355, 0.350, 0.594, 0.872),  # Cristiano
]
PLAYERS_HEATMAP = [
    ("L. Messi", "VAEP/partido: 0.972"),
    ("Cristiano Ronaldo", "VAEP/partido: 0.581"),
]


def _crop_panel(img: Image.Image, box: tuple[float, float, float, float],
                size: tuple[int, int]) -> np.ndarray:
    w, h = img.size
    x0, y0, x1, y1 = box
    crop = img.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))
    return np.asarray(crop.resize(size, Image.Resampling.LANCZOS)).astype(np.float32)


def _line_mask(panel: np.ndarray) -> np.ndarray:
    """Píxeles claros y neutros (líneas de la cancha), para conservarlos."""
    mn = panel.min(axis=2)
    mx = panel.max(axis=2)
    return (mn > 150) & ((mx - mn) < 45)


def _grid_luminance(panel: np.ndarray, M: int = 16, N: int = 12) -> np.ndarray:
    """Muestrea la luminancia media de cada celda de la grilla M×N."""
    h, w, _ = panel.shape
    grid = np.zeros((N, M), dtype=np.float32)
    for j in range(N):
        for i in range(M):
            x0, x1 = int(i * w / M), int((i + 1) * w / M)
            y0, y1 = int(j * h / N), int((j + 1) * h / N)
            cell = panel[y0:y1, x0:x1].reshape(-1, 3)
            # Ignorar líneas blancas para no contaminar la escala
            mn = cell.min(axis=1)
            mx = cell.max(axis=1)
            is_line = (mn > 150) & ((mx - mn) < 45)
            c = cell[~is_line] if (~is_line).sum() > 10 else cell
            med = np.median(c, axis=0)
            grid[j, i] = 0.2126 * med[0] + 0.7152 * med[1] + 0.0722 * med[2]
    return grid


def _mask_until(panel: np.ndarray, grid_norm: np.ndarray, t: float) -> np.ndarray:
    """Oculta las celdas cuya intensidad normalizada supera t.

    Las líneas de la cancha se conservan siempre.
    """
    h, w, _ = panel.shape
    N, M = grid_norm.shape
    out = panel.copy()
    bg = np.array([14, 17, 22], dtype=np.float32)
    lines = _line_mask(panel)

    for j in range(N):
        for i in range(M):
            if grid_norm[j, i] <= t:
                continue
            x0, x1 = int(i * w / M), int((i + 1) * w / M)
            y0, y1 = int(j * h / N), int((j + 1) * h / N)
            cell = out[y0:y1, x0:x1]
            lm = lines[y0:y1, x0:x1]
            cell[~lm] = bg
    return np.clip(out, 0, 255)


def _gradient_bar(width: int, height: int, cmap_name: str = "viridis") -> Image.Image:
    cmap = plt.get_cmap(cmap_name)
    grad = (np.linspace(0, 1, width) * 255).astype(np.uint8)
    arr = (cmap(grad / 255)[:, :3] * 255).astype(np.uint8)
    arr = np.repeat(arr[None, :, :], height, axis=0)
    return Image.fromarray(arr, "RGB")


def animar_heatmap_vaep(out_dir: Path, fps: int = FPS) -> None:
    print("\n[3/4] Heat maps VAEP Messi / Cristiano")
    if not VAEP_HEATMAP.exists():
        print(f"  ! No existe {VAEP_HEATMAP.relative_to(ROOT)}")
        print("    Corré primero: python video/scripts/extraer_figuras.py")
        return

    src = Image.open(VAEP_HEATMAP).convert("RGB")
    panel_size = (820, 540)
    panels = [_crop_panel(src, box, panel_size) for box in PANEL_BOXES]

    grids = [_grid_luminance(p) for p in panels]
    vmax = max(np.percentile(g, 99.5) for g in grids)
    grids_norm = [np.clip(g / max(vmax, 1e-6), 0, 1) for g in grids]

    f_title = ImageFont.truetype(FONT_BOLD, 56)
    f_sub = ImageFont.truetype(FONT_REG, 32)
    f_name = ImageFont.truetype(FONT_BOLD, 32)
    f_stat = ImageFont.truetype(FONT_REG, 25)
    f_small = ImageFont.truetype(FONT_REG, 22)

    grad = _gradient_bar(760, 22)

    with tempfile.TemporaryDirectory(prefix="frames_heatmap_") as tmp:
        tmp = Path(tmp)
        frames = 96
        hold = 18
        total = frames + hold

        for i in range(total):
            if i < frames:
                t = ease_in_out(i / (frames - 1))
            else:
                t = 1.0

            canvas = Image.new("RGB", (W, H), BG)
            d = ImageDraw.Draw(canvas)

            # Título
            title = "Zonas calientes de generación de valor"
            bbox = d.textbbox((0, 0), title, font=f_title)
            d.text(((W - (bbox[2] - bbox[0])) / 2, 52), title, font=f_title, fill=TEXT)

            sub = "VAEP ofensivo por zona  ·  temporada 2017/18"
            bbox = d.textbbox((0, 0), sub, font=f_sub)
            d.text(((W - (bbox[2] - bbox[0])) / 2, 130), sub, font=f_sub, fill=MUTED)

            # Paneles
            xs = [110, 1010]
            ys = 255
            for k, (panel, grid_norm) in enumerate(zip(panels, grids_norm)):
                shown = _mask_until(panel, grid_norm, t).astype(np.uint8)
                pil = Image.fromarray(shown, "RGB")
                canvas.paste(pil, (xs[k], ys))
                d.rectangle([xs[k], ys, xs[k] + panel_size[0], ys + panel_size[1]],
                            outline="#2B3645", width=2)

                name, stat = PLAYERS_HEATMAP[k]
                bbox = d.textbbox((0, 0), name, font=f_name)
                d.text((xs[k] + (panel_size[0] - (bbox[2] - bbox[0])) / 2, ys - 45),
                       name, font=f_name, fill=TEXT)
                bbox = d.textbbox((0, 0), stat, font=f_stat)
                d.text((xs[k] + (panel_size[0] - (bbox[2] - bbox[0])) / 2, ys + panel_size[1] + 14),
                       stat, font=f_stat, fill=MUTED)

            # Barra de escala
            bar_x = (W - 760) // 2
            bar_y = 910
            canvas.paste(grad, (bar_x, bar_y))
            d.text((bar_x - 110, bar_y - 4), "menor", font=f_small, fill=MUTED)
            d.text((bar_x + 775, bar_y - 4), "mayor", font=f_small, fill=MUTED)
            label = "VAEP ofensivo"
            bbox = d.textbbox((0, 0), label, font=f_small)
            d.text(((W - (bbox[2] - bbox[0])) / 2, bar_y - 40), label, font=f_small, fill=TEXT)

            canvas.save(tmp / f"frame_{i + 1:04d}.png")

        encode_frames(tmp, out_dir / "esc05_heatmap_vaep.mp4", fps)

    # Frame final como PNG de referencia
    final = _mask_until(panels[0], grids_norm[0], 1.0)
    Image.fromarray(final.astype(np.uint8), "RGB").save(
        GRAF / "esc05" / "esc05_heatmap_vaep_messi_final.png"
    )


# ---------------------------------------------------------------------------
# 4. UMAP de jugadores
# ---------------------------------------------------------------------------

def build_umap_data() -> pd.DataFrame:
    print("  Cargando acciones y perfiles...")
    df = pd.read_parquet(SPADL_PATH, columns=["player_id", "type_name"])
    profile = df.groupby(["player_id", "type_name"]).size().unstack(fill_value=0)
    profile = profile[profile.sum(axis=1) >= 100]
    profile = profile.div(profile.sum(axis=1), axis=0)

    rank = pd.read_csv(RANKINGS_PATH).set_index("player_id")
    pv = profile.join(rank[["vaep_p90", "off_total", "def_total", "cluster", "jugador"]], how="inner")
    # Incluimos player_id 0 (jugador desconocido de Wyscout) para reproducir
    # exactamente los 1.201 jugadores y los tamaños de cluster del notebook P3.
    pv = pv.copy()

    action_cols = profile.columns.tolist()
    feat_cols = action_cols + ["vaep_p90", "off_total", "def_total"]
    X = pv[feat_cols].to_numpy(dtype=float)

    from sklearn.preprocessing import StandardScaler

    Xs = StandardScaler().fit_transform(X)

    print(f"  Jugadores: {len(pv)} · features: {len(feat_cols)}")
    print("  Calculando UMAP (puede tardar ~20 s)...")
    import umap

    emb = umap.UMAP(
        n_components=2,
        n_neighbors=15,
        min_dist=0.1,
        metric="cosine",
        random_state=42,
    ).fit_transform(Xs)

    pv = pv.reset_index()
    pv["umap_x"] = emb[:, 0]
    pv["umap_y"] = emb[:, 1]
    pv["cluster"] = pv["cluster"].astype(int)
    return pv


def animar_umap(umap_df: pd.DataFrame, out_dir: Path, fps: int = FPS) -> None:
    print("\n[4/4] UMAP de jugadores")
    out_csv = out_dir / "umap_embedding.csv"
    umap_df[["player_id", "jugador", "cluster", "umap_x", "umap_y", "vaep_p90"]].to_csv(
        out_csv, index=False
    )
    print(f"  Embedding guardado: {out_csv.relative_to(ROOT)}")

    # Anotaciones de jugadores destacados (por player_id) con offset manual
    # para evitar que se pisen entre sí.
    stars = {
        3359: ("Messi", (16, 12)),
        120353: ("Salah", (-70, 14)),
        3322: ("Cristiano", (16, -24)),
        3353: ("Iniesta", (16, -22)),
    }

    xs = umap_df["umap_x"].to_numpy()
    ys = umap_df["umap_y"].to_numpy()
    cl = umap_df["cluster"].to_numpy()
    ids = umap_df["player_id"].to_numpy()

    fig_frames = 25
    hold = 30
    total = fig_frames * 4 + hold
    frame_id = 1

    with tempfile.TemporaryDirectory(prefix="frames_umap_") as tmp:
        tmp = Path(tmp)

        for i in range(total):
            fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
            fig.patch.set_facecolor(BG)
            ax.set_facecolor(BG)

            if i < fig_frames * 4:
                active = i // fig_frames  # 0..3
                frac = (i % fig_frames + 1) / fig_frames
            else:
                active = 3
                frac = 1.0

            for c in range(4):
                mask = cl == c
                color = CLUSTER_COLORS[c]
                if c < active:
                    n_show = mask.sum()
                elif c == active:
                    n_show = int(mask.sum() * ease_in_out(frac))
                else:
                    n_show = 0

                if n_show == 0:
                    continue
                idx = np.where(mask)[0][:n_show]
                ax.scatter(xs[idx], ys[idx], s=20, c=color, alpha=0.85,
                           edgecolors="none", zorder=3)

            # Etiquetas de cluster (aparecen al completarse)
            for c in range(4):
                if c < active or (c == active and frac > 0.55):
                    mask = cl == c
                    cx, cy = np.median(xs[mask]), np.median(ys[mask])
                    ax.text(cx, cy + 0.35, CLUSTER_NAMES[c], ha="center", va="bottom",
                            fontsize=15, fontweight="bold", color=CLUSTER_COLORS[c],
                            alpha=0.95, zorder=5,
                            bbox=dict(boxstyle="round,pad=0.28", facecolor=BG,
                                      edgecolor=CLUSTER_COLORS[c], alpha=0.75))

            # Jugadores destacados al final
            if i >= fig_frames * 4 - 10:
                alpha = 0.0
                if i >= fig_frames * 4 - 10:
                    alpha = min(1.0, (i - (fig_frames * 4 - 10)) / 10)
                for pid, (name, offset) in stars.items():
                    hit = np.where(ids == pid)[0]
                    if len(hit) == 0:
                        continue
                    k = hit[0]
                    ax.annotate(
                        name, (xs[k], ys[k]), xytext=offset,
                        textcoords="offset points", fontsize=10, color=TEXT,
                        alpha=alpha, zorder=6,
                    )

            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_visible(False)

            fig.text(0.5, 0.945, "UMAP — espacio de jugadores por perfil de juego",
                     ha="center", va="center", fontsize=30, fontweight="bold", color=TEXT)
            fig.text(0.5, 0.895, "1.201 jugadores  ·  K-Means (k=4)  ·  21 features",
                     ha="center", va="center", fontsize=17, color=MUTED)

            fig.subplots_adjust(left=0.03, right=0.97, top=0.86, bottom=0.05)
            fig.savefig(tmp / f"frame_{frame_id:04d}.png", dpi=120, facecolor=BG)
            plt.close(fig)
            frame_id += 1

        encode_frames(tmp, out_dir / "esc05_umap_clusters.mp4", fps)

    # PNG final de referencia
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    for c in range(4):
        mask = cl == c
        ax.scatter(xs[mask], ys[mask], s=22, c=CLUSTER_COLORS[c], alpha=0.85,
                   edgecolors="none", label=f"{CLUSTER_NAMES[c]} (n={mask.sum()})", zorder=3)
    for c in range(4):
        mask = cl == c
        ax.text(np.median(xs[mask]), np.median(ys[mask]) + 0.35, CLUSTER_NAMES[c],
                ha="center", va="bottom", fontsize=15, fontweight="bold",
                color=CLUSTER_COLORS[c], zorder=5,
                bbox=dict(boxstyle="round,pad=0.28", facecolor=BG,
                          edgecolor=CLUSTER_COLORS[c], alpha=0.75))
    for pid, (name, offset) in stars.items():
        hit = np.where(ids == pid)[0]
        if len(hit) == 0:
            continue
        k = hit[0]
        ax.annotate(name, (xs[k], ys[k]), xytext=offset, textcoords="offset points",
                    fontsize=10, color=TEXT, zorder=6)
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.legend(loc="upper right", frameon=False, labelcolor=TEXT, fontsize=11)
    fig.text(0.5, 0.945, "UMAP — espacio de jugadores por perfil de juego",
             ha="center", va="center", fontsize=30, fontweight="bold", color=TEXT)
    fig.text(0.5, 0.895, "1.201 jugadores  ·  K-Means (k=4)  ·  21 features",
             ha="center", va="center", fontsize=17, color=MUTED)
    fig.subplots_adjust(left=0.03, right=0.97, top=0.86, bottom=0.05)
    fig.savefig(GRAF / "esc05" / "esc05_umap_final.png", dpi=120, facecolor=BG)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Genera las animaciones del video.")
    parser.add_argument(
        "--solo",
        default="todo",
        help="Lista separada por comas: xt,heatmap,umap,contador (default: todo).",
    )
    parser.add_argument("--fps", type=int, default=FPS)
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    (GRAF / "esc05").mkdir(parents=True, exist_ok=True)

    todo = args.solo.strip().lower() in ("todo", "all", "")
    pedidos = {"contador", "xt", "heatmap", "umap"} if todo else {
        s.strip() for s in args.solo.split(",") if s.strip()
    }

    print(f"Salida: {OUT}")
    print(f"Animaciones: {', '.join(sorted(pedidos))}")

    if "contador" in pedidos:
        animar_contador(OUT, fps=args.fps)

    if "xt" in pedidos or "umap" in pedidos:
        print("\nCargando SPADL...")
        cols = ["player_id", "type_name", "result_name", "start_x", "start_y", "end_x", "end_y"]
        df = pd.read_parquet(SPADL_PATH, columns=cols)
        print(f"  {len(df):,} acciones · {df['player_id'].nunique()} jugadores")

        if "xt" in pedidos:
            animar_xt(df, OUT, fps=args.fps)

        if "umap" in pedidos:
            umap_df = build_umap_data()
            animar_umap(umap_df, OUT, fps=args.fps)

    if "heatmap" in pedidos:
        animar_heatmap_vaep(OUT, fps=args.fps)

    print("\nListo. Archivos en video/animaciones/")
    for p in sorted(OUT.glob("*.mp4")):
        print(f"  · {p.name}")


if __name__ == "__main__":
    main()
