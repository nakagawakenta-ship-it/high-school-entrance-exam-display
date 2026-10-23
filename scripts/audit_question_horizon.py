import glob
import json
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from difflib import SequenceMatcher
from pathlib import Path
from zoneinfo import ZoneInfo

START = date(2026, 10, 14)
END = date(2027, 2, 28)
TODAY_JST = datetime.now(ZoneInfo("Asia/Tokyo")).date()

result = {
    "start": START.isoformat(),
    "end": END.isoformat(),
    "today_jst": TODAY_JST.isoformat(),
    "days_checked": 0,
    "questions_checked": 0,
    "prepared_future_days_checked": 0,
    "errors": [],
    "content_warnings": [],
    "exact_duplicate_groups": [],
    "template_duplicate_groups": [],
    "near_duplicate_pairs": [],
    "history_duplicate_groups": [],
    "recent_template_repeat_groups": [],
    "topic_counts": {},
    "source_counts": {"daily": 0, "prepared": 0},
}

def norm(text):
    text = str(text).casefold()
    text = re.sub(r"\d+(?:,\d{3})*(?:\.\d+)?", "<n>", text)
    text = re.sub(r"\b(mika|ken|yuta|rina|emi|hana|sota|aki|riku|sara|aya)\b", "<name>", text)
    text = re.sub(r"\b(kamakura|yokohama|hakone|odawara|kyoto|fujisawa|kawasaki|sagamihara|chigasaki)\b", "<city>", text)
    return re.sub(r"\s+", "", text)

def exact_norm(text):
    return re.sub(r"\s+", "", str(text)).casefold()

def template(text):
    s = str(text).casefold()
    s = re.sub(r"\b(mika|ken|yuta|rina|emi|hana|sota|aki|riku|sara|aya)\b", "<name>", s)
    s = re.sub(r"\b(kamakura|yokohama|hakone|odawara|kyoto|fujisawa|kawasaki|sagamihara|chigasaki)\b", "<city>", s)
    s = re.sub(r"\d+(?:,\d{3})*(?:\.\d+)?", "<n>", s)
    s = re.sub(r"\s+", "", s)
    return s

def load_files(pattern):
    items = {}
    for filename in sorted(glob.glob(pattern)):
        path = Path(filename)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            day = date.fromisoformat(data.get("date") or path.stem)
            if day in items:
                result["errors"].append({"file": filename, "error": f"duplicate date file {day.isoformat()}"})
            items[day] = {"path": filename, "data": data}
        except Exception as exc:
            result["errors"].append({"file": filename, "error": str(exc)})
    return items

daily_by_date = load_files("daily/*.json")
prepared_by_date = load_files("prepared/*.json")

# Past displayed daily files are the record of what was shown. For today and earlier,
# prefer daily/*.json. For future dates, require and inspect prepared/*.json.
canonical = {}
day = START
while day <= END:
    if day <= TODAY_JST:
        source = daily_by_date.get(day) or prepared_by_date.get(day)
        source_kind = "daily" if day in daily_by_date else "prepared"
    else:
        source = prepared_by_date.get(day)
        source_kind = "prepared"
        if source is None:
            result["errors"].append({"date": day.isoformat(), "error": "missing future prepared file"})
            source = daily_by_date.get(day)
            source_kind = "daily"
    if source is None:
        result["errors"].append({"date": day.isoformat(), "error": "no daily or prepared file"})
    else:
        canonical[day] = {"path": source["path"], "data": source["data"], "source": source_kind}
        result["source_counts"][source_kind] += 1
    day += timedelta(days=1)

expected_days = (END - START).days + 1
if len(canonical) != expected_days:
    result["errors"].append({"error": f"expected {expected_days} dates, found {len(canonical)}"})

expected_future = max(0, (END - max(START, TODAY_JST + timedelta(days=1))).days + 1)
result["prepared_future_days_checked"] = sum(
    1 for d in prepared_by_date if max(START, TODAY_JST + timedelta(days=1)) <= d <= END
)
if result["prepared_future_days_checked"] != expected_future:
    result["errors"].append({
        "error": f"expected {expected_future} future prepared files, found {result['prepared_future_days_checked']}"
    })

# Only dates before the requested horizon are historical duplicate references.
history = []
history_keys = defaultdict(list)
for d, item in daily_by_date.items():
    if d >= START:
        continue
    for q in item["data"].get("questions", []):
        entry = {"date": d.isoformat(), "topic": q.get("topic", "unknown"), "question": q.get("question", "")}
        history.append(entry)
        history_keys[exact_norm(entry["question"])].append(entry)

all_questions = []
ids = set()
for d in sorted(canonical):
    item = canonical[d]
    data = item["data"]
    qs = data.get("questions", [])
    result["days_checked"] += 1
    result["questions_checked"] += len(qs)
    if len(qs) != 10:
        result["errors"].append({"date": d.isoformat(), "error": f"expected 10 questions, got {len(qs)}"})
    if sum(q.get("subject") == "english" for q in qs) != 5:
        result["errors"].append({"date": d.isoformat(), "error": "English count is not 5"})
    if sum(q.get("subject") == "social" for q in qs) != 5:
        result["errors"].append({"date": d.isoformat(), "error": "Social count is not 5"})

    seen_on_day = defaultdict(list)
    for q in qs:
        subject = q.get("subject")
        question = str(q.get("question", ""))
        choices = q.get("choices", [])
        answer = q.get("answer")
        topic = q.get("topic", "unknown")
        qid = q.get("id")
        if subject not in ("english", "social"):
            result["errors"].append({"date": d.isoformat(), "question": question, "error": f"invalid subject {subject!r}"})
        if not question.strip():
            result["errors"].append({"date": d.isoformat(), "error": "empty question text"})
        if qid:
            if qid in ids:
                result["errors"].append({"date": d.isoformat(), "question_id": qid, "error": "duplicate question id"})
            ids.add(qid)
        if not isinstance(choices, list) or len(choices) != 4 or len(set(map(str, choices))) != 4:
            result["errors"].append({"date": d.isoformat(), "question": question, "error": "choices must be four unique options"})
        if not isinstance(choices, list) or answer not in choices:
            result["errors"].append({"date": d.isoformat(), "question": question, "error": "answer is not among choices"})

        result["topic_counts"][topic] = result["topic_counts"].get(topic, 0) + 1
        entry = {
            "date": d.isoformat(), "topic": topic, "subject": subject,
            "question": question, "choices": choices, "answer": answer,
            "source": item["source"]
        }
        all_questions.append(entry)
        seen_on_day[exact_norm(question)].append(entry)

        if subject == "english" and re.search(r"\ba\s+(?:engineer|artist)\b", question, re.I):
            result["content_warnings"].append({
                "date": d.isoformat(), "question": question,
                "warning": "article before a vowel sound should be checked (e.g. an engineer/an artist)"
            })
        if subject == "english" and re.search(r"(how can .*get to|how do i get to|way from)", question, re.I):
            if re.search(r"(turn left|turn right|go straight)", str(answer), re.I) and not re.search(r"(map|street|corner|traffic light|on your left|on your right|opposite)", question, re.I):
                result["content_warnings"].append({
                    "date": d.isoformat(), "question": question,
                    "warning": "route direction is not supported by a map or route clue"
                })
        if subject == "social":
            if re.search(r"(急傾斜地|山間部)", question) and re.search(r"(洪水|浸水|高潮)", str(answer)):
                result["content_warnings"].append({
                    "date": d.isoformat(), "question": question,
                    "warning": "disaster type may not match steep-slope/mountain setting"
                })
            if re.search(r"(川沿い|河川|川の水位|河口)", question) and re.search(r"土砂災害警戒区域", str(answer)):
                result["content_warnings"].append({
                    "date": d.isoformat(), "question": question,
                    "warning": "disaster type may not match river/flood setting"
                })
            if re.search(r"気候の特徴がみられる地域|特徴がみられる地域は", question) and re.search(r"(雪|雨|温暖|乾燥|降水量|台風)", str(answer)):
                result["content_warnings"].append({
                    "date": d.isoformat(), "question": question,
                    "warning": "question asks for a region but answer appears to be a climate feature"
                })

# Exact duplicates within the horizon; same-date daily/prepared copies are not both counted.
by_exact = defaultdict(list)
by_template = defaultdict(list)
for q in all_questions:
    by_exact[exact_norm(q["question"])].append({k: q[k] for k in ("date", "subject", "topic", "question", "source")})
    by_template[(q["subject"], q["topic"], template(q["question"]))].append(
        {k: q[k] for k in ("date", "subject", "topic", "question", "source")}
    )

result["exact_duplicate_groups"] = [v for v in by_exact.values() if len(v) > 1]
for q in all_questions:
    prior = history_keys.get(exact_norm(q["question"]), [])
    if prior:
        result["history_duplicate_groups"].append({"question": q, "prior_daily_history": prior})

result["template_duplicate_groups"] = [
    v for v in by_template.values() if len({x["date"] for x in v}) > 1
]

# The future bank must not repeat a normalized template within six days.
recent_by_template = defaultdict(list)
for q in all_questions:
    if q["source"] == "prepared" and q["date"] > TODAY_JST.isoformat():
        recent_by_template[(q["subject"], q["topic"], template(q["question"]))].append(
            {k: q[k] for k in ("date", "subject", "topic", "question")}
        )
for entries in recent_by_template.values():
    entries.sort(key=lambda x: x["date"])
    for i, a in enumerate(entries):
        da = date.fromisoformat(a["date"])
        for b in entries[i + 1:]:
            db = date.fromisoformat(b["date"])
            if (db - da).days <= 6:
                result["recent_template_repeat_groups"].append({"a": a, "b": b})

# Similarity candidates are review warnings, not automatic failures; common skills can share words.
groups = defaultdict(list)
for q in all_questions:
    groups[(q["subject"], q["topic"])].append(q)
for _, qs in groups.items():
    for i, a in enumerate(qs):
        for b in qs[i + 1:]:
            if a["date"] == b["date"]:
                continue
            ratio = SequenceMatcher(None, exact_norm(a["question"]), exact_norm(b["question"])).ratio()
            if ratio >= 0.88:
                result["near_duplicate_pairs"].append({
                    "similarity": round(ratio, 3), "subject": a["subject"], "topic": a["topic"],
                    "a": {"date": a["date"], "question": a["question"]},
                    "b": {"date": b["date"], "question": b["question"]}
                })
result["near_duplicate_pairs"].sort(key=lambda x: x["similarity"], reverse=True)
result["template_duplicate_group_count"] = len(result["template_duplicate_groups"])
result["near_duplicate_pair_count"] = len(result["near_duplicate_pairs"])
result["exact_duplicate_group_count"] = len(result["exact_duplicate_groups"])
result["history_duplicate_group_count"] = len(result["history_duplicate_groups"])
result["recent_template_repeat_count"] = len(result["recent_template_repeat_groups"])
result["content_warning_count"] = len(result["content_warnings"])
result["daily_history_questions_checked"] = len(history)
result["content_warnings"] = result["content_warnings"][:300]
result["near_duplicate_pairs"] = result["near_duplicate_pairs"][:1000]
result["template_duplicate_groups"] = result["template_duplicate_groups"][:300]

Path("question_quality_audit.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(json.dumps({
    "start": result["start"], "end": result["end"],
    "days_checked": result["days_checked"], "questions_checked": result["questions_checked"],
    "prepared_future_days_checked": result["prepared_future_days_checked"],
    "exact_duplicate_group_count": result["exact_duplicate_group_count"],
    "history_duplicate_group_count": result["history_duplicate_group_count"],
    "recent_template_repeat_count": result["recent_template_repeat_count"],
    "template_duplicate_group_count": result["template_duplicate_group_count"],
    "near_duplicate_pair_count": result["near_duplicate_pair_count"],
    "content_warning_count": result["content_warning_count"],
    "errors": result["errors"][:20]
}, ensure_ascii=False, indent=2))
if result["errors"] or result["exact_duplicate_groups"] or result["history_duplicate_groups"]:
    sys.exit(1)

# Re-run the audit after the 2026-10-24 validated horizon regeneration.

# Re-audit after repairing archived daily-question warnings.

# Re-audit after de-duplicating the corrected October 15 archive entry.
