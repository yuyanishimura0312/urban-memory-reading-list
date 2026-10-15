"""Generate the 'issue notes' tab (tab 4) and insert it into index.html.

Five key points of the research plan in tab 3, each as a short statement plus
concrete details. Every detail restates what tab 3 (plan or appendix essay)
already says; cited works are those listed in tabs 1-2.
Re-running is idempotent: the block between the TAB markers is replaced, and the
tab button, cover note and style are added once.
"""
import html, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
e = html.escape

POINTS = [
 ("気候災害は「断絶」から「条件」へ変わり、非日常が日常になる",
  "研究全体の出発点。",
  ["豪雨・洪水・猛暑・山火事が同じ地域を繰り返し襲うと、災害は一時的な出来事ではなく暮らしの前提になる。",
   "「被災し、復旧し、元の暮らしへ戻る」という復興の時間の型が、そのままでは成り立たなくなる。",
   "問うのは、この非日常の常態化が、場所の記憶と人々のつながりに何を求めるのかである。"]),
 ("場所の記憶を「保存」ではなく「作り直し」として捉える",
  "記憶研究が暗に前提としてきた、場所の安定性を問い直す。",
  ["ノラ（1989）の「記憶の場」は、失われゆくものを場所に託して保存する営みとして記憶を描いた。",
   "託すはずの場所そのものが壊れ、形を変えるとき、保存という発想はそのままでは成り立たない。",
   "故郷にとどまったまま、故郷が変わっていく苦しみを、アルブレヒトら（2007）は「ソラスタルジア」と名づけた。"]),
 ("記憶も災害も、「誰の過去を残すか」をめぐる政治の問題である",
  "技術や自然現象の問題として閉じず、権力と選別の問題として読む。",
  ["コナトン（2008）は、「忘れる」の内側に抑圧的な抹消や計画的な陳腐化など、少なくとも7つの型があることを示した。",
   "ハーツフェルド（2010）は、歴史の保存がかえって住民の入れ替わりを正当化する過程を描いた。",
   "オリバー＝スミス（1996）は、災害を破壊的な力と社会が生んだ脆弱性との組み合わせとして捉えた。"]),
 ("回復を支えるのは、形式の外側に根づく人々のつながりである",
  "深層民主主義を手がかりに、制度の外の合意と相互扶助を記述する。",
  ["アルドリッチとマイヤー（2015）は、回復を左右するのは堤防などの物理的な基盤より、人と人のつながりという社会的な基盤だという知見をまとめた。",
   "深層民主主義は、投票や議会といった形式とは別に、日々の実践に根づく民主主義の形と、地域とグローバルをつなぐ回路を捉える。",
   "蓮葉果紅という組織におけるコミュニティ（成員と目的を持つ）と、成員も目的も定まらず境界を越えて結びつくつながりとを対比し、両者が補い合うのか、別の原理で動くのかを問う。"]),
 ("記憶は、変化に備えるための共同の資源になりうる",
  "喪失を嘆く装置ではなく、次の災害を生き延びる力として記憶を捉え、民族誌で確かめる。",
  ["バルテルら（2010）は、市民農園で受け継がれる知恵や慣習を「社会・生態の記憶」と呼び、変化から立ち直る力の源とした。",
   "ティル（2012）の「記憶の作業」とケアの倫理、コックスとペリー（2011）の「再定位」は、記憶を作り直す実践を捉える手がかりになる。",
   "研究では、気候災害を繰り返し経験する地域で参与観察と聞き取りを行い、人々が実際に何を覚え、誰と何を決めているのかを確かめる。"]),
]

BUTTON = '  <a class="lit-tab" role="tab" id="tabbtn-notes" href="#tab-notes" aria-controls="tab-notes"><span class="n">04</span>論点ノート</a>\n'
COVER_NOTE = "<br>2026.10.16 追加: タブ4「論点ノート」研究計画の要点5つ"

STYLE = '''<style id="notes-tab-style">
#tab-notes ol.notes { list-style: none; counter-reset: none; padding: 0; margin: var(--space-3) 0 0; max-width: var(--measure-wide); }
#tab-notes ol.notes > li { display: grid; grid-template-columns: 3.2em 1fr; gap: 0 var(--space-2); padding: var(--space-3) 0; border-top: 1px solid var(--es-rule-light); }
#tab-notes ol.notes > li:first-child { border-top: 2px solid var(--es-ink); }
#tab-notes .nn { font-family: var(--font-mono); font-size: 1.6rem; font-weight: 700; color: var(--accent); line-height: 1.2; }
#tab-notes .nh { font-size: 1.15rem; font-weight: 900; line-height: 1.5; margin: 0; max-width: var(--measure); }
#tab-notes .ns { color: var(--ink-soft); font-weight: 500; margin: 6px 0 10px; max-width: var(--measure); }
#tab-notes ol.notes ul.pts { margin: 0; }
#tab-notes .nrefs { margin-top: var(--space-2); max-width: var(--measure); }
#tab-notes .nrefs .subhead { margin-top: var(--space-2); }
#tab-notes ol.nreflist { list-style: none; padding: 0; margin: 0; }
#tab-notes ol.nreflist > li { padding: 14px 0; border-top: 1px solid var(--es-rule-light); }
#tab-notes ol.nreflist > li:first-child { border-top: 0; padding-top: 4px; }
#tab-notes .ncite { font-size: 14px; line-height: 1.7; font-weight: 700; margin: 0 0 8px; overflow-wrap: anywhere; }
#tab-notes .ncite a { font-weight: 400; color: var(--es-ink-mute); margin-left: 4px; }
#tab-notes .ncite .lit-basis { margin-left: 8px; }
#tab-notes blockquote.nq { margin: 0 0 8px; padding: 8px 14px; border-left: 3px solid var(--accent); background: var(--surface-warm); font-size: 14px; line-height: 1.7; }
#tab-notes .nja, #tab-notes .nuse { font-size: 14px; line-height: 1.8; margin: 0 0 6px; }
#tab-notes .nl { display: inline-block; font-size: 11px; font-weight: 700; letter-spacing: .12em; color: var(--accent); border: 1px solid var(--accent); padding: 0 6px; margin-right: 8px; vertical-align: 1px; }
#tab-notes .nbasis { font-size: 12px; color: var(--es-ink-mute); margin: 0; }
@media (max-width: 800px) { #tab-notes ol.notes > li { grid-template-columns: 2.4em 1fr; } }
</style>
'''


# References per point. quote = verbatim English from the source; basis says where it was
# checked: 要旨 = abstract via Crossref/OpenAlex, 本文 = full text PDF, 二次 = secondary
# citations only. quote=None means no verbatim text could be checked, so none is given.
# ja = our translation (not a quotation). role marks works beyond tab 3.
REFS = {
 1: [
  dict(cite="Norris, F. H., Stevens, S. P., Pfefferbaum, B., Wyche, K. F., & Pfefferbaum, R. L. (2008). Community resilience as a metaphor, theory, set of capacities, and strategy for disaster readiness. American Journal of Community Psychology, 41(1-2), 127-150.",
       doi="10.1007/s10464-007-9156-6", basis="要旨", role="補足（タブ2より）",
       quote="Community resilience is a process linking a network of adaptive capacities (resources with dynamic attributes) to adaptation after a disturbance or adversity.",
       ja="地域の回復力とは、適応能力（動的な性質をもつ資源）の網を、撹乱や逆境の後の適応へとつなぐ過程である。",
       use="回復を「元に戻ること」ではなく、繰り返す撹乱への適応の過程として捉える枠組みとして参照する。"),
  dict(cite="Adger, W. N., Barnett, J., Brown, K., Marshall, N., & O'Brien, K. (2013). Cultural dimensions of climate change impacts and adaptation. Nature Climate Change, 3(2), 112-117.",
       doi="10.1038/nclimate1666", basis=None, role="補足（タブ2より）", quote=None, ja=None,
       use="気候変動の被害と適応を、物理的・経済的な損失だけでなく文化の次元から捉え直す議論として参照する。"),
  dict(cite="Cutter, S. L., Barnes, L., Berry, M., Burton, C., Evans, E., Tate, E., & Webb, J. (2008). A place-based model for understanding community resilience to natural disasters. Global Environmental Change, 18(4), 598-606.",
       doi="10.1016/j.gloenvcha.2008.07.013", basis=None, role="補足（タブ2より）", quote=None, ja=None,
       use="災害の前から地域が抱える社会・自然・建造環境の条件が回復を左右するという、場所を単位とするモデル（DROP）として参照する。"),
 ],
 2: [
  dict(cite="Nora, P. (1989). Between memory and history: Les lieux de mémoire. Representations, 26, 7-24.",
       doi="10.2307/2928520", basis="二次", role=None,
       quote="There are lieux de mémoire, sites of memory, because there are no longer milieux de mémoire, real environments of memory.",
       ja="記憶の場があるのは、もはや記憶の環境、つまり現実に記憶が生きられる環境がないからである。",
       use="記憶を、失われゆくものを場所に託して保存する営みとして描いた出発点として参照し、その前提（場所の安定）を問い直す。"),
  dict(cite="Hoelscher, S., & Alderman, D. H. (2004). Memory and place: Geographies of a critical relationship. Social & Cultural Geography, 5(3), 347-355.",
       doi="10.1080/1464936042000252769", basis="要旨", role="基盤論文の候補（特定は確認中）",
       quote="Together, memory and place conjoin to produce much of the context for modern identities;",
       ja="記憶と場所は結びついて、近代のアイデンティティの文脈の多くを生み出している。",
       use="場所と記憶の研究を包括的・批判的に整理した論考の候補。研究計画の理論的基盤の一方の柱に当たる。"),
  dict(cite="Albrecht, G., Sartore, G.-M., Connor, L., Higginbotham, N., Freeman, S., Kelly, B., Stain, H., Tonna, A., & Pollard, G. (2007). Solastalgia: The distress caused by environmental change. Australasian Psychiatry, 15(Suppl. 1), S95-S98.",
       doi="10.1080/10398560701701288", basis="要旨", role=None,
       quote="solastalgia is the distress that is produced by environmental change impacting on people while they are directly connected to their home environment.",
       ja="ソラスタルジアとは、人々が住まいの環境と直接つながったままでいるときに、環境の変化がもたらす苦しみである。",
       use="場所が壊れ、変わっていく只中での記憶と愛着の経験を名指す概念として参照する。"),
 ],
 3: [
  dict(cite="Connerton, P. (2008). Seven types of forgetting. Memory Studies, 1(1), 59-71.",
       doi="10.1177/1750698007083889", basis="要旨", role=None,
       quote="I suggest that we can distinguish at least seven types: repressive erasure; prescriptive forgetting; forgetting that is constitutive in the formation of a new identity; structural amnesia; forgetting as annulment; forgetting as planned obsolescence; forgetting as humiliated silence.",
       ja="少なくとも7つの型を区別できる。抑圧的な抹消、規範として求められる忘却、新しいアイデンティティの形成を構成する忘却、構造的な健忘、無効化としての忘却、計画的な陳腐化としての忘却、屈辱による沈黙としての忘却である。",
       use="復興や再開発で何が忘れられるのかを、一様な喪失ではなく型の違う忘却として読み分ける道具として参照する。"),
  dict(cite="Herzfeld, M. (2010). Engagement, gentrification, and the neoliberal hijacking of history. Current Anthropology, 51(S2), S259-S267.",
       doi="10.1086/653420", basis=None, role=None, quote=None, ja=None,
       use="歴史的な町並みの保存が、住民の入れ替わり（ジェントリフィケーション）を正当化する口実になる過程の民族誌として参照する。"),
  dict(cite="Oliver-Smith, A. (1996). Anthropological research on hazards and disasters. Annual Review of Anthropology, 25, 303-328.",
       doi="10.1146/annurev.anthro.25.1.303", basis="要旨", role=None,
       quote="Recent perspectives in anthropological research define a disaster as a process/event involving the combination of a potentially destructive agent(s) from the natural and/or technological environment and a population in a socially and technologically produced condition of vulnerability.",
       ja="近年の人類学の研究は、災害を、自然や技術の環境に由来する潜在的に破壊的な力と、社会的・技術的に生み出された脆弱な状態にある人々との組み合わせからなる過程であり出来事であると定義する。",
       use="災害を自然現象ではなく、社会が生み出した脆弱性の問題として捉える視座として参照する。"),
 ],
 4: [
  dict(cite="Aldrich, D. P., & Meyer, M. A. (2015). Social capital and community resilience. American Behavioral Scientist, 59(2), 254-269.",
       doi="10.1177/0002764214550299", basis="要旨", role=None,
       quote="...continue to spend heavily on hardening levees, raising existing homes, and repairing damaged facilities despite evidence that social, not physical, infrastructure drives resilience.",
       ja="（政府機関は）回復力を駆動するのは物理的な基盤ではなく社会的な基盤だという証拠があるにもかかわらず、堤防の強化や住宅のかさ上げ、被災施設の修繕に多額の費用を投じ続けている。",
       use="回復を支えるのが人と人のつながりであることを示す知見として参照する。"),
  dict(cite="Appadurai, A. (2001). Deep democracy: Urban governmentality and the horizon of politics. Environment and Urbanization, 13(2), 23-43.",
       doi="10.1177/095624780101300203", basis="要旨", role="基盤論文の候補（特定は確認中）",
       quote="They are, or can be, instruments of deep democracy, rooted in local context and able to mediate globalizing forces in ways that benefit the poor.",
       ja="それら（都市貧困層の連合）は深層民主主義の道具であり、あるいはそうなりうる。地域の文脈に根ざし、グローバル化の力を貧しい人々の利益になるように媒介することができる。",
       use="形式的な制度の外側で人々の実践に根づく民主主義と、地域とグローバルをつなぐ回路を捉える概念として参照する。同じ要旨は「下からのグローバル化のネットワーク（networks of globalization from below）」にも触れている。"),
 ],
 5: [
  dict(cite="Barthel, S., Folke, C., & Colding, J. (2010). Social-ecological memory in urban gardens: Retaining the capacity for management of ecosystem services. Global Environmental Change, 20(2), 255-265.",
       doi="10.1016/j.gloenvcha.2010.01.001", basis=None, role=None, quote=None, ja=None,
       use="市民農園で受け継がれる知恵と慣習を「社会・生態の記憶」と呼び、変化から立ち直る力の源とする議論として参照する。"),
  dict(cite="Till, K. E. (2012). Wounded cities: Memory-work and a place-based ethics of care. Political Geography, 31(1), 3-14.",
       doi="10.1016/j.polgeo.2011.10.008", basis="本文", role=None,
       quote="Through memory-work and what I call a place-based ethics of care, historical and current resources might sustain more just possible futures. (p. 5)",
       ja="記憶の作業と、私が場所に根ざしたケアの倫理と呼ぶものを通じて、歴史的な資源と現在の資源は、より公正でありうる未来を支えうる。",
       use="記憶を作り直す実践を、喪失への応答ではなく未来を支えるケアとして捉える手がかりとして参照する。同論文は「傷ついた都市」を、国家による暴力がもたらした物理的な破壊・立ち退き・個人と社会のトラウマの歴史によって損なわれ、形づくられてきた密集地と定義している（p. 6）。"),
  dict(cite="Cox, R. S., & Perry, K.-M. E. (2011). Like a fish out of water: Reconsidering disaster recovery and the role of place and social capital in community disaster resilience. American Journal of Community Psychology, 48(3-4), 395-411.",
       doi="10.1007/s10464-011-9427-0", basis="要旨", role=None,
       quote="The reorientation process emphasizes the critical importance of place not only as an orienting framework in recovery but also as the ground upon which social capital and community disaster resilience are built.",
       ja="再定位の過程は、場所が、回復における方向づけの枠組みとしてだけでなく、社会関係資本と地域の災害回復力が築かれる土台としても決定的に重要であることを示している。",
       use="被災後に人々が場所との関係のなかで向きを取り直す過程を捉える概念として参照する。"),
 ],
}

BASIS_LABEL = {"要旨": "要旨で照合", "本文": "全文で照合", "二次": "二次文献での引用に基づく・原文は未照合"}


def refs_html(i):
    out = []
    for r in REFS[i]:
        tag = f'<span class="lit-basis">{e(r["role"])}</span>' if r.get("role") else ""
        q = ""
        if r["quote"]:
            q = (f'\n            <blockquote class="nq" lang="en">{e(r["quote"])}</blockquote>'
                 f'\n            <p class="nja"><span class="nl">訳</span>{e(r["ja"])}</p>')
        basis = BASIS_LABEL.get(r["basis"], "引用は未照合（要旨・本文に到達できず）のため、書誌と参照のみ記す")
        out.append(f'''          <li>
            <p class="ncite">{e(r["cite"])} <a href="https://doi.org/{e(r["doi"])}">doi:{e(r["doi"])}</a>{tag}</p>{q}
            <p class="nuse"><span class="nl">参照</span>{e(r["use"])}</p>
            <p class="nbasis">{e(basis)}</p>
          </li>''')
    return '        <div class="nrefs">\n          <div class="subhead">文献と引用</div>\n          <ol class="nreflist">\n' + "\n".join(out) + "\n          </ol>\n        </div>\n"


def build():
    items = "\n".join(
        f'''    <li id="n{i}">
      <div class="nn">{i:02d}</div>
      <div>
        <p class="nh">{e(head)}</p>
        <p class="ns">{e(sub)}</p>
        <ul class="pts">
''' + "\n".join(f'          <li>{e(d)}</li>' for d in details) + '''
        </ul>
''' + refs_html(i) + '''      </div>
    </li>'''
        for i, (head, sub, details) in enumerate(POINTS, 1))
    return f'''<!-- TAB:notes:begin (generated by tools/notes_tab.py) -->
<div class="lit-panel" id="tab-notes" role="tabpanel" aria-labelledby="tabbtn-notes">
<main class="page">
<section class="section" id="n-intro">
  <div class="sec-head">
    <div class="eyebrow"><span class="n">00</span>Issue notes</div>
    <h2>論点ノート ― 研究計画の要点5つ</h2>
    <p class="lead">タブ3「研究計画（修士論文）」の記述のうち、要となる論点を5つに絞った。各論点は、簡潔な記述と具体的な詳細に続けて、拠り所となる論文・著者・原文からの引用・本研究での参照の仕方を示す。原文の引用は、要旨または全文と照合できたものに限り、照合できなかった文献は書誌と参照のみを記す。訳は引用ではなく、本ノートによる訳である。</p>
  </div>
  <ol class="notes">
{items}
  </ol>
  <div class="note ink">研究計画と同じく下書き（2026-10-16）。理論的基盤の中心に据える2本（場所と記憶の包括的な批判的論考、深層民主主義の論文）は特定を確認中。</div>
</section>
</main>
</div>
<!-- TAB:notes:end -->
'''


def main():
    src = PAGE.read_text(encoding="utf-8")
    block = build()
    if "<!-- TAB:notes:begin" in src:
        src = re.sub(r"<!-- TAB:notes:begin.*?<!-- TAB:notes:end -->\n", lambda m: block, src, flags=re.S)
    else:
        src = src.replace("<!-- TAB:plan:end -->\n", "<!-- TAB:plan:end -->\n" + block, 1)
    if 'id="tabbtn-notes"' not in src:
        anchor = re.search(r'  <a class="lit-tab"[^\n]*id="tabbtn-plan"[^\n]*\n', src)
        src = src[:anchor.end()] + BUTTON + src[anchor.end():]
    if "タブ4「論点ノート」" not in src:
        src = re.sub(r'(タブ3「研究計画（修士論文）」[^<]*)', lambda m: m.group(1) + COVER_NOTE, src, count=1)
    if 'id="notes-tab-style"' in src:
        src = re.sub(r'<style id="notes-tab-style">.*?</style>\n', lambda m: STYLE, src, flags=re.S)
    else:
        src = src.replace("</head>", STYLE + "</head>", 1)
    PAGE.write_text(src, encoding="utf-8")


if __name__ == "__main__":
    main()
