import json,glob,re,sys
from datetime import date,timedelta
from pathlib import Path
sys.path.insert(0,'scripts')
from expanded_question_bank import fresh_questions
start=date(2026,10,16)
end=date(2027,2,28)
seen=set()
for p in glob.glob('daily/*.json'):
    try:
        data=json.loads(Path(p).read_text(encoding='utf-8'))
        if data.get('date','')>=start.isoformat():continue
        for q in data.get('questions',[]):
            seen.add(re.sub(r'\s+','',q['question']).casefold())
    except (ValueError,OSError,KeyError):pass
Path('prepared').mkdir(exist_ok=True)
count=0
d=start
while d<=end:
    questions=fresh_questions(d,seen)
    if len(questions)!=10:raise RuntimeError('Incorrect count '+str(d))
    if sum(q['subject']=='english' for q in questions)!=5:raise RuntimeError('English count '+str(d))
    if sum(q['subject']=='social' for q in questions)!=5:raise RuntimeError('Social count '+str(d))
    for q in questions:
        if len(q['choices'])!=4 or len(set(q['choices']))!=4 or q['answer'] not in q['choices']:
            raise RuntimeError('Invalid answers '+str(d))
    payload={'date':d.isoformat(),'title':'高校入試 今日の問題 '+d.isoformat(),'questions':questions}
    Path('prepared',d.isoformat()+'.json').write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    count+=10
    d+=timedelta(days=1)
print('PREPARED',count,'questions through',end.isoformat())
