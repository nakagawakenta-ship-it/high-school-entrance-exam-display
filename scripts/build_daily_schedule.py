"""Build dated daily JSON files from the prepared English/Social banks.
Run this only when refreshing the long-term schedule; the daily workflow itself does not use AI.
"""
import json, random
from datetime import date, timedelta
from pathlib import Path

START = date(2026, 9, 16)
END = date(2027, 2, 15)  # day before the common academic test

english = json.loads(Path("questions/english.json").read_text(encoding="utf-8"))
social = json.loads(Path("questions/social.json").read_text(encoding="utf-8"))

if len(english) < 5 or len(social) < 5:
    raise SystemExit("Need at least 5 English and 5 Social questions in public banks")

out = Path("daily")
out.mkdir(exist_ok=True)
prev_e = set(); prev_s = set()
d = START
while d <= END:
    rng = random.Random(int(d.strftime("%Y%m%d")))
    epool = [q for q in english if q.get("id") not in prev_e] or english[:]
    spool = [q for q in social if q.get("id") not in prev_s] or social[:]
    es = rng.sample(epool, min(5, len(epool)))
    ss = rng.sample(spool, min(5, len(spool)))
    if len(es) < 5: es += rng.sample([q for q in english if q not in es], 5-len(es))
    if len(ss) < 5: ss += rng.sample([q for q in social if q not in ss], 5-len(ss))
    payload = {"date": d.isoformat(), "title": f"高校入試 日替わり問題 {d.isoformat()}", "questions": es + ss}
    (out / f"{d.isoformat()}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    prev_e = {q["id"] for q in es}; prev_s = {q["id"] for q in ss}
    d += timedelta(days=1)
