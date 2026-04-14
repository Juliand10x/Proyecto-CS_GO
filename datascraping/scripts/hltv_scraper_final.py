import asyncio
import pandas as pd
import argparse
import os
import re
from playwright.async_api import async_playwright

BASE_URL = "https://www.hltv.org"
OUTPUT_DIR = "data"

EVENTS = {
    "Budapest 2025": 8042,   # empezamos con 1 para probar
}

os.makedirs(OUTPUT_DIR, exist_ok=True)


async def safe_text(el):
    try:
        return (await el.inner_text()).strip()
    except:
        return ""


# ════════════════════════════════════════
# 1. EXTRAER LINKS DE MATCHES (MÉTODO NUEVO)
# ════════════════════════════════════════
async def get_match_links(page, event_id):
    print(f"\n🔗 Extrayendo links de matches event={event_id}")

    url = f"{BASE_URL}/results?event={event_id}"
    await page.goto(url)

    await page.wait_for_timeout(5000)

    links = await page.query_selector_all("a[href*='/matches/']")

    match_links = []
    seen = set()

    for link in links:
        href = await link.get_attribute("href")
        if not href:
            continue

        if "/matches/" not in href:
            continue

        match_id = href.split("/")[2]

        if match_id in seen:
            continue

        seen.add(match_id)
        match_links.append(BASE_URL + href)

    print(f"✅ {len(match_links)} match links encontrados")
    return match_links


# ════════════════════════════════════════
# 2. EXTRAER MAPSTATS DESDE MATCH
# ════════════════════════════════════════
async def get_map_links(page, match_url):
    await page.goto(match_url)

    await page.wait_for_timeout(4000)

    links = await page.query_selector_all("a[href*='/mapstatsid/']")

    map_links = []

    for link in links:
        href = await link.get_attribute("href")
        if href:
            map_links.append(BASE_URL + href)

    return map_links


# ════════════════════════════════════════
# 3. SCRAPEAR MAPA (LO IMPORTANTE)
# ════════════════════════════════════════
async def scrape_map(page, url):
    await page.goto(url)

    await page.wait_for_selector(".stats-table", timeout=15000)

    teams = await page.query_selector_all(".teamName")
    if len(teams) < 2:
        return None, []

    team1 = await safe_text(teams[0])
    team2 = await safe_text(teams[1])

    scores = await page.query_selector_all(".totalScore")
    if len(scores) < 2:
        return None, []

    score1 = await safe_text(scores[0])
    score2 = await safe_text(scores[1])

    tables = await page.query_selector_all(".stats-table")

    players = []

    for i, table in enumerate(tables[:2]):
        rows = await table.query_selector_all("tbody tr")
        team = team1 if i == 0 else team2

        for r in rows:
            cols = await r.query_selector_all("td")
            if len(cols) < 6:
                continue

            players.append({
                "team": team,
                "player": await safe_text(cols[0]),
                "kills": await safe_text(cols[1]),
                "deaths": await safe_text(cols[2]),
                "adr": await safe_text(cols[4]),
                "kast": await safe_text(cols[5]),
                "rating": await safe_text(cols[-1]),
                "map_url": url
            })

    return {
        "team1": team1,
        "team2": team2,
        "score1": score1,
        "score2": score2,
        "map_url": url
    }, players


# ════════════════════════════════════════
# MAIN
# ════════════════════════════════════════
async def run(test_mode=False):
    all_maps = []
    all_players = []

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(BASE_URL)
        await page.wait_for_timeout(3000)

        for event_name, event_id in EVENTS.items():
            match_links = await get_match_links(page, event_id)

            if test_mode:
                match_links = match_links[:1]

            for match_url in match_links:
                print(f"\n🎮 Match: {match_url}")

                map_links = await get_map_links(page, match_url)

                print(f"   → {len(map_links)} mapas")

                for ml in map_links:
                    map_data, players = await scrape_map(page, ml)

                    if map_data:
                        map_data["event"] = event_name
                        all_maps.append(map_data)

                    all_players.extend(players)

        await browser.close()

    pd.DataFrame(all_maps).to_csv(f"{OUTPUT_DIR}/maps.csv", index=False)
    pd.DataFrame(all_players).to_csv(f"{OUTPUT_DIR}/players.csv", index=False)

    print("\n✅ Scraping completo")


# ENTRY
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    asyncio.run(run(test_mode=args.test))