import json, glob, re, sys
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher
from datetime import date

START = date(2026, 10, 20)
END = date(2027, 2, 28)
result = {
    "start": START.isoformat(), "end": END.isoformat(),
    "days_checked": 0, "questions_checked": 0, "errors": [],
    "exact_duplicate_groups": [], "template_duplicate_groups": [],
    "near_duplicate_pairs": [], "topic_counts": {}
}

def norm(text):
    return re.sub(r"\s+", "", str(text)).casefold()

def template(text):
    s = str(text).casefold()
    s = re.sub(r"\b(mika|ken|yuta|rina|emi|hana|sota|aki)\b", "<name>", s)
    s = re.sub(r"\b(kamakura|yokohama|hakone|odawara|kyoto|fujisawa|kawasaki|sagamihara|chigasaki)\b", "<city>", s)
    s = re.sub(r"\d+(?:,\d{3})*(?:\.\d+)?", "<n>", s)
    s = re.sub(r"\s+", "", s)
    return s

history_questions = []
history_keys = defaultdict(list)
for path in sorted(glob.glob("daily/*.json")):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        for q in data.get("questions", []):
            item = {"date": data.get("date", ""), "topic": q.get("topic", "unknown"), "question": q.get("question", "")}
            history_questions.append(item)
            history_keys[norm(item["question"])].append(item)
    except Exception as exc:
        result["errors"].append({"file": path, "error": str(exc)})

all_questions = []
for path in sorted(glob.glob("prepared/*.json")):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        day = date.fromisoformat(data["date"])
        if not (START <= day <= END):
            continue
        qs = data["questions"]
        if len(qs) != 10:
            result["errors"].append({"date": data.get("date"), "error": f"expected 10 questions, got {len(qs)}"})
        if sum(q.get("subject") == "english" for q in qs) != 5:
            result["errors"].append({"date": data.get("date"), "error": "English count is not 5"})
        if sum(q.get("subject") == "social" for q in qs) != 5:
            result["errors"].append({"date": data.get("date"), "error": "Social count is not 5"})
        result["days_checked"] += 1
        result["questions_checked"] += len(qs)
        for q in qs:
            if len(q.get("choices", [])) != 4 or len(set(q.get("choices", []))) != 4:
                result["errors"].append({"date": data.get("date"), "question": q.get("question"), "error": "choices must be four unique options"})
            if q.get("answer") not in q.get("choices", []):
                result["errors"].append({"date": data.get("date"), "question": q.get("question"), "error": "answer is not among choices"})
            topic = q.get("topic", "unknown")
            result["topic_counts"][topic] = result["topic_counts"].get(topic, 0) + 1
            all_questions.append({"date": data["date"], "topic": topic, "subject": q.get("subject"), "question": q.get("question", "")})
    except Exception as exc:
        result["errors"].append({"file": path, "error": str(exc)})

expected_days = (END - START).days + 1
if result["days_checked"] != expected_days:
    result["errors"].append({"error": f"expected {expected_days} prepared dates, found {result['days_checked']}"})

by_exact = defaultdict(list)
by_template = defaultdict(list)
for q in all_questions:
    by_exact[norm(q["question"])].append({k: q[k] for k in ("date", "topic", "question")})
    by_template[(q["topic"], template(q["question"]))].append({k: q[k] for k in ("date", "topic", "question")})
result["exact_duplicate_groups"] = [v for v in by_exact.values() if len(v) > 1]
result["duplicates_with_daily_history"] = []
for q in all_questions:
    prior = history_keys.get(norm(q["question"]), [])
    if prior:
        result["duplicates_with_daily_history"].append({"prepared": q, "daily_history": prior})
result["template_duplicate_groups"] = [v for v in by_template.values() if len(v) > 1]
result["daily_history_questions_checked"] = len(history_questions)

# Report high textual similarity between different dates within the same topic after checking all daily-history collisions.
# This is a review signal, not an automatic failure: some skill families naturally share vocabulary.
seen_pairs = set()
for i, a in enumerate(all_questions):
    for b in all_questions[i + 1:]:
        if a["date"] == b["date"] or a["topic"] != b["topic"]:
            continue
        pair = tuple(sorted((a["date"], b["date"], a["question"], b["question"])))
        if pair in seen_pairs:
            continue
        ratio = SequenceMatcher(None, norm(a["question"]), norm(b["question"])).ratio()
        if ratio >= 0.88:
            seen_pairs.add(pair)
            result["near_duplicate_pairs"].append({
                "similarity": round(ratio, 3),
                "topic": a["topic"],
                "a": {"date": a["date"], "question": a["question"]},
                "b": {"date": b["date"], "question": b["question"]}
            })
result["near_duplicate_pairs"].sort(key=lambda x: x["similarity"], reverse=True)
result["near_duplicate_pair_count"] = len(result["near_duplicate_pairs"])
result["template_duplicate_group_count"] = len(result["template_duplicate_groups"])
result["exact_duplicate_group_count"] = len(result["exact_duplicate_groups"])

Path("question_quality_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
if result["errors"] or result["exact_duplicate_groups"] or result["duplicates_with_daily_history"]:
    sys.exit(1)
