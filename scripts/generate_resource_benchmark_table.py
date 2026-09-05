"""Genera la tabla del benchmark de recursos desde artefactos auditados.

Las repeticiones del benchmark son técnicas. Este script valida la cobertura,
los hashes declarados por la auditoría y la correspondencia entre los modelos
del resumen y los escenarios de costo antes de escribir LaTeX.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path


MODEL_LABELS = {
    "finite_hmm": "HMM finito",
    "hdp_hmm": "HDP-HMM truncado",
    "transformer": "Transformador",
    "vomm": "VOMM",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def load_json(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} no contiene un objeto JSON")
    return payload


def validate_audit(input_dir: Path, audit: dict[str, object]) -> None:
    if audit.get("status") != "passed":
        raise ValueError("La auditoría del benchmark no terminó con estado passed")
    coverage = audit.get("coverage")
    if not isinstance(coverage, dict) or coverage.get("observed_rows") != 12:
        raise ValueError("La auditoría no acredita las doce mediciones esperadas")
    for item in audit.get("files", []):
        if not isinstance(item, dict):
            raise ValueError("Entrada inválida en el manifiesto de archivos")
        path = input_dir / str(item["relative_path"])
        if not path.is_file():
            raise FileNotFoundError(path)
        if sha256(path) != str(item["sha256"]).upper():
            raise ValueError(f"El hash no coincide para {path.name}")


def format_seconds(row: dict[str, str], phase: str) -> str:
    median = float(row[f"{phase}_wall_clock_s_median"])
    minimum = float(row[f"{phase}_wall_clock_s_min"])
    maximum = float(row[f"{phase}_wall_clock_s_max"])
    decimals = 2 if median < 10 else 1
    return f"{median:.{decimals}f} [{minimum:.{decimals}f}, {maximum:.{decimals}f}]"


def format_cost(value: float) -> str:
    if value < 0.0001:
        return f"{value:.6f}"
    return f"{value:.4f}"


def scenario_costs(costs: dict[str, object]) -> dict[str, dict[str, float]]:
    if costs.get("currency") != "USD":
        raise ValueError("La tabla LaTeX está definida para escenarios en USD")
    if costs.get("source_engineering_costs") != "resource_benchmark_raw.csv":
        raise ValueError("El escenario no identifica el CSV crudo del benchmark")
    result: dict[str, dict[str, float]] = {}
    observations = costs.get("observations")
    if not isinstance(observations, list):
        raise ValueError("El archivo de costos no contiene observaciones")
    for observation in observations:
        if not isinstance(observation, dict):
            raise ValueError("Observación de costo inválida")
        model = str(observation["model"])
        if model in result:
            raise ValueError(f"El modelo {model} aparece más de una vez en los costos")
        if int(observation.get("n_rows", 0)) != 3:
            raise ValueError(f"El escenario de {model} no procede de tres repeticiones")
        result[model] = {}
        for scenario in observation.get("scenario_costs", []):
            if not isinstance(scenario, dict):
                raise ValueError("Escenario de costo inválido")
            name = str(scenario["name"])
            value = float(scenario["estimated_cost"])
            if name in result[model] or not math.isfinite(value) or value < 0:
                raise ValueError(f"Costo inválido o duplicado para {model}:{name}")
            result[model][name] = value
        if set(result[model]) != {"selection_and_fit", "one_hundred_evaluations"}:
            raise ValueError(f"Escenarios incompletos para {model}")
    if set(result) != set(MODEL_LABELS):
        raise ValueError("Los costos no contienen exactamente los cuatro modelos esperados")
    return result


def generate(input_dir: Path, output: Path) -> None:
    audit_path = input_dir / "resource_benchmark_audit.json"
    summary_path = input_dir / "resource_benchmark_summary.csv"
    costs_path = input_dir / "cost_scenarios.json"
    audit = load_json(audit_path)
    validate_audit(input_dir, audit)
    costs_payload = load_json(costs_path)
    if costs_payload.get("status") != "computed_from_isolated_measurements":
        raise ValueError("Los escenarios no proceden de mediciones aisladas")
    costs = scenario_costs(costs_payload)

    with summary_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if {row["model"] for row in rows} != set(MODEL_LABELS):
        raise ValueError("El resumen no contiene exactamente los cuatro modelos esperados")
    if any(int(row["repetitions"]) != 3 for row in rows):
        raise ValueError("Cada modelo debe tener tres repeticiones técnicas")
    numeric_suffixes = (
        "selection_wall_clock_s_median",
        "selection_wall_clock_s_min",
        "selection_wall_clock_s_max",
        "evaluation_wall_clock_s_median",
        "evaluation_wall_clock_s_min",
        "evaluation_wall_clock_s_max",
    )
    if any(
        not math.isfinite(float(row[field])) or float(row[field]) < 0
        for row in rows
        for field in numeric_suffixes
    ):
        raise ValueError("El resumen contiene tiempos ausentes, infinitos o negativos")

    lines = []
    for model in ("transformer", "finite_hmm", "hdp_hmm", "vomm"):
        row = next(item for item in rows if item["model"] == model)
        if model not in costs:
            raise ValueError(f"Falta el escenario de costo para {model}")
        lines.append(
            f"{MODEL_LABELS[model]} & {format_seconds(row, 'selection')} & "
            f"{format_seconds(row, 'evaluation')} & "
            f"{format_cost(costs[model]['selection_and_fit'])} & "
            f"{format_cost(costs[model]['one_hundred_evaluations'])} \\\\"
        )

    content = (
        "% Archivo generado; no editar cifras manualmente.\n"
        f"% Auditoría: {sha256(audit_path)}\n"
        f"% Resumen: {sha256(summary_path)}\n"
        f"% Escenarios: {sha256(costs_path)}\n"
        "\\begin{tabular}{lrrrr}\n"
        "\\hline\n"
        "Modelo & Ajuste (s) & Evaluación (s) & Ajuste (USD) & 100 eval. (USD) \\\\\n"
        "\\hline\n"
        + "\n".join(lines)
        + "\n\\hline\n\\end{tabular}\n"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=Path("D:/"))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "chapters"
        / "tables"
        / "chapter4_resource_benchmark.tex",
    )
    args = parser.parse_args()
    generate(args.input_dir.resolve(), args.output.resolve())


if __name__ == "__main__":
    main()
