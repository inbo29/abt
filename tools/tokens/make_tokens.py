import json
from palette3 import HEX
D, L = HEX['dark'], HEX['light']
def c(name, usage, alias=None, dark=None, light=None):
    if alias: return {"name": name, "value": "{"+alias+"}", "usage": usage}
    return {"name": name, "value": {"dark": dark or D[name], "light": light or L[name]}, "usage": usage}
colors = [
 c("bg", "앱 바탕: 사이드 메뉴 오른쪽 작업 영역 뒤. 위 글자는 ink, ink-muted."),
 c("surface", "패널·표·카드 바탕. ink, ink-muted와 상태 글자 progress·positive·attention·critical이 모두 4.5:1 이상."),
 c("surface-raised", "떠 있는 레이어(드롭다운, 시트, 대화상자)와 사이드 메뉴 바탕. 위 글자는 ink, ink-muted."),
 c("surface-hover", "표 행·메뉴 항목에 포인터를 올렸을 때."),
 c("surface-sunken", "입력 필드 바탕, 표 머리줄, 행사코드 칩 바탕. 위 글자는 ink, ink-muted."),
 c("surface-selected", "선택된 행, 현재 메뉴, 확정 배정 막대, 무채색 배지 바탕. 선택은 색이 아니라 이 면으로 표시한다. 위 글자는 ink, ink-muted."),
 c("line", "장식용 구분선: 패널 테두리, 표 행 구분. 의미를 싣지 않는다."),
 c("line-strong", "입력·체크박스 테두리, 예상 값의 점선 테두리, 차트 기준선. 모든 surface와 bg에서 3:1 이상."),
 c("ink", "본문, 확정 금액, 이름. bg, 모든 surface, 모든 *-soft 위에서 읽힌다."),
 c("ink-muted", "보조 글자: 라벨, 표 머리글, 통화코드, 시간대, 예상 금액. bg와 모든 surface 위."),
 c("ink-faint", "비활성 글자 전용(대비 기준 면제). 정보를 담은 글자에는 쓰지 않는다."),
 c("action", "주 버튼 채움. 무채색이며 화면당 주 행동 하나에만 쓴다."),
 c("action-hover", "주 버튼 hover·누름 채움."),
 c("on-action", "action·action-hover 채움 위 글자."),
 c("progress", "진행·대기 상태 전용: 요청, 제출, 검토 중, 진행 중, 부분 입금, 조사 중. 글자로 bg, surface, progress-soft 위. 상태가 아닌 곳(버튼, 링크, 선택)에 쓰지 않는다."),
 c("progress-soft", "진행 상태 배지·알림 바탕. 위 글자는 progress 또는 ink."),
 c("on-progress", "progress 채움(진행 중 행사 배지) 위 글자."),
 c("positive", "정상·확정 상태 전용: 승인, 입금 완료, 송금 완료, 정산 확정, 가이드 확인, 해결. 글자로 bg, surface, positive-soft 위."),
 c("positive-soft", "정상 상태 배지·알림 바탕. 위 글자는 positive 또는 ink."),
 c("attention", "주의 상태 전용: 예산 초과, 증빙 누락, 단가 차이, 중복 청구 후보, 마진 하락, 기한 임박, 재개방, 미배정. 판정이 아니라 검토 후보. 글자로 bg, surface, attention-soft 위."),
 c("attention-soft", "주의 배지·알림·KPI 바탕. 위 글자는 attention 또는 ink."),
 c("critical", "위험 상태 전용: 적자, 연체, 반려, 사고, 처리 기한 초과, 일정 충돌. 글자로 bg, surface, critical-soft 위. 반려·삭제 버튼의 채움."),
 c("critical-soft", "위험 배지·알림·KPI 바탕. 위 글자는 critical 또는 ink."),
 c("on-critical", "critical 채움(반려 버튼, 긴급 배지) 위 글자."),
 c("chart-actual", "차트의 실제 값 막대·선(무채색). 기준을 넘은 부분만 attention·critical로 칠한다. surface와 bg에서 3:1 이상."),
 c("chart-expected", "차트의 예상·예산 값. line-strong의 별칭이며 점선 테두리로만 그린다.", alias="line-strong"),
 c("chart-grid", "차트 격자선과 축. line의 별칭이며 실선 1px만 쓴다(점선은 예상 전용).", alias="line"),
 c("focus", "키보드 포커스 링 색. ink의 별칭. focus-ring 그림자와 같은 색.", alias="ink"),
 {"name": "scrim", "value": {"dark": "rgba(5, 8, 10, 0.64)", "light": "rgba(19, 26, 31, 0.40)"}, "usage": "시트·대화상자 뒤를 덮는 막."},
]
tokens = {
 "name": "ABT Ops",
 "version": 1,
 "color": {"themes": [{"id": "dark", "name": "다크"}, {"id": "light", "name": "라이트"}], "tokens": colors},
 "type": {
  "fonts": [],
  "families": {
   "sans": "\"IBM Plex Sans\", \"IBM Plex Sans KR\", \"Apple SD Gothic Neo\", \"Malgun Gothic\", system-ui, sans-serif",
   "mono": "\"IBM Plex Mono\", ui-monospace, \"SF Mono\", Menlo, monospace"
  },
  "groups": [
   {"name": "관리자 웹", "family": "sans", "note": "PC 기준. 숫자가 세로로 줄 서는 곳(표, 축)은 tabular-nums, 혼자 크게 서는 숫자(KPI)는 비례 숫자.", "styles": [
     {"name": "title-1", "fontSize": "22px", "lineHeight": "30px", "fontWeight": 600, "letterSpacing": "-0.01em", "sample": "10월 행사 손익", "usage": "화면 제목. 화면당 하나."},
     {"name": "title-2", "fontSize": "17px", "lineHeight": "24px", "fontWeight": 600, "sample": "지상비 예산 대비 실제", "usage": "패널 제목."},
     {"name": "title-3", "fontSize": "15px", "lineHeight": "22px", "fontWeight": 600, "sample": "송금 요청 2건", "usage": "패널 안 소제목, 시트의 구획 제목."},
     {"name": "body", "fontSize": "14px", "lineHeight": "22px", "fontWeight": 400, "sample": "현장 비용은 회계 승인 후 정산에 반영됩니다.", "usage": "기본 글자."},
     {"name": "body-strong", "fontSize": "14px", "lineHeight": "22px", "fontWeight": 600, "sample": "승인 대기 7건", "usage": "강조할 문장, 사람·업체 이름."},
     {"name": "cell", "fontSize": "13px", "lineHeight": "20px", "fontWeight": 400, "sample": "고비 사막 5박 6일 · 18+1명", "usage": "표 칸. 금액·수량 열은 tabular-nums."},
     {"name": "label", "fontSize": "12px", "lineHeight": "16px", "fontWeight": 500, "sample": "여행사", "usage": "입력 라벨, 표 머리글, KPI 라벨. ink-muted."},
     {"name": "caption", "fontSize": "12px", "lineHeight": "18px", "fontWeight": 400, "sample": "10.01 09:00 KST 기준 · KRW 환산", "usage": "도움말, 집계 기준, 환율 근거 같은 메타 정보."},
     {"name": "kpi", "fontSize": "26px", "lineHeight": "32px", "fontWeight": 600, "letterSpacing": "-0.01em", "sample": "4,820만", "usage": "KPI 값. 비례 숫자."}
   ]},
   {"name": "가이드 모바일", "family": "sans", "note": "390px 폭 기준. 본문 16px 이상, 터치 영역 44px 이상.", "styles": [
     {"name": "m-title", "fontSize": "20px", "lineHeight": "28px", "fontWeight": 700, "sample": "오늘의 행사", "usage": "모바일 화면 제목."},
     {"name": "m-body", "fontSize": "16px", "lineHeight": "24px", "fontWeight": 400, "sample": "픽업 07:30 · 칭기즈칸 호텔 로비", "usage": "모바일 본문."},
     {"name": "m-label", "fontSize": "14px", "lineHeight": "20px", "fontWeight": 500, "sample": "사용처", "usage": "모바일 입력 라벨, 목록 보조 줄."},
     {"name": "m-caption", "fontSize": "13px", "lineHeight": "18px", "fontWeight": 400, "sample": "임시저장 10.01 14:30 ULAT", "usage": "모바일 메타 정보."}
   ]},
   {"name": "식별자", "family": "mono", "styles": [
     {"name": "code", "fontSize": "13px", "lineHeight": "18px", "fontWeight": 500, "sample": "MN2610-014", "usage": "행사코드, 송금번호 같은 식별자 전용. 일반 라벨에 쓰지 않는다."}
   ]}
  ]
 },
 "spacing": {"note": "4px 단위. 관리자 웹은 촘촘하게, 가이드 모바일은 터치 영역 우선.", "tokens": [
  {"name": "space-1", "value": "4px", "usage": "배지 안쪽 세로, 금액과 통화코드 사이."},
  {"name": "space-2", "value": "8px", "usage": "컨트롤 안쪽, 나란한 버튼 사이."},
  {"name": "space-3", "value": "12px", "usage": "표 칸 좌우 안쪽, 필드 사이."},
  {"name": "space-4", "value": "16px", "usage": "패널 안쪽 여백, 모바일 화면 좌우 여백."},
  {"name": "space-5", "value": "20px", "usage": "패널 머리와 본문 사이."},
  {"name": "space-6", "value": "24px", "usage": "패널 사이, 작업 영역 좌우 여백."},
  {"name": "space-8", "value": "32px", "usage": "화면 머리와 본문 사이."},
  {"name": "space-10", "value": "40px", "usage": "큰 구획 사이."},
  {"name": "space-12", "value": "48px", "usage": "빈 상태 위아래."}
 ]},
 "radius": {"note": "작고 단정하게. 계층마다 다르다.", "tokens": [
  {"name": "radius-sm", "value": "4px", "usage": "버튼, 입력, 배지, 행사코드 칩."},
  {"name": "radius-md", "value": "6px", "usage": "패널, 표 테두리, 드롭다운."},
  {"name": "radius-lg", "value": "12px", "usage": "모바일 카드와 시트."},
  {"name": "radius-full", "value": "9999px", "usage": "개수 표시, 승인 단계 점."}
 ]},
 "shadow": {"note": "다크에서는 테두리로 구분하고 그림자는 떠 있는 레이어에만.", "tokens": [
  {"name": "shadow-sm", "value": {"dark": "0 1px 0 #0000004d", "light": "0 1px 2px #131a1f0f, 0 1px 3px #131a1f14"}, "usage": "패널 아래 경계. 라이트에서만 보인다."},
  {"name": "shadow-lg", "value": {"dark": "0 16px 40px -8px #000000b3, 0 0 0 1px #2e353b", "light": "0 12px 32px -6px #131a1f2e, 0 2px 6px #131a1f14"}, "usage": "떠 있는 레이어: 드롭다운, 시트, 대화상자."},
  {"name": "focus-ring", "value": {"dark": "0 0 0 2px #12181c, 0 0 0 4px #e9edf0", "light": "0 0 0 2px #ffffff, 0 0 0 4px #131a1f"}, "usage": "키보드 포커스: 바탕색 2px 틈 다음 ink 2px 실선. box-shadow라 모서리를 따른다."}
 ]},
 "size": {"note": "컨트롤과 레이아웃의 고정 치수.", "tokens": [
  {"name": "control-sm", "value": "28px", "usage": "필터 줄처럼 좁은 곳의 버튼·입력 높이."},
  {"name": "control-md", "value": "34px", "usage": "관리자 웹 기본 버튼·입력 높이."},
  {"name": "control-lg", "value": "48px", "usage": "가이드 모바일 버튼·입력 높이(터치 44px 이상)."},
  {"name": "row-compact", "value": "32px", "usage": "촘촘한 표 행: 원장, 감사 로그."},
  {"name": "row-regular", "value": "40px", "usage": "기본 표 행."},
  {"name": "sidebar-width", "value": "232px", "usage": "사이드 메뉴 폭."},
  {"name": "tabbar-height", "value": "64px", "usage": "모바일 하단 탭 높이."}
 ]}
}
import os
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
out = os.path.join(ROOT, 'design-system', 'tokens.json')
json.dump(tokens, open(out, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=2)
# tokens.css for the screens (screens/ds/abt/tokens.css)
def css():
    out=[]
    first, second = 'dark','light'
    def val(t, theme):
        v=t['value']
        if isinstance(v,str):
            if v.startswith('{'): return f"var(--{v[1:-1]})"
            return v
        return v.get(theme) or v.get(first)
    root=[f"  --{t['name']}: {val(t,first)};" for t in colors]
    root+= [f"  --{t['name']}: {val(t,first)};" for t in tokens['shadow']['tokens']]
    out.append(':root, [data-theme="dark"] {\n'+'\n'.join(root)+'\n}')
    lt=[f"  --{t['name']}: {val(t,second)};" for t in colors if not (isinstance(t['value'],str))]
    lt+=[f"  --{t['name']}: {val(t,second)};" for t in tokens['shadow']['tokens']]
    lt+=[f"  --{t['name']}: {val(t,second)};" for t in colors if isinstance(t['value'],str)]
    out.append('[data-theme="light"] {\n'+'\n'.join(lt)+'\n}')
    r=[]
    for fam in ['spacing','radius','size']:
        r+=[f"  --{t['name']}: {t['value']};" for t in tokens[fam]['tokens']]
    for k,v in tokens['type']['families'].items(): r.append(f"  --font-{k}: {v};")
    out.append(':root {\n'+'\n'.join(r)+'\n}')
    for g in tokens['type']['groups']:
        fam=g['family']
        for s in g['styles']:
            decl=[f"font-family: var(--font-{s.get('family',fam)})", f"font-size: {s['fontSize']}", f"line-height: {s['lineHeight']}", f"font-weight: {s['fontWeight']}"]
            if 'letterSpacing' in s: decl.append(f"letter-spacing: {s['letterSpacing']}")
            out.append(f".{s['name']} {{ {'; '.join(decl)}; }}")
    return '\n'.join(out)+'\n'
open(os.path.join(ROOT, 'screens', 'ds', 'abt', 'tokens.css'), 'w', encoding='utf-8', newline='\n').write(css())
print('ok', len(colors), 'colors')
