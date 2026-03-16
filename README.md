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
Todos los integrantes del equipo deben configurar su entorno para obtener los datasets. Este proceso **debe hacerlo cada persona individualmente** una única vez para tener acceso a las fuentes de datos pesadas (Kaggle).

#### 1. Instalación de dependencias y Entorno Virtual
Para evitar conflictos con el sistema, crea un entorno virtual antes de instalar:
```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno
# En Linux/Mac:
source venv/bin/activate
# En Windows:
.\venv\Scripts\activate

# Instalar las librerías
pip install -r requirements.txt
```

#### 2. Configuración de la API de Kaggle (Paso a Paso)
Para descargar los datasets maestros que usaremos en el modelo:
1. **Crear cuenta:** Regístrate en [Kaggle.com](https://www.kaggle.com) si aún no tienes cuenta.
2. **Generar Token:** Ve a tu perfil (arriba a la derecha) -> **Settings**. Desliza hasta la sección **API** y haz clic en **Create New API Token**. Se descargará un archivo llamado `kaggle.json`.
3. **Ubicar el Token:**
   - **Linux/Mac:** Crea una carpeta oculta llamada `.kaggle` en tu home y mueve el archivo allí:
     ```bash
     mkdir -p ~/.kaggle
     mv ~/Downloads/kaggle.json ~/.kaggle/
     chmod 600 ~/.kaggle/kaggle.json
     ```
   - **Windows:** Mueve el archivo a `C:\Users\<TuUsuario>\.kaggle\kaggle.json`.
4. **Ejecutar Captura:** Una vez configurado el token, corre el script:
   ```bash
   python3 src/data/capture_data.py
   ```

**¿Qué hace este script?**
1. Crea automáticamente la carpeta `data/raw/` si no existe.
2. Descarga los datasets configurados (ej. `csgo_match_results.csv`) desde GitHub y, próximamente, los de Kaggle usando la API.
3. Genera un archivo `data_version.txt` para asegurar que todos estemos trabajando con la misma versión de los datos.

---

## 📂 Inventario de Bases de Datos Identificadas

Tras una búsqueda exhaustiva, hemos seleccionado las siguientes fuentes principales para alimentar nuestro modelo bayesiano:

1. **CS:GO Match Results (2019-2022) [GitHub/hojlund123]:** Dataset principal con resultados de mapas y series (CSV directo).
2. **Professional Matches Complete [Kaggle]:** Contiene `economy.csv`, `picks.csv` y `players.csv`. Fundamental para variables tácticas.
3. **CS2 Statistics (2024-2025) [Kaggle]:** Datos actualizados para CS2.
4. **HLTV Betting & Odds:** Datos históricos de cuotas para utilizarlos como *priors* bayesianos.

---

## 🚀 Progreso del Proyecto y Registro de Cambios

Hasta el momento, se han completado los siguientes hitos:

1. **Inicialización del Repositorio:** Creación y vinculación del repositorio local con GitHub.
2. **Setup de Estructura de Data Science:** Se crearon los subdirectorios estándar de trabajo (`data. raw/processed`, `notebooks`, `src`, `models`, `reports/figures`).
3. **Configuración Inicial:** Intercambio de ignorar archivos pesados e irrelevantes vía `.gitignore` y un contenedor para dependencias en `requirements.txt`.
4. **Propuesta Técnica Finalizada:** Documento `entrega.tex` de 6 páginas con metodología bayesiana y revisión de literatura.
5. **Sistema de Captura de Datos:** Implementación de `src/data/capture_data.py` y configuración de descarga automatizada.
6. **Manejo de Ramas:** Flujo de trabajo con PRs (`First_advance`, `entregable-1`, etc.) garantizando la sincronización del equipo.
