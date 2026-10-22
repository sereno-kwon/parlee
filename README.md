# Parlee Cycles Korea

parleecycles.co.kr 원페이지 정적 사이트 (GitHub Pages). tsubasabicycles.co.kr, bastioncycles.co.kr과 같은 구조입니다.

- `index.html` 원페이지 본체 (PARLEE · OURAY · TAOS · Z-ZERO GT · BESPOKE · PAINT LAB · HISTORY · SHOWROOM)
- `index.src.html` 편집용 원본. 지오메트리 표는 `{{GEO_*}}` 자리에 빌드 시 채워집니다. 표를 고치지 않을 때는 `index.html`을 직접 수정해도 됩니다.
- `404.html` 하위 주소(/ouray, /taos, /z-zero-gt 등)를 섹션으로 연결
- `images/` 섹션별 이미지 (`hero`, `brand`, `ouray`, `taos`, `gt`, `anniversary`, `bespoke`, `process`, `team`, `paint`, `history`)
- `.github/image-manifest.txt` + `fetch-images.yml` 팔리 공식 사이트(parleecycles.com) CDN 이미지 이전용 워크플로

## 이미지
매니페스트를 수정해 main에 푸시하면 Actions가 이미지를 받아 `images/`에 커밋합니다.
이미 받은 파일은 건너뛰므로, 이미지를 교체할 때는 해당 파일을 지우거나 새 파일명으로 추가합니다.
