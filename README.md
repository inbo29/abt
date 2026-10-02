# ABT Ops 프로토타입

ABT 한국·몽골 여행 운영·정산 통합 관리 시스템의 화면 프로토타입과 디자인 시스템입니다. 관리자 웹 22개 화면(대표·운영·회계, 1440px)과 가이드 모바일 웹 10개 화면(390×844)으로 되어 있습니다.

이 저장소의 파일은 Claude 디자인 캔버스에 게시된 원본과 바이트 단위로 같습니다(2026-10-02 기준). `tools/`의 스크립트로 다시 만들어도 같은 파일이 나옵니다. 모든 이름·금액·날짜는 예시 데이터입니다.

## 폴더 구조

```
.
├── screens/                화면 32개 (캔버스 원본 그대로)
│   ├── *.dc.html           화면 파일 — 마크업과 화면 로직이 한 파일에
│   ├── canvas.json         캔버스 배치: 보드 위치·크기·제목·메모·순서
│   └── ds/abt/             화면이 불러오는 디자인 시스템 사본(tokens.css, bundle.js, bundle.css, tokens.json)
├── design-system/          디자인 시스템 "ABT Ops" (원본 그대로)
│   ├── README.md           브랜드북: 원칙, 글쓰기, 상태 단어, 색, 글꼴, 간격, 아이콘
│   ├── tokens.json         디자인 토큰(다크·라이트)
│   ├── design-system.json  디자인 시스템 목록 정보
│   └── components/
│       ├── src/            컴포넌트 소스(React 18, TSX) — index.tsx, icons.ts
│       ├── bundle.js       빌드 결과: window.Abt 에 컴포넌트 22개
│       ├── bundle.css      컴포넌트 스타일(직접 관리하는 소스)
│       ├── index.d.ts      컴포넌트 props 타입
│       └── <컴포넌트>/     README.md(쓰는 법), preview.html(미리보기)
├── tools/                  다시 만드는 스크립트
│   ├── build-all.sh        토큰 → 컴포넌트 번들 → 화면 순서로 전부 다시 생성
│   ├── package.json        빌드 도구 esbuild 0.24.2 (package-lock.json으로 버전 고정)
│   ├── tokens/             make_tokens.py (색은 palette3.py의 OKLCH 값에서 계산)
│   ├── design-system/      build.sh (esbuild로 bundle.js, screens/ds/abt 사본 갱신)
│   └── screens/            gen.py(공통 틀) + batch*.py(화면별 소스) + generate.sh
└── docs/
    ├── screens.md          화면 32개 목록: 하는 일, 이동, 저장 데이터
    └── data-and-flows.md   프로토타입 데이터 구조, 화면 간 연결, 업무 규칙
```

## 화면 구성

| 영역 | 화면 |
| --- | --- |
| 시작·현황 | 로그인·2단계 인증, 대시보드(대표/운영/회계), 알림, 리포트 |
| 운영 | 행사 목록, 행사 등록, 행사 상세(예시 MN2609-033), 배정 캘린더, 현장 보고, 클레임 |
| 회계와 정산 | 입금·미수, 비용 승인, 송금, 과입·차감, 정산·마감 |
| 기준정보·관리 | 여행사, 상품, 협력업체·요금표, 가이드·차량, 매뉴얼, 사용자·권한, 감사 로그 |
| 가이드 모바일 | 오늘, 브리핑, 내 일정, 현장 등록, 현장 비용, 옵션 판매, 사고·클레임 보고, 완료 보고, 내 정산, 알림 |

화면별 설명은 [docs/screens.md](docs/screens.md), 데이터와 화면 간 연결은 [docs/data-and-flows.md](docs/data-and-flows.md)에 있습니다.

## 화면 파일(`.dc.html`) 읽는 법

Claude 디자인 캔버스 형식입니다. 한 파일에 두 부분이 있습니다.

- **템플릿** `<x-dc> … </x-dc>`: HTML에 `{{값}}` 자리를 둡니다. `<sc-for list="{{rows}}" as="r">`는 반복, `<sc-if value="{{cond}}">`는 조건부 표시입니다. `<x-import component-from-global-scope="Abt.DataTable" columns="{{cols}}" on-row-click="{{pick}}">`는 디자인 시스템 컴포넌트이고, 케밥 표기 속성이 카멜 표기 props(`onRowClick`)로 넘어갑니다.
- **로직** `<script type="text/x-dc" data-dc-script>`: `class Component extends DCLogic`. `this.state`가 화면 상태이고, `renderVals()`가 템플릿의 `{{값}}`을 모두 돌려줍니다. 버튼 동작도 여기 있는 함수입니다. `data-props`에는 테마 속성과 미리보기 크기(`$preview`)가 있습니다.

화면 파일 첫머리의 `./support.js`는 캔버스 런타임으로, 캔버스가 제공하며 `screens/`에는 없습니다. 그래서 `screens/`의 파일을 브라우저에서 바로 열면 화면이 그려지지 않습니다. 캔버스 밖에서 보려면 아래 「미리보기 사이트」를 씁니다.

## 미리보기 사이트

`tools/site/`가 디자인 시스템 문서(브랜드북·토큰·컴포넌트 미리보기)와 동작하는 화면 32개를 정적 사이트 `_site/`로 만듭니다. `screens/`와 `design-system/`의 파일은 그대로 복사하고, 캔버스가 하던 일만 대신합니다.

- `tools/site/support.js`: 캔버스 런타임 대체. `<x-dc>` 템플릿을 React 18로 그립니다(`{{}}` 바인딩, `sc-for`, `sc-if`, `x-import`, `DCLogic`, `<helmet>`). 가이드 모바일 화면은 390px 폭으로 가운데에 놓습니다.
- 컴포넌트 `preview.html`에는 캔버스가 넣어 주던 `tokens.css`·`bundle.css`·React·`bundle.js`를 `<head>`에 넣어 복사합니다.
- React 18 UMD는 `tools/node_modules`에서 복사합니다(외부 CDN 없음).
- 사이트 첫 화면은 `screens/Login.dc.html`이고, 디자인 시스템 문서는 `guide.html`에 있습니다. 기본 테마는 라이트입니다(`support.js`의 `SITE_DEFAULTS`).
- 버튼을 누른 결과 알림(공통 `hasNotice`, 리포트 `exported`)은 본문에 끼우지 않고 토스트로 띄워 6초 뒤 닫습니다(`support.js`의 `TOASTS`). 리스크·증빙 누락처럼 데이터 상태를 알리는 알림은 본문에 그대로 둡니다.

```bash
cd tools && npm ci && cd ..
node tools/site/build.mjs --serve   # _site/ 생성 후 http://localhost:4173
```

GitHub Pages: `.github/workflows/pages.yml`이 `main`에 push할 때마다 `_site/`를 만들어 배포합니다. 저장소 Settings › Pages › Source를 「GitHub Actions」로 한 번 바꿔 두어야 합니다.

## 디자인 시스템

- 컴포넌트 22개: Icon, Button, StatusBadge, Money, EventCode, DateTime, KpiTile, DataTable, BudgetBar, ApprovalSteps, AuditLog, Alert, ScheduleGrid, Tabs, Segmented, TextField, Select, MoneyField, Checkbox, Attachment, SideNav, MobileTabBar.
- `bundle.js`는 React 18을 `window.React`에서 가져오는 스크립트 하나이고 `window.Abt`에 컴포넌트를 둡니다. 불러오는 순서: Google Fonts → `tokens.css` → `bundle.css` → React 18 → ReactDOM 18 → `bundle.js`.
- 색은 상태(진행·정상·주의·위험) 전용이고, 점선은 예상·미확정, 실선은 확정입니다. 상태 단어 표와 글쓰기 규칙은 [design-system/README.md](design-system/README.md)에 있습니다.
- 다크가 기본이고 라이트는 상위 요소의 `data-theme="light"`로 바꿉니다.

## 다시 만들기

필요한 것: Python 3.9 이상, Node.js 18 이상(npm). Windows에서는 WSL(권장)이나 Git Bash에서 `.sh`를 실행합니다.

```bash
cd tools && npm ci && cd ..     # esbuild 0.24.2 설치 (package-lock.json에 고정)
bash tools/build-all.sh         # 토큰 → 컴포넌트 번들 → 화면 32개
git status                      # 아무것도 안 바뀌었으면 정상
```

하나씩 돌릴 때:

| 무엇을 고칠 때 | 고칠 파일 | 실행 |
| --- | --- | --- |
| 색·간격·글꼴 토큰 | `tools/tokens/palette3.py`(색 값), `tools/tokens/make_tokens.py`(토큰 목록·용도) | `python3 tools/tokens/make_tokens.py` |
| 컴포넌트 | `design-system/components/src/index.tsx`, `icons.ts`, `bundle.css` | `bash tools/design-system/build.sh` |
| 화면 | `tools/screens/batch*.py`(아래 표), 공통 틀은 `gen.py` | `bash tools/screens/generate.sh` |

`screens/*.dc.html`과 `bundle.js`, `tokens.json`, `tokens.css`는 생성 결과입니다. 직접 고치면 다음 생성 때 덮어써지므로 소스를 고친 뒤 다시 만듭니다.

| 스크립트 | 만드는 화면 |
| --- | --- |
| `batch1.py` | Login, Main, Alerts, Reports |
| `batch2a.py` | EventNew |
| `batch2b.py` | EventDetail |
| `batch2c.py` | Schedule |
| `batch2d.py` | FieldReports, Claims |
| `batch2e.py` | Events |
| `batch3a.py` | Receipts, Balance |
| `batch3b.py` | Remittance, Settlement |
| `batch3c.py` | Approvals |
| `batch4a.py` | Agencies, Products, Partners |
| `batch4b.py` | Resources, Manuals, Users, Audit |
| `batch5.py` | 가이드 모바일 10개 |

`gen.py`에는 모든 화면이 함께 쓰는 틀이 있습니다: 사이드 메뉴, 모바일 상단·하단 탭, 다크·라이트 전환, 알림 표시, 브라우저 저장소 도우미. `shared_data.py`에는 여러 화면이 함께 쓰는 예시 매뉴얼 데이터가 있습니다.

## 프로토타입의 한계

- 서버가 없습니다. 등록·배정·작성한 내용은 브라우저 `localStorage`(`abt:` 키)에만 저장되고 다른 사람·기기와 공유되지 않습니다. 로그인 화면의 「예시 데이터로 되돌리기」로 지웁니다.
- 행사 상세는 예시 행사(MN2609-033) 한 건만 있습니다. 목록의 어떤 행사를 눌러도 이 화면이 열립니다.
- 권한은 화면 위 「보기 권한」으로 바꿔 보는 시연용입니다. 실제 인증·권한 검사는 없습니다.

## 서드파티

- 아이콘: [Lucide](https://lucide.dev) 일부(ISC License) — `design-system/components/src/icons.ts`
- 글꼴: IBM Plex Sans, IBM Plex Sans KR, IBM Plex Mono(SIL Open Font License 1.1), Google Fonts에서 불러옴
- 빌드: esbuild(MIT), 개발 의존성
