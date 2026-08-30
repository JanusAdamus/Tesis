# Registro de reproducibilidad entre Melodies y la tesis

Este documento vincula el manuscrito con el estado verificable del repositorio experimental. Su función es impedir que tablas, figuras o afirmaciones numéricas se incorporen sin una procedencia identificable y distinguir entre artefactos primarios, reportes derivados y pruebas de software.

## Estado de los repositorios al 29 de agosto de 2026

- Repositorio experimental: `https://github.com/JanusAdamus/Melodies.git`.
- Rama y commit consultados: `master`, `2535e70`, que integra los resultados de `009119c` mediante `2700393` y añade las figuras finales.
- Reportes principales: `docs/resultados-comparacion-auditada.md` y `docs/parada-curva-rehecha-2026-08-29.md`.
- Script de figuras: `scripts/figuras_tesis.py`.
- Repositorio del manuscrito: `D:\Tesis`, rama `master`.

La evidencia pública y la evidencia primaria no tienen el mismo alcance. El repositorio de Melodies versiona los reportes, el script y las seis figuras finales. Los CSV y JSON de las corridas no están versionados y tampoco aparecen en una clonación limpia de `master`. Los reportes registran que los artefactos primarios estuvieron disponibles en la máquina de ejecución y que las cinco corridas citadas aprobaron la auditoría. Por ello puede afirmarse que los resultados fueron auditados en esa máquina y que su procedencia está documentada; no puede afirmarse que una clonación limpia baste para regenerarlos.

## Corridas incorporadas

| Corrida | Cambio respecto de la principal | Alcance | Auditoría registrada |
|---|---|---|---|
| `tesis_3000_gpu_20260823_1941` | ninguno | cinco fracciones; resultado principal | `passed` |
| `sens_stride128` | desplazamiento 128, sin solapamiento | fracción completa | `passed` |
| `sens_hmm_grid` | HMM finito con `K=48,96,144,192` | fracción completa | `passed` |
| `sens_split17` | semilla de partición 17 | fracción completa | `passed` |
| `sens_split29` | semilla de partición 29 | fracción completa | `passed` |

Las cinco corridas comparten una muestra de 3000 archivos de PDMX con semilla de muestreo 7. El preprocesamiento dejó 2933 piezas y 67 exclusiones. La corrida principal contiene 693 754 eventos preparados, 424 archivos de prueba y 500 959 eventos de entrenamiento en la fracción completa. Después de agrupar variantes, cada corrida utiliza 414 obras canónicas para los contrastes pareados. La diferencia entre 423 y 428 archivos de prueba, según la partición, y las 414 obras se explicó mediante canonicalización, sin descartes por métricas no finitas. Persiste la salvedad del identificador mal formado `after mr`, cuya corrección llevaría el denominador a 415.

Las sensibilidades cambian un factor a la vez. No forman un experimento factorial y no permiten sumar el efecto de eliminar el solapamiento con el efecto de ampliar la rejilla del HMM. Las particiones alternativas también cambian el número de eventos de entrenamiento y conservan el HMM limitado a `K=48`; se usan para verificar el orden dentro de cada partición, no para comparar sus niveles en horizontal.

## Resultados que sustentan el capítulo 4

- En la corrida principal, los valores de *perplexity* de la fracción completa son 5.8225 para el transformador, 7.3560 para el HMM finito, 7.9677 para el HDP-HMM y 8.0220 para el VOMM.
- Con la rejilla ampliada, el HMM finito mejora a 6.9835, pero la selección vuelve a tocar el extremo de la rejilla. No se localizó el óptimo.
- Con ventanas sin solapamiento, el transformador pasa a 6.4394. Su ventaja pareada frente al HMM finito se reduce de 0.2505 a 0.1521 nats, un 39 %, sin cambiar de signo.
- En las cinco corridas, ninguno de los 30 intervalos pareados del 95 % cruza el cero. El orden por obra es transformador, HMM finito, VOMM y HDP-HMM.
- Por obra, VOMM supera al HDP-HMM por 0.0336 nats; al ponderar por eventos, el HDP-HMM supera al VOMM por 0.0076. La obra es la unidad principal y el evento se conserva como lectura secundaria.
- Los diagnósticos del HDP-HMM registran deriva. Su *perplexity* se utiliza; el número de estados activos no se interpreta como una estimación estable.
- La evaluación estructural permanece en `not_evaluated` por falta de anotaciones de referencia y de predicciones estructurales comparables.

El diagnóstico de capacidad que llega a `K=384` utiliza una semilla y *perplexity* de validación. El punto de `K=384` costó 11 019 segundos por ajuste. La línea cuadrática de la figura es una referencia anclada, no una ley ajustada a los tiempos. La corrida `curva_rehecha` quedó incompleta, sin `results_summary.csv`, y no se utiliza como resultado citable.

## Figuras incorporadas

Las figuras proceden de `artifacts/figuras/` del commit `2535e70`. Antes de incorporarlas se corrigieron algunos títulos y rótulos en castellano mediante `scripts/apply_figure_text_corrections.py`. La intervención cubre únicamente texto editorial: no modifica datos, escalas, marcas, intervalos ni posiciones. El script recibe como entrada los PDF originales del repositorio experimental y escribe las copias utilizadas por la tesis en `figures/chapter4/`.

| Figura | SHA-256 original | SHA-256 en la tesis | Uso |
|---|---|---|---|
| `fig1_curva_aprendizaje.pdf` | `445C113E1B3DE64994D1250313920E4587E3FD3EE0738E9F74B58B24C8E88469` | `7C8AC2B195CCA12A8379AD8B1E63E57357FF38C2AB2BE522054843F5BCCECE55` | curva principal y dispersión entre semillas |
| `fig2_capacidad_hmm.pdf` | `6A1E4AE7FA9DCD07DE7BAEE46D3F79A5E9893B1F35CC878C8674232447DC5E1D` | `5D6D00757777AC57B477421201E14F656489A32C08FFAD353A45283DD593B17F` | diagnóstico de capacidad y costo del HMM |
| `fig3_sensibilidades.pdf` | `64A57AF1E2E2D41E8063D9409B94851B28E8B87D8FA44A47DF66E24AE59680C4` | `B2125B15549A7728A20A63F6177B3EA7E3492E283022217B160826E105EA6AE1` | exposición, capacidad y particiones |
| `fig4_comparaciones_pareadas.pdf` | `F37E45A075D5CF7B503B7F36550AD237151CC1290917AD1CE6E1549FEDF1E710` | `3E9BCF4562AF542910D106E98FF97472717BFA1EF0189FE77FD66F8A6DBB7CD6` | 30 contrastes pareados |
| `fig5_pareto_prediccion_costo.pdf` | `07C7EA078C3BC74D5BC19FC055A30F6F6AB0C0742D8F0980830D2DB6B692169E` | `C2B711E2E6EA7F108668CE78F2DFAC83C54581AE64BA23286AD57FCD3132BAA5` | proyección bidimensional de NLL y ajuste |
| `fig6_unidad_de_analisis.pdf` | `81D80834390C0BBC490F29B899BB7CEAA37E10BDFF1C940EAA2FC24E2D623DE6` | `3FF5C3827F155D5F3108147A95FEEB76F56DDB2F5D19BDC3C74EA37E88C02466` | diferencia entre promediar por obra y por evento |

Las fuentes declaradas por el script son `results_summary.csv`, `engineering_costs.csv`, `piece_metrics_raw.csv`, `pairwise_comparisons.json` y tres diagnósticos de capacidad. Como estos archivos no están en Git, las figuras finales pueden verificarse por hash, pero no regenerarse desde una clonación limpia. Además, el script contiene algunos metadatos fijos ---entre ellos la referencia de ±0.047 y el denominador 414---, por lo que el manuscrito no describe las figuras como derivadas exclusivamente de datos leídos en tiempo de ejecución.

## Tablas de la corrida principal

Las tablas `chapter4_learning_curve_results.tex`, `chapter4_cost_results.tex` y `chapter4_pairwise_results.tex` fueron generadas originalmente desde el reporte histórico de la corrida principal en el commit `b11a2731a6fb3c812dc0bfd0831b7b065a016142`, mediante `scripts/generate_chapter4_results.py`. Sus valores principales coinciden con el reporte auditado integrado en `2535e70`. Se conservan sus comentarios de procedencia histórica; no se sustituyó el commit a mano.

Las sensibilidades se incorporan mediante figuras y prosa, no mediante cambios manuales a esas tablas. Una futura regeneración directa requeriría recuperar los CSV y JSON primarios y ampliar el generador para leerlos.

## Ejercicio manual sobre Bach

El Capítulo 2 conserva una comprobación manual sobre el *Preludio en Do mayor*, BWV 846. Su procedencia es distinta de las corridas automatizadas:

- `figures/Inferida.png` conserva la matriz inferida original;
- `figures/real.png` conserva la matriz construida mediante etiquetado y conteo manual;
- `figures/Error.png` conserva la diferencia absoluta registrada durante el ejercicio;
- no se localizó la hoja intermedia de conteos ni una segunda anotación independiente.

Los tres originales se conservan sin modificaciones. `scripts/generate_bach_manual_figures.py` transcribe los valores visibles y genera versiones limpias en PDF y PNG. `figures/bach_manual_figures_manifest.json` registra rutas, hashes SHA-256 y transformaciones de presentación. La matriz de error se transcribe de su propia imagen y no se recalcula a partir de las otras dos, pues los valores visibles están redondeados a dos decimales.

El conteo narrativo asociado registra 30 cambios en la referencia manual, 27 en la trayectoria inferida y 22 coincidencias. Estas cantidades se presentan como un ejercicio ilustrativo. No se utilizan como estimación general de exactitud ni como evidencia de superioridad entre familias de modelos.

## Límites que deben permanecer visibles

- La curva principal del HMM finito utiliza `K<=48`; la sensibilidad ampliada mejora el resultado, pero tampoco encierra el óptimo.
- Las barras de la curva miden dispersión entre semillas dentro de una partición. Las tres particiones muestran una variación mayor y contienen distinto número de eventos de entrenamiento.
- La comparación temporal mezcla GPU para el transformador y CPU para los modelos clásicos, además de presupuestos de selección distintos.
- La proyección de NLL y tiempo de ajuste coloca al VOMM y al transformador en la frontera; si se añade tiempo de evaluación, cambia la relación de dominancia. Ninguna de las dos sustituye el eje estructural faltante.
- La obra y el evento responden preguntas diferentes. El manuscrito declara la obra como unidad de inferencia principal.
- No hubo anotaciones estructurales. La menor NLL no demuestra que un modelo haya recuperado frases, secciones o funciones armónicas.
- Las pruebas unitarias y de regresión respaldan contratos de software; no se presentan como evidencia musical ni sustituyen las corridas.
