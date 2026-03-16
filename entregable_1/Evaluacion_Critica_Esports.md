# Marco Inicial para Analizar Investigación en Ciencia de Datos

**Caso de Estudio Base:** *Data Science and Analytics for Esports (Agrawal et al.)*
**Evaluador:** Julian Jimenez, Julian Duarte, Tomas Rincon

---

### 1. Pregunta de Investigación
**¿Qué se quiere entender o explicar realmente?**

La investigación busca resolver un problema fundamental de escalabilidad en el análisis táctico de *Counter-Strike: Global Offensive* (CS:GO). Tradicionalmente, los entrenadores y analistas dependen de la revisión manual de videos (VODs) para entender las dinámicas del juego, un proceso lento y propenso a sesgos cognitivos. La pregunta central del estudio no es de naturaleza causal o predictiva, sino de **Ingeniería de Software e Infraestructura de Datos**: ¿Cómo se puede diseñar, implementar y validar una herramienta computacional (un *parser*) capaz de procesar masivamente los archivos binarios de las partidas para transformar eventos deterministas complejos (coordenadas espaciales, trayectorias de daño, alteraciones en la economía) en estructuras de datos tabulares y legibles que permitan una evaluación empírica y a gran escala del desempeño de los equipos?

### 2. Supuestos Subyacentes
**¿Qué se da por sentado sobre el fenómeno, los datos, las personas o el contexto?**

El estudio edifica su propuesta sobre varios supuestos epistemológicos fuertes respecto al ecosistema competitivo:
1. **Visión Mecanicista del Rendimiento:** Se asume que el rendimiento táctico y estratégico de un equipo puede ser capturado y cuantificado en su totalidad por métricas discretas (como el Daño Promedio por Ronda o el porcentaje de Tiros a la Cabeza). 
2. **Aditividad del Rendimiento Individual:** Se asume implícitamente que el éxito del colectivo es, en gran medida, la suma lineal de las métricas de eficacia individual, dejando en un segundo plano las sinergias no cuantificables espacialmente.
3. **Ergodicidad Táctica:** Se da por sentado que los patrones históricos capturados en estos *demofiles* son representativos de la habilidad pura ("True Skill") y que estos comportamientos tenderán a repetirse bajo condiciones similares, obviando la constante evolución adaptativa del *metajuego* entre torneos.
4. **Aislamiento Psicológico:** El modelo subyacente asume que los actores (jugadores) operan como agentes racionales maximizadores de utilidad, ignorando factores humanos críticos en un entorno de alta presión deportiva.

### 3. Evidencia Utilizada
**¿Qué datos se usan y qué representan? ¿Qué queda fuera del dataset?**

**Naturaleza de la evidencia:** Se emplean los *demofiles* (archivos con extensión `.dem`) generados nativamente por el motor Source de Valve. A diferencia del análisis en deportes tradicionales, donde la recolección de eventos depende de la observación humana (con un margen de error inherente), estos datos representan la **verdad absoluta del servidor**. Registran posiciones tridimensionales (X, Y, Z), vectores de mirada, y alteraciones de estado de los jugadores con una frecuencia muy alta (64 o 128 *ticks* por segundo).

**¿Qué queda fuera del dataset?:** A pesar de la precisión milimétrica del registro espacial, el dataset excluye dimensiones vitales del fenómeno competitivo:
* La comunicación verbal e intra-equipo (*voice comms*), la cual dicta frecuentemente si un error de posicionamiento fue un fallo individual o una instrucción táctica mal ejecutada derivada de un *callout* erróneo (el *In-Game Leader*).
* Factores de entorno exógeno: Diferencias de latencia cognitiva (Ping) en partidos clasificatorios *online* versus torneos presenciales (LAN) en estadios con miles de espectadores, los cuales alteran profundamente el nivel de estrés.
* El historial del *Draft* o fase de bloqueos (Picks & Bans) que establece un marco psicológico pre-partida sobre qué equipo fue forzado a jugar en un mapa incómodo.

### 4. Método e Inferencias
**¿Qué tipo de resultados e inferencias permite (y cuáles no)?**

El método principal es la manipulación de flujos de bytes (un *parser* desarrollado en Python) para transformar datos no estructurados en *DataFrames* de Pandas y calcular agregaciones estadísticas (medianas, conteos).

* **Lo que SÍ permite:** Realizar inferencias **estrictamente descriptivas y retrospectivas** de alta fidelidad. Permite responder "qué", "quién" y "dónde" sucedió un evento específico (por ejemplo, los mapas de calor de posiciones defensivas).
* **Lo que NO permite:** Al ser un enfoque de extracción, el método **no** permite inferir causalidad estatística (¿Perdió el equipo A la ronda *porque* el jugador X compró el arma equivocada?). Tampoco permite la inferencia **predictiva ni la modelación bajo incertidumbre** (no provee intervalos de confianza ni estimaciones bayesianas sobre futuros resultados) debido a la ausencia de un marco probabilístico o modelo de regresión.

### 5. Resultados y Robustez
**¿Qué métricas, patrones o relaciones aparecen? ¿Qué tan robustos son esos resultados?**

El estudio produce matrices estructuradas, visualizaciones 2D de posicionamiento y resúmenes de *box scores* clásicos del entorno FPS (ADR, KPR, Sobrevivencia, etc.) aplicados a encuentros emblemáticos (ej. Astralis vs. Team Liquid).

**Sobre la robustez:** Es fundamental realizar una distinción técnica. Desde el dominio de la estructura de la base de datos, los resultados son **100% robustos y deterministas**, carentes de ruido de medición porque el motor del juego nunca miente sobre lo reportado. Sin embargo, analíticamente, **los resultados son débiles o superficiales**. No se reportan pruebas de significancia estadística, correlaciones cruzadas ni coeficientes que midan la varianza explicada. Son, en esencia, relaciones observacionales planas de primer nivel.

### 6. Interpretaciones y Conclusiones Críticas
**¿Qué afirmaciones sobre el fenómeno se hacen? ¿Hay saltos lógicos, causalidad insinuada o generalizaciones indebidas?**

Los autores concluyen que su herramienta provee un método de evaluación "puramente objetivo" para que las organizaciones midan la eficacia de sus jugadores frente a oponentes de primer nivel. 

* **El Salto Lógico principal:** Existe una generalización indebida al confundir la *Ingeniería de Datos* (Extracción, Transformación y Carga, ETL) con el *Análisis Táctico Avanzado*. Afirman que estas tablas estandarizadas equivalen a poseer una ventaja estratégica. Sin embargo, la acumulación masiva de datos y el cálculo descriptivo por sí solo no garantiza *insights* valiosos a menos que sea cruzado por un analista humano brillante o introducido en un modelo matemático inferencial jerárquico.
* **Causalidad Insinuada:** Se insinúa un marco de causa-efecto donde la mejora en indicadores numéricos estáticos (como el K/D) desemboca directamente en victorias en serie, ignorando la altísima colinealidad que existe en un juego de economía compartida como CS:GO.

### 7. Implicaciones, Alcance y Límites
**¿Qué se sugiere hacer con estos resultados? ¿A quién aplica y a quién no? ¿Dónde deja de ser válido lo que se concluye?**

El artículo finaliza sugiriendo, de manera muy acertada, que esta estructura de datos limpia debe funcionar como la base fundacional (el *input pipeline*) para alimentar en el futuro algoritmos predictivos complejos (como Redes Neuronales o modelos de Inteligencia Artificial espaciotemporal).

* **A quién aplica:** A equipos y organizaciones profesionales (Tier 1 / Tier 2) que posean la capacidad e infraestructura de emplear analistas de datos o desarrolladores en plantilla capaces de consumir herramientas programáticas basadas en Python y Pandas.
* **A quién NO aplica:** A equipos semi-profesionales carentes de literacidad técnica, o a sistemas predictivos pre-partida (como modelos de casas de apuestas y estimadores de cuotas), ya que los datos aquí procesados solamente se generan **después** de que la partida ha concluido, limitando radicalmente su uso *in-play* o de pronóstico en vivo.
* **Límites críticos (Pérdida de Validez):** La limitación terminal más grave recae sobre la arquitectura y propiedad del videojuego. Dado que CS:GO es un software propietario de la compañía *Valve*, cualquier actualización invisible del desarrollador que altere un mínimo byte de la codificación del protocolo de red en el archivo `.dem` puede quebrar el *parser* por completo. Esto hace que las conclusiones y utilidades de la herramienta dependan de una constante labor de mantenimiento reactivo de ingeniería inversa sobre un formato cerrado y ofuscado.
