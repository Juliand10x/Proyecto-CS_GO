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

## 🚀 Progreso del Proyecto y Registro de Cambios

Hasta el momento, se han completado los siguientes hitos:

1. **Inicialización del Repositorio:** Creación y vinculación del repositorio local con GitHub.
2. **Setup de Estructura de Data Science:** Se crearon los subdirectorios estándar de trabajo (`data. raw/processed`, `notebooks`, `src`, `models`, `reports/figures`).
3. **Configuración Inicial:** Intercambio de ignorar archivos pesados e irrelevantes vía `.gitignore` y un contenedor para dependencias en `requirements.txt`.
4. **Pull Request de Configuración:** Rama `feature/setup-structure` con PR directo a `main`.
5. **Preparación Taller 2:** Se creó y activó la rama `entregable-taller-2` destinada al entregable académico.
6. **Migración de Recursos:** Adición del caso de estudio/contexto base `S2_Pensamiento_Critico.pdf` dentro del repositorio de trabajo.
7. **Revisión de Literatura (Taller 2):** Creación del código fuente LaTeX y estructura para el entregable del Taller 2 sobre revisión crítica de literatura, alojados en el directorio `entregable_2/`.
