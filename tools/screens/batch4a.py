import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import *

ROW = 'display: grid; grid-template-columns: minmax(0, 1fr) auto; align-items: center; gap: 12px; padding: 8px 0; border-top: 1px solid var(--line); font-size: 13px; line-height: 20px'
SUB = '<span class="label" style="color: var(--ink-muted); padding-top: 4px">{}</span>'

# ------------------------------------------------------------------ Agencies (여행사)
body = header('여행사', '거래처(여행사)와 담당자·거래 조건·운영 요청사항 · 행사·매출·미수금이 여행사별로 이어집니다', '''<x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{toggleNew}}">{{newLabel}}</x-import>''')
body += NOTICE
body += '''<sc-if value="{{creating}}" hint-placeholder-val="{{false}}">
''' + PANEL + panel_title('여행사 등록', '거래처 코드는 저장할 때 부여됩니다') + field_grid(200) + '''
<x-import component-from-global-scope="Abt.TextField" label="여행사명" required="{{yes}}" value="{{nf.name}}" on-change="{{onNf.name}}" error="{{nfErr.name}}"></x-import>
<x-import component-from-global-scope="Abt.Select" label="채널" options="{{channelOptions}}" value="{{nf.channel}}" on-change="{{onNf.channel}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="담당자" value="{{nf.contact}}" on-change="{{onNf.contact}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="연락처" value="{{nf.phone}}" on-change="{{onNf.phone}}"></x-import>
<x-import component-from-global-scope="Abt.Select" label="계약금" options="{{depositOptions}}" value="{{nf.deposit}}" on-change="{{onNf.deposit}}"></x-import>
<x-import component-from-global-scope="Abt.Select" label="잔금 기한" options="{{dueOptions}}" value="{{nf.due}}" on-change="{{onNf.due}}"></x-import>
</div>
<div style="display: flex; justify-content: flex-end; gap: 8px"><x-import component-from-global-scope="Abt.Button" variant="ghost" on-click="{{toggleNew}}">취소</x-import><x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{submitNew}}">등록</x-import></div>
</section>
</sc-if>
''' + TWO_PANE + '''
<x-import component-from-global-scope="Abt.DataTable" columns="{{cols}}" rows="{{rows}}" totals="{{totals}}" on-row-click="{{pick}}" caption="여행사 목록"></x-import>
''' + SIDE_PANEL + '''<div style="display: flex; flex-direction: column; gap: 6px">
<div style="display: flex; align-items: center; justify-content: space-between; gap: 8px"><span style="font: 500 13px/20px var(--font-mono); color: var(--ink-muted)">{{cur.id}}</span><x-import component-from-global-scope="Abt.StatusBadge" tone="{{cur.tone}}" size="md">{{cur.stLabel}}</x-import></div>
<h2 class="title-2" style="margin: 0">{{cur.name}}</h2>
<span class="caption" style="color: var(--ink-muted)">{{cur.channel}}</span>
</div>
''' + dl([('담당자', '{{cur.contact}} · {{cur.phone}}'), ('거래 조건', '{{cur.terms}}'), ('정산 방식', '{{cur.settle}}'), ('조회 계정', '{{cur.portal}}')], 80) + '''<div style="display: flex; flex-direction: column; gap: 6px">
<span class="label" style="color: var(--ink-muted)">운영 요청사항</span>
<sc-if value="{{notEditing}}" hint-placeholder-val="{{true}}"><p class="body" style="margin: 0; font-size: 13px; line-height: 20px">{{cur.request}}</p></sc-if>
<sc-if value="{{editing}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.TextField" aria-label="운영 요청사항" multiline="{{yes}}" rows="{{three}}" value="{{draft}}" on-change="{{setDraft}}" help="가이드 브리핑의 여행사별 매뉴얼에 그대로 나갑니다"></x-import>
<div style="display: flex; justify-content: flex-end; gap: 8px"><x-import component-from-global-scope="Abt.Button" size="sm" variant="ghost" on-click="{{cancelEdit}}">취소</x-import><x-import component-from-global-scope="Abt.Button" size="sm" variant="primary" on-click="{{saveEdit}}">저장</x-import></div>
</sc-if>
</div>
<sc-if value="{{cur.hasAlert}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.Alert" tone="{{cur.alertTone}}" title="{{cur.alertTitle}}" action="{{cur.alertAction}}">{{cur.alertBody}}</x-import>
</sc-if>
<div style="display: flex; flex-direction: column">
''' + SUB.format('최근 행사') + '''
<sc-for list="{{cur.events}}" as="e" hint-placeholder-count="3">
<div style="''' + ROW + '''"><span style="display: flex; align-items: center; gap: 8px; min-width: 0"><x-import component-from-global-scope="Abt.EventCode" code="{{e.code}}" href="EventDetail.dc.html"></x-import><span style="min-width: 0">{{e.text}}</span></span><x-import component-from-global-scope="Abt.StatusBadge" axis="event" status="{{e.status}}"></x-import></div>
</sc-for>
</div>
<div style="display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 8px">
<sc-if value="{{notEditing}}" hint-placeholder-val="{{true}}"><x-import component-from-global-scope="Abt.Button" size="sm" on-click="{{startEdit}}">요청사항 수정</x-import></sc-if>
<x-import component-from-global-scope="Abt.Button" size="sm" href="Manuals.dc.html">여행사별 매뉴얼</x-import>
<x-import component-from-global-scope="Abt.Button" size="sm" variant="primary" href="EventNew.dc.html">이 여행사로 행사 등록</x-import>
</div>
</section>
</div>
'''
pre = '''
    const A = s.agencies;
    const cur = A.find((a) => a.id === s.selected) || A[0];
    const nf = s.nf;
'''
vals = '''      creating: !!s.creating,
      newLabel: s.creating ? '등록 닫기' : '여행사 등록',
      toggleNew: () => set({ creating: !s.creating, nfErr: {} }),
      channelOptions: ['일반 패키지', '골프 전문', '기업 인센티브', '승마·체험', '소규모·맞춤'],
      depositOptions: ['30%', '50%', '없음(잔금 일괄)'],
      dueOptions: ['출발 7일 전', '출발 2일 전', '출발일', '출발 후 4일'],
      nf,
      onNf: { name: (e) => set({ nf: { ...s.nf, name: e.target.value }, nfErr: {} }), channel: (e) => set({ nf: { ...s.nf, channel: e.target.value } }), contact: (e) => set({ nf: { ...s.nf, contact: e.target.value } }), phone: (e) => set({ nf: { ...s.nf, phone: e.target.value } }), deposit: (e) => set({ nf: { ...s.nf, deposit: e.target.value } }), due: (e) => set({ nf: { ...s.nf, due: e.target.value } }) },
      nfErr: s.nfErr || {},
      submitNew: () => {
        if (!nf.name.trim()) { set({ nfErr: { name: '여행사명을 입력하세요.' } }); return; }
        if (A.some((a) => a.name === nf.name.trim())) { set({ nfErr: { name: '같은 이름의 여행사가 이미 있습니다.' } }); return; }
        const a = { id: 'AG-0' + (A.length + 13), name: nf.name.trim(), channel: nf.channel, contact: nf.contact || '—', phone: nf.phone || '—', terms: `계약금 ${nf.deposit} · 잔금 ${nf.due}`, settle: '행사별 청구 · KRW', portal: '없음', request: '아직 없습니다.', events: [], count: 0, sales: 0, rest: 0, st: 'new' };
        this.setState({ agencies: A.concat([a]), selected: a.id, creating: false, nf: { name: '', channel: '일반 패키지', contact: '', phone: '', deposit: '30%', due: '출발 7일 전' }, notice: { tone: 'positive', title: `${a.name}을(를) 등록했습니다`, body: `거래처 코드 ${a.id} · 이제 행사 등록에서 고를 수 있습니다.`, action: { label: '행사 등록', href: 'EventNew.dc.html' } } });
      },
      cols: [
        { key: 'name', label: '여행사', type: 'stack' },
        { key: 'contact', label: '담당자', type: 'muted' },
        { key: 'count', label: '올해 행사', type: 'number', suffix: '건' },
        { key: 'sales', label: '매출', type: 'money', currency: 'KRW' },
        { key: 'rest', label: '미수', type: 'money', currency: 'KRW' },
        { key: 'st', label: '상태', type: 'status' }
      ],
      rows: A.map((a) => ({ id: a.id, name: { primary: a.name, secondary: a.channel }, contact: a.contact, count: a.count, sales: a.sales, rest: a.rest || null, st: a.st === 'watch' ? { tone: 'critical', status: '미수 연체' } : a.st === 'new' ? { tone: 'neutral', form: 'dashed', status: '신규' } : { tone: 'neutral', status: '거래 중' }, selected: a.id === cur.id })),
      totals: { label: '합계', sales: A.reduce((x, a) => x + a.sales, 0), rest: A.reduce((x, a) => x + a.rest, 0) },
      pick: (row) => set({ selected: row.id, editing: false }),
      cur: { ...cur, tone: cur.st === 'watch' ? 'critical' : 'neutral', stLabel: cur.st === 'watch' ? '미수 연체' : cur.st === 'new' ? '신규' : '거래 중', hasAlert: !!cur.alert, alertTone: cur.alert ? cur.alert.tone : 'progress', alertTitle: cur.alert ? cur.alert.title : '', alertBody: cur.alert ? cur.alert.body : '', alertAction: cur.alert ? cur.alert.action : null },
      editing: !!s.editing,
      notEditing: !s.editing,
      draft: s.draft,
      setDraft: (e) => set({ draft: e.target.value }),
      startEdit: () => set({ editing: true, draft: cur.request }),
      cancelEdit: () => set({ editing: false }),
      saveEdit: () => this.setState({ agencies: A.map((a) => (a.id === cur.id ? { ...a, request: s.draft } : a)), editing: false, notice: { tone: 'positive', title: `${cur.name} 요청사항을 바꿨습니다`, body: '다음 행사부터 가이드 브리핑에 바뀐 내용이 나갑니다. 변경 전후는 감사 로그에 남습니다.' } }),'''
state = '''{ selected: 'AG-003', creating: false, editing: false, draft: '', nfErr: {}, notice: null,
      nf: { name: '', channel: '일반 패키지', contact: '', phone: '', deposit: '30%', due: '출발 7일 전' },
      agencies: [
        { id: 'AG-001', name: '푸른하늘여행', channel: '일반 패키지 · 직판 B2B', contact: '최민정 과장', phone: '02-6012-3381', terms: '계약금 30% · 잔금 출발 7일 전', settle: '행사별 청구 · KRW · 세금계산서', portal: '조회 계정 1개(최민정) · 공유 정산서만', request: '단체 사진 촬영 필수 · 일정 변경은 24시간 안에 메일 통보 · 마지막 날 한식 만찬 선호', count: 14, sales: 248600000, rest: 10350000, st: 'ok', events: [ { code: 'MN2610-002', text: '고비 사막 · 10.02 출발', status: 'confirmed' }, { code: 'MN2610-014', text: 'UB 시티 · 10.10 출발', status: 'booked' }, { code: 'MN2609-033', text: '고비 사막 · 정산 검토', status: 'completed' } ] },
        { id: 'AG-002', name: '한빛투어', channel: '골프 전문', contact: '박지현 대리', phone: '02-3446-7720', terms: '계약금 30% · 잔금 출발 7일 전', settle: '행사별 청구 · KRW', portal: '없음', request: '티오프 2시간 전 재확인 · 골프백 운송 확인 · 라운드 후 사우나 일정 선호', count: 11, sales: 186400000, rest: 0, st: 'ok', alert: { tone: 'progress', title: '과입 1,850,000 KRW', body: '09.28 잔금이 더 들어왔습니다. 다음 청구에서 차감 예정입니다.', action: { label: '과입·차감', href: 'Balance.dc.html' } }, events: [ { code: 'MN2610-005', text: '테를지 골프 · 10.03 출발', status: 'confirmed' }, { code: 'MN2610-019', text: '테를지 골프 · 10.16 출발', status: 'confirmed' } ] },
        { id: 'AG-003', name: '다온여행사', channel: '일반 패키지', contact: '이수진 팀장', phone: '02-777-1029', terms: '계약금 없음 · 잔금 출발 후 4일', settle: '행사별 청구 · KRW', portal: '없음', request: '식사 메뉴는 출발 3일 전 공유 · 고령 고객이 많아 이동 시간 2시간마다 휴식', count: 9, sales: 152300000, rest: 12400000, st: 'watch', alert: { tone: 'critical', title: '미수 연체 12,400,000 KRW', body: 'MN2609-031 잔금 · 기한 09.30 · 재알림 2회. 취소 환불 660,000 KRW와 상계할 수 있습니다.', action: { label: '입금 원장', href: 'Receipts.dc.html' } }, events: [ { code: 'MN2610-009', text: '홉스골 · 10.04 출발 · 미배정', status: 'confirmed' }, { code: 'MN2610-024', text: 'UB 시티 · 취소(수수료 20%)', status: 'cancelled' }, { code: 'MN2609-031', text: '홉스골 · 적자 · 연체', status: 'completed' } ] },
        { id: 'AG-004', name: '누리투어', channel: '기업 인센티브', contact: '오현우 부장', phone: '02-2088-5530', terms: '계약금 30% + 중도금 · 잔금 출발 2일 전', settle: '기업별 통합 청구 · KRW', portal: '조회 계정 2개', request: 'VIP 차량 별도 · 영문 일정표 · 만찬 무대 장비 사전 확인', count: 6, sales: 211000000, rest: 20500000, st: 'ok', events: [ { code: 'MN2610-012', text: '기업 인센티브 · 10.08 출발', status: 'confirmed' } ] },
        { id: 'AG-005', name: '제이원트래블', channel: '승마·체험', contact: '한승희 실장', phone: '051-805-2290', terms: '계약금 50% · 잔금 출발 7일 전', settle: '행사별 청구 · KRW', portal: '없음', request: '승마 경험 수준을 출발 전 설문으로 받음 · 초보는 별도 조', count: 8, sales: 121600000, rest: 0, st: 'ok', events: [ { code: 'MN2609-038', text: '테를지 승마 · 진행 중', status: 'in-progress' }, { code: 'MN2610-017', text: '고비 사막 · 10.15 출발', status: 'booked' } ] },
        { id: 'AG-006', name: '솔빛여행', channel: '소규모·맞춤', contact: '장소영 대리', phone: '02-6203-1188', terms: '계약금 50% · 잔금 출발일', settle: '행사별 청구 · KRW', portal: '없음', request: '일정 변경은 카카오톡으로 먼저 알림 · 소규모라 차량은 스타렉스 선호', count: 6, sales: 64300000, rest: 4950000, st: 'ok', events: [ { code: 'MN2609-040', text: 'UB 시티 · 진행 중', status: 'in-progress' }, { code: 'MN2610-021', text: '홉스골 · 10.18 출발', status: 'booked' } ] }
      ] }'''
admin('Agencies.dc.html', '여행사', 'agencies', 'ops', body, pre=pre, vals=vals, state=state, height=1000)
print('Agencies written')


# ------------------------------------------------------------------ Products (상품)
body = header('상품', '상품코드·일정 템플릿·포함/불포함·옵션 · 새 버전을 게시해도 이미 확정된 행사에는 자동으로 반영되지 않습니다', '')
body += NOTICE
body += TWO_PANE + '''
<x-import component-from-global-scope="Abt.DataTable" columns="{{cols}}" rows="{{rows}}" on-row-click="{{pick}}" caption="상품 목록"></x-import>
''' + SIDE_PANEL + '''<div style="display: flex; flex-direction: column; gap: 6px">
<div style="display: flex; align-items: center; justify-content: space-between; gap: 8px"><span style="font: 500 13px/20px var(--font-mono)">{{cur.code}}</span><x-import component-from-global-scope="Abt.StatusBadge" tone="{{cur.verTone}}" form="{{cur.verForm}}" size="md">{{cur.verLabel}}</x-import></div>
<h2 class="title-2" style="margin: 0">{{cur.name}}</h2>
<span class="caption" style="color: var(--ink-muted)">{{cur.type}} · {{cur.nights}}박 {{cur.days}}일 · 기본 판매가 {{cur.priceText}} KRW</span>
</div>
''' + dl([('지상비 기준', '{{cur.costText}}'), ('포함', '{{cur.incl}}'), ('불포함', '{{cur.excl}}')], 80) + '''<div style="display: flex; flex-direction: column">
''' + SUB.format('일정 템플릿') + '''
<sc-for list="{{cur.plan}}" as="d" hint-placeholder-count="4">
<div style="display: grid; grid-template-columns: 48px minmax(0, 1fr); gap: 12px; padding: 6px 0; border-top: 1px solid var(--line); font-size: 13px; line-height: 20px"><span style="color: var(--ink-muted)">{{d.k}}</span><span>{{d.v}}</span></div>
</sc-for>
</div>
<div style="display: flex; flex-direction: column">
''' + SUB.format('옵션') + '''
<sc-for list="{{cur.options}}" as="o" hint-placeholder-count="2">
<div style="''' + ROW + '''"><span>{{o.name}}</span><x-import component-from-global-scope="Abt.Money" amount="{{o.price}}" currency="MNT" size="sm"></x-import></div>
</sc-for>
</div>
<sc-if value="{{cur.hasDraft}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.Alert" tone="progress" title="{{cur.draftTitle}}">{{cur.draftBody}}</x-import>
</sc-if>
<div style="display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 8px">
<sc-if value="{{cur.canNew}}" hint-placeholder-val="{{true}}"><x-import component-from-global-scope="Abt.Button" on-click="{{newVersion}}">새 버전 만들기</x-import></sc-if>
<sc-if value="{{cur.hasDraft}}" hint-placeholder-val="{{false}}"><x-import component-from-global-scope="Abt.Button" variant="ghost" on-click="{{dropDraft}}">초안 삭제</x-import><x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{publish}}">새 버전 게시</x-import></sc-if>
</div>
</section>
</div>
'''
pre = '''
    const P = s.products;
    const cur = P.find((p) => p.code === s.selected) || P[0];
'''
vals = '''      cols: [
        { key: 'code', label: '상품코드', type: 'strong' },
        { key: 'name', label: '상품 / 유형', type: 'stack' },
        { key: 'len', label: '박/일', type: 'muted' },
        { key: 'price', label: '기본 판매가', type: 'money', currency: 'KRW' },
        { key: 'use', label: '진행·예정 행사', type: 'number', suffix: '건' },
        { key: 'ver', label: '버전', type: 'status' }
      ],
      rows: P.map((p) => ({ id: p.code, code: p.code, name: { primary: p.name, secondary: p.type }, len: `${p.nights}박 ${p.nights + 1}일`, price: p.price, use: p.use, ver: p.draft ? { tone: 'progress', form: 'dashed', status: `v${p.ver} · 새 버전 작성 중` } : { tone: 'neutral', status: `v${p.ver} 게시` }, selected: p.code === cur.code })),
      pick: (row) => set({ selected: row.id }),
      cur: { ...cur, days: cur.nights + 1, priceText: fmt(cur.price), costText: `1인 ${fmt(cur.per)} MNT + 차량·가이드 ${fmt(cur.fixed)} MNT · 2026 동계 요금표`, verLabel: cur.draft ? `v${cur.ver + 1} 초안` : `v${cur.ver} 게시`, verTone: cur.draft ? 'progress' : 'neutral', verForm: cur.draft ? 'dashed' : 'solid', hasDraft: !!cur.draft, canNew: !cur.draft, draftTitle: `v${cur.ver + 1} 초안 · 게시 전`, draftBody: `게시해도 이미 확정된 행사 ${cur.use}건은 v${cur.ver}를 그대로 씁니다. 게시 이후 새로 등록하는 행사부터 v${cur.ver + 1}이 적용됩니다.` },
      newVersion: () => this.setState({ products: P.map((p) => (p.code === cur.code ? { ...p, draft: true } : p)), notice: { tone: 'progress', title: `${cur.code} v${cur.ver + 1} 초안을 만들었습니다`, body: '일정 템플릿·포함/불포함·옵션을 고친 뒤 게시하세요.' } }),
      dropDraft: () => this.setState({ products: P.map((p) => (p.code === cur.code ? { ...p, draft: false } : p)), notice: null }),
      publish: () => this.setState({ products: P.map((p) => (p.code === cur.code ? { ...p, draft: false, ver: p.ver + 1 } : p)), notice: { tone: 'positive', title: `${cur.code} v${cur.ver + 1}을 게시했습니다`, body: `확정 행사 ${cur.use}건은 v${cur.ver} 그대로이고, 변경 이력에 남았습니다. 새 행사부터 v${cur.ver + 1}이 적용됩니다.` } }),'''
state = '''{ selected: 'GOBI-56', notice: null,
      products: [
        { code: 'GOBI-56', name: '고비 사막 5박 6일', type: '자연·사막', nights: 5, price: 1150000, per: 1800000, fixed: 9500000, use: 3, ver: 3, incl: '국내선 1회, 숙박 5박, 전 일정 식사, 차량·유류, 한국어 가이드, 입장료', excl: '국제선, 개인 경비, 승마·낙타 외 옵션, 여행자 보험', plan: [ { k: '1일차', v: '울란바토르 도착 → 국내선 달란자드가드 · 캠프' }, { k: '2일차', v: '욜링암 협곡 트레킹 · 별 관측' }, { k: '3일차', v: '홍고린 엘스 모래언덕 · 낙타 체험' }, { k: '4일차', v: '바얀자그(불타는 절벽)' }, { k: '5일차', v: '육로 이동 → 울란바토르 · 호텔' }, { k: '6일차', v: '시내 관광 · 송별 만찬 · 출국' } ], options: [ { name: '낙타 체험 1시간', price: 45000 }, { name: '승마 1시간', price: 60000 }, { name: '전통 공연 관람', price: 45000 } ] },
        { code: 'TRJ-GOLF-34', name: '테를지 골프 3박 4일', type: '골프', nights: 3, price: 1600000, per: 2700000, fixed: 4200000, use: 2, ver: 2, incl: '숙박 3박, 그린피 3라운드, 카트, 식사, 차량, 가이드', excl: '캐디피, 국제선, 개인 경비', plan: [ { k: '1일차', v: '도착 · 테를지 이동 · 리조트' }, { k: '2일차', v: '스카이 리조트 18홀' }, { k: '3일차', v: '18홀 · 테를지 국립공원' }, { k: '4일차', v: '9홀 · 출국' } ], options: [ { name: '추가 라운드 9홀', price: 180000 }, { name: '전통 공연 관람', price: 45000 } ] },
        { code: 'KHS-67', name: '홉스골 호수 6박 7일', type: '자연·호수', nights: 6, price: 1350000, per: 2200000, fixed: 13400000, use: 3, ver: 2, incl: '국내선 왕복, 숙박 6박, 식사, 차량, 가이드', excl: '국제선, 보트·승마, 개인 경비', plan: [ { k: '1일차', v: '도착 · 국내선 무릉' }, { k: '2일차', v: '하트갈 · 호숫가 캠프' }, { k: '3–5일차', v: '호수 트레킹 · 순록 마을 · 보트' }, { k: '6일차', v: '무릉 → 울란바토르' }, { k: '7일차', v: '시내 · 출국' } ], options: [ { name: '보트 투어', price: 70000 }, { name: '승마 2시간', price: 100000 } ] },
        { code: 'UB-CITY-34', name: '울란바토르 시티 3박 4일', type: '도시', nights: 3, price: 1100000, per: 1800000, fixed: 4500000, use: 3, ver: 4, incl: '숙박 3박, 식사, 차량, 가이드, 입장료', excl: '국제선, 개인 경비', plan: [ { k: '1일차', v: '도착 · 자이승 전망대' }, { k: '2일차', v: '간단 사원 · 국립박물관' }, { k: '3일차', v: '테를지 당일 · 거북바위' }, { k: '4일차', v: '시장 · 출국' } ], options: [ { name: '전통 공연 관람', price: 45000 }, { name: '캐시미어 공장 방문', price: 0 } ] },
        { code: 'INC-45', name: '기업 인센티브 4박 5일', type: '기업 단체', nights: 4, price: 1700000, per: 2900000, fixed: 13900000, use: 1, ver: 1, incl: '5성 호텔, 만찬 2회, 전용 버스, 가이드 2명', excl: '국제선, 개인 경비, 행사 장비', plan: [ { k: '1일차', v: '도착 · 환영 만찬' }, { k: '2일차', v: '테를지 · 게르 체험' }, { k: '3일차', v: '팀 빌딩 · 승마' }, { k: '4일차', v: '시내 · 갈라 디너' }, { k: '5일차', v: '출국' } ], options: [ { name: '갈라 디너 공연', price: 1500000 } ] },
        { code: 'TRJ-HORSE-23', name: '테를지 승마·게르 2박 3일', type: '체험', nights: 2, price: 1100000, per: 1700000, fixed: 4700000, use: 1, ver: 2, incl: '게르 2박, 승마 2회, 식사, 차량, 가이드', excl: '국제선, 개인 경비', plan: [ { k: '1일차', v: '도착 · 테를지 게르' }, { k: '2일차', v: '승마 트레킹 · 유목민 방문' }, { k: '3일차', v: '거북바위 · 출국' } ], options: [ { name: '활쏘기 체험', price: 30000 } ] }
      ] }'''
admin('Products.dc.html', '상품', 'products', 'ops', body, pre=pre, vals=vals, state=state, height=1000)
print('Products written')


# ------------------------------------------------------------------ Partners (협력업체·요금표)
body = header('협력업체·요금표', '호텔·캠프·식당·관광지·차량업체 · 시즌별 단가·통화·적용 기간 · 비용 입력 때 계약 단가와 자동 비교합니다',
              '<x-import component-from-global-scope="Abt.Segmented" options="{{kindOptions}}" value="{{kind}}" on-change="{{setKind}}" aria-label="업체 구분"></x-import>')
body += NOTICE
body += TWO_PANE + '''
<x-import component-from-global-scope="Abt.DataTable" columns="{{cols}}" rows="{{rows}}" on-row-click="{{pick}}" caption="협력업체 목록" empty="이 구분의 업체가 없습니다."></x-import>
''' + SIDE_PANEL + '''<div style="display: flex; flex-direction: column; gap: 6px">
<div style="display: flex; align-items: center; justify-content: space-between; gap: 8px"><span class="caption" style="color: var(--ink-muted)">{{cur.kind}} · {{cur.area}}</span><sc-if value="{{cur.repeat}}" hint-placeholder-val="{{false}}"><x-import component-from-global-scope="Abt.StatusBadge" axis="risk" status="repeat" size="md"></x-import></sc-if></div>
<h2 class="title-2" style="margin: 0">{{cur.name}}</h2>
<span class="caption" style="color: var(--ink-muted)">{{cur.contact}}</span>
</div>
<x-import component-from-global-scope="Abt.Segmented" size="sm" options="{{seasonOptions}}" value="{{season}}" on-change="{{setSeason}}" aria-label="요금표 시즌"></x-import>
<div style="display: flex; flex-direction: column">
<div style="display: flex; align-items: baseline; justify-content: space-between; gap: 8px; padding-bottom: 4px"><span class="label" style="color: var(--ink-muted)">{{rate.title}}</span><x-import component-from-global-scope="Abt.StatusBadge" tone="{{rate.tone}}" form="{{rate.form}}">{{rate.state}}</x-import></div>
<sc-for list="{{rate.items}}" as="r" hint-placeholder-count="3">
<div style="''' + ROW + '''"><span style="display: flex; flex-direction: column; gap: 2px"><span>{{r.item}}</span><span class="caption" style="color: var(--ink-muted)">{{r.unit}}</span></span><x-import component-from-global-scope="Abt.Money" amount="{{r.price}}" currency="{{r.cur}}" size="sm"></x-import></div>
</sc-for>
</div>
<sc-if value="{{cur.isVehicle}}" hint-placeholder-val="{{false}}">
<div style="display: flex; flex-direction: column; gap: 8px; padding: 12px; border: 1px solid var(--line); border-radius: 6px">
<span class="body-strong" style="font-size: 13px">유류비 예상</span>
<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px">
<x-import component-from-global-scope="Abt.Select" label="차종" size="sm" options="{{carOptions}}" value="{{car}}" on-change="{{setCar}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="거리" size="sm" suffix="km" align="end" input-mode="numeric" value="{{km}}" on-change="{{setKm}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="실제 지출" size="sm" suffix="MNT" align="end" input-mode="numeric" value="{{spent}}" on-change="{{setSpent}}"></x-import>
</div>
<p class="caption" style="margin: 0; color: var(--ink-muted)">{{fuel.text}}</p>
<x-import component-from-global-scope="Abt.BudgetBar" label="예상 대비 실제" budget="{{fuel.expected}}" actual="{{fuel.actual}}" currency="MNT"></x-import>
</div>
</sc-if>
<sc-if value="{{cur.hasNote}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.Alert" tone="attention" title="{{cur.noteTitle}}" action="{{cur.noteAction}}">{{cur.noteBody}}</x-import>
</sc-if>
<div style="display: flex; justify-content: flex-end; gap: 8px">
<x-import component-from-global-scope="Abt.Button" on-click="{{newRate}}">{{newRateLabel}}</x-import>
</div>
</section>
</div>
'''
pre = '''
    const P = [
      { id: 'p1', name: '고비 오아시스 캠프', kind: '숙박', area: '남고비 · 달란자드가드', contact: '바트바야르 매니저 · +976 9909-1180', contract: '2026 연간 계약', uses: 9, claims: 3, repeat: true, note: { title: '반복 클레임 3건(90일)', body: '온수 2건·식사 1건 · 책임 확인 1건. 거래 조건 검토 대상입니다.', action: { label: '클레임', href: 'Claims.dc.html' } },
        rates: { summer: { title: '2026 하계 v3 · 05.01–09.30', items: [ { item: '게르 1동 1박(2인)', unit: '조식 포함', price: 380000, cur: 'MNT' }, { item: '석식', unit: '1인', price: 25000, cur: 'MNT' }, { item: '중식 도시락', unit: '1인', price: 15000, cur: 'MNT' } ] }, winter: { title: '2026 동계 v1 · 10.01–04.30', items: [ { item: '게르 1동 1박(2인)', unit: '조식 포함', price: 300000, cur: 'MNT' }, { item: '석식', unit: '1인', price: 22000, cur: 'MNT' }, { item: '중식 도시락', unit: '1인', price: 14000, cur: 'MNT' } ] } } },
      { id: 'p2', name: '고비모터스', kind: '차량', area: '울란바토르', contact: '에르덴 대표 · +976 8811-2034', contract: '2026 연간 계약', uses: 14, claims: 2, repeat: true, vehicle: true, note: { title: '단가 차이 · 10월 청구', body: '10월 운행에 하계 단가 420,000 MNT/일을 청구했습니다. 동계 계약 단가는 400,000 MNT/일입니다.', action: { label: '과입·차감', href: 'Balance.dc.html' } },
        rates: { summer: { title: '2026 하계 v2 · 05.01–09.30', items: [ { item: '푸르공 1일(기사 포함)', unit: '대·일', price: 420000, cur: 'MNT' }, { item: '랜드크루저 1일', unit: '대·일', price: 520000, cur: 'MNT' }, { item: '45인승 버스 1일', unit: '대·일', price: 950000, cur: 'MNT' } ] }, winter: { title: '2026 동계 v1 · 10.01–04.30', items: [ { item: '푸르공 1일(기사 포함)', unit: '대·일', price: 400000, cur: 'MNT' }, { item: '랜드크루저 1일', unit: '대·일', price: 500000, cur: 'MNT' }, { item: '45인승 버스 1일', unit: '대·일', price: 900000, cur: 'MNT' } ] } } },
      { id: 'p3', name: '테를지 리버 캠프', kind: '숙박', area: '테를지', contact: '수렌 매니저 · +976 9191-4470', contract: '2026 연간 계약', uses: 12, claims: 0,
        rates: { summer: { title: '2026 하계 v2 · 05.01–09.30', items: [ { item: '게르 1동 1박(2인)', unit: '조식 포함', price: 320000, cur: 'MNT' }, { item: '조식 추가', unit: '1인', price: 30000, cur: 'MNT' } ] }, winter: { title: '2026 동계 v1 · 10.01–04.30', items: [ { item: '게르 1동 1박(2인)', unit: '조식 포함', price: 260000, cur: 'MNT' }, { item: '조식 추가', unit: '1인', price: 28000, cur: 'MNT' } ] } } },
      { id: 'p4', name: '블루스카이 호텔', kind: '숙박', area: '울란바토르', contact: '예약실 · +976 7010-0505', contract: '연간 기업 요금', uses: 15, claims: 0,
        rates: { summer: { title: '2026 연간 v3 · 01.01–12.31', items: [ { item: '트윈 1실 1박', unit: '조식 포함', price: 95, cur: 'USD' }, { item: '싱글 1실 1박', unit: '조식 포함', price: 85, cur: 'USD' } ] }, winter: { title: '2026 연간 v3 · 01.01–12.31', items: [ { item: '트윈 1실 1박', unit: '조식 포함', price: 95, cur: 'USD' }, { item: '싱글 1실 1박', unit: '조식 포함', price: 85, cur: 'USD' } ] } } },
      { id: 'p5', name: '서울가든', kind: '식당', area: '울란바토르', contact: '김정훈 사장 · +976 9900-8282', contract: '단체 메뉴 계약', uses: 21, claims: 0,
        rates: { summer: { title: '2026 연간 v2', items: [ { item: '한식 단체 만찬', unit: '1인', price: 90000, cur: 'MNT' }, { item: '한식 점심', unit: '1인', price: 45000, cur: 'MNT' } ] }, winter: { title: '2026 연간 v2', items: [ { item: '한식 단체 만찬', unit: '1인', price: 90000, cur: 'MNT' }, { item: '한식 점심', unit: '1인', price: 45000, cur: 'MNT' } ] } } },
      { id: 'p6', name: '국립박물관', kind: '관광지', area: '울란바토르', contact: '단체 예약 · +976 7011-0913', contract: '공시 요금', uses: 18, claims: 0,
        rates: { summer: { title: '2026 공시 요금', items: [ { item: '성인 입장', unit: '1인', price: 30000, cur: 'MNT' }, { item: '사진 촬영권', unit: '1인', price: 10000, cur: 'MNT' } ] }, winter: { title: '2026 공시 요금', items: [ { item: '성인 입장', unit: '1인', price: 30000, cur: 'MNT' }, { item: '사진 촬영권', unit: '1인', price: 10000, cur: 'MNT' } ] } } }
    ];
    const kind = s.kind;
    const list = kind === '전체' ? P : P.filter((p) => p.kind === kind);
    const cur = P.find((p) => p.id === s.selected) || P[0];
    const rt = cur.rates[s.season];
    const drafts = s.drafts || {};
    const CARS = { '푸르공': 18, '랜드크루저': 14, '45인승 버스': 30 };
    const L = CARS[s.car] || 18;
    const km = Number(String(s.km).replace(/[^0-9]/g, '')) || 0;
    const expected = Math.round(km * L / 100 * 3000);
    const actual = Number(String(s.spent).replace(/[^0-9]/g, '')) || 0;
'''
vals = '''      kindOptions: ['전체', '숙박', '식당', '차량', '관광지'],
      kind,
      setKind: (v) => set({ kind: v }),
      cols: [
        { key: 'name', label: '업체 / 구분', type: 'stack' },
        { key: 'area', label: '지역', type: 'muted' },
        { key: 'contract', label: '계약', type: 'muted' },
        { key: 'uses', label: '이용(90일)', type: 'number', suffix: '건' },
        { key: 'claims', label: '클레임', type: 'number', suffix: '건' },
        { key: 'flags', label: '검토 후보', type: 'flags' }
      ],
      rows: list.map((p) => ({ id: p.id, name: { primary: p.name, secondary: p.kind }, area: p.area, contract: p.contract, uses: p.uses, claims: p.claims, flags: p.repeat ? ['repeat'] : [], selected: p.id === cur.id })),
      pick: (row) => set({ selected: row.id }),
      seasonOptions: [ { value: 'winter', label: '동계 · 적용 중' }, { value: 'summer', label: '하계' } ],
      season: s.season,
      setSeason: (v) => set({ season: v }),
      rate: { ...rt, state: drafts[cur.id] && s.season === 'winter' ? '새 버전 승인 대기' : s.season === 'winter' ? '적용 중' : '기간 종료', tone: drafts[cur.id] && s.season === 'winter' ? 'progress' : s.season === 'winter' ? 'positive' : 'neutral', form: drafts[cur.id] && s.season === 'winter' ? 'dashed' : 'solid' },
      cur: { ...cur, isVehicle: !!cur.vehicle, repeat: !!cur.repeat, hasNote: !!cur.note, noteTitle: cur.note ? cur.note.title : '', noteBody: cur.note ? cur.note.body : '', noteAction: cur.note ? cur.note.action : null },
      carOptions: Object.keys(CARS),
      car: s.car,
      setCar: (e) => set({ car: e.target.value }),
      km: s.km,
      setKm: (e) => set({ km: e.target.value }),
      spent: s.spent,
      setSpent: (e) => set({ spent: e.target.value }),
      fuel: { expected, actual, text: `${s.car} ${L} L/100km × ${fmt(km)} km × AI-92 3,000 MNT/L = 예상 ${fmt(expected)} MNT` },
      newRateLabel: drafts[cur.id] ? '승인 요청 취소' : '요금표 새 버전',
      newRate: () => (drafts[cur.id] ? set({ drafts: { ...drafts, [cur.id]: false }, notice: null }) : this.setState({ drafts: { ...drafts, [cur.id]: true }, season: 'winter', notice: { tone: 'progress', title: `${cur.name} 동계 v2 초안을 만들고 승인을 요청했습니다`, body: '적용 시작일 11.01 · 승인 전까지 지금 요금표가 그대로 쓰입니다. 바뀐 단가는 그날 이후 비용 입력부터 비교에 쓰입니다.' } })),'''
state = "{ kind: '전체', selected: 'p2', season: 'winter', car: '푸르공', km: '1400', spent: '780000', drafts: {}, notice: null }"
admin('Partners.dc.html', '협력업체·요금표', 'partners', 'ops', body, pre=pre, vals=vals, state=state, height=1080)
print('Partners written')
