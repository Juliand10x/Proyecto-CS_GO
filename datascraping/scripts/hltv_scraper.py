import asyncio
import pandas as pd
import argparse
from playwright.async_api import async_playwright

BASE_URL = "https://www.hltv.org"

EVENTS = {
    "Copenhagen 2024": 7148,
    "Shanghai 2024": 7524,
    "Austin 2025": 7902,
    "Budapest 2025": 8042
}

OUTPUT_DIR = "data"


# ════════════════════════════════════════
# UTILIDADES
# ════════════════════════════════════════
async def safe_text(el):
    try:
        return (await el.inner_text()).strip()
    except:
        return ""


# ════════════════════════════════════════
# 1. SCRAPEAR MATCHES (CORREGIDO)
# ════════════════════════════════════════
async def get_matches(page, event_id, event_name):
    print(f"📊 Obteniendo matches: {event_name}")
    await page.goto(f"{BASE_URL}/results?event={event_id}")
    await page.wait_for_timeout(5000)

    matches = []
    seen = set()

    links = await page.query_selector_all("a[href*='/matches/']")

    for link in links:
        href = await link.get_attribute("href")
        if not href or "/matches/" not in href:
            continue

        match_id = href.split("/")[2]
        if match_id in seen:
            continue
        seen.add(match_id)

        container = await link.evaluate_handle("el => el.closest('.result-con')")
        if not container:
            continue

        try:
            team1_el = await container.query_selector(".team1 .team")
            team2_el = await container.query_selector(".team2 .team")
            score_el = await container.query_selector(".result-score")
        except:
            continue

        if not team1_el or not team2_el or not score_el:
            continue

        team1 = await safe_text(team1_el)
        team2 = await safe_text(team2_el)
        score = await safe_text(score_el)

        if "-" not in score:
            continue

        s1, s2 = score.split("-")

        # 🔥 FILTRO: SOLO MATCHES JUGADOS
        if not s1.isdigit() or not s2.isdigit():
            continue

        matches.append({
            "event": event_name,
            "match_id": match_id,
            "team1": team1,
            "team2": team2,
            "score1": int(s1),
            "score2": int(s2),
            "url": BASE_URL + href
        })

    print(f"✅ {len(matches)} matches válidos")
    return matches


# ════════════════════════════════════════
# 2. OBTENER MAPAS
# ════════════════════════════════════════
async def get_maps(page, match):
    await page.goto(match["url"])
    await page.wait_for_timeout(4000)

    maps = []
    links = await page.query_selector_all("a[href*='/mapstatsid/']")

    for link in links:
        href = await link.get_attribute("href")
        if not href:
            continue

        maps.append({
            "match_id": match["match_id"],
            "map_url": BASE_URL + href
        })

    return maps


# ════════════════════════════════════════
# 3. STATS POR MAPA (CORREGIDO)
# ════════════════════════════════════════
async def get_map_stats(page, map_entry, match):
    await page.goto(map_entry["map_url"])
    await page.wait_for_timeout(5000)

    # Equipos
    teams = await page.query_selector_all(".teamName")
    if len(teams) < 2:
        return None, []

    team1 = await safe_text(teams[0])
    team2 = await safe_text(teams[1])

    # Score
    scores = await page.query_selector_all(".totalScore")
    if len(scores) < 2:
        return None, []

    score1 = await safe_text(scores[0])
    score2 = await safe_text(scores[1])

    # Tablas correctas
    tables = await page.query_selector_all(".stats-table")
    if len(tables) < 2:
        return None, []

    player_rows = []

    for i, table in enumerate(tables[:2]):
        rows = await table.query_selector_all("tbody tr")
        team = team1 if i == 0 else team2

        for r in rows:
            cols = await r.query_selector_all("td")
            if len(cols) < 6:
                continue

            player_rows.append({
                "event": match["event"],
                "match_id": match["match_id"],
                "team": team,
                "player": await safe_text(cols[0]),
                "kills": await safe_text(cols[1]),
                "deaths": await safe_text(cols[2]),
                "adr": await safe_text(cols[4]),
                "kast": await safe_text(cols[5]),
                "rating": await safe_text(cols[-1]),
            })

    map_result = {
        "event": match["event"],
        "match_id": match["match_id"],
        "team1": team1,
        "team2": team2,
        "score1": score1,
        "score2": score2
    }

    return map_result, player_rows


# ════════════════════════════════════════
# MAIN
# ════════════════════════════════════════
async def run(test_mode=False):
    all_matches = []
    all_maps = []
    all_players = []

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        page = await browser.new_page()

        # Cookies
        await page.goto(BASE_URL)
        await page.wait_for_timeout(3000)

        for event_name, event_id in EVENTS.items():
            matches = await get_matches(page, event_id, event_name)

            # 🧪 TEST MODE → solo 1 match
            if test_mode:
                matches = matches[:1]

            for match in matches:
                print(f"➡️ {match['team1']} vs {match['team2']}")

                maps = await get_maps(page, match)

                for m in maps:
                    map_res, players = await get_map_stats(page, m, match)

                    if map_res:
                        all_maps.append(map_res)
                    all_players.extend(players)

                all_matches.append(match)

        await browser.close()

    # Guardar CSV
    pd.DataFrame(all_matches).to_csv(f"{OUTPUT_DIR}/matches.csv", index=False)
    pd.DataFrame(all_maps).to_csv(f"{OUTPUT_DIR}/maps.csv", index=False)
    pd.DataFrame(all_players).to_csv(f"{OUTPUT_DIR}/players.csv", index=False)

    print("\n✅ Scraping completo")


# ════════════════════════════════════════
# ENTRY POINT
# ════════════════════════════════════════
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Solo 1 match")
    args = parser.parse_args()

    asyncio.run(run(test_mode=args.test))