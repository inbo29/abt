# KpiTile

대시보드의 핵심 수치 하나를 보여주고, 기준을 넘으면 타일 전체를 주의·위험 색으로 바꾸며, 원장으로 가는 링크를 단다.

- **label**(문장형, 콜론 없이), **value**+**unit** 또는 **money** `{amount, currency}`(원화는 "4,820만"으로 줄여 쓴다).
- **delta** `{value, unit, period, good}`: 지난 기간 대비 증감. `good`은 늘어나는 게 좋은지(`up`) 줄어드는 게 좋은지(`down`)다. 나쁜 방향일 때만 `attention` 글자로 표시하고, 좋은 방향은 무채색으로 둔다.
- **state**: `attention` · `critical`. 관리자가 정한 경고 기준을 넘었을 때만 켠다. **stateLabel**에 이유를 짧게 쓴다("기한 임박 3건").
- **caption**: 집계 기준("10.01 09:00 KST 기준 · KRW 환산"). **href**+**linkLabel**: "원장 보기", "행사 보기".
- 한 화면의 KPI는 4~6개로 줄인다. 아이콘이나 장식 그래프를 넣지 않는다.
