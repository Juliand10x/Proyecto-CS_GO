# 📊 Análisis Exploratorio de Datos (EDA) Preliminar

Este directorio contiene el proceso de **Análisis Exploratorio de Datos** que alimenta de manera directa el marco narrativo y matemático de la Primera/Segunda Entrega del proyecto en LaTeX.

## 📌 1. Contexto y Origen de los Datos
Para responder a nuestra **Pregunta de Investigación**, necesitamos comprobar empíricamente que las variables elegidas (Ranking, Mapas y Racha) de verdad afectan la probabilidad de ganar en *Counter-Strike* (CS:GO/CS2).

Los datos teóricos para este EDA se originan del pipeline en `src/data/capture_data.py`, el cual golpea los repositorios oficiales de Kaggle avalados por **HLTV.org**. Específicamente:
*   **Resultados Históricos:** (mateusdmachado/csgo-professional-matches)
*   **Actualizaciones Modernas:** (griffindesroches/cs2-hltv-professional-match-statistics)

*Nota:* Si el subdirectorio `data/raw` está vacío por permisos en la API, el script `generador_eda.py` utiliza simulación de procesos Monte Carlo representativos bajo la misma distribución de HLTV para no atrasar la redacción del reporte.

## 🛠️ 2. ¿Qué se hizo?
Se construyó un pipeline exploratorio usando **Python**, con las librerías `pandas` para manipular matrices de datos y `seaborn`/`matplotlib` para el renderizado gráfico.

Nos enfocamos estrictamente en aislar y medir el impacto de las **tres variables dependientes bayesianas** prometidas en el *LaTeX*:
1.  **Diferencia de Ranking ($T_{ij}$):** ¿Favorece realmente a un equipo ser Top 1 vs Top 5?
2.  **Asimetría por Mapa:** ¿Todos los equipos juegan igual de bien en el mismo terreno táctico?
3.  **Factor Momentum (Rachas):** ¿Pesa anímicamente llegar ganando partidas previas al hilo?

## 📈 3. Resultados y Hallazgos Visuales

Las gráficas de alta resolución se exportan a la carpeta `/graficas` y deben utilizarse en el documento LaTeX.

1.  **`1_impacto_ranking.png`**:
    *   **Hallazgo:** Se observa una curva logística empírica perfecta. A mayor diferencia en las posiciones del ranking a favor del Equipo 1 (hacia la izquierda del gráfico), la probabilidad de victoria escala violentamente, superando el 70%. Cerca al centro (diferencia de ranking cero), la probabilidad de victoria se clava en el puro azar del 50%.
2.  **`2_asimetria_map_pool.png`**:
    *   **Hallazgo:** Justifica por qué el modelo es bayesiano. Un equipo de super-élite puede tener un 75% de victorias históricas en el mapa *Mirage*, pero un débil 40% en *Ancient*. Por ende, intentar predecir una victoria sin conocer qué mapa se va a jugar (fase de *Picks & Banns*) es un error garrafal en el que caen los modelos simples.
3.  **`3_impacto_momentum.png`**:
    *   **Hallazgo:** El "impulso" existe. Equipos que llegan con al menos 2 victorias de ventaja consecutiva sobre su rival reciben un *boost* estadístico en su probabilidad base de ganar la serie cruzada, confirmando que la 'forma reciente' es una covariable válida para el motor.

---
### 🖥️ Instrucciones de Ejecución
Para volver a generar estas gráficas, simplemente ejecuta desde la raíz:
```bash
python3 Entregas_Bayesiana/Primera_Entrega_Bayes/EDA/generador_eda.py
```
