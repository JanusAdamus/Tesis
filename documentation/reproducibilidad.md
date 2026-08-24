# Registro de reproducibilidad entre Melodies y la tesis

Este documento vincula el manuscrito con el estado verificable del repositorio experimental. Su función es impedir que tablas, figuras o afirmaciones numéricas se incorporen sin una procedencia identificable y distinguir entre artefactos primarios, reportes derivados y pruebas de software.

## Estado de los repositorios al 24 de agosto de 2026

- Repositorio experimental consultado: `D:\Melodies`.
- Remoto: `https://github.com/JanusAdamus/Melodies.git`.
- Commit remoto utilizado: `b11a2731a6fb3c812dc0bfd0831b7b065a016142` (`experiment tunint`).
- Reporte versionado de la corrida: `docs/resultados-comparacion-3000.md` en ese commit.
- Rama local de `D:\Melodies`: `master` en `d8d3bc6`; conserva 7 commits propios y está 19 commits detrás de `origin/master`.
- Decisión de integración: no se fusionó la historia divergente. El manuscrito consulta el objeto Git remoto por commit exacto.
- Repositorio del manuscrito: `D:\Tesis`, rama `master`.
- Estado remoto previo a esta actualización: `853b928`, sin ramas adicionales publicadas. No se localizaron en GitHub los diagramas previos mencionados por el autor.

La divergencia de `D:\Melodies` es material. Cualquier reproducción debe declarar si usa la rama local `d8d3bc6`, el remoto `b11a273` o una integración posterior; no son estados intercambiables.

## Corrida principal

La evidencia del capítulo 4 procede de la corrida:

`tesis_3000_gpu_20260823_1941`

El reporte versionado registra:

| Elemento | Valor |
|---|---:|
| Fecha de la corrida | 2026-08-23 |
| Archivos PDMX muestreados | 3000 |
| Semilla de muestreo | 7 |
| Piezas preparadas | 2933 |
| Exclusiones | 67 |
| Eventos preparados | 693 754 |
| Piezas de prueba | 424 |
| Piezas de entrenamiento en fracción completa | 2173 |
| Tokens de entrenamiento en fracción completa | 500 959 |
| Celdas del diseño | 15 de 15 terminadas |
| Filas en `results_raw.csv` | 105 |

Los modelos comparados son VOMM, HMM finito, HDP-HMM truncado y transformador. El transformador se ajustó en CUDA; los tres modelos restantes se ejecutaron en CPU con doce procesos. Los tiempos de pared sólo describen ese hardware disponible.

## Disponibilidad de artefactos

El reporte identifica como salida primaria:

`artifacts/Comparacion/tesis_3000_gpu_20260823_1941/`

La ruta no está presente en la copia actual de `D:\Melodies`, y los artefactos de corridas están excluidos del repositorio. Por ello, todavía no se han abierto localmente `results_raw.csv`, `results_summary.csv`, `piece_metrics_raw.csv`, `engineering_costs.csv`, `pairwise_comparisons.json`, `protocol_audit.json`, `structural_evaluation.json` ni `pareto_summary.json` de esta corrida.

Esta ausencia impone dos niveles de procedencia:

1. el reporte Markdown, fijado por commit, respalda las cifras actualmente incorporadas;
2. los CSV y JSON de la corrida siguen siendo la fuente primaria pendiente de recuperación.

Antes de la defensa se debe recuperar el directorio completo, comprobar que `run_summary` indique terminación, contrastar cada cifra contra los archivos estructurados y preservar una copia con hash. Si aparece cualquier discrepancia, prevalece el artefacto primario y deben regenerarse tablas y prosa.

## Generación de tablas del capítulo 4

Las tablas numéricas no se editaron directamente. Se generan desde el reporte fijado mediante:

```powershell
python scripts\generate_chapter4_results.py `
  --melodies-repo D:\Melodies `
  --ref b11a2731a6fb3c812dc0bfd0831b7b065a016142 `
  --run-name tesis_3000_gpu_20260823_1941
```

El generador valida la identidad de la corrida, los encabezados, el conjunto de modelos y el número de filas antes de escribir:

- `chapters/tables/chapter4_learning_curve_results.tex`;
- `chapters/tables/chapter4_cost_results.tex`;
- `chapters/tables/chapter4_pairwise_results.tex`.

Cada archivo generado incluye un comentario con el commit y la ruta del reporte. El generador falla si cambia el contrato esperado; no completa valores ausentes. Cuando se recuperen los CSV, el script deberá ampliarse para leerlos y el modo basado en el reporte quedará como verificación histórica secundaria.

## Ejercicio manual sobre Bach

El Capítulo~2 recupera una comprobación manual realizada sobre el \emph{Preludio en Do mayor}, BWV~846. Su procedencia es distinta de las corridas automatizadas:

- `figures/Inferida.png` conserva la matriz inferida original;
- `figures/real.png` conserva la matriz construida mediante etiquetado y conteo manual;
- `figures/Error.png` conserva la diferencia absoluta registrada durante el ejercicio;
- no se localizó la hoja intermedia de conteos ni una segunda anotación independiente.

Los tres originales se conservan sin modificaciones. `scripts/generate_bach_manual_figures.py` transcribe los valores visibles y genera versiones limpias en PDF y PNG. `figures/bach_manual_figures_manifest.json` registra las rutas, los hashes SHA-256 y las transformaciones de presentación. La matriz de error se transcribe de su propia imagen y no se recalcula a partir de las otras dos, pues los valores visibles están redondeados a dos decimales.

El conteo narrativo asociado registra $30$ cambios en la referencia manual, $27$ en la trayectoria inferida y $22$ coincidencias. Estas cantidades se presentan como resultado de un ejercicio manual ilustrativo. No se utilizan como estimación general de exactitud ni como evidencia de superioridad entre familias de modelos.

## Correspondencia con el manuscrito

| Elemento de la tesis | Fuente | Estado |
|---|---|---|
| Protocolo del capítulo 4 | `Comparacion/config.py`, `docs/multidimensional-evaluation.md` y reporte en `b11a273` | Contrastado con el remoto. |
| Tamaño del corpus y particiones | Sección 2 del reporte versionado | Incorporado; pendiente de contraste con JSON primario. |
| Curva de *perplexity* | Sección 3 del reporte y tabla generada | Incorporada sin barras de error; los CSV faltan localmente. |
| Costos de la fracción completa | Sección 4 del reporte y tabla generada | Incorporados con advertencia CPU/GPU. |
| Contrastes pareados | Sección 5 del reporte y tabla generada | Incorporados; 414 obras válidas por par. |
| Estado estructural | Sección 6.1 del reporte | `not_evaluated`; no se inventaron métricas. |
| Diagrama del enfoque | Código TikZ en `chapters/chapter4.tex` | Reproducible dentro del manuscrito; no depende de una imagen externa. |
| Tablas y figuras del capítulo 3 | Artefactos históricos del pipeline clásico | Se conservaron las cifras exportadas y sólo se corrigieron texto y acentuación; no se regeneraron sin los artefactos primarios. |

El archivo histórico `figures/chapter3/single_anchor_transition_comparison.png` se conserva en el repositorio, pero se retiró del manuscrito. La inspección visual encontró etiquetas superpuestas y una mezcla entre nombres armónicos y estados anónimos que impedía interpretarlo sin ambigüedad. No se sustituyó manualmente porque faltan los artefactos primarios necesarios para regenerarlo.

## Correcciones metodológicas incorporadas

El estado remoto corrige o amplía el protocolo anterior en varios puntos:

1. la descripción estructural se declara eje principal, la predicción tarea común secundaria y el costo eje transversal;
2. VOMM se incorpora como control diagnóstico con órdenes candidatos 1, 2, 4 y 8;
3. BOS es contexto y no objetivo, mientras que PAD queda fuera de la distribución puntuada;
4. `protocol_audit.json` comprueba cobertura, orden, omisiones y duplicados por obra;
5. la inferencia de la fracción completa produce seis comparaciones, con *bootstrap*, Wilcoxon y Holm;
6. el truncamiento del HDP-HMM baja de 40 a 24, con ocupación efectiva observada entre 14 y 17 estados;
7. la caché respeta la selección actual de archivos y la reanudación tolera una última línea incompleta de *checkpoint*;
8. las rutas vectorizadas de HMM y HDP-HMM tienen pruebas de regresión contra las formulaciones previas.

Las pruebas unitarias y de regresión respaldan contratos de software. No se presentan como evidencia musical ni sustituyen la corrida principal.

## Límites que deben permanecer visibles

- Las treinta selecciones del HMM finito eligieron el techo de 48 estados. Sólo puede afirmarse una meseta para la rejilla evaluada.
- En la fracción completa las tres semillas de datos producen el mismo subconjunto. No deben tratarse como réplicas independientes.
- El orden entre HDP-HMM y VOMM cambia entre la media ponderada por tokens y el promedio pareado por obra. El manuscrito declara qué estimador usa en cada caso.
- El VOMM cambia de orden seleccionado dentro de la curva; parte de su pendiente refleja un cambio de capacidad.
- No hubo anotaciones estructurales. La frontera de Pareto disponible es predictiva-costo y explícitamente parcial.
- La comparación temporal mezcla GPU para el transformador y CPU para los modelos clásicos.

## Recuperación y auditoría pendientes

Al recuperar los artefactos primarios se debe verificar, como mínimo:

1. que el nombre de corrida, el commit, el corpus y la configuración coincidan con el reporte;
2. que se conserven las 67 exclusiones y sus razones;
3. que ninguna obra canónica cruce entre entrenamiento, validación y prueba;
4. que la auditoría cubra cada evento exactamente una vez por modelo;
5. que las 105 filas correspondan al plan y que la fracción completa no se interprete como tres muestras de datos distintas;
6. que los seis contrastes usen 414 obras válidas por par y promedien primero dentro de obra;
7. que `structural_evaluation.json` permanezca en `not_evaluated` si no se añaden anotaciones;
8. que tablas, prosa y cualquier figura futura coincidan con los CSV y JSON recuperados.
