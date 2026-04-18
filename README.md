# 🎮 Proyecto CS:GO - Predicción Bayesiana de Victorias

Este repositorio contiene el desarrollo del modelo probabilístico para estimar la probabilidad de victoria en partidas profesionales de Counter-Strike: Global Offensive.

---

## 📄 Propuesta Resumida del Proyecto

**Tema:** Estimación bayesiana de la probabilidad de victoria en partidas profesionales de Counter-Strike: Global Offensive antes del inicio del encuentro.

**Pregunta de investigación:** ¿De qué manera influyen la destreza técnica de los equipos y las ventajas tácticas del mapa en la probabilidad de victoria en CS:GO, y cómo podemos medir qué tan seguros estamos de estos pronósticos ante la naturaleza impredecible del juego?

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

---

## 🛠️ Guía de Inicio Rápido (Entorno y Datos)

Para mantener el repositorio liviano, **no subimos archivos CSV pesados**. Cada integrante debe configurar su entorno local siguiendo estos pasos:

### 1. Preparar el Entorno Virtual (venv)
Es obligatorio usar un entorno virtual para evitar conflictos con las librerías del sistema:
```bash
# Crear el entorno virtual
python3 -m venv venv

# ACTIVAR (Hacer esto siempre antes de trabajar)
source venv/bin/activate  # En Linux/Mac
# .\venv\Scripts\activate  # En Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar la API de Kaggle (Paso a Paso)
El script descarga automáticamente datasets de varios GB desde Kaggle. Para esto necesitas una "llave":
1. **Bajar la llave:** Ve a [Kaggle Settings](https://www.kaggle.com/settings) -> Sección **API** -> Botón **Create New API Token**. Se bajará un archivo `kaggle.json`.
2. **Ubicar la llave:**
   - **Linux/Mac:** `mkdir -p ~/.kaggle && mv ~/Downloads/kaggle.json ~/.kaggle/`
   - **Windows:** Mover a `C:\Users\<Usuario>\.kaggle\kaggle.json`
3. **SEGURIDAD (Vital):** En Linux ejecuta `chmod 600 ~/.kaggle/kaggle.json`. Si no lo haces, la API dará error.
4. **ACEPTAR REGLAS:** Ve a estos links y dale al botón **Download** una vez para aceptar términos (si no lo haces dará error 403):
   - [Dataset Histórico (MateusD)](https://www.kaggle.com/datasets/mateusdmachado/csgo-professional-matches)
   - [Dataset CS2 (Griffin)](https://www.kaggle.com/datasets/griffindesroches/cs2-hltv-professional-match-statistics-dataset)

### 3. Descargar los Datos
Con el entorno activo (`source venv/bin/activate`), ejecuta:
```bash
python3 src/data/capture_data.py
```

---

## 📂 Estructura de Datos Generada
Tras correr el script, tu carpeta `data/raw/` contendrá:
- `results.csv`: Resultados históricos por mapa.
- `picks.csv`: Datos de vetos y selecciones de mapas (Crucial para el modelo).
- `economy.csv`: Valor de equipo por cada ronda jugada.
- `players.csv`: Rendimiento individual de cada jugador.
- `cs2_newestcombinedmatches.csv`: Datos actualizados a la versión **CS2 (2024-2025)**.

---

## 🚀 Progreso del Proyecto y Registro de Cambios

1. **Propuesta Técnica Finalizada:** Documento `entrega.tex` de 6 páginas con metodología bayesiana (MCMC/NUTS) y revisión de literatura.
2. **Sistema de Captura Robusto:** Integración de `kagglehub` y `requests` para descarga automática y control de versiones.
3. **Manejo de Ramas:** Estructura organizada por ramas (`First_advance`, `data_download`) y flujo de Pull Requests.
4. **Entorno Estandarizado:** Uso de `venv` y `requirements.txt` para asegurar que todo el equipo trabaje con las mismas versiones.
