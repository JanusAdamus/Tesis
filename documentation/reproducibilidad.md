# Registro de reproducibilidad entre Melodies y la tesis

Este documento vincula el manuscrito con el estado local del repositorio experimental. Su función es impedir que tablas, figuras o afirmaciones numéricas se incorporen sin una procedencia verificable.

## Estado de referencia

- Repositorio experimental: `D:\Melodies`.
- Rama local: `master`.
- Commit integrado y validado: `bbb5575` (`Harden classical-transformer comparison integration`).
- Remoto al momento de la integración: `origin/master` en `374b72c`.
- Estado de publicación: el avance hasta `bbb5575` es local y todavía no se ha enviado al remoto.
- Repositorio del manuscrito: `D:\Tesis`, inicializado localmente en `master`.

## Entorno verificado

La validación se realizó con:

- Python `3.11.15`;
- PyTorch `2.13.0+cpu`;
- music21 `10.5.0`;
- pandas `3.0.5`;
- SciPy `1.17.1`.

La suite completa del protocolo preparado produjo `53 passed`. El entorno aislado utilizado se encuentra en `C:\Users\AdrianGonzalez\.codex\venvs\melodies-py311`; esta ruta es una condición local de ejecución, no una ruta que deba escribirse en el código o en el cuerpo de la tesis.

## Corrida de integración

Se ejecutó una validación de extremo a extremo con ocho partituras del corpus local, una semilla de datos, una semilla de modelo, la fracción completa de entrenamiento y una época del transformador. Los artefactos se encuentran en:

`D:\Melodies\artifacts\Comparacion\integration_smoke`

La corrida preparó ocho obras, no registró exclusiones y generó un resultado para cada familia. Las métricas observadas fueron:

| Modelo | Tokens de entrenamiento | NLL de prueba por token | *Perplexity* de prueba |
|---|---:|---:|---:|
| HMM finito | 5151 | 2.7345107711 | 15.4022063882 |
| HDP-HMM truncado | 5151 | 2.4659021852 | 11.7740997799 |
| Transformador | 5151 | 2.3722491391 | 10.7214792849 |

Estos valores demuestran que el pipeline común funciona y produce métricas homogéneas. No constituyen evidencia final: hay una sola repetición y una sola obra en la partición de prueba, por lo que el contraste de Wilcoxon quedó marcado como `insufficient_pairs`.

Después de corregir cobertura, agrupación, repeticiones y análisis estadístico se ejecutó una segunda validación en:

`D:\Melodies\artifacts\Comparacion\final_protocol_smoke_20260814`

Esta corrida preparó ocho partituras, no produjo exclusiones y completó las tres corridas planeadas. La auditoría confirmó que HMM finito, HDP-HMM y transformador evaluaron los mismos 2482 tokens de la obra de prueba. También se comprobó que `--resume` reconoce los checkpoints terminados y no repite los ajustes. Los tres contrastes quedaron como `insufficient_pairs` porque la validación contiene una sola obra canónica de prueba. Por ello, tampoco se utilizan sus métricas predictivas como evidencia del capítulo.

## Correspondencia con capítulos, tablas y figuras

| Elemento de la tesis | Fuente o generador esperado | Estado de verificación |
|---|---|---|
| Tablas y figuras del capítulo 3 | `D:\Melodies\scripts\generate_thesis_chapter3_assets.py` y artefactos del pipeline clásico | Pendiente de regenerar desde `bbb5575`; los archivos actuales preceden a este registro Git. |
| Tablas conceptuales del capítulo 4 | `chapters/tables/chapter4_*.tex` | Son plantillas argumentales, no resultados finales. |
| Curvas HMM/HDP-HMM/transformador | `D:\Melodies\Comparacion` y `artifacts\Comparacion\<run>` | Protocolo final verificado mediante `final_protocol_smoke_20260814`; falta ejecutar la corrida canónica. |
| Valores finales del capítulo 4 | `results_raw.csv`, `results_summary.csv`, `piece_metrics_raw.csv` y manifiestos de splits de la corrida canónica | Pendiente. No deben completarse con los valores de humo. |

## Regla de actualización

Antes de modificar una cifra del manuscrito se debe registrar:

1. commit exacto de `D:\Melodies`;
2. configuración y nombre de corrida;
3. corpus, exclusiones y asignación de obras a cada partición;
4. semillas y presupuesto experimental;
5. ruta del artefacto estructurado del que se obtiene la cifra;
6. comprobación de consistencia entre CSV, tabla, figura y prosa.

Si alguno de estos elementos falta, el resultado debe conservarse como pendiente y no presentarse como conclusión cerrada.

## Protocolo preparado para la corrida canónica

La comparación principal se ejecutará sin `--max-files`, sobre los 58 archivos MXL candidatos del corpus local. El número efectivo de partituras y obras canónicas se obtiene del informe de preprocesamiento y de los manifiestos de partición. La configuración fija cinco fracciones de entrenamiento (`0.10,0.25,0.50,0.75,1.00`), tres semillas de datos (`1,2,3`) y dos semillas de modelo (`1,2`) para las fracciones parciales. En la fracción completa se deduplican los subconjuntos idénticos y se utilizan cinco semillas de modelo independientes (`1,2,3,4,5`). El número exacto de ajustes se obtiene de `scenario_manifest.json` después de planificar el corpus completo.

Los cuatro ajustes identificados antes de la preparación quedaron incorporados:

1. las fracciones anidadas agrupan por `canonical_work_id`;
2. los tres modelos reinician contexto en los mismos segmentos de evaluación e incluyen todos los remanentes;
3. la fracción `1.00` utiliza cinco semillas independientes sin repetición por semilla de datos;
4. se generan los tres contrastes por obra, diferencias medias y medianas, intervalos bootstrap del 95% y ajuste de Holm.

Primero se congela el corpus y el plan sin entrenar:

```powershell
& 'C:\Users\AdrianGonzalez\.codex\venvs\melodies-py311\Scripts\python.exe' -m Comparacion.cli `
  --run-name thesis_canonical_v1 `
  --corpus-root external/library/scores `
  --data-seeds 1,2,3 `
  --model-seeds 1,2 `
  --full-fraction-model-seeds 1,2,3,4,5 `
  --fractions 0.10,0.25,0.50,0.75,1.00 `
  --transformer-device cpu `
  --plan-only
```

Después de revisar `corpus_manifest.json`, los archivos de `splits/` y `scenario_manifest.json`, se ejecuta el mismo comando sin `--plan-only` y con `--resume`. Cada modelo terminado actualiza checkpoints atómicos. La reanudación se rechaza si no coinciden la configuración, las secuencias del corpus o las particiones. Si se modifica cualquier decisión después de consultar los resultados de prueba, la nueva ejecución debe recibir otro nombre y clasificarse como exploratoria.

Antes de incorporar resultados al capítulo 4 se debe comprobar:

1. que `preprocessing_report.json` y `exclusions.csv` expliquen el tamaño efectivo del corpus;
2. que ninguna obra canónica aparezca en más de una partición;
3. que `run_summary.json` indique `complete` y el mismo número de corridas planeadas y terminadas;
4. que las repeticiones esperadas estén presentes y correspondan a semillas independientes;
5. que `piece_metrics_raw.csv` contenga las mismas obras de prueba para las tres familias;
6. que los contrastes pareados incluyan HMM finito frente a HDP-HMM, HMM finito frente a transformador y HDP-HMM frente a transformador, con tamaño de diferencia e incertidumbre;
7. que las tablas y figuras de la tesis se generen desde los CSV y no mediante transcripción manual.

`token_coverage_audit.json` debe indicar cobertura idéntica y `pairwise_tests.json` debe contener los tres contrastes previstos. También se recomienda repetir el análisis con semillas adicionales de partición como sensibilidad; esas repeticiones no sustituyen la partición primaria fijada con semilla `7`.
