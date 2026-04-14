# Solución Punto 3.2.6: Primera especificación de las Priors

Para la realización de esta entrega, se ha optado por un enfoque de **Inferencia Paramétrica Bayesiana** a través de una **Regresión Logística**. La especificación de las *priors* se divide en tres niveles de información (Informativa, Débilmente Informativa y No Informativa), asegurando la coherencia metodológica entre el análisis exploratorio de datos (EDA) técnico y el modelo predictivo.

---

### 1. Perfil de las Priors Seleccionadas (Resumen)

| Parámetro | Variable | Tipo de Prior | Distribución | Hiperparámetros |
| :--- | :--- | :--- | :--- | :--- |
| **Habilidad Técnica** | `diff_rating` | **Informativa** | $N(\mu, \sigma^2)$ | $\mu=4.79, \sigma=1.28$ |
| **Factor Táctico** | `diff_impact` | **Débilmente Inf.** | $N(\mu, \sigma^2)$ | $\mu=1.99, \sigma=5.00$ |
| **Neutralidad Base** | Intercepto ($\alpha$) | **No Informativa** | $N(\mu, \sigma^2)$ | $\mu=0.01, \sigma=100.0$ |

---

### 2. Evidencia y Justificación Sugerida

#### **A. Análisis de Correlación con la Victoria**
Para evitar que las variables salgan "de la nada", se fundamentó la selección en la matriz de correlación ajustada contra la variable objetivo `target_t1_win` (Victoria del Equipo 1). Como se evidencia en la nueva gráfica **`justificacion_correlacion_barras.png`**, el diferencial de **Rating** tiene la correlación positiva más fuerte con el éxito, seguido por el **Impacto**.

#### **B. Justificación Prior Informativa: Diferencial de Rating**
*   **Distribución:** Normal $N(4.79, 1.28^2)$.
*   **Evidencia en EDA:** Se generó la gráfica **`evidencia_rating_winrate.png`**, la cual muestra una línea ascendente casi perfecta: a medida que el `diff_rating` aumenta, el porcentaje de victorias reales en el dataset sube del 30% al 85%.
*   **Pensamiento Crítico:** Esto justifica una prior informativa; no estamos asumiendo el efecto por capricho, sino capturando una ley natural del juego observada empíricamente.

#### **C. Justificación Prior Débilmente Informativa: Diferencial de Impacto**
*   **Distribución:** Normal $N(1.99, 5.00^2)$.
*   **Evidencia en EDA:** La gráfica **`evidencia_impacto_violin.png`** muestra que los ganadores (Target=1) tienen una distribución de impacto mucho más alta que los perdedores, pero con una varianza (dispersión) mayor que la del rating.
*   **Pensamiento Crítico:** Al haber más "solapamiento" entre ganadores y perdedores en esta métrica, decidimos usar una $\sigma=5.0$ más laxa para que los datos específicos de la entrega tengan mayor libertad de ajuste.

#### **D. Justificación de Sesgo de Mapa**
*   **Evidencia en EDA:** La gráfica **`evidencia_mapa_bias.png`** confirma asimetrías tácticas (ej. Nuke siendo fuertemente CT-sided). Esto justifica la inclusión de una prior de ajuste si el modelo final se separa por escenarios.
