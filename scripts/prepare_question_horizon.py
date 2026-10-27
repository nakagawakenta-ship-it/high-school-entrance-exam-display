import json,glob,re,sys,random
from datetime import date,timedelta,datetime
from pathlib import Path
from zoneinfo import ZoneInfo
sys.path.insert(0,'scripts')
from expanded_question_bank import fresh_questions,template_key

today=datetime.now(ZoneInfo('Asia/Tokyo')).date()
start=max(date(2026,10,20),today+timedelta(days=1))
end=date(2027,2,28)
seen=set()
recent_history=[]
for p in glob.glob('daily/*.json'):
    try:
        data=json.loads(Path(p).read_text(encoding='utf-8'))
        day=date.fromisoformat(data.get('date') or Path(p).stem)
        for q in data.get('questions',[]):
            seen.add(re.sub(r'\s+','',q['question']).casefold())
        if day < start:
            keys={(q.get('subject'),q.get('topic','unknown'),template_key(q.get('question',''))) for q in data.get('questions',[])}
            recent_history.append((day,keys))
    except (ValueError,OSError,KeyError):pass
Path('prepared').mkdir(exist_ok=True)
count=0
fallback_days=[]
d=start
while d<=end:
    questions=None
    cooldown_used=None
    for cooldown in (7,5,3):
        cutoff=d-timedelta(days=cooldown)
        recent_templates={key for history_day,keys in recent_history if cutoff <= history_day < d for key in keys}
        candidate_seen=set(seen)
        try:
            candidate_questions=fresh_questions(d,candidate_seen,recent_templates)
        except RuntimeError:
            if cooldown==3:
                raise
            continue
        questions=candidate_questions
        seen=candidate_seen
        cooldown_used=cooldown
        break
    if questions is None:
        raise RuntimeError('Unable to generate questions with adaptive template cooldown: '+str(d))
    if cooldown_used < 7:
        fallback_days.append({'date':d.isoformat(),'cooldown_days':cooldown_used})
    if len(questions)!=10:raise RuntimeError('Incorrect count '+str(d))
    if sum(q['subject']=='english' for q in questions)!=5:raise RuntimeError('English count '+str(d))
    if sum(q['subject']=='social' for q in questions)!=5:raise RuntimeError('Social count '+str(d))
    for index,q in enumerate(questions):
        if len(q['choices'])!=4 or len(set(q['choices']))!=4 or q['answer'] not in q['choices']:
            raise RuntimeError('Invalid answers '+str(d))
        random.Random(int(d.strftime('%Y%m%d')) + index * 997).shuffle(q['choices'])
    payload={'date':d.isoformat(),'title':'高校入試 今日の問題 '+d.isoformat(),'questions':questions}
    Path('prepared',d.isoformat()+'.json').write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    recent_history.append((d,{(q.get('subject'),q.get('topic','unknown'),template_key(q.get('question',''))) for q in questions}))
    count+=10
    d+=timedelta(days=1)
print('PREPARED',count,'questions from',start.isoformat(),'through',end.isoformat())
print('COOLDOWN_FALLBACK_DAYS',len(fallback_days),json.dumps(fallback_days,ensure_ascii=False))
