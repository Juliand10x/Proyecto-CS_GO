# Proceso de Desarrollo - Entregable 4

## Objetivo
Desarrollar un modelo de Regresión Logística Bayesiana para predecir el ganador de encuentros de CS:GO basándonos en datos históricos, selecciones de mapas y estadísticas de jugadores.

## Estado de los Datasets
Se han analizado 5 fuentes principales de datos en `data/raw/`:
1.  **`results.csv`**: Resultados históricos de partidas.
2.  **`picks.csv`**: Fase de vetos y elección de mapas.
3.  **`players.csv`**: Rendimiento individual por mapa.
4.  **`economy.csv`**: Datos económicos por ronda.
5.  **`cs2_newestcombinedmatches.csv`**: Un dataset pre-procesado con características de CS2.

## Acciones Recientes
- **Análisis de Datasets:** Se identificaron las variables clave para el modelado bayesiano.
- **Estructuración:** Creación del directorio `entregable_4` para centralizar el desarrollo del hito actual.

## 2. Análisis Exploratorio de Datos (EDA)
Se realizó un análisis de los datasets principales para identificar las variables más influyentes en la predicción de victorias.

### Hallazgos Clave:
- **resultados.csv**: El Team 1 tiene una ligera ventaja histórica (53.75% de win rate), lo cual debe ser considerado en el modelo Bayesiano para evitar sesgos.
- **picks.csv**: Los mapas más jugados son **Mirage** e **Inferno**. Esto sugiere que el rendimiento en estos mapas tendrá mas peso estadístico debido a la mayor disponibilidad de datos.
- **cs2_newestcombinedmatches.csv**: Las variables con mayor correlación con la victoria son:
  - `rating_diff` (0.2617): Confirmando que la diferencia de habilidad es el predictor primario.
  - `kpr_diff` (0.2247): La diferencia en bajas por ronda es un indicador fuerte de dominancia.
  - `adr_diff` (0.2087): El daño promedio por ronda también muestra una correlación significativa.

## 3. Próximos Pasos
- [ ] Implementar el modelo de Regresión Logística Bayesiana utilizando `PyMC`.
- [ ] Definir priors basados en el `rating_diff` histórico.
- [ ] Integrar el contexto del mapa como una variable categórica.
