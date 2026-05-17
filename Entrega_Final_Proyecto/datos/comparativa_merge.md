# Comparativa: Merge Case-Sensitive vs Case-Insensitive

## El Problema

El dataset `csgo_games.csv` tiene los nombres de equipo en **MAYÚSCULAS** (`'ASTRALIS'`, `'CLOUD9'`, `'FAZE'`), mientras que `results.csv` los tiene **capitalizados** (`'Astralis'`, `'Cloud9'`, `'FaZe'`). El merge original usando `on=['team_1', 'team_2']` no encontraba coincidencias por esta diferencia de capitalización, obteniendo solo **218 observaciones**.

## La Solución

Normalizar ambos datasets a mayúsculas (`str.upper().str.strip()`) antes de hacer el merge. El merge case-insensitive encontró que **todos los 69 equipos de csgo_games tienen contraparte en results**, elevando las observaciones a **5,745**.

## Tabla Comparativa

| Métrica | Antes (case-sensitive) | Ahora (case-insensitive) | Cambio |
|:---|---:|---:|:---|
| **Observaciones** | 218 | **5,745** | **26× más** |
| **Partidas únicas** | ~119 | **3,341** | 28× |
| **Mapas** | 9 | 10 (incluye Default) | +1 |
| **Balance target** | ~50/50 | ~50.6/49.4 | Sin cambio |

### Coeficientes Posteriores (β)

| Predictor | Antes (Media, HDI 94%) | Ahora (Media, HDI 94%) | Efecto |
|:---|---:|---:|:---|
| **diff_rating** | 2.32 [-4.56, 9.46] | **4.95 [2.87, 7.08]** | ✅ HDI > 0 |
| **diff_impact** | 1.98 [-5.41, 9.32] | **0.36 [-1.72, 2.55]** | HDI cruza 0 |
| **diff_dmr (ADR)** | −0.05 [-0.30, 0.20] | **0.095 [0.04, 0.15]** | ✅ HDI > 0 |
| **diff_kast** | 3.27 [-4.70, 10.96] | **−5.47 [-8.29, −2.80]** | ⚠️ HDI < 0 |

### Métricas de Evaluación

| Métrica | Antes | Ahora | Interpretación |
|:---|---:|---:|:---|
| **Brier Score** | 0.2384 | 0.2404 | Similar (~24% error) |
| **Mejora vs nulo** | 4.6% | 3.8% | Ligeramente menor |
| **AUC-ROC** | 0.6335 | 0.6117 | Moderado |
| **Log-Loss** | 0.6696 | 0.6737 | Similar |
| **Δelpd (vs nulo)** | −0.57 ❌ | **+101.61** ✅ | **Jerárquico sólidamente superior** |

### Diagnóstico de Convergencia

| Métrica | Antes | Ahora |
|:---|---:|---:|
| **R-hat (todos)** | ~1.0 | **1.000–1.001** |
| **ESS bulk** | 2,500–8,800 | **10,500–20,000** |
| **ESS tail** | 5,900–12,900 | **10,500–20,000** |

### Interceptos por Mapa (α_j)

| Mapa | Antes (Media, Prob Base) | Ahora (Media, Prob Base) |
|:---|---:|---:|
| Mirage | — | 0.146 (p=0.536) ✅ HDI > 0 |
| Train | — | 0.079 (p=0.520) |
| Cache | — | 0.028 (p=0.507) |
| Dust2 | — | 0.001 (p=0.500) |
| Vertigo | — | 0.001 (p=0.500) |
| Nuke | — | −0.020 (p=0.495) |
| Cobblestone | — | −0.032 (p=0.492) |
| Inferno | — | −0.050 (p=0.488) |
| **Overpass** | — | **−0.160 (p=0.460) ✅ HDI < 0** |

## Conclusiones

1. **Rating 2.0** es el predictor dominante (β=4.95, HDI [2.87, 7.08]).
2. **ADR** ahora muestra efecto positivo significativo que se perdía con pocos datos.
3. **KAST** muestra efecto negativo (posible colinealidad inversa: equipos con más KAST tienen menor rating/impacto).
4. La **estructura jerárquica** está sólidamente justificada: Δelpd=+101.6 vs modelo nulo.
5. **Mirage** favorece más al equipo marcado como T1; **Overpass** lo desfavorece.
