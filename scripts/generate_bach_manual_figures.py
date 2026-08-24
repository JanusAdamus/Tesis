"""Regenera las figuras limpias del ejercicio manual sobre Bach.

Los valores son una transcripción de las cifras impresas en las imágenes
históricas ``figures/Inferida.png``, ``figures/real.png`` y
``figures/Error.png``. Los originales se conservan sin modificaciones. La
matriz de error se transcribe de su propia imagen: no se recalcula a partir de
las otras dos porque sus valores visibles están redondeados a dos decimales.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"

STATES = [
    "A min",
    "C Maj",
    "C min",
    "D Maj",
    "D min",
    "E min",
    "F Maj",
    "F min",
    "G Maj",
    "G min",
]

INFERRED = np.array(
    [
        [0.92, 0.00, 0.00, 0.08, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [0.01, 0.93, 0.00, 0.01, 0.01, 0.00, 0.02, 0.00, 0.02, 0.00],
        [0.00, 0.08, 0.92, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [0.00, 0.00, 0.00, 0.92, 0.00, 0.00, 0.00, 0.00, 0.08, 0.00],
        [0.00, 0.03, 0.00, 0.00, 0.94, 0.00, 0.00, 0.00, 0.03, 0.00],
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.94, 0.02, 0.04, 0.00],
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.97, 0.03, 0.00],
        [0.00, 0.05, 0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.93, 0.01],
        [0.00, 0.00, 0.00, 0.00, 0.08, 0.00, 0.00, 0.00, 0.00, 0.92],
    ],
    dtype=float,
)

REFERENCE = np.array(
    [
        [0.92, 0.04, 0.00, 0.02, 0.00, 0.00, 0.00, 0.02, 0.00, 0.00],
        [0.02, 0.94, 0.00, 0.01, 0.01, 0.00, 0.01, 0.00, 0.02, 0.00],
        [0.00, 0.00, 0.92, 0.00, 0.00, 0.00, 0.00, 0.08, 0.00, 0.00],
        [0.00, 0.00, 0.00, 0.92, 0.00, 0.00, 0.00, 0.00, 0.08, 0.00],
        [0.04, 0.00, 0.00, 0.00, 0.92, 0.00, 0.00, 0.00, 0.04, 0.00],
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.92, 0.08, 0.00, 0.00, 0.00],
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.94, 0.00, 0.06, 0.00],
        [0.00, 0.00, 0.04, 0.00, 0.00, 0.00, 0.00, 0.92, 0.04, 0.00],
        [0.01, 0.04, 0.00, 0.00, 0.00, 0.01, 0.00, 0.00, 0.93, 0.01],
        [0.00, 0.00, 0.00, 0.00, 0.08, 0.00, 0.00, 0.00, 0.00, 0.92],
    ],
    dtype=float,
)

ABSOLUTE_ERROR = np.array(
    [
        [0.00, 0.04, 0.00, 0.06, 0.00, 0.00, 0.00, 0.02, 0.00, 0.00],
        [0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.02, 0.00, 0.00, 0.00],
        [0.00, 0.08, 0.00, 0.00, 0.00, 0.00, 0.00, 0.08, 0.00, 0.00],
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [0.04, 0.03, 0.00, 0.00, 0.03, 0.00, 0.00, 0.00, 0.01, 0.00],
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.92, 0.08, 0.00, 0.00, 0.00],
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.02, 0.01, 0.00],
        [0.00, 0.00, 0.04, 0.00, 0.00, 0.00, 0.00, 0.06, 0.01, 0.00],
        [0.01, 0.01, 0.01, 0.00, 0.00, 0.01, 0.00, 0.00, 0.00, 0.00],
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    ],
    dtype=float,
)

SOURCE_IMAGES = {
    "inferred": FIGURES / "Inferida.png",
    "reference": FIGURES / "real.png",
    "absolute_error": FIGURES / "Error.png",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def render_heatmap(
    matrix: np.ndarray,
    *,
    title: str,
    stem: str,
    cmap: str,
    colorbar_label: str,
    mark_empty_row: bool = False,
) -> list[str]:
    with mpl.rc_context(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.titlesize": 13,
            "axes.labelsize": 10,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
        }
    ):
        fig, ax = plt.subplots(figsize=(7.1, 5.7), layout="constrained")
        image = ax.imshow(matrix, cmap=cmap, vmin=0.0, vmax=1.0, aspect="equal")

        ylabels = STATES.copy()
        if mark_empty_row:
            ylabels[5] = "E min*"
            ax.add_patch(
                Rectangle(
                    (-0.5, 4.5),
                    len(STATES),
                    1,
                    fill=False,
                    edgecolor="#333333",
                    linewidth=1.2,
                    linestyle="--",
                )
            )

        ax.set_xticks(range(len(STATES)), STATES, rotation=45, ha="left")
        ax.set_yticks(range(len(STATES)), ylabels)
        ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
        ax.set_xlabel("Siguiente estado")
        ax.xaxis.set_label_position("top")
        ax.set_ylabel("Estado actual")
        ax.set_title(title, pad=12)

        ax.set_xticks(np.arange(-0.5, len(STATES), 1), minor=True)
        ax.set_yticks(np.arange(-0.5, len(STATES), 1), minor=True)
        ax.grid(which="minor", color="white", linewidth=0.8)
        ax.tick_params(which="minor", bottom=False, left=False)
        for spine in ax.spines.values():
            spine.set_visible(False)

        for row in range(matrix.shape[0]):
            for column in range(matrix.shape[1]):
                value = matrix[row, column]
                if value <= 0.0:
                    continue
                color = "white" if value >= 0.55 else "#111111"
                ax.text(
                    column,
                    row,
                    f"{value:.2f}",
                    ha="center",
                    va="center",
                    color=color,
                    fontsize=8,
                )

        colorbar = fig.colorbar(image, ax=ax, fraction=0.045, pad=0.035)
        colorbar.set_label(colorbar_label)
        colorbar.outline.set_visible(False)
        colorbar.set_ticks([0.0, 0.25, 0.5, 0.75, 1.0])

        outputs: list[str] = []
        for extension in ("pdf", "png"):
            output = FIGURES / f"{stem}.{extension}"
            save_options: dict[str, object] = {
                "dpi": 300 if extension == "png" else None,
            }
            if extension == "pdf":
                # Suprimir fechas variables para que el PDF sea idéntico al
                # regenerarlo a partir de los mismos datos y el mismo entorno.
                save_options["metadata"] = {
                    "Creator": "scripts/generate_bach_manual_figures.py",
                    "CreationDate": None,
                    "ModDate": None,
                }
            fig.savefig(output, **save_options)
            outputs.append(str(output.relative_to(ROOT)))
        plt.close(fig)
        return outputs


def main() -> None:
    for source in SOURCE_IMAGES.values():
        if not source.is_file():
            raise FileNotFoundError(source)

    outputs: list[str] = []
    outputs.extend(
        render_heatmap(
            INFERRED,
            title="Matriz de transición inferida",
            stem="bach_manual_inferred",
            cmap="Purples",
            colorbar_label="Probabilidad",
            mark_empty_row=True,
        )
    )
    outputs.extend(
        render_heatmap(
            REFERENCE,
            title="Matriz de transición de referencia manual",
            stem="bach_manual_reference",
            cmap="Purples",
            colorbar_label="Probabilidad",
        )
    )
    outputs.extend(
        render_heatmap(
            ABSOLUTE_ERROR,
            title="Diferencia absoluta registrada",
            stem="bach_manual_absolute_error",
            cmap="Reds",
            colorbar_label="Diferencia absoluta",
        )
    )

    manifest = {
        "description": "Figuras limpias del ejercicio manual sobre Bach.",
        "source_images": {
            name: {
                "path": str(path.relative_to(ROOT)),
                "sha256": sha256(path),
            }
            for name, path in SOURCE_IMAGES.items()
        },
        "transformation": [
            "Transcripción de los valores impresos a dos decimales.",
            "Eliminación de las marcas naranjas de presentación.",
            "Las celdas iguales a cero se dejan sin texto para reducir saturación visual.",
            "La matriz de error se transcribe de Error.png y no se recalcula desde valores redondeados.",
        ],
        "outputs": outputs,
    }
    manifest_path = FIGURES / "bach_manual_figures_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
