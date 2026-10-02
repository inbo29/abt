import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import *

ROW = 'display: grid; grid-template-columns: minmax(0, 1fr) auto; align-items: baseline; gap: 12px; padding: 8px 0; border-top: 1px solid var(--line); font-size: 13px; line-height: 20px'

# ------------------------------------------------------------------ Receipts (입금)
body = header('입금', '여행사 청구와 실제 통장 입금을 따로 기록합니다 · 예상 잔금만으로 입금 완료 처리하지 않습니다 · 입금은 행사별로 배분합니다', '''<x-import component-from-global-scope="Abt.Button" variant="secondary" on-click="{{exportXls}}">엑셀 다운로드</x-import>
<x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{toggleNew}}">{{newLabel}}</x-import>''')
body += NOTICE
body += '''<section aria-label="입금 지표" style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px">
<x-import component-from-global-scope="Abt.KpiTile" label="미수 합계" money="{{kpi.rest}}" state="attention" state-label="{{kpi.restLabel}}" caption="{{kpi.restCaption}}"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="연체" money="{{kpi.overdue}}" state="{{kpi.overdueState}}" state-label="{{kpi.overdueLabel}}" caption="{{kpi.overdueCaption}}"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="미배분 입금" money="{{kpi.unalloc}}" caption="{{kpi.unallocCaption}}"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="과입·환불 대기" money="{{kpi.over}}" caption="한빛투어 과입 · 다온여행사 취소 환불" href="Balance.dc.html" link-label="과입·차감"></x-import>
</section>

<sc-if value="{{creating}}" hint-placeholder-val="{{false}}">
''' + PANEL + panel_title('입금 등록', '통장에 실제로 들어온 금액을 그대로 적고, 어느 행사의 계약금·잔금인지 배분합니다') + field_grid(170) + '''
<x-import component-from-global-scope="Abt.TextField" label="입금일" type="date" value="{{nf.date}}" on-change="{{onNf.date}}"></x-import>
<x-import component-from-global-scope="Abt.Select" label="입금자" options="{{agencyOptions}}" value="{{nf.payer}}" on-change="{{onNf.payer}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="입금액" required="{{yes}}" input-mode="numeric" align="end" suffix="KRW" value="{{nf.amount}}" on-change="{{onNf.amount}}" error="{{nfErr.amount}}"></x-import>
<x-import component-from-global-scope="Abt.Select" label="입금 계좌" options="{{bankOptions}}" value="{{nf.bank}}" on-change="{{onNf.bank}}"></x-import>
</div>
<x-import component-from-global-scope="Abt.Select" label="배분 대상" required="{{yes}}" options="{{targetOptions}}" value="{{nf.target}}" on-change="{{onNf.target}}" error="{{nfErr.target}}" help="{{targetHelp}}"></x-import>
<div style="display: flex; align-items: center; justify-content: space-between; gap: 12px">
<x-import component-from-global-scope="Abt.Attachment" kind="proof" name="입금내역_캡처.png" meta="0.3 MB"></x-import>
<div style="display: flex; gap: 8px">
<x-import component-from-global-scope="Abt.Button" variant="ghost" on-click="{{toggleNew}}">취소</x-import>
<x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{submitNew}}">입금 등록</x-import>
</div>
</div>
</section>
</sc-if>

<x-import component-from-global-scope="Abt.Tabs" items="{{tabs}}" value="{{tab}}" on-change="{{setTab}}" aria-label="입금 보기"></x-import>

<sc-if value="{{isAr}}" hint-placeholder-val="{{true}}">
<div style="display: grid; grid-template-columns: minmax(0, 1fr) 360px; gap: 16px; align-items: start">

<x-import component-from-global-scope="Abt.DataTable" columns="{{arCols}}" rows="{{arRows}}" totals="{{arTotals}}" on-row-click="{{pick}}" caption="청구와 미수"></x-import>
''' + SIDE_PANEL + '''<div style="display: flex; flex-direction: column; gap: 8px">
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 8px">
<x-import component-from-global-scope="Abt.EventCode" code="{{cur.code}}" href="EventDetail.dc.html" size="md"></x-import>
<x-import component-from-global-scope="Abt.StatusBadge" axis="payment" status="{{cur.status}}" size="md"></x-import>
</div>
<h2 class="title-2" style="margin: 0">{{cur.agency}} · {{cur.product}}</h2>
<p class="caption" style="margin: 0; color: var(--ink-muted)">{{cur.terms}}</p>
</div>
<div style="display: flex; flex-direction: column">
<sc-for list="{{cur.lines}}" as="l" hint-placeholder-count="4">
<div style="''' + ROW + '''"><span style="display: flex; flex-direction: column; gap: 2px"><span>{{l.label}}</span><span class="caption" style="color: var(--ink-muted)">{{l.sub}}</span></span><x-import component-from-global-scope="Abt.Money" amount="{{l.amount}}" currency="KRW" kind="{{l.kind}}" size="sm"></x-import></div>
</sc-for>
<div style="''' + ROW + '''; font-weight: 600"><span>남은 금액</span><x-import component-from-global-scope="Abt.Money" amount="{{cur.rest}}" currency="KRW"></x-import></div>
</div>
<sc-if value="{{cur.isOverdue}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.Alert" tone="critical" title="{{cur.overdueTitle}}" action="{{remindAction}}">{{cur.overdueBody}}</x-import>
</sc-if>
<sc-if value="{{cur.hasNote}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.Alert" tone="progress" title="{{cur.noteTitle}}" action="{{cur.noteAction}}">{{cur.noteBody}}</x-import>
</sc-if>
<div style="display: flex; justify-content: flex-end; gap: 8px">
<sc-if value="{{cur.hasRest}}" hint-placeholder-val="{{true}}">
<x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{payThis}}">이 행사로 입금 등록</x-import>
</sc-if>
</div>
</section>
</div>
</sc-if>

<sc-if value="{{isDep}}" hint-placeholder-val="{{false}}">
<sc-for list="{{unallocated}}" as="u" hint-placeholder-count="1">
<x-import component-from-global-scope="Abt.Alert" tone="attention" title="{{u.title}}" action="{{u.action}}">{{u.body}}</x-import>
</sc-for>
<x-import component-from-global-scope="Abt.DataTable" columns="{{depCols}}" rows="{{depRows}}" caption="입금 내역"></x-import>
<p class="caption" style="margin: 0; color: var(--ink-muted)">입금 1건을 여러 행사에 나눠 배분할 수 있습니다 · 청구액보다 많이 들어온 돈은 과입으로 잔액 원장에 남습니다</p>
</sc-if>
'''

pre = '''
    const AR = s.ar;
    const cur = AR.find((r) => r.id === s.selected) || AR[0];
    const restOf = (r) => r.billed - r.paid;
    const statusOf = (r) => (r.cancelled ? 'paid' : restOf(r) <= 0 ? 'paid' : r.overdue ? 'overdue' : r.dueSoon ? 'due-soon' : r.paid > 0 ? 'partial' : 'billed');
    const open = AR.filter((r) => restOf(r) > 0);
    const totalRest = open.reduce((a, r) => a + restOf(r), 0);
    const overdue = open.filter((r) => r.overdue);
    const DEP = s.deps;
    const unalloc = DEP.filter((d) => !d.to);
    const nf = s.nf;
    const num = (v) => Number(String(v || '').replace(/[^0-9]/g, '')) || 0;
    const NOW = '10.01 16:00 KST';
    const applyPay = (arId, amount, depPatch) => {
      const r = AR.find((x) => x.id === arId);
      const rest = restOf(r);
      const use = Math.min(rest, amount);
      const over = amount - use;
      const ar2 = AR.map((x) => (x.id === arId ? { ...x, paid: x.paid + use, history: (x.history || []).concat([{ label: `입금 ${NOW.slice(0, 5)}`, sub: depPatch.sub, amount: use }]) } : x));
      return { ar2, use, over, r };
    };
'''
vals = '''      user: { name: '박서연', role: '회계담당자' },
      navCounts: { alerts: 5, field: 2, claims: { n: 2, tone: 'critical' }, receipts: overdue.length ? { n: overdue.length, tone: 'critical' } : undefined, costs: { n: 7, tone: 'attention' }, remit: 3 },
      kpi: {
        rest: { amount: totalRest, currency: 'KRW', compact: false },
        restLabel: `${open.length}건`,
        restCaption: '판매·청구 기준 · 실제 입금과 차이',
        overdue: { amount: overdue.reduce((a, r) => a + restOf(r), 0), currency: 'KRW', compact: false },
        overdueState: overdue.length ? 'critical' : undefined,
        overdueLabel: overdue.length ? `${overdue.length}건 · 09.30 기한` : '',
        overdueCaption: overdue.length ? '다온여행사 · 담당자 재알림 2회' : '연체 없음',
        unalloc: { amount: unalloc.reduce((a, d) => a + d.amount, 0), currency: 'KRW', compact: false },
        unallocCaption: unalloc.length ? `${unalloc.length}건 · 어느 행사 돈인지 배분 필요` : '모두 배분됨',
        over: { amount: s.overTotal, currency: 'KRW', compact: false }
      },
      exportXls: () => say('positive', '입금·미수 원장을 내려받았습니다', '청구액과 입금액을 다른 열로 담았습니다. 기준일 10.01 · 통화 KRW.'),
      creating: !!s.creating,
      newLabel: s.creating ? '입력 닫기' : '입금 등록',
      toggleNew: () => set({ creating: !s.creating, nfErr: {} }),
      agencyOptions: ['푸른하늘여행', '한빛투어', '다온여행사', '누리투어', '제이원트래블', '솔빛여행'],
      bankOptions: ['기업은행 ··· 2041 (원화)', '신한은행 ··· 7730 (외화)'],
      targetOptions: [{ value: '', label: '선택하세요' }].concat(open.map((r) => ({ value: r.id, label: `${r.code} · ${r.agency} · ${r.kind} 잔액 ${fmt(restOf(r))} KRW` }))),
      targetHelp: nf.target ? (() => { const r = AR.find((x) => x.id === nf.target); const a = num(nf.amount); return a > restOf(r) ? `잔액보다 ${fmt(a - restOf(r))} KRW 많습니다 · 초과분은 과입으로 잔액 원장에 남습니다` : `배분 후 잔액 ${fmt(restOf(r) - a)} KRW`; })() : '미수가 남은 행사만 고를 수 있습니다',
      nf,
      onNf: { date: (e) => set({ nf: { ...s.nf, date: e.target.value } }), payer: (e) => set({ nf: { ...s.nf, payer: e.target.value } }), amount: (e) => set({ nf: { ...s.nf, amount: e.target.value }, nfErr: {} }), bank: (e) => set({ nf: { ...s.nf, bank: e.target.value } }), target: (e) => set({ nf: { ...s.nf, target: e.target.value }, nfErr: {} }) },
      nfErr: s.nfErr || {},
      submitNew: () => {
        const a = num(nf.amount);
        const er = { amount: a > 0 ? '' : '입금액을 입력하세요.', target: nf.target ? '' : '배분할 행사를 고르세요.' };
        if (er.amount || er.target) { set({ nfErr: er }); return; }
        const { ar2, use, over, r } = applyPay(nf.target, a, { sub: `${nf.payer} · ${nf.bank.split(' (')[0]}` });
        const dep = { id: 'd' + (DEP.length + 1), at: `${nf.date.slice(5).replace('-', '.')} 16:00`, payer: nf.payer, amount: a, bank: nf.bank.split(' (')[0], to: `${r.code} ${r.kind}`, over };
        this.setState({ ar: ar2, deps: [dep].concat(DEP), creating: false, selected: r.id, overTotal: s.overTotal + over, nf: { ...nf, amount: '', target: '' }, notice: { tone: over ? 'attention' : 'positive', title: `${r.code} ${r.kind}에 ${fmt(use)} KRW 배분했습니다`, body: over ? `청구 잔액보다 ${fmt(over)} KRW 많이 들어왔습니다. 초과분은 과입으로 잔액 원장에 남겨 상계하거나 환불합니다.` : restOf(r) - use > 0 ? `남은 금액 ${fmt(restOf(r) - use)} KRW · 부분 입금으로 표시됩니다.` : '잔액이 0이 되어 입금 완료로 바뀌었습니다.', action: over ? { label: '과입·차감', href: 'Balance.dc.html' } : null } });
      },
      tabs: [ { id: 'ar', label: '청구·미수', count: open.length }, { id: 'dep', label: '입금 내역', count: unalloc.length ? unalloc.length : undefined, tone: unalloc.length ? 'attention' : undefined } ],
      tab: s.tab,
      setTab: (id) => set({ tab: id }),
      isAr: s.tab === 'ar',
      isDep: s.tab === 'dep',
      arCols: [
        { key: 'code', label: '행사코드', type: 'code' },
        { key: 'who', label: '여행사 / 기한', type: 'stack' },
        { key: 'billed', label: '청구액', type: 'money', currency: 'KRW' },
        { key: 'paid', label: '입금액', type: 'money', currency: 'KRW' },
        { key: 'rest', label: '잔액', type: 'money', currency: 'KRW' },
        { key: 'status', label: '상태', type: 'status', axis: 'payment' }
      ],
      arRows: AR.map((r) => ({ id: r.id, code: r.code, href: 'EventDetail.dc.html', who: { primary: r.agency, secondary: `${r.kind} · ${r.due}` }, billed: r.billed, paid: r.paid, rest: restOf(r) > 0 ? restOf(r) : 0, status: statusOf(r), selected: r.id === cur.id, dim: r.cancelled })),
      arTotals: { label: '합계', billed: AR.reduce((a, r) => a + r.billed, 0), paid: AR.reduce((a, r) => a + r.paid, 0), rest: totalRest },
      pick: (row) => set({ selected: row.id }),
      cur: { ...cur, status: statusOf(cur), rest: Math.max(0, restOf(cur)), hasRest: restOf(cur) > 0, isOverdue: !!cur.overdue && restOf(cur) > 0, overdueTitle: `기한 09.30 경과 · ${fmt(restOf(cur))} KRW 미입금`, overdueBody: s.reminded ? `${NOW} 미수 안내를 다시 보냈습니다. 3일 안에 입금이 없으면 대표에게 보고됩니다.` : '담당자 재알림 2회(09.30, 10.01). 송금은 이미 끝나 이 행사는 미수가 풀릴 때까지 적자로 집계됩니다.', lines: [ { label: '청구액', sub: cur.kind, amount: cur.billed, kind: 'expected' } ].concat((cur.history || []).map((h) => ({ label: h.label, sub: h.sub, amount: h.amount, kind: 'actual' }))), hasNote: !!cur.note, noteTitle: cur.note ? cur.note.title : '', noteBody: cur.note ? cur.note.body : '', noteAction: cur.note ? cur.note.action : null },
      remindAction: { label: s.reminded ? '안내 보냄' : '미수 안내 보내기', onClick: () => set({ reminded: true, notice: { tone: 'progress', title: '다온여행사에 미수 안내를 보냈습니다', body: '담당자 이메일과 알림으로 청구서·입금 계좌를 다시 보냈습니다. 감사 로그에 남습니다.' } }) },
      payThis: () => set({ creating: true, nf: { ...nf, target: cur.id, payer: cur.agency, amount: String(restOf(cur)) }, nfErr: {} }),
      unallocated: unalloc.map((d) => ({ title: `미배분 입금 · ${d.payer} ${fmt(d.amount)} KRW (${d.at})`, body: `${d.bank} · 입금자명 「${d.payer}」 · 누리투어 미수는 MN2610-012 잔금 ${fmt(restOf(AR.find((x) => x.code === 'MN2610-012')))} KRW 하나입니다.`, action: { label: 'MN2610-012에 배분', onClick: () => { const { ar2 } = applyPay('a4', d.amount, { sub: `${d.payer} · ${d.bank}` }); this.setState({ ar: ar2, deps: DEP.map((x) => (x.id === d.id ? { ...x, to: 'MN2610-012 잔금' } : x)), notice: { tone: 'positive', title: `${fmt(d.amount)} KRW를 MN2610-012 잔금에 배분했습니다`, body: '미배분 입금이 없어졌고 미수 잔액이 줄었습니다.' } }); } } })),
      depCols: [
        { key: 'at', label: '입금 시각(KST)' },
        { key: 'payer', label: '입금자', type: 'strong' },
        { key: 'amount', label: '입금액', type: 'money', currency: 'KRW' },
        { key: 'bank', label: '계좌', type: 'muted' },
        { key: 'to', label: '배분', type: 'stack' },
        { key: 'st', label: '상태', type: 'status' }
      ],
      depRows: DEP.map((d) => ({ id: d.id, at: d.at, payer: d.payer, amount: d.amount, bank: d.bank, to: d.to ? { primary: d.to, secondary: d.over ? `과입 ${fmt(d.over)} KRW → 잔액 원장` : '' } : { primary: '—', secondary: '배분 필요' }, st: d.to ? { tone: 'positive', status: '배분 완료' } : { tone: 'attention', status: '미배분' } })),'''

state = '''{ tab: 'ar', selected: 'a1', creating: false, reminded: false, nfErr: {}, notice: null, overTotal: 2510000,
      nf: { date: '2026-10-01', payer: '솔빛여행', amount: '', bank: '기업은행 ··· 2041 (원화)', target: '' },
      ar: [
        { id: 'a1', code: 'MN2609-031', agency: '다온여행사', product: '홉스골 호수 6박 7일', kind: '잔금', due: '09.30(수)', dueNote: '1일 경과', billed: 32400000, paid: 20000000, overdue: true, terms: '판매금액 32,400,000 KRW · 계약금 없이 잔금 일괄 · 출발 후 4일 기한', history: [ { label: '입금 09.25', sub: '다온여행사 · 기업은행', amount: 20000000 } ] },
        { id: 'a2', code: 'MN2609-040', agency: '솔빛여행', product: '울란바토르 시티 3박 4일', kind: '잔금', due: '10.02(금)', dueNote: '내일', billed: 9900000, paid: 4950000, dueSoon: true, terms: '판매금액 9,900,000 KRW · 계약금 50% 입금(09.30)', history: [ { label: '계약금 09.30', sub: '솔빛여행 · 기업은행', amount: 4950000 } ] },
        { id: 'a3', code: 'MN2610-002', agency: '푸른하늘여행', product: '고비 사막 5박 6일', kind: '잔금', due: '10.02(금)', dueNote: '내일 · 출발일', billed: 20700000, paid: 10350000, dueSoon: true, terms: '판매금액 20,700,000 KRW · 계약금 50% 입금(09.29)', history: [ { label: '계약금 09.29', sub: '푸른하늘여행 · 기업은행', amount: 10350000 } ] },
        { id: 'a4', code: 'MN2610-012', agency: '누리투어', product: '기업 인센티브 4박 5일', kind: '잔금', due: '10.06(화)', dueNote: '5일 남음', billed: 54400000, paid: 33900000, terms: '판매금액 54,400,000 KRW · 계약금 30% + 중도금 입금', history: [ { label: '계약금 09.10', sub: '누리투어 · 기업은행', amount: 16320000 }, { label: '중도금 09.24', sub: '누리투어 · 기업은행', amount: 17580000 } ] },
        { id: 'a5', code: 'MN2610-005', agency: '한빛투어', product: '테를지 골프 3박 4일', kind: '잔금', due: '09.26(토)', dueNote: '완료', billed: 12800000, paid: 12800000, terms: '판매금액 12,800,000 KRW', history: [ { label: '입금 09.28', sub: '한빛투어 14,650,000 중 배분', amount: 12800000 } ], note: { title: '과입 1,850,000 KRW', body: '09.28 입금 14,650,000 KRW 중 남는 금액은 과입으로 잔액 원장에 있습니다.', action: { label: '과입·차감', href: 'Balance.dc.html' } } },
        { id: 'a6', code: 'MN2609-033', agency: '푸른하늘여행', product: '고비 사막 5박 6일', kind: '계약금+잔금', due: '09.15(화)', dueNote: '완료', billed: 23000000, paid: 23000000, terms: '판매금액 23,000,000 KRW · 계약금 30% · 잔금 70%', history: [ { label: '계약금 08.26', sub: '푸른하늘여행 · 기업은행', amount: 6900000 }, { label: '잔금 09.15', sub: '푸른하늘여행 · 기업은행', amount: 16100000 } ] },
        { id: 'a7', code: 'MN2610-024', agency: '다온여행사', product: '울란바토르 시티 3박 4일 (취소)', kind: '계약금 · 취소', due: '09.18(금)', dueNote: '취소 09.29', billed: 1980000, paid: 1980000, cancelled: true, terms: '판매금액 6,600,000 KRW · 계약금 30% 입금 후 취소 · 취소 수수료 20%(1,320,000 KRW)', history: [ { label: '계약금 09.17', sub: '다온여행사 · 기업은행', amount: 1980000 } ], note: { title: '취소 환불 대기 660,000 KRW', body: '계약금 1,980,000 − 취소 수수료 1,320,000. 환불하거나 같은 여행사 미수(MN2609-031)와 상계합니다.', action: { label: '과입·차감', href: 'Balance.dc.html' } } }
      ],
      deps: [
        { id: 'd8', at: '10.01 09:12', payer: '누리투어', amount: 3000000, bank: '기업은행 ··· 2041', to: null },
        { id: 'd7', at: '09.30 15:40', payer: '솔빛여행', amount: 4950000, bank: '기업은행 ··· 2041', to: 'MN2609-040 계약금' },
        { id: 'd6', at: '09.29 11:05', payer: '푸른하늘여행', amount: 10350000, bank: '기업은행 ··· 2041', to: 'MN2610-002 계약금' },
        { id: 'd5', at: '09.28 10:30', payer: '한빛투어', amount: 14650000, bank: '기업은행 ··· 2041', to: 'MN2610-005 잔금', over: 1850000 },
        { id: 'd4', at: '09.25 10:30', payer: '다온여행사', amount: 20000000, bank: '기업은행 ··· 2041', to: 'MN2609-031 잔금 일부' },
        { id: 'd3', at: '09.24 14:00', payer: '누리투어', amount: 17580000, bank: '기업은행 ··· 2041', to: 'MN2610-012 중도금' },
        { id: 'd2', at: '09.17 13:20', payer: '다온여행사', amount: 1980000, bank: '기업은행 ··· 2041', to: 'MN2610-024 계약금' },
        { id: 'd1', at: '09.15 11:00', payer: '푸른하늘여행', amount: 16100000, bank: '기업은행 ··· 2041', to: 'MN2609-033 잔금' }
      ] }'''
admin('Receipts.dc.html', '입금', 'receipts', None, body, pre=pre, vals=vals, state=state, height=1180)
print('Receipts written')


# ------------------------------------------------------------------ Balance (과입·차감 원장)
body = header('과입·차감', '거래처·행사·통화별 잔액 원장 · 발생 → 사용·상계·환불 순서로 기록하고 잔액이 0이 되면 닫습니다 · 부호: + 우리가 돌려줄 돈, − 받을 돈',
              '<x-import component-from-global-scope="Abt.Segmented" options="{{filterOptions}}" value="{{filter}}" on-change="{{setFilter}}" aria-label="잔액 구분"></x-import>')
body += NOTICE
body += '''<section aria-label="잔액 지표" style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px">
<x-import component-from-global-scope="Abt.KpiTile" label="여행사에 돌려줄 돈" money="{{kpi.payable}}" caption="과입·취소 환불 · KRW"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="업체에서 받을 돈" money="{{kpi.receivable}}" caption="보상·단가 차감 · MNT"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="상계 대기" value="{{kpi.offset}}" unit="건" caption="다음 청구·지급에서 정리"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="환불 대기" value="{{kpi.refund}}" unit="건" caption="계좌·증빙 확인 후 처리"></x-import>
</section>
''' + TWO_PANE + '''
<x-import component-from-global-scope="Abt.DataTable" columns="{{cols}}" rows="{{rows}}" on-row-click="{{pick}}" caption="잔액 원장" empty="해당하는 잔액이 없습니다."></x-import>
''' + SIDE_PANEL + '''<div style="display: flex; flex-direction: column; gap: 8px">
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 8px">
<span style="font: 500 13px/20px var(--font-mono)">{{cur.id}}</span>
<x-import component-from-global-scope="Abt.StatusBadge" tone="{{cur.tone}}" form="{{cur.form}}" size="md">{{cur.stLabel}}</x-import>
</div>
<h2 class="title-2" style="margin: 0">{{cur.party}} · {{cur.title}}</h2>
<x-import component-from-global-scope="Abt.Money" amount="{{cur.balance}}" currency="{{cur.cur}}" size="lg" align="start" sign="always"></x-import>
</div>
''' + dl([('관련 행사', '{{cur.event}}'), ('발생 사유', '{{cur.reason}}'), ('근거', '{{cur.proof}}')], 80) + '''<div style="display: flex; flex-direction: column">
<span class="label" style="color: var(--ink-muted); padding-bottom: 4px">원장</span>
<sc-for list="{{cur.lines}}" as="l" hint-placeholder-count="3">
<div style="''' + ROW + '''"><span style="display: flex; flex-direction: column; gap: 2px"><span>{{l.label}}</span><span class="caption" style="color: var(--ink-muted)">{{l.sub}}</span></span><x-import component-from-global-scope="Abt.Money" amount="{{l.amount}}" currency="{{cur.cur}}" size="sm" sign="always"></x-import></div>
</sc-for>
</div>
<sc-if value="{{cur.isOpen}}" hint-placeholder-val="{{true}}">
<div style="display: flex; flex-direction: column; gap: 12px; padding-top: 12px; border-top: 1px solid var(--line)">
<x-import component-from-global-scope="Abt.Select" label="처리 방법" options="{{cur.methods}}" value="{{method}}" on-change="{{setMethod}}" help="{{methodHelp}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="처리 근거" placeholder="예: 다온여행사 담당 확인 메일(10.01)" value="{{why}}" on-change="{{setWhy}}" error="{{whyError}}"></x-import>
<div style="display: flex; justify-content: flex-end"><x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{settle}}">{{settleLabel}}</x-import></div>
</div>
</sc-if>
</section>
</div>
'''

pre = '''
    const L = s.ledger;
    const bal = (e) => e.lines.reduce((a, l) => a + l.amount, 0);
    const filter = s.filter;
    const list = L.filter((e) => (filter === '잔액 있음' ? bal(e) !== 0 : filter === '정리됨' ? bal(e) === 0 : true));
    const cur = L.find((e) => e.id === s.selected) || L[0];
    const NOW = '10.01 16:05 KST';
    const M = cur.methods || [];
    const method = s.method && M.includes(s.method) ? s.method : M[0];
    const HELP = {
      'MN2609-031 미수와 상계': '다온여행사 MN2609-031 잔금 12,400,000 KRW에서 660,000 KRW를 뺍니다. 환불 송금은 생기지 않습니다.',
      '환불 송금': '여행사 계좌로 돌려보냅니다. 송금증을 붙여야 완료됩니다.',
      '다음 청구에서 차감(MN2610-031)': '11월 행사 계약금 청구서에 −1,850,000 KRW 줄로 들어갑니다.',
      '10월 지급에서 차감': '다음 캠프 지급 요청에서 같은 금액을 빼고 송금합니다.',
      '단가 확인 후 차감': '계약 단가가 맞으면 다음 지급에서 360,000 MNT를 뺍니다.'
    };
'''
vals = '''      user: { name: '박서연', role: '회계담당자' },
      filterOptions: ['잔액 있음', '정리됨', '전체'],
      filter,
      setFilter: (v) => set({ filter: v }),
      kpi: {
        payable: { amount: L.filter((e) => e.cur === 'KRW' && bal(e) > 0).reduce((a, e) => a + bal(e), 0), currency: 'KRW', compact: false },
        receivable: { amount: -L.filter((e) => e.cur === 'MNT' && bal(e) < 0).reduce((a, e) => a + bal(e), 0), currency: 'MNT', compact: false },
        offset: L.filter((e) => bal(e) !== 0 && e.plan === '상계').length,
        refund: L.filter((e) => bal(e) !== 0 && e.plan === '환불').length
      },
      cols: [
        { key: 'id', label: '번호', type: 'muted' },
        { key: 'party', label: '거래처 / 사유', type: 'stack' },
        { key: 'event', label: '행사', type: 'code' },
        { key: 'balance', label: '잔액', type: 'money' },
        { key: 'st', label: '상태', type: 'status' }
      ],
      rows: list.map((e) => { const b = bal(e); return { id: e.id, href: 'EventDetail.dc.html', party: { primary: e.party, secondary: e.title }, event: e.code, balance: { amount: b, currency: e.cur, sign: 'always' }, st: b === 0 ? { tone: 'neutral', status: '정리됨' } : { tone: e.plan === '환불' ? 'attention' : 'progress', form: 'dashed', status: `${e.plan} 대기` }, selected: e.id === cur.id, dim: b === 0 }; }),
      pick: (row) => set({ selected: row.id, method: null, why: '', whyError: '' }),
      cur: { ...cur, balance: bal(cur), isOpen: bal(cur) !== 0, stLabel: bal(cur) === 0 ? '정리됨' : `${cur.plan} 대기`, tone: bal(cur) === 0 ? 'neutral' : cur.plan === '환불' ? 'attention' : 'progress', form: bal(cur) === 0 ? 'solid' : 'dashed' },
      method,
      setMethod: (e) => set({ method: e.target.value }),
      methodHelp: HELP[method] || '',
      why: s.why,
      setWhy: (e) => set({ why: e.target.value, whyError: '' }),
      whyError: s.whyError || '',
      settleLabel: method && method.includes('환불') ? '환불 요청' : '상계 처리',
      settle: () => {
        if (!s.why.trim()) { set({ whyError: '처리 근거를 남겨야 합니다. 감사 로그에 같이 저장됩니다.' }); return; }
        const b = bal(cur);
        const line = { label: `${method.includes('환불') ? '환불' : '상계'} ${NOW.slice(0, 5)}`, sub: `${method} · ${s.why.trim()}`, amount: -b };
        this.setState({ ledger: L.map((e) => (e.id === cur.id ? { ...e, lines: e.lines.concat([line]) } : e)), why: '', method: null, notice: { tone: 'positive', title: `${cur.id} 잔액을 0으로 정리했습니다`, body: method === 'MN2609-031 미수와 상계' ? '다온여행사 MN2609-031 미수가 12,400,000 → 11,740,000 KRW로 줄었습니다.' : method.includes('환불') ? '회계 송금 대기열에 환불 1건이 올라갔습니다. 송금증을 붙이면 완료됩니다.' : '다음 청구·지급 때 차감되도록 연결했습니다.', action: method === 'MN2609-031 미수와 상계' ? { label: '입금 원장', href: 'Receipts.dc.html' } : null } });
      },'''

state = '''{ filter: '잔액 있음', selected: 'BL-1001', method: null, why: '', whyError: '', notice: null,
      ledger: [
        { id: 'BL-1001', party: '다온여행사', title: '취소 환불 대기', code: 'MN2610-024', event: 'MN2610-024 울란바토르 시티 · 09.29 취소', cur: 'KRW', plan: '환불', reason: '계약금 1,980,000 − 취소 수수료 20% 1,320,000', proof: '취소 요청 메일(09.29) · 약관 제7조', methods: ['MN2609-031 미수와 상계', '환불 송금'], lines: [ { label: '발생 09.29', sub: '계약금 1,980,000 입금분 중 환불 대상', amount: 660000 } ] },
        { id: 'BL-0928', party: '한빛투어', title: '잔금 과입', code: 'MN2610-005', event: 'MN2610-005 테를지 골프', cur: 'KRW', plan: '상계', reason: '09.28 입금 14,650,000 − 청구 잔금 12,800,000', proof: '기업은행 입금 내역(09.28)', methods: ['다음 청구에서 차감(MN2610-031)', '환불 송금'], lines: [ { label: '발생 09.28', sub: '입금 배분 후 남은 금액', amount: 1850000 } ] },
        { id: 'BL-0926', party: '고비 오아시스 캠프', title: '보상 차감', code: 'MN2609-033', event: 'MN2609-033 고비 사막 · CL2609-003', cur: 'MNT', plan: '상계', reason: '캠프 온수 고장 1박 환불을 업체가 부담', proof: '캠프 확인서(09.27) · 이도윤 승인', methods: ['10월 지급에서 차감', '환불 송금'], lines: [ { label: '발생 09.27', sub: '업체 책임 확인 · 다음 지급에서 차감', amount: -2260000 } ] },
        { id: 'BL-0925', party: '고비모터스', title: '단가 차이 차감', code: 'MN2610-002', event: 'MN2610-002 고비 사막 · 푸르공 3대', cur: 'MNT', plan: '상계', reason: '청구 420,000 vs 계약 400,000 MNT/일 × 3대 × 6일', proof: '2026 동계 요금표 · 고비모터스 청구서', methods: ['단가 확인 후 차감', '10월 지급에서 차감'], lines: [ { label: '발생 10.01', sub: '단가 차이 검토 후보에서 생성', amount: -360000 } ] },
        { id: 'BL-0912', party: '한빛투어', title: '8월 과입 상계', code: 'MN2608-012', event: 'MN2608-012 테를지 골프', cur: 'KRW', plan: '상계', reason: '8월 잔금 과입', proof: '8월 재개방 승인(09.12)', methods: [], lines: [ { label: '발생 08.28', sub: '잔금 과입', amount: 1200000 }, { label: '상계 09.12', sub: '9월 계약금 청구에서 차감', amount: -1200000 } ] }
      ] }'''
admin('Balance.dc.html', '과입·차감', 'balance', None, body, pre=pre, vals=vals, state=state, height=1000)
print('Balance written')
