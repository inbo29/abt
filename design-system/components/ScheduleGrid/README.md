# ScheduleGrid

가이드·차량·기사별 배정을 날짜 칸 위의 막대로 보여주는 배정 캘린더이며, 같은 줄에서 겹치는 일정은 자동으로 "충돌"로 표시한다.

- **days**: `{label, dow, weekend, today}` 배열. **rows**: `{id, name, meta, items}`; item은 `{start, span, label, state, href}`(start는 days의 순번).
- state: `confirmed`(실선, 무채색) · `tentative`(가배정, 점선) · `changed`(가이드 확인 전 변경, `attention`) · `conflict`(`critical`) · `off`(휴무·배정 불가, 빗금).
- **prefix**(선택): 막대 앞 굵은 단어를 바꾼다. 정원 초과처럼 겹침이 아닌 문제는 `state: "conflict", prefix: "정원 초과"`로 쓴다.
- **detectConflicts**(기본 켬): 같은 줄에서 기간이 겹치면 둘 다 충돌로 칠한다. 휴무일과 겹친 배정도 충돌이다.
- **cellWidth**: 월 보기 36~44px, 2주 보기 52px 이상. **rowLabel**: "가이드", "차량", "기사".
