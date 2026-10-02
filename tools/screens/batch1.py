import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import *

T = os.path.dirname(os.path.abspath(__file__)) + '/'
ceo_body = open(T + '_ceo_body.html', encoding='utf-8').read()
# links that used to be empty now go to real screens
ceo_body = ceo_body.replace('state="attention" state-label="기한 임박 2건" href="#" link-label="입금 원장"', 'state="attention" state-label="기한 임박 2건" href="Receipts.dc.html" link-label="입금 원장"')
ceo_body = ceo_body.replace('caption="보상 예정 320,000 MNT" href="#" link-label="클레임 보기"', 'caption="보상 예정 320,000 MNT" href="Claims.dc.html" link-label="클레임 보기"')

# ------------------------------------------------------------------ Main (role-based first screens)
main_body = header('{{title}}', '{{caption}}', '''<span class="label" style="color: var(--ink-muted)">보기 역할</span>
<x-import component-from-global-scope="Abt.Segmented" options="{{roles}}" value="{{role}}" on-change="{{setRole}}" aria-label="보기 역할"></x-import>
<x-import component-from-global-scope="Abt.Button" variant="secondary" href="Reports.dc.html">리포트</x-import>
<x-import component-from-global-scope="Abt.Button" variant="primary" href="EventNew.dc.html">행사 등록</x-import>''') + '''
<sc-if value="{{isCeo}}" hint-placeholder-val="{{true}}">
''' + ceo_body + '''
</sc-if>

<sc-if value="{{isOps}}" hint-placeholder-val="{{false}}">
<section aria-label="오늘 운영 지표" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(170px, 100%), 1fr)); gap: 12px">
<x-import component-from-global-scope="Abt.KpiTile" label="진행 중 행사" value="2" unit="건" caption="MN2609-038 · MN2609-040" href="Events.dc.html" link-label="행사 보기"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="오늘 출국" value="1" unit="건" caption="OM302 21:40 · 14+1명" href="#arrivals" link-label="입출국 보기"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="내일 입국" value="1" unit="건" caption="OM301 10:20 · 18+1명" href="#arrivals" link-label="입출국 보기"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="미배정" value="2" unit="건" state="attention" state-label="D-3 1건" href="Schedule.dc.html" link-label="배정하기"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="일정 충돌" value="1" unit="건" state="critical" state-label="10.03" href="Schedule.dc.html" link-label="배정 변경"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="현장 보고 검토" value="2" unit="건" caption="완료 보고 1 · 일정 변경 1" href="FieldReports.dc.html" link-label="보고 보기"></x-import>
</section>
<div style="display: grid; grid-template-columns: minmax(0, 1.55fr) minmax(0, 1fr); gap: 16px; align-items: start">
<section id="arrivals" style="display: flex; flex-direction: column; gap: 12px">
''' + panel_title('오늘·내일 입출국', '항공 시각은 현지(ULAT) · 행을 누르면 행사 상세') + '''<x-import component-from-global-scope="Abt.DataTable" columns="{{flightCols}}" rows="{{flightRows}}" caption="오늘·내일 입출국"></x-import>
</section>
''' + PANEL + panel_title('처리할 운영 건') + '''<sc-for list="{{opsTodo}}" as="t" hint-placeholder-count="5">
<a href="{{t.href}}" style="display: grid; grid-template-columns: 112px minmax(0, 1fr); gap: 12px; align-items: center; padding: 10px 0; border-top: 1px solid var(--line); text-decoration: none; color: var(--ink)">
<x-import component-from-global-scope="Abt.StatusBadge" axis="{{t.axis}}" status="{{t.status}}"></x-import>
<span style="display: flex; flex-direction: column; gap: 2px; min-width: 0">
<span class="body-strong" style="font-size: 13px; line-height: 20px">{{t.title}}</span>
<span class="caption" style="color: var(--ink-muted)">{{t.meta}}</span>
</span>
</a>
</sc-for>
</section>
</div>
</sc-if>

<sc-if value="{{isAcc}}" hint-placeholder-val="{{false}}">
<section aria-label="회계 지표" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(170px, 100%), 1fr)); gap: 12px">
<x-import component-from-global-scope="Abt.KpiTile" label="미수금" money="{{accReceivable}}" state="attention" state-label="기한 임박 2건" href="Receipts.dc.html" link-label="입금 원장"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="연체" money="{{accOverdue}}" state="critical" state-label="1건" caption="다온여행사 · 09.30 기한" href="Receipts.dc.html" link-label="입금 원장"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="비용 검토 대기" value="5" unit="건" state="attention" state-label="검토 후보 3" caption="9,255,000 MNT" href="Approvals.dc.html" link-label="비용 승인"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="송금 대기" value="3" unit="건" caption="요청 2 · 승인 후 미송금 1" href="Remittance.dc.html" link-label="송금"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="과입 잔액" money="{{accOverpaid}}" caption="상계 대기 1건" href="Balance.dc.html" link-label="과입·차감"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="9월 마감" value="D-4" caption="처리할 항목 4건" href="Settlement.dc.html" link-label="정산·마감"></x-import>
</section>
<div style="display: grid; grid-template-columns: minmax(0, 1.55fr) minmax(0, 1fr); gap: 16px; align-items: start">
<section style="display: flex; flex-direction: column; gap: 12px">
''' + panel_title('입금 예정·연체', '판매·청구 금액과 실제 받은 돈을 따로 봅니다') + '''<x-import component-from-global-scope="Abt.DataTable" columns="{{dueCols}}" rows="{{dueRows}}" totals="{{dueTotals}}" caption="입금 예정과 연체"></x-import>
</section>
''' + PANEL + panel_title('검토·승인 대기') + '''<sc-for list="{{accTodo}}" as="t" hint-placeholder-count="5">
<a href="{{t.href}}" style="display: grid; grid-template-columns: 112px minmax(0, 1fr); gap: 12px; align-items: center; padding: 10px 0; border-top: 1px solid var(--line); text-decoration: none; color: var(--ink)">
<x-import component-from-global-scope="Abt.StatusBadge" axis="{{t.axis}}" status="{{t.status}}"></x-import>
<span style="display: flex; flex-direction: column; gap: 2px; min-width: 0">
<span class="body-strong" style="font-size: 13px; line-height: 20px">{{t.title}}</span>
<span class="caption" style="color: var(--ink-muted)">{{t.meta}}</span>
</span>
</a>
</sc-for>
</section>
</div>
</sc-if>
'''

ceo_js = open(T + '_ceo_js.txt', encoding='utf-8').read()
# take the CEO data object literal (everything inside "return { ... };") and fold it into our vals
ret = ceo_js.split('return {', 1)[1].rsplit('};', 1)[0]
pre_ceo = ceo_js.split('return {', 1)[0]
pre_ceo = pre_ceo.replace("const view = this.state.chartView;", "const view = s.chartView;")
pre_ceo = '\n'.join(l for l in pre_ceo.split('\n') if 'const fmt =' not in l)
# drop the CEO's own theme/links/navCounts/user lines (provided by the generator)
lines = [l for l in ret.split('\n') if not l.strip().startswith(('theme:', 'links:', 'navCounts:', 'user:'))]
ceo_vals = '\n'.join(lines).strip().rstrip(',')
ceo_vals = ceo_vals.replace("{ risk: 'claim-delay', code: 'MN2609-031', href: '#',", "{ risk: 'claim-delay', code: 'MN2609-031', href: 'Claims.dc.html',")

pre = pre_ceo + '''
    const role = s.role;
    const D = 'EventDetail.dc.html';
    const TITLES = { '대표': ['대표 대시보드', '10.01(목) 09:00 KST 기준 · 금액은 KRW 환산(10.01 적용 환율) · 예상은 점선'], '운영': ['운영 첫 화면', '10.01(목) 14:40 ULAT · 오늘 입출국, 진행 행사, 미배정·충돌을 먼저 봅니다'], '회계': ['회계 첫 화면', '10.01(목) 15:40 KST · 입금, 송금, 검토 대기를 먼저 봅니다'] };
    const PEOPLE = { '대표': { name: '이도윤', role: '대표' }, '운영': { name: '김지훈', role: '운영관리자' }, '회계': { name: '박서연', role: '회계담당자' } };
'''
vals = '''      user: PEOPLE[role],
      roles: ['대표', '운영', '회계'],
      role,
      setRole: (v) => set({ role: v }),
      title: TITLES[role][0],
      caption: TITLES[role][1],
      isCeo: role === '대표',
      isOps: role === '운영',
      isAcc: role === '회계',
      flightCols: [
        { key: 'when', label: '일시', type: 'stack' },
        { key: 'kind', label: '구분', type: 'strong' },
        { key: 'flight', label: '항공편' },
        { key: 'code', label: '행사코드', type: 'code' },
        { key: 'who', label: '여행사 / 인원', type: 'stack' },
        { key: 'crew', label: '가이드 / 차량', type: 'stack' },
        { key: 'assign', label: '배정', type: 'status', axis: 'assign' }
      ],
      flightRows: [
        { id: 'f1', when: { primary: '10.01(목) 21:40', secondary: '공항 도착 19:10' }, kind: '출국', flight: 'OM302', code: 'MN2609-038', href: D, who: { primary: '제이원트래블', secondary: '14+1명' }, crew: { primary: '간바타르', secondary: '푸르공 1호차' }, assign: 'acknowledged' },
        { id: 'f2', when: { primary: '10.02(금) 10:20', secondary: '픽업 칭기즈칸 국제공항' }, kind: '입국', flight: 'OM301', code: 'MN2610-002', href: D, who: { primary: '푸른하늘여행', secondary: '18+1명' }, crew: { primary: '바트-에르덴', secondary: '푸르공 1–3호차' }, assign: 'changed' },
        { id: 'f3', when: { primary: '10.03(토) 08:30', secondary: '픽업 칭기즈칸 국제공항' }, kind: '입국', flight: 'KE867', code: 'MN2610-005', href: D, who: { primary: '한빛투어', secondary: '8명' }, crew: { primary: '오윤치메그', secondary: '랜드크루저 1·2호' }, assign: 'conflict' },
        { id: 'f4', when: { primary: '10.03(토) 11:05', secondary: '공항 도착 08:30' }, kind: '출국', flight: 'KE868', code: 'MN2609-040', href: D, who: { primary: '솔빛여행', secondary: '9명' }, crew: { primary: '오윤치메그', secondary: '스타렉스' }, assign: 'conflict' }
      ],
      opsTodo: [
        { axis: 'assign', status: 'conflict', title: '오윤치메그 10.03 일정 충돌', meta: 'MN2609-040 출국과 MN2610-005 입국이 같은 아침', href: 'Schedule.dc.html' },
        { axis: 'assign', status: 'unassigned', title: 'MN2610-009 홉스골 · D-3 미배정', meta: '24+1명 · 한국어 가이드 1명 필요', href: 'Schedule.dc.html' },
        { axis: 'assign', status: 'changed', title: 'MN2610-002 귀국편 변경 미확인', meta: '바트-에르덴 · 10.01 11:20 알림 발송', href: 'Schedule.dc.html' },
        { axis: 'report', status: 'submitted', title: '현장 보고 2건 확인', meta: 'MN2609-040 일정 변경 · MN2609-031 완료 보고(지연)', href: 'FieldReports.dc.html' },
        { axis: 'claim', status: 'overdue', title: 'CL2609-004 처리 기한 초과', meta: '홉스골 숙소 온수 · 기한 3일 경과', href: 'Claims.dc.html' }
      ],
      accReceivable: { amount: 48200000, currency: 'KRW' },
      accOverdue: { amount: 12400000, currency: 'KRW', compact: false },
      accOverpaid: { amount: 1850000, currency: 'KRW', compact: false },
      dueCols: [
        { key: 'code', label: '행사코드', type: 'code' },
        { key: 'who', label: '여행사 / 기한', type: 'stack' },
        { key: 'billed', label: '청구액', type: 'money', currency: 'KRW' },
        { key: 'paid', label: '입금액', type: 'money', currency: 'KRW' },
        { key: 'rest', label: '잔액', type: 'money', currency: 'KRW' },
        { key: 'state', label: '상태', type: 'status', axis: 'payment' }
      ],
      dueRows: [
        { id: 'd1', code: 'MN2609-031', href: 'Receipts.dc.html', who: { primary: '다온여행사', secondary: '잔금 · 09.30(수)' }, billed: 32400000, paid: 20000000, rest: 12400000, state: 'overdue' },
        { id: 'd2', code: 'MN2609-040', href: 'Receipts.dc.html', who: { primary: '솔빛여행', secondary: '잔금 · 10.02(금)' }, billed: 9900000, paid: 4950000, rest: 4950000, state: 'due-soon' },
        { id: 'd3', code: 'MN2610-002', href: 'Receipts.dc.html', who: { primary: '푸른하늘여행', secondary: '잔금 · 10.02(금)' }, billed: 20700000, paid: 10350000, rest: 10350000, state: 'due-soon' },
        { id: 'd4', code: 'MN2610-012', href: 'Receipts.dc.html', who: { primary: '누리투어', secondary: '잔금 · 10.06(화)' }, billed: 54400000, paid: 33900000, rest: 20500000, state: 'partial' }
      ],
      dueTotals: { label: '미수 합계', billed: 117400000, paid: 69200000, rest: 48200000 },
      accTodo: [
        { axis: 'risk', status: 'duplicate', title: '중복 청구 후보 1건', meta: 'MN2609-033 · 525,000 MNT', href: 'Approvals.dc.html' },
        { axis: 'cost', status: 'reviewing', title: '비용 검토 대기 5건', meta: '9,255,000 MNT · 단가 차이 1건 포함', href: 'Approvals.dc.html' },
        { axis: 'remit', status: 'approved', title: 'RM2609-021-2 승인 후 미송금', meta: '10,500,000 MNT · 송금증 필요', href: 'Remittance.dc.html' },
        { axis: 'remit', status: 'requested', title: '송금 요청 2건 검토', meta: '64,600,000 MNT', href: 'Remittance.dc.html' },
        { axis: 'settle', status: 'open', title: '9월 마감 전 처리 4건', meta: '마감 예정 10.05(월)', href: 'Settlement.dc.html' }
      ],
''' + '      ' + ceo_vals + ','

admin('Main.dc.html', '대시보드', 'dashboard', None, main_body, pre=pre, vals=vals, state="{ role: '대표', chartView: '차트' }", height=1420)

# ------------------------------------------------------------------ Login
login = head('로그인') + '''<div data-theme="{{theme}}" class="abt-root" style="min-height: 100vh; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); background: var(--bg); color: var(--ink); font-family: var(--font-sans)">
<div style="display: flex; flex-direction: column; justify-content: space-between; gap: 40px; padding: 48px; border-right: 1px solid var(--line)">
<div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 16px">
<div style="display: flex; flex-direction: column; gap: 8px">
<p class="title-3" style="margin: 0">ABT Ops</p>
<p class="caption" style="margin: 0; color: var(--ink-muted)">ABT 여행 운영·정산 통합 관리</p>
</div>
<x-import component-from-global-scope="Abt.Segmented" size="sm" options="{{themeOptions}}" value="{{theme}}" on-change="{{setTheme}}" aria-label="화면 테마"></x-import>
</div>
<div style="display: flex; flex-direction: column; gap: 12px; max-width: 460px">
<p style="margin: 0; font: 600 34px/44px var(--font-sans); letter-spacing: -0.02em">행사 한 건으로 배정부터 정산까지 잇습니다.</p>
<p class="body" style="margin: 0; color: var(--ink-muted)">대표는 리스크를, 운영팀은 오늘 일정을, 회계팀은 입금·송금을, 가이드는 오늘 할 일을 먼저 봅니다.</p>
</div>
<div style="display: flex; flex-direction: column; gap: 10px">
<sc-for list="{{legend}}" as="l" hint-placeholder-count="3">
<div style="display: flex; align-items: center; gap: 12px">
<span style="box-sizing: border-box; width: 120px; height: 14px; border-radius: 4px; background: {{l.bg}}; border: {{l.border}}"></span>
<span class="caption" style="color: var(--ink-muted)">{{l.text}}</span>
</div>
</sc-for>
</div>
</div>
<div style="display: flex; align-items: center; justify-content: center; padding: 48px">
<div style="width: 100%; max-width: 400px; display: flex; flex-direction: column; gap: 20px">
<sc-if value="{{stepId}}" hint-placeholder-val="{{true}}">
<h1 class="title-1" style="margin: 0">로그인</h1>
<x-import component-from-global-scope="Abt.TextField" label="아이디" value="dy.lee@abt-travel.kr"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="비밀번호" type="password" value="password123"></x-import>
<x-import component-from-global-scope="Abt.Checkbox" label="이 기기에서 로그인 유지" description="공용 PC에서는 켜지 마세요."></x-import>
<x-import component-from-global-scope="Abt.Button" variant="primary" size="lg" block="{{yes}}" on-click="{{next}}">로그인</x-import>
<p class="caption" style="margin: 0; color: var(--ink-muted)">퇴사하거나 계약이 끝난 계정은 로그인할 수 없습니다. 비밀번호를 잊었으면 관리자에게 요청하세요.</p>
</sc-if>
<sc-if value="{{stepCode}}" hint-placeholder-val="{{false}}">
<h1 class="title-1" style="margin: 0">추가 인증</h1>
<p class="body" style="margin: 0; color: var(--ink-muted)">관리자·회계 계정은 휴대폰으로 보낸 6자리 코드를 한 번 더 확인합니다.</p>
<x-import component-from-global-scope="Abt.TextField" label="인증 코드" value="482 913" help="010-****-2741로 보냈습니다 · 4분 52초 남음"></x-import>
<x-import component-from-global-scope="Abt.Button" variant="primary" size="lg" block="{{yes}}" href="Main.dc.html">확인</x-import>
<x-import component-from-global-scope="Abt.Button" variant="ghost" block="{{yes}}" on-click="{{back}}">다른 계정으로 로그인</x-import>
</sc-if>
<div style="display: flex; flex-direction: column; gap: 10px; padding-top: 20px; border-top: 1px solid var(--line)">
<p class="label" style="margin: 0; color: var(--ink-muted)">프로토타입 바로 보기</p>
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px">
<x-import component-from-global-scope="Abt.Button" href="Main.dc.html" block="{{yes}}">관리자 웹</x-import>
<x-import component-from-global-scope="Abt.Button" href="GuideToday.dc.html" block="{{yes}}">가이드 모바일</x-import>
</div>
<p class="caption" style="margin: 0; color: var(--ink-muted)">대시보드 오른쪽 위에서 대표·운영·회계 첫 화면을 바꿔 볼 수 있습니다. 등록·배정한 내용은 이 브라우저에 남습니다.</p>
<x-import component-from-global-scope="Abt.Button" variant="ghost" block="{{yes}}" on-click="{{resetData}}">예시 데이터로 되돌리기</x-import>
<sc-if value="{{hasNotice}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.Alert" tone="{{notice.tone}}" title="{{notice.title}}">{{notice.body}}</x-import>
</sc-if>
</div>
</div>
</div>
</div>
</x-dc>
''' + script(1440, 900, "{ step: 'id' }", '', '''      stepId: s.step === 'id',
      stepCode: s.step === 'code',
      next: () => set({ step: 'code' }),
      resetData: () => { try { Object.keys(window.localStorage).filter((k) => k.indexOf('abt:') === 0).forEach((k) => window.localStorage.removeItem(k)); } catch (e) {} say('positive', '예시 데이터로 되돌렸습니다', '새로 등록한 행사·가이드·차량·매뉴얼과 배정 기록을 지웠습니다. 테마 설정은 그대로입니다.'); },
      back: () => set({ step: 'id' }),
      legend: [
        { bg: 'var(--chart-actual)', border: '0', text: '실선·채움은 확정된 값' },
        { bg: 'transparent', border: '1px dashed var(--line-strong)', text: '점선은 아직 예상이거나 요청인 값' },
        { bg: 'var(--critical)', border: '0', text: '색은 정산·리스크 상태에만' }
      ],''')
open(OUT + '/Login.dc.html', 'w', encoding='utf-8', newline='\n').write(login)

# ------------------------------------------------------------------ Alerts
alerts_body = header('알림', '읽음과 처리 완료를 따로 셉니다 · 기한을 넘긴 건은 책임자에게 다시 알립니다', '''<x-import component-from-global-scope="Abt.Button" variant="secondary" on-click="{{readAll}}">모두 읽음 표시</x-import>''') + '''
<x-import component-from-global-scope="Abt.Tabs" items="{{tabs}}" value="{{filter}}" on-change="{{setFilter}}" aria-label="알림 구분"></x-import>
''' + PANEL_TIGHT + '''
<sc-for list="{{items}}" as="n" hint-placeholder-count="6">
<div style="display: grid; grid-template-columns: 10px 120px minmax(0, 1fr) auto; align-items: center; gap: 14px; padding: 14px 0; border-top: 1px solid var(--line)">
<span style="width: 8px; height: 8px; border-radius: 9999px; background: {{n.dot}}"></span>
<x-import component-from-global-scope="Abt.StatusBadge" tone="{{n.tone}}" form="{{n.form}}">{{n.kind}}</x-import>
<div style="display: flex; flex-direction: column; gap: 2px; min-width: 0">
<span class="body" style="font-weight: {{n.weight}}">{{n.title}}</span>
<span class="caption" style="color: var(--ink-muted)">{{n.meta}}</span>
</div>
<div style="display: flex; align-items: center; gap: 8px">
<x-import component-from-global-scope="Abt.Button" size="sm" href="{{n.href}}">열기</x-import>
<sc-if value="{{n.open}}" hint-placeholder-val="{{true}}">
<x-import component-from-global-scope="Abt.Button" size="sm" variant="ghost" on-click="{{n.finish}}">처리 완료</x-import>
</sc-if>
<sc-if value="{{n.closed}}" hint-placeholder-val="{{false}}">
<span class="caption" style="color: var(--ink-muted)">처리 완료</span>
</sc-if>
</div>
</div>
</sc-for>
<sc-if value="{{empty}}" hint-placeholder-val="{{false}}">
<p class="body" style="margin: 0; padding: 32px 0; text-align: center; color: var(--ink-muted)">이 구분에 알림이 없습니다.</p>
</sc-if>
</section>
'''
alerts_pre = '''    const base = [
      { id: 'a1', tone: 'critical', form: 'solid', kind: '일정 충돌', title: '오윤치메그 10.03 일정 충돌 · MN2609-040 / MN2610-005', meta: '10.01 09:12 KST · 운영 · 출발 2일 전', href: 'Schedule.dc.html' },
      { id: 'a2', tone: 'critical', form: 'solid', kind: '기한 초과', title: 'CL2609-004 홉스골 숙소 온수 클레임 처리 기한 3일 초과', meta: '10.01 09:00 KST · 운영관리자 재알림 2회', href: 'Claims.dc.html' },
      { id: 'a3', tone: 'critical', form: 'solid', kind: '연체', title: '다온여행사 MN2609-031 잔금 12,400,000 KRW 연체 1일', meta: '10.01 09:00 KST · 회계', href: 'Receipts.dc.html' },
      { id: 'a4', tone: 'attention', form: 'solid', kind: '승인 요청', title: '검토 대기 비용 5건 · 9,255,000 MNT', meta: '10.01 08:20 KST · 회계 · 검토 후보 3건 포함', href: 'Approvals.dc.html' },
      { id: 'a5', tone: 'attention', form: 'solid', kind: '변경 미확인', title: '바트-에르덴이 MN2610-002 귀국편 변경을 아직 확인하지 않았습니다', meta: '10.01 11:20 KST 발송 · 출발 1일 전', href: 'Schedule.dc.html' },
      { id: 'a6', tone: 'progress', form: 'dashed', kind: '송금 대기', title: 'RM2609-021-2 승인 후 미송금 · 10,500,000 MNT', meta: '09.27 승인 · 송금증 필요', href: 'Remittance.dc.html' },
      { id: 'a7', tone: 'progress', form: 'solid', kind: '현장 보고', title: '간바타르가 MN2609-038 완료 보고를 제출했습니다', meta: '10.01 14:30 ULAT · 운영 확인 필요', href: 'FieldReports.dc.html' },
      { id: 'a8', tone: 'positive', form: 'solid', kind: '브리핑 확인', title: 'MN2610-002 가이드 브리핑 확인 완료', meta: '10.01 13:05 ULAT · 바트-에르덴', href: 'EventDetail.dc.html', info: true }
    ];
    const done = s.done, read = s.read;
    const all = base.map((n) => ({ ...n, isDone: !!done[n.id] || !!n.info, isRead: !!read[n.id] || !!done[n.id] }));
    const groups = { '처리 필요': all.filter((n) => !n.isDone), '읽지 않음': all.filter((n) => !n.isRead), '처리 완료': all.filter((n) => n.isDone), '전체': all };
    const list = groups[s.filter] || all;
    const items = list.map((n) => ({ ...n, dot: n.isRead ? 'transparent' : 'var(--ink)', weight: n.isRead ? 400 : 600, open: !n.isDone, closed: n.isDone, finish: () => set({ done: { ...done, [n.id]: true } }) }));
'''
alerts_vals = '''      user: { name: '김지훈', role: '운영관리자' },
      tabs: [
        { id: '처리 필요', label: '처리 필요', count: groups['처리 필요'].length, tone: 'critical' },
        { id: '읽지 않음', label: '읽지 않음', count: groups['읽지 않음'].length },
        { id: '처리 완료', label: '처리 완료', count: groups['처리 완료'].length },
        { id: '전체', label: '전체', count: all.length }
      ],
      filter: s.filter,
      setFilter: (v) => set({ filter: v }),
      readAll: () => { const r = {}; base.forEach((n) => { r[n.id] = true; }); set({ read: r }); },
      items,
      empty: items.length === 0,'''
admin('Alerts.dc.html', '알림', 'alerts', None, alerts_body, pre=alerts_pre, vals=alerts_vals, state="{ filter: '처리 필요', done: {}, read: {} }", height=1000)

# ------------------------------------------------------------------ Reports
reports_body = header('리포트', '모든 리포트에 집계 기준 시각·통화·환율·예상/확정 구분을 표시합니다 · 내보내기에는 권한이 있는 열만 담깁니다', '''<x-import component-from-global-scope="Abt.Select" inline="{{yes}}" label="기간" options="{{periods}}" value="{{period}}" on-change="{{setPeriod}}"></x-import>''') + NOTICE + '''
<div style="display: grid; grid-template-columns: 280px minmax(0, 1fr); gap: 16px; align-items: start">
<nav aria-label="리포트 목록" style="display: flex; flex-direction: column; gap: 2px; padding: 8px; background: var(--surface); border: 1px solid var(--line); border-radius: 6px">
<sc-for list="{{reports}}" as="r" hint-placeholder-count="8">
<button type="button" onClick="{{r.pick}}" style="display: flex; flex-direction: column; align-items: flex-start; gap: 2px; padding: 10px 12px; border: 0; border-radius: 4px; text-align: left; cursor: pointer; color: var(--ink); background: {{r.bg}}">
<span style="font: 600 14px/20px var(--font-sans)">{{r.name}}</span>
<span style="font: 400 12px/18px var(--font-sans); color: var(--ink-muted)">{{r.desc}}</span>
</button>
</sc-for>
</nav>
''' + PANEL + '''<div style="display: flex; flex-wrap: wrap; align-items: flex-start; justify-content: space-between; gap: 12px">
<div style="display: flex; flex-direction: column; gap: 2px">
<h2 class="title-2" style="margin: 0">{{cur.name}}</h2>
<p class="caption" style="margin: 0; color: var(--ink-muted)">{{cur.basis}}</p>
</div>
<div style="display: flex; gap: 8px">
<x-import component-from-global-scope="Abt.Segmented" size="sm" options="{{modes}}" value="{{mode}}" on-change="{{setMode}}" aria-label="금액 구분"></x-import>
<x-import component-from-global-scope="Abt.Button" size="sm" on-click="{{print}}">인쇄용 보기</x-import>
<x-import component-from-global-scope="Abt.Button" size="sm" variant="primary" on-click="{{export}}">엑셀 다운로드</x-import>
</div>
</div>
<sc-if value="{{exported}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.Alert" tone="positive" title="{{exportTitle}}">권한이 있는 열만 담았습니다. 집계 기준과 환율이 첫 행에 들어갑니다.</x-import>
</sc-if>
<sc-if value="{{hasBars}}" hint-placeholder-val="{{false}}">
<div style="display: flex; flex-direction: column; gap: 10px; padding: 4px 0 8px">
<sc-for list="{{bars}}" as="b" hint-placeholder-count="6">
<div class="abt-tip-host" tabindex="0" style="display: grid; grid-template-columns: 120px minmax(0, 1fr) 120px; align-items: center; gap: 12px">
<span class="caption" style="color: var(--ink)">{{b.name}}</span>
<div style="position: relative; height: 16px">
<span class="abt-tip" role="tooltip" style="left: {{b.actualPct}}%"><span class="abt-tip__title">{{b.name}}</span><sc-for list="{{b.tip}}" as="t" hint-placeholder-count="3"><span class="abt-tip__row"><span>{{t.k}}</span><span>{{t.v}}</span></span></sc-for></span>
<div style="position: absolute; left: 0; top: 0; bottom: 0; width: {{b.planPct}}%; box-sizing: border-box; border: 1px dashed var(--chart-expected); border-radius: 0 4px 4px 0"></div>
<div style="position: absolute; left: 0; top: 0; bottom: 0; width: {{b.actualPct}}%; background: var(--chart-actual); border-radius: 0 4px 4px 0"></div>
</div>
<span class="caption" style="text-align: right; color: var(--ink); font-variant-numeric: tabular-nums">{{b.label}}</span>
</div>
</sc-for>
<p class="caption" style="margin: 0; color: var(--ink-muted)">막대: 확정 매출(실선) · 예상 포함(점선) · 단위 KRW</p>
</div>
</sc-if>
<x-import component-from-global-scope="Abt.DataTable" columns="{{cur.cols}}" rows="{{cur.rows}}" totals="{{cur.totals}}" density="compact" caption="{{cur.name}}"></x-import>
</section>
</div>
'''
reports_pre = '''    const R = [
      { id: 'daily', name: '일일 행사', desc: '오늘 진행·입출국 행사', basis: '10.01(목) 기준 · 현지 시각 ULAT',
        cols: [ { key: 'code', label: '행사코드', type: 'code' }, { key: 'agency', label: '여행사' }, { key: 'day', label: '일차' }, { key: 'pax', label: '인원', align: 'end' }, { key: 'guide', label: '가이드' }, { key: 'note', label: '오늘', type: 'muted' } ],
        rows: [ { id: 1, code: 'MN2609-038', href: 'EventDetail.dc.html', agency: '제이원트래블', day: '3/3일', pax: '14+1', guide: '간바타르', note: '21:40 OM302 출국' }, { id: 2, code: 'MN2609-040', href: 'EventDetail.dc.html', agency: '솔빛여행', day: '2/4일', pax: '9', guide: '오윤치메그', note: '울란바토르 시내' } ] },
      { id: 'monthly', name: '월별 행사', desc: '월별 팀 수·인원·상태', basis: '2026.05 – 11 · 출발일 기준',
        cols: [ { key: 'm', label: '월' }, { key: 'teams', label: '팀', type: 'number', suffix: '팀' }, { key: 'pax', label: '인원', type: 'number', suffix: '명' }, { key: 'done', label: '완료', type: 'number' }, { key: 'cancel', label: '취소', type: 'number' } ],
        rows: [ { id: 5, m: '5월', teams: 18, pax: 286, done: 18, cancel: 1 }, { id: 6, m: '6월', teams: 27, pax: 431, done: 27, cancel: 0 }, { id: 7, m: '7월', teams: 41, pax: 702, done: 41, cancel: 2 }, { id: 8, m: '8월', teams: 38, pax: 655, done: 38, cancel: 1 }, { id: 9, m: '9월', teams: 29, pax: 462, done: 28, cancel: 0 }, { id: 10, m: '10월', teams: 18, pax: 251, done: 0, cancel: 1 } ],
        totals: { label: '합계', teams: 171, pax: 2787 } },
      { id: 'agency', name: '여행사별 매출', desc: '판매·확정 매출과 미수', basis: '2026.09 – 10 출발 · KRW · 확정은 정산 확정분', bars: true,
        cols: [ { key: 'name', label: '여행사', type: 'strong' }, { key: 'teams', label: '팀', type: 'number' }, { key: 'sales', label: '확정 매출', type: 'money', currency: 'KRW' }, { key: 'plan', label: '예상 포함', type: 'money', currency: 'KRW', kind: 'expected' }, { key: 'ar', label: '미수금', type: 'money', currency: 'KRW' } ],
        rows: [ { id: 1, name: '한빛투어', teams: 9, sales: 132400000, plan: 164000000, ar: 0 }, { id: 2, name: '푸른하늘여행', teams: 8, sales: 98300000, plan: 132200000, ar: 10350000 }, { id: 3, name: '다온여행사', teams: 6, sales: 61200000, plan: 93600000, ar: 12400000 }, { id: 4, name: '제이원트래블', teams: 6, sales: 57100000, plan: 75500000, ar: 0 }, { id: 5, name: '누리투어', teams: 4, sales: 48600000, plan: 103000000, ar: 20500000 }, { id: 6, name: '솔빛여행', teams: 5, sales: 31800000, plan: 41700000, ar: 4950000 } ],
        totals: { label: '합계', teams: 38, sales: 429400000, plan: 610000000, ar: 48200000 } },
      { id: 'guide', name: '가이드 배정', desc: '가동일·행사 실적·수당', basis: '2026년 9월 · 배정 확정분',
        cols: [ { key: 'name', label: '가이드', type: 'strong' }, { key: 'days', label: '가동일', type: 'number', suffix: '일' }, { key: 'events', label: '행사', type: 'number', suffix: '건' }, { key: 'pay', label: '가이드비·수당', type: 'money', currency: 'MNT' }, { key: 'claims', label: '클레임', type: 'number' } ],
        rows: [ { id: 1, name: '바트-에르덴', days: 22, events: 4, pay: 4840000, claims: 0 }, { id: 2, name: '간바타르', days: 20, events: 5, pay: 4400000, claims: 1 }, { id: 3, name: '오윤치메그', days: 18, events: 5, pay: 3960000, claims: 0 }, { id: 4, name: '뭉흐-오치르', days: 17, events: 3, pay: 3740000, claims: 0 }, { id: 5, name: '사롤', days: 9, events: 2, pay: 1620000, claims: 0 } ] },
      { id: 'remit', name: '송금', desc: '요청·승인·완료·수수료', basis: '2026년 9월 · 한국 → 몽골 · 내부거래',
        cols: [ { key: 'stage', label: '단계', type: 'status', axis: 'remit' }, { key: 'n', label: '건', type: 'number' }, { key: 'mnt', label: '금액', type: 'money', currency: 'MNT' }, { key: 'fee', label: '수수료', type: 'money', currency: 'KRW' } ],
        rows: [ { id: 1, stage: 'requested', n: 1, mnt: 54800000, fee: null }, { id: 2, stage: 'reviewing', n: 1, mnt: 9800000, fee: null }, { id: 3, stage: 'approved', n: 1, mnt: 10500000, fee: null }, { id: 4, stage: 'completed', n: 4, mnt: 149300000, fee: 76000 }, { id: 5, stage: 'rejected', n: 1, mnt: 17500000, fee: null } ] },
      { id: 'ar', name: '미수금', desc: '여행사별 경과 일수', basis: '10.01 09:00 KST · KRW · 청구 기준',
        cols: [ { key: 'name', label: '여행사', type: 'strong' }, { key: 'd0', label: '기한 전', type: 'money', currency: 'KRW' }, { key: 'd7', label: '1–7일', type: 'money', currency: 'KRW' }, { key: 'd30', label: '8–30일', type: 'money', currency: 'KRW' }, { key: 'd31', label: '30일 넘음', type: 'money', currency: 'KRW' } ],
        rows: [ { id: 1, name: '다온여행사', d0: 0, d7: 12400000, d30: 0, d31: 0 }, { id: 2, name: '누리투어', d0: 20500000, d7: 0, d30: 0, d31: 0 }, { id: 3, name: '푸른하늘여행', d0: 10350000, d7: 0, d30: 0, d31: 0 }, { id: 4, name: '솔빛여행', d0: 4950000, d7: 0, d30: 0, d31: 0 } ],
        totals: { label: '합계', d0: 35800000, d7: 12400000, d30: 0, d31: 0 } },
      { id: 'pl', name: '행사별 손익', desc: '한국 마진·현지 수익·통합', basis: '2026년 9월 · KRW 환산 0.3985 · 내부거래 제외',
        cols: [ { key: 'code', label: '행사코드', type: 'code' }, { key: 'sales', label: '판매금액', type: 'money', currency: 'KRW' }, { key: 'k', label: '한국 마진', type: 'money', currency: 'KRW', lossTone: true }, { key: 'm', label: '현지 수익', type: 'money', currency: 'KRW', lossTone: true }, { key: 'c', label: '통합 손익', type: 'money', currency: 'KRW', lossTone: true } ],
        rows: [ { id: 1, code: 'MN2609-031', href: 'EventDetail.dc.html', sales: 32400000, k: 3708000, m: -4949370, c: -1241370 }, { id: 2, code: 'MN2609-033', href: 'EventDetail.dc.html', sales: 23000000, k: 2875750, m: -693390, c: 2182360 }, { id: 3, code: 'MN2609-035', href: 'EventDetail.dc.html', sales: 25300000, k: 4259200, m: 757150, c: 5016350 }, { id: 4, code: 'MN2609-036', href: 'EventDetail.dc.html', sales: 41800000, k: 7529000, m: 916550, c: 8445550 } ] },
      { id: 'mpl', name: '월 손익', desc: '행사 손익과 고정 운영비', basis: '2026.05 – 09 · KRW · 9월은 정산 검토 중',
        cols: [ { key: 'm', label: '월' }, { key: 'event', label: '행사 손익', type: 'money', currency: 'KRW', lossTone: true }, { key: 'fixed', label: '고정 운영비', type: 'money', currency: 'KRW' }, { key: 'company', label: '회사 손익', type: 'money', currency: 'KRW', lossTone: true } ],
        rows: [ { id: 5, m: '5월', event: 61300000, fixed: 38500000, company: 22800000 }, { id: 6, m: '6월', event: 89500000, fixed: 39200000, company: 50300000 }, { id: 7, m: '7월', event: 124000000, fixed: 41800000, company: 82200000 }, { id: 8, m: '8월', event: 118600000, fixed: 41500000, company: 77100000 }, { id: 9, m: '9월', event: { amount: 74200000, kind: 'expected' }, fixed: 39900000, company: { amount: 34300000, kind: 'expected' } } ] }
    ];
    const cur = R.find((r) => r.id === s.report) || R[2];
    const maxPlan = Math.max(...(R[2].rows.map((r) => r.plan)));
    const bars = R[2].rows.map((r) => ({ name: r.name, planPct: Math.round((r.plan / maxPlan) * 1000) / 10, actualPct: Math.round(((s.mode === '확정' ? r.sales : r.plan) / maxPlan) * 1000) / 10, label: fmt(Math.round((s.mode === '확정' ? r.sales : r.plan) / 10000)) + '만',
      tip: [ { k: '확정 매출', v: fmt(r.sales) + ' KRW' }, { k: '예상 포함', v: fmt(r.plan) + ' KRW' }, { k: '미수금', v: fmt(r.ar) + ' KRW' }, { k: '팀', v: r.teams + '팀' } ] }));
'''
reports_vals = '''      user: { name: '이도윤', role: '대표' },
      periods: ['2026.09 – 10', '2026년 9월', '2026년 3분기'],
      period: s.period,
      setPeriod: (e) => set({ period: e.target.value, exported: false }),
      reports: R.map((r) => ({ ...r, pick: () => set({ report: r.id, exported: false }), bg: r.id === cur.id ? 'var(--surface-selected)' : 'transparent' })),
      cur: { ...cur, totals: cur.totals || undefined, basis: s.period === '2026.09 – 10' ? cur.basis : `조회 기간 ${s.period} · ` + cur.basis.split(' · ').slice(1).join(' · ') },
      modes: ['확정', '예상 포함'],
      mode: s.mode,
      setMode: (v) => set({ mode: v }),
      hasBars: !!cur.bars,
      bars,
      exported: s.exported,
      exportTitle: '엑셀 파일을 만들었습니다 · ' + cur.name.replace(/ /g, '') + '_2026-10-01.xlsx',
      export: () => set({ exported: true }),
      print: () => say('progress', '인쇄용 화면을 만들었습니다', `A4 가로 · ${cur.name} · 머리말에 집계 기준(${s.period})·통화·환율·예상/확정 구분이 들어갑니다.`),'''
admin('Reports.dc.html', '리포트', 'reports', None, reports_body, pre=reports_pre, vals=reports_vals, state="{ report: 'agency', mode: '확정', exported: false, period: '2026.09 – 10', notice: null }", height=1000)
print('batch1 written')
