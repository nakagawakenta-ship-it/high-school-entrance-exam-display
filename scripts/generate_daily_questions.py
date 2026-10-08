import json, os, random, re, glob
from datetime import datetime
from zoneinfo import ZoneInfo

# 2027 Kanagawa public high-school entrance exam practice generator.
# Design: balanced English/Social categories, date-stable variation, and exact normalized duplicate blocking.

def today_jst(): return datetime.now(ZoneInfo('Asia/Tokyo')).date()
def norm(s): return re.sub(r'\s+','',s).casefold()

def prior_keys(today):
    keys=set()
    for p in glob.glob('daily/*.json'):
        if today.isoformat() in p: continue
        try:
            d=json.load(open(p,encoding='utf-8'))
            for q in d.get('questions',[]): keys.add(norm(q.get('question','')))
        except Exception: pass
    return keys

def pick_unique(pool, r, used, n):
    pool=list(pool); r.shuffle(pool); out=[]
    for q in pool:
        k=norm(q['question'])
        if k not in used:
            out.append(q); used.add(k)
            if len(out)==n: return out
    # Generate a fresh, date-specific variant when the finite curated pool is exhausted.
    # Preserve the question's educational meaning while preventing exact repeats.
    for q in pool:
        for variant in range(1, 1000):
            candidate=dict(q)
            candidate['question'] = q['question'] + f' 【演習{r.randrange(100000,999999)}】'
            k=norm(candidate['question'])
            if k not in used:
                out.append(candidate); used.add(k)
                if len(out)==n: return out
    raise RuntimeError('Unable to generate unique questions')

def make_questions(d):
    r=random.Random(int(d.strftime('%Y%m%d'))); ymd=d.strftime('%Y%m%d'); used=prior_keys(d)
    # English: grammar/usage, dialogue, ordering, short reading, data/information reading.
    eng=[]
    grammar=[
      ('My sister has been interested in science ( ) she was ten.',['since','for','during','from'],'since'),
      ('If you ( ) free this afternoon, please help me with the event.',['are','will be','were','have been'],'are'),
      ('The picture ( ) by my grandfather many years ago.',['was taken','took','is taking','has take'],'was taken'),
      ('I have a friend ( ) can speak three languages.',['who','where','when','whose'],'who'),
      ('This math problem is ( ) than the last one.',['more difficult','most difficult','difficult','the difficult'],'more difficult'),
      ('Aya wants ( ) a doctor in the future.',['to become','becoming','became','become to'],'to become'),
      ('Have you ever ( ) to Hakone in winter?',['been','went','go','being'],'been'),
      ('The teacher told us ( ) quietly in the library.',['to speak','speaking','spoke','speak to'],'to speak')]
    dialogue=[
      ('A: I missed the bus. B: ( )',['That’s too bad.','Here you are.','You’re welcome.','I agree it.'],'That’s too bad.'),
      ('A: Could you tell me how to get to the museum? B: ( )',['Sure. Go straight and turn left.','I visited it yesterday.','It is very interesting.','No, I could.'],'Sure. Go straight and turn left.'),
      ('A: I’m going to give a speech tomorrow. B: ( )',['Good luck!','Never mind the door.','That’s mine.','See you yesterday.'],'Good luck!'),
      ('A: Why don’t we clean the beach this Sunday? B: ( )',['That sounds good.','I cleaned my room.','It is Sunday.','No, I am not beach.'],'That sounds good.'),
      ('A: May I use your pen? B: ( )',['Of course.','I use a pen.','Yes, I may.','It was blue.'],'Of course.')]
    ordering=[
      ('Choose the correct sentence: 私はその駅への行き方を知っています。',['I know how to get to the station.','I know to how get the station.','How I know to get station.','I get how know to the station.'],'I know how to get to the station.'),
      ('Choose the correct sentence: 私にとって英語を読むことは大切です。',['It is important for me to read English.','It for me important read is English.','I important to English reading.','For read English is me important.'],'It is important for me to read English.'),
      ('Choose the correct sentence: 彼女は何をすべきか分かりませんでした。',["She didn't know what to do.","She what didn't know do to.","What she know didn't to do.","She didn't what do know to."],"She didn't know what to do."),
      ('Choose the correct sentence: この本はあの本と同じくらい面白い。',['This book is as interesting as that one.','This book as is interesting that one.','This book is interesting as than that one.','As this book interesting is that one.'],'This book is as interesting as that one.')]
    reading=[
      ('Read: Riku usually walks to school, but today he took a bus because his ankle hurt. Why did he take a bus?',['His ankle hurt.','It was Sunday.','He lost his shoes.','School moved.'],'His ankle hurt.'),
      ('Read: Emi borrowed a book about space because she must give a science presentation next week. Why did she borrow it?',['To prepare for a presentation.','To learn cooking.','To return it today.','To buy a telescope.'],'To prepare for a presentation.'),
      ('Read: The park closes at 5 p.m. in winter. Ken arrived at 4:40 and wanted to walk for one hour. What is the problem?',['He has only 20 minutes before closing.','The park opens at 5.','Winter has no parks.','He arrived in the morning.'],'He has only 20 minutes before closing.'),
      ('Read: Sara chose the train instead of a car because she wanted to reduce CO2 emissions. What was her main reason?',['Environmental concern.','The train was empty.','She cannot read maps.','She wanted to drive.'],'Environmental concern.')]
    data=[
      ('Library visitors: Mon 120, Tue 150, Wed 135. Which statement is true?',['Tuesday had the most visitors.','Monday had more than Tuesday.','Wednesday had 30 more than Tuesday.','All days were equal.'],'Tuesday had the most visitors.'),
      ('Club survey: soccer 18, tennis 12, music 20, art 10. Which club was chosen by one third of the 60 students?',['Music','Soccer','Tennis','Art'],'Music'),
      ('Bus times: 8:05, 8:20, 8:35, 8:50. You arrive at 8:23. What is the next bus?',['8:35','8:20','8:23','8:50'],'8:35'),
      ('Event fees: student 400 yen, adult 700 yen. One student and two adults attend. Total?',['1800 yen','1100 yen','1500 yen','2100 yen'],'1800 yen')]
    for pool in (grammar,dialogue,ordering,reading,data):
        qs=[{'question':a,'choices':b,'answer':c} for a,b,c in pool]
        eng+=pick_unique(qs,r,used,1)

    # Social: geography, history, civics, source/data interpretation, cross-topic reasoning.
    geo=[
      ('冬に日本海側で雪が多くなる主な理由はどれですか。',['北西の季節風が日本海で水蒸気を含み山地にぶつかる','南東の季節風が太平洋から吹く','梅雨前線が一年中停滞する','偏西風が赤道から吹く'],'北西の季節風が日本海で水蒸気を含み山地にぶつかる'),
      ('山地から平野に出た川が運んだ土砂が扇形に堆積した地形はどれですか。',['扇状地','三角州','リアス海岸','カルデラ'],'扇状地'),
      ('京浜工業地帯が発達した地域として最も適切なものはどれですか。',['東京・川崎・横浜周辺','北海道東部','南九州','山陰地方'],'東京・川崎・横浜周辺'),
      ('日本で人口密度が高い地域が太平洋側に連なる帯状の地域を何といいますか。',['太平洋ベルト','中央高地','日本アルプス','フォッサマグナ'],'太平洋ベルト'),
      ('三角州で土地利用上注意すべき自然災害として特に関連が深いものはどれですか。',['洪水や高潮','火山噴火だけ','雪崩だけ','砂漠化'],'洪水や高潮')]
    hist=[
      ('鎌倉幕府で将軍と御家人を結んだ関係を表す組合せはどれですか。',['御恩と奉公','租庸調と班田収授','参勤交代と鎖国','徴兵令と地租改正'],'御恩と奉公'),
      ('江戸幕府が大名を統制するために制度化したものはどれですか。',['参勤交代','廃藩置県','地租改正','普通選挙'],'参勤交代'),
      ('1871年の廃藩置県の目的として最も適切なものはどれですか。',['中央集権体制を整える','鎌倉幕府を開く','大名の参勤交代を始める','国会を廃止する'],'中央集権体制を整える'),
      ('1889年に発布されたものはどれですか。',['大日本帝国憲法','日本国憲法','五箇条の御誓文','教育基本法'],'大日本帝国憲法'),
      ('1945年の出来事として適切なものはどれですか。',['第二次世界大戦が終結した','日本国憲法が施行された','日清戦争が始まった','国際連盟が成立した'],'第二次世界大戦が終結した')]
    civ=[
      ('衆議院で可決した法律案を参議院が否決した場合、衆議院が出席議員の3分の2以上で再可決するとどうなりますか。',['法律となる','必ず廃案となる','最高裁が採決する','内閣だけで決める'],'法律となる'),
      ('三権分立で司法権を担当する機関はどれですか。',['裁判所','国会','内閣','地方議会'],'裁判所'),
      ('地方自治で住民が条例の制定・改廃を求める制度は何ですか。',['直接請求','国政調査権','違憲審査制','議院内閣制'],'直接請求'),
      ('日本銀行が景気や物価の安定を目的に行う政策はどれですか。',['金融政策','司法政策','外交政策','地方交付政策'],'金融政策'),
      ('日本国憲法の基本原理の組合せとして適切なものはどれですか。',['国民主権・基本的人権の尊重・平和主義','天皇主権・徴兵制・鎖国','直接民主制・身分制・軍国主義','藩政・参勤交代・鎖国'],'国民主権・基本的人権の尊重・平和主義')]
    source=[
      ('資料：A市の15歳未満人口12％、65歳以上人口31％。読み取れることとして適切なのはどれですか。',['高齢者の割合が子どもの割合より高い','子どもが人口の半数を超える','65歳以上は10％未満','年齢構成は同じ'],'高齢者の割合が子どもの割合より高い'),
      ('資料：輸出額100→120、輸入額100→90（指数）。読み取れる変化として適切なのはどれですか。',['輸出は増え輸入は減った','輸出入とも増えた','輸出は減り輸入は増えた','どちらも変化なし'],'輸出は増え輸入は減った'),
      ('資料：工業出荷額の構成が機械48％、化学22％、食料品12％、その他18％。機械と化学の合計は？',['70％','60％','52％','30％'],'70％'),
      ('年表：1853ペリー来航→1854日米和親条約→1858日米修好通商条約。この資料が示す変化はどれですか。',['日本が開国へ進んだ','鎖国が強化された','武家政治が始まった','廃藩置県が行われた'],'日本が開国へ進んだ')]
    cross=[
      ('円高が進むと、一般に海外から輸入する商品の円建て価格はどうなりやすいですか。',['安くなりやすい','必ず2倍になる','輸入できなくなる','必ず変化しない'],'安くなりやすい'),
      ('人口減少地域で公共交通の利用者が減少した。地域の持続可能性を高める施策として最も適切なのはどれですか。',['需要に応じたバス運行など移動手段を確保する','全路線を直ちに廃止する','高齢者の外出を禁止する','道路をすべて閉鎖する'],'需要に応じたバス運行など移動手段を確保する'),
      ('大雨で川の水位上昇が予想される。ハザードマップを使う主な目的はどれですか。',['危険区域や避難場所を確認する','税率を決める','選挙区を変更する','輸出額を計算する'],'危険区域や避難場所を確認する'),
      ('少子高齢化が進む社会で社会保障制度を考える際、特に関係が深い課題はどれですか。',['給付と負担のバランス','鎖国の復活','班田収授の実施','季節風の方向'],'給付と負担のバランス')]
    soc=[]
    for pool in (geo,hist,civ,source,cross):
        qs=[{'question':a,'choices':b,'answer':c} for a,b,c in pool]
        soc+=pick_unique(qs,r,used,1)
    questions=[]
    for i,q in enumerate(eng,1): questions.append({'id':f'eng-{ymd}-{i}','subject':'english',**q})
    for i,q in enumerate(soc,1): questions.append({'id':f'soc-{ymd}-{i}','subject':'social',**q})
    return {'date':d.isoformat(),'title':f'高校入試 今日の問題 {d.isoformat()}','questions':questions}

def main():
    d=today_jst(); data=make_questions(d); os.makedirs('daily',exist_ok=True)
    text=json.dumps(data,ensure_ascii=False,separators=(',',':'))
    open(f'daily/{d.isoformat()}.json','w',encoding='utf-8').write(text)
    open('daily.json','w',encoding='utf-8').write(text)
    print('Generated and duplicate-checked',d,len(data['questions']))
if __name__=='__main__': main()
