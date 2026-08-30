"""Aplica correcciones editoriales a las figuras importadas de Melodies.

El script no modifica datos, escalas ni marcas. Superpone únicamente títulos y
rótulos cuya redacción resultaba demasiado absoluta, ambigua o poco natural en
castellano. Los originales se leen desde el directorio indicado y las copias
corregidas se escriben en el directorio de salida.
"""

from __future__ import annotations

import argparse
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))


def cover_from_top(
    page,
    drawing: canvas.Canvas,
    *,
    x0: float,
    top: float,
    x1: float,
    bottom: float,
) -> None:
    height = float(page.mediabox.height)
    drawing.setFillColorRGB(1, 1, 1)
    drawing.rect(x0, height - bottom, x1 - x0, bottom - top, fill=1, stroke=0)


def text_from_top(
    page,
    drawing: canvas.Canvas,
    text: str,
    *,
    x: float,
    top: float,
    max_width: float,
    font: str = "Arial-Bold",
    size: float = 10.0,
    min_size: float = 5.8,
) -> None:
    while size > min_size and stringWidth(text, font, size) > max_width:
        size -= 0.2
    height = float(page.mediabox.height)
    drawing.setFillColorRGB(0.12, 0.12, 0.12)
    drawing.setFont(font, size)
    drawing.drawString(x, height - top - size, text)


def build_overlay(page, operations: list[dict]) -> PdfReader:
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    stream = BytesIO()
    drawing = canvas.Canvas(stream, pagesize=(width, height))
    for operation in operations:
        cover_from_top(page, drawing, **operation["cover"])
        text_from_top(page, drawing, operation["text"], **operation["draw"])
    drawing.save()
    stream.seek(0)
    return PdfReader(stream)


CORRECTIONS: dict[str, list[dict]] = {
    "fig1_curva_aprendizaje.pdf": [
        {
            "cover": {"x0": 0, "top": 0, "x1": 340.3, "bottom": 16.0},
            "text": "Curvas de aprendizaje en la corrida principal",
            "draw": {"x": 2.2, "top": 1.5, "max_width": 332.0, "size": 10.6},
        }
    ],
    "fig2_capacidad_hmm.pdf": [
        {
            "cover": {"x0": 292.0, "top": 49.0, "x1": 470.8, "bottom": 64.0},
            "text": "y el tiempo observado aumenta con K",
            "draw": {"x": 295.5, "top": 52.4, "max_width": 171.0, "size": 8.8},
        }
    ],
    "fig3_sensibilidades.pdf": [
        {
            "cover": {"x0": 81.0, "top": 184.0, "x1": 210.0, "bottom": 200.0},
            "text": "±0.047: máx. desv. estándar",
            "draw": {
                "x": 82.0,
                "top": 188.0,
                "max_width": 125.0,
                "font": "Arial",
                "size": 6.5,
            },
        }
    ],
    "fig4_comparaciones_pareadas.pdf": [
        {
            "cover": {"x0": 30.0, "top": 17.0, "x1": 432.0, "bottom": 31.0},
            "text": (
                "414 obras por corrida; 6 pares por 5 corridas. IC 95 % por bootstrap; "
                "mayor p ajustado de Wilcoxon-Holm: 0.004."
            ),
            "draw": {
                "x": 33.4,
                "top": 20.0,
                "max_width": 394.0,
                "font": "Arial",
                "size": 7.2,
            },
        }
    ],
    "fig5_pareto_prediccion_costo.pdf": [
        {
            "cover": {"x0": 0, "top": 0, "x1": 331.7, "bottom": 16.0},
            "text": "Calidad predictiva y tiempo observado en la corrida principal",
            "draw": {"x": 2.2, "top": 1.5, "max_width": 325.0, "size": 10.4},
        },
        {
            "cover": {"x0": 66.0, "top": 194.0, "x1": 331.7, "bottom": 209.5},
            "text": "Segundos de selección y ajuste, frac = 1.0 (escala logarítmica)",
            "draw": {
                "x": 68.0,
                "top": 198.0,
                "max_width": 260.0,
                "font": "Arial",
                "size": 7.0,
            },
        },
    ],
    "fig6_unidad_de_analisis.pdf": [
        {
            "cover": {"x0": 0, "top": 0, "x1": 433.0, "bottom": 16.0},
            "text": "La comparación entre HDP-HMM y VOMM cambia con la unidad de agregación",
            "draw": {"x": 2.2, "top": 1.5, "max_width": 425.0, "size": 10.6},
        },
        {
            "cover": {"x0": 57.0, "top": 53.0, "x1": 278.0, "bottom": 68.0},
            "text": "La diferencia es mayor en los cuartiles intermedios",
            "draw": {"x": 60.5, "top": 56.7, "max_width": 214.0, "size": 8.8},
        },
        {
            "cover": {"x0": 315.0, "top": 53.0, "x1": 432.0, "bottom": 68.0},
            "text": "La unidad cambia el orden",
            "draw": {"x": 319.0, "top": 56.7, "max_width": 109.0, "size": 8.8},
        },
    ],
}


def correct(source: Path, destination: Path, operations: list[dict]) -> None:
    reader = PdfReader(source)
    if len(reader.pages) != 1:
        raise ValueError(f"Se esperaba una pagina en {source}")
    page = reader.pages[0]
    overlay = build_overlay(page, operations)
    page.merge_page(overlay.pages[0], over=True)
    writer = PdfWriter()
    writer.add_page(page)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as handle:
        writer.write(handle)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    for name, operations in CORRECTIONS.items():
        source = args.source_dir / name
        if not source.is_file():
            raise FileNotFoundError(source)
        correct(source, args.output_dir / name, operations)


if __name__ == "__main__":
    main()
