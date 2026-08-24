# Auditoría bibliográfica final

## Alcance

Esta revisión fue una auditoría dirigida de afirmaciones del manuscrito, no una revisión sistemática del campo. Su objetivo fue identificar conceptos importantes que aparecían sin respaldo, verificar fuentes adecuadas y evitar una acumulación de citas que no ayudara al argumento.

Fecha de búsqueda: 24 de agosto de 2026.

## Criterios

Se incluyeron fuentes que cumplen al menos una de estas funciones:

1. presentan el método matemático o computacional utilizado;
2. documentan una aplicación musical directamente relacionada con la interpretación propuesta;
3. definen un formato o corpus del que depende el experimento;
4. respaldan la motivación probabilística de la expectativa musical.

Se prefirieron trabajos primarios, fuentes fundacionales y especificaciones oficiales. Se descartaron referencias que sólo ampliaban el panorama tecnológico sin sostener una afirmación concreta del manuscrito.

## Fuentes consultadas

- OpenAlex, para búsqueda temática y localización de DOI;
- Crossref, para verificar metadatos de artículos con DOI;
- archivos oficiales de ISMIR, para el trabajo de HMM aplicado a acordes;
- sitios de los editores y actas oficiales de Wiley, MIT Press, NeurIPS y OpenReview;
- especificación oficial MusicXML 4.0 del W3C Music Notation Community Group.

## Consultas principales

- `On Prediction Using Variable Order Markov Models`
- `Chord Segmentation and Recognition Using EM-Trained Hidden Markov Models`
- `MusicXML An Internet-Friendly Format for Sheet Music`
- `Music Transformer Generating Music with Long-Term Structure`
- `A tutorial on hidden Markov models and selected applications in speech recognition`
- `Auditory expectation statistical learning music Pearce Wiggins 2012`
- `Music and Probability Temperley 2007`

## Referencias incorporadas o activadas

| Clave | Función en la tesis | Verificación principal |
|---|---|---|
| `pearce2012` | Expectativa musical y modelado probabilístico | DOI y página de Wiley |
| `sheh2003` | Uso de HMM y EM en segmentación y reconocimiento de acordes | Archivo oficial de ISMIR 2003 |
| `begleiter2004` | Definición y evaluación de modelos de Markov de orden variable | DOI de JAIR y OpenAlex |
| `musicxml2021` | Naturaleza y propósito del formato MusicXML/MXL | Informe oficial del W3C Music Notation Community Group |
| `rabiner1989` | Problemas clásicos, algoritmo hacia adelante, Viterbi y Baum-Welch | DOI de IEEE/Crossref |
| `temperley2007` | Probabilidad, expectativa y contexto tonal en música | MIT Press |
| `vaswani2017` | Arquitectura del transformador | Actas oficiales de NeurIPS |
| `huang2018musictransformer` | Aplicación del transformador a música simbólica | OpenReview/ICLR |

También se completaron DOI o metadatos faltantes en referencias ya utilizadas cuando la fuente primaria los proporcionó.

## Decisiones de moderación

- La afirmación antropológica general con la que comenzaba el capítulo 1 se eliminó en vez de añadir varias citas tangenciales.
- No se incorporaron referencias a S4, Mamba ni otras arquitecturas porque no participan en la comparación ejecutada.
- No se añadieron citas a cada decisión de implementación. Las semillas, tamaños de muestra y configuraciones se respaldan mediante artefactos del proyecto, no mediante literatura externa.
- El ejercicio histórico del preludio de Bach se reincorporó después de que el autor aclaró que la referencia procedía de un conteo manual. Se conservan las imágenes originales y se declara la ausencia de la hoja intermedia de conteos; una cita bibliográfica no sustituye esa procedencia experimental.
