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

La suite completa produjo `44 passed`. El entorno aislado utilizado se encuentra en `C:\Users\AdrianGonzalez\.codex\venvs\melodies-py311`; esta ruta es una condición local de ejecución, no una ruta que deba escribirse en el código o en el cuerpo de la tesis.

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

## Correspondencia con capítulos, tablas y figuras

| Elemento de la tesis | Fuente o generador esperado | Estado de verificación |
|---|---|---|
| Tablas y figuras del capítulo 3 | `D:\Melodies\scripts\generate_thesis_chapter3_assets.py` y artefactos del pipeline clásico | Pendiente de regenerar desde `bbb5575`; los archivos actuales preceden a este registro Git. |
| Tablas conceptuales del capítulo 4 | `chapters/tables/chapter4_*.tex` | Son plantillas argumentales, no resultados finales. |
| Curvas HMM/HDP-HMM/transformador | `D:\Melodies\Comparacion` y `artifacts\Comparacion\<run>` | Pipeline verificado mediante `integration_smoke`; falta la corrida canónica con múltiples semillas. |
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
