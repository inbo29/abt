# DataTable

행사 목록, 원장, 정산표처럼 촘촘한 표를 열 정의(columns)와 행 데이터(rows)만으로 그린다.

- **columns**: `{key, label, type, align, width, wrap, sortable}`. type이 칸을 그린다:
  `code`(EventCode, 행의 `href`), `money`(Money, 열의 `currency`·`kind`·`lossTone`), `number`(`suffix`), `percent`, `status`(열의 `axis`), `flags`(검토 후보 배지 목록), `datetime`(열의 `zone`), `budget`(`{budget, actual}` → 작은 BudgetBar), `stack`(`{primary, secondary}` 두 줄), `strong`, `muted`.
- **rows**: 각 행에 `id`와 열 key의 값. `selected`, `dim`(취소된 행)을 줄 수 있다. 값이 없으면 "—"로 보인다.
- 행에 **href**를 주면 행 어디를 눌러도 그 화면으로 간다(행 안의 링크·버튼·입력은 제 동작을 한다). `onRowClick`을 주면 그쪽이 우선한다.
- **totals**: 합계 행(첫 칸은 `label`). **density**: `regular`(40px) · `compact`(32px, 원장·감사 로그).
- **selectable**은 앞에 체크박스 열을 단다. **sort** `{key, dir}`와 **onSort**로 정렬 표시를 한다.
- 금액 열은 오른쪽 정렬과 `tabular-nums`가 자동이다. 칸 글자는 한 줄로 쓰고 길면 `wrap`을 켠다.
- 차트 옆에는 같은 값의 DataTable을 둔다.
