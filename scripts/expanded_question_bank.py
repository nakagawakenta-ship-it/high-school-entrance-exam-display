import random, re

def question(kind, r):
    if kind == 'grammar':
        name=r.choice(['Mika','Ken','Yuta','Rina','Emi','Hana'])
        city=r.choice(['Kamakura','Yokohama','Hakone','Odawara','Kyoto'])
        year=r.randint(2011,2023)
        return f'{name} has lived in {city} ( ) {year}.',['since','for','during','while'],'since'
    if kind == 'comparison':
        a,b=r.sample(['Ken','Yuta','Mika','Emi','Hana','Sota'],2)
        x=r.randrange(130,160); y=x+r.randrange(5,25)
        return f'{a} is {x} cm tall; {b} is {y} cm. Who is taller?',[b,a,'Both','Cannot tell'],b
    if kind == 'dialogue':
        p=r.choice(['station','museum','library','aquarium','hospital','city hall'])
        d=r.choice(['turn left','turn right','go straight'])
        good=f'Please {d}.'
        return f'A: How can I get to the {p}? B: ( )',[good,'I went yesterday.','It is interesting.','I like reading.'],good
    if kind == 'reading':
        name=r.choice(['Mika','Ken','Yuta','Hana','Emi'])
        p,reason=r.choice([('library','study for a test'),('museum','learn history'),('park','join a cleanup'),('station','meet a friend'),('shop','buy a gift')])
        return f'{name} went to the {p} to {reason}. Why did {name} go there?',[f'To {reason}.','To play tennis.','To cook dinner.','To watch TV.'],f'To {reason}.'
    if kind == 'schedule':
        start=r.randrange(8*60,10*60,5); gap=r.choice([10,15,20])
        t=[start+i*gap for i in range(4)]; arrive=t[1]+r.randrange(1,gap)
        fmt=lambda v:f'{v//60}:{v%60:02d}'
        return f'Buses: {", ".join(map(fmt,t))}. You arrive at {fmt(arrive)}. Next bus?',[fmt(t[2]),fmt(t[0]),fmt(t[1]),fmt(t[3])],fmt(t[2])
    if kind == 'fee':
        student=r.randrange(200,600,50); adult=student+r.randrange(200,450,50); n=r.choice([2,3,4])
        total=student+adult*n
        return f'Tickets: student {student} yen, adult {adult} yen. One student and {n} adults: total?',[str(total),str(total-adult),str(total+adult),str(total+student)],str(total)
    if kind == 'relative':
        name=r.choice(['Ken','Emi','Hana','Rina','Yuta'])
        job=r.choice(['teacher','doctor','scientist','artist','engineer'])
        return f'{name} knows a {job} ( ) works in Yokohama.',['who','where','when','whose'],'who'
    if kind == 'passive':
        name=r.choice(['bridge','school','museum','library','station'])
        year=r.randrange(1980,2020)
        return f'The {name} was ( ) in {year}.',['built','build','building','builds'],'built'
    if kind == 'if':
        event=r.choice(['sports day','picnic','beach cleanup','school trip'])
        day=r.choice(['Saturday','Sunday','Monday'])
        return f'If it ( ) on {day}, we will cancel the {event}.',['rains','will rain','rained','raining'],'rains'
    if kind == 'data':
        days=r.sample(['Mon','Tue','Wed','Thu','Fri'],3); nums=r.sample(range(80,240,5),3)
        winner=days[nums.index(max(nums))]
        return 'Visitors: '+', '.join(f'{d} {n}' for d,n in zip(days,nums))+'. Which day had the most?',[winner]+[d for d in days if d!=winner]+['Equal'],winner
    if kind == 'geography':
        river=r.choice(['相模川','多摩川','酒匂川','鶴見川','境川'])
        return f'{river}の河口付近の低地で特に注意すべき災害は？',['洪水・高潮','雪崩','砂漠化','火砕流だけ'],'洪水・高潮'
    if kind == 'landform':
        feature,meaning=r.choice([('扇状地','山地から平野に出た川の土砂が扇形に堆積'),('三角州','河口に土砂が堆積'),('リアス海岸','谷が沈水して海岸が入り組む'),('河岸段丘','川沿いに階段状の地形ができる')])
        return f'「{meaning}」に当たる地形は？',[feature]+[x for x in ['扇状地','三角州','リアス海岸','河岸段丘'] if x!=feature],feature
    if kind == 'history':
        year,event=r.choice([(1853,'ペリー来航'),(1854,'日米和親条約'),(1867,'大政奉還'),(1871,'廃藩置県'),(1873,'地租改正'),(1889,'大日本帝国憲法発布'),(1925,'普通選挙法')])
        others=[x for x in ['鎌倉幕府成立','日清戦争','日本国憲法施行','大政奉還'] if x!=event][:3]
        return f'{year}年の出来事として正しいものは？',[event]+others,event
    if kind == 'chronology':
        years=r.sample([(1853,'ペリー来航'),(1867,'大政奉還'),(1871,'廃藩置県'),(1889,'大日本帝国憲法発布'),(1925,'普通選挙法')],3)
        years.sort()
        correct='→'.join(x[1] for x in years)
        wrong=['→'.join(years[i][1] for i in seq) for seq in [(1,0,2),(0,2,1),(2,1,0)]]
        return '出来事を古い順に並べたものは？',[correct]+wrong,correct
    if kind == 'civics':
        seats=r.choice([90,120,150,180,210,240])
        votes=seats*2//3
        return f'衆議院の出席議員{seats}人。法律案再可決に必要な賛成の最少数は？',[str(votes),str(seats//2),str(seats//3),str(seats-1)],str(votes)
    if kind == 'population':
        young=r.randrange(9,19); old=r.randrange(22,38); work=100-young-old
        return f'人口構成：15歳未満{young}％、15～64歳{work}％、65歳以上{old}％。最大の層は？',['15～64歳','15歳未満','65歳以上','すべて同じ'],'15～64歳'
    if kind == 'trade':
        ex=r.randrange(105,155,5); im=r.randrange(60,100,5)
        return f'輸出指数100→{ex}、輸入指数100→{im}。正しい説明は？',['輸出増・輸入減','両方増加','輸出減・輸入増','両方減少'],'輸出増・輸入減'
    if kind == 'exchange':
        a=r.choice([130,140,150,160]);b=a-r.choice([10,15,20])
        return f'為替が1ドル{a}円から{b}円に変化した。これは？',['円高・ドル安','円安・ドル高','変化なし','必ず物価が2倍'],'円高・ドル安'
    if kind == 'disaster':
        area=r.choice(['相模川沿い','酒匂川沿い','境川沿い','鶴見川沿い'])
        weather=r.choice(['台風','大雨','長雨'])
        return f'{weather}時に{area}の住民がハザードマップで確認すべきことは？',['浸水区域と避難場所','選挙区','税率','輸出額'],'浸水区域と避難場所'
    if kind == 'budget':
        a=r.randrange(25,38);b=r.randrange(10,20);c=r.randrange(8,16)
        return f'歳出：社会保障{a}％、教育{b}％、公共事業{c}％。最も大きい項目は？',['社会保障','教育','公共事業','同率'],'社会保障'
    raise ValueError(kind)

EN=['grammar','comparison','dialogue','reading','schedule','fee','relative','passive','if','data']
SO=['geography','landform','history','chronology','civics','population','trade','exchange','disaster','budget']
def fresh_questions(date, used):
    seed=int(date.strftime('%Y%m%d')); r=random.Random(seed)
    results=[]
    for subject, kinds in [('english',EN),('social',SO)]:
        # Five different question families per subject each day, rotating across days.
        shift=(date.toordinal()*3)%len(kinds)
        selected=[kinds[(shift+i*3)%len(kinds)] for i in range(5)]
        for index,kind in enumerate(selected,1):
            for _ in range(10000):
                q,choices,answer=question(kind,r)
                key=re.sub(r'\s+','',q).casefold()
                if key not in used and len(set(choices))==4 and answer in choices:
                    used.add(key)
                    results.append(dict(id=f'{"eng" if subject=="english" else "soc"}-{date:%Y%m%d}-{index}',subject=subject,topic=kind,question=q,choices=choices,answer=answer))
                    break
            else:
                raise RuntimeError('Unable to produce a unique valid '+kind+' question')
    return results
