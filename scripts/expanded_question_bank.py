import random, re

def template_key(text):
    s=str(text).casefold()
    s=re.sub(r"\b(mika|ken|yuta|rina|emi|hana|sota|aki|riku|sara|aya)\b","<name>",s)
    s=re.sub(r"\b(kamakura|yokohama|hakone|odawara|kyoto|fujisawa|kawasaki|sagamihara|chigasaki)\b","<city>",s)
    s=re.sub(r"\d+(?:,\d{3})*(?:\.\d+)?","<n>",s)
    return re.sub(r"\s+","",s)

def question(kind, r):
    if kind == 'grammar':
        mode=r.randrange(8)
        if mode==0:
            name=r.choice(['Mika','Ken','Yuta','Rina','Emi','Hana'])
            city=r.choice(['Kamakura','Yokohama','Hakone','Odawara','Kyoto'])
            year=r.randint(2011,2023)
            return f'{name} has lived in {city} ( ) {year}.',['since','for','during','while'],'since'
        if mode==1:
            name=r.choice(['Mika','Ken','Yuta','Rina','Emi','Hana'])
            years=r.choice(['two years','three years','five years','six months'])
            return f'{name} has studied English ( ) {years}.',['for','since','during','from'],'for'
        if mode==2:
            return 'If you ( ) free this afternoon, please help me with the event.',['are','will be','were','have been'],'are'
        if mode==3:
            return 'The picture ( ) by my grandfather many years ago.',['was taken','took','is taking','has take'],'was taken'
        if mode==4:
            return 'My sister has never ( ) sushi.',['eaten','ate','eat','eating'],'eaten'
        if mode==5:
            return 'It is important ( ) the environment.',['to protect','protecting','protect','protected'],'to protect'
        if mode==6:
            return 'The girl ( ) lives next door is kind.',['who','where','when','whose'],'who'
        return 'This math problem is ( ) than the last one.',['more difficult','most difficult','difficult','the difficult'],'more difficult'
    if kind == 'comparison':
        mode=r.randrange(5)
        if mode==0:
            a,b=r.sample(['Ken','Yuta','Mika','Emi','Hana','Sota'],2)
            x=r.randrange(130,160); y=x+r.randrange(5,25)
            return f'{a} is {x} cm tall; {b} is {y} cm. Who is taller?',[b,a,'Both','Cannot tell'],b
        if mode==1:
            a,b=r.sample(['Mika','Ken','Yuta','Emi','Hana','Sota'],2)
            x=r.randrange(500,1501,100); y=x+r.randrange(100,501,100)
            return f"{a}'s book costs {x} yen and {b}'s book costs {y} yen. Which book is more expensive?",[b,a,'They cost the same','Cannot tell'],b
        if mode==2:
            a,b=r.sample(['Route A','Route B','Route C','Route D'],2)
            x=r.randrange(2,8); y=x+r.randrange(1,5)
            return f'{a} is {x} km long and {b} is {y} km long. Which route is shorter?',[a,b,'They are equal','Cannot tell'],a
        if mode==3:
            return 'This math problem is ( ) than the last one.',['more difficult','most difficult','difficult','the difficult'],'more difficult'
        return 'Choose the sentence that means both people have the same height.',['Mika is as tall as Ken.','Mika is taller Ken.','Mika is the tallest than Ken.','Mika is tall as Ken.'],'Mika is as tall as Ken.'
    if kind == 'dialogue':
        name=r.choice(['Mika','Ken','Yuta','Rina','Emi','Hana','Sota','Aki'])
        scenarios=[
            ("A: I am sorry I am late, {name}. B: ( )","That is all right.",["You are welcome.","See you tomorrow.","Here is your ticket."]),
            ("A: Thank you for helping me, {name}. B: ( )","You are welcome.",["I am sorry to hear that.","Good luck yesterday.","Here you are."]),
            ("A: I am going to give a speech tomorrow. B: ( )","Good luck!",["You are welcome.","That is mine.","I went yesterday."]),
            ("A: Why don't we clean the beach on Sunday? B: ( )","That sounds good.",["It is blue.","I cannot find it.","Here you are."]),
            ("A: May I use your pen? B: ( )","Of course.",["I used it yesterday.","It is Monday.","You are welcome."]),
            ("A: Would you like some tea? B: ( )","Yes, please.",["At the station.","For three years.","See you yesterday."]),
            ("A: I have a headache. B: ( )","You should get some rest.",["You are welcome.","It is ten o clock.","I like baseball."]),
            ("A: Could you open the window? B: ( )","Certainly.",["I opened it yesterday.","It is a window.","No, I am not."]),
            ("A: What do you think of this book? B: ( )","I think it is interesting.",["It costs five minutes.","I bought it tomorrow.","You are welcome."]),
            ("A: I cannot find my notebook. B: ( )","Let us look for it together.",["You are welcome.","It was sunny.","I am good at math."]),
            ("A: How was your school trip? B: ( )","It was a lot of fun.",["At six o clock.","For three years.","I am going to school."]),
            ("A: Could you tell me the time? B: ( )","It is half past three.",["At the library.","I am thirteen years old.","You are welcome."]),
            ("A: I lost my wallet, {name}. B: ( )","I am sorry to hear that.",["Congratulations!","You are welcome.","At half past five."]),
            ("A: I passed the entrance exam! B: ( )","Congratulations!",["I am sorry to hear that.","You are welcome.","It is next to the bank."]),
            ("A: I am going to visit Kyoto this weekend. B: ( )","Have a nice trip!",["You are welcome.","I am sorry to hear that.","It is ten yen."]),
            ("A: I finished my homework, {name}. B: ( )","Well done!",["I am sorry to hear that.","Here is your ticket.","At seven o clock."]),
            ("A: Would you like to join our study group? B: ( )","Yes, I would love to.",["I went there last week.","It is very expensive.","You are welcome."]),
            ("A: How about playing badminton after school? B: ( )","Sounds fun.",["I am sorry to hear that.","It is on the desk.","I have two sisters."]),
            ("A: I do not understand this math problem. B: ( )","Let me help you.",["You are welcome.","It was yesterday.","I am thirteen years old."]),
            ("A: Could you carry this box for me? B: ( )","Sure, no problem.",["I am sorry to hear that.","It costs five minutes.","See you last week."]),
            ("A: Can I borrow your umbrella, {name}? B: ( )","Sure. Here you are.",["You are welcome.","I went there yesterday.","It is half past three."]),
            ("A: My phone battery is dead. B: ( )","You can use my charger.",["Congratulations!","I am thirteen years old.","You are welcome."]),
            ("A: I missed the bus this morning. B: ( )","That is too bad.",["You are welcome.","Here is your ticket.","I like reading books."]),
            ("A: It is very hot outside. B: ( )","Let us get some cold water.",["I am sorry to hear that.","It is on Monday.","You are welcome."]),
            ("A: I want to visit the science museum. B: ( )","That sounds interesting.",["I am sorry to hear that.","At six o clock.","You are welcome."]),
            ("A: Shall we meet at the library at three? B: ( )","Okay, see you then.",["I am sorry to hear that.","It costs five minutes.","You are welcome."]),
            ("A: Thank you for inviting me, {name}. B: ( )","I am glad you can come.",["I am sorry to hear that.","At the station.","I went yesterday."]),
            ("A: I am nervous about my interview. B: ( )","Just do your best.",["You are welcome.","It is next Tuesday.","I am sorry I am late."]),
            ("A: I got a new puppy yesterday. B: ( )","How nice!",["I am sorry to hear that.","You are welcome.","It is half past three."]),
            ("A: I do not feel well today. B: ( )","You should tell your teacher.",["Congratulations!","I bought it tomorrow.","You are welcome."]),
            ("A: Could you repeat that, please? B: ( )","Sure, I will say it again.",["I am sorry to hear that.","At the bus stop.","You are welcome."]),
            ("A: I forgot to bring my homework. B: ( )","Please talk to your teacher.",["Congratulations!","It costs five minutes.","You are welcome."]),
            ("A: Would you like to join us for lunch? B: ( )","Yes, I would like to.",["I am sorry to hear that.","At six o clock.","I went there yesterday."]),
            ("A: I won the tennis match! B: ( )","Congratulations!",["I am sorry to hear that.","You are welcome.","It is under the desk."]),
            ("A: The movie was great. B: ( )","I am glad you enjoyed it.",["I am sorry to hear that.","At seven o clock.","You are welcome."]),
            ("A: It is my birthday today. B: ( )","Happy birthday!",["I am sorry to hear that.","You are welcome.","It is on the desk."]),
            ("A: I cannot come to your party. B: ( )","I am sorry to hear that.",["Congratulations!","You are welcome.","It is half past three."]),
            ("A: I am going to the dentist tomorrow. B: ( )","I hope it goes well.",["You are welcome.","At the station.","I went there yesterday."]),
            ("A: What do you want to be in the future? B: ( )","I want to be a nurse.",["At six o clock.","For three years.","You are welcome."]),
            ("A: How long have you lived here? B: ( )","For five years.",["At the station.","It is ten yen.","I went there tomorrow."]),
            ("A: Which do you prefer, tea or coffee? B: ( )","I prefer tea.",["At half past three.","You are welcome.","I am sorry to hear that."]),
            ("A: Can I sit here? B: ( )","Yes, this seat is free.",["I am sorry to hear that.","It is five years old.","You are welcome."]),
            ("A: Thank you for your advice, {name}. B: ( )","You are welcome.",["Congratulations!","At the station.","I am sorry I am late."]),
            ("A: I am sorry I broke your ruler. B: ( )","Do not worry about it.",["Congratulations!","At six o clock.","You are welcome."]),
            ("A: I am hungry. B: ( )","Let us have lunch.",["I am sorry to hear that.","It is on the desk.","You are welcome."]),
            ("A: Let us take a walk after dinner. B: ( )","Good idea.",["I am sorry to hear that.","At the station.","You are welcome."]),
            ("A: How was the concert last night? B: ( )","It was amazing.",["At six o clock.","For three years.","You are welcome."]),
            ("A: I need to study for the exam. B: ( )","I can help you review.",["I am sorry to hear that.","It costs five minutes.","You are welcome."]),
            ("A: I am looking for a gift for my sister. B: ( )","How about a book?",["I am sorry to hear that.","At seven o clock.","You are welcome."]),
            ("A: I have never been to Hokkaido. B: ( )","You should visit it someday.",["I am sorry to hear that.","It is ten yen.","You are welcome."]),
            ("A: Would you like to play soccer after school? B: ( )","Sure, I would love to.",["I am sorry to hear that.","At the station.","You are welcome."]),
            ("A: Thank you for showing me the way. B: ( )","No problem.",["I am sorry to hear that.","It is Monday.","Congratulations!"]),
            ("A: I do not know how to use this app. B: ( )","Let me show you.",["You are welcome.","It is half past three.","I went there yesterday."]),
            ("A: I am sorry for the noise, {name}. B: ( )","Do not worry about it.",["Congratulations!","At the station.","You are welcome."]),
            ("A: Can you help me with this question? B: ( )","Of course. Let us try it together.",["I am sorry to hear that.","At six o clock.","You are welcome."]),
            ("A: I am going to visit my grandparents this weekend. B: ( )","Have a nice time!",["I am sorry to hear that.","It is on the desk.","You are welcome."]),
            ("A: I have a cold today. B: ( )","I hope you feel better soon.",["Congratulations!","At the station.","You are welcome."]),
            ("A: I missed the train, {name}. B: ( )","That is too bad.",["Congratulations!","You are welcome.","It is ten yen."]),
            ("A: I need a dictionary for class. B: ( )","You can borrow mine.",["I am sorry to hear that.","At seven o clock.","Congratulations!"]),
            ("A: Do you have any plans for the weekend? B: ( )","I am going to visit my cousin.",["At half past three.","You are welcome.","It is ten yen."])
        ]
        stem, answer, wrong = r.choice(scenarios)
        stem = stem.format(name=name)
        return stem,[answer]+wrong,answer
    if kind == 'reading':
        name=r.choice(['Mika','Ken','Yuta','Hana','Emi','Rina','Sota','Aki'])
        p,reason=r.choice([('library','study for a test'),('museum','learn history'),('park','join a cleanup'),('station','meet a friend'),('shop','buy a gift'),('community center','practice music'),('beach','collect trash'),('science museum','see an exhibition'),('bookstore','buy a dictionary'),('gym','play basketball')])
        stem=r.choice([f'{name} went to the {p} to {reason}. Why did {name} go there?',f'{name} visited the {p} because {name} wanted to {reason}. What was the purpose of the visit?'])
        return stem,[f'To {reason}.','To play tennis.','To cook dinner.','To watch TV.'],f'To {reason}.'
    if kind == 'schedule':
        mode=r.randrange(5)
        fmt=lambda v:f'{v//60}:{v%60:02d}'
        if mode==0:
            start=r.randrange(8*60,10*60,5); gap=r.choice([10,15,20])
            t=[start+i*gap for i in range(4)]; arrive=t[1]+r.randrange(1,gap)
            answer=fmt(t[2])
            return f'Buses: {", ".join(map(fmt,t))}. You arrive at {fmt(arrive)}. Next bus?',[answer,fmt(t[0]),fmt(t[1]),fmt(t[3])],answer
        if mode==1:
            start=r.randrange(8*60,10*60,10); gap=r.choice([10,15,20])
            t=[start+i*gap for i in range(4)]; arrive=t[0]+r.randrange(1,gap)
            answer=fmt(t[1])
            return f'Trains leave at {", ".join(map(fmt,t))}. You reach the platform at {fmt(arrive)}. Which train can you catch first?',[answer,fmt(t[0]),fmt(t[2]),fmt(t[3])],answer
        if mode==2:
            start=r.randrange(9*60,15*60,10); duration=r.choice([35,45,50,60,75]); end=start+duration
            answer=f'{duration} minutes'
            return f'A school event starts at {fmt(start)} and finishes at {fmt(end)}. How long does it last?',[answer,f'{duration+10} minutes',f'{duration-10} minutes',f'{duration*2} minutes'],answer
        if mode==3:
            start=r.randrange(8*60,10*60,10); gap=r.choice([12,15,20])
            t=[start+i*gap for i in range(4)]; arrive=t[2]-r.randrange(1,gap); answer=fmt(t[2])
            return f'A shuttle departs at {", ".join(map(fmt,t))}. If you arrive at {fmt(arrive)}, what is the next departure?',[answer,fmt(t[0]),fmt(t[1]),fmt(t[3])],answer
        start=r.randrange(13*60,16*60,5); duration=r.choice([80,90,100,110]); end=start+duration; answer=fmt(end)
        return f'A film begins at {fmt(start)} and lasts {duration} minutes. When does it end?',[answer,fmt(end+30),fmt(end-30),fmt(start+duration*2)],answer
    if kind == 'fee':
        mode=r.randrange(6)
        if mode==0:
            student=r.randrange(200,600,50); adult=student+r.randrange(200,450,50); n=r.choice([2,3,4])
            total=student+adult*n
            stem=f'Tickets: student {student} yen, adult {adult} yen. One student and {n} adults: total?'
            answer=str(total); choices=[answer,str(total-adult),str(total+adult),str(total+student)]
        elif mode==1:
            child=r.randrange(150,401,50); adult=child+r.randrange(200,401,50)
            total=2*child+2*adult
            stem=f'At a museum, a child ticket costs {child} yen and an adult ticket costs {adult} yen. What is the total for two children and two adults?'
            answer=f'{total} yen'; choices=[answer,f'{total-child} yen',f'{total+child} yen',f'{total+adult} yen']
        elif mode==2:
            student=r.randrange(250,601,50); adult=student+r.randrange(150,401,50)
            diff=adult-student
            stem=f'An adult ticket costs {adult} yen and a student ticket costs {student} yen. How much more is the adult ticket?'
            answer=f'{diff} yen'; choices=[answer,f'{student} yen',f'{adult} yen',f'{adult+student} yen']
        elif mode==3:
            adult=r.randrange(500,1001,100); student=r.randrange(200,501,50); n=r.choice([2,3,4])
            total=2*adult+n*student
            stem=f'A group buys two adult tickets at {adult} yen each and {n} student tickets at {student} yen each. How much do they pay?'
            answer=f'{total} yen'; choices=[answer,f'{total+student} yen',f'{total-adult} yen',f'{adult+n*student} yen']
        elif mode==4:
            price=r.randrange(300,901,50); count=r.choice([2,3,4]); total=price*count
            stem=f'Each ticket costs {price} yen. A family buys {count} tickets. What is the total cost?'
            answer=f'{total} yen'; choices=[answer,f'{total-price} yen',f'{total+price} yen',f'{price+count} yen']
        else:
            adult=r.randrange(600,1001,100); discount=r.choice([100,150,200,250]); student=adult-discount
            count=r.choice([2,3,4]); total=student*count
            stem=f'An adult ticket costs {adult} yen. A student ticket is {discount} yen cheaper. How much do {count} students pay in total?'
            answer=f'{total} yen'; choices=[answer,f'{total+discount} yen',f'{total-discount} yen',f'{adult*count} yen']
        return stem,choices,answer
    if kind == 'relative':
        mode=r.randrange(4)
        if mode==0:
            name=r.choice(['Ken','Emi','Hana','Rina','Yuta','Sota','Mika','Aki'])
            job=r.choice(['teacher','doctor','scientist','artist','engineer','writer','nurse','cook'])
            city=r.choice(['Yokohama','Kamakura','Fujisawa','Odawara','Kawasaki','Sagamihara','Chigasaki'])
            article='an' if job[0].lower() in 'aeiou' else 'a'
            return f'{name} knows {article} {job} ( ) works in {city}.',['who','where','when','whose'],'who'
        if mode==1:
            return 'The woman ( ) lives next door is a doctor.',['who','where','when','whose'],'who'
        if mode==2:
            return 'This is the book ( ) I bought yesterday.',['that','who','where','when'],'that'
        return 'I visited a town ( ) has a famous castle.',['which','who','when','where'],'which'
    if kind == 'passive':
        mode=r.randrange(6)
        if mode==0:
            name=r.choice(['bridge','school','museum','library','station']); year=r.randrange(1980,2020)
            return f'The {name} was ( ) in {year}.',['built','build','building','builds'],'built'
        if mode==1:
            return 'The letter was ( ) by Ken yesterday.',['written','wrote','write','writing'],'written'
        if mode==2:
            return 'This song was ( ) by a Japanese composer.',['composed','compose','composing','composes'],'composed'
        if mode==3:
            return 'English is ( ) in many countries.',['spoken','speak','speaking','speaks'],'spoken'
        if mode==4:
            return 'The picture was ( ) by Mika last week.',['drawn','drew','draw','drawing'],'drawn'
        return 'The first telephone was ( ) by Alexander Graham Bell.',['invented','invent','inventing','invents'],'invented'
    if kind == 'if':
        event=r.choice(['sports day','picnic','beach cleanup','school trip','soccer game','outdoor concert','class trip','tennis match'])
        day=r.choice(['Saturday','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday'])
        name=r.choice(['Mika','Ken','Yuta','Rina','Emi','Hana','Sota','Aki'])
        stem=r.choice([f'If it ( ) on {day}, {name} will cancel the {event}.',f'If it ( ) this weekend, {name} will move the {event} indoors.',f'{name} will cancel the {event} if it ( ) on {day}.'])
        return stem,['rains','will rain','rained','raining'],'rains'
    if kind == 'data':
        mode=r.randrange(4)
        if mode==0:
            days=r.sample(['Mon','Tue','Wed','Thu','Fri'],3); nums=r.sample(range(80,240,5),3)
            winner=days[nums.index(max(nums))]
            return 'Visitors: '+', '.join(f'{d} {n}' for d,n in zip(days,nums))+'. Which day had the most?',[winner]+[d for d in days if d!=winner]+['Equal'],winner
        if mode==1:
            clubs=r.sample(['soccer','tennis','music','art','science','drama'],4); counts=r.sample(range(8,31,2),4)
            winner=clubs[counts.index(max(counts))]
            return 'Club survey: '+', '.join(f'{c} {n}' for c,n in zip(clubs,counts))+'. Which club had the most members?',[winner]+[c for c in clubs if c!=winner],winner
        if mode==2:
            days=r.sample(['Mon','Tue','Wed','Thu','Fri'],4); nums=r.sample(range(70,201,10),4)
            lowest=days[nums.index(min(nums))]
            return 'Daily rainfall (mm): '+', '.join(f'{d} {n}' for d,n in zip(days,nums))+'. Which day had the least rain?',[lowest]+[d for d in days if d!=lowest],lowest
        scores=r.sample(range(55,101,5),3); names=r.sample(['Mika','Ken','Yuta','Rina','Emi','Hana'],3)
        best=names[scores.index(max(scores))]
        return 'Test scores: '+', '.join(f'{n} {v}' for n,v in zip(names,scores))+'. Who got the highest score?',[best]+[n for n in names if n!=best]+['All the same'],best
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
            climates=[('太平洋側','冬に晴天が多く乾燥しやすい'),('日本海側','冬に雪や雨が多い'),('瀬戸内','降水量が比較的少ない'),('中央高地','内陸で年較差が大きい'),('北海道','冷涼で梅雨の影響が比較的小さい'),('南西諸島','一年を通じて温暖で台風の影響を受けやすい'),('東北地方','冬の寒さが厳しく、日本海側では雪が多い'),('南四国','黒潮の影響を受け温暖で降水量が多い')]
            climate=r.choice(climates)
            if r.choice([True,False]):
                stem=f'日本の気候区分で「{climate[0]}」の特徴は？'
                options=[climate[1],'一年中ほぼ毎日同じ量の雨が降る','年間を通じて気温が常に30℃を超える','冬でも必ず台風が上陸する']
                return stem,options,climate[1]
            stem=f'「{climate[1]}」という特徴がみられる地域は？'
            regions=[x[0] for x in climates if x[0]!=climate[0]]
            options=[climate[0]]+r.sample(regions,3)
            return stem,options,climate[0]
        if mode==3:
            crops=[('北海道','てんさい'),('新潟平野','米'),('高知平野','促成栽培の野菜'),('鹿児島','畜産'),('長野県','高原野菜'),('沖縄県','さとうきび'),('青森県','りんご'),('山梨県','ぶどう'),('静岡県','茶'),('群馬県','こんにゃくいも'),('千葉県','落花生'),('愛媛県','みかん'),('熊本県','すいか'),('宮崎県','きゅうりの促成栽培'),('北海道十勝地方','大規模な畑作'),('三重県','養殖真珠'),('広島県','かきの養殖'),('富山平野','米'),('鳥取県','らっきょう'),('福井県','米'),('岩手県','肉用牛'),('和歌山県','うめ'),('栃木県','いちご'),('茨城県','れんこん'),('佐賀平野','米'),('徳島県','すだち'),('長崎県','じゃがいも'),('奈良県','柿'),('福岡県','いちご'),('石川県','米')]
            crop=r.choice(crops)
            stem=r.choice([f'「{crop[1]}」の生産がさかんな地域はどこ？',f'農業の地域差について、「{crop[1]}」と結びつきが強い地域を選びなさい。'])
            distractors=[x[0] for x in crops if x[0]!=crop[0] and x[1]!=crop[1]]
            options=[crop[0]]+r.sample(distractors,3)
            return stem,options,crop[0]
        if mode==4:
            resources=[('瀬戸内海沿岸','造船・鉄鋼などの工業'),('京浜工業地帯','機械・化学などの工業'),('中京工業地帯','自動車工業'),('北九州工業地域','かつての製鉄業'),('阪神工業地帯','機械・化学・金属工業'),('京葉工業地域','石油化学工業'),('東海地方','自動車・楽器などの工業'),('北陸地方','化学・機械などの工業'),('瀬戸内工業地域','石油化学・造船'),('鹿島臨海工業地域','石油化学・鉄鋼')]
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
        fmt=r.randrange(10)
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
        elif fmt==7:
            stem=f'地形の特徴を表す資料「{meaning}」から判断できる地形名は？'
        elif fmt==8:
            stem=f'日本の地理に関する問いです。「{meaning}」を表す地形用語は？'
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
        stem=r.choice([
            f'{year}年の出来事として正しいものは？',
            f'次のうち、{year}年に起きた出来事は？',
            f'日本史で{year}年の出来事として正しいものを選びなさい。',
            f'年表の{year}年にあたる出来事はどれ？',
            f'年代を確認し、{year}年の出来事を選びなさい。',
            f'次の出来事のうち、{year}年に該当するものは？',
            f'歴史資料に示された{year}年の出来事は？',
            f'日本史の年代問題です。{year}年にあったことは？',
            f'「{year}年」の欄に入る出来事を選びなさい。',
            f'歴史の流れから、{year}年に起きたことを選びなさい.'
        ])
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
        mode=r.randrange(7)
        if mode==0:
            seats=r.randrange(60,451,10); votes=(2*seats+2)//3
            stem=r.choice([f'衆議院の出席議員{seats}人。法律案再可決に必要な賛成の最少数は？',f'出席議員が{seats}人の衆議院で、法律案を再可決するには最低何人の賛成が必要？'])
            return stem,[str(votes),str(seats//2),str(seats//3),str(seats-1)],str(votes)
        if mode==1:
            return '参議院が否決した法律案を衆議院で再可決するには、出席議員の何分の何以上の賛成が必要？',['3分の2以上','過半数','3分の1以上','全員一致'],'3分の2以上'
        if mode==2:
            return '日本で司法権を担当する機関はどれですか。',['裁判所','国会','内閣','地方議会'],'裁判所'
        if mode==3:
            return '住民が条例の制定・改廃などを求める地方自治の制度は？',['直接請求','国政調査権','違憲審査制','議院内閣制'],'直接請求'
        if mode==4:
            return '日本の国政選挙で投票できる年齢は原則何歳以上ですか。',['18歳','16歳','20歳','21歳'],'18歳'
        if mode==5:
            return '法律や命令が憲法に違反していないかを裁判所が判断する権限は？',['違憲審査権','国政調査権','条例制定権','予算編成権'],'違憲審査権'
        return '内閣総理大臣を指名する機関はどれですか。',['国会','最高裁判所','都道府県知事','日本銀行'],'国会'
    if kind == 'population':
        mode=r.randrange(4)
        young=r.randrange(9,19); old=r.randrange(22,38); work=100-young-old
        if mode==0:
            return f'人口構成：15歳未満{young}％、15～64歳{work}％、65歳以上{old}％。最大の層は？',['15～64歳','15歳未満','65歳以上','すべて同じ'],'15～64歳'
        if mode==1:
            diff=old-young
            return f'ある地域では15歳未満が{young}％、65歳以上が{old}％である。高齢者の割合は子どもの割合より何ポイント高い？',[f'{diff}ポイント',f'{old+young}ポイント',f'{young}ポイント',f'{old}ポイント'],f'{diff}ポイント'
        if mode==2:
            return f'年齢別人口：15歳未満{young}％、15～64歳{work}％、65歳以上{old}％。最も割合が小さい層は？',['15歳未満','15～64歳','65歳以上','すべて同じ'],'15歳未満'
        return f'高齢者が人口の{old}％、子どもが{young}％を占める地域がある。どちらの割合が大きい？',['65歳以上','15歳未満','同じ','資料だけでは分からない'],'65歳以上'
    if kind == 'trade':
        mode=r.randrange(6)
        if mode==0:
            ex=r.randrange(105,155,5); im=r.randrange(60,100,5)
            return f'輸出指数100→{ex}、輸入指数100→{im}。正しい説明は？',['輸出増・輸入減','両方増加','輸出減・輸入増','両方減少'],'輸出増・輸入減'
        if mode==1:
            ex=r.randrange(110,151,5); im=r.randrange(105,146,5)
            return f'ある年の輸出指数は100から{ex}へ、輸入指数は100から{im}へ変化した。両方について正しい説明は？',['輸出入とも増加','輸出増・輸入減','輸出減・輸入増','両方減少'],'輸出入とも増加'
        if mode==2:
            ex=r.randrange(70,96,5); im=r.randrange(105,136,5)
            return f'輸出指数が100から{ex}に下がり、輸入指数が100から{im}に上がった。どの変化が起きた？',['輸出減・輸入増','輸出増・輸入減','輸出入とも増加','変化なし'],'輸出減・輸入増'
        if mode==3:
            ex=r.randrange(120,181,10); im=r.randrange(70,100,10)
            return f'輸出額の指数が{ex}、輸入額の指数が{im}（基準年はいずれも100）である。基準年と比べた説明は？',['輸出は増え、輸入は減った','輸出は減り、輸入は増えた','輸出入とも減った','輸出入とも変化なし'],'輸出は増え、輸入は減った'
        if mode==4:
            exports=r.randrange(120,301,20); imports=exports-r.randrange(20,101,20)
            return f'ある国の輸出額が{exports}億円、輸入額が{imports}億円だった。貿易収支はどの状態？',['貿易黒字','貿易赤字','必ず均衡','判断できない'],'貿易黒字'
        return '輸入額が輸出額を上回っている状態を何といいますか。',['貿易赤字','貿易黒字','財政黒字','経常黒字'],'貿易赤字'
    if kind == 'exchange':
        mode=r.randrange(6)
        if mode==0:
            a=r.choice(list(range(100,181,5))); b=a-r.choice([5,10,15,20,25,30])
            stem=r.choice([f'為替が1ドル{a}円から{b}円に変化した。これは？',f'1ドルあたり{a}円だった為替相場が{b}円になった。この変化を何という？'])
            return stem,['円高・ドル安','円安・ドル高','変化なし','必ず物価が2倍'],'円高・ドル安'
        if mode==1:
            a=r.choice(list(range(100,161,5))); b=a+r.choice([5,10,15,20,25,30])
            return f'1ドル{a}円から{b}円に変化したとき、円とドルの関係は？',['円安・ドル高','円高・ドル安','変化なし','円とドルが同じ価値'],'円安・ドル高'
        if mode==2:
            return '円高が進むと、一般に海外から輸入する商品の円建て価格はどうなりやすいですか。',['安くなりやすい','高くなりやすい','必ず2倍になる','輸入できなくなる'],'安くなりやすい'
        if mode==3:
            return '円安が進んだとき、日本から海外旅行に行く人の外貨購入費用は一般にどうなりやすい？',['高くなりやすい','安くなりやすい','必ず無料になる','変化しない'],'高くなりやすい'
        if mode==4:
            return '1ドルを買うのに必要な円が120円から100円に減った。この変化は？',['円高','円安','物価上昇だけ','為替変動なし'],'円高'
        return '円安とは、外国通貨1単位を買うために必要な円が一般にどうなることですか。',['多くなる','少なくなる','ゼロになる','必ず変わらない'],'多くなる'
    if kind == 'disaster':
        settings=[
            ('相模川沿い','flood'),('酒匂川沿い','flood'),('境川沿い','flood'),
            ('鶴見川沿い','flood'),('多摩川沿い','flood'),('河口付近の低地','flood'),
            ('海岸近く','coastal'),('急傾斜地の近く','landslide'),('山間部','landslide')
        ]
        area,hazard=r.choice(settings)
        weather=r.choice(['台風','大雨','長雨','線状降水帯による豪雨','大雨と満潮'])
        if hazard=='landslide':
            concern=('土砂災害警戒区域と避難経路','土砂災害')
        elif hazard=='coastal':
            concern=('高潮・浸水の想定区域と避難場所','高潮や浸水')
        else:
            concern=('浸水想定区域と避難場所','洪水')
        stem=r.choice([f'{weather}時に{area}で{concern[1]}に備え、ハザードマップで確認すべきことは？',f'{area}の住民が{weather}による{concern[1]}の危険を確認するには、ハザードマップのどこを見る？'])
        return stem,[concern[0],'選挙区','税率','輸出額'],concern[0]
    if kind == 'budget':
        a=r.randrange(25,38); b=r.randrange(10,20); c=r.randrange(8,16)
        mode=r.randrange(5)
        if mode==0:
            return f'歳出：社会保障{a}％、教育{b}％、公共事業{c}％。最も大きい項目は？',['社会保障','教育','公共事業','同率'],'社会保障'
        if mode==1:
            total=a+b
            return f'歳出のうち社会保障が{a}％、教育が{b}％である。2項目の合計は何％？',[f'{total}％',f'{a-b}％',f'{total+10}％',f'{c}％'],f'{total}％'
        if mode==2:
            if c==b:
                c = c-1 if c>8 else c+1
            answer='公共事業' if c<b else '教育'
            return f'資料：社会保障{a}％、教育{b}％、公共事業{c}％。最も割合が小さい項目は？',['公共事業','教育','社会保障','すべて同じ'],answer
        if mode==3:
            diff=a-b
            return f'社会保障費の割合は{a}％、教育費は{b}％である。社会保障費は何ポイント高い？',[f'{diff}ポイント',f'{a+b}ポイント',f'{b}ポイント',f'{a}ポイント'],f'{diff}ポイント'
        total=a+b+c
        return f'資料の3項目：社会保障{a}％、教育{b}％、公共事業{c}％。合計は何％？',[f'{total}％',f'{a+b}％',f'{total+10}％',f'{a+c}％'],f'{total}％'
    if kind == 'tense':
        mode=r.randrange(5)
        if mode==0:
            name=r.choice(['Mika','Ken','Yuta','Rina','Emi','Hana','Sota','Aki'])
            activity=r.choice(['the museum','soccer','a letter','dinner','the piano','a book'])
            time=r.choice(['yesterday','last Sunday','two days ago','last night'])
            verb={'the museum':'visit','soccer':'play','a letter':'write','dinner':'cook','the piano':'practice','a book':'read'}[activity]
            past={'visit':'visited','play':'played','write':'wrote','cook':'cooked','practice':'practiced','read':'read'}[verb]
            return f'{name} ( ) {activity} {time}.',['visits',past,'has visited','visiting'],past
        if mode==1:
            return 'Have you ever ( ) to Hokkaido?',['been','went','go','being'],'been'
        if mode==2:
            return 'They ( ) the science museum yesterday.',['visited','visit','have visited','visiting'],'visited'
        if mode==3:
            return 'We ( ) our grandparents next Sunday.',['will visit','visited','have visited','visiting'],'will visit'
        return 'When I called Mika, she ( ) dinner.',['was cooking','cooked','cooks','is cooking'],'was cooking'
    if kind == 'conjunction':
        a,b=r.choice([('It was raining','we stayed home'),('Mika was tired','she went to bed early'),('Ken studied hard','he passed the test'),('The bag was heavy','I carried it carefully')])
        good=r.choice(['so','because','although','unless'])
        if good=='because':
            stem=f'{b.capitalize()} ( ) {a}.'
            answer='because'
        elif good=='although':
            stem=f'( ) it was difficult, Ken finished the work.'
            answer='Although'
        elif good=='unless':
            stem='You cannot enter ( ) you have a ticket.'
            answer='unless'
        else:
            stem=f'{a}, ( ) {b}.'
            answer='so'
        opts=[answer, 'but' if answer.lower()!='but' else 'so', 'unless' if answer.lower()!='unless' else 'because', 'although' if answer.lower()!='although' else 'and']
        frame=r.choice(['Choose the best conjunction to complete the sentence.','Select the word that best connects the ideas.','Which conjunction makes the sentence natural?','Complete the sentence with the most suitable word.','Choose the correct connecting word.','Read the sentence and select the best answer.','Which word best expresses the relationship between the clauses?','Select the most appropriate conjunction.','Choose the word that completes the sentence logically.','Which option best connects the two parts?','Pick the conjunction that fits the meaning.','Complete the sentence using the correct connector.'])
        return frame+' '+stem,opts,answer
    if kind == 'word_order':
        name=r.choice(['Mika','Ken','Yuta','Rina','Emi','Hana'])
        obj=r.choice(['English','science','history','math','music','sports','art','geography'])
        correct=f'{name} is interested in {obj}.'
        stem=r.choice([f'Choose the correctly ordered sentence: {name} / interested / is / in / {obj}.',f'Put the words in the correct order to make a sentence: {name} / is / in / interested / {obj}.'])
        return stem,[correct,f'{name} interested is in {obj}.',f'Is {name} in interested {obj}.',f'{name} is in {obj} interested.'],correct
    if kind == 'infinitive':
        mode=r.randrange(5)
        if mode==0:
            name=r.choice(['Mika','Ken','Yuta','Rina','Emi','Hana','Sota','Aki'])
            place,verb=r.choice([('the museum','visit'),('English','study'),('a letter','write'),('a cake','make'),('the guitar','play'),('a new song','sing'),('the park','visit'),('dinner','cook')])
            return f'{name} wants ( ) {place}.',['to '+verb,verb,verb+'ing',verb+'ed'],'to '+verb
        if mode==1:
            return 'It is important ( ) English every day.',['to study','studying','study','studied'],'to study'
        if mode==2:
            return 'Ken went to the library ( ) a book.',['to borrow','borrow','borrowing','borrowed'],'to borrow'
        if mode==3:
            return 'I have a lot of homework ( ) tonight.',['to do','doing','do','did'],'to do'
        return 'She was happy ( ) you again.',['to see','seeing','saw','see'],'to see'
    if kind == 'pronoun':
        name,answer=r.choice([('Tom','him'),('Mary','her'),('the children','them'),('my brother','him'),('my sister','her'),('Mr. Sato','him'),('Ms. Sato','her'),('the players','them'),('the visitors','them'),('my aunt','her'),('the students','them')])
        # The object referred to by "it" must be singular or uncountable.
        obj=r.choice(['the present','the book','the message','the invitation','the key','the homework'])
        sentence_name=name[0].upper()+name[1:]
        stem=r.choice([f'I gave {obj} to {name}. I gave it to ( ).',f'{sentence_name} needed {obj}, so I gave it to ( ).',f'I sent {obj} to {name}. I sent it to ( ).'])
        return stem,[answer,'he' if answer=='him' else 'she' if answer=='her' else 'they','his','themselves'],answer
    if kind == 'preposition':
        place=r.choice(['the station','the library','the airport','school','the museum','the hospital','the park','the city hall'])
        time=r.choice(['at eight','in the morning','on Monday','at noon','last night','at six thirty','on Friday','in the afternoon'])
        stem=r.choice([f'We arrived ( ) {place} {time}.',f'They arrived ( ) {place} {time}.'])
        return stem,['at','in','on','for'],'at'
    if kind == 'modal':
        action=r.choice(['wear a helmet','follow the rules','be quiet in the library','help people in need','keep the room clean','check the traffic light before crossing','save water when possible','return books on time','listen carefully to others','protect the environment','use a seat belt','wash your hands before eating','tell the truth','keep your password private','recycle paper and cans','take care of public property','arrive on time for class','turn off unused lights','respect different opinions','ask for help when necessary'])
        stem=r.choice([f'You ( ) {action}. It is the right thing to do.',f'In this situation, you ( ) {action}.',f'For safety, people ( ) {action}.'])
        return stem,['should','would','might','could have'],'should'
    if kind == 'indirect':
        place=r.choice(['the library','the station','the city museum','the nearest bus stop','the post office','the science museum','the city hall','the public pool','the art gallery','the community center','the nearest pharmacy','the bus terminal','the train platform','the school gym','the sports center','the history museum','the concert hall','the information desk','the bookshop','the town office','the nearest bank','the police station','the aquarium','the botanical garden','the shopping center','the local hospital','the ferry port','the language school','the tourist office','the nearest restroom','the main entrance','the conference room','the music room','the swimming pool','the ticket counter','the post office near here','the nearest park','the city library','the train station exit','the meeting room'])
        return f'A visitor asks about {place}: Could you tell me ( )?', [f'where {place} is',f'where is {place}',f'where does {place}',f'where {place}'],f'where {place} is'
    if kind == 'superlative':
        mode=r.randrange(4)
        if mode==0:
            names=r.sample(['Ken','Yuta','Mika','Emi','Hana','Sota','Rina','Aki'],3)
            heights=r.sample(range(145,181,5),3); tallest=names[heights.index(max(heights))]
            data=', '.join(f'{n}: {h} cm' for n,h in zip(names,heights))
            return f'Heights ({data}). Who is the tallest?',[tallest]+[n for n in names if n!=tallest]+['They are equal'],tallest
        if mode==1:
            return 'Of the three books, this one is the ( ).',['most interesting','more interesting','interesting','as interesting'],'most interesting'
        if mode==2:
            names=r.sample(['Mika','Ken','Yuta','Rina','Emi','Hana'],3); times=r.sample(range(12,31),3)
            fastest=names[times.index(min(times))]; data=', '.join(f'{n}: {t} seconds' for n,t in zip(names,times))
            return f'Race times ({data}). Who ran the fastest?',[fastest]+[n for n in names if n!=fastest]+['They tied'],fastest
        return 'Choose the sentence that correctly compares three places.',['Mount A is the highest of the three.','Mount A is higher than all the three.','Mount A is the most high.','Mount A is as highest as B.'],'Mount A is the highest of the three.'
    if kind == 'dialogue_intent':
        stem,answer,wrong=r.choice([
            ('A: Thank you for helping me. B: ( )','You are welcome.',['I am sorry.','Here you are.','Good luck yesterday.']),
            ('A: I am sorry I am late. B: ( )','That is all right.',['You are welcome.','See you tomorrow.','Here is your ticket.']),
            ('A: Would you like some tea? B: ( )','Yes, please.',['I am twelve.','At the station.','It is Monday.']),
            ('A: How was your weekend? B: ( )','It was great.',['At seven o’clock.','I am fine, thank you.','Two kilometers.'])
        ])
        frame=r.choice(['Choose the most natural response.','Select the best reply for the conversation.','Which response fits the situation?','Choose the appropriate answer for B.','What should B say next?','Pick the most suitable reply.','Which sentence completes the dialogue naturally?','Choose the best response in this conversation.','What is the most appropriate thing for B to say?','Select the reply that matches A’s words.','Which answer makes the conversation natural?','Complete the short dialogue with the best response.'])
        return frame+' '+stem,[answer]+wrong,answer
    if kind == 'world_region':
        country,feature=r.choice([('Brazil','アマゾン川流域の熱帯雨林'),('Egypt','ナイル川'),('Australia','グレートバリアリーフ'),('India','モンスーンの影響を受ける気候'),('Canada','広い針葉樹林帯'),('Saudi Arabia','高温で乾燥した砂漠気候')])
        stem=r.choice([f'{country}と関連が深い地理的特徴はどれ？',f'世界地理の資料にある{country}の特徴として正しいものは？',f'{country}の自然環境を説明したものはどれ？',f'{country}について、自然や気候の特徴として適切なものは？',f'次のうち{country}に結びつく地理的特色はどれ？',f'{country}の地理に関する説明として正しいものを選びなさい。',f'{country}で見られる自然環境として最も適切なものは？'])
        return stem,[feature,'国土全体が永久凍土に覆われる','季節による気候の変化がない','国土全体が南極海にある'],feature
    if kind == 'map_scale':
        mode=r.randrange(6)
        if mode==0:
            cm=r.randrange(2,41); scale=50000; km=cm*scale/100000
            good=f'{km:g} km'
            return f'縮尺1:{scale:,}の地図で2地点が{cm}cm離れている。実際の距離は？',[good,f'{km*10:g} km',f'{km/5:g} km',f'{km+3:g} km'],good
        if mode==1:
            cm=r.randrange(2,41); scale=25000; km=cm*scale/100000
            good=f'{km:g} km'
            return f'縮尺1:{scale:,}の地図上で2地点の間が{cm}cmだった。現地での距離は？',[good,f'{km*2:g} km',f'{km/2:g} km',f'{km+5:g} km'],good
        if mode==2:
            km=r.choice([1,1.5,2,2.5,3,4,5]); scale=50000; cm=km*100000/scale
            good=f'{cm:g} cm'
            return f'縮尺1:{scale:,}の地図で、実際に{km:g}km離れた2地点は地図上で何cm離れる？',[good,f'{cm*2:g} cm',f'{cm+2:g} cm',f'{cm/2:g} cm'],good
        if mode==3:
            km=r.choice([1,2,3,4,5]); scale=100000; cm=km*100000/scale
            good=f'{cm:g} cm'
            return f'縮尺1:{scale:,}の地図を使う。実際に{km}kmの道のりは地図上で何cm？',[good,f'{cm+3:g} cm',f'{cm*10:g} cm',f'{cm/2:g} cm'],good
        if mode==4:
            cm=r.randrange(2,21); meters=cm*250
            good=f'{meters} m'
            return f'地図では1cmが実際の250mを表す。地図上で{cm}cmの道のりは実際に何m？',[good,f'{meters+250} m',f'{meters*2} m',f'{cm*25} m'],good
        cm=r.choice([2,4,5,8,10]); actual_km=r.choice([1,2,2.5,4,5])
        denominator=int(actual_km*100000/cm)
        good=f'1:{denominator:,}'
        return f'地図上で{cm}cmが実際の{actual_km:g}kmに当たる。この地図の縮尺は？',[good,'1:25,000','1:50,000','1:100,000'],good
    if kind == 'population_change':
        mode=r.randrange(4)
        if mode==0:
            total=r.randrange(800,3001,20); group=total//4
            return f'人口{total}人の町で15歳未満が{group}人いる。15歳未満の割合は？',['25%','50%','12.5%','75%'],'25%'
        if mode==1:
            total=r.randrange(1000,5001,100); pct=r.choice([10,15,20,30]); children=total*pct//100
            return f'人口{total}人の市で子どもが全体の{pct}％を占める。子どもは何人？',[str(children),str(children+100),str(total//2),str(total-children)],str(children)
        if mode==2:
            before=r.choice([1000,2000,5000]); after=before-r.choice([100,200,300,400,500]); pct=(before-after)*100//before
            answer=f'{pct}%'
            plausible=[2,4,5,6,8,10,12,15,20,25,30,35,40,45,50]
            distractors=[f'{value}%' for value in plausible if value != pct]
            choices=[answer]+r.sample(distractors,3)
            return f'ある町の人口は{before}人から{after}人に減った。人口減少率は何％？',choices,answer
        before=r.randrange(1000,5001,100); after=before+before//5
        return f'人口が{before}人から{after}人に増えた。増加した人数は？',[str(after-before),str(after),str(before//5+100),str(before-after)],str(after-before)
    if kind == 'industry':
        region,industry=r.choice([('中京工業地帯','自動車工業'),('京浜工業地帯','機械・化学工業'),('京葉工業地域','石油化学工業'),('瀬戸内工業地域','造船・石油化学工業'),('北九州工業地域','かつての製鉄業')])
        stem=r.choice([f'{region}と関連が深い工業はどれ？',f'工業地域の特色として、{region}に当てはまるものは？',f'{region}の工業について正しい説明はどれ？',f'日本の工業地帯・地域を学ぶ問題です。{region}と結びつく工業は？',f'{region}で発達した工業の特徴を選びなさい。',f'次のうち{region}を代表する工業はどれ？',f'{region}についての説明として最も適切なものは？',f'地理資料から判断すると、{region}と関連する産業はどれ？'])
        return stem,[industry,'大規模な茶の栽培','寒冷地での小麦栽培','絹織物だけの生産'],industry
    if kind == 'constitution':
        stem,answer,wrong=r.choice([
            ('日本国憲法で、思想・良心の自由に関係する権利は？','精神の自由',['経済の自由','社会権','参政権']),
            ('健康で文化的な最低限度の生活を求める権利は？','生存権',['請求権','参政権','財産権']),
            ('選挙で代表者を選ぶことに関係する権利は？','参政権',['環境権','自由権','請求権']),
            ('裁判を受ける権利などに関係する分類は？','請求権',['社会権','参政権','環境権'])
        ])
        frame=r.choice(['公民の知識をもとに答えなさい。','日本国憲法に関する問いです。','権利の分類について、次の問いに答えなさい。','憲法と人権について正しいものを選びなさい。','公民分野の資料を読んで答えなさい。','日本の政治と人権に関する問題です。','次の説明に当てはまる権利を選びなさい。','憲法上の権利について、最も適切なものは？','社会の授業で学ぶ権利の分類に関する問いです。','人権の保障に関して、正しい答えを選びなさい。'])
        return frame+' '+stem,[answer]+wrong,answer
    if kind == 'election':
        mode=r.randrange(4); voters=r.randrange(500,10001,100)
        if mode==0:
            cast=voters*3//5
            return f'有権者{voters}人のうち{cast}人が投票した。投票率は何％？',['60%','40%','75%','80%'],'60%'
        if mode==1:
            cast=voters*45//100
            return f'有権者{voters}人のうち{cast}人が投票した。投票率を選びなさい。',['45%','55%','60%','75%'],'45%'
        if mode==2:
            rate=r.choice([50,60,70,80]); cast=voters*rate//100
            return f'有権者{voters}人で投票率が{rate}％だった。投票した人は何人？',[str(cast),str(voters-cast),str(voters//2),str(voters+cast)],str(cast)
        rate=r.choice([50,60,70,80]); cast=voters*rate//100
        return f'投票率が{rate}％で、投票した人が{cast}人だった。選挙人名簿の人数は？',[str(voters),str(cast),str(voters+cast),str(voters-cast)],str(voters)
    if kind == 'tax':
        mode=r.randrange(6)
        price=r.randrange(500,5001,100)
        rate=r.choice([8,10])
        tax=price*rate//100
        total=price+tax
        if mode==0:
            answer=f'{total}円'
            return f'税抜き{price}円の商品に消費税{rate}％を加えると、税込み価格はいくら？',[answer,f'{price}円',f'{price*2}円',f'{total+500}円'],answer
        if mode==1:
            answer=f'{tax}円'
            return f'税抜き{price}円の商品に消費税{rate}％をかけると、税額はいくら？',[answer,f'{price}円',f'{total}円',f'{tax+100}円'],answer
        if mode==2:
            base=r.randrange(500,5001,100); incl=base*11//10
            answer=f'{base}円'
            return f'消費税10％込みで{incl}円の商品がある。税抜き価格はいくら？',[answer,f'{incl}円',f'{base+100}円',f'{base-100}円'],answer
        if mode==3:
            base=r.randrange(500,5001,100); discounted=base*8//10; incl=discounted*11//10
            answer=f'{incl}円'
            return f'{base}円の商品を20％引きで買い、さらに消費税10％を加えた。支払額はいくら？',[answer,f'{base}円',f'{discounted}円',f'{incl+100}円'],answer
        if mode==4:
            p1=r.randrange(600,2001,100); p2=p1+r.randrange(100,501,100)
            return f'商品Aは税抜き{p1}円、商品Bは税抜き{p2}円。どちらも消費税10％なら、税込み価格が高いのは？',['商品B','商品A','同じ価格','判断できない'],'商品B'
        p=r.randrange(500,5001,100); t=p*11//10
        answer=f'{t}円'
        return f'税抜き価格が{p}円の商品を買う。消費税率10％のとき、レジで払う金額は？',[answer,f'{p}円',f'{t+100}円',f'{p*2}円'],answer
    if kind == 'history_person':
        person,event=r.choice([('聖徳太子','十七条の憲法'),('源頼朝','鎌倉幕府を開いた'),('織田信長','楽市・楽座を進めた'),('伊藤博文','初代内閣総理大臣'),('福沢諭吉','『学問のすゝめ』を著した'),('板垣退助','自由民権運動を進めた'),('ペリー','黒船で来航した')])
        stem=r.choice([f'{person}の業績として正しいものはどれ？',f'歴史上の人物{person}について、正しい説明を選びなさい。',f'{person}と関係の深い出来事・業績はどれ？',f'日本史の人物{person}に関する説明として適切なものは？',f'{person}についての記述で正しいものを選びなさい。',f'次のうち、{person}が行ったことはどれ？',f'{person}に関連する歴史的な事柄はどれ？',f'歴史資料に登場する{person}について答えなさい。',f'{person}の活動を説明したものとして最も適切なのは？',f'人物と業績の組み合わせとして、{person}に当てはまるものは？'])
        return stem,[event,'大日本帝国憲法を廃止した','元寇を指揮した','江戸幕府を開いた'],event
    if kind == 'map_direction':
        stem,answer,wrong=r.choice([
            ('地図で、北を上にしたとき東はどの方向？','右',['左','上','下']),
            ('ある地点から北へ進み、その後東へ進んだ。最終地点は出発点からどの方角？','北東',['北西','南東','南西']),
            ('地図上で西はどちらの方向？','左',['右','上','下']),
            ('北を上にした地図で、南東はどの方向？','右下',['左下','右上','左上'])
        ])
        frame=r.choice(['地図の方位について答えなさい。','地図の読み取りに関する問いです。','方位を正しく理解して答えなさい。','地理の基礎知識として正しいものは？','次の地図上の移動について答えなさい。','方角の表し方に関する問題です。','地図を北が上になるように見た場合を考えなさい。','地理資料の方位について、適切な答えを選びなさい。','地図上の位置関係について答えなさい。','方位と移動の関係を確認しましょう。'])
        return frame+' '+stem,[answer]+wrong,answer
    if kind == 'energy':
        stem,answer,wrong=r.choice([
            ('日本でエネルギーの安定供給が課題となる理由は？','化石燃料の多くを輸入に頼るため',['国内に石油が無限にあるため','電力を一切使わないため','再生可能エネルギーが存在しないため']),
            ('再生可能エネルギーに当てはまるものは？','太陽光発電',['石炭火力発電','石油火力発電','天然ガス火力発電']),
            ('省エネルギーの取り組みとして適切なものは？','使わない照明を消す',['冷暖房を窓を開けたまま最大にする','使わない機器を常に動かす','必要以上に車を使う'])
        ])
        frame=r.choice(['環境と資源について答えなさい。','エネルギー問題に関する問いです。','次の説明として正しいものを選びなさい。','資源の利用について、適切な答えはどれ？','日本のエネルギー事情について答えなさい。','環境保全の視点から考えましょう。','社会とエネルギーに関する問題です。','資料をもとにエネルギーの特徴を判断しなさい。','資源・環境分野の問いに答えなさい。','エネルギーの生産と利用に関する問いです。','持続可能な社会について、正しいものは？','次のうち、エネルギー政策に関する説明はどれ？','環境負荷を減らす方法として適切なものは？','日本の資源と電力について、正しいものを選びなさい。','エネルギーの安定利用を考える問題です。'])
        return frame+' '+stem,[answer]+wrong,answer

    raise ValueError(kind)

EN=['grammar','comparison','dialogue','reading','schedule','fee','relative','passive','if','data','tense','conjunction','word_order','infinitive','pronoun','preposition','modal','indirect','superlative','dialogue_intent']
SO=['geography','landform','history','chronology','civics','population','trade','exchange','disaster','budget','world_region','map_scale','population_change','industry','constitution','election','tax','history_person','map_direction','energy']
def fresh_questions(date, used, recent_templates=None):
    seed=int(date.strftime('%Y%m%d')); r=random.Random(seed)
    recent_templates=set(recent_templates or ())
    results=[]
    for subject, kinds in [('english',EN),('social',SO)]:
        # Rotate a five-topic window by seven positions so adjacent days do not reuse four of five families.
        shift=(date.toordinal()*7)%len(kinds)
        selected=[kinds[(shift+i)%len(kinds)] for i in range(5)]
        for index,kind in enumerate(selected,1):
            for _ in range(10000):
                q,choices,answer=question(kind,r)
                key=re.sub(r'\s+','',q).casefold()
                template_id=(subject,kind,template_key(q))
                if key not in used and template_id not in recent_templates and len(set(choices))==4 and answer in choices:
                    used.add(key)
                    results.append(dict(id=f'{"eng" if subject=="english" else "soc"}-{date:%Y%m%d}-{index}',subject=subject,topic=kind,question=q,choices=choices,answer=answer))
                    break
            else:
                raise RuntimeError('Unable to produce a unique valid '+kind+' question after recent-template filtering')
    return results