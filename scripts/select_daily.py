from datetime import datetime, timezone, timedelta
import json
from pathlib import Path

JST = timezone(timedelta(hours=9))
TODAY = datetime.now(JST).date().isoformat()

english = json.loads(Path('questions/english.json').read_text(encoding='utf-8'))
social = json.loads(Path('questions/social.json').read_text(encoding='utf-8'))

history_path = Path('history.json')
history = json.loads(history_path.read_text(encoding='utf-8')) if history_path.exists() else []
recent_ids = {qid for day in history[-3:] for qid in day.get('ids', [])}
previous_ids = set(history[-1].get('ids', [])) if history else set()

def choose(bank, count, offset):
    ranked = sorted(bank, key=lambda q: (q['id'] in previous_ids, q['id'] in recent_ids, -q.get('prediction_weight', 1), q['id']))
    if not ranked:
        return []
    start = offset % len(ranked)
    rotated = ranked[start:] + ranked[:start]
    chosen = []
    for q in rotated + ranked:
        if q['id'] not in {x['id'] for x in chosen} and q['id'] not in previous_ids:
            chosen.append(q)
            if len(chosen) == count:
                return chosen
    return chosen[:count]

ordinal = datetime.now(JST).date().toordinal()
selected = choose(english, 5, ordinal * 3) + choose(social, 5, ordinal * 7)

data = {
    'date': TODAY,
    'title': f'高校入試 今日の問題 {TODAY}',
    'questions': selected,
}
Path('daily.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

history.append({'date': TODAY, 'ids': [q['id'] for q in selected]})
history = history[-7:]
Path('history.json').write_text(json.dumps(history, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(TODAY, [q['id'] for q in selected])
