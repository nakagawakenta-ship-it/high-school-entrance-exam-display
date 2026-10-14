import sys,json,glob,re
from datetime import date,timedelta
sys.path.insert(0,'scripts')
from expanded_question_bank import fresh_questions
start=date(2026,10,16)
end=date(2027,2,28)
used=set()
for p in glob.glob('daily/*.json'):
    try:
        for q in json.load(open(p,encoding='utf-8')).get('questions',[]):
            used.add(re.sub(r'\s+','',q['question']).casefold())
    except (OSError,ValueError,KeyError):
        pass
result={'start':start.isoformat(),'end':end.isoformat(),'days_checked':0,'questions_checked':0,'errors':[],'topic_counts':{}}
d=start
while d<=end:
    try:
        questions=fresh_questions(d,used)
        assert len(questions)==10
        for q in questions:
            assert len(q['choices'])==4 and len(set(q['choices']))==4
            assert q['answer'] in q['choices']
            topic=q.get('topic','unknown')
            result['topic_counts'][topic]=result['topic_counts'].get(topic,0)+1
        result['days_checked']+=1
        result['questions_checked']+=len(questions)
    except Exception as exc:
        result['errors'].append({'date':d.isoformat(),'error':str(exc)})
        break
    d+=timedelta(days=1)
with open('question_quality_audit.json','w',encoding='utf-8') as f:
    json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps(result,ensure_ascii=False,indent=2))
if result['errors']:
    sys.exit(1)
