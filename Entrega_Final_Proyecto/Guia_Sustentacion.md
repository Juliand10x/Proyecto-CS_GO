# 🏆 Guía de Sustentación Cronometrada (7 Minutos) y Defensa Técnica

Esta guía está estructurada **siguiendo exactamente el "Esquema General del Trabajo" de tu proyecto**. Está organizada en diapositivas muy cortas de **Apoyo Visual** (indicándote qué mostrar en pantalla), acompañadas de tu **Guión Verbal exacto cronometrado** y, de manera clave, las **Preguntas Técnicas y Respuestas** correspondientes a cada fase integradas directamente en su sección.

---

## 🖥️ Libreto de Exposición e Integración Técnica

---

### **Diapositiva 1: Selección del Problema e Introducción [Minuto 0:00 - 0:45]**

*   **Apoyo Visual Recomendado:** 
    *   Un slide muy limpio y premium en modo oscuro.
    *   El título del proyecto en tipografía grande y elegante.
    *   Una imagen sutil de un servidor de CS:GO en alta tensión (marcador 14-14).
*   **Guión Verbal (Qué decir):**
    > *"Buenos días, profesor y miembros del jurado. Imaginen que están viendo la Gran Final de un mundial de Counter-Strike. El marcador está empatado 14-14. El jugador estrella de un equipo elimina a tres oponentes de manera espectacular, lo que parece asegurar el mapa. Sin embargo, segundos después, el rival desactiva la bomba y se lleva la victoria.*
    >
    > *Esta paradoja motivó nuestro proyecto: ¿Por qué el brillo individual no garantiza el triunfo colectivo? ¿Cuánto influye el mapa táctico en el que se juega? Y sobre todo, ante la extrema paridad y volatilidad de la escena profesional, ¿cómo podemos estimar la probabilidad de éxito reconociendo con honestidad la incertidumbre? Hoy les presentaremos un modelo bayesiano jerárquico que resuelve esto con total honestidad estadística."*

---

### **Diapositiva 2: Búsqueda de Datos, Propuesta y Análisis Bibliográfico [Minuto 0:45 - 1:30]**

*   **Apoyo Visual Recomendado:** 
    *   Logotipo de **HLTV.org** y logos de las investigaciones de referencia (Makarov, Hodge, Gelman).
    *   Dos columnas sencillas: **Enfoque Clásico** (Modelos deterministas de Machine Learning que venden falsas certezas) vs. **Enfoque Propuesto** (Estadística Bayesiana + Estructura Jerárquica).
*   **Guión Verbal (Qué decir):**
    > *"El Counter-Strike profesional es una industria millonaria donde los equipos juegan a un nivel casi idéntico. Al revisar la literatura previa, identificamos que la mayoría de los modelos predictivos tradicionales son deterministas y opacos: arrojan probabilidades rígidas ignorando el azar intrínseco de cada ronda.*
    >
    > *Para llenar este vacío, planteamos una propuesta basada en dos pilares bibliográficos y metodológicos: primero, la **Estadística Bayesiana** para modelar y cuantificar transparentemente la incertidumbre en los parámetros; y segundo, un **Modelo Jerárquico** para agrupar los datos según su contexto físico y táctico: el mapa disputado."*

---

### **Diapositiva 3: Análisis de Datos Secundarios, EDA y Problemas con los Datos [Minuto 1:30 - 2:30]**

*   **Apoyo Visual Recomendado:** 
    *   Un gráfico simple que muestre la superposición extrema de rendimiento entre ganadores y perdedores (EDA).
    *   Un esquema visual del hito de ingeniería: **Cruce Estricto Inicial ($N = 218$) $\rightarrow$ Limpieza Case-insensitive y Ventana de 3 Días $\rightarrow$ Muestra Final ($N = 5,745$ mapas, 3,341 partidas)**.
*   **Guión Verbal (Qué decir):**
    > *"Nuestros datos secundarios provienen de HLTV entre 2016 y 2020. Al intentar unir las tablas de rendimiento individual de los jugadores con los resultados generales de las partidas, enfrentamos un problema de calidad crítico: los nombres de los equipos diferían en mayúsculas y minúsculas. Un cruce estricto reducía la muestra útil a apenas 218 mapas, comprometiendo la estabilidad estadística.*
    >
    > *Diseñamos un proceso de limpieza para normalizar el texto a mayúsculas combinado con una ventana de coincidencia temporal de 3 días. Gracias a esto, nuestra muestra útil creció 26 veces hasta consolidar **5,745 observaciones de mapas**. *
    >
    > *Durante el EDA, detectamos una colinealidad del 97% entre el ratio de bajas/muertes (KDR) y el Rating 2.0. Con rigor metodológico, decidimos excluir el KDR para evitar redundancia e inestabilidad en los cálculos, preservando el Rating 2.0 como métrica reina."*

#### **💬 Posible Pregunta Técnica de esta sección:**
*   **Pregunta del Profesor:** *¿Cómo afectó el problema de inconsistencia de nombres en la representatividad y el sesgo de la muestra?*
*   **Respuesta de Defensa:** 
    > *"Profesor, de habernos quedado con la muestra inicial de 218 observaciones generada por el cruce estricto, habríamos sufrido de un severo sesgo de selección, limitando el análisis únicamente a los pocos equipos cuyos nombres coincidían perfectamente por azar en ambas tablas. Al aplicar la normalización de texto y la ventana de 3 días, garantizamos que la muestra definitiva de 5,745 mapas sea representativa de todo el circuito competitivo de élite internacional, eliminando el sesgo y aumentando drásticamente la robustez de las estimaciones."*

---

### **Diapositiva 4: Búsqueda de Expertos y Definición de las Priors [Minuto 2:30 - 3:15]**

*   **Apoyo Visual Recomendado:**
    *   Ecuaciones de los priors en LaTeX limpio: $\beta_k \sim \text{Normal}(0, 5^2)$, $\mu_\alpha \sim \text{Normal}(0, 5^2)$, $\sigma_\alpha \sim \text{HalfNormal}(2)$.
    *   Nota conceptual: *"Los expertos definen el problema y el rango de los priors, pero la verosimilitud de la gran muestra domina la estimación final sin sesgar la verosimilitud (Likelihood)."*
*   **Guión Verbal (Qué decir):**
    > *"En la estadística bayesiana, la definición de las distribuciones previas o priors es crucial. Consultando la teoría y la opinión de expertos del juego, seleccionamos las cuatro variables de desempeño explicativas fundamentales (Rating, Daño, Impacto y KAST).*
    >
    > *Para no imponer sesgos subjetivos en las estimaciones, definimos priors de filosofía débilmente informativa: distribuciones normales centradas en cero con desviación estándar de 5 para los coeficientes de desempeño y para la media global de los mapas, y una distribución Half-Normal para la desviación estándar entre escenarios. Esto actúa como un regularizador matemático que estabiliza el modelo, pero permite que la enorme masa de datos del servidor domine la estimación de la posterior."*

#### **💬 Posible Pregunta Técnica de esta sección:**
*   **Pregunta del Profesor:** *¿Por qué priors normales débilmente informativas ($Normal(0, 5^2)$) en lugar de priors planas o uniformes no informativas?*
*   **Respuesta de Defensa:**
    > *"Profesor, los priors planos (como los uniformes de $-\infty$ a $+\infty$) son computacionalmente peligrosos en los modelos jerárquicos bayesianos. Permiten al algoritmo MCMC explorar regiones del espacio de parámetros con densidad de probabilidad absurda, lo que produce fallos de muestreo conocidos como transiciones divergentes.*
    >
    > *Un prior débilmente informativo como el $Normal(0, 25)$ actúa como un regulador suave: asume que es sumamente improbable encontrar un efecto de desempeño gigantesco en la escala logit. Dado que nuestra muestra definitiva cuenta con 5,745 mapas, la verosimilitud de los datos domina por completo el posterior, pero el prior estabiliza el sampler MCMC, asegurando la convergencia computacional."*

---

### **Diapositiva 5: Definición de la Likelihood e Imposibilidad de la Posterior [Minuto 3:15 - 4:15]**

*   **Apoyo Visual Recomendado:**
    *   Fórmula del modelo jerárquico en LaTeX:
        *   Likelihood: $y_i \sim \text{Bernoulli}(p_i)$
        *   Logit Link: $\text{logit}(p_i) = \alpha_{map[i]} + \sum \beta_k X_{ki}$
        *   Jerarquía (Mapas): $\alpha_j \sim \text{Normal}(\mu_\alpha, \sigma_\alpha^2)$
    *   Texto destacado: *"La no-conjugación matemática por la función logística rompe la solución analítica, obligando a aproximar la posterior."*
*   **Guión Verbal (Qué decir):**
    > *"Modelamos la verosimilitud de la victoria mediante una distribución de Bernoulli conectada a través de una función de enlace logit inversa, que curva la combinación lineal de los predictores en una 'S', limitando las probabilidades estrictamente entre 0% y 100%.*
    >
    > *Incorporamos la asimetría estratégica de los mapas mediante interceptos aleatorios $\alpha_j$ por cada escenario. Debido a la introducción de la función logística no lineal, se rompe la conjugación matemática entre la verosimilitud Bernoulli y los priors normales. Esto hace que sea analíticamente imposible calcular la distribución posterior de forma directa a través de integraciones clásicas, obligándonos a utilizar métodos de simulación numérica para aproximar la posterior."*

#### **💬 Posible Pregunta Técnica de esta sección:**
*   **Pregunta del Profesor:** *¿Cómo justifica matemáticamente la estructura jerárquica frente a una regresión agrupada (Pooled) o desagrupada (Unpooled)?*
*   **Respuesta de Defensa:**
    > *"La estructura jerárquica se justifica por el balance sesgo-varianza mediante la agrupación parcial o 'partial pooling'. Un modelo agrupado (pooled) ignoraría la asimetría de los mapas, asumiendo erróneamente que todos los mapas tienen la misma favorabilidad base, lo que introduce sesgos predictivos.*
    >
    > *Un modelo desagrupado (unpooled) estimaría los interceptos de forma aislada, lo cual generaría estimaciones con una varianza inaceptablemente alta en mapas con pocas observaciones históricas.*
    >
    > *El modelo jerárquico permite que los mapas compartan información a través de una distribución común superior (hiperpriors $\mu_\alpha$ y $\sigma_\alpha$), encogiendo (*shrinkage*) los interceptos extremos hacia la media global cuando hay poca información. Además, la comparación de modelos mediante el criterio WAIC demostró estadísticamente la inmensa superioridad del enfoque jerárquico por más de 101 unidades predictivas logarítmicas."*

---

### **Diapositiva 6: Implementación MCMC y Salud del Sampler [Minuto 4:15 - 5:00]**

*   **Apoyo Visual Recomendado:**
    *   Indicadores de convergencia en texto grande: **$\hat{R} = 1.000$ - $1.001$**, **ESS > 10,000**.
    *   Un fragmento visual que represente la superposición perfecta del Chequeo Predictivo Posterior (PPC) (línea roja observada dentro de las bandas simuladas azules).
*   **Guión Verbal (Qué decir):**
    > *"Para aproximar la posterior imposible, implementamos algoritmos de muestreo avanzados MCMC, específicamente el sampler NUTS en PyMC. La salud computacional de las simulaciones fue impecable.*
    >
    > *El indicador de convergencia $\hat{R}$ se situó en un rango perfecto de entre 1.000 y 1.001 para todos los parámetros principales, indicando que las cadenas se mezclaron perfectamente. Asimismo, el tamaño de muestra efectivo, o ESS, superó las 10,000 muestras independientes, descartando problemas de autocorrelación. Finalmente, validamos la convergencia mediante Chequeos Predictivos Posteriores o PPC, donde la distribución de las partidas virtuales simuladas por el modelo encajó perfectamente con las partidas reales del servidor."*

#### **💬 Posible Pregunta Técnica de esta sección:**
*   **Pregunta del Profesor:** *¿Cómo aseguran que el muestreo MCMC realmente convergió y es representativo para las inferencias?*
*   **Respuesta de Defensa:**
    > *"Nos aseguramos mediante tres criterios estrictos. Primero, el semáforo estadístico $\hat{R}$ está estrictamente por debajo del límite académico de 1.01 para cada coeficiente e intercepto, lo que prueba que las cadenas convergieron al mismo espacio posterior. Segundo, el elevado ESS Bulk y Tail garantiza que tenemos suficientes muestras independientes para estimar los intervalos de credibilidad HDI sin ruido numérico. Tercero, la ausencia total de advertencias de transiciones divergentes durante el muestreo confirma que el sampler NUTS exploró con éxito todo el espacio posterior sin perderse en zonas de alta curvatura."*

---

### **Diapositiva 7: Interpretación de Resultados: Coeficientes y Asimetría [Minuto 5:00 - 6:15]**

*   **Apoyo Visual Recomendado:**
    *   Una tabla o gráfico de coeficientes $\beta_k$: **Rating 2.0 (+4.95)**, **Daño ADR (+0.095)**, **KAST (-5.47)**, **Impacto (+0.36, cruza el cero)**.
    *   Gráfico de asimetrías de mapas: Mirage favorable (53.6%), Overpass desfavorable (46.0%).
*   **Guión Verbal (Qué decir):**
    > *"Las estimaciones de los coeficientes arrojaron descubrimientos muy fuertes que desafían las creencias populares del juego competitivo:*
    >
    > *Primero, el diferencial de **Rating 2.0** es el rey indiscutible de la victoria, con un efecto altamente positivo de 4.95. *
    >
    > *Segundo, el **Impacto Táctico** presenta una alta incertidumbre marginal; su intervalo HDI cruza ampliamente el cero, revelando que las jugadas espectaculares pero aisladas, como los clutches, no compensan la falta de consistencia general del equipo.*
    >
    > *Tercero, la **Paradoja de KAST**. Estimamos un coeficiente fuertemente negativo de -5.47. Esto representa un *efecto de supresión*: una vez controlado el daño y la efectividad general, un KAST alto captura estilos pasivos de supervivencia tardía para salvar armas (*'saving'*). En la élite, ceder pasivamente el control espacial del mapa condena al fracaso.*
    >
    > *Finalmente, confirmamos que Mirage favorece al local con una probabilidad base del 53.6%, mientras que en Overpass cae al 46.0%, demostrando sesgos tácticos reales de cada mapa."*

#### **💬 Posible Pregunta Técnica de esta sección:**
*   **Pregunta del Profesor:** *¿Cómo se interpreta el coeficiente negativo de KAST si es una métrica de consistencia que se premia como algo positivo en la escena competitiva?*
*   **Respuesta de Defensa:**
    > *"Profesor, esto se explica estadísticamente por un efecto de supresión derivado de la colinealidad condicional. En el modelo ya estamos controlando de forma directa las variables que capturan la agresión y efectividad física (el Rating 2.0 y el ADR). Por lo tanto, el coeficiente de KAST pasa a capturar el efecto puro de la consistencia pasiva de supervivencia o asistencia sin efectividad de fuego.*
    >
    > *Esto refleja con precisión una dinámica estratégica real de Counter-Strike: equipos que intentan jugar de forma excesivamente conservadora, salvando armamento constantemente en situaciones tardías en lugar de buscar intercambios de bajas activos, terminan cediendo todo el control de mapa al oponente y, en consecuencia, desploman su probabilidad real de ganar."*

---

### **Diapositiva 8: Calibración Predictiva (ECE) y Conclusiones [Minuto 6:15 - 7:00]**

*   **Apoyo Visual Recomendado:**
    *   Curva de calibración visual del modelo mostrando el **Expected Calibration Error (ECE) = 1.2%**.
    *   Métricas clave en texto destacado: **Brier Score = 0.2404**, **WAIC $\Delta\text{elpd} = +101.61$**.
    *   Mensaje de cierre: *"La honestidad estadística e incertidumbre superan a las certezas falsas en el análisis predictivo."*
*   **Guión Verbal (Qué decir):**
    > *"Evaluamos el modelo bajo un marco de absoluta honestidad estadística. El modelo obtuvo un **Brier Score de 0.2404**, superando significativamente al azar. Pero nuestro mayor hito es el **Expected Calibration Error, o ECE, de apenas 1.2%**.*
    >
    > *Esto demuestra una calibración predictiva extraordinaria: si el modelo estima un 70% de probabilidades de ganar, en la realidad el equipo gana el 71.2% de las veces. No sufrimos de sobreconfianza.*
    >
    > *En conclusión, este proyecto demuestra que el éxito en el Counter-Strike profesional se construye sobre la consistencia silenciosa y desmitifica los estilos de juego excesivamente pasivos. Nuestra mayor contribución es proponer un estándar de honestidad estadística que, en lugar de vender certezas absolutas falsas, asume con madurez la asimetría de los escenarios y cuantifica con total transparencia la incertidumbre predictiva del juego.*
    >
    > *Muchas gracias. Quedamos abiertos a sus comentarios y preguntas."*

#### **💬 Posible Pregunta Técnica de esta sección:**
*   **Pregunta del Profesor:** *¿Un Brier Score de 0.2404 y un AUC-ROC de 0.6117 no son métricas algo bajas para un modelo predictivo?*
*   **Respuesta de Defensa:**
    > *"En los Esports de élite, la paridad técnica de los equipos es extrema y el azar tiene un rol protagónico dentro del servidor. Cualquier modelo que prometa una precisión del 90% en este nivel competitivo está sufriendo de un grave sobreajuste (overfitting).*
    >
    > *Nuestro AUC-ROC de 0.6117 es un valor honesto que describe con rigor el límite real de lo que los datos acumulados antes de la partida pueden explicarnos. El Brier Score de 0.2404 es mejor que el azar (que sería 0.25). Pero el verdadero valor no radica en forzar una clasificación determinista, sino en nuestra extraordinaria calibración del 1.2% de error ECE."*
