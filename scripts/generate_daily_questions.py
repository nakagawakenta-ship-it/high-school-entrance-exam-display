import json
import os
import random
from datetime import datetime
from zoneinfo import ZoneInfo

# Deterministic date-based generator for 2027 Kanagawa public high-school entrance exam practice.
# Each date gets a stable set. IDs and parameters vary by date so daily.json changes every day.

def today_jst():
    return datetime.now(ZoneInfo('Asia/Tokyo')).date()


def make_questions(d):
    seed = int(d.strftime('%Y%m%d'))
    r = random.Random(seed)
    ymd = d.strftime('%Y%m%d')

    names = ['Ken', 'Mika', 'Yuki', 'Sota', 'Aya', 'Rina', 'Taro', 'Emi']
    places = ['library', 'station', 'museum', 'park', 'school', 'community center']
    activities = ['play tennis', 'visit the museum', 'study English', 'clean the park', 'practice soccer']
    n = r.choice(names); p = r.choice(places); a = r.choice(activities)
    years = r.randint(2, 8)
    x = r.randint(11, 24); y = r.randint(5, x-2); z = r.randint(7, 20)

    eng = [
      {'question': f'If it ( ) sunny tomorrow, {n} will {a}.', 'choices':['is','will be','was','has been'], 'answer':'is'},
      {'question': f'This is the {p} ( ) {n} visited last Sunday.', 'choices':['that','where','when','whose'], 'answer':'that'},
      {'question': f'{n} has lived in Kanagawa ( ) {years} years.', 'choices':['for','since','from','during'], 'answer':'for'},
      {'question': f'A survey shows: A {x}, B {y}, C {z}. How many more chose A than B?', 'choices':[str(x-y),str(x+y),str(abs(z-y)),str(x)], 'answer':str(x-y)},
      {'question': f'{n} uses a reusable bottle to reduce plastic waste. Why does {n} use it?', 'choices':['To reduce plastic waste','To buy more plastic','To carry books','To make school longer'], 'answer':'To reduce plastic waste'}
    ]

    geo = [
      ('神奈川県の県庁所在地はどこですか。',['横浜市','藤沢市','川崎市','鎌倉市'],'横浜市'),
      ('神奈川県にある国際貿易港として発展した港はどれですか。',['横浜港','新潟港','博多港','小樽港'],'横浜港'),
      ('日本の太平洋側で人口や工業が集中する帯状の地域を何といいますか。',['太平洋ベルト','中央高地','リアス海岸','フォッサマグナ'],'太平洋ベルト')]
    hist = [
      ('1889年に発布された憲法はどれですか。',['大日本帝国憲法','日本国憲法','十七条の憲法','五箇条の御誓文'],'大日本帝国憲法'),
      ('第二次世界大戦が終わった年は何年ですか。',['1945年','1939年','1947年','1951年'],'1945年'),
      ('鎌倉幕府を開いた人物は誰ですか。',['源頼朝','徳川家康','足利尊氏','豊臣秀吉'],'源頼朝')]
    civ = [
      ('日本国憲法で国会は何と定められていますか。',['唯一の立法機関','最高の司法機関','行政の最高機関','地方自治の機関'],'唯一の立法機関'),
      ('国民主権とはどのような考え方ですか。',['政治の最終的な決定権が国民にある','裁判所だけが政治を決める','内閣だけが法律を作る','地方だけが国政を決める'],'政治の最終的な決定権が国民にある'),
      ('三権分立で司法を担当する機関はどれですか。',['裁判所','国会','内閣','地方議会'],'裁判所')]
    g=r.choice(geo); h=r.choice(hist); c=r.choice(civ)
    pop0=r.choice([10,20,25,40]); pct=r.choice([4,5,10]); pop1=pop0*(100+pct)//100
    soc = [
      {'question':g[0],'choices':g[1],'answer':g[2]},
      {'question':h[0],'choices':h[1],'answer':h[2]},
      {'question':c[0],'choices':c[1],'answer':c[2]},
      {'question':f'ある地域の人口が{pop0}万人から{pop1}万人に増えました。増加率として最も近いものはどれですか。','choices':[f'{pct}％','1％','20％','50％'],'answer':f'{pct}％'},
      {'question':'円高が進んだ場合、一般に日本の輸入品の価格にはどのような影響が考えられますか。','choices':['安くなりやすい','必ず2倍になる','変化しない','輸入できなくなる'],'answer':'安くなりやすい'}
    ]

    questions=[]
    for i,q in enumerate(eng,1): questions.append({'id':f'eng-{ymd}-{i}','subject':'english',**q})
    for i,q in enumerate(soc,1): questions.append({'id':f'soc-{ymd}-{i}','subject':'social',**q})
    return {'date':d.isoformat(),'title':f'高校入試 日替わり問題 {d.isoformat()}','questions':questions}


def main():
    d=today_jst()
    data=make_questions(d)
    os.makedirs('daily',exist_ok=True)
    text=json.dumps(data,ensure_ascii=False,separators=(',',':'))
    with open(f'daily/{d.isoformat()}.json','w',encoding='utf-8') as f: f.write(text)
    with open('daily.json','w',encoding='utf-8') as f: f.write(text)
    print(f'Generated {len(data["questions"])} questions for {d.isoformat()}')

if __name__=='__main__': main()
