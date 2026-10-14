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
        places=['station','museum','library','aquarium','hospital','city hall','sports center','post office','park','art museum','bus stop','shopping mall']
        start,dest=r.sample(places,2)
        name=r.choice(['Mika','Ken','Yuta','Rina','Emi','Hana','Sota','Aki'])
        d=r.choice(['turn left','turn right','go straight'])
        good=f'Please {d}.'
        stem=r.choice([
            f'A: How can I get from the {start} to the {dest}? B: ( )',
            f'A: {name} is at the {start}. How can {name} get to the {dest}? B: ( )',
            f'A: Excuse me. I am at the {start}. How do I get to the {dest}? B: ( )',
            f'A: Could you tell me the way from the {start} to the {dest}? B: ( )'
        ])
        return stem,[good,'I went there last week.','It opens at nine.','I like reading books.'],good
    if kind == 'reading':
        name=r.choice(['Mika','Ken','Yuta','Hana','Emi','Rina','Sota','Aki'])
        p,reason=r.choice([('library','study for a test'),('museum','learn history'),('park','join a cleanup'),('station','meet a friend'),('shop','buy a gift'),('community center','practice music'),('beach','collect trash'),('science museum','see an exhibition'),('bookstore','buy a dictionary'),('gym','play basketball')])
        stem=r.choice([f'{name} went to the {p} to {reason}. Why did {name} go there?',f'{name} visited the {p} because {name} wanted to {reason}. What was the purpose of the visit?'])
        return stem,[f'To {reason}.','To play tennis.','To cook dinner.','To watch TV.'],f'To {reason}.'
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
        name=r.choice(['Ken','Emi','Hana','Rina','Yuta','Sota','Mika','Aki'])
        job=r.choice(['teacher','doctor','scientist','artist','engineer','writer','nurse','cook'])
        city=r.choice(['Yokohama','Kamakura','Fujisawa','Odawara','Kawasaki','Sagamihara','Chigasaki'])
        return f'{name} knows a {job} ( ) works in {city}.',['who','where','when','whose'],'who'
    if kind == 'passive':
        name=r.choice(['bridge','school','museum','library','station'])
        year=r.randrange(1980,2020)
        return f'The {name} was ( ) in {year}.',['built','build','building','builds'],'built'
    if kind == 'if':
        event=r.choice(['sports day','picnic','beach cleanup','school trip','soccer game','outdoor concert','class trip','tennis match'])
        day=r.choice(['Saturday','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday'])
        name=r.choice(['Mika','Ken','Yuta','Rina','Emi','Hana','Sota','Aki'])
        stem=r.choice([f'If it ( ) on {day}, {name} will cancel the {event}.',f'If it ( ) this weekend, {name} will move the {event} indoors.',f'{name} will cancel the {event} if it ( ) on {day}.'])
        return stem,['rains','will rain','rained','raining'],'rains'
    if kind == 'data':
        days=r.sample(['Mon','Tue','Wed','Thu','Fri'],3); nums=r.sample(range(80,240,5),3)
        winner=days[nums.index(max(nums))]
        return 'Visitors: '+', '.join(f'{d} {n}' for d,n in zip(days,nums))+'. Which day had the most?',[winner]+[d for d in days if d!=winner]+['Equal'],winner
    if kind == 'geography':
        mode=r.randrange(6)
        if mode==0:
            river=r.choice(['相模川','多摩川','酒匂川','鶴見川','境川','早川','金目川','引地川','帷子川','大岡川'])
            stem=r.choice([f'{river}の河口付近の低地で特に注意すべき災害は？',f'{river}流域で大雨が続いた場合に想定される危険は？',f'神奈川県の{river}周辺で洪水対策として重要な情報は？',f'{river}沿いの低地に住む人が大雨前に確認すべきことは？'])
            return stem,['洪水・高潮','雪崩','砂漠化','火砕流だけ'],'洪水・高潮'
        if mode==1:
            place,feature=r.choice([('横浜港','貿易港として発達'),('箱根','火山地形と温泉'),('相模原台地','関東ローム層が広がる台地'),('三浦半島','海岸線が複雑で漁業も行われる'),('丹沢山地','山地が広がり森林が多い'),('湘南海岸','海水浴場や観光で知られる')])
            return f'神奈川県の{place}の特徴として適切なものは？',[feature,'大規模な砂漠が広がる','一年中永久凍土に覆われる','標高がすべて海面以下'],feature
        if mode==2:
            climate=r.choice([('太平洋側','冬に晴天が多く乾燥しやすい'),('日本海側','冬に雪や雨が多い'),('瀬戸内','降水量が比較的少ない'),('中央高地','内陸で年較差が大きい'),('北海道','冷涼で梅雨の影響が比較的小さい'),('南西諸島','一年を通じて温暖で台風の影響を受けやすい'),('東北地方','冬の寒さが厳しく、日本海側では雪が多い'),('南四国','黒潮の影響を受け温暖で降水量が多い')])
            stem=r.choice([f'日本の気候区分で「{climate[0]}」の特徴は？',f'「{climate[1]}」という気候の特徴がみられる地域は？'])
            options=[climate[1],'一年中ほぼ毎日同じ量の雨が降る','年間を通じて気温が常に30℃を超える','冬でも必ず台風が上陸する']
            return stem,options,climate[1]
        if mode==3:
            crops=[('北海道','てんさい'),('新潟平野','米'),('高知平野','促成栽培の野菜'),('鹿児島','畜産'),('長野県','高原野菜'),('沖縄県','さとうきび'),('青森県','りんご'),('山梨県','ぶどう'),('静岡県','茶'),('群馬県','こんにゃくいも'),('千葉県','落花生'),('愛媛県','みかん'),('熊本県','すいか'),('宮崎県','きゅうりの促成栽培'),('北海道十勝地方','大規模な畑作'),('三重県','養殖真珠'),('広島県','かきの養殖'),('富山平野','米'),('鳥取県','らっきょう'),('福井県','米'),('岩手県','肉用牛'),('和歌山県','うめ'),('栃木県','いちご'),('茨城県','れんこん'),('佐賀平野','米'),('徳島県','すだち'),('長崎県','じゃがいも'),('奈良県','柿'),('福岡県','いちご'),('石川県','米')]
            crop=r.choice(crops)
            stem=r.choice([f'「{crop[1]}」の生産がさかんな地域はどこ？',f'農業の地域差について、「{crop[1]}」と結びつきが強い地域を選びなさい。'])
            options=[crop[0]]+[x[0] for x in r.sample([x for x in crops if x[0]!=crop[0]],3)]
            return stem,options,crop[0]
        if mode==4:
            resources=[('瀬戸内海沿岸','造船・鉄鋼などの工業'),('京浜工業地帯','機械・化学などの工業'),('中京工業地帯','自動車工業'),('北九州工業地域','かつての製鉄業'),('阪神工業地帯','機械・化学・金属工業'),('京葉工業地域','石油化学工業'),('東海地方','自動車・楽器などの工業'),('北陸地方','化学・機械などの工業'),('瀬戸内工業地域','石油化学・造船'),('鹿島臨海工業地域','石油化学・鉄鋼')])
            resource=r.choice(resources)
            stem=f'「{resource[0]}」と関連が深い工業の特徴は？'
            options=[resource[1]]+[x[1] for x in r.sample([x for x in resources if x[1]!=resource[1]],3)]
            return stem,options,resource[1]
        river=r.choice(['相模川','多摩川','酒匂川','鶴見川','境川','早川','金目川','引地川','帷子川','大岡川'])
        stem=r.choice([f'{river}などの川沿いで大雨時に避難情報を確認する主な理由は？',f'{river}の流域で住民が防災情報を確認する必要があるのはなぜ？',f'大雨の際、{river}沿いの地域で注意すべきことは？',f'{river}周辺で避難判断に役立つ情報として最も重要なものは？'])
        return stem,['河川の増水や浸水のおそれ','必ず火山が噴火するため','海水温が必ず氷点下になるため','日照時間が必ずゼロになるため'],'河川の増水や浸水のおそれ'
    if kind == 'landform':
        pairs=[
            ('扇状地','山地から平野に出た川の土砂が扇形に堆積'),
            ('三角州','河口に土砂が堆積'),
            ('リアス海岸','谷が沈水して海岸が入り組む'),
            ('河岸段丘','川沿いに階段状の地形ができる'),
            ('自然堤防','洪水時に運ばれた土砂が川沿いに帯状に堆積'),
            ('氾濫原','洪水時に川の水が広がる平坦な低地'),
            ('砂州','波や沿岸流で運ばれた砂が細長く堆積'),
            ('砂丘','風で運ばれた砂が積み重なる'),
            ('V字谷','川の侵食で谷底が深く削られる'),
            ('カルスト地形','石灰岩が雨水などに溶かされてできる')
        ]
        feature,meaning=r.choice(pairs)
        fmt=r.randrange(8)
        if fmt==0:
            stem=f'地形の特徴「{meaning}」に当たる名称は？'
        elif fmt==1:
            stem=f'次の説明「{meaning}」に該当する地形はどれ？'
        elif fmt==2:
            stem=f'地形図の読解：{meaning}という特徴をもつ地形は？'
        elif fmt==3:
            stem=f'河川・海岸などのはたらきで「{meaning}」となった地形は？'
        elif fmt==4:
            stem=f'地理の資料に「{meaning}」と記されている。該当する地形名は？'
        elif fmt==5:
            stem=f'「{meaning}」という説明に最もよく当てはまる地形を選びなさい。'
        elif fmt==6:
            stem=f'地形の成り立ちを説明した文「{meaning}」に合う用語は？'
        else:
            stem=f'地形の分類問題：特徴が「{meaning}」であるものはどれ？'
        options=[feature]+[x[0] for x in r.sample([x for x in pairs if x[0]!=feature],3)]
        return stem,options,feature
    if kind == 'history':
        events=[
            (645,'大化の改新'),(710,'平城京遷都'),(794,'平安京遷都'),(894,'遣唐使の停止'),
            (1185,'壇ノ浦の戦い'),(1192,'源頼朝が征夷大将軍に任命'),(1274,'文永の役'),
            (1333,'鎌倉幕府滅亡'),(1338,'足利尊氏が征夷大将軍に任命'),(1467,'応仁の乱'),
            (1543,'鉄砲伝来'),(1549,'キリスト教伝来'),(1600,'関ヶ原の戦い'),(1603,'江戸幕府成立'),
            (1639,'ポルトガル船来航禁止'),(1853,'ペリー来航'),(1854,'日米和親条約'),
            (1867,'大政奉還'),(1868,'明治維新'),(1871,'廃藩置県'),(1873,'地租改正'),
            (1889,'大日本帝国憲法発布'),(1894,'日清戦争開始'),(1904,'日露戦争開始'),
            (1914,'第一次世界大戦開始'),(1925,'普通選挙法成立'),(1931,'満州事変'),
            (1937,'日中戦争開始'),(1941,'太平洋戦争開始'),(1945,'第二次世界大戦終結'),
            (1946,'日本国憲法公布'),(1947,'日本国憲法施行'),(1951,'サンフランシスコ平和条約調印'),
            (1964,'東京オリンピック開催'),(1972,'沖縄返還'),(1973,'石油危機'),
            (1989,'消費税導入'),(1995,'阪神・淡路大震災'),(2011,'東日本大震災')
        ]
        year,event=r.choice(events)
        stem=r.choice([f'{year}年の出来事として正しいものは？',f'次のうち、{year}年に起きた出来事は？'])
        distractors=[x[1] for x in r.sample([x for x in events if x[1]!=event],3)]
        return stem,[event]+distractors,event
    if kind == 'chronology':
        events=[(645,'大化の改新'),(710,'平城京遷都'),(794,'平安京遷都'),(894,'遣唐使の停止'),(1185,'壇ノ浦の戦い'),(1192,'源頼朝が征夷大将軍に任命'),(1274,'文永の役'),(1333,'鎌倉幕府滅亡'),(1338,'足利尊氏が征夷大将軍に任命'),(1467,'応仁の乱'),(1543,'鉄砲伝来'),(1549,'キリスト教伝来'),(1600,'関ヶ原の戦い'),(1603,'江戸幕府成立'),(1639,'ポルトガル船来航禁止'),(1853,'ペリー来航'),(1854,'日米和親条約'),(1867,'大政奉還'),(1868,'明治維新'),(1871,'廃藩置県'),(1873,'地租改正'),(1889,'大日本帝国憲法発布'),(1894,'日清戦争開始'),(1904,'日露戦争開始'),(1914,'第一次世界大戦開始'),(1925,'普通選挙法成立'),(1931,'満州事変'),(1937,'日中戦争開始'),(1941,'太平洋戦争開始'),(1945,'第二次世界大戦終結'),(1946,'日本国憲法公布'),(1947,'日本国憲法施行'),(1951,'サンフランシスコ平和条約調印'),(1964,'東京オリンピック開催'),(1972,'沖縄返還'),(1973,'石油危機'),(1989,'消費税導入'),(1995,'阪神・淡路大震災'),(2011,'東日本大震災')]
        years=r.sample(events,3)
        years.sort()
        correct='→'.join(x[1] for x in years)
        wrong=['→'.join(years[i][1] for i in seq) for seq in [(1,0,2),(0,2,1),(2,1,0)]]
        return f'次の3件（{", ".join(x[1] for x in years)}）を古い順に並べると？',[correct]+wrong,correct
    if kind == 'civics':
        seats=r.randrange(60,601,10)
        votes=(2*seats+2)//3
        stem=r.choice([f'衆議院の出席議員{seats}人。法律案再可決に必要な賛成の最少数は？',f'出席議員が{seats}人の衆議院で、法律案を再可決するには最低何人の賛成が必要？'])
        options=[str(votes),str(seats//2),str(seats//3),str(seats-1)]
        return stem,options,str(votes)
    if kind == 'population':
        young=r.randrange(9,19); old=r.randrange(22,38); work=100-young-old
        return f'人口構成：15歳未満{young}％、15～64歳{work}％、65歳以上{old}％。最大の層は？',['15～64歳','15歳未満','65歳以上','すべて同じ'],'15～64歳'
    if kind == 'trade':
        ex=r.randrange(105,155,5); im=r.randrange(60,100,5)
        return f'輸出指数100→{ex}、輸入指数100→{im}。正しい説明は？',['輸出増・輸入減','両方増加','輸出減・輸入増','両方減少'],'輸出増・輸入減'
    if kind == 'exchange':
        a=r.choice(list(range(100,181,5)))
        b=a-r.choice([5,10,15,20,25,30])
        stem=r.choice([f'為替が1ドル{a}円から{b}円に変化した。これは？',f'1ドルあたり{a}円だった為替相場が{b}円になった。この変化を何という？'])
        return stem,['円高・ドル安','円安・ドル高','変化なし','必ず物価が2倍'],'円高・ドル安'
    if kind == 'disaster':
        area=r.choice(['相模川沿い','酒匂川沿い','境川沿い','鶴見川沿い','多摩川沿い','海岸近く','急傾斜地の近く','山間部'])
        weather=r.choice(['台風','大雨','長雨','線状降水帯による豪雨','大雨と満潮'])
        concern=r.choice([('浸水区域と避難場所','洪水'),('土砂災害警戒区域と避難経路','土砂災害')])
        stem=r.choice([f'{weather}時に{area}で{concern[1]}に備え、ハザードマップで確認すべきことは？',f'{area}の住民が{weather}により{concern[1]}の危険を確認するには、ハザードマップのどこを見る？'])
        return stem,[concern[0],'選挙区','税率','輸出額'],concern[0]
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
