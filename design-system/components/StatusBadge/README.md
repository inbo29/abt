# StatusBadge

행사, 비용, 송금, 입금, 정산, 배정, 클레임, 검토 후보의 상태를 정해진 단어 하나로 보여준다.

- **axis** + **status**를 넘기면 단어와 색이 정해진다: `<StatusBadge axis="remit" status="approved"/>` → 점선 "승인".
- axis: `event` · `cost` · `remit` · `payment` · `settle` · `assign` · `claim` · `report` · `risk`. 각 상태 키는 `Abt.STATUS`에 있다.
- 형태: 점선은 아직 실제가 아닌 상태(예약, 요청, 승인 후 미송금), 실선은 확정·결과, 채움은 지금 움직여야 하는 상태(진행 중 행사, 긴급 클레임)다.
- 표에 없는 상태가 꼭 필요하면 `tone`(neutral·progress·positive·attention·critical), `form`, children으로 만들되, 먼저 이 표에 추가할지 정한다.
- 아이콘을 붙이지 않는다. 단어가 상태를 전하고, 색은 그 단어를 빨리 찾게 돕는다.
