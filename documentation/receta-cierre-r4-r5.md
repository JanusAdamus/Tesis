# Receta para cerrar reproducibilidad y costo computacional

Esta receta completa los requisitos R4 y R5 de la tesis. Debe ejecutarse en la computadora que contiene el corpus PDMX y los artefactos originales. No sustituye las sensibilidades ya realizadas ni autoriza a cambiar cifras del manuscrito antes de obtener artefactos auditados.

> **Estado al 5 de septiembre de 2026.** El benchmark de configuraciones fijadas, su auditoría, el manifiesto del entorno y los escenarios monetarios ya fueron ejecutados y recibidos. Con ellos se actualizó R5. La medición de RAM conserva una salvedad de atribución porque los modelos compartieron proceso. Para R4 todavía faltan el paquete público de la comparación predictiva y la comprobación desde una clonación limpia. Las instrucciones siguientes se conservan como registro del procedimiento; no deben repetirse las etapas ya terminadas salvo que se busque corregir la atribución de RAM.

## 1. Conservar el estado que se va a ejecutar

Antes de mover el repositorio, revisar los cambios locales de `Melodies`. En particular, la versión de `music21` debe quedar fijada en `9.9.1`, porque otra versión cambia el conjunto efectivo de piezas. El registro de hardware también debe guardar esa versión.

```powershell
cd D:\Melodies
git status --short
git diff --check
git log -1 --oneline
```

Si aparecen cambios locales, integrarlos en un commit propio antes de pasar a la computadora principal. No mezclar ese commit con resultados de una corrida.

En la computadora principal, partir de una clonación limpia o de una rama sin modificaciones:

```powershell
git pull --ff-only origin master
py -3.12 -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install --upgrade pip
& '.\.venv\Scripts\python.exe' -m pip install -e .
& '.\.venv\Scripts\python.exe' -m unittest discover -s tests
& '.\.venv\Scripts\python.exe' -m unittest discover -s next_token_experiment/tests
git diff --check
```

Anotar el `commit` ejecutado, la versión de Python y el resultado de las dos suites. Si falla una prueba, detenerse antes de entrenar.

## 2. Verificar el corpus antes de cualquier corrida

Usar el mismo muestreo de 3000 archivos, la misma semilla y el caché reconstruido con `music21==9.9.1`. Antes de entrenar, comprobar estos datos:

- 3000 entradas en el caché;
- 2933 piezas preparadas;
- 67 exclusiones;
- 693754 eventos;
- SHA-256 del caché: `F42F9D7AB8550A4C366CFCF410C3CF67C85FAD46F5C4F54818403DEEC328E144`.

La ruta del corpus puede cambiar de una máquina a otra. Esa ruta no debe aparecer en los artefactos que se publiquen. El manifiesto sí debe conservar el identificador del corpus, el hash del caché, las versiones de las bibliotecas y el recuento de exclusiones.

## 3. Completar la medición de recursos

El código actual registra tiempos, dispositivo, complejidad del modelo y memoria máxima asignada por CUDA. Para cerrar R5 falta medir de manera consistente la memoria del proceso en CPU y distinguir la búsqueda de configuraciones del ajuste final.

### Cambio de código propuesto

Agregar `Comparacion/resource_monitor.py` con un monitor que:

1. muestree el RSS del proceso y de sus procesos hijos mediante `psutil`;
2. registre el máximo observado en bytes;
3. reinicie y lea `torch.cuda.max_memory_allocated()` cuando el modelo utilice CUDA;
4. guarde el intervalo de muestreo y el alcance de la medición;
5. no modifique las semillas, los datos ni el procedimiento de ajuste.

Integrar el monitor en el punto donde el `runner` ya mide `fit_seconds` y `evaluation_seconds`. Añadir a `engineering_costs.csv`, como mínimo, estas columnas:

```text
model
data_fraction
data_seed
model_seed
fit_seconds
evaluation_seconds
peak_process_memory_bytes
peak_gpu_memory_bytes
device
cpu_model
gpu_model
logical_cpu_count
python_version
music21_version
numpy_version
torch_version
```

Cuando una medida no aplique, guardar un valor nulo junto con un campo de estado. No convertir un dato ausente en cero.

Añadir pruebas que usen una carga pequeña y comprueben que:

- el máximo de memoria del proceso es positivo;
- la memoria de los procesos hijos se incluye;
- la memoria CUDA queda nula, con estado `not_applicable`, en CPU;
- las columnas nuevas aparecen en `engineering_costs.csv`;
- el monitor no altera las predicciones ni la selección de configuraciones.

## 4. Ejecutar un benchmark del ajuste final

La corrida principal mezcla búsqueda de configuraciones y ajuste. Esa cifra debe conservarse porque describe el costo del protocolo. Para comparar el costo de los modelos con mayor limpieza, añadir un modo de benchmark que cargue de una corrida auditada la configuración elegida para cada familia y repita sólo el ajuste final y la evaluación.

El comando puede exponerse como `scripts/run_resource_benchmark.py`. Debe recibir la corrida de origen, la fracción, la partición y el número de repeticiones. Una interfaz suficiente sería:

```powershell
& '.\.venv\Scripts\python.exe' scripts\run_resource_benchmark.py `
  --source-run artifacts\Comparacion\tesis_3000_gpu_20260823_1941 `
  --fraction 1.0 --split-seed 7 --repetitions 3 `
  --output-dir artifacts\resource_benchmark\final_fit_split7
```

Las tres repeticiones son repeticiones técnicas de tiempo y memoria. Deben usar la misma configuración y la misma semilla del modelo; no cuentan como nuevas réplicas estadísticas del desempeño. Ejecutarlas sin otras cargas intensivas y registrar temperatura o estrangulamiento térmico si el equipo lo informa.

El benchmark debe producir:

- `resource_benchmark_raw.csv`, con una fila por modelo y repetición;
- `resource_benchmark_summary.csv`, con mediana, mínimo y máximo de tiempo y memoria;
- `resource_benchmark_environment.json`, con hardware, sistema y versiones;
- `resource_benchmark_config.json`, con la corrida de origen, partición, configuraciones y semillas;
- `resource_benchmark_audit.json`, con cobertura, hashes y estado final.

Los modelos clásicos pueden ejecutarse en CPU y el transformador en GPU, como en el uso previsto, pero el informe debe identificar los dispositivos. Esta medición describe un escenario operativo controlado; no demuestra que un algoritmo sea intrínsecamente más barato que otro.

## 5. Ejecutar y auditar las corridas pendientes

Usar el orden que ya está documentado en `docs/auditoria-ejecucion-pendiente.md`: exposición de ventanas, rejilla ampliada del HMM, particiones 17 y 29, y diagnósticos del HDP-HMM. Antes de cada corrida, ejecutar el modo de planeación y comprobar que el corpus no esté vacío.

Para el corpus principal, conservar siempre estos argumentos:

```text
--max-files 3000
--corpus-sample-seed 7
--corpus-cache artifacts\corpus_cache_3000.jsonl
--n-workers 6
--transformer-device cuda
```

No usar doce trabajadores al mismo tiempo que la GPU. La ejecución anterior mostró que esa combinación satura la máquina. Si una corrida se interrumpe, retomarla con el mismo nombre y `--resume`.

Al terminar cada corrida:

```powershell
& '.\.venv\Scripts\python.exe' -m Comparacion.cli `
  --audit-run artifacts\Comparacion\NOMBRE_DE_CORRIDA
```

Sólo un estado `passed` permite trasladar cifras a la tesis.

## 6. Preparar un paquete reproducible para R4

Crear un paquete sin el corpus y sin rutas personales. Debe contener:

- configuración completa y semillas;
- manifiesto del corpus y exclusiones;
- asignación de obras a entrenamiento, validación y prueba;
- `results_raw.csv` y `results_summary.csv`;
- comparaciones pareadas, sensibilidades y diagnósticos;
- `engineering_costs.csv` y los archivos del benchmark de recursos;
- manifiesto SHA-256 de todos los archivos;
- informe de auditoría;
- instrucciones exactas para regenerar tablas y figuras.

Si el paquete es pequeño y no contiene material restringido, puede publicarse en el repositorio. Si no lo es, usar una entrega versionada y enlazarla desde el repositorio. No publicar partituras de terceros ni rutas absolutas del equipo.

Después, repetir la verificación desde una clonación nueva:

1. instalar el entorno;
2. recuperar el corpus según su fuente documentada;
3. verificar el hash del caché;
4. ejecutar una corrida pequeña para comprobar el pipeline;
5. regenerar las tablas y figuras desde los CSV y JSON publicados;
6. comparar los hashes de los productos deterministas;
7. documentar cualquier variación esperada de las operaciones no deterministas.

## 7. Validar los requisitos sin dar por cumplido lo que falta

Agregar `docs/engineering-requirements.json` con R1 a R7 y las rutas de evidencia. Implementar `scripts/validate_engineering_requirements.py` para comprobar archivos, hashes, estados de auditoría y campos obligatorios.

El validador debe mantener R4 como `partial` si falta el paquete de resultados o si una clonación limpia no regenera tablas y figuras. R5 debe permanecer `partial` si falta la memoria máxima, el benchmark del ajuste final o un escenario económico con tarifas y fecha documentadas.

El resultado debe guardarse en:

```text
artifacts/requirements_validation.json
artifacts/requirements_validation.md
```

Las pruebas del validador deben incluir casos incompletos. El objetivo es detectar huecos, no producir un estado favorable por defecto.

## 8. Traslado posterior a la tesis

Cuando estén listos los artefactos, actualizar únicamente:

- la fila R4 de la tabla de trazabilidad, si la reproducción limpia fue satisfactoria;
- la fila R5, si ya existen memoria máxima y benchmark auditado;
- la sección de costo del Capítulo 4;
- el balance de viabilidad y las conclusiones.

Las tablas y figuras deben generarse desde los artefactos estructurados. Conviene mantener separadas cuatro afirmaciones: qué se observó, cómo se interpreta, qué limitación permanece y qué trabajo se propone. No atribuir a la nueva medición una ventaja estadística ni una mejora musical que no haya sido evaluada.

## Entrega que debe regresar de la computadora principal

Para incorporar los resultados bastan estos elementos:

1. hash del `commit` ejecutado;
2. nombres de las corridas y estados de auditoría;
3. paquete reproducible o enlace a la entrega versionada;
4. `resource_benchmark_raw.csv` y `resource_benchmark_summary.csv`;
5. manifiesto del entorno;
6. registro de la prueba desde clonación limpia;
7. salida del validador de requisitos.

Con esa evidencia se podrá cerrar R4 y R5 sin reconstruir cifras a partir de capturas o notas manuales.
