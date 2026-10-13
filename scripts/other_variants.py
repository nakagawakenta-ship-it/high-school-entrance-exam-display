"""Larger pools and varied answers for English and civics/data practice."""
def other_question(kind,r):
    if kind=='dialogue':
        place=r.choice(['station','museum','library','aquarium','hospital','city hall','post office','park','school','bus stop','bank','bookstore','zoo','supermarket','theater','gym','hotel','restaurant','police station','art gallery'])
        move=r.choice(['turn left','turn right','go straight','cross the bridge','walk two blocks'])
        good='Please '+move+'.'
        return f'A: How can I get to the {place}? B: ( )',[good,'I went there yesterday.','I am thirteen.','It opens at nine.'],good
    if kind=='reading':
        name=r.choice(['Mika','Ken','Yuta','Hana','Emi','Rina','Sota','Mai','Taro','Lisa'])
        where,why=r.choice([('library','study'),('museum','learn history'),('park','clean up'),('station','meet a friend'),('shop','buy a gift'),('beach','collect trash'),('hospital','visit her aunt'),('zoo','see pandas'),('farm','pick apples'),('school','practice music'),('pool','swim'),('gym','play basketball'),('bakery','buy bread'),('cafe','meet classmates'),('garden','take photos'),('river','watch birds'),('hall','hear a concert'),('stadium','watch a game')])
        answer='To '+why+'.'
        return f'{name} went to the {where} to {why}. Why did {name} go?',[answer,'To sleep.','To watch TV.','To cook rice.'],answer
    if kind=='if':
        event=r.choice(['sports day','picnic','beach cleanup','school trip','soccer match','baseball game','field trip','outdoor concert','festival','hike','camp','barbecue','marathon','market','garden party','boat tour','nature walk','parade'])
        day=r.choice(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
        return f'If it ( ) on {day}, we will cancel the {event}.',['rains','will rain','rained','raining'],'rains'
    if kind=='relative':
        name=r.choice(['Ken','Emi','Hana','Rina','Yuta','Sota','Mai','Lisa'])
        job=r.choice(['teacher','doctor','scientist','artist','engineer','pilot','writer','farmer','musician','chef','nurse','designer'])
        city=r.choice(['Yokohama','Kamakura','Tokyo','Odawara','Fujisawa','Kyoto','Osaka','Sapporo'])
        return f'{name} knows a {job} ( ) works in {city}.',['who','where','when','whose'],'who'
    if kind=='civics':
        seats=r.randrange(60,451,3)
        votes=(seats*2+2)//3
        return f'衆院の出席議員{seats}人。再可決に必要な賛成の最少数は？',[str(votes),str(seats//2+1),str(seats//3),str(seats-1)],str(votes)
    if kind=='exchange':
        a=r.randrange(90,181,5);delta=r.choice([5,10,15,20,25,30]);b=a+r.choice([-delta,delta])
        answer='円高・ドル安' if b<a else '円安・ドル高'
        return f'1ドル{a}円→{b}円。この変化は？',[answer,'円安・ドル高' if b<a else '円高・ドル安','円の価値は不変','円とドルが同時に上昇'],answer
    if kind=='trade':
        ex=r.randrange(60,151,5);im=r.randrange(60,151,5)
        if ex==100 or im==100:return other_question(kind,r)
        answer=('輸出増' if ex>100 else '輸出減')+'・'+('輸入増' if im>100 else '輸入減')
        return f'指数：輸出100→{ex}、輸入100→{im}。正しいのは？',['輸出増・輸入増','輸出増・輸入減','輸出減・輸入増','輸出減・輸入減'],answer
    if kind=='disaster':
        area=r.choice(['相模川流域','鶴見川流域','酒匂川流域','境川流域','多摩川流域','東京湾沿岸','湘南の海岸','三浦半島','箱根の山地','丹沢の山地','横浜の丘陵','鎌倉の谷戸','小田原の海岸','逗子の斜面','藤沢の低地','平塚の河口','横須賀の海岸','大磯の海岸','川崎の低地','秦野の斜面'])
        event,answer=r.choice([('大雨','浸水想定区域'),('地震','指定避難場所'),('台風','避難経路'),('豪雨','土砂災害警戒区域'),('長雨','河川の水位'),('地震発生後','周囲の安全')])
        return f'{area}で{event}に備える。確認すべき情報は？',[answer,'観光客数','輸出額','選挙結果'],answer
    if kind=='budget':
        a,b,c=r.sample(range(12,41),3)
        answer=max([('社会保障',a),('教育',b),('公共事業',c)],key=lambda x:x[1])[0]
        return f'歳出：社会保障{a}％、教育{b}％、公共事業{c}％。最大は？',['社会保障','教育','公共事業','同率'],answer
    if kind=='population':
        young=r.randrange(8,30);old=r.randrange(17,46);work=100-young-old
        vals=[('15歳未満',young),('15～64歳',work),('65歳以上',old)]
        m=max(x[1] for x in vals)
        if sum(v==m for _,v in vals)!=1:return other_question(kind,r)
        answer=next(k for k,v in vals if v==m)
        return f'人口構成：年少{young}％、生産年齢{work}％、老年{old}％。最多は？',['15歳未満','15～64歳','65歳以上','すべて同じ'],answer
    return None
