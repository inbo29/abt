# Tabs

행사 상세처럼 한 대상의 여러 면(개요, 일정, 배정, 비용, 입금, 송금, 정산, 클레임, 변경 이력)을 바꿔 보는 밑줄 탭이다.

- **items**: `{id, label, count, tone, href}`. count에 tone(`attention`, `critical`)을 주면 처리할 건수가 상태색으로 보인다.
- **value**, **onChange**로 제어하거나 비워 두면 스스로 상태를 갖는다. 화면을 옮기는 탭은 `href`를 쓴다.
- **ariaLabel**(마크업에서는 `aria-label`): 탭 묶음이 무엇을 나누는지. 예: "행사 상세 구분".
- 탭 이름은 명사 하나로 짧게 쓴다.
