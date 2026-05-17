#!/usr/bin/env python3
"""
HLTV Scraper — Extiende el dataset con partidas 2020–2026.

Extrae:
  - Lista de matches de un evento (equipos, scores, fechas)
  - Mapas jugados por match (nombres de mapa)
  - Resultados por mapa (extraídos cuando sea posible)

No puede extraer stats por jugador (rating/impact/ADR/KAST) — Cloudflare bloquea /stats/

Uso:
  python hltv_scraper.py --test              # 1 match de prueba
  python hltv_scraper.py --event 7524        # 1 evento
  python hltv_scraper.py --auto --max-events 5  # eventos automáticos
  python hltv_scraper.py                     # eventos predefinidos

Output:
  scraped/matches_scraped.csv   → matches con mapas
  scraped/results_scraped.csv   → formato results.csv
"""

import json, os, sys, time, random, re
import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError

BASE_URL = "https://www.hltv.org"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "scraped")
CHECKPOINT_FILE = os.path.join(OUTPUT_DIR, "checkpoint.json")
DELAY_MIN, DELAY_MAX = 1.0, 2.5

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Eventos predefinidos con IDs conocidos
KNOWN_EVENTS = {
    "Austin 2025 Major": 7902,
    "Shanghai 2024 Major": 7524,
    "Copenhagen 2024 Major": 7148,
    "Paris 2023 Major": 6793,
    "Rio 2022 Major": 6248,
    "Antwerp 2022 Major": 6133,
    "Stockholm 2021 Major": 5802,
    "IEM Katowice 2025": 7887,
    "IEM Katowice 2024": 7003,
    "IEM Katowice 2023": 6262,
    "IEM Katowice 2022": 6130,
    "IEM Cologne 2024": 7246,
    "IEM Cologne 2023": 6597,
    "IEM Cologne 2022": 6440,
    "BLAST Fall Final 2024": 7618,
    "BLAST Spring Final 2024": 7413,
    "BLAST World Final 2024": 7646,
    "ESL Pro League S20 2024": 7561,
    "ESL Pro League S19 2024": 7368,
    "ESL Pro League S18 2023": 6685,
}

S = "═" * 60


def delay():
    time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))


def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE) as f:
            return json.load(f)
    return {"done_events": [], "done_matches": {}}


def save_checkpoint(cp):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(cp, f, indent=2)


def new_browser(headless=True):
    pw = sync_playwright().start()
    browser = pw.chromium.launch(
        headless=headless,
        args=["--no-sandbox", "--disable-blink-features=AutomationControlled",
              "--disable-dev-shm-usage", "--disable-setuid-sandbox"]
    )
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080},
        locale="en-US",
    )
    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
    return pw, browser, ctx, page


# ── 1. Extraer eventos automáticamente ──
def auto_events(page, max_pages=3):
    events = {}
    for pn in range(max_pages):
        url = f"{BASE_URL}/events?eventType=PREMIER&offset={pn*50}"
        print(f"  [auto] p{pn+1}: {url}")
        try:
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)
        except:
            break
        links = page.query_selector_all("a[href*='/events/']")
        seen = set()
        for link in links:
            href = link.get_attribute("href") or ""
            if "/events/" not in href:
                continue
            eid = href.split("/events/")[1].split("/")[0]
            if not eid.isdigit() or eid in seen:
                continue
            seen.add(eid)
            name = link.query_selector(".event-name") or link
            try:
                name_text = name.inner_text().strip()[:60]
            except:
                name_text = f"Event_{eid}"
            if name_text:
                events[name_text] = int(eid)
        print(f"    → {len(seen)} eventos")
    return events


# ── 2. Extraer matches de evento ──
def extract_matches(page, event_id, event_name, limit=None):
    url = f"{BASE_URL}/results?event={event_id}"
    print(f"  [matches] {event_name} (id={event_id})")
    try:
        page.goto(url, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_timeout(4000)
    except:
        return []

    links = page.query_selector_all("a[href*='/matches/']")
    matches, seen = [], set()

    for link in links:
        href = link.get_attribute("href") or ""
        if "/matches/" not in href:
            continue
        mid = href.split("/matches/")[1].split("/")[0]
        if mid in seen:
            continue
        seen.add(mid)
        try:
            row = link.evaluate_handle("el => el.closest('.result-con')")
            if not row:
                continue
            t1 = row.query_selector(".team1 .team")
            t2 = row.query_selector(".team2 .team")
            sc = row.query_selector(".result-score")
            if not t1 or not t2 or not sc:
                continue
            score_text = sc.inner_text().strip()
            if "-" not in score_text:
                continue
            s1s, s2s = score_text.split("-", 1)
            if not s1s.strip().isdigit() or not s2s.strip().isdigit():
                continue
            matches.append({
                "match_id": mid,
                "event_id": event_id,
                "event": event_name,
                "team_1": t1.inner_text().strip(),
                "team_2": t2.inner_text().strip(),
                "score_1": int(s1s.strip()),
                "score_2": int(s2s.strip()),
                "url": f"{BASE_URL}/matches/{mid}",
            })
        except:
            continue
        if limit and len(matches) >= limit:
            break

    print(f"    → {len(matches)} matches")
    return matches


# ── 3. Extraer mapas de match ──
def extract_maps(page, match):
    try:
        page.goto(match["url"], timeout=25000, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)
    except:
        return []

    maps = []
    all_links = page.query_selector_all("a")
    for link in all_links:
        href = link.get_attribute("href") or ""
        if "/stats/matches/mapstatsid/" not in href:
            continue
        # Extraer mapstats ID
        mid_match = re.search(r"mapstatsid/(\d+)", href)
        mapstats_id = mid_match.group(1) if mid_match else ""

        # Nombre del mapa
        map_name = ""
        try:
            container = link.evaluate_handle(
                "el => el.closest('.mapholder')?.querySelector('.mapname')"
            )
            if container:
                map_name = container.inner_text().strip()
        except:
            pass

        # Resultado
        score1, score2 = "", ""
        try:
            container = link.evaluate_handle("el => el.closest('.mapholder')")
            if container:
                results = container.query_selector_all(".results-center .results")
                if len(results) >= 2:
                    team_won_el = container.query_selector(".results-left .results-team-won, .results-right .results-team-won")
                    score1 = results[0].inner_text().strip()
                    score2 = results[1].inner_text().strip()
        except:
            pass

        maps.append({
            "match_id": match["match_id"],
            "event_id": match["event_id"],
            "map_name": map_name,
            "mapstats_id": mapstats_id,
            "score_1": score1,
            "score_2": score2,
        })

    return maps


# ── MAIN ──
def run(events, test_mode=False, max_per_event=None):
    cp = load_checkpoint()
    all_matches = []
    all_maps = []

    pw, browser, ctx, page = new_browser(headless=False)

    # Calentar sesión
    print("🌐 Calentando sesión HLTV...")
    page.goto(BASE_URL, timeout=20000, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    print(f"   Homepage: {page.title()[:80]}")

    for ev_name, ev_id in events.items():
        if str(ev_id) in cp["done_events"]:
            print(f"\n⏭️  {ev_name} — ya completado")
            continue

        print(f"\n{S}\n📊 {ev_name} (id={ev_id})\n{S}")
        delay()

        matches = extract_matches(page, ev_id, ev_name, limit=max_per_event)
        if test_mode:
            matches = matches[:1]
            print("   🧪 TEST MODE: 1 match")

        event_maps = []
        for mi, m in enumerate(matches):
            mid = m["match_id"]
            ev_k = str(ev_id)
            done_list = cp["done_matches"].get(ev_k, [])
            if mid in done_list:
                continue

            print(f"   [{mi+1}/{len(matches)}] {m['team_1']} {m['score_1']}-{m['score_2']} {m['team_2']}")
            delay()

            maps = extract_maps(page, m)
            for mp in maps:
                print(f"      → {mp['map_name']:15s} {mp['score_1']}-{mp['score_2']}")
                event_maps.append(mp)

            all_matches.append(m)
            done_list.append(mid)
            cp["done_matches"][ev_k] = done_list
            save_checkpoint(cp)

            if test_mode:
                break

        all_maps.extend(event_maps)
        cp["done_events"].append(str(ev_id))
        save_checkpoint(cp)
        print(f"   ✅ {ev_name}: {len(matches)} matches, {len(event_maps)} mapas")

    browser.close()
    pw.stop()

    # ── GUARDAR ──
    print(f"\n{S}\n🏁 SCRAPING COMPLETO\n{S}")
    print(f"Total matches: {len(all_matches)}")
    print(f"Total mapas:   {len(all_maps)}")

    if all_matches:
        pd.DataFrame(all_matches).to_csv(f"{OUTPUT_DIR}/matches_scraped.csv", index=False)
        print(f"→ {OUTPUT_DIR}/matches_scraped.csv")

    if all_maps:
        maps_df = pd.DataFrame(all_maps)
        maps_df.to_csv(f"{OUTPUT_DIR}/maps_scraped.csv", index=False)
        print(f"→ {OUTPUT_DIR}/maps_scraped.csv")

        # Formato results.csv
        results_rows = []
        for _, mp in maps_df.iterrows():
            # Encontrar el match correspondiente
            match_row = next((m for m in all_matches if m["match_id"] == mp["match_id"]), None)
            if not match_row:
                continue
            results_rows.append({
                "date": match_row.get("event", ""),
                "team_1": match_row["team_1"],
                "team_2": match_row["team_2"],
                "_map": mp["map_name"],
                "result_1": mp.get("score_1", ""),
                "result_2": mp.get("score_2", ""),
                "event_id": mp["event_id"],
                "match_id": mp["match_id"],
                "scraped": True,
            })
        if results_rows:
            pd.DataFrame(results_rows).to_csv(f"{OUTPUT_DIR}/results_scraped.csv", index=False)
            print(f"→ {OUTPUT_DIR}/results_scraped.csv ({len(results_rows)} filas)")

    print("✅ Listo.")


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="HLTV Scraper — CS:GO matches + maps")
    p.add_argument("--test", action="store_true", help="1 match de prueba")
    p.add_argument("--event", type=int, help="Scrapear 1 evento por ID")
    p.add_argument("--auto", action="store_true", help="Buscar eventos automáticamente")
    p.add_argument("--max", type=int, default=None, help="Máx matches por evento")
    p.add_argument("--max-events", type=int, default=None, help="Máx eventos a scrapear")
    args = p.parse_args()

    if args.event:
        events = {f"Event_{args.event}": args.event}
    elif args.auto:
        print("🔍 Extrayendo eventos de HLTV.org/events...")
        pw, browser, ctx, page = new_browser(headless=False)
        page.goto(BASE_URL, timeout=20000, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        events = auto_events(page)
        browser.close()
        pw.stop()
        print(f"→ {len(events)} eventos encontrados")
        if args.max_events:
            events = dict(list(events.items())[:args.max_events])
    else:
        events = KNOWN_EVENTS
        print(f"Usando {len(events)} eventos predefinidos")

    run(events, test_mode=args.test, max_per_event=args.max)
