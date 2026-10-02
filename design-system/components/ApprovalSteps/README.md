# ApprovalSteps

비용 승인이나 송금처럼 단계가 있는 처리의 진행 위치와 처리자, 시각을 한 줄(또는 세로)로 보여준다.

- **steps**: `{label, state, actor, at, note}`. state는 `done`(초록 점, 실선 연결) · `current`(파란 고리) · `pending`(점선 고리, 점선 연결) · `rejected`(빨간 점, 반려 사유를 note에) · `skipped`.
- **orientation**: `horizontal`(기본, 상세 화면 머리) · `vertical`(시트, 모바일).
- 단계 이름은 업무 문서와 같은 말로 쓴다: 비용 등록 → 운영 확인 → 회계 검토 → 권한자 승인 → 지급·정산 반영.
