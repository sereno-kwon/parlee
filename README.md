# Parlee Cycles Korea

parleecycles.co.kr 원페이지 정적 사이트 (GitHub Pages). tsubasabicycles.co.kr, bastioncycles.co.kr과 같은 구조입니다.

- `index.html` 한국어 원페이지 (PARLEE · OURAY · TAOS · Z-ZERO GT · BESPOKE · PAINT LAB · HISTORY · SHOWROOM)
- `en/index.html`, `ja/index.html` 영어 · 일본어 페이지 (빌드로 생성, 직접 수정하지 않음)
- `index.src.html` 편집용 한국어 원본. 지오메트리 표는 `{{GEO_*}}` 자리에 빌드 시 채워집니다.
- `i18n/` 번역 사전 (`ko.json` 원문 목록, `en.json` · `ja.json` 원문→번역)
- `tools/build.py` 한국어 페이지, 번역 페이지, sitemap.xml을 한 번에 생성
- `404.html` 하위 주소(/ouray, /taos, /z-zero-gt 등)를 섹션으로 연결
- `images/` 섹션별 이미지 (`hero`, `brand`, `ouray`, `taos`, `gt`, `anniversary`, `bespoke`, `process`, `team`, `paint`, `history`)
- `.github/image-manifest.txt` + `fetch-images.yml` 팔리 공식 사이트(parleecycles.com) CDN 이미지 이전용 워크플로

## 이미지
매니페스트를 수정해 main에 푸시하면 Actions가 이미지를 받아 `images/`에 커밋합니다.
이미 받은 파일은 건너뛰므로, 이미지를 교체할 때는 해당 파일을 지우거나 새 파일명으로 추가합니다.

## 문구 수정과 번역
1. `index.src.html`의 한국어 문구를 고칩니다.
2. `python3 tools/build.py` 로 한국어 페이지를 만들고, `python3 i18n/extract.py` 로 `ko.json`을 갱신합니다.
3. 새로 생기거나 바뀐 한국어 문장을 `en.json` · `ja.json`에 같은 키로 추가합니다. HTML 태그는 원문과 똑같이 유지합니다.
4. 다시 `python3 tools/build.py` 를 실행하면 번역되지 않은 문장이 있을 때 목록으로 알려줍니다.

## 구글 애널리틱스 (GA4)
루비컴퍼니 브랜드 사이트(츠바사·바스티온·팔리·크러스트) 공통 코드입니다.

- 측정 ID는 `index.src.html` 맨 위의 `var GA_ID = '';` 한 곳에 넣습니다. 비어 있으면 GA를 불러오지 않습니다. 바꾼 뒤 `python3 tools/build.py`로 세 언어 페이지를 다시 만듭니다.
- 페이지 언어가 콘텐츠 그룹(`content_group`: ko, en, ja)으로 기록됩니다.
- 이벤트
  - `section_view` 섹션 도달 (section_name), 섹션별 1회
  - `consulting_click` 상담 링크(rubiworkshop.com/models) 클릭 (link_location: header, menu, 섹션 id, footer)
  - `dealer_click` 루비서플라이 링크 클릭 (link_location)
  - `language_switch` 언어 전환 (from, to)
  - `social_click` 인스타그램·카카오·유튜브 클릭 (network, link_location)
  - `image_view` 사진 확대 보기 (gallery)
- GA 관리 > 이벤트에서 `consulting_click`을 주요 이벤트로 표시하면 상담 전환을 따로 볼 수 있습니다.

## 운영시간
루비워크샵 쇼룸 운영시간은 모든 브랜드 사이트에서 월~금 12:00~18:00으로 통일합니다.
