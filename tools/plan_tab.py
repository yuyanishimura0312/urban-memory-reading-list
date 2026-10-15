"""Generate the 'master's thesis research plan' tab (tab 3) and insert it into index.html.

Part A is an essay that sets out the problem behind the plan; Part B is the plan.
Both are drafts (2026-10-16). Cited works are those listed in tabs 1-2; the two
foundation texts the student named (a critical review of place and memory, and a
paper on deep democracy) are still being identified, so no bibliography is given
for them. 蓮葉果紅 is an organisation named by the user; nothing about it is
asserted beyond what the user said.
Re-running is idempotent: the block between the TAB markers is replaced, and the
tab button and cover note are added once.
"""
import html, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
e = html.escape

TITLE = "気候災害の非日常における場所の記憶と深層民主主義"
SUBTITLE = "形式の外側で人々を結ぶものの民族誌的研究"

# ---------------- Part A: essay ----------------
ESSAY_TITLE = "非日常が日常になるとき、場所の記憶は何を支えうるか"
ESSAY = [
 "災害はこれまで、日常を一時的に断ち切る出来事として理解されてきた。被災し、避難し、復旧し、やがて元の暮らしへ戻る。復興という語には、断絶の後に日常が回復するという時間の型が埋め込まれている。ところが気候変動は、この型そのものを揺るがしている。豪雨や洪水、猛暑や山火事が同じ地域を繰り返し襲うようになれば、災害は断絶ではなく条件になる。非日常が日常の側に入り込み、次の災害を待つ時間が暮らしの一部になる。本研究の問題意識は、この「非日常の常態化」が、場所の記憶と人々のつながりに何を求めるのかという点にある。",
 "記憶研究はこれまで、場所が比較的安定していることを暗黙の前提としてきた。ノラ（1989）は、共同体の暮らしのなかで生きられていた記憶の環境が失われたからこそ、記念碑や史跡といった「記憶の場」が意図して作られるようになったと論じた。そこでは、記憶は失われゆくものを場所に託して保存する営みとして描かれる。だが、託すはずの場所そのものが繰り返し壊され、形を変えていくとき、保存という発想はそのままでは成り立たない。アルブレヒトら（2007）が「ソラスタルジア」と名づけたのは、故郷を離れずにいながら、その故郷が変わっていくことに苦しむ経験であった。気候災害の時代の場所の記憶は、喪失の後に残るものというより、変化の只中で絶えず作り直されるものとして捉え直される必要がある。",
 "作り直しは、つねに穏やかに進むわけではない。コナトン（2008）は「忘れる」という一語に、抑圧的な抹消、新しい自己像のための忘却、計画的な陳腐化など、少なくとも7つの異なる型が含まれることを示した。復興計画が新しい街並みを描くとき、そこでは何が記憶され、何が忘れられることになるのか。ハーツフェルド（2010）が描いたように、歴史の保存がかえって住民の入れ替わりを正当化する場合もある。記憶をめぐる決定は、技術の問題である以前に、誰の過去を残すかという政治の問題である。",
 "災害そのものも、同じく政治の問題として理解されてきた。オリバー＝スミス（1996）は、災害を自然現象としてではなく、破壊的な力と社会が生み出した脆弱性との組み合わせとして捉える人類学の視座を整理した。アルドリッチとマイヤー（2015）は、生き延びることと回復を左右するのは堤防のような物理的な基盤よりも、人と人のつながりという社会的な基盤だという知見をまとめている。そうであれば、回復を支える力は、行政の計画や合意形成の会議といった形式の内側だけにあるのではない。むしろ、形式が届かない場所で人々が互いを気にかけ、記録し、語り継ぐ日々の実践のなかにある。深層民主主義の議論が示すのは、まさにこの、制度の外側で人々の実践に根づく民主主義の形である。",
 "ここで本研究は、蓮葉果紅という組織におけるコミュニティとは異なる、人々のつながりのあり方に目を向ける。組織は成員と目的を持ち、その内側で関係を育てる。これに対して、災害の繰り返しのなかで立ち上がるつながりは、成員を定めず、目的もそのつど変わり、地域の境界を越えて他の被災地や国外の運動とも結びつきうる。この緩やかなつながりは、組織のコミュニティを補うものなのか、それとも別の原理で動くものなのか。この問いは、地域性とグローバル性がどう接続されるかという問いと重なっている。",
 "回復とは、元の場所へ戻ることだけを意味しない。コックスとペリー（2011）は、山火事に見舞われたカナダの2つの農村で、人々が象徴的・物質的な場所の変化によって方向を見失い、互いの関係のなかで向きを取り直していく過程を「再定位」と呼んだ。記憶を過去の保存ではなく、変化に備える能力として捉える視点もすでに示されている。バルテルら（2010）は、都市の市民農園で受け継がれる知恵や慣習を「社会・生態の記憶」と呼び、それが環境の変化から立ち直る力の源になると論じた。ティル（2012）は、暴力や立ち退きの傷を抱えた都市で住民や芸術家が続ける「記憶の作業」に、場所に根ざしたケアの倫理を見いだした。これらを手がかりにすれば、場所の記憶は、喪失を嘆く装置ではなく、次の災害を生き延びるための共同の資源になりうる。",
 "以上から、本研究の問題意識は次のように定まる。気候災害が繰り返される時代には、場所を前提とした記憶、制度を前提とした民主主義、継承を前提とした文化のいずれもが、前提ごと問い直される。そこで必要とされるのは、変化の只中で作り直される記憶であり、形式の外側で人々を結ぶ民主主義であり、壊れることを織り込んだ文化である。本研究は、それらがどのように生まれ、あるいは生まれずにいるのかを、地域の具体的な実践から記述することを目指す。答えを先に決めるのではなく、繰り返す災害のなかで人々が実際に何を覚え、誰と何を決めているのかを確かめることから始めたい。",
]

# ---------------- Part B: plan ----------------
PLAN = [
 ("pl1", "Background", "背景と問題意識", [
  "気候変動によって、豪雨・洪水・猛暑・山火事といった甚大な災害は、かつての「まれな出来事」から、繰り返し訪れる条件へと変わりつつある。災害は日常を断ち切る非日常であると同時に、その非日常が常態になっていくという矛盾を地域に突きつける。このとき揺らぐのは住まいや街並みだけではない。場所に結びついた記憶、そこで受け継がれてきた文化、人々が互いを支え合う関係の形もまた揺らぐ。本研究は、この揺らぎのなかで、地域が新たな記憶と民主主義と文化をどのように生み出しうるのかを問う（問題意識の詳細は巻末の参考論考を参照）。",
 ], None),
 ("pl2", "Theoretical basis", "理論的基盤", [
  "本研究は2つの側から問いを組み立てる。一方の側は、場所と記憶の研究と、深層民主主義の研究である。前者については、場所と記憶の関係を包括的に批判検討した論考を基盤とする。この論考は、ノラの「記憶の場」、アルヴァックス以来の集合的記憶論、場所への愛着研究といった基本となる研究群を整理したうえで、その限界を指摘している。すなわち、記憶が国家や記念碑の側から語られやすく、日々の暮らしのなかで生きられる記憶が捉えにくいという点である。あわせて、忘却を7つの型に分けたコナトン（2008）と、傷を負った都市での「記憶の作業」とケアの倫理を論じたティル（2012）を、失われることを一様な喪失として扱わず読み分けるための手がかりとする。",
  "後者の深層民主主義の研究は、投票や議会といった形式的な制度とは別に、人々の日々の実践のなかに根づく民主主義の形を捉え、地域の運動がグローバルな連帯と接続する回路を示している。この概念は、蓮葉果紅という組織におけるコミュニティとは異なる、人々のつながりと取り組みのあり方を記述するための概念的な足場を与えると期待される。",
  "もう一方の側は、気候変動時代の災害研究である。災害を自然現象ではなく、社会が生み出した脆弱性との組み合わせとして捉える人類学の視座（Oliver-Smith 1996）、故郷にとどまりながら環境の変化に苦しむ経験を名づけた「ソラスタルジア」（Albrecht ほか 2007）、気候変動の被害と適応を文化の次元から捉え直す議論（Adger ほか 2013）、記憶を過去の保存ではなく変化に備える能力とみる「社会・生態の記憶」（Barthel ほか 2010）がこれにあたる。これらは、災害の非日常が既存の記憶を壊すだけでなく、新たな記憶・民主主義・文化を必要とすることを示唆している。",
 ], None),
 ("pl3", "Research questions", "研究の問い", [
  "中心となる問いは、「気候災害が繰り返される地域において、場所の記憶はどのように作り直され、それは形式的な制度とは別の民主主義の形をどのように生み出すのか」である。これを次の3つの問いに分ける。",
 ], "rq"),
 ("pl4", "Field and methods", "対象と方法", [
  "方法は、参与観察と半構造化インタビューを中心とする民族誌である。復興や防災をめぐる会合、祭礼や清掃などの共同作業、記録や語り継ぎの活動に参加し、住民・支援者・行政担当者の語りを集める。あわせて、災害の記録誌、地域紙、記念碑や伝承碑といった、物として残る記憶の担い手も資料として分析する。分析では、記憶研究の批判的な論点を手がかりに、上から与えられる記憶と、暮らしのなかで生きられる記憶とを区別して読む。蓮葉果紅という組織におけるコミュニティとの対比は、観察されたつながりの性質を見極めるための分析の軸の1つとする。",
 ], "method"),
 ("pl5", "Contribution", "期待される貢献と限界", [
  "本研究は、場所と記憶の研究に、災害の非日常が常態になっていくという気候変動時代の条件を持ち込む。また、深層民主主義の概念を気候災害の被災地へと広げ、その適用範囲と限界を検討する。これにより、制度による防災や復興計画だけでは捉えられない、地域の文化と人々のつながりが回復を支える仕組みを明らかにすることを目指す。",
  "一方で、単一地域の民族誌から言えるのは、その地域で観察された過程までである。結論を被災地一般に広げるには、先行事例との照合や他地域との比較を重ねる必要がある。",
 ], None),
]

RQ = [
 ("問い1", "災害の前後で、人々は場所の何を記憶し、何を忘れ、何を新たな記憶として立ち上げるのか。"),
 ("問い2", "その記憶の作り直しのなかで、行政や自治会といった形式とは別の、どのような合意と相互扶助の形が生まれるのか。"),
 ("問い3", "そうした地域の実践は、他地域や国外の被災経験・気候運動とどのようにつながっているのか。あるいは、つながれずにいるのか。"),
]

METHOD = [
 ("対象", "近年、豪雨などの気候災害を繰り返し経験している国内の一地域（仮置き・指導教員と調整）"),
 ("方法", "参与観察・半構造化インタビュー・資料分析（記録誌・地域紙・記念碑や伝承碑）"),
 ("期間", "修士課程2年間のうち約1年（仮置き）。出水期の前後を含め、備えと記憶の季節による動きを追う"),
 ("分析の軸", "上から与えられる記憶と、暮らしのなかで生きられる記憶の区別／蓮葉果紅という組織におけるコミュニティとの対比"),
]

BUTTON = '  <a class="lit-tab" role="tab" id="tabbtn-plan" href="#tab-plan" aria-controls="tab-plan"><span class="n">03</span>研究計画（修士論文）</a>\n'
COVER_NOTE = "<br>2026.10.16 追加: タブ3「研究計画（修士論文）」論考と計画の下書き"


def paras(ps):
    return "\n".join(f'  <p class="lit-summary">{e(p)}</p>' for p in ps)


def extra(kind):
    if kind == "rq":
        rows = "\n".join(f'    <li><b>{e(k)}</b>　{e(v)}</li>' for k, v in RQ)
        return f'  <ul class="pts">\n{rows}\n  </ul>\n'
    if kind == "method":
        rows = "\n".join(f'      <tr><td class="nm">{e(k)}</td><td>{e(v)}</td></tr>' for k, v in METHOD)
        return ('  <table class="tbl plan-tbl">\n    <thead><tr><th scope="col">項目</th><th scope="col">内容</th></tr></thead>\n'
                f'    <tbody>\n{rows}\n    </tbody>\n  </table>\n')
    return ""


def chars(ps):
    return sum(len(p) for p in ps)


def build():
    plan_body_chars = sum(chars(ps) for _, _, _, ps, _ in PLAN) + sum(len(v) for _, v in RQ)
    toc_a = '      <a class="toc-item" href="#p-essay"><span class="n">B-1</span><span class="t">参考論考：問題意識<small>' + e(ESSAY_TITLE) + '</small></span></a>'
    toc_b = "\n".join(
        f'      <a class="toc-item" href="#{sid}"><span class="n">{i:02d}</span><span class="t">{e(h)}<small>{e(en)}</small></span></a>'
        for i, (sid, en, h, _, _) in enumerate(PLAN, 1))
    plan_html = "\n".join(
        f'''<section class="section" id="{sid}">
  <div class="sec-head"><div class="eyebrow"><span class="n">{i:02d}</span>{e(en)}</div><h2>{e(h)}</h2></div>
{paras(ps)}
{extra(kind)}</section>'''
        for i, (sid, en, h, ps, kind) in enumerate(PLAN, 1))
    return f'''<!-- TAB:plan:begin (generated by tools/plan_tab.py) -->
<div class="lit-panel" id="tab-plan" role="tabpanel" aria-labelledby="tabbtn-plan">
<main class="page">
<section class="section" id="p-intro">
  <div class="sec-head">
    <div class="eyebrow"><span class="n">00</span>Research plan · Draft</div>
    <h2>{e(TITLE)}</h2>
    <p class="plan-sub">{e(SUBTITLE)}</p>
    <p class="lead">タブ1「地域の文化 × 都市の記憶」とタブ2「災害・気候変動 × 場所の記憶」の文献を下敷きに組み立てた、修士論文の研究計画の下書きである。巻末に、研究の背景にある問題意識を述べた論考を参考として添える。</p>
  </div>
  <div class="facts">
    <div class="fact"><div class="fact-label">研究計画</div><div class="fact-num ink">{plan_body_chars:,}<span class="unit">字</span></div><div class="fact-desc">背景・理論的基盤・問い・方法・貢献</div></div>
    <div class="fact"><div class="fact-label">参考論考</div><div class="fact-num ink">{chars(ESSAY):,}<span class="unit">字</span></div><div class="fact-desc">巻末「{e(ESSAY_TITLE)}」</div></div>
    <div class="fact"><div class="fact-label">研究の問い</div><div class="fact-num ink">{len(RQ)}<span class="unit">つ</span></div><div class="fact-desc">記憶の作り直し・形式の外の合意・地域とグローバルの接続</div></div>
  </div>
  <div class="note ink">下書き（2026-10-16）。理論的基盤の中心に据える2本（場所と記憶の包括的な批判的論考、深層民主主義の論文）は特定を確認中のため、書誌を挙げていない。調査地と調査期間は仮置きで、指導教員との調整を前提とする。引用した文献はタブ1・タブ2に書誌と概要がある。</div>
</section>

<section class="section" id="p-toc">
  <div class="sec-head"><div class="eyebrow"><span class="n">00</span>Contents</div><h2>目次</h2></div>
  <div class="toc">
    <div class="toc-col a">
      <div class="toc-head"><div class="letter">A</div><div class="lab"><small>Part A</small>研究計画</div></div>
{toc_b}
    </div>
    <div class="toc-col b">
      <div class="toc-head"><div class="letter">B</div><div class="lab"><small>Part B</small>参考</div></div>
{toc_a}
    </div>
  </div>
</section>

<section class="section" id="p-plan-head">
  <div class="sec-head">
    <div class="eyebrow"><span class="n">A</span>Research plan</div>
    <h2>研究計画</h2>
    <p class="lead">{e(TITLE)}――{e(SUBTITLE)}</p>
  </div>
</section>

{plan_html}

<section class="section" id="p-essay">
  <div class="sec-head">
    <div class="eyebrow"><span class="n">B-1</span>Appendix · Problem statement</div>
    <h2>{e(ESSAY_TITLE)}</h2>
    <p class="lead">参考として、研究計画の背景にある問題意識を論考として述べる。</p>
  </div>
{paras(ESSAY)}
</section>
</main>
</div>
<!-- TAB:plan:end -->
'''


STYLE = '''<style id="plan-tab-style">
#tab-plan .plan-sub { font-size: var(--fs-lead); font-weight: 700; color: var(--ink-soft); margin: 8px 0 0; }
#tab-plan p.lit-summary { text-indent: 1em; line-height: 1.95; }
#tab-plan .facts { grid-template-columns: repeat(3, minmax(0, 1fr)); }
#tab-plan table.plan-tbl { max-width: var(--measure-wide); }
#tab-plan table.plan-tbl td.nm { width: 8em; white-space: nowrap; vertical-align: top; }
#tab-plan table.plan-tbl td { vertical-align: top; line-height: 1.7; }
#tab-plan ul.pts b { color: var(--accent); }
@media (max-width: 800px) { #tab-plan .facts { grid-template-columns: 1fr; } #tab-plan table.plan-tbl td.nm { width: auto; white-space: normal; } }
</style>
'''


def main():
    src = PAGE.read_text(encoding="utf-8")
    block = build()
    if "<!-- TAB:plan:begin" in src:
        src = re.sub(r"<!-- TAB:plan:begin.*?<!-- TAB:plan:end -->\n", lambda m: block, src, flags=re.S)
    else:
        src = src.replace("<!-- TAB:disaster:end -->\n", "<!-- TAB:disaster:end -->\n" + block, 1)
    if 'id="tabbtn-plan"' not in src:
        anchor = re.search(r'  <a class="lit-tab"[^\n]*id="tabbtn-disaster"[^\n]*\n', src)
        src = src[:anchor.end()] + BUTTON + src[anchor.end():]
    src = re.sub(r'<br>2026\.10\.16 追加: タブ3「研究計画（修士論文）」[^<]*', COVER_NOTE, src, count=1)
    if "タブ3「研究計画" not in src:
        src = src.replace("タブ2「災害・気候変動 × 場所の記憶」論文10本</div>",
                          "タブ2「災害・気候変動 × 場所の記憶」論文10本" + COVER_NOTE + "</div>", 1)
    if 'id="plan-tab-style"' in src:
        src = re.sub(r'<style id="plan-tab-style">.*?</style>\n', lambda m: STYLE, src, flags=re.S)
    else:
        src = src.replace("</head>", STYLE + "</head>", 1)
    PAGE.write_text(src, encoding="utf-8")


if __name__ == "__main__":
    main()
