"""Genera las tablas del capítulo 4 desde el reporte versionado de Melodies.

Este generador no completa valores ausentes. Lee el reporte asociado con una
corrida terminada directamente desde un objeto Git, valida su identidad y sólo
entonces escribe las tablas LaTeX derivadas. Cuando se recuperen los CSV
originales, éstos deberán sustituir al reporte Markdown como fuente primaria.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess


DEFAULT_REF = "b11a2731a6fb3c812dc0bfd0831b7b065a016142"
DEFAULT_RUN = "tesis_3000_gpu_20260823_1941"
REPORT_PATH = "docs/resultados-comparacion-3000.md"


def read_report(repo: Path, ref: str) -> str:
    command = [
        "git",
        "-c",
        f"safe.directory={repo.as_posix()}",
        "-C",
        str(repo),
        "show",
        f"{ref}:{REPORT_PATH}",
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True, encoding="utf-8")
    return result.stdout


def section(text: str, heading: str, next_heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## {re.escape(next_heading)}\s*$)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise ValueError(f"No se encontró la sección {heading!r}")
    return match.group(1)


def markdown_tables(text: str) -> list[list[list[str]]]:
    tables: list[list[list[str]]] = []
    current: list[list[str]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("|") and line.endswith("|"):
            cells = [cell.strip() for cell in line[1:-1].split("|")]
            if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                continue
            current.append(cells)
        elif current:
            tables.append(current)
            current = []
    if current:
        tables.append(current)
    return tables


def require_table(rows: list[list[str]], header: list[str], expected_rows: int) -> list[list[str]]:
    if not rows or rows[0] != header:
        raise ValueError(f"Encabezado inesperado: {rows[0] if rows else 'tabla vacía'}")
    if len(rows) - 1 != expected_rows:
        raise ValueError(f"Se esperaban {expected_rows} filas y se encontraron {len(rows) - 1}")
    return rows[1:]


def write(path: Path, content: str, ref: str) -> None:
    header = (
        "% Archivo generado; no editar cifras manualmente.\n"
        f"% Fuente: Melodies {ref}:{REPORT_PATH}\n"
    )
    path.write_text(header + content.rstrip() + "\n", encoding="utf-8", newline="\n")


def generate(report: str, output_dir: Path, ref: str, run_name: str) -> None:
    if f"`{run_name}`" not in report:
        raise ValueError(f"El reporte no identifica la corrida esperada {run_name!r}")

    predictive = require_table(
        markdown_tables(section(report, "3. Resultado predictivo", "4. Costo"))[0],
        ["modelo", "frac=0.1", "frac=0.25", "frac=0.5", "frac=0.75", "frac=1.0", "mejora 0.1→1.0"],
        4,
    )
    expected_models = ["transformer", "finite_hmm", "hdp_hmm", "vomm"]
    if [row[0] for row in predictive] != expected_models:
        raise ValueError("El orden o el conjunto de modelos predictivos cambió")

    predictive_labels = {
        "transformer": "Transformador",
        "finite_hmm": "HMM finito",
        "hdp_hmm": "HDP-HMM truncado",
        "vomm": "VOMM",
    }
    predictive_lines = []
    for row in predictive:
        values = [cell.replace("**", "").replace("−", "-").replace("%", r"\%") for cell in row[1:]]
        predictive_lines.append(f"{predictive_labels[row[0]]} & " + " & ".join(values) + r" \\")
    write(
        output_dir / "chapter4_learning_curve_results.tex",
        """\\begin{tabular}{lrrrrrr}
\\hline
Modelo & $0.10$ & $0.25$ & $0.50$ & $0.75$ & $1.00$ & Cambio $0.10\\to1.00$ \\\\
\\hline
""" + "\n".join(predictive_lines) + "\n\\hline\n\\end{tabular}",
        ref,
    )

    cost = require_table(
        markdown_tables(section(report, "4. Costo", "5. Inferencia estadística"))[0],
        ["modelo", "parámetros", "ajuste (s)", "evaluación (s)", "NLL"],
        4,
    )
    if [row[0] for row in cost] != ["transformer", "hdp_hmm", "finite_hmm", "vomm"]:
        raise ValueError("El orden o el conjunto de modelos de costo cambió")
    cost_lines = []
    for row in cost:
        params = row[1].replace(" (tabla de conteos)", r"$^{a}$")
        cost_lines.append(
            f"{predictive_labels[row[0]]} & {params} & {row[2]} & {row[3]} & {row[4]}" + r" \\"
        )
    write(
        output_dir / "chapter4_cost_results.tex",
        """\\begin{tabular}{lrrrr}
\\hline
Modelo & Parámetros & Selección y ajuste (s) & Evaluación (s) & NLL \\\\
\\hline
""" + "\n".join(cost_lines) + "\n\\hline\n\\end{tabular}",
        ref,
    )

    paired = require_table(
        markdown_tables(section(report, "5. Inferencia estadística", "6. Lo que esta corrida NO establece"))[0],
        ["comparación", "diferencia media", "IC 95%", "p (Holm)"],
        6,
    )
    pair_labels = {
        "finite_hmm − hdp_hmm": "HMM finito $-$ HDP-HMM",
        "finite_hmm − transformer": "HMM finito $-$ transformador",
        "finite_hmm − vomm": "HMM finito $-$ VOMM",
        "hdp_hmm − transformer": "HDP-HMM $-$ transformador",
        "hdp_hmm − vomm": "HDP-HMM $-$ VOMM",
        "transformer − vomm": "Transformador $-$ VOMM",
    }
    paired_lines = []
    for name, difference, interval, p_value in paired:
        if name not in pair_labels:
            raise ValueError(f"Comparación inesperada: {name}")
        difference = difference.replace("−", "-")
        interval = interval.replace("−", "-")
        p_value = p_value.replace("\\u2212", "-").replace("−", "-")
        exponent = re.fullmatch(r"([0-9.]+)e([+-]?\d+)", p_value)
        if exponent is None:
            raise ValueError(f"Valor p inesperado: {p_value}")
        formatted_p = rf"${exponent.group(1)}\times 10^{{{int(exponent.group(2))}}}$"
        paired_lines.append(
            f"{pair_labels[name]} & ${difference}$ & ${interval}$ & {formatted_p}" + r" \\"
        )
    write(
        output_dir / "chapter4_pairwise_results.tex",
        """\\begin{tabular}{lrrr}
\\hline
Comparación & Diferencia media & IC del $95\\%$ & $p$ ajustado \\\\
\\hline
""" + "\n".join(paired_lines) + "\n\\hline\n\\end{tabular}",
        ref,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--melodies-repo", type=Path, default=Path(r"D:\Melodies"))
    parser.add_argument("--ref", default=DEFAULT_REF)
    parser.add_argument("--run-name", default=DEFAULT_RUN)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "chapters" / "tables",
    )
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    report = read_report(args.melodies_repo.resolve(), args.ref)
    generate(report, args.output_dir, args.ref, args.run_name)


if __name__ == "__main__":
    main()
