# Especificación del Modelo: Regresión Logística Bayesiana Jerárquica

## 1. Estructura General

Modelamos la probabilidad de victoria de un equipo en una partida de CS:GO mediante una **regresión logística con interceptos aleatorios por mapa** (modelo jerárquico o multinivel).

---

## 2. Likelihood (Verosimilitud)

Dado que el resultado de cada partida $i$ es binario (victoria = 1, derrota = 0), definimos:

$$y_i \sim \text{Bernoulli}(p_i)$$

donde $p_i$ es la probabilidad de que el equipo 1 gane la partida $i$.

---

## 3. Función de Enlace (Link Function)

Usamos la función **logit** para transformar la combinación lineal de predictores al rango $[0, 1]$:

$$\text{logit}(p_i) = \ln\left(\frac{p_i}{1 - p_i}\right) = \alpha_{\text{map}[i]} + \beta_1 X_{i1} + \beta_2 X_{i2} + \beta_3 X_{i3} + \beta_4 X_{i4}$$

donde:
- $\alpha_{\text{map}[i]}$ = intercepto aleatorio para el mapa de la partida $i$
- $X_{i1}$ = `diff_rating` (diferencial de Rating 2.0 promedio del equipo)
- $X_{i2}$ = `diff_impact` (diferencial de Impacto táctico promedio)
- $X_{i3}$ = `diff_dmr` (diferencial de ADR — daño por ronda)
- $X_{i4}$ = `diff_kast` (diferencial de KAST — contribución en rondas)

---

## 4. Estructura Jerárquica (Interceptos por Mapa)

Cada mapa $j$ tiene su propio intercepto $\alpha_j$, que captura la asimetría táctica del mapa (ventaja CT/T, tamaño, estilo de juego). Los interceptos comparten una distribución común:

$$\alpha_j \sim \text{Normal}(\mu_\alpha, \sigma_\alpha^2), \quad j = 1, \dots, J$$

donde $J$ es el número de mapas en el pool competitivo (Nuke, Mirage, Inferno, Dust2, Overpass, Vertigo, Ancient, Anubis).

Esta estructura permite que mapas con pocas observaciones se beneficien del **pooling parcial** (regularización hacia la media global $\mu_\alpha$).

---

## 5. Priors (Distribuciones Iniciales)

Siguiendo un enfoque de "honestidad estadística", seleccionamos priors que permitan a los datos hablar sin imponer sesgos restrictivos:

### 5.1 Coeficientes de Desempeño ($\beta_k$)

$$\beta_k \sim \text{Normal}(0, 5^2), \quad k = 1, \dots, 4$$

**Justificación:** Priors débilmente informativas. Centradas en cero (asumiendo inicialmente que no sabemos si el efecto es positivo o negativo), con una desviación de 5 que permite una amplia gama de efectos en el espacio logit.

### 5.2 Intercepto Global ($\mu_\alpha$)

$$\mu_\alpha \sim \text{Normal}(0, 5^2)$$

**Justificación:** Prior neutral sobre la probabilidad base de victoria. En el espacio logit, $\mu_\alpha = 0$ corresponde a $p = 0.5$ (equipos igualados).

### 5.3 Hiperparámetro de Variabilidad entre Mapas ($\sigma_\alpha$)

$$\sigma_\alpha \sim \text{HalfNormal}(2)$$

**Justificación:** HalfNormal asegura que la desviación estándar sea positiva. $\sigma = 2$ es suficientemente flexible para capturar diferencias realistas entre mapas sin sobreadaptarse a mapas con pocos datos.

---

## 6. Diagrama del Modelo (DAG)

```
                    μ_α ~ Normal(0, 5)
                    σ_α ~ HalfNormal(2)
                        |
                   α_j ~ Normal(μ_α, σ_α²)
                      /    \
         β_k ~ Normal(0, 5²) \
              |               |
    logit(p_i) = α_map[i] + Σ_k β_k · X_ik
              |
          y_i ~ Bernoulli(p_i)
```

---

## 7. Inferencia

La inferencia se realiza mediante **MCMC** (Markov Chain Monte Carlo) usando el algoritmo **NUTS** (No-U-Turn Sampler), implementado en **PyMC**.

### Configuración del Muestreador

| Parámetro | Valor |
|:---|---|
| Cadenas | 4 |
| Warmup (tuning) | 2,000 iteraciones |
| Muestras por cadena | 4,000 |
| Muestras totales | 16,000 |
| Algoritmo | NUTS |
| Diagnóstico convergencia | R̂ < 1.01 |

---

## 8. Evaluación del Modelo

### 8.1 Chequeos Predictivos Posteriores (PPC)

- Generar $y_{\text{sim}}$ a partir del posterior predictivo
- Comparar distribución de $y_{\text{sim}}$ con $y_{\text{obs}}$
- Verificar que el modelo capture la proporción global de victorias

### 8.2 Intervalos de Densidad (HDI)

Para cada parámetro $\beta_k$, $\alpha_j$, reportar:
- Media posterior
- HDI al 94%
- Probabilidad de dirección (PD): $P(\beta_k > 0 | \text{datos})$

### 8.3 Métricas de Calibración

| Métrica | Propósito |
|:---|---|
| **Brier Score** | Precisión de las probabilidades pronosticadas |
| **Expected Calibration Error (ECE)** | Calibración en segmentos de probabilidad |
| **Log-Loss** | Penalización por exceso de confianza |
| **AUC-ROC** | Capacidad discriminativa |

### 8.4 Comparación de Modelos

| Modelo | Descripción |
|:---|---|
| M0: Nulo | Solo intercepto fijo (sin predictores) |
| M1: Plano | Regresión logística sin jerarquía |
| **M2: Jerárquico** | Regresión logística con interceptos aleatorios por mapa |

Comparación mediante **WAIC** (Watanabe-Akaike Information Criterion) y **LOO-CV** (Leave-One-Out Cross-Validation).

---

## 9. Visualizaciones Planificadas

1. **Forest plot** de coeficientes $\beta_k$ con HDI 94%
2. **Efectos marginales** — curva logística $P(\text{victoria})$ vs cada predictor
3. **Interceptos por mapa** $\alpha_j$ ordenados por ventaja CT/T
4. **PPC plot** — histograma comparativo de $y_{\text{sim}}$ vs $y_{\text{obs}}$
5. **Curva de calibración** — probabilidad predicha vs frecuencia observada
6. **Matriz de correlación posterior** entre parámetros

---

## 10. Implementación Propuesta (PyMC)

El modelo se implementará siguiendo esta estructura conceptual:

```python
import pymc as pm

with pm.Model() as hierarchical_model:
    # Hiperpriors
    mu_alpha = pm.Normal("mu_alpha", 0, 5)
    sigma_alpha = pm.HalfNormal("sigma_alpha", 2)
    
    # Interceptos por mapa
    alpha_map = pm.Normal("alpha_map", mu_alpha, sigma_alpha, shape=n_maps)
    
    # Coeficientes
    betas = pm.Normal("betas", 0, 5, shape=n_predictors)
    
    # Predictor lineal
    logit_p = alpha_map[map_idx] + pm.math.dot(X, betas)
    
    # Likelihood
    y = pm.Bernoulli("y", logit_p=logit_p, observed=y_obs)
    
    # Muestreo
    trace = pm.sample(4000, tune=2000, chains=4, target_accept=0.9)
```

---

## Notas Importantes

1. **Los datos están listos:** `csgo_games.csv` contiene las variables necesarias, aunque no tiene columna de mapa. Se necesita un proceso de merge con `results.csv` o alternativamente modelar usando directamente `results.csv`.

2. **No ejecutar aún:** Este documento es la especificación completa del modelo. La implementación y ejecución se realizarán en la siguiente fase del proyecto.

3. **Referencia:** La especificación sigue la estructura descrita en la Sección 5 (Diseño Metodológico) del paper en `main.tex`.
