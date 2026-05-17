# Resultados Clave del EDA — Proyecto CS:GO Bayesiano Jerárquico

## Resumen del Dataset

| Característica | Valor |
|:---|---:|
| Partidas analizadas | 3,787 |
| Variables por partida | 170 |
| Rango temporal | 2016–2020 |
| Victorias Team 1 | ~48.5% |
| Victorias Team 2 | ~48.5% |
| Empates | ~3% |

---

## 1. Paridad Competitiva

Las distribuciones de **Rating 2.0** se superponen casi completamente entre equipos de alto nivel. La brecha técnica entre ganadores y perdedores es mínima, lo que implica que **el ranking mundial no es un predictor suficiente por sí solo**.

> **Implicación:** Se necesita un enfoque probabilístico (bayesiano) que cuantifique la incertidumbre en lugar de un clasificador determinista.

---

## 2. Ranking de Predictores (Correlación con Victoria)

| Predictor | r con Victoria | Fuerza |
|:---|---:|:---|
| diff_rating | **+0.196** | Fuerte |
| diff_kdr | +0.203 | Fuerte (colineal) |
| diff_dmr (ADR) | +0.190 | Fuerte |
| diff_impact | +0.189 | Fuerte |
| diff_kpr | +0.186 | Moderada |
| diff_rank | −0.190 | Moderada (negativa) |
| diff_h2h | +0.12 | Débil |
| diff_kast | +0.15 | Moderada |

**Hallazgo clave:** Rating, Impacto y ADR tienen correlaciones muy similares (~0.19), lo que sugiere que **capturan dimensiones complementarias del rendimiento**.

---

## 3. Relación Rating → Victoria (Monótona y Lineal en Logit)

El análisis por deciles muestra una relación **monótona creciente** entre el diferencial de Rating y la tasa de victoria:
- Decil inferior (peor rating): ~30% de victorias
- Decil superior (mejor rating): ~85% de victorias

El **empirical logit plot** confirma que la relación es aproximadamente **lineal en el espacio logit**, validando el uso de la función de enlace logit en el modelo.

---

## 4. Impacto Táctico como Factor Diferenciador

Equipos con **Rating similar** pueden tener resultados distintos. El **Impacto** (multikills, opening kills) explica esta divergencia:
- Los ganadores tienen un impacto **más consistente** (distribución más concentrada)
- Los perdedores tienen un impacto **más disperso** (mayor varianza)

> **Interpretación:** No basta con "disparar bien" (Rating); hay que "aparecer en los momentos clave" (Impacto).

---

## 5. Asimetría Táctica por Mapa (Justificación Jerárquica)

| Mapa | % Rondas CT | Ventaja CT | Partidas |
|:---|---:|---:|---:|
| Nuke | 56.8% | +6.8% | ~4,200 |
| Vertigo | 55.2% | +5.2% | ~2,800 |
| Overpass | 53.5% | +3.5% | ~5,100 |
| Inferno | 52.1% | +2.1% | ~6,500 |
| Dust2 | 51.5% | +1.5% | ~7,800 |
| Mirage | 50.8% | +0.8% | ~6,200 |
| Train | 49.5% | −0.5% | ~3,400 |

> **Conclusión:** La variabilidad del balance CT/T entre mapas (rango: 49.5%–56.8%) justifica **interceptos aleatorios por mapa** en el modelo jerárquico.

---

## 6. Multicolinealidad (VIF)

| Variable | VIF | Decisión |
|:---|---:|:---|
| diff_rating | 3.2 | ✅ Incluir |
| diff_impact | 2.8 | ✅ Incluir |
| diff_dmr (ADR) | 4.1 | ✅ Incluir |
| diff_kast | 3.5 | ✅ Incluir |
| diff_kdr | **8.7** | ❌ Excluir (colineal con rating) |
| diff_rank | 1.5 | ⚠️ Opcional |

---

## 7. Predictores Seleccionados para el Modelo

| Predictor | Justificación |
|:---|---|
| `diff_rating` | Métrica integral de rendimiento (mayor correlación) |
| `diff_impact` | Captura momentos críticos, factor diferenciador |
| `diff_dmr` (ADR) | Daño infligido por ronda, complementa al rating |
| `diff_kast` | Contribución consistente (baja/asistencia/supervivencia) |

---

## 8. Evolución Temporal

Las métricas de rendimiento se han mantenido **relativamente estables** entre 2016 y 2020, con ligeras variaciones anuales. Esto sugiere que el modelo es **generalizable** a través del tiempo y no depende de una temporada específica.

---

## 9. Decisión de Modelado (derivada del EDA)

| Aspecto | Decisión |
|:---|---|
| Tipo de modelo | Regresión Logística Bayesiana Jerárquica |
| Likelihood | Bernoulli (yᵢ ~ Bernoulli(pᵢ)) |
| Función de enlace | Logit |
| Predictores | diff_rating, diff_impact, diff_dmr, diff_kast |
| Estructura jerárquica | Intercepto aleatorio por mapa (α_mapⱼ) |
| Priors para β | Normal(0, 5²) — débilmente informativas |
| Hiperprior σ_α | HalfNormal(2) |
| Evaluación | PPC, HDI 94%, Brier Score, ECE, Log-Loss |
