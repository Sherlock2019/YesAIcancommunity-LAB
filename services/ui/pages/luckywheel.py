#!/usr/bin/env python3
"""🎱 Lucky Wheel EuroMillions page."""
from __future__ import annotations

import random
from datetime import datetime
from typing import Any, Dict, List, Tuple
from urllib.parse import urljoin

import numpy as np
import pandas as pd
import requests
import streamlit as st

try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    import subprocess
    import sys

    st.warning("Installing beautifulsoup4 for the Lucky Wheel experience…")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
    from bs4 import BeautifulSoup  # type: ignore  # noqa: E402

DEFAULT_SCRAPE_URL = "https://www.beatlottery.co.uk/euromillions/draw-history"
MAIN_POOL = list(range(1, 51))
STAR_POOL = list(range(1, 13))

SAMPLE_DRAWS: List[Dict[str, Any]] = [
    {"date": "2025-11-21", "numbers": [17, 19, 29, 35, 48], "lucky": [5, 9], "jackpot": "£131,464,184"},
    {"date": "2025-11-18", "numbers": [2, 4, 15, 21, 48], "lucky": [6, 12], "jackpot": "£118,491,408"},
    {"date": "2025-11-14", "numbers": [9, 26, 27, 45, 48], "lucky": [8, 9], "jackpot": "£108,302,730"},
    {"date": "2025-11-11", "numbers": [4, 22, 32, 36, 47], "lucky": [2, 10], "jackpot": "£95,492,878"},
    {"date": "2025-11-07", "numbers": [11, 21, 39, 40, 43], "lucky": [2, 8], "jackpot": "Rollover"},
]

CSS = """
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Arial',sans-serif; background:linear-gradient(135deg,#667eea 0%,#764ba2 100%); }
.container { max-width:1400px; margin:0 auto; background:rgba(255,255,255,0.95); border-radius:20px; padding:30px; box-shadow:0 20px 40px rgba(0,0,0,0.1); }
.header { text-align:center; margin-bottom:30px; }
.header h1 { color:#764ba2; font-size:3em; margin-bottom:10px; text-shadow:2px 2px 4px rgba(0,0,0,0.1); }
.scraping-section { background:#e8f4f8; border-radius:18px; padding:20px; border:2px solid #b8d4e3; margin-bottom:25px; }
.scraping-section h3 { color:#2c5282; margin-bottom:10px; }
.url-input { width:100%; padding:12px; border:2px solid #b8d4e3; border-radius:8px; font-size:16px; margin-bottom:12px; }
.scraped-data { max-height:320px; overflow-y:auto; background:#fff; border-radius:12px; padding:15px; border:1px solid #e1e4eb; margin-top:15px; }
.draw-entry { display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #eee; font-family:monospace; }
.draw-date { font-weight:bold; color:#2c5282; min-width:110px; }
.draw-numbers { display:flex; gap:8px; flex-wrap:wrap; }
.number-ball-small { width:30px; height:30px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:bold; color:#fff; }
.main-grid { display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:30px; }
.panel { background:#f8f9fa; border-radius:18px; padding:20px; box-shadow:0 5px 15px rgba(0,0,0,0.08); }
.panel h2 { color:#495057; margin-bottom:15px; }
.btn { background:linear-gradient(135deg,#667eea 0%,#764ba2 100%); color:#fff; border:none; padding:12px 24px; border-radius:8px; font-size:16px; font-weight:600; cursor:pointer; margin:5px; box-shadow:0 5px 15px rgba(0,0,0,0.15); }
.btn-success { background:linear-gradient(135deg,#28a745,#20c997); }
.btn-warning { background:linear-gradient(135deg,#ffc107,#fd7e14); color:#212529; }
.btn:hover { transform:translateY(-2px); box-shadow:0 8px 20px rgba(0,0,0,0.2); }
.lottery-grid { display:grid; grid-template-columns:repeat(10,1fr); gap:10px; margin:15px 0; }
.number-ball { width:48px; height:48px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:18px; cursor:pointer; border:3px solid transparent; transition:transform 0.2s; background:#e2e6ff; }
.number-ball:hover { transform:scale(1.05); }
.number-ball.selected { background:#764ba2!important; color:#fff; border-color:#5a3a8a; }
.frequency-bar { display:flex; align-items:center; margin-bottom:8px; }
.frequency-label { width:30px; font-weight:bold; color:#495057; }
.frequency-progress { flex:1; height:18px; background:#e9ecef; border-radius:10px; margin:0 10px; overflow:hidden; }
.frequency-fill { height:100%; background:linear-gradient(90deg,#667eea,#764ba2); }
.frequency-count { width:40px; text-align:right; font-size:12px; color:#6c757d; }
.prediction-set { background:#fff; border-radius:12px; padding:15px; box-shadow:0 5px 15px rgba(0,0,0,0.08); margin-bottom:15px; }
.number-display { display:flex; gap:10px; flex-wrap:wrap; align-items:center; }
.mini-ball { width:35px; height:35px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:14px; background:#e9ecef; }
.mini-ball.predicted { background:#ffc107; color:#212529; }
.mini-ball.correct { background:#28a745; color:#fff; }
.probability-badge { background:#ede7ff; color:#4b3bc2; padding:6px 12px; border-radius:999px; font-size:0.85rem; }
.stats-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:15px; margin-top:20px; }
.stat-card { background:#fff; border-radius:12px; padding:18px; text-align:center; box-shadow:0 5px 15px rgba(0,0,0,0.08); }
.stat-value { font-size:2rem; color:#764ba2; font-weight:700; }
.lottery-wheel-container { text-align:center; margin:30px 0; position:relative; }
.lottery-wheel { width:300px; height:300px; border-radius:50%; background:linear-gradient(45deg,#ffd700,#ffed4e,#ffd700,#ffed4e); border:15px solid #b8860b; margin:0 auto; position:relative; box-shadow:0 0 50px rgba(255,215,0,0.5); }
.lottery-wheel.spinning { animation:spinWheel 3s cubic-bezier(0.17,0.67,0.83,0.67); }
@keyframes spinWheel { from{transform:rotate(0deg);} to{transform:rotate(1800deg);} }
.wheel-center { position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:80px; height:80px; border-radius:50%; background:radial-gradient(circle,#8b4513,#a0522d); border:5px solid #654321; }
.wheel-pointer { position:absolute; top:-30px; left:50%; transform:translateX(-50%); width:0; height:0; border-left:20px solid transparent; border-right:20px solid transparent; border-top:40px solid #dc143c; }
.results-box { background:linear-gradient(135deg,#2c3e50,#34495e); border-radius:15px; padding:30px; margin:30px 0; box-shadow:0 10px 30px rgba(0,0,0,0.3); text-align:center; color:#ecf0f1; }
.results-numbers { display:flex; gap:15px; flex-wrap:wrap; justify-content:center; align-items:center; }
.result-ball { width:60px; height:60px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:20px; font-weight:bold; color:#fff; border:3px solid #fff; box-shadow:0 4px 15px rgba(0,0,0,0.3); animation:resultBallAppear 0.5s ease-out; }
.result-ball.star { background:linear-gradient(135deg,#ffd700,#ffed4e); color:#333; }
@keyframes resultBallAppear { 0%{transform:scale(0) rotate(180deg); opacity:0;} 50%{transform:scale(1.2) rotate(90deg); opacity:0.8;} 100%{transform:scale(1) rotate(0); opacity:1;} }
@media(max-width:768px){ .main-grid{grid-template-columns:1fr;} .lottery-grid{grid-template-columns:repeat(5,1fr);} .lottery-wheel{width:250px;height:250px;} }
</style>
"""


def init_state() -> None:
    ss = st.session_state
    ss.setdefault("lw_data", None)
    ss.setdefault("lw_synthetic", None)
    ss.setdefault("lw_predictions", None)
    ss.setdefault("lw_eval_rows", None)
    ss.setdefault("lw_status", "Load live EuroMillions data or samples to get started.")
    ss.setdefault("lw_main_selected", [])
    ss.setdefault("lw_star_selected", [])
    ss.setdefault("lw_stats", {"total": 0, "correct": 0, "accuracy": 0, "history": 0})
    ss.setdefault("lw_scrape_url", DEFAULT_SCRAPE_URL)
    ss.setdefault("lw_scrape_limit", 120)
    ss.setdefault("lw_wheel_main", [])
    ss.setdefault("lw_wheel_lucky", [])
    ss.setdefault("lw_wheel_spinning", False)

def parse_draw_date(text: str) -> datetime | None:
    for fmt in ("%d %b %Y", "%d %B %Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(text.strip(), fmt)
        except ValueError:
            continue
    return None


def scrape_draw_history(url: str, limit: int) -> pd.DataFrame:
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.select_one("div.table-responsive table")
    if not table:
        raise ValueError("Could not locate draw table at the supplied URL.")

    rows: List[Dict[str, Any]] = []
    for tr in table.select("tr"):
        cells = tr.find_all("td")
        if len(cells) < 4:
            continue
        numbers_box = tr.select_one("div.results-ball-box")
        if not numbers_box:
            continue
        main = [int(span.text) for span in numbers_box.select("span.ball-euromillions") if span.text.isdigit()]
        lucky = [int(span.text) for span in numbers_box.select("span.ball-euromillions-lucky-star") if span.text.isdigit()]
        if len(main) < 5:
            continue
        date_raw = cells[0].get_text(strip=True)
        jackpot = cells[4].get_text(strip=True) if len(cells) > 4 else ""
        rows.append(
            {
                "draw_date": parse_draw_date(date_raw),
                "draw_date_raw": date_raw,
                "weekday": cells[2].get_text(strip=True) if len(cells) > 2 else "",
                "numbers": main[:5],
                "lucky": lucky[:2],
                "jackpot": jackpot,
            }
        )
        if len(rows) >= limit:
            break
    if not rows:
        raise ValueError("No draw rows parsed from the page.")
    return pd.DataFrame(rows)


def load_sample_dataframe() -> pd.DataFrame:
    df = pd.DataFrame(SAMPLE_DRAWS)
    df["draw_date"] = pd.to_datetime(df["date"])
    df["draw_date_raw"] = df["date"]
    return df.drop(columns=["date"])


def compute_frequency(df: pd.DataFrame) -> Tuple[Dict[int, int], Dict[int, int]]:
    main_freq = {n: 0 for n in MAIN_POOL}
    star_freq = {n: 0 for n in STAR_POOL}
    for _, row in df.iterrows():
        for n in row["numbers"]:
            main_freq[n] += 1
        for s in row["lucky"]:
            star_freq[s] += 1
    return main_freq, star_freq


def generate_synthetic_draws(df: pd.DataFrame, count: int = 60) -> pd.DataFrame:
    rng = np.random.default_rng(123)
    synthetic = []
    for idx in range(count):
        main = sorted(rng.choice(MAIN_POOL, size=5, replace=False))
        lucky = sorted(rng.choice(STAR_POOL, size=2, replace=False))
        synthetic.append(
            {
                "draw_date": None,
                "draw_date_raw": f"Synthetic-{idx+1}",
                "weekday": "AI",
                "numbers": main,
                "lucky": lucky,
                "jackpot": f"£{rng.integers(20, 120)}m",
            }
        )
    return pd.DataFrame(synthetic)


def generate_prediction_sets(df: pd.DataFrame, count: int = 10) -> List[Dict[str, Any]]:
    if df is None or df.empty:
        raise ValueError("No draws available for prediction.")
    main_freq, star_freq = compute_frequency(df)
    rarity_main = sorted(main_freq.items(), key=lambda kv: kv[1])
    rarity_star = sorted(star_freq.items(), key=lambda kv: kv[1])
    rng = random.Random(2025)

    predictions: List[Dict[str, Any]] = []
    last_draw = df.iloc[0]
    predictions.append(
        {
            "prediction_id": 1,
            "numbers": last_draw["numbers"],
            "lucky": last_draw["lucky"],
            "improbability": 1.0,
            "confidence": 3.0,
            "label": "Exact mirror of last draw",
        }
    )

    for idx in range(1, count + 1):
        main_window = max(6, int(len(rarity_main) * max(0.15, 1 - idx / (count + 2))))
        star_window = max(4, int(len(rarity_star) * max(0.25, 1 - idx / (count + 2))))
        main_pool = [n for n, _ in rarity_main[:main_window]]
        star_pool = [n for n, _ in rarity_star[:star_window]]
        numbers = sorted(rng.sample(main_pool, 5))
        lucky = sorted(rng.sample(star_pool, 2))
        score = round(max(0.05, 1 - idx / (count + 2)), 3)
        predictions.append(
            {
                "prediction_id": idx + 1,
                "numbers": numbers,
                "lucky": lucky,
                "improbability": score,
                "confidence": round((1 - score) * 100, 2),
                "label": "Rarest pool" if idx <= 3 else "Mid probability" if idx <= 7 else "Plausible",
            }
        )
    return predictions[:count]


def evaluate_predictions(preds: List[Dict[str, Any]], actual_main: List[int], actual_lucky: List[int]) -> List[Dict[str, Any]]:
    rows = []
    for pred in preds:
        hit_main = len(set(pred["numbers"]) & set(actual_main))
        hit_lucky = len(set(pred["lucky"]) & set(actual_lucky))
        rows.append(
            {
                "prediction": pred["prediction_id"],
                "numbers": pred["numbers"],
                "lucky": pred["lucky"],
                "main_hits": hit_main,
                "lucky_hits": hit_lucky,
                "total": hit_main + hit_lucky,
            }
        )
    return rows
