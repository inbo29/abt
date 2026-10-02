# 화면 목록

`screens/` 화면 32개입니다. 「이동」은 화면 안의 버튼·링크·표의 행이 여는 화면이고(관리자 화면의 사이드 메뉴와 로그아웃, 가이드 화면의 하단 탭은 모든 화면에 공통이라 뺐습니다), 「저장 데이터」는 브라우저 `localStorage`에서 읽고 쓰는 `abt:` 키입니다. 키 구조는 [data-and-flows.md](data-and-flows.md)에 있습니다.

## 시작·현황

| 파일 | 화면 | 하는 일 | 이동 | 저장 데이터 |
| --- | --- | --- | --- | --- |
| `Login.dc.html` | 로그인 · 2단계 인증 | 이메일·비밀번호 로그인 → 관리자·회계 계정 2단계 인증(6자리 코드). 프로토타입 바로 보기(관리자 웹/가이드 모바일), 다크·라이트 전환, 「예시 데이터로 되돌리기」(저장된 `abt:` 데이터 삭제). | GuideToday, Main | `abt:` 전부 삭제(되돌리기) |
| `Main.dc.html` | 대시보드 · 대표/운영/회계 | 역할별 대시보드 — 「보기 역할」로 대표·운영·회계 첫 화면 전환. 월별 통합 손익, 오늘 운영, 검토 후보, 확인이 필요한 행사, 반복 문제 파트너, 오늘·내일 입출국, 입금 예정·연체, 검토·승인 대기. 「행사 등록」 버튼. | Approvals, Balance, Claims, EventDetail, EventNew, Events, FieldReports, Receipts, Remittance, Reports, Schedule, Settlement | — |
| `Alerts.dc.html` | 알림 | 알림함. 처리 필요·읽지 않음·처리 완료·전체 탭, 처리 완료 표시, 모두 읽음, 각 알림의 원문 화면으로 이동. | Approvals, Claims, EventDetail, FieldReports, Receipts, Remittance, Schedule | — |
| `Reports.dc.html` | 리포트 | 리포트 목록과 미리보기. 예상 포함/확정 금액 구분, 기간 선택, 인쇄용 보기, 엑셀 다운로드. 집계 기준 시각·통화·환율 표시. | EventDetail | — |

## 운영

| 파일 | 화면 | 하는 일 | 이동 | 저장 데이터 |
| --- | --- | --- | --- | --- |
| `Events.dc.html` | 행사 목록 | 행사 목록. 새로 등록한 행사가 맨 위에 「새로 등록」으로, 배정 캘린더의 가배정 상태가 함께 보임. 행을 누르면 행사 상세, 「행사 등록」으로 등록 화면. | EventDetail, EventNew | 읽기 `assign`, `events` |
| `EventNew.dc.html` | 행사 등록 | 행사 등록 폼: 여행사·상품·도착일·인원(여행객+인솔)·담당·판매가·지상비. 저장하면 행사코드(MN+연월-순번)가 붙고 예약 상태로 시작. 저장 뒤 목록 보기·하나 더 등록. | Events, Schedule | 읽기 `events`; 쓰기 `events` |
| `EventDetail.dc.html` | 행사 상세 · MN2609-033(예시) | 행사 한 건의 전체(예시 MN2609-033): 행사 정보 수정, 금액 요약, 먼저 처리할 일, 항목별 예산 대비 실제, 비용 내역, 손익 계산, 정산 확정 전 확인, 클레임 처리 단계, 배정, 입금·송금 요약, 엑셀 다운로드, 정산 확정. | Approvals, Claims, Events, FieldReports, Receipts, Remittance, Schedule | — |
| `Schedule.dc.html` | 배정 캘린더 | 가이드·차량 배정 캘린더(2주·10월·11월). 미배정 행사 → 배정 패널: 가이드는 1명 선택, 차량은 여러 대 선택하고 날짜별 좌석 합계 확인. 가배정·배정·변경, 일정 충돌 자동 표시, 불가일 회색 막대, 되돌리기. 명단은 가이드·차량 화면에서 옴. | EventDetail, Resources | 읽기 `events`, `guideReplies`, `guides`, `offs`, `vehicles`; 쓰기 `assign`, `scheduleOps` |
| `FieldReports.dc.html` | 현장 보고 | 가이드가 낸 현장 보고(일정 체크·변경·옵션·사고·완료)를 운영팀이 확인 완료·보완 요청. 현장 비용은 비용 승인에서 따로 검토. | Approvals, Claims, EventDetail | — |
| `Claims.dc.html` | 클레임 | 클레임 접수와 처리 단계(접수 → 조사 → 조치 → 해결 확인 → 종결), 긴급도, 처리 기한, 업체 책임, 보상 승인 요청. | Approvals, EventDetail, Partners | — |

## 회계와 정산

| 파일 | 화면 | 하는 일 | 이동 | 저장 데이터 |
| --- | --- | --- | --- | --- |
| `Receipts.dc.html` | 입금·미수 | 여행사 청구와 실제 통장 입금을 따로 기록. 입금 1건을 여러 행사의 계약금·잔금에 배분, 청구보다 많이 들어온 돈은 과입으로 잔액 원장에 남김. 미수·연체. | Balance, EventDetail | — |
| `Approvals.dc.html` | 비용 승인 | 현장 비용 승인: 비용 등록 → 운영 확인 → 회계 검토 → 권한자 승인 → 지급·정산 반영(300,000 MNT 미만은 회계 검토로 확정). 검토 후보(중복 청구·단가 차이·증빙 누락), 반려·보완 요청. 「보기 권한」으로 운영·회계·대표 처리 전환. | EventDetail | — |
| `Remittance.dc.html` | 송금 | ABT 한국 → ABT Mongolia LLC 지상비 송금 원장: 송금 요청·검토·승인·송금증 첨부·송금 완료. 내부거래라 통합 매출에서 뺌. 「보기 권한」. | EventDetail | — |
| `Balance.dc.html` | 과입·차감 | 거래처·행사·통화별 잔액 원장(과입, 취소 환불, 보상·단가 차감). 상계·환불 처리, 처리 근거 필수. 잔액 0이면 닫힘. | EventDetail, Receipts | — |
| `Settlement.dc.html` | 정산·마감 | 월 정산·마감: 마감 전에 처리할 항목, 행사별 손익, 마감, 재개방 요청·승인, 마감 이력, 정산서 내려받기. 「보기 권한」. | Approvals, EventDetail, Receipts, Remittance | — |

## 기준정보·관리

| 파일 | 화면 | 하는 일 | 이동 | 저장 데이터 |
| --- | --- | --- | --- | --- |
| `Agencies.dc.html` | 여행사 | 여행사(거래처) 등록·수정: 담당자, 거래 조건, 정산 방식, 조회 계정, 운영 요청사항. 여행사별 행사·매출·미수, 여행사별 매뉴얼, 이 여행사로 행사 등록. | Balance, EventDetail, EventNew, Manuals, Receipts | — |
| `Products.dc.html` | 상품 | 상품 버전 관리: 상품코드, 일정 템플릿, 포함/불포함, 옵션. 새 버전 만들기·초안 삭제·게시(확정된 행사에는 자동 반영 안 됨). | — | — |
| `Partners.dc.html` | 협력업체·요금표 | 협력업체(호텔·캠프·식당·관광지·차량업체)와 시즌별 요금표: 단가·통화·적용 기간, 이용·클레임·검토 후보. | Balance, Claims | — |
| `Resources.dc.html` | 가이드·차량 | 가이드·차량 명단(배정 캘린더의 출처). 가이드 등록, 차량 등록(차종·정원·기사), 가이드 배정 불가일·차량 정비 일정 등록. | Schedule | 읽기 `guides`, `offs`, `vehicles`; 쓰기 `guides`, `offs`, `vehicles` |
| `Manuals.dc.html` | 매뉴얼 | 매뉴얼 목록·상세·작성. 편집기(제목·구분·연결 대상·태그·핵심 주의사항·섹션·사진)와 가이드 앱 미리보기, 개인 정보 확인. 작성 중 → 검토 중 → 게시, 작성자에게 돌려보내기, 새 버전 작성, 가이드 확인 현황·미확인 알림. | — | 읽기 `manuals`; 쓰기 `manuals` |
| `Users.dc.html` | 사용자·권한 | 사용자와 역할별 메뉴 권한(조회·등록·수정·승인·다운로드)·데이터 범위. 사용자 초대, 2단계 인증 초기화, 잠금·해제, 퇴사·계약 종료 처리. | Audit | — |
| `Audit.dc.html` | 감사 로그 | 감사 로그: 금액·승인·마감·권한·로그인·다운로드 기록(변경 전후·사유·승인자). 기간·구분·사용자·검색 필터, 내보내기. 기록은 수정·삭제 불가. | — | — |

## 가이드 모바일

| 파일 | 화면 | 하는 일 | 이동 | 저장 데이터 |
| --- | --- | --- | --- | --- |
| `GuideToday.dc.html` | 가이드 · 오늘 | 가이드 첫 화면: 오늘 행사, 일정 체크(방문 완료), 브리핑 보기, 현장 등록 바로가기(현장 비용·옵션 판매·사고 보고·완료 보고). | GuideBriefing, GuideExpense, GuideIncident, GuideOption, GuideReport | — |
| `GuideBriefing.dc.html` | 가이드 · 브리핑 | 행사 브리핑: 변경 확인, 꼭 지킬 것(고객 특이사항), 오늘 일정별 주의사항, 여행사 요청, 연결된 매뉴얼(「읽었습니다」), 인수인계, 오늘 체크리스트. | GuideReport, GuideToday | 읽기 `manuals`; 쓰기 `manuals` |
| `GuideSchedule.dc.html` | 가이드 · 내 일정 | 내 일정(목록·월): 배정 수락·어려움 전달, 변경 확인, 배정 불가일 등록. 결과는 배정 캘린더와 가이드·차량 화면에 반영. | — | 읽기 `guideReplies`, `offs`; 쓰기 `guideReplies`, `offs` |
| `GuideAdd.dc.html` | 가이드 · 현장 등록 | 현장 등록 메뉴: 현장 비용, 옵션 판매, 사고·클레임 보고, 완료 보고. 임시저장한 건 목록. | GuideExpense, GuideIncident, GuideOption, GuideReport, GuideToday | — |
| `GuideExpense.dc.html` | 가이드 · 현장 비용 | 현장 비용 등록: 금액·통화·사용처·영수증, 임시저장·제출, 내가 등록한 비용과 처리 상태. | GuideAdd | — |
| `GuideOption.dc.html` | 가이드 · 옵션 판매 | 옵션 판매 등록(수량 ±), 오늘 판매 목록, 취소·환불. | GuideAdd | — |
| `GuideIncident.dc.html` | 가이드 · 사고·클레임 보고 | 사고·클레임 보고: 긴급도, 내용, 임시저장·제출. | GuideAdd | — |
| `GuideReport.dc.html` | 가이드 · 완료 보고 | 완료 보고: 출국 뒤 제출, 실제 인원·변경·돈과 증빙 자동 집계, 임시저장·제출, 내 정산으로 이동. | GuideAdd, GuideSettle | — |
| `GuideSettle.dc.html` | 가이드 · 내 정산 | 내 정산(월 선택): 가이드비·수당·옵션 배분·선지급·환급 내역. 회사 마진과 다른 가이드 정보는 보이지 않음. | GuideExpense | — |
| `GuideNotice.dc.html` | 가이드 · 알림 | 가이드 알림: 읽음과 확인을 따로 기록, 확인이 필요한 건은 「확인함」까지 남음, 모두 읽음. | GuideExpense, GuideSchedule | — |

## 공통

- 관리자 화면 22개는 왼쪽 `SideNav`(메뉴·건수·사용자·로그아웃·다크/라이트)를, 가이드 화면 10개는 위쪽 테마 전환과 아래 `MobileTabBar`(오늘·내 일정·현장 등록·내 정산·알림)를 함께 씁니다. 틀은 `tools/screens/gen.py`에 있습니다.
- 다크·라이트 선택은 `localStorage`의 `abt-theme`에 저장되어 화면을 옮겨도 유지됩니다.
- 처리 결과는 화면 위 알림(`Alert`)으로 보여 줍니다. 서버 호출은 없습니다.
