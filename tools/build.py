"""팔리 사이클 코리아 사이트 빌드.

index.src.html(한국어 원본)에서
  1) 지오메트리 표를 채워 index.html(한국어)을 만들고
  2) i18n/en.json, i18n/ja.json 번역으로 en/index.html, ja/index.html을 만들고
  3) sitemap.xml을 다시 씁니다.

사용법: python3 tools/build.py
문구를 고친 뒤에는 python3 i18n/extract.py 로 ko.json을 갱신하고,
새로 생긴 문장만 en.json / ja.json에 추가한 다음 빌드합니다.
"""
import json, re, sys, pathlib
from bs4 import BeautifulSoup, NavigableString, Comment

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'i18n'))
from extract import HANGUL  # noqa: E402

SITE = 'https://parleecycles.co.kr/'

# ---------------------------------------------------------------- geometry
def table(sizes, rows):
    h = '<table class="geo"><thead><tr><th></th>' + ''.join(f'<th>{s}</th>' for s in sizes) + '</tr></thead><tbody>'
    for name, vals in rows:
        vals = vals.split()
        if len(vals) == 1:
            vals = vals * len(sizes)
        assert len(vals) == len(sizes), (name, vals)
        h += f'<tr><th>{name}</th>' + ''.join(f'<td>{v}</td>' for v in vals) + '</tr>'
    return h + '</tbody></table>'

S5 = ['XS', 'S', 'M', 'L', 'XL']
S6 = ['XS', 'S', 'M', 'L', 'XL', '2XL']
GEO = {
 '{{GEO_OURAY}}': table(S5, [
  ('탑튜브 길이 (가상)', '507 526 547 568 588'), ('스택', '536 558 579 606 628'), ('리치', '363 366 375 382 393'),
  ('헤드 앵글', '70.75 71 71.5 72 72.5'), ('싯튜브 앵글', '75 74 73.5 73 72.5'), ('싯튜브 길이 (실측)', '415 455 492 537 574'),
  ('체인스테이 길이', '420'), ('BB 드롭', '80 80 80 80 77'), ('포크 레이크', '53 53 45 45 45'),
  ('스탠드오버', '693 728 759 798 831'), ('헤드튜브 길이', '125 147 164 191 214'), ('프론트 센터', '584 592 595 606 619'),
  ('휠베이스', '991 999 1002 1013 1027'), ('포크 길이', '380')]),
 '{{GEO_GT_RACE}}': table(S6, [
  ('스택', '513 535 552 584 603 635'), ('리치', '375 378 388 396 405 407'), ('탑튜브 길이 (가상)', '515 533 552 575 592 603'),
  ('싯튜브 길이 (C-C)', '417 438 464 494 504 543'), ('탑튜브 슬로프 (°)', '9 9 8 8 8 8'), ('헤드 앵글', '70.5 71.5 72 72.5 72.5 73'),
  ('싯튜브 앵글', '75 74 73.5 73 72.75 72.75'), ('체인스테이 길이', '422'), ('BB 드롭', '80 80 80 80 77 77'), ('포크 레이크', '47'),
  ('스탠드오버', '725 745 766 794 807 846'), ('헤드튜브 길이', '102 121 137 169 192 220'), ('프론트 센터', '583 585 596 610 624 630'),
  ('휠베이스', '992 994 1005 1019 1035 1041'), ('트레일', '72 66 63 59 59 56'), ('포크 길이', '377')]),
 '{{GEO_GT_SPORT}}': table(S6, [
  ('스택', '535 558 572 606 627 650'), ('리치', '363 366 372 382 388 393'), ('탑튜브 길이 (가상)', '510 528 543 568 583 595'),
  ('싯튜브 길이 (C-C)', '437 461 487 512 539 564'), ('탑튜브 슬로프 (°)', '9 9 8 8 8 8'), ('헤드 앵글', '70.25 71 71.5 72 72 72.25'),
  ('싯튜브 앵글', '75 74 73.5 73 72.75 72.75'), ('체인스테이 길이', '427'), ('BB 드롭', '80 80 80 80 77 77'), ('포크 레이크', '47'),
  ('스탠드오버', '744 767 787 811 840 865'), ('헤드튜브 길이', '127 148 161 194 219 243'), ('프론트 센터', '582 586 592 608 621 630'),
  ('휠베이스', '996 1000 1006 1022 1036 1046'), ('트레일', '74 69 66 63 63 61'), ('포크 길이', '377')]),
}

def build_ko():
    s = (ROOT / 'index.src.html').read_text()
    for k, v in GEO.items():
        s = s.replace(k, v)
    assert '{{' not in s
    assert '—' not in re.sub(r'<!--.*?-->', '', s, flags=re.S), 'em dash in Korean page'
    (ROOT / 'index.html').write_text(s)
    return s

# ---------------------------------------------------------------- translate
LANG = {
 'en': {'locale': 'en_US', 'path': 'en/'},
 'ja': {'locale': 'ja_JP', 'path': 'ja/'},
}

def translate(ko_html, lang):
    tr = json.loads((ROOT / f'i18n/{lang}.json').read_text())
    missing = set()
    def t(s):
        k = s.strip()
        if not HANGUL.search(k):
            return s
        if k in tr:
            return s.replace(k, tr[k])
        missing.add(k)
        return s

    soup = BeautifulSoup(ko_html, 'html.parser')
    soup.html['lang'] = lang
    if soup.title:
        soup.title.string = t(soup.title.string)
    for m in soup.find_all('meta'):
        if m.has_attr('content'):
            m['content'] = t(m['content'])
    for sc in soup.find_all('script', type='application/ld+json'):
        data = json.loads(sc.string)
        def walk(o):
            if isinstance(o, dict):
                return {k: walk(v) for k, v in o.items()}
            if isinstance(o, list):
                return [walk(v) for v in o]
            if isinstance(o, str):
                return t(o)
            return o
        data = walk(data)
        for node in data.get('@graph', []):
            if node.get('@type') == 'WebSite':
                node['url'] = SITE + LANG[lang]['path']
                node['inLanguage'] = lang
        sc.string = '\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    for el in soup.body.find_all(True):
        for a in ('alt', 'aria-label', 'title'):
            if el.has_attr(a):
                el[a] = t(el[a])

    def visit(el):
        if el.name in ('script', 'style'):
            return
        direct = any(isinstance(c, NavigableString) and not isinstance(c, Comment) and HANGUL.search(c) for c in el.children)
        if direct:
            k = el.decode_contents().strip()
            if k in tr:
                el.clear()
                frag = BeautifulSoup(tr[k], 'html.parser')
                for c in list(frag.contents):
                    el.append(c)
            else:
                missing.add(k)
            return
        for c in list(el.children):
            if getattr(c, 'name', None):
                visit(c)
    visit(soup.body)

    # canonical, og, hreflang self, language switcher
    soup.find('link', rel='canonical')['href'] = SITE + LANG[lang]['path']
    soup.find('meta', property='og:url')['content'] = SITE + LANG[lang]['path']
    soup.find('meta', property='og:locale')['content'] = LANG[lang]['locale']
    for a in soup.select('nav.lang a'):
        code = a['hreflang']
        a['href'] = '../' if code == 'ko' else ('./' if code == lang else f'../{code}/')
        if code == lang:
            a['class'] = ['on']; a['aria-current'] = 'page'
        else:
            a.attrs.pop('class', None); a.attrs.pop('aria-current', None)
    if lang == 'ja':
        f = soup.find('link', href=re.compile('fonts.googleapis.com/css2'))
        f['href'] = f['href'].replace('&display=swap', '&family=Noto+Sans+JP:wght@300;400;700&display=swap')

    out = str(soup)
    # 하위 폴더에서 이미지 경로 보정
    out = out.replace('src="images/', 'src="../images/').replace('url(images/', 'url(../images/').replace('href="images/', 'href="../images/')
    left = [k for k in missing]
    return out, left

def sitemap(html):
    imgs = sorted(set(re.findall(r'images/[\w/.-]+\.(?:jpg|png|webp)', html)))
    imgs = [i for i in imgs if not re.search(r'logo|favicon|apple-touch', i)]
    alts = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{h}" href="{SITE}{p}"/>' for h, p in [('ko', ''), ('en', 'en/'), ('ja', 'ja/'), ('x-default', '')])
    urls = []
    for p in ['', 'en/', 'ja/']:
        u = f'  <url>\n    <loc>{SITE}{p}</loc>{alts}\n    <lastmod>2026-10-22</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{"1.0" if not p else "0.8"}</priority>'
        if not p:
            u += ''.join(f'\n    <image:image><image:loc>{SITE}{i}</image:loc></image:image>' for i in imgs)
        urls.append(u + '\n  </url>')
    x = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
         'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
         + '\n'.join(urls) + '\n</urlset>\n')
    (ROOT / 'sitemap.xml').write_text(x)

if __name__ == '__main__':
    ko = build_ko()
    print('ko  index.html', len(ko))
    for lang in LANG:
        if not (ROOT / f'i18n/{lang}.json').exists():
            print(lang, 'skipped (no translation file)'); continue
        out, left = translate(ko, lang)
        d = ROOT / LANG[lang]['path']; d.mkdir(exist_ok=True)
        (d / 'index.html').write_text(out)
        hangul = len(HANGUL.findall(re.sub(r'<script(?![^>]*ld\+json).*?</script>', '', out, flags=re.S)))
        print(lang, f'{d.name}/index.html', len(out), 'untranslated units:', len(left), 'hangul chars left:', hangul)
        for k in left[:20]:
            print('   -', k[:90])
    sitemap(ko)
