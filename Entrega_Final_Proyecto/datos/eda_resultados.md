# Informe de Análisis Exploratorio de Datos (EDA)

Este documento detalla el proceso, la justificación y los hallazgos del análisis exploratorio realizado sobre la base de datos de encuentros profesionales de CS:GO.

## 1. Análisis de Paridad y Distribución
**¿Por qué se hizo?**
Para verificar si el nivel de los equipos profesionales es lo suficientemente cercano como para justificar el uso de modelos probabilísticos avanzados en lugar de simples rankings.

**Resultados:**
* Se observó una superposición extrema en las distribuciones de `Rating` de los equipos top.
* La brecha técnica es mínima, lo que implica que el ranking mundial no es un predictor suficiente por sí solo.
* Esto justifica la necesidad de cuantificar la **incertidumbre**, ya que los encuentros se deciden por márgenes muy pequeños.

## 2. Relación Desempeño vs. Éxito (Rating vs. Winrate)
**¿Por qué se hizo?**
Para validar que las métricas de desempeño individual capturadas realmente se traducen en victorias de equipo.

**Resultados:**
* Existe una correlación positiva clara: incluso mejoras marginales en el Rating promedio del equipo aumentan significativamente la probabilidad de ganar el mapa.
* El Rating es una de las variables clave que permite iniciar la discriminación entre ganadores y perdedores.

## 3. Identificación de las Variables más Influyentes: El Impacto
**¿Por qué se hizo?**
Buscábamos las variables que explicaran por qué equipos con Rating similar obtienen resultados distintos.

**Resultados:**
* El **Impacto Táctico** mostró ser más consistente en los equipos ganadores.
* Mientras el Rating mide "qué tan bien disparas", el Impacto mide "qué tanto importan tus bajas". Los ganadores no solo matan más, sino que matan en momentos críticos (multikills, bajas de apertura).

## 4. Análisis de Estructura Jerárquica (Mapas)
**¿Por qué se hizo?**
Para entender si el contexto del mapa (lado CT vs. lado T) altera la dinámica de las variables.

**Resultados:**
* Se confirmaron asimetrías tácticas: algunos mapas favorecen históricamente al bando defensivo (CT), lo que altera el balance de las partidas.
* Esto llevó a la decisión de usar una **estructura jerárquica** en el modelo bayesiano para que el "conocimiento" del modelo se ajuste según el mapa jugado.

## 5. Matriz de Correlación
**Resultados Clave:**
* La sinergia más fuerte se encuentra entre el **Impacto Táctico** y el **Daño Promedio (ADR)**.
* Estas dos variables, combinadas con el Rating, forman el núcleo predictivo del modelo desarrollado.
