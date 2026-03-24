# Entregable 3: Diagnóstico de Viabilidad Empírica

Este directorio contiene los archivos correspondientes al **Taller 03** del proyecto de Pensamiento Crítico. El objetivo de esta fase es evaluar la factibilidad técnica y empírica del modelo bayesiano para la predicción de resultados en CS:GO.

## Contenido del Entregable
1.  **[Taller3_Diagnostico_Viabilidad.tex](./Taller3_Diagnostico_Viabilidad.tex):** Documento fuente en LaTeX con la matriz de viabilidad y el diagnóstico crítico.
2.  **[pensamiento 3.png](./pensamiento%203.png):** Imagen de referencia con las instrucciones originales del taller.

## Resumen del Diagnóstico
*   **Fuente de Datos Identificada:** Datasets profesionales de HLTV (Kaggle), que incluyen estadísticas de los últimos 3 meses, rankings históricos y resultados de mapas.
*   **Variable Dependiente:** `match_winner` (Resultado binario de la partida).
*   **Decisión Metodológica:** Se mantiene el uso de **Inferencia Bayesiana** debido a su superioridad en la cuantificación de incertidumbre pre-match.
*   **Ajuste de Alcance:** El proyecto se enfocará exclusivamente en encuentros de **Tier 1 (Top 30 equipos)** para garantizar la consistencia y calidad de los datos empíricos.

## Instrucciones para Overleaf
Para visualizar este entregable en Overleaf:
1. Sube el archivo `.tex` a tu proyecto de Overleaf.
2. Asegúrate de tener configurado el compilador en **pdfLaTeX** o **LuaLaTeX**.
3. El documento está configurado para usar `babel` en español.
