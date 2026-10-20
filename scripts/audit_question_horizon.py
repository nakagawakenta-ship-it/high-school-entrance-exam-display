import json, glob, re, sys
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher
from datetime import date, timedelta, datetime
from zoneinfo import ZoneInfo

START = date(2026, 10, 14)
END = date(2027, 2, 28)
TODAY_JST = datetime.now(ZoneInfo("Asia/Tokyo")).date()

result = {
    "start": START.isoformat(), "end": END.isoformat(),
    "today_jst": TODAY_JST.isoformat(),
    "days_expected": (END - START).days + 1,
    "days_checked": 0, "questions_checked": 0,
    "daily_source_days": 0, "prepared_source_days": 0,
    "errors": [], "warnings": [],
    "exact_duplicate_groups": [], "duplicates_with_prior_history": [],
    "template_duplicate_groups": [], "near_duplicate_pairs": [],
    "topic_counts": {}
}

def norm(text):
    return re.sub(r"\s+", "", str(text)).casefold()

def item_text(q):
    choices = q.get("choices", [])
    return str(q.get("question", "")) + " [choices] " + " | ".join(map(str, choices)) + " [answer] " + str(q.get("answer", ""))

def template(text):
    s = str(text).casefold()
    s = re.sub(r"\b(mika|ken|yuta|rina|emi|hana|sota|aki|tom|yuki)\b", "<name>", s)
    places = [
        "kamakura","yokohama","hakone","odawara","kyoto","fujisawa","kawasaki","sagamihara","chigasaki",
        "sagamihara","brazil","egypt","australia","india","canada","saudi arabia",
        "相模川","多摩川","酒匂川","鶴見川","境川","早川","金目川","引地川","帷子川","大岡川",
        "太平洋側","日本海側","中央高地","南西諸島","北海道","瀬戸内","新潟平野","高知平野",
        "鹿児島","長野県","沖縄県","青森県","山梨県","静岡県","群馬県","千葉県","愛媛県",
        "熊本県","宮崎県","三重県","広島県","富山平野","鳥取県","福井県","岩手県","和歌山県",
        "栃木県","茨城県","佐賀平野","徳島県","長崎県","奈良県","福岡県","石川県",
        "京浜工業地帯","中京工業地帯","京葉工業地域","北九州工業地域","瀬戸内工業地域","東海地方"
    ]
    for place in sorted(places, key=len, reverse=True):
        s = re.sub(re.escape(place.casefold()), "<place>", s)
    s = re.sub(r"\d+(?:,\d{3})*(?:\.\d+)?", "<n>", s)
    s = re.sub(r"\s+", "", s)
    return s

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

daily_by_date = {}
prior_history = []
for path in sorted(glob.glob("daily/*.json")):
    try:
        data = load_json(path)
        day = date.fromisoformat(data["date"])
        if day < START:
            for q in data.get("questions", []):
                prior_history.append({
                    "date": day.isoformat(),
                    "topic": q.get("topic", "unknown"),
                    "question": q.get("question", "")
                })
        elif START <= day <= END:
            daily_by_date[day] = (path, data)
    except Exception as exc:
        result["errors"].append({"file": path, "error": str(exc)})

prepared_by_date = {}
for path in sorted(glob.glob("prepared/*.json")):
    try:
        data = load_json(path)
        day = date.fromisoformat(data["date"])
        if START <= day <= END:
            prepared_by_date[day] = (path, data)
    except Exception as exc:
        result["errors"].append({"file": path, "error": str(exc)})

selected = []
day = START
while day <= END:
    if day in daily_by_date:
        path, data = daily_by_date[day]
        source = "daily"
        result["daily_source_days"] += 1
    elif day in prepared_by_date:
        path, data = prepared_by_date[day]
        source = "prepared"
        result["prepared_source_days"] += 1
    else:
        result["errors"].append({"date": day.isoformat(), "error": "missing both daily and prepared file"})
        day += timedelta(days=1)
        continue

    if data.get("date") != day.isoformat():
        result["errors"].append({"file": path, "error": f"date field {data.get('date')} does not match filename/day {day.isoformat()}"})
    qs = data.get("questions", [])
    if len(qs) != 10:
        result["errors"].append({"date": day.isoformat(), "error": f"expected 10 questions, got {len(qs)}"})
    if sum(q.get("subject") == "english" for q in qs) != 5:
        result["errors"].append({"date": day.isoformat(), "error": "English count is not 5"})
    if sum(q.get("subject") == "social" for q in qs) != 5:
        result["errors"].append({"date": day.isoformat(), "error": "Social count is not 5"})

    day_questions = set()
    for q in qs:
        question = str(q.get("question", ""))
        choices = q.get("choices", [])
        answer = q.get("answer")
        topic = q.get("topic", "unknown")
        if len(choices) != 4 or len(set(map(str, choices))) != 4:
            result["errors"].append({"date": day.isoformat(), "question": question, "error": "choices must be four unique options"})
        if answer not in choices:
            result["errors"].append({"date": day.isoformat(), "question": question, "error": "answer is not among choices"})
        qkey = norm(question)
        if qkey in day_questions:
            result["errors"].append({"date": day.isoformat(), "question": question, "error": "duplicate question within the same day"})
        day_questions.add(qkey)

        # Semantic checks are strict for today's display and future prepared questions.
        strict_semantics = day >= TODAY_JST or source == "prepared"
        if strict_semantics:
            if re.search(r"\ba\s+(engineer|artist|actor|architect|astronaut)\b", question, re.I):
                result["errors"].append({"date": day.isoformat(), "question": question, "error": "article should be 'an' before this vowel-sound noun"})
            if topic == "dialogue" and re.search(r"how can i get from|how do i get to|the way from", question, re.I) and re.search(r"turn left|turn right|go straight", str(answer), re.I):
                result["errors"].append({"date": day.isoformat(), "question": question, "error": "route answer is not uniquely determined without a map"})
            if topic == "geography" and "という気候の特徴がみられる地域は" in question:
                regions = {"太平洋側","日本海側","瀬戸内","中央高地","北海道","南西諸島"}
                if answer not in regions:
                    result["errors"].append({"date": day.isoformat(), "question": question, "error": "asks for a region but answer is a climate feature"})
            if topic == "disaster":
                if any(x in question for x in ("急傾斜地","山間部")) and any(x in question for x in ("洪水","洪水・浸水","洪水・高潮")):
                    result["errors"].append({"date": day.isoformat(), "question": question, "error": "slope/mountain setting is mismatched with flood hazard in this template"})
                if any(x in question for x in ("相模川沿い","酒匂川沿い","境川沿い","鶴見川沿い","多摩川沿い")) and "土砂災害" in question:
                    result["errors"].append({"date": day.isoformat(), "question": question, "error": "river-side setting is mismatched with this generated landslide template"})
            if topic == "history_person" and answer == "鎌倉幕府を開いた" and any("1192年に最初の幕府を開いた" in str(c) for c in choices):
                result["errors"].append({"date": day.isoformat(), "question": question, "error": "a second choice may also describe the answer"})
        else:
            if re.search(r"\ba\s+(engineer|artist|actor|architect|astronaut)\b", question, re.I):
                result["warnings"].append({"date": day.isoformat(), "question": question, "warning": "historical displayed item contains a likely article error"})
        result["topic_counts"][topic] = result["topic_counts"].get(topic, 0) + 1
        selected.append({
            "date": day.isoformat(), "source": source, "topic": topic,
            "subject": q.get("subject"), "question": question,
            "choices": list(map(str, choices)), "answer": str(answer)
        })
    result["days_checked"] += 1
    result["questions_checked"] += len(qs)
    day += timedelta(days=1)

# Exact duplicate questions across dates, independent of choice order.
by_exact = defaultdict(list)
by_template = defaultdict(list)
for q in selected:
    by_exact[norm(q["question"])].append({k:q[k] for k in ("date","topic","question","source")})
    signature = template(item_text(q))
    by_template[(q["topic"], signature)].append({k:q[k] for k in ("date","topic","question","choices","answer","source")})

result["exact_duplicate_groups"] = [v for v in by_exact.values() if len(v) > 1]
result["template_duplicate_groups"] = [v for v in by_template.values() if len(v) > 1]
result["template_duplicate_group_count"] = len(result["template_duplicate_groups"])
result["exact_duplicate_group_count"] = len(result["exact_duplicate_groups"])

# Compare each selected item against daily history strictly before the requested window.
history_keys = defaultdict(list)
for q in prior_history:
    history_keys[norm(q["question"])].append(q)
for q in selected:
    prior = history_keys.get(norm(q["question"]), [])
    if prior:
        result["duplicates_with_prior_history"].append({"selected": q, "prior_daily_history": prior})
result["prior_daily_history_questions_checked"] = len(prior_history)

# Near-duplicate review compares the whole item (question + choices + answer), not just the generic stem.
near = []
for i, a in enumerate(selected):
    ta = template(item_text(a))
    for b in selected[i + 1:]:
        if a["date"] == b["date"] or a["topic"] != b["topic"]:
            continue
        tb = template(item_text(b))
        ratio = SequenceMatcher(None, ta, tb).ratio()
        if ratio >= 0.90:
            near.append({
                "similarity": round(ratio, 3), "topic": a["topic"],
                "a": {"date": a["date"], "question": a["question"], "choices": a["choices"], "answer": a["answer"]},
                "b": {"date": b["date"], "question": b["question"], "choices": b["choices"], "answer": b["answer"]}
            })
near.sort(key=lambda x: x["similarity"], reverse=True)
result["near_duplicate_pair_count"] = len(near)
result["near_duplicate_pairs"] = near[:500]

if result["exact_duplicate_groups"]:
    result["errors"].append({"error": f"{len(result['exact_duplicate_groups'])} exact duplicate question groups found across the requested horizon"})
if result["duplicates_with_prior_history"]:
    result["errors"].append({"error": f"{len(result['duplicates_with_prior_history'])} exact question duplicates found against daily history before the requested horizon"})
if result["template_duplicate_groups"]:
    result["warnings"].append({"warning": f"{len(result['template_duplicate_groups'])} normalized item-template groups repeat across dates; review near-duplicates before declaring full quality complete"})
if result["near_duplicate_pair_count"]:
    result["warnings"].append({"warning": f"{result['near_duplicate_pair_count']} high-similarity item pairs need review; up to 500 examples are included"})

result["quality_status"] = "fail" if result["errors"] else ("needs_review" if result["warnings"] else "pass")
Path("question_quality_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
if result["errors"]:
    sys.exit(1)
