# Guía de estilo de redacción de la tesis

Esta guía registra la voz que ya domina los capítulos 0--4 y el Apéndice A. Su propósito es conservarla al incorporar resultados nuevos, en particular la comparación entre HMM, HDP-HMM y transformador. No obliga a reproducir errores gramaticales, notas provisionales ni inconsistencias presentes en borradores antiguos.

## Voz y tono

- Escribir en español académico, sobrio y explicativo.
- Preferir construcciones impersonales: «se adopta», «se considera», «se obtiene», «conviene distinguir» y «esta tesis propone».
- Reservar la primera persona para decisiones efectivamente tomadas por el autor y evitar cambios arbitrarios entre «yo», «nosotros» y la voz impersonal.
- Formular afirmaciones con fuerza proporcional a la evidencia. Usar «muestra» para resultados directos, «sugiere» para interpretaciones y «no prueba» o «debe leerse con cautela» cuando existan límites de alcance.
- Evitar lenguaje promocional, superlativos, dramatización y oposiciones simplistas entre modelos «clásicos» y «modernos».

## Progresión argumental

La unidad típica de exposición sigue este orden:

1. presentar el problema conceptual o la pregunta que motiva la sección;
2. explicar por qué la formulación anterior resulta insuficiente;
3. introducir la definición, ecuación, algoritmo o diseño experimental;
4. traducir su significado al contexto musical;
5. cerrar con alcance, limitación y enlace hacia el paso siguiente.

Los capítulos comienzan recuperando el resultado conceptual del capítulo anterior y explicando qué decisión de modelado se modifica. Las secciones no deben aparecer como piezas aisladas: cada una debe responder una pregunta explícita y preparar la siguiente.

## Construcción de párrafos

- Favorecer párrafos continuos de entre dos y cinco oraciones, con una idea central reconocible.
- Abrir con la función del párrafo y desarrollar después la precisión técnica.
- Usar transiciones con moderación y sentido lógico: «En particular», «Por ello», «En consecuencia», «Aun así», «Sin embargo», «Dicho de otro modo» y «Bajo esta luz».
- Integrar enumeraciones breves dentro de la prosa. Usar `enumerate` únicamente cuando el orden sea metodológico o constituya un criterio de decisión explícito.
- Evitar cadenas de frases telegráficas, listas decorativas y conclusiones que repitan literalmente el párrafo anterior.

## Matemáticas y algoritmos

- Definir símbolos, dominio e interpretación antes de emplearlos.
- Introducir cada ecuación con una oración completa y explicar inmediatamente después qué significa.
- Mantener el puente entre formulación probabilística e interpretación musical; ninguna derivación extensa debe quedar sin lectura sustantiva.
- Distinguir con claridad modelo conceptual, aproximación computacional y parámetros concretos de una corrida.
- Conservar notación uniforme entre capítulos, tablas, figuras y código: HMM finito, HDP-HMM truncado, estados efectivos, log-verosimilitud, NLL por token, *perplexity* y exactitud *top-k*.

## Presentación de resultados

Cada resultado nuevo debe vincularse con un artefacto reproducible y presentarse en cuatro movimientos:

1. identificar corpus, división, representación, semilla y presupuesto experimental;
2. reportar magnitud, denominador, unidad y métrica sin redondeos engañosos;
3. explicar qué comparación permite sostener;
4. declarar qué no permite concluir y qué alternativa sigue abierta.

Separar siempre observación e interpretación. Una mejora predictiva no implica por sí misma superioridad musicológica; una reducción de estados no implica automáticamente mejor segmentación; una corrida de validación rápida no constituye evidencia final.

## Comparación entre modelos

La comparación central debe realizarse sobre la misma tarea de predicción, los mismos *splits* por obra, el mismo corpus y métricas compatibles. El objetivo no es enfrentar etiquetas tecnológicas, sino evaluar compromisos entre:

- calidad predictiva;
- complejidad latente o capacidad del modelo;
- tiempo, memoria y hardware;
- costo de implementación y reproducción;
- interpretabilidad musical.

Cuando las familias requieran métricas adicionales propias, éstas deben reportarse como complemento y no sustituir el núcleo comparable. La conclusión debe distinguir qué modelo resulta preferible para predicción, explicación estructural o costo experimental.

## Tablas, figuras y evidencia

- Introducir toda tabla o figura antes de insertarla y explicar después el patrón relevante.
- No transcribir manualmente valores que puedan generarse desde artefactos estructurados.
- Mantener consistentes cifras, nombres de corridas y tamaños de muestra en texto, tablas y pies.
- No inventar referencias, resultados, configuraciones, tiempos ni detalles metodológicos. Marcar lo faltante como pendiente de verificación.
- Conservar resultados negativos, errores de ejecución y experimentos inconclusos cuando afecten la interpretación.

## Convenciones de LaTeX y lengua

- Mantener acentos, signos de apertura y ortografía española.
- Usar `\emph{}` para términos extranjeros en prosa y `\texttt{}` para perfiles, rutas o identificadores de código.
- Usar comillas LaTeX ``así'' cuando corresponda.
- Asignar `\label{}` estable a capítulos, secciones, ecuaciones, tablas y figuras que se referencien.
- Evitar introducir anglicismos si existe un término técnico español claro; conservar el término inglés cuando sea el nombre estándar de una métrica o implementación.

## Plantilla breve para incorporar un experimento

> La comparación se realizó sobre [corpus y división], utilizando [representación] y [configuración verificable]. La Tabla~`\ref{...}` muestra que [resultado numérico directo]. Esta diferencia sugiere [interpretación acotada], pero no basta para afirmar [conclusión más fuerte]. En particular, [limitación o explicación alternativa]. Por ello, el siguiente contraste debe aislar [factor pendiente].

Esta plantilla orienta la secuencia lógica; no debe copiarse de manera mecánica ni completarse con datos no verificados.
