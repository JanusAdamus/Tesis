# Plan para explicitar el proceso de diseño computacional

## Propósito

Enmarcar la tesis como el diseño, implementación, verificación y validación de una solución computacional, sin alterar retrospectivamente la historia del proyecto ni presentar la tabla de trazabilidad como si fuera, por sí sola, el proceso de diseño.

El manuscrito ya contiene los elementos sustantivos: delimita el problema, declara requisitos y restricciones, considera cuatro alternativas, describe la arquitectura común, documenta la implementación y valida el sistema mediante pruebas, auditorías y experimentos. La brecha actual es principalmente expositiva: esos elementos aparecen distribuidos y el lector debe reconstruir la secuencia de decisiones.

## Resultado esperado

Al terminar, el Capítulo 0 deberá permitir que una persona que lee la tesis por primera vez responda, sin acudir al código, las siguientes preguntas:

1. ¿Qué problema de ingeniería se intenta resolver?
2. ¿Qué requisitos, restricciones y supuestos condicionan la solución?
3. ¿Qué alternativas se consideraron y con qué criterios se eligieron?
4. ¿Qué se diseñó antes de ejecutar la comparación final?
5. ¿Cómo se verificó que la implementación respetara el protocolo?
6. ¿Cómo se validó que la solución permitiera responder la pregunta de investigación?
7. ¿Qué decisiones se revisaron después de observar resultados o fallas?
8. ¿Qué requisitos permanecen parciales o fuera del alcance?

## Criterio histórico

El proceso se describirá como iterativo. No se afirmará que toda la verificación precedió a la primera implementación. La tesis sí puede sostener, con la evidencia versionada, que la especificación consolidada del protocolo se registró antes de la corrida experimental principal y que las auditorías y sensibilidades posteriores comprobaron o revisaron decisiones concretas.

Se conservará la siguiente distinción:

- **Verificación:** comprobar que el sistema implementa los requisitos y el protocolo declarados.
- **Validación:** comprobar que la solución produce evidencia pertinente para responder la pregunta de investigación dentro de su alcance.

## Proceso que debe quedar visible

| Etapa | Pregunta que responde | Evidencia ya disponible | Intervención necesaria |
|---|---|---|---|
| 1. Identificación y delimitación | ¿Cuál es el problema y qué queda fuera? | Pregunta central, alcance predictivo y exclusión de afirmaciones estructurales sin referencia | Reunirlo como entrada del proceso |
| 2. Requisitos, restricciones y supuestos | ¿Qué debe cumplir una comparación válida? | R1--R7, condiciones del corpus, hardware y anotaciones | Enlazar cada requisito con la etapa que lo origina |
| 3. Generación de alternativas | ¿Qué soluciones podían atender el problema? | HMM finito, HDP-HMM, VOMM y transformador | Explicar el papel de cada alternativa sin presentarlas sólo como capítulos teóricos |
| 4. Criterios y decisión | ¿Con qué compromisos se comparan? | NLL por evento, cobertura, costo, complejidad e interpretabilidad | Añadir una síntesis breve de los criterios y sus límites |
| 5. Especificación de la solución | ¿Qué arquitectura y protocolo se fijaron? | Representación común, particiones por obra, selección con validación y auditorías | Señalar la línea de base previa a la corrida final |
| 6. Implementación | ¿Qué componentes materializan el diseño? | Preparación, modelos, evaluación, puntos de reanudación y artefactos | Relacionar componentes con decisiones, no sólo enumerarlos |
| 7. Verificación | ¿El sistema hace lo especificado? | Pruebas automatizadas, auditorías de denominadores, canonicalización y selección | Separar explícitamente esta evidencia de los resultados experimentales |
| 8. Validación | ¿La solución permite responder la pregunta? | Corrida común, comparación pareada, costos y análisis de sensibilidad | Vincular las métricas con requisitos y pregunta central |
| 9. Iteración | ¿Qué se corrigió al encontrar límites o errores? | Ventanas sin solapamiento, rejilla del HMM, particiones alternativas, presupuesto de inferencia y reglas de parada | Presentar estas acciones como retroalimentación del proceso |

La Tabla de trazabilidad R1--R7 será una salida de este proceso: mostrará la relación entre requisitos, decisiones y evidencia. No sustituirá la narración de cómo se tomaron y comprobaron las decisiones.

## Cambios en el manuscrito

### 1. Incorporar una sección explícita

**Archivo:** `chapters/chapter0.tex`

Añadir, antes de la exposición detallada del flujo experimental, una sección titulada `Proceso de diseño de la solución`. La sección debe partir de la intuición de que comparar algoritmos heterogéneos requiere diseñar primero el terreno común de comparación. Después debe recorrer las nueve etapas anteriores de manera continua y remitir a las secciones donde se desarrollan.

La sección no debe duplicar el contenido del capítulo. Su función es proporcionar el mapa argumental y explicar por qué el resultado de ingeniería es el sistema reproducible de comparación, no uno de los cuatro modelos aislados.

### 2. Añadir un diagrama iterativo

**Archivo:** `chapters/chapter0.tex` o un archivo TikZ incluido desde `figures/`

Representar el flujo:

```text
problema -> requisitos -> alternativas -> decisión y especificación
        -> implementación -> verificación -> validación
        -> revisión de decisiones
                      |___________________________|
```

El retorno debe señalar que las sensibilidades y correcciones refinan decisiones concretas. No se dibujará un ciclo que sugiera entrenamiento indefinido ni que oculte la línea de base usada para la corrida final.

### 3. Reubicar conceptualmente la tabla de trazabilidad

**Archivos:** `chapters/chapter0.tex` y `chapters/tables/chapter0_trazabilidad.tex`

Introducir la tabla como comprobación del diseño consolidado. Mantener visibles los estados `Parcial` y `No evaluado`; un faltante no debe convertirse en cumplimiento por redacción. Cuando exista la matriz generada por Melodies, sustituir la transcripción manual por la salida reproducible.

### 4. Hacer explícitas las decisiones de alternativa

**Archivo:** `chapters/chapter0.tex`

Resumir por qué se conservaron cuatro familias y qué pregunta permite formular cada una:

- HMM finito: referencia latente de capacidad controlada;
- HDP-HMM truncado: flexibilidad en la ocupación de estados;
- VOMM: referencia predictiva interpretable basada en contexto variable;
- transformador: alternativa de mayor capacidad contextual.

No se afirmará que una familia fue elegida como solución final antes de la validación. La decisión de diseño fue construir el banco común y evaluar compromisos entre familias.

### 5. Conectar capítulos y artefactos

Añadir referencias cruzadas para que cada etapa apunte a su evidencia:

- fundamentos y representación: capítulos 1--3;
- protocolo, arquitectura, métricas y resultados: capítulo 4;
- respuesta de validación, viabilidad y límites: capítulo 5;
- requisitos y evidencia: Tabla R1--R7;
- especificaciones, pruebas y artefactos: repositorio Melodies.

## Cambios reproducibles en Melodies

El encuadre textual puede completarse sin una nueva corrida. Sin embargo, dos piezas fortalecen el cierre formal y deben integrarse cuando estén verificadas:

1. `requirements_validation.py` y `docs/engineering-requirements.json`, para generar la matriz de validación desde evidencia estructurada;
2. el paquete público de evidencia y el benchmark aislado de recursos, para cerrar R4 y R5 si las reglas se satisfacen.

La tesis no esperará esos resultados para explicar el proceso, pero tampoco adelantará su cumplimiento.

## Orden de ejecución

1. Redactar la sección `Proceso de diseño de la solución` con el contexto inmediato del Capítulo 0.
2. Incorporar el diagrama y comprobar su lectura en escala de impresión.
3. Revisar la transición hacia `De la partitura a una comparación común` para evitar repetición.
4. Ajustar la introducción de la tabla R1--R7 y las referencias cruzadas.
5. Comprobar que verificación, validación y sensibilidad no se empleen como sinónimos.
6. Revisar que cada decisión importante tenga requisito, justificación o limitación.
7. Compilar con `latexmk`, revisar referencias indefinidas y examinar visualmente las páginas modificadas.
8. Contrastar las cifras y estados con los artefactos de Melodies antes de confirmar el cambio.
9. Actualizar la tabla desde la matriz generada sólo cuando el módulo de validación esté probado y sus insumos estén disponibles.

## Criterios de aceptación

- El proceso de diseño se identifica por nombre y se entiende sin reconstruirlo entre capítulos.
- El problema, los requisitos, las alternativas y los criterios de decisión preceden narrativamente a la implementación.
- La solución se define como un sistema reproducible de comparación.
- La verificación y la validación se distinguen y cada una apunta a evidencia concreta.
- Las correcciones y sensibilidades se presentan como iteraciones, no como decisiones fijadas de antemano.
- La tabla R1--R7 aparece como trazabilidad del diseño y conserva los estados parciales.
- No se atribuye estructura musical sin anotaciones de referencia.
- No se inventan resultados de memoria, costo, uso social o precedencia histórica.
- La compilación termina sin errores y no introduce referencias cruzadas indefinidas.
- Una lectura completa del Capítulo 0 responde las ocho preguntas declaradas en este plan.

## Definición de terminado

El encuadre se considerará cerrado cuando la versión compilada muestre la sección y el diagrama, la tabla de trazabilidad esté integrada como evidencia del proceso y una revisión cruzada confirme que las afirmaciones de verificación y validación coinciden con los artefactos disponibles. Los requisitos R4 y R5 podrán permanecer parciales si todavía falta recuperar o medir evidencia; su estado no impide documentar correctamente el proceso de diseño.
