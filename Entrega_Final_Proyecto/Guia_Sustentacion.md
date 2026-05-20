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
    *   Gráfico de superposición del EDA de ganadores/perdedores.
    *   Diagrama de flujo del merge:
        *   `csgo_games.csv` (Metadatos de partidas) + `csgo_players.csv` (Rendimiento individual).
        *   *Problema:* Discordancia en nombres (`'ASTRALIS'` vs `'Astralis'`) y desajuste en timestamps de scrapers.
        *   *Algoritmo:* Normalización `str.upper()` + Mapeo de sinónimos + **Ventana temporal de coincidencia de 3 días ($\pm$ 72h)**.
        *   *Resultado:* Aumento de muestra de $N = 218$ a **$N = 5,745$ mapas** ($N_{partidas} = 3,341$). (¡Muestra 26x mayor!).
*   **Guión Verbal (Qué decir):**
    > *"Para sustentar nuestro modelo, extrajimos datos secundarios de HLTV entre 2016 y 2020 a través de dos bases de datos masivas: `csgo_games.csv` para los metadatos de las partidas y `csgo_players.csv` para las estadísticas individuales de cada jugador. Al intentar fusionarlas, nos topamos con un grave problema de calidad: inconsistencia de nombres en los equipos —por ejemplo, mayúsculas y minúsculas mezcladas como 'ASTRALIS' y 'Astralis'— y ligeras diferencias de fecha y hora debido a las zonas horarias de los scrapers.
    >
    > Un cruce estricto convencional destruía el 96.2% de nuestra información, dejándonos con una muestra minúscula de apenas 218 mapas, lo que creaba un severo sesgo de selección. 
    >
    > Para solucionarlo, diseñamos un pipeline de ingeniería de datos en Python: primero, convertimos todos los nombres a mayúsculas, removimos espacios y estandarizamos sinónimos tácticos. Segundo, implementamos una lógica de **cruce por ventana temporal deslizante**: emparejamos las estadísticas agregadas de los jugadores con su respectiva partida si la fecha de juego coincidía dentro de una ventana de tolerancia de **$\pm$ 3 días**.
    >
    > Este algoritmo de unión flexible rescató la base de datos, expandiéndola a **5,745 observaciones de mapas en 3,341 partidas**. En el EDA subsiguiente, calculamos los diferenciales promedio por mapa (Equipo 1 menos Equipo 2) de cada estadística y excluimos la variable de bajas/muertes (KDR) por mostrar una colinealidad del 97% con el Rating 2.0, garantizando la independencia lineal de nuestros regresores."*

#### **💬 Posible Pregunta Técnica de esta sección:**
*   **Pregunta del Profesor:** *¿Cómo se realizó técnicamente la limpieza y consolidación de la base de datos, y cómo afectaron las inconsistencias y la ventana temporal al sesgo de selección?*
*   **Respuesta de Defensa:** 
    > *"Profesor, la fusión original fallaba porque `csgo_games.csv` registraba las fechas a nivel de día de la partida y `csgo_players.csv` registraba la hora exacta del servidor, la cual a menudo difería por desfases de huso horario de los raspadores.
    >
    > Si hubiéramos conservado el cruce rígido inicial de 218 filas, habríamos incurrido en un sesgo de selección masivo: solo habríamos analizado partidos de equipos populares con nombres simples y horarios perfectamente sincronizados. 
    >
    > Al aplicar la unificación case-insensitive, eliminar espacios vacíos y construir un join condicional con una ventana temporal de $\pm$ 3 días en Pandas, logramos conservar 5,745 mapas. Esto asegura que la muestra representa fielmente todo el espectro competitivo de la escena internacional, reduciendo significativamente el error de estimación de nuestro posterior."*

---

### **Diapositiva 4: Búsqueda de Expertos y Definición de las Priors [Minuto 2:30 - 3:15]**

*   **Apoyo Visual Recomendado:**
    *   Ecuaciones de los priors en LaTeX limpio: $\beta_k \sim \text{Normal}(0, 5^2)$, $\mu_\alpha \sim \text{Normal}(0, 5^2)$, $\sigma_\alpha \sim \text{HalfNormal}(2)$.
    *   Nota conceptual: *"Los expertos definen el problema y el rango de los priors, pero la verosimilitud de la gran muestra domina la estimación final sin sesgar la verosimilitud (Likelihood)."*
*   **Guión Verbal (Qué decir):**
    > *"En la estadística bayesiana, la definición de las distribuciones previas o priors es crucial. Consultando la teoría y la opinión de expertos del juego, seleccionamos las cuatro variables de desempeño explicativas fundamentales (Rating, Daño, Impacto y KAST).
    >
    > Para no imponer sesgos subjetivos en las estimaciones, definimos priors de filosofía débilmente informativa: distribuciones normales centradas en cero con desviación estándar de 5 para los coeficientes de desempeño y para la media global de los mapas, y una distribución Half-Normal para la desviación estándar entre escenarios. Esto actúa como un regularizador matemático que estabiliza el modelo, pero permite que la enorme masa de datos del servidor domine la estimación de la posterior."*

#### **💬 Posible Pregunta Técnica de esta sección:**
*   **Pregunta del Profesor:** *¿Por qué priors normales débilmente informativas ($Normal(0, 5^2)$) en lugar de priors planas o uniformes no informativas?*
*   **Respuesta de Defensa:**
    > *"Profesor, los priors planos (como los uniformes de $-\infty$ a $+\infty$) son computacionalmente peligrosos en los modelos jerárquicos bayesianos. Permiten al algoritmo MCMC explorar regiones del espacio de parámetros con densidad de probabilidad absurda, lo que produce fallos de muestreo conocidos como transiciones divergentes.
    >
    > Un prior débilmente informativo como el $Normal(0, 25)$ actúa como un regulador suave: asume que es sumamente improbable encontrar un efecto de desempeño gigantesco en la escala logit. Dado que nuestra muestra definitiva cuenta con 5,745 mapas, la verosimilitud de los datos domina por completo el posterior, pero el prior estabiliza el sampler MCMC, asegurando la convergencia computacional."*

---

### **Diapositiva 5: Definición de la Likelihood e Imposibilidad de la Posterior [Minuto 3:15 - 4:15]**

*   **Apoyo Visual Recomendado:**
    *   Fórmulas matemáticas en LaTeX:
        *   Verosimilitud (Likelihood): $y_i \sim \text{Bernoulli}(p_i)$
        *   Enlace Logístico: $\text{logit}(p_i) = \alpha_{map[i]} + \beta_1 \cdot \text{diff\_rating}_i + \beta_2 \cdot \text{diff\_impact}_i + \beta_3 \cdot \text{diff\_adr}_i + \beta_4 \cdot \text{diff\_kast}_i$
        *   Interceptos Jerárquicos: $\alpha_j \sim \text{Normal}(\mu_\alpha, \sigma_\alpha^2) \quad (j = 1,\dots, 9 \text{ mapas})$
    *   Esquema de código PyMC (para mostrar rigor de programación):
        ```python
        # pm.Model() en PyMC 5.x
        # Interceptos por mapa (Partial Pooling)
        alpha = pm.Normal('alpha', mu=mu_alpha, sigma=sigma_alpha, shape=9)
        # Sampler: pm.sample(draws=2000, tune=2000, chains=4, target_accept=0.95)
        ```
*   **Guión Verbal (Qué decir):**
    > *"Nuestra verosimilitud o Likelihood sigue una distribución de Bernoulli, idónea para la variable binaria 'Victoria o Derrota'. Conectamos esta probabilidad con las variables mediante una función de enlace logit inversa para curvar la combinación lineal linealmente y restringirla estrictamente entre 0 y 1. 
    >
    > La asimetría base de los mapas la modelamos a través de interceptos aleatorios jerárquicos $\alpha_j$. La introducción de la función logística no lineal destruye la conjugación matemática entre nuestra verosimilitud de Bernoulli y los priors normales. Esto significa que la integral del denominador de la regla de Bayes no tiene una solución en forma cerrada; es analíticamente imposible de calcular.
    >
    > Para solucionarlo, construimos el modelo en Python usando **PyMC 5.x**, estructurando el modelo jerárquico con indexación de mapas para aplicar 'partial pooling'. Estimamos la posterior mediante simulaciones avanzadas con el muestreador **MCMC NUTS (No-U-Turn Sampler)**, configurando **4 cadenas paralelas**, con **2,000 pasos de tuneo (calentamiento)** y **2,000 muestras útiles** por cadena, consolidando un total de **8,000 muestras de la posterior** y configurando un `target_accept` alto de 0.95 para garantizar una estabilidad matemática perfecta."*

#### **💬 Posible Pregunta Técnica de esta sección:**
*   **Pregunta del Profesor:** *¿Cómo estructuró técnicamente el modelo en código y cómo parametrizó el muestreador MCMC para evitar sesgos numéricos e inestabilidades?*
*   **Respuesta de Defensa:**
    > *"Profesor, el modelo se programó en PyMC declarando un bloque contextual `pm.Model()`. Mapeamos los 9 escenarios competitivos a un vector entero de índices (`map_idx` de 0 a 8) para que actúe como índice de asignación de los interceptos aleatorios.
    >
    > Para el muestreo, parametrizamos el algoritmo NUTS (No-U-Turn Sampler), que es una variante avanzada del MCMC Hamiltoniano que utiliza la geometría del gradiente de la posterior para explorar el espacio de forma inteligente.
    >
    > Estipulamos 2,000 pasos de `tune` por cadena para permitir que el sampler auto-calibrara su matriz de masa y el tamaño de paso óptimo, y 2,000 `draws` por cadena para recopilar las muestras de la posterior. Al ejecutar 4 cadenas independientes obtuvimos 8,000 estimaciones independientes. Elevamos el parámetro `target_accept` a 0.95 para forzar al sampler a tomar pasos más finos y evitar transiciones divergentes debido a la geometría jerárquica, resultando en 0 divergencias."*

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
