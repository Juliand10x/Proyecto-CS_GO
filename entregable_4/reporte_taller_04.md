# Taller 04 - Diseño Metodológico del Proyecto

## Parte 0: Diseño Metodológico en la Literatura (Revisión)

### 1. Enfoque metodológico predominante
Los estudios previos sobre estimación de victorias en *esports* utilizan principalmente un **enfoque predictivo** apoyado por **diseños observacionales retrospectivos**. El propósito central de estos análisis es proyectar el resultado de los encuentros (victoria/derrota) basándose en indicadores históricos de rendimiento, elo/glicko o rankings previos.

### 2. Características comunes de los estudios
- **Tipo de datos más usados:** Bases de datos de corte transversal repetido procedentes de APIs públicas y repositorios como HLTV (estadísticas de *box-score* y parseo de demos históricas).
- **Estrategia analítica típica:** Aplicación extensiva de modelos de Machine Learning tradicionales (Random Forest, Gradient Boosting) y modelos estadísticos frecuentistas como la regresión logística binaria.

### 3. Limitaciones recurrentes
- **Limitaciones metodológicas:** La gran mayoría de los enfoques carecen de cuantificación de la incertidumbre epistémica y aleatoria, produciendo estimaciones sobre-confiadas (calibración probabilística pobre).
- **Problemas de interpretación:** A menudo los modelos de ML de caja negra no permiten interpretar el peso de variables clave, y existe la tendencia a confundir correlaciones de desempeño pre-partido con causalidad absoluta.

### 4. Implicación para nuestro proyecto
Nuestro enfoque actual está fuertemente alineado con llenar las brechas identificadas en la literatura. Al adoptar un modelo de Regresión Logística Bayesiana, no solo pasamos de predicciones puntuales a distribuciones probabilísticas, sino que abordamos de manera directa la necesidad de evaluar la incertidumbre (utilizando intervalos de credibilidad HDi) antes del inicio del encuentro.

---

## Parte 1: Clasificación de la Pregunta

**1. Pregunta de Investigación Refinada:**
¿Cómo puede estimarse la probabilidad posterior de victoria de un equipo profesional de CS:GO/CS2 mediante un modelo de regresión logística bayesiana que incorpore rendimiento reciente, ranking relativo y desempeño histórico por mapa?

**2. Clasificación:**
- **Primaria:** Predictiva.
- **Secundaria:** Descriptiva/Explicativa.

**3. Justificación de la Clasificación:**
Es preeminentemente **predictiva** porque el objetivo principal es utilizar información *a priori* (histórico de equipos, estadísticas por mapa seleccionado, momento de forma) para estimar qué tan probable es un resultado binario futuro o no observado (gana o pierde). Al mismo tiempo, goza de un matiz *explicativo* dado que, al emplear inferencia bayesiana de parámetros interpretables, permite entender la distribución y peso específico que tiene jugar un mapa frente a otro.

---

## Parte 2: Caracterización de los Datos

- **Datos disponibles:** Contamos con bases de datos públicas históricas de CS:GO y CS2 consolidadas desde Kaggle (scrapeadas de HLTV). Poseemos un set masivo primario `results.csv` para etiquetado, un set de variables de entorno de juego `picks.csv`, y sobre todo un dataset depurado `cs2_newestcombinedmatches.csv` que concentra *features* precalculados como la diferencia de clasificación (`rating_diff`) y daño (`adr_diff`).
- **Tipo de estructura:** Datos observacionales estructurados como panel desbalanceado o *pooled cross-section*. Observamos a múltiples equipos y jugadores, en variados mapas, agrupados transversalmente por cada evento individual (`match_id`).
- **Nivel de acceso:** Datos de carácter público. Los datos ya están ingestados localmente a través del pipeline `capture_data.py`.
- **Limitaciones:** Los datos adolecen de un "sesgo de supervivencia" en el formato de *Picks & Bans* (equipos nunca juegan mapas donde estadísticamente son defectuosos). Además, existe ruido introducido por factores exógenos como cambios sorpresivos de *rosters* de jugadores, la evolución entre parches, y el cambio generacional de CS:GO a CS2.

---

## Parte 3: Propuesta de Diseño Metodológico

- **Estrategia general:** Se plantea un diseño de carácter cuantitativo, observacional y retrospectivo.
- **Tipo de análisis:** Modelado Predictivo e Inferencia Bayesiana (Regresión Logística Bayesiana).
- **Qué buscamos obtener:** En lugar de perseguir estimaciones puntuales estáticas de *Machine Learning*, nuestro objetivo es computar la **distribución posterior de los parámetros**. Buscamos que la predicción final devuelva una probabilidad clara de victoria acompañada de su Intervalo de Densidad Más Alta (HDI), de modo que demostremos *certidumbre matemática* (ej: 65% probabilidad de victoria, con un HDI del 58% al 72%).

---

## Parte 4: Evaluación de Coherencia

- **¿Este diseño responde realmente la pregunta?** Sí, el diseño bayesiano se acopla perfectamente a nuestra formulación: estimar *probabilidades posteriores*. Es el enfoque matemáticamente correcto para actualizar creencias según evidencia.
- **¿Los datos permiten este análisis?** Definitivamente. Como comprobamos en el EDA inicial, variables continuas clave como el `rating_diff` tienen suficiente nivel de correlación (0.26) con la variable respuesta binaria como para modelar un efecto logit sobre la victoria. La granularidad de los *match_id* enlazados con *picks* provee información suficiente para nutrir la función de verosimilitud (*likelihood*).
- **¿Qué no podemos afirmar con este diseño?** No podremos emitir afirmaciones causales de naturaleza determinista (v.g. "Seleccionar jugar Inferno CAUSA imperativamente un aumento de 15% en victorias"). Tampoco pronosticaremos disrupciones repentinas en pleno evento en vivo que la estadística retrospectiva no contempla (fatiga del día, estado mental de un jugador).

---

## Parte 5: Matriz de Coherencia Metodológica

| Elemento                          | Descripción                                                                                                                                                                                                                                                                                                                                                                                                         |
| :-------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Pregunta de investigación**     | ¿Cómo estimar la probabilidad posterior de victoria de un equipo de CS:GO/CS2 con un modelo logístico bayesiano usando ranking, mapa y rendimiento reciente?                                                                                                                                                                                                                                                        |
| **Tipo de pregunta**              | Predictiva (naturaleza probabilística).                                                                                                                                                                                                                                                                                                                                                                             |
| **Datos disponibles o esperados** | Datos secundarios observacionales de repositorios públicos (*Kaggle/HLTV*). *Datasets* rectangulares de matches.                                                                                                                                                                                                                                                                                                    |
| **Diseño metodológico**           | Diseño cuantitativo observacional / estadístico.                                                                                                                                                                                                                                                                                                                                                                    |
| **Técnica o modelo sugerido**     | Regresión Logística Bayesiana (Generación de Muestras vía cadenas de Markov Monte Carlo - MCMC).                                                                                                                                                                                                                                                                                                                    |
| **Limitaciones**                  | Incapacidad para detectar causalidad directa; sesgo estructurado por el veto de mapas; falta de variables psicológicas o físicas del entorno presencial.                                                                                                                                                                                                                                                            |
| **Justificación de Coherencia**   | Al poseer variables predictores contínuas sólidas y un *target* categórico (Victoria/Derrota), la *Regresión Logística* es estándar. Pero incorporarle inferencia *Bayesiana*, garantiza que el modelo contemple la dinámica del *prior* y refleje en forma de densidades matemáticas la incertidumbre inherente del *esport*, respondiendo a la premisa de la pregunta exacta y el valor diferencial del proyecto. |
