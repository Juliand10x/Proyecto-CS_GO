# 🎮 Proyecto CS:GO - Predicción Bayesiana de Victorias

Este repositorio contiene el desarrollo del modelo probabilístico para estimar la probabilidad de victoria en partidas profesionales de Counter-Strike: Global Offensive.

---

## 📄 Propuesta Resumida del Proyecto

**Tema:** Estimación bayesiana de la probabilidad de victoria en partidas profesionales de Counter-Strike: Global Offensive antes del inicio del encuentro.

**Pregunta de investigación:** ¿Cómo puede estimarse la probabilidad posterior de victoria de un equipo profesional de CS:GO mediante un modelo de regresión logística bayesiana que incorpore rendimiento reciente, ranking relativo y desempeño histórico por mapa?

---

## 👥 Público Objetivo

El modelo está diseñado para aportar valor a:
1. **Equipos profesionales:** Para tomar decisiones estratégicas fundamentadas en datos medibles.
2. **Casas de apuestas:** Para estimar y ajustar cuotas de manera cuantitativa considerando la incertidumbre real.
3. **Plataformas de análisis:** Para robustecer sus dashboards con métricas probabilísticas.
4. **Inversionistas en esports:** Para evaluar el riesgo competitivo y la consistencia de los equipos.
5. **Investigadores:** Como aplicación formal de inferencia bayesiana en entornos deportivos.

---

## 📊 Salidas del Modelo

El modelo entrega más que una predicción binaria (gana/pierde):
- Probabilidad estimada de victoria (ej. 63%).
- Intervalo de incertidumbre (HDi/Credible Interval).
- Impacto probabilístico (pesos) de cada variable (Ranking, Mapa, Forma reciente).
- Simulación de escenarios (Ej: ¿Qué ocurre si cambiamos de mapa o si la forma del equipo mejora?).

---

## 🧠 Valor Diferencial del Proyecto

El valor principal no recae en ser "el modelo más preciso empíricamente" (accuracy), sino en la **interpretabilidad**, la **cuantificación explícita de incertidumbre** y su capacidad de ser actualizado con nueva evidencia. Su transparencia lo hace una herramienta robusta de apoyo en decisiones estratégicas bajo incertidumbre.

---

---

## 🛠️ Guía de Uso del Sistema de Datos

Para mantener el repositorio liviano y evitar subir archivos CSV pesados, hemos implementado un sistema de captura automatizada.

### ¿Cómo descargar los datos?
Todos los integrantes del equipo pueden obtener los mismos datos ejecutando el siguiente comando desde la raíz del proyecto:

```bash
python src/data/capture_data.py
```

**¿Qué hace este script?**
1. Crea automáticamente la carpeta `data/raw/` si no existe.
2. Descarga los datasets configurados (ej. `csgo_match_results.csv`) directamente desde fuentes públicas.
3. Genera un archivo `data_version.txt` para asegurar que todos estemos trabajando con la misma versión de los datos.

---

## 📂 Inventario de Bases de Datos Identificadas

Tras una búsqueda exhaustiva, hemos seleccionado las siguientes fuentes principales para alimentar nuestro modelo bayesiano:

1. **CS:GO Match Results (2019-2022) [GitHub/hojlund123]:** Dataset principal con resultados de mapas y series. (Ya integrado en el script).
2. **Professional Matches Complete [Kaggle/Gabriel Tardochi]:** Dataset exhaustivo con `economy.csv`, `picks.csv` (vetos de mapas) y `players.csv`. Ideal para el análisis de especialización por mapa.
3. **HLTV Statistics (2024-2025) [Kaggle/Mateus Machado]:** Datos recientes de CS2 para asegurar que el modelo sea válido en la versión actual del juego.
4. **PandasScore API:** Fuente secundaria para obtener datos en tiempo real de torneos en curso (requiere API Key).

---

## 🚀 Progreso del Proyecto y Registro de Cambios

Hasta el momento, se han completado los siguientes hitos:

1. **Inicialización del Repositorio:** Creación y vinculación del repositorio local con GitHub.
2. **Setup de Estructura de Data Science:** Se crearon los subdirectorios estándar de trabajo (`data. raw/processed`, `notebooks`, `src`, `models`, `reports/figures`).
3. **Configuración Inicial:** Intercambio de ignorar archivos pesados e irrelevantes vía `.gitignore` y un contenedor para dependencias en `requirements.txt`.
4. **Propuesta Técnica Finalizada:** Documento `entrega.tex` de 6 páginas con metodología bayesiana y revisión de literatura.
5. **Sistema de Captura de Datos:** Implementación de `src/data/capture_data.py` y configuración de descarga automatizada.
6. **Manejo de Ramas:** Flujo de trabajo con PRs (`First_advance`, `entregable-1`, etc.) garantizando la sincronización del equipo.
