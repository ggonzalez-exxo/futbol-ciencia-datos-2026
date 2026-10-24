#!/usr/bin/env python3
"""Arma el proyecto Kdenlive del video final a partir de video/edl.json.

 Usa la API core de cli-anything-kdenlive en proceso (el estado de la CLI no
 persiste entre invocaciones), mide duraciones con ffprobe y exporta:

   - video/kdenlive/proyecto.json  (proyecto de la CLI, editable/reabrible)
   - video/kdenlive/proyecto.mlt   (MLT para Kdenlive / melt)

 Los assets marcados "optional" que no existan aún (VO, música, ambiente) se
 saltan con un warning para que el timeline se pueda regenerar a medida que
 llegan las grabaciones.

 Uso:
   .venv-kdenlive/bin/python video/scripts/build_kdenlive_timeline.py [--edl PATH] [--out-dir PATH]
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from cli_anything.kdenlive.core.bin import import_clip
from cli_anything.kdenlive.core.export import generate_kdenlive_xml
from cli_anything.kdenlive.core.guides import add_guide
from cli_anything.kdenlive.core.project import create_project, save_project
from cli_anything.kdenlive.core.timeline import add_clip_to_track, add_track

REPO = Path(__file__).resolve().parents[2]
VIDEO = REPO / "video"
DEFAULT_EDL = VIDEO / "edl.json"
DEFAULT_OUT = VIDEO / "kdenlive"


def ffprobe_duration(path: Path) -> float:
    out = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    if out.returncode != 0:
        raise RuntimeError(f"ffprobe falló para {path}: {out.stderr.strip()}")
    return float(json.loads(out.stdout)["format"]["duration"])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--edl", type=Path, default=DEFAULT_EDL)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    edl = json.loads(args.edl.read_text())
    assets_root = VIDEO / edl.get("assets_root", ".")

    proj = create_project(name=edl["project"]["name"], profile=edl["project"]["profile"])

    track_ids = {}
    for spec in edl["tracks"]:
        track = add_track(proj, name=spec["name"], track_type=spec["type"])
        track_ids[spec["name"]] = track["id"]

    skipped = []
    placed = []
    for scene in edl["scenes"]:
        for clip_spec in scene["clips"]:
            asset = assets_root / clip_spec["asset"]
            if not asset.exists():
                if clip_spec.get("optional"):
                    skipped.append(f"{scene['id']}: {clip_spec['asset']}")
                    continue
                print(f"ERROR: asset requerido no encontrado: {asset}", file=sys.stderr)
                return 1

            duration = ffprobe_duration(asset)
            bin_clip = import_clip(
                proj,
                source=str(asset),
                name=f"{scene['id']}::{asset.stem}",
                duration=duration,
                clip_type="audio" if Path(clip_spec["asset"]).suffix in {".wav", ".mp3", ".aac", ".m4a", ".flac"} else "video",
            )
            in_point = clip_spec.get("in", 0.0)
            out_point = clip_spec.get("out", duration)
            add_clip_to_track(
                proj,
                track_ids[clip_spec["track"]],
                bin_clip["id"],
                position=clip_spec["position"],
                in_point=in_point,
                out_point=out_point,
            )
            placed.append(f"{scene['id']}: {clip_spec['asset']} @ {clip_spec['position']}s en {clip_spec['track']}")

    for guide in edl["guides"]:
        add_guide(proj, guide["position"], label=guide["label"])

    args.out_dir.mkdir(parents=True, exist_ok=True)
    project_json = args.out_dir / "proyecto.json"
    project_mlt = args.out_dir / "proyecto.mlt"
    save_project(proj, str(project_json))
    xml = generate_kdenlive_xml(proj)
    project_mlt.write_text(xml)

    print(f"Proyecto: {project_json}")
    print(f"MLT:       {project_mlt}")
    print(f"Clips colocados: {len(placed)}")
    for line in placed:
        print(f"  + {line}")
    if skipped:
        print(f"Assets opcionales omitidos (aún no existen): {len(skipped)}")
        for line in skipped:
            print(f"  - {line}")

    # Validación: melt debe poder cargar y consumir el MLT generado.
    check = subprocess.run(
        ["melt", str(project_mlt), "-consumer", "null"],
        capture_output=True,
        text=True,
    )
    if check.returncode != 0:
        print(f"ERROR: melt no pudo cargar el MLT:\n{check.stderr}", file=sys.stderr)
        return 1
    print("Validación melt: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
