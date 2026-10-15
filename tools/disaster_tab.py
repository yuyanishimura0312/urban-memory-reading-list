"""Generate the 'disaster x place memory' tab and insert it into index.html.

Bibliographic data and citation counts: OpenAlex, 2026-10-16.
Summaries are written in Japanese from the abstract (basis=要旨) or, where
OpenAlex has no abstract, from the bibliography and secondary accounts (basis=紹介).
Re-running is idempotent: the block between the TAB markers is replaced.
"""
import html, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"

PAPERS = [
 dict(n=1, au="Fran H. Norris ほか", year=2008, src="American Journal of Community Psychology 41", cites="5,235",
  title="Community Resilience as a Metaphor, Theory, Set of Capacities, and Strategy for Disaster Readiness",
  lead="地域の回復力を、災害後の適応へつなぐ「適応能力の網」として定義する。",
  oa=True, url="https://doi.org/10.1007/s10464-007-9156-6", basis="要旨",
  s="災害の後に地域が機能を取り戻し、うまく適応できる力を、いくつもの分野の知見を束ねて理論化した論文である。著者らは地域の回復力を、撹乱や逆境の後の適応へとつながる「適応能力の網」の過程として定義し、その能力を経済の発展、社会関係資本、情報とコミュニケーション、地域の力量の4群に分ける。適応の成果は、住民の心身の健康や生活の質が高く、偏りなく保たれることで測る。そのうえで、危険と資源の不平等を減らすこと、住民を減災に参加させること、組織どうしをつなぐこと、そして計画が通用しない事態に備えることを提言する。場所の記憶を回復の資源として論じるときの、基本の枠組みとして引かれることが多い。"),
 dict(n=2, au="Susan L. Cutter ほか", year=2008, src="Global Environmental Change 18", cites="4,309",
  title="A place-based model for understanding community resilience to natural disasters",
  lead="脆弱性と回復力を「場所」を単位に結びつけるモデル（DROP）を示す。",
  oa=False, url="https://doi.org/10.1016/j.gloenvcha.2008.07.013", basis="紹介",
  s="災害に対する地域の弱さ（脆弱性）と、立ち直る力（回復力）は、別々の研究伝統で論じられてきた。カッターらはこの2つを「場所」を単位につなぐモデルを提案し、DROP（場所の災害回復力）モデルと名づけた。災害の前から地域が抱えている社会・自然・建造環境の条件が、被害の受け止め方と、その後の適応や学習を左右するという見取り図である。あわせて、生態・社会・経済・制度・基盤・地域の力量の各面で回復力を測る指標の候補を示し、比較と政策の議論に道を開いた。回復を地域ごとの条件に根ざしたものとして捉える視点を与える。要旨は未入手で、書誌と二次的な紹介に基づく。"),
 dict(n=3, au="Daniel P. Aldrich, Michelle A. Meyer", year=2015, src="American Behavioral Scientist 59", cites="2,294",
  title="Social Capital and Community Resilience",
  lead="回復を左右するのは堤防ではなく、人のつながりという「社会の基盤」だと論じる。",
  oa=False, url="https://doi.org/10.1177/0002764214550299", basis="要旨",
  s="災害対策の予算と研究は、堤防のかさ上げや住宅の高床化、施設の修繕といった物理的な基盤に偏ってきた。アルドリッチとマイヤーは、生き延びることと回復を実際に左右しているのは物理的な基盤ではなく社会的な基盤だという証拠を整理し、社会関係資本とネットワークの役割を論じる。社会関係資本の定義、測り方、結束型・橋渡し型・連結型といった種類、働く仕組みを概観し、災害の管理者や行政、NGO に向けて、地域の社会的な基盤を強める具体的な提言で締めくくる。東日本大震災の調査でも知られる著者による総説で、地域文化が回復を支える仕組みを考える入口になる。"),
 dict(n=4, au="W. Neil Adger ほか", year=2013, src="Nature Climate Change 3", cites="1,456",
  title="Cultural dimensions of climate change impacts and adaptation",
  lead="気候変動の被害と適応を、文化という次元から捉え直すよう求める。",
  oa=False, url="https://doi.org/10.1038/nclimate1666", basis="紹介",
  s="気候変動の影響と適応は、主に物理的・経済的な損失として論じられてきた。アジャーらは、文化がこの問題の両側に関わると指摘する。一方で、人々が何を危険と感じ、何を大切に思い、どう応じるかは文化によって形づくられる。他方で、気候変動は場所や暮らしの慣習、それに結びついた自己像そのものを失わせうる。そのため、適応策が文化的な価値と食い違えば受け入れられず、守るべきものが見落とされる、と論じる。数値で測りにくい文化的な損失を政策の議論に入れることを求めた論文で、気候変動時代の地域文化の持続可能性を考える際の出発点になる。要旨は未入手で、書誌と二次的な紹介に基づく。"),
 dict(n=5, au="Glenn Albrecht ほか", year=2007, src="Australasian Psychiatry 15", cites="1,356",
  title="Solastalgia: The Distress Caused by Environmental Change",
  lead="故郷を離れずにいながら、その故郷が変わってしまうことの苦しみに名を与える。",
  oa=False, url="https://doi.org/10.1080/10398560701701288", basis="要旨",
  s="ノスタルジアは、愛着のある故郷から離れた人が抱く郷愁である。これに対しアルブレヒトらは、故郷にとどまったまま、その環境が変わっていくことで生じる苦しみを「ソラスタルジア」と名づけた。オーストラリア・ニューサウスウェールズ州で、長引く干ばつに見舞われた農村と、大規模な露天掘り炭鉱が広がるアッパーハンター地域を対象に、聞き取り・グループ討議・住民調査を行った。いずれの地域でも、変化を自分では止められないという無力感が苦しみを強めていた。災害や気候変動で「場所」が変わるとき、人がその場所との結びつきから受ける痛みを捉える概念として、広く使われている。"),
 dict(n=6, au="Anthony Oliver-Smith", year=1996, src="Annual Review of Anthropology 25", cites="814", anth=True,
  title="Anthropological Research on Hazards and Disasters",
  lead="災害を、破壊的な力と社会が生んだ脆弱性との組み合わせとして捉える人類学の総説。",
  oa=False, url="https://doi.org/10.1146/annurev.anthro.25.1.303", basis="要旨",
  s="災害は自然現象そのものではなく、潜在的に破壊的な力と、社会的・技術的に生み出された脆弱な状態にある人々とが組み合わさって起きる過程であり出来事である。オリバー＝スミスはこの理解に立って、人類学の災害研究を3つの流れに整理する。行動と組織の対応を見る流れ、社会変化を見る流れ、そして途上国を中心に脆弱性の歴史的・構造的な成り立ちを問う政治経済・環境の流れである。災害管理への応用や、危険の知覚と評価の研究にも触れ、人と環境の関係や社会文化の変化を考える理論の場として災害研究の可能性を論じる。災害を地域の文化と歴史の中で読むための基礎文献である。"),
 dict(n=7, au="Barbara B. Brown, Douglas D. Perkins", year=1992, src="Place Attachment（Altman &amp; Low 編）", cites="762",
  title="Disruptions in Place Attachment",
  lead="場所への愛着が断ち切られる前・最中・後の過程を描く。",
  oa=False, url="https://doi.org/10.1007/978-1-4684-8753-4_13", basis="紹介",
  s="場所への愛着研究の古典的な論集に収められた章である。ブラウンとパーキンスは、転居のような自ら選んだ変化から、災害や犯罪のような望まない出来事まで、人と場所の結びつきが断ち切られる場面を取り上げる。愛着の崩れを一度の出来事ではなく、断絶の前に結びつきが築かれる段階、断絶の段階、その後に人々が対処し新しい場所との結びつきを作り直す段階として捉える見方を示した。災害で住まいや町を失った人々が、どのように場所との関係を取り戻すのか、あるいは取り戻せないのかを考えるときに、繰り返し参照される枠組みである。要旨は未入手で、書誌と二次的な紹介に基づく。"),
 dict(n=8, au="Mindy Thompson Fullilove", year=1996, src="American Journal of Psychiatry 153", cites="695",
  title="Psychiatric implications of displacement: contributions from the psychology of place",
  lead="住む場所を追われることが、愛着・なじみ・自己像の3つを同時に脅かすと示す。",
  oa=False, url="https://doi.org/10.1176/ajp.153.12.1516", basis="要旨",
  s="戦争や脱植民地化、感染症、自然災害によって、多くの人が住まいを追われている。精神科医のフリラブは地理学・心理学・人類学・精神医学の文献を検討し、「場所の心理学」を組み立てた。人は「ほどよい」環境を必要とし、その環境と愛着、なじみ（周囲についての細かな知識）、場所に根ざした自己像という3つの心理的な過程で結びついている。住む場所を追われるとこの3つがそろって脅かされ、郷愁、方向感覚の喪失、疎外が生じうる。のちに都市再開発による立ち退きを論じた著書『ルート・ショック』につながる論文で、場所の記憶が失われることの心理的な重さを示す。"),
 dict(n=9, au="Stephan Barthel, Carl Folke, Johan Colding", year=2010, src="Global Environmental Change 20", cites="555",
  title="Social–ecological memory in urban gardens—Retaining the capacity for management of ecosystem services",
  lead="都市の市民農園が、自然と付き合う知恵を受け継ぐ「記憶の器」になっていると示す。",
  oa=False, url="https://doi.org/10.1016/j.gloenvcha.2010.01.001", basis="紹介",
  s="ストックホルムの市民農園を事例に、自然とどう付き合うかについての経験・知識・実践が、どのように保たれ受け継がれていくかを調べた研究である。著者らはこれを「社会・生態の記憶」と呼び、それが日々の作業や慣習、道具や景観、人から人への非公式なつながりの中に蓄えられていることを示す。こうした記憶は、環境が大きく変わったときに地域が立ち直り、生態系の恵みを管理し続けるための力の源になる、と論じる。記憶を過去の保存ではなく、変化に備える能力として捉える視点を与え、場所の記憶と地域の回復力を結びつけるうえで鍵となる論文である。要旨は未入手で、書誌と二次的な紹介に基づく。"),
 dict(n=10, au="Robin S. Cox, Karen-Marie E. Perry", year=2011, src="American Journal of Community Psychology 48", cites="504",
  title="Like a Fish Out of Water: Reconsidering Disaster Recovery and the Role of Place and Social Capital in Community Disaster Resilience",
  lead="被災後の回復を、場所を失った人々の「向き直り」の過程として描く民族誌。",
  oa=False, url="https://doi.org/10.1007/s10464-011-9427-0", basis="要旨",
  s="カナダ、ブリティッシュコロンビア州で山火事に見舞われた2つの農村で、複数の場所にまたがる批判的な民族誌を行った研究である。著者らは、場所とアイデンティティ、社会関係資本が回復の過程でどれほど大きな意味を持つかを調べ、災害の回復を捉え直す必要があると論じる。人々は火災がもたらした象徴的・物質的な場所の変化によって方向を見失い、その中で心理的・社会的・感情的に向きを取り直していく。著者らはこれを「再定位（reorientation）」と呼ぶ。場所は回復の拠り所であるだけでなく、社会関係資本と地域の回復力が築かれる土台でもある、という主張は、場所の記憶の力を考えるうえで直接の手がかりになる。"),
]

RESERVE = [
 ("Adger, Barnett, Chapin &amp; Ellemor（2011）", "This Must Be the Place", "Global Environmental Politics・被引用372"),
 ("Chamlee-Wright &amp; Storr（2009）", "“There’s No Place like New Orleans”", "Journal of Urban Affairs・被引用362"),
 ("Holtorf（2018）", "Embracing change: how cultural resilience is increased through cultural heritage", "World Archaeology・被引用283"),
 ("Tschakert ほか（2017）", "Climate change and loss, as if people mattered", "WIREs Climate Change・被引用272"),
 ("Sesana ほか（2021）", "Climate change impacts on cultural heritage: A literature review", "WIREs Climate Change・被引用568"),
]


def paper_html(p):
    n2 = f"{p['n']:02d}"
    tag = '<span class="lit-tag">人類学</span>' if p.get("anth") else ""
    st = '<span class="lit-st open">全文</span>' if p["oa"] else '<span class="lit-st paywall">購読</span>'
    stw = "全文" if p["oa"] else "購読"
    stn = "無料で全文を読める" if p["oa"] else "所属機関の契約か購入で読む"
    return f'''<section class="section" id="d{p['n']}">
  <div class="sec-head">
    <div class="eyebrow"><span class="n">{n2}</span>{p['src']} · {p['year']}{(' ' + tag) if tag else ''}</div>
    <h2>{html.escape(p['title'])}</h2>
    <p class="lead">{p['lead']}</p>
  </div>
  <div class="lit-meta people">
    <div><b>{p['au']}</b>著者</div>
    <div><b>{p['src']}</b>誌名<br><small>{p['year']}</small></div>
    <div><b class="mono">{p['cites']}</b>被引用<br><small>OpenAlex・2026-10-16</small></div>
    <div><b>{stw}</b>本文の公開<br><small>{stn}</small></div>
  </div>
  <div class="lit-sumhead"><div class="subhead">概要</div><span class="lit-basis">根拠: {p['basis']}</span></div>
  <p class="lit-summary" data-id="d{p['n']}">{p['s']}</p>
  <p class="lit-link">{st}<a href="{p['url']}">{p['url']}</a></p>
</section>
'''


def build():
    toc = "\n".join(
        f'      <a class="toc-item" href="#d{p["n"]}"><span class="n">{p["n"]:02d}</span><span class="t">{p["au"].split(",")[0].split(" ほか")[0].split(" ")[-1]} {p["year"]}<small>{html.escape(p["title"][:60])}</small></span></a>'
        for p in PAPERS)
    rows = "\n".join(f'        <li>{a}『{t}』<small style="display:block;color:var(--es-ink-mute)">{s}</small></li>' for a, t, s in RESERVE)
    n_oa = sum(p["oa"] for p in PAPERS)
    body = "".join(paper_html(p) for p in PAPERS)
    return f'''<!-- TAB:disaster:begin (generated by tools/disaster_tab.py) -->
<div class="lit-panel" id="tab-disaster" role="tabpanel" aria-labelledby="tabbtn-disaster">
<main class="page">
<section class="section" id="d-intro">
  <div class="sec-head">
    <div class="eyebrow"><span class="n">00</span>Introduction</div>
    <h2>気候変動時代の災害と、場所の記憶の力を考えるための10本</h2>
    <p class="lead">気候変動によって甚大な災害が増えるなかで、被災と復興の過程で人々が持つ場所の記憶がどんな力を持ち、地域の文化はどう持続しうるのか。この問いを考えるために、まず読んでおきたい10本を被引用数の多い順に並べた。前のタブの「都市の記憶」の議論を、災害・回復力・気候変動の研究へとつなぐ一覧である。</p>
  </div>
  <div class="facts">
    <div class="fact"><div class="fact-label">論文</div><div class="fact-num ink">10<span class="unit">本</span></div><div class="fact-desc">被引用数の多い順。補欠5本を末尾に添える</div></div>
    <div class="fact"><div class="fact-label">主題の内訳</div><div class="fact-num ink">3<span class="unit">群</span></div><div class="fact-desc">回復力と社会関係（01-03）・場所と喪失（04-08）・記憶と回復（09-10）</div></div>
    <div class="fact"><div class="fact-label">無料で全文を確認</div><div class="fact-num ink">{n_oa}<span class="unit">本</span></div><div class="fact-desc">01 番。残りは購読が必要</div></div>
    <div class="fact"><div class="fact-label">被引用の範囲</div><div class="fact-num ink">504<span class="unit">〜</span>5,235</div><div class="fact-desc">OpenAlex・2026-10-16 時点の値。以後は動く</div></div>
  </div>
  <div class="note ink">選び方: OpenAlex で「場所への愛着×災害」「集合的記憶×災害」「気候変動×文化遺産」「ソラスタルジア」などの語を題名から検索し、被引用数の多い論文から、場所の記憶・災害からの回復・地域文化の持続という主題に直接関わるものを選んだ。年は掲載巻の年。凡例（公開状態・概要の根拠）は前のタブと同じ。</div>
</section>

<section class="section" id="d-toc">
  <div class="sec-head"><div class="eyebrow"><span class="n">00</span>Contents</div><h2>目次</h2></div>
  <div class="toc">
    <div class="toc-col a">
      <div class="toc-head"><div class="letter">A</div><div class="lab"><small>Part A</small>主要論文10本</div></div>
{toc}
    </div>
    <div class="toc-col b">
      <div class="toc-head"><div class="letter">B</div><div class="lab"><small>Part B</small>付記</div></div>
      <a class="toc-item" href="#d-b1"><span class="n">B-1</span><span class="t">補欠<small>補欠5本</small></span></a>
      <a class="toc-item" href="#d-limits"><span class="n">B-2</span><span class="t">この一覧の限界<small>検索範囲・概要の根拠・時点</small></span></a>
    </div>
  </div>
</section>

{body}
<section class="section" id="d-b1">
  <div class="sec-head">
    <div class="eyebrow"><span class="n">B-1</span>Reserve papers</div>
    <h2>補欠</h2>
    <p class="lead">10本に入れなかったが、同じ問いに近い論文。被引用数は OpenAlex・2026-10-16 時点。</p>
  </div>
  <ul class="pts">
{rows}
  </ul>
</section>

<section class="section" id="d-limits">
  <div class="sec-head">
    <div class="eyebrow"><span class="n">B-2</span>Limits of this list</div>
    <h2>この一覧の限界</h2>
  </div>
  <div class="note ink">検索は英語の題名に限っており、日本語文献と書籍（Erikson『Everything in Its Path』、Aldrich『Building Resilience』など）は含めていない。東日本大震災をはじめ日本の事例を扱う研究は、別に探す必要がある。概要の根拠が「紹介」の項目（02・04・07・09）は要旨が入手できず、書誌と二次的な紹介に基づくため、精度が他より低い。被引用数は分野の大きさにも左右されるため、心理学・地理学の論文が人類学の論文より多く出やすい。</div>
</section>
</main>
</div>
<!-- TAB:disaster:end -->
'''


def main():
    src = PAGE.read_text(encoding="utf-8")
    block = build()
    if "<!-- TAB:disaster:begin" in src:
        src = re.sub(r"<!-- TAB:disaster:begin.*?<!-- TAB:disaster:end -->\n", lambda m: block, src, flags=re.S)
    else:
        src = src.replace('<footer class="foot">', block + '<footer class="foot">', 1)
    PAGE.write_text(src, encoding="utf-8")


if __name__ == "__main__":
    main()
