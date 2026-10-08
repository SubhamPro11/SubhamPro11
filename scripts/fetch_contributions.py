#!/usr/bin/env python3
"""Scrape the public contribution calendar (no token) and write data/contributions.json."""
import datetime, json, os, re, sys
import requests
from bs4 import BeautifulSoup
from theme import USER

URL = f"https://github.com/users/{USER}/contributions"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "contributions.json")


def fetch_days():
    r = requests.get(URL, headers={"User-Agent": "profile-readme-bot/1.0"}, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    cells = soup.select("td.ContributionCalendar-day")
    if not cells:
        sys.exit("no calendar cells found - GitHub markup may have changed")
    days = []
    for td in cells:
        date = td.get("data-date")
        if not date:
            continue
        tip = soup.find("tool-tip", attrs={"for": td.get("id")}) if td.get("id") else None
        text = tip.get_text(strip=True) if tip else ""
        m = re.match(r"(\d+)", text)
        count = 0 if (not m or re.search("no contributions", text, re.I)) else int(m.group(1))
        days.append({"date": date, "count": count, "level": int(td.get("data-level") or 0)})
    days.sort(key=lambda d: d["date"])
    return days


def streaks(days):
    # current: today may still be empty, so don't let it break the streak
    i = len(days) - 1
    if days[i]["count"] == 0:
        i -= 1
    end = i
    while i >= 0 and days[i]["count"] > 0:
        i -= 1
    cur = {"length": end - i, "start": days[i + 1]["date"] if end > i else None,
           "end": days[end]["date"] if end > i else None}
    best = {"length": 0, "start": None, "end": None}
    run, s = 0, 0
    for k, d in enumerate(days):
        if d["count"] > 0:
            if run == 0:
                s = k
            run += 1
            if run > best["length"]:
                best = {"length": run, "start": days[s]["date"], "end": d["date"]}
        else:
            run = 0
    return cur, best


def build(days):
    total = sum(d["count"] for d in days)
    active = sum(1 for d in days if d["count"])
    top = max(days, key=lambda d: d["count"])
    cur, lng = streaks(days)
    monthly = {}
    for d in days:
        monthly[d["date"][:7]] = monthly.get(d["date"][:7], 0) + d["count"]
    return {
        "username": USER,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]},
        "total_contributions": total, "active_days": active,
        "avg_per_active_day": round(total / active, 1) if active else 0,
        "current_streak": cur, "longest_streak": lng,
        "best_day": {"date": top["date"], "count": top["count"]},
        "monthly": [{"month": k, "total": v} for k, v in sorted(monthly.items())],
        "days": days,
    }


if __name__ == "__main__":
    data = build(fetch_days())
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(data, open(OUT, "w"), indent=2)
    print(f"{USER}: {data['total_contributions']} contributions, "
          f"current streak {data['current_streak']['length']}, longest {data['longest_streak']['length']}")
