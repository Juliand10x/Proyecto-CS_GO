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
