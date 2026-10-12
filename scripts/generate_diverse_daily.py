import json,glob,re,os
from datetime import datetime
from zoneinfo import ZoneInfo
from expanded_question_bank import fresh_questions
d=datetime.now(ZoneInfo('Asia/Tokyo')).date()
seen=set()
for p in glob.glob('daily/*.json'):
    try:
        j=json.load(open(p,encoding='utf-8'))
        if j.get('date')==d.isoformat():continue
        for q in j.get('questions',[]):
            seen.add(re.sub(r'\s+','',q['question']).casefold())
    except (OSError,ValueError,KeyError):pass
questions=fresh_questions(d,seen)
import random
for i,q in enumerate(questions):
    random.Random(int(d.strftime('%Y%m%d'))+i*997).shuffle(q['choices'])
data={'date':d.isoformat(),'title':f'高校入試 今日の問題 {d.isoformat()}','questions':questions}
os.makedirs('daily',exist_ok=True)
payload=json.dumps(data,ensure_ascii=False,separators=(',',':'))
open('daily.json','w',encoding='utf-8').write(payload)
open(f'daily/{d.isoformat()}.json','w',encoding='utf-8').write(payload)
print('Validated',len(questions),'unique questions')
