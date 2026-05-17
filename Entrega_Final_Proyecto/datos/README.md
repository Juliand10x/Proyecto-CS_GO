# Contexto de la Base de Datos: CS:GO Professional Matches

Esta base de datos contiene registros detallados de partidas profesionales de Counter-Strike: Global Offensive (CS:GO). El objetivo principal de este conjunto de datos es permitir el análisis del rendimiento individual y colectivo para predecir el resultado de los encuentros y cuantificar la incertidumbre en un entorno altamente competitivo.

## Estructura de las Filas
Cada fila representa un **encuentro profesional (mapa único)** disputado entre dos equipos. La base de datos incluye más de 3,700 partidas, lo que proporciona una muestra robusta del circuito de élite.

## Diccionario de Columnas

### Metadatos del Encuentro
* `match_date`: Fecha en la que se disputó la partida.
* `team_1` / `team_2`: Nombres de los equipos enfrentados.
* `t1_points` / `t2_points`: Rondas ganadas por cada equipo (marcador final del mapa).
* `winner`: Identificador del ganador (`t1` o `t2`).

### Variables de Ranking y Contexto
* `t1_world_rank` / `t2_world_rank`: Posición en el ranking mundial de HLTV al momento del partido.
* `t1_h2h_win_perc` / `t2_h2h_win_perc`: Porcentaje histórico de victorias entre estos dos equipos específicos.

### Variables de Rendimiento por Jugador
Para cada equipo (`t1` y `t2`) y cada jugador (del 1 al 5), se registran las siguientes métricas (ejemplo para `t1_player1_...`):

* `rating`: Rating 2.0 (métrica integral de rendimiento que combina bajas, supervivencia e impacto).
* `impact`: Valor de impacto (mide jugadas que cambian el curso de la ronda, como multikills y clutches).
* `kdr`: Kill/Death Ratio.
* `dmr`: Daño promedio por ronda (ADR).
* `kpr` / `apr` / `dpr`: Bajas, asistencias y muertes promedio por ronda.
* `opk_ratio`: Ratio de bajas de apertura (entry kills).
* `opk_rating`: Rating específico en duelos iniciales.
* `wins_perc_after_fk`: Porcentaje de rondas ganadas después de que este jugador obtiene la primera baja.
* `multikill_perc`: Porcentaje de rondas en las que el jugador logra más de una baja.
* `is_sniper`: Variable booleana que indica si el jugador tiene el rol de AWP (francotirador).
* `clutch_win_perc`: Porcentaje de éxito en situaciones de desventaja numérica.

## Lo que TENEMOS en la base de datos
* Datos granulares de desempeño individual (16 métricas por jugador).
* Contexto de jerarquía competitiva (World Rank).
* Resultados históricos directos (Head-to-Head).

## Lo que NO TENEMOS (Limitaciones)
* **Economía:** No se registra el estado monetario de los equipos en cada ronda (loss bonus, equipo comprado vs. eco).
* **Utilidad:** No hay datos sobre el daño por granadas, cegadoras efectivas o humo.
* **Estado Anímico:** Variables latentes como el cansancio de los jugadores o la presión psicológica del evento físico (LAN) vs. Online.
* **Comunicaciones:** No se dispone del registro de las llamadas tácticas (IGL calls) durante la partida.
