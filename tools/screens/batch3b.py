import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import *

ROLE_SEG = '''<span class="label" style="color: var(--ink-muted)">보기 권한</span>
<x-import component-from-global-scope="Abt.Segmented" options="{{roleOptions}}" value="{{role}}" on-change="{{setRole}}" aria-label="보기 권한"></x-import>'''

# ------------------------------------------------------------------ Remittance (송금)
body = header('송금', 'ABT 한국 → ABT Mongolia LLC 지상비 송금 원장 · 내부거래라 통합 매출에서 뺍니다', ROLE_SEG + '''
<x-import component-from-global-scope="Abt.Button" variant="secondary" on-click="{{exportXls}}">엑셀 다운로드</x-import>
<x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{toggleNew}}">{{newLabel}}</x-import>''')
body += NOTICE
body += '''<section aria-label="송금 단계별 현황" style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px">
<x-import component-from-global-scope="Abt.KpiTile" label="요청·검토 중" money="{{kpi.pending}}" caption="{{kpi.pendingCaption}}"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="승인 후 미송금" money="{{kpi.approved}}" state="{{kpi.approvedState}}" state-label="{{kpi.approvedLabel}}" caption="{{kpi.approvedCaption}}"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="9월 이후 송금 완료" money="{{kpi.done}}" caption="{{kpi.doneCaption}}"></x-import>
</section>

<sc-if value="{{creating}}" hint-placeholder-val="{{false}}">
''' + PANEL + panel_title('송금 요청', '확정된 지상비 범위 안에서만 요청합니다 · 같은 행사·금액의 처리 중 요청이 있으면 막습니다') + field_grid(200) + '''
<x-import component-from-global-scope="Abt.Select" label="대상 행사" required="{{yes}}" options="{{eventOptions}}" value="{{nf.event}}" on-change="{{onNf.event}}" help="{{eventHelp}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="요청액" required="{{yes}}" input-mode="numeric" align="end" suffix="MNT" value="{{nf.amount}}" on-change="{{onNf.amount}}" error="{{nfErr.amount}}" help="{{amountHelp}}"></x-import>
<x-import component-from-global-scope="Abt.Select" label="보내는 통화" options="{{sendOptions}}" value="{{nf.send}}" on-change="{{onNf.send}}"></x-import>
</div>
<x-import component-from-global-scope="Abt.TextField" label="{{reasonLabel}}" placeholder="예: 숙박 업체 선결제 조건(출발 7일 전)" value="{{nf.reason}}" on-change="{{onNf.reason}}" error="{{nfErr.reason}}"></x-import>
<div style="display: flex; justify-content: flex-end; gap: 8px">
<x-import component-from-global-scope="Abt.Button" variant="ghost" on-click="{{toggleNew}}">취소</x-import>
<x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{submitNew}}">요청 보내기</x-import>
</div>
</section>
</sc-if>

<div style="display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(380px, 1fr); gap: 16px; align-items: start">
<section style="display: flex; flex-direction: column; gap: 10px; min-width: 0">
<p class="caption" style="margin: 0; color: var(--ink-muted)">분할 송금은 같은 번호에 -1, -2를 붙입니다 · 행을 누르면 오른쪽에서 처리합니다</p>
<x-import component-from-global-scope="Abt.DataTable" columns="{{cols}}" rows="{{rows}}" on-row-click="{{pick}}" caption="송금 원장"></x-import>
</section>
''' + SIDE_PANEL + '''<div style="display: flex; flex-direction: column; gap: 8px">
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 8px">
<span style="font: 500 14px/20px var(--font-mono)">{{cur.no}}</span>
<x-import component-from-global-scope="Abt.StatusBadge" axis="remit" status="{{cur.status}}" size="md"></x-import>
</div>
<h2 class="title-2" style="margin: 0">{{cur.title}}</h2>
<x-import component-from-global-scope="Abt.Money" amount="{{cur.mnt}}" currency="MNT" size="lg" align="start" converted="{{cur.converted}}"></x-import>
</div>
''' + dl([('대상 행사', '{{cur.events}}'), ('수취인', 'ABT Mongolia LLC · 칸은행 ****4821'), ('요청', '{{cur.requested}}'), ('환율·수수료', '{{cur.fxText}}')], 88) + '''<x-import component-from-global-scope="Abt.ApprovalSteps" steps="{{cur.steps}}" orientation="vertical"></x-import>
<sc-if value="{{cur.hasNote}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.Alert" tone="{{cur.noteTone}}" title="{{cur.noteTitle}}">{{cur.noteBody}}</x-import>
</sc-if>
<sc-if value="{{act.decide}}" hint-placeholder-val="{{false}}">
<div style="display: flex; flex-direction: column; gap: 12px; padding-top: 12px; border-top: 1px solid var(--line)">
<x-import component-from-global-scope="Abt.TextField" label="의견" placeholder="반려하면 사유가 요청자에게 갑니다" value="{{note}}" on-change="{{setNote}}" error="{{noteError}}"></x-import>
<div style="display: flex; justify-content: flex-end; gap: 8px">
<x-import component-from-global-scope="Abt.Button" variant="danger" on-click="{{reject}}">반려</x-import>
<x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{pass}}">{{act.passLabel}}</x-import>
</div>
</div>
</sc-if>
<sc-if value="{{act.send}}" hint-placeholder-val="{{true}}">
<div style="display: flex; flex-direction: column; gap: 12px; padding-top: 12px; border-top: 1px solid var(--line)">
<x-import component-from-global-scope="Abt.Alert" tone="progress" title="승인됐지만 아직 송금되지 않았습니다">은행 송금증을 붙이고 실제 송금일·환율·수수료를 입력해야 송금 완료가 됩니다.</x-import>
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px">
<x-import component-from-global-scope="Abt.TextField" label="실제 송금일" type="date" value="{{sendDate}}" on-change="{{setSendDate}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="송금 수수료" value="{{fee}}" on-change="{{setFee}}" input-mode="numeric" suffix="KRW" align="end"></x-import>
</div>
<x-import component-from-global-scope="Abt.MoneyField" label="실제 보낸 금액" amount="{{cur.sendAmount}}" currency="KRW" currencies="{{sendCurrencies}}" rate="{{receiveRate}}" help="받는 쪽 금액(MNT)은 실제 적용 환율로 계산합니다."></x-import>
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 8px">
<x-import component-from-global-scope="Abt.Attachment" kind="proof" name="신한은행_해외송금확인서_1001.pdf" meta="380 KB" missing="{{proofMissing}}"></x-import>
<div style="display: flex; gap: 8px">
<x-import component-from-global-scope="Abt.Button" variant="secondary" on-click="{{attach}}">송금증 첨부</x-import>
<x-import component-from-global-scope="Abt.Button" variant="primary" disabled="{{proofMissing}}" on-click="{{complete}}">송금 완료 처리</x-import>
</div>
</div>
</div>
</sc-if>
<sc-if value="{{act.wait}}" hint-placeholder-val="{{false}}">
<p class="caption" style="margin: 0; padding-top: 12px; border-top: 1px solid var(--line); color: var(--ink-muted)">{{act.waitText}}</p>
</sc-if>
</section>
</div>
'''

pre = '''
    const ROLES = { '회계': { name: '박서연', role: '회계담당자' }, '운영관리자': { name: '김지훈', role: '운영관리자' }, '대표': { name: '이도윤', role: '대표' } };
    const STAGE_ROLE = { review: '운영관리자', approve: '대표', send: '회계' };
    const role = s.role;
    const R = s.items;
    const cur = R.find((i) => i.id === s.selected) || R[0];
    const NOW = '10.01 16:10 KST';
    const fm = (n, c) => new Intl.NumberFormat('ko-KR', { minimumFractionDigits: c === 'USD' ? 2 : 0, maximumFractionDigits: c === 'USD' ? 2 : 0 }).format(n);
    const stepsOf = (i) => {
      const order = ['request', 'review', 'approve', 'send'];
      const names = ['송금 요청', '검토', '승인', '송금 완료'];
      const idx = i.stage === 'done' ? 4 : i.stage === 'rejected' ? -1 : order.indexOf(i.stage);
      return order.map((st, k) => {
        const log = (i.log || {})[st] || {};
        let state = idx === 4 || k < idx ? 'done' : k === idx ? 'current' : 'pending';
        if (i.stage === 'rejected') state = log.state || (log.actor ? 'done' : 'skipped');
        return { label: names[k], state, actor: log.actor || (state === 'current' ? { review: '김지훈(운영관리자)', approve: '이도윤(대표)', send: '박서연(회계)' }[st] : undefined), at: log.at, note: log.note };
      });
    };
    const statusOf = (i) => (i.stage === 'done' ? 'completed' : i.stage === 'rejected' ? 'rejected' : i.stage === 'send' ? 'approved' : i.stage === 'approve' ? 'reviewing' : 'requested');
    const pendingItems = R.filter((i) => i.stage === 'review' || i.stage === 'approve');
    const approvedItems = R.filter((i) => i.stage === 'send');
    const doneItems = R.filter((i) => i.stage === 'done');
    const EV = [
      { value: 'MN2610-012', label: 'MN2610-012 · 누리투어 인센티브', budget: 112500000, sent: 0, paidState: '부분 입금' },
      { value: 'MN2610-009', label: 'MN2610-009 · 다온여행사 홉스골', budget: 68400000, sent: 0, paidState: '입금 전' },
      { value: 'MN2610-019', label: 'MN2610-019 · 한빛투어 테를지 골프', budget: 38700000, sent: 0, paidState: '입금 완료' },
      { value: 'MN2609-040', label: 'MN2609-040 · 솔빛여행 UB 시티', budget: 19600000, sent: 9800000, paidState: '부분 입금' }
    ];
    const nf = s.nf;
    const ev = EV.find((e) => e.value === nf.event);
    const inFlight = (code) => R.filter((i) => i.events.includes(code) && i.stage !== 'done' && i.stage !== 'rejected').reduce((a, i) => a + i.mnt, 0);
    const avail = ev ? ev.budget - ev.sent - inFlight(ev.value) : 0;
    const num = (v) => Number(String(v || '').replace(/[^0-9]/g, '')) || 0;
    const mine = cur.stage in STAGE_ROLE && STAGE_ROLE[cur.stage] === role;
    const decide = (ok) => {
      const note = (s.note || '').trim();
      if (!ok && !note) { set({ noteError: '반려 사유를 적어 주세요.' }); return; }
      const nextStage = ok ? (cur.stage === 'review' ? 'approve' : 'send') : 'rejected';
      const who = ROLES[role].name;
      const log = { ...(cur.log || {}), [cur.stage]: { actor: who, at: NOW, note: note || undefined, state: ok ? 'done' : 'rejected' } };
      this.setState({ items: R.map((i) => (i.id === cur.id ? { ...i, stage: nextStage, log } : i)), note: '', noteError: '', notice: { tone: ok ? 'positive' : 'critical', title: ok ? `${cur.no} ${cur.stage === 'review' ? '검토를 마쳤습니다' : '승인했습니다'}` : `${cur.no} 반려했습니다`, body: ok ? (cur.stage === 'review' ? '대표 승인을 기다립니다.' : '회계가 실제로 송금하고 송금증을 올려야 완료됩니다.') : '사유가 요청자(박서연)에게 전달됐습니다.' } });
    };
'''
vals = '''      user: ROLES[role],
      roleOptions: ['회계', '운영관리자', '대표'],
      role,
      setRole: (v) => set({ role: v, note: '', noteError: '' }),
      navCounts: { alerts: 5, field: 2, claims: { n: 2, tone: 'critical' }, receipts: { n: 1, tone: 'critical' }, costs: { n: 7, tone: 'attention' }, remit: pendingItems.length + approvedItems.length || undefined },
      kpi: {
        pending: { amount: pendingItems.reduce((a, i) => a + i.mnt, 0), currency: 'MNT' },
        pendingCaption: `${pendingItems.length}건 · 승인 전`,
        approved: { amount: approvedItems.reduce((a, i) => a + i.mnt, 0), currency: 'MNT' },
        approvedState: approvedItems.length ? 'attention' : undefined,
        approvedLabel: approvedItems.length ? '송금증 대기' : '',
        approvedCaption: approvedItems.length ? approvedItems.map((i) => i.no).join(' · ') : '없음',
        done: { amount: doneItems.reduce((a, i) => a + i.mnt, 0), currency: 'MNT' },
        doneCaption: `${doneItems.length}건 · 송금증 모두 보관`
      },
      exportXls: () => say('positive', '송금 원장을 내려받았습니다', '요청액·실제 보낸 금액·적용 환율·수수료·증빙 여부를 각각 다른 열로 담았습니다.'),
      creating: !!s.creating,
      newLabel: s.creating ? '요청 닫기' : '송금 요청',
      toggleNew: () => (role !== '회계' ? say('attention', '송금 요청은 회계담당자가 합니다', '보기 권한을 회계로 바꾸면 요청할 수 있습니다. 요청자와 승인자는 같은 사람이 될 수 없습니다.') : set({ creating: !s.creating, nfErr: {} })),
      eventOptions: EV.map((e) => ({ value: e.value, label: e.label })),
      eventHelp: ev ? `지상비 예산 ${fmt(ev.budget)} · 송금 ${fmt(ev.sent)} · 처리 중 ${fmt(inFlight(ev.value))} → 가능 ${fmt(avail)} MNT · ${ev.paidState}` : '',
      amountHelp: avail > 0 ? `최대 ${fmt(avail)} MNT · 절반이면 분할 송금(-1, -2)으로 나눕니다` : '이 행사는 더 보낼 수 있는 금액이 없습니다',
      sendOptions: ['KRW (기업은행)', 'USD (신한은행)'],
      reasonLabel: ev && ev.paidState !== '입금 완료' ? '선지급 사유 (입금 전 송금)' : '메모',
      nf,
      onNf: { event: (e) => set({ nf: { ...s.nf, event: e.target.value, amount: '' }, nfErr: {} }), amount: (e) => set({ nf: { ...s.nf, amount: e.target.value }, nfErr: {} }), send: (e) => set({ nf: { ...s.nf, send: e.target.value } }), reason: (e) => set({ nf: { ...s.nf, reason: e.target.value }, nfErr: {} }) },
      nfErr: s.nfErr || {},
      submitNew: () => {
        const a = num(nf.amount);
        const er = {};
        if (!a) er.amount = '요청액을 입력하세요.';
        else if (a > avail) er.amount = avail > 0 ? `송금 가능액 ${fmt(avail)} MNT를 넘습니다.` : '처리 중인 요청이 있어 더 보낼 수 없습니다 (중복 요청 방지).';
        if (ev && ev.paidState !== '입금 완료' && !nf.reason.trim()) er.reason = '입금 전 송금은 선지급 사유가 필요합니다.';
        if (er.amount || er.reason) { set({ nfErr: er }); return; }
        const split = a < avail;
        const no = split ? 'RM2610-005-1' : 'RM2610-005';
        const usd = nf.send.startsWith('USD');
        const it = { id: 'r' + (R.length + 1), no, title: `${ev.label.split(' · ')[1]} 지상비${split ? ' · 분할 1/2' : ''}`, events: ev.value, ev: { primary: ev.value, secondary: ev.label.split(' · ')[1] }, mnt: a, send: usd ? { amount: Math.round(a / 3497.1 * 100) / 100, currency: 'USD' } : { amount: Math.round(a * 0.3985), currency: 'KRW' }, fx: { primary: usd ? '3,497.1 MNT/USD (예상)' : '0.3985 KRW/MNT (예상)', secondary: '수수료 미정' }, stage: 'review', requested: `박서연 · ${NOW}`, log: { request: { actor: '박서연', at: NOW, note: nf.reason.trim() || undefined } } };
        this.setState({ items: [it].concat(R), selected: it.id, creating: false, nf: { event: 'MN2610-012', amount: '', send: 'KRW (기업은행)', reason: '' }, notice: { tone: 'positive', title: `${no} 송금 요청을 보냈습니다`, body: `${fmt(a)} MNT · 운영관리자 검토 → 대표 승인 → 송금 순서로 진행됩니다.` } });
      },
      cols: [
        { key: 'no', label: '송금번호', type: 'strong' },
        { key: 'ev', label: '대상 행사', type: 'stack' },
        { key: 'mnt', label: '요청액', type: 'money', currency: 'MNT' },
        { key: 'sent', label: '보낸 금액 / 환율·수수료', type: 'stack', wrap: true },
        { key: 'status', label: '단계', type: 'status', axis: 'remit' }
      ],
      rows: R.map((i) => ({ id: i.id, no: i.no, ev: i.ev, mnt: i.mnt, sent: { primary: i.stage === 'done' ? `${fm(i.send.amount, i.send.currency)} ${i.send.currency}` : i.stage === 'rejected' ? '보내지 않음' : `예정 ${fm(i.send.amount, i.send.currency)} ${i.send.currency}`, secondary: `${i.fx.primary} · ${i.fx.secondary}` }, status: statusOf(i), selected: i.id === cur.id })),
      pick: (row) => set({ selected: row.id, note: '', noteError: '' }),
      cur: { ...cur, status: statusOf(cur), steps: stepsOf(cur), converted: { amount: cur.send.amount, currency: cur.send.currency }, fxText: `${cur.fx.primary} · ${cur.fx.secondary}`, sendAmount: cur.send.currency === 'KRW' ? cur.send.amount : Math.round(cur.mnt * 0.3985), hasNote: !!cur.noteTitle, noteTone: cur.noteTone, noteTitle: cur.noteTitle, noteBody: cur.noteBody },
      act: {
        decide: mine && (cur.stage === 'review' || cur.stage === 'approve'),
        passLabel: cur.stage === 'review' ? '검토 완료' : '승인',
        send: mine && cur.stage === 'send',
        wait: !mine && cur.stage in STAGE_ROLE,
        waitText: cur.stage in STAGE_ROLE ? `이 단계는 ${STAGE_ROLE[cur.stage]} 권한입니다. 지금 보기 권한(${role})으로는 처리할 수 없습니다.` : ''
      },
      note: s.note,
      setNote: (e) => set({ note: e.target.value, noteError: '' }),
      noteError: s.noteError || '',
      pass: () => decide(true),
      reject: () => decide(false),
      sendDate: s.sendDate,
      setSendDate: (e) => set({ sendDate: e.target.value }),
      fee: s.fee,
      setFee: (e) => set({ fee: e.target.value }),
      sendCurrencies: ['KRW', 'USD'],
      receiveRate: { value: 2.5094, base: 'MNT', date: '10.01' },
      proofMissing: !s.attached[cur.id],
      attach: () => set({ attached: { ...s.attached, [cur.id]: true } }),
      complete: () => {
        const log = { ...(cur.log || {}), send: { actor: '박서연', at: `${s.sendDate.slice(5).replace('-', '.')} · 송금증 첨부`, note: `수수료 ${s.fee} KRW` } };
        this.setState({ items: R.map((i) => (i.id === cur.id ? { ...i, stage: 'done', log, fx: { primary: i.fx.primary.replace(' (예상)', ''), secondary: `수수료 ${s.fee} KRW` }, noteTitle: '', noteTone: '', noteBody: '' } : i)), notice: { tone: 'positive', title: `${cur.no} 송금 완료로 처리했습니다`, body: cur.no.startsWith('RM2609-021') ? 'RM2609-021 분할 송금 2건이 모두 끝나 MN2609-033 송금 상태가 송금 완료로 바뀝니다.' : '송금증·실제 환율·수수료가 함께 보관됐습니다.', action: cur.no.startsWith('RM2609-021') ? { label: '행사 상세', href: 'EventDetail.dc.html' } : null } });
      },'''

state = '''{ role: '회계', selected: 'r3', creating: false, note: '', noteError: '', attached: {}, sendDate: '2026-10-01', fee: '12,000', nfErr: {}, notice: null,
      nf: { event: 'MN2610-012', amount: '', send: 'KRW (기업은행)', reason: '' },
      items: [
        { id: 'r1', no: 'RM2610-004', title: '10월 출발 2건 지상비', events: 'MN2610-002 · MN2610-005', ev: { primary: 'MN2610-002 외 1', secondary: '푸른하늘여행 · 한빛투어' }, mnt: 54800000, send: { amount: 15670, currency: 'USD' }, fx: { primary: '3,497.1 MNT/USD (예상)', secondary: '수수료 미정' }, stage: 'review', requested: '박서연 · 10.01 09:40 KST', log: { request: { actor: '박서연', at: '10.01 09:40 KST' } } },
        { id: 'r2', no: 'RM2610-003', title: 'MN2609-040 지상비 잔액', events: 'MN2609-040', ev: { primary: 'MN2609-040', secondary: '솔빛여행' }, mnt: 9800000, send: { amount: 3905300, currency: 'KRW' }, fx: { primary: '0.3985 KRW/MNT (예상)', secondary: '수수료 미정' }, stage: 'approve', requested: '박서연 · 09.30 17:10 KST', log: { request: { actor: '박서연', at: '09.30 17:10 KST', note: '선지급 사유: 현지 업체 선결제 조건' }, review: { actor: '김지훈', at: '10.01 10:20 KST', note: '잔금 미입금 확인 · 선지급 동의' } }, noteTone: 'attention', noteTitle: '입금 전 송금', noteBody: '솔빛여행 잔금 4,950,000 KRW가 아직 들어오지 않았습니다(기한 10.02). 선지급 사유가 기록돼 있습니다.' },
        { id: 'r3', no: 'RM2609-021-2', title: '분할 송금 2/2 · 지상비 잔액', events: 'MN2609-033', ev: { primary: 'MN2609-033', secondary: '푸른하늘여행' }, mnt: 10500000, send: { amount: 4184250, currency: 'KRW' }, fx: { primary: '0.3985 KRW/MNT (예상)', secondary: '수수료 미정' }, stage: 'send', requested: '박서연 · 09.26 11:20 KST', log: { request: { actor: '박서연', at: '09.26' }, review: { actor: '김지훈', at: '09.26' }, approve: { actor: '이도윤', at: '09.27' } } },
        { id: 'r4', no: 'RM2609-021-1', title: '분할 송금 1/2 · 지상비 선금', events: 'MN2609-033', ev: { primary: 'MN2609-033', secondary: '푸른하늘여행' }, mnt: 40000000, send: { amount: 15940000, currency: 'KRW' }, fx: { primary: '0.3985 KRW/MNT', secondary: '수수료 18,000 KRW' }, stage: 'done', requested: '박서연 · 09.16 10:05 KST', log: { request: { actor: '박서연', at: '09.16' }, review: { actor: '김지훈', at: '09.16' }, approve: { actor: '이도윤', at: '09.17' }, send: { actor: '박서연', at: '09.18 · 송금증 첨부' } }, noteTone: 'positive', noteTitle: '송금 완료', noteBody: '실제 환율 0.3985, 수수료 18,000 KRW, 은행 송금증이 함께 보관되어 있습니다.' },
        { id: 'r5', no: 'RM2609-019', title: 'MN2609-031 지상비 전액', events: 'MN2609-031', ev: { primary: 'MN2609-031', secondary: '다온여행사' }, mnt: 72000000, send: { amount: 20590, currency: 'USD' }, fx: { primary: '3,496.8 MNT/USD', secondary: '수수료 28,000 KRW' }, stage: 'done', requested: '박서연 · 09.12 15:00 KST', log: { request: { actor: '박서연', at: '09.12' }, review: { actor: '김지훈', at: '09.13' }, approve: { actor: '이도윤', at: '09.14' }, send: { actor: '박서연', at: '09.15 · 송금증 첨부' } }, noteTone: 'attention', noteTitle: '입금보다 먼저 송금됨', noteBody: '다온여행사 잔금 12,400,000 KRW가 연체 중입니다. 미수가 풀리기 전까지 이 행사는 적자로 집계됩니다.' },
        { id: 'r6', no: 'RM2609-016', title: 'MN2609-029 지상비 전액', events: 'MN2609-029', ev: { primary: 'MN2609-029', secondary: '솔빛여행' }, mnt: 17500000, send: { amount: 6973750, currency: 'KRW' }, fx: { primary: '0.3985 KRW/MNT', secondary: '—' }, stage: 'rejected', requested: '박서연 · 09.10 16:30 KST', log: { request: { actor: '박서연', at: '09.10', state: 'done' }, review: { actor: '김지훈', at: '09.10', state: 'done' }, approve: { actor: '이도윤', at: '09.11', note: '수취 계좌 확인서 누락 · RM2609-018로 재요청', state: 'rejected' } }, noteTone: 'critical', noteTitle: '반려됨', noteBody: '수취 계좌 확인서가 없어 반려했습니다. 같은 금액을 RM2609-018로 다시 요청해 09.12에 송금했습니다.' }
      ] }'''
admin('Remittance.dc.html', '송금', 'remit', None, body, pre=pre, vals=vals, state=state, height=1200)
print('Remittance written')


# ------------------------------------------------------------------ Settlement (정산·마감)
body = header('{{title}}', '{{caption}}', ROLE_SEG + '''
<x-import component-from-global-scope="Abt.Select" inline="{{yes}}" label="정산 월" options="{{months}}" value="{{month}}" on-change="{{setMonth}}"></x-import>
<x-import component-from-global-scope="Abt.Button" variant="secondary" on-click="{{download}}">정산서 내려받기</x-import>''')
body += NOTICE
body += '''<section aria-label="월 손익" style="display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 12px">
<x-import component-from-global-scope="Abt.KpiTile" label="확정 매출" money="{{m.kpiSales}}" caption="{{m.salesCaption}}"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="한국 마진" money="{{m.kpiKorea}}" caption="판매금액 − 몽골 송금 지상비"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="현지 수익" money="{{m.kpiLocal}}" caption="송금 지상비 − 실제 지상비"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="통합 손익" money="{{m.kpiTotal}}" delta="{{m.delta}}" caption="{{m.totalCaption}}"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="정산 확정" value="{{m.settledValue}}" unit="건" caption="{{m.settledCaption}}"></x-import>
</section>

<sc-if value="{{isSep}}" hint-placeholder-val="{{true}}">
''' + PANEL + '''<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 4px">
<div style="display: flex; flex-direction: column; gap: 2px"><h2 class="title-2" style="margin: 0">마감 전에 처리할 항목</h2><p class="caption" style="margin: 0; color: var(--ink-muted)">미수금은 마감을 막지 않고 다음 달로 이월됩니다 · 마감 예정 10.05(월)</p></div>
<div style="display: flex; align-items: center; gap: 12px"><span class="caption" style="color: var(--ink-muted)">4건을 처리하면 마감할 수 있습니다</span><x-import component-from-global-scope="Abt.Button" variant="primary" disabled="{{yes}}">9월 마감</x-import></div>
</div>
<sc-for list="{{blockers}}" as="b" hint-placeholder-count="5">
<div style="display: grid; grid-template-columns: 132px minmax(0, 1fr) 140px 120px; align-items: center; gap: 16px; padding: 10px 0; border-top: 1px solid var(--line)">
<x-import component-from-global-scope="Abt.StatusBadge" axis="{{b.axis}}" status="{{b.status}}"></x-import>
<div style="display: flex; flex-direction: column; gap: 2px; min-width: 0">
<span class="body-strong" style="font-size: 13px; line-height: 20px">{{b.title}}</span>
<span class="caption" style="color: var(--ink-muted)">{{b.detail}}</span>
</div>
<span class="caption" style="color: var(--ink-muted)">{{b.blocking}}</span>
<a href="{{b.href}}" class="caption" style="justify-self: end; color: var(--ink); text-decoration: underline; text-underline-offset: 3px">{{b.link}}</a>
</div>
</sc-for>
</section>
</sc-if>

<sc-if value="{{isAug}}" hint-placeholder-val="{{false}}">
''' + PANEL + '''<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px">
<div style="display: flex; align-items: center; gap: 10px"><h2 class="title-2" style="margin: 0">8월 마감 상태</h2><x-import component-from-global-scope="Abt.StatusBadge" tone="{{aug.tone}}" form="{{aug.form}}" size="md">{{aug.label}}</x-import></div>
<sc-if value="{{aug.canRequest}}" hint-placeholder-val="{{true}}"><x-import component-from-global-scope="Abt.Button" on-click="{{openReopen}}">재개방 요청</x-import></sc-if>
<sc-if value="{{aug.canReclose}}" hint-placeholder-val="{{false}}"><x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{reclose}}">다시 마감</x-import></sc-if>
</div>
<p class="caption" style="margin: 0; color: var(--ink-muted)">{{aug.text}}</p>
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px 16px">
<x-import component-from-global-scope="Abt.TextField" label="MN2608-019 정산 조정액" value="{{adj}}" on-change="{{setAdj}}" suffix="KRW" align="end" locked="{{aug.locked}}" help="{{aug.adjHelp}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="조정 사유" value="{{adjWhy}}" on-change="{{setAdjWhy}}" locked="{{aug.locked}}" help="{{aug.whyHelp}}"></x-import>
</div>
<sc-if value="{{reopenForm}}" hint-placeholder-val="{{false}}">
<div style="display: flex; flex-direction: column; gap: 12px; padding: 16px; border: 1px solid var(--line-strong); border-radius: 6px">
<span class="body-strong" style="font-size: 14px">재개방 요청</span>
''' + field_grid(220) + '''
<x-import component-from-global-scope="Abt.Select" label="대상" options="{{reopenTargets}}" value="{{rf.target}}" on-change="{{onRf.target}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="예상 영향" placeholder="예: 통합 손익 −380,000 KRW" value="{{rf.impact}}" on-change="{{onRf.impact}}"></x-import>
</div>
<x-import component-from-global-scope="Abt.TextField" label="사유" required="{{yes}}" multiline="{{yes}}" rows="{{two}}" placeholder="무엇이 틀렸고 어떤 근거로 고치는지 적습니다" value="{{rf.reason}}" on-change="{{onRf.reason}}" error="{{rfError}}"></x-import>
<div style="display: flex; align-items: center; justify-content: space-between; gap: 12px"><span class="caption" style="color: var(--ink-muted)">승인자: 이도윤(대표) · 승인 전까지 8월 자료는 잠겨 있습니다</span><div style="display: flex; gap: 8px"><x-import component-from-global-scope="Abt.Button" variant="ghost" on-click="{{closeReopen}}">취소</x-import><x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{sendReopen}}">요청 보내기</x-import></div></div>
</div>
</sc-if>
<sc-if value="{{aug.canApprove}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.Alert" tone="attention" title="{{aug.reqTitle}}">{{aug.reqBody}}</x-import>
<div style="display: flex; justify-content: flex-end; gap: 8px"><x-import component-from-global-scope="Abt.Button" variant="danger" on-click="{{denyReopen}}">반려</x-import><x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{approveReopen}}">재개방 승인</x-import></div>
</sc-if>
</section>
</sc-if>

<section style="display: flex; flex-direction: column; gap: 12px">
<div style="display: flex; flex-wrap: wrap; align-items: baseline; justify-content: space-between; gap: 12px">
<h2 class="title-2" style="margin: 0">행사별 손익</h2>
<p class="caption" style="margin: 0; color: var(--ink-muted)">{{m.tableCaption}}</p>
</div>
<x-import component-from-global-scope="Abt.DataTable" columns="{{cols}}" rows="{{m.rows}}" totals="{{m.totals}}" caption="행사별 손익"></x-import>
</section>

<section style="display: flex; flex-direction: column; gap: 8px">
<h2 class="title-2" style="margin: 0">마감 이력</h2>
<div style="padding: 4px 20px; background: var(--surface); border: 1px solid var(--line); border-radius: 6px">
<x-import component-from-global-scope="Abt.AuditLog" entries="{{history}}"></x-import>
</div>
</section>
'''

pre = '''
    const R = 0.3985;
    const D = 'EventDetail.dc.html';
    const ROLES = { '회계': { name: '박서연', role: '회계담당자' }, '대표': { name: '이도윤', role: '대표' } };
    const role = s.role;
    const isSep = s.month === '2026년 9월';
    const sep = [
      { id: 1, code: 'MN2609-027', agency: '한빛투어', product: '테를지 골프 3박 4일', S: 9600000, T: 19800000, A: 18900000, st: 'settled', flags: [] },
      { id: 2, code: 'MN2609-029', agency: '솔빛여행', product: '울란바토르 시티 3박 4일', S: 8400000, T: 17500000, A: 17100000, st: 'settled', flags: [] },
      { id: 3, code: 'MN2609-030', agency: '누리투어', product: '테를지 승마·게르 2박 3일', S: 11200000, T: 22600000, A: 21950000, st: 'settled', flags: [] },
      { id: 4, code: 'MN2609-031', agency: '다온여행사', product: '홉스골 호수 6박 7일', S: 32400000, T: 72000000, A: 84420000, st: 'reviewing', flags: ['deficit', 'missing-proof'] },
      { id: 5, code: 'MN2609-033', agency: '푸른하늘여행', product: '고비 사막 5박 6일', S: 23000000, T: 50500000, A: 52240000, st: 'reviewing', flags: ['margin-drop', 'duplicate'] },
      { id: 6, code: 'MN2609-035', agency: '제이원트래블', product: '고비 사막 5박 6일', S: 25300000, T: 52800000, A: 50900000, st: 'settled', flags: [] },
      { id: 7, code: 'MN2609-036', agency: '한빛투어', product: '기업 인센티브 4박 5일', S: 41800000, T: 86000000, A: 83700000, st: 'settled', flags: [] },
      { id: 8, code: 'MN2609-038', agency: '제이원트래블', product: '테를지 승마·게르 2박 3일', S: 15400000, T: 31000000, A: 29800000, st: 'open', flags: [], open: true }
    ];
    const aug = [
      { id: 11, code: 'MN2608-012', agency: '한빛투어', product: '테를지 골프 3박 4일', S: 12800000, T: 25800000, A: 25100000, st: 'closed', flags: [] },
      { id: 12, code: 'MN2608-015', agency: '푸른하늘여행', product: '고비 사막 5박 6일', S: 34500000, T: 70950000, A: 69800000, st: 'closed', flags: [] },
      { id: 13, code: 'MN2608-019', agency: '누리투어', product: '기업 인센티브 4박 5일', S: 61200000, T: 126000000, A: 121400000, st: 'closed', flags: [] },
      { id: 14, code: 'MN2608-021', agency: '다온여행사', product: '홉스골 호수 6박 7일', S: 37800000, T: 79800000, A: 78100000, st: 'closed', flags: [] },
      { id: 15, code: 'MN2608-024', agency: '제이원트래블', product: '테를지 승마·게르 2박 3일', S: 15400000, T: 31000000, A: 30200000, st: 'closed', flags: [] },
      { id: 16, code: 'MN2608-027', agency: '솔빛여행', product: '울란바토르 시티 3박 4일', S: 9900000, T: 19600000, A: 19950000, st: 'closed', flags: [] }
    ];
    const augState = s.augState;
    const ev = isSep ? sep : aug.map((e) => ({ ...e, st: augState === 'reopened' ? 'reopened' : 'closed' }));
    const k = (e) => Math.round(e.S - e.T * R);
    const m = (e) => Math.round((e.T - e.A) * R);
    const rows = ev.map((e) => { const c = k(e) + m(e); const exp = e.open ? 'expected' : 'actual'; return { id: e.id, code: e.code, href: D, who: { primary: e.agency, secondary: e.product }, sales: e.S, cost: { amount: e.A, kind: exp }, korea: k(e), local: { amount: m(e), kind: exp }, total: { amount: c, kind: exp }, rate: Math.round((c / e.S) * 1000) / 10, st: e.st, flags: e.flags }; });
    const sum = (f) => ev.reduce((a, e) => a + f(e), 0);
    const NOW = '2026-10-01T16:20';
    const log = s.log;
    const rf = s.rf;
    const AUG_TEXT = {
      closed: '8월은 09.13에 다시 마감했습니다. 마감한 자료는 직접 고칠 수 없고, 재개방을 요청해 대표 승인을 받은 뒤 고칩니다.',
      requested: '재개방 요청을 보냈습니다. 대표가 승인하기 전까지 자료는 계속 잠겨 있습니다.',
      reopened: '재개방됐습니다. 조정 금액과 사유를 고친 뒤 다시 마감하세요. 바뀐 값은 모두 이력에 남습니다.'
    };
'''
vals = '''      user: ROLES[role],
      roleOptions: ['회계', '대표'],
      role,
      setRole: (v) => set({ role: v }),
      months: ['2026년 9월', '2026년 8월 (마감)'],
      month: s.month,
      setMonth: (e) => set({ month: e.target.value, reopenForm: false }),
      title: isSep ? '9월 정산·마감' : '8월 정산·마감',
      caption: isSep ? '마감 예정 10.05(월) · 마감한 자료는 직접 고칠 수 없고 재개방 승인 후 고칩니다 · KRW 환산은 거래별 적용 환율' : '8월은 마감된 달입니다 · 재개방은 회계가 요청하고 대표가 승인합니다 · 마감 후 바뀐 값은 사유와 함께 남습니다',
      download: () => say('positive', `${isSep ? '9월' : '8월'} 정산서를 내려받았습니다`, '집계 기준일·통화·환율·예상/확정 구분이 표지에 들어갑니다. 권한이 있는 항목만 담았습니다.'),
      isSep,
      isAug: !isSep,
      m: isSep ? {
        kpiSales: { amount: 552000000, currency: 'KRW' }, salesCaption: '29건 · 여행사 청구 기준', kpiKorea: { amount: 48600000, currency: 'KRW' }, kpiLocal: { amount: 25600000, currency: 'KRW' }, kpiTotal: { amount: 74200000, currency: 'KRW' }, delta: { value: -37.4, period: '8월 대비(비수기)', good: 'up', digits: 1 }, totalCaption: '내부거래 제외 · 마진율 13.4%', settledValue: '24 / 29', settledCaption: '검토 중 4건 · 미정산 1건', tableCaption: '29건 중 8건 표시 · 지상비는 MNT 원금, 손익은 KRW 환산(0.3985) · 손실은 빨간 글자 · 행을 누르면 행사 상세',
        rows, totals: { label: '표시 8건', sales: sum((e) => e.S), cost: { amount: sum((e) => e.A), kind: 'expected' }, korea: sum(k), local: { amount: sum(m), kind: 'expected' }, total: { amount: sum(k) + sum(m), kind: 'expected' } }
      } : {
        kpiSales: { amount: 798400000, currency: 'KRW' }, salesCaption: '41건 · 마감', kpiKorea: { amount: 71300000, currency: 'KRW' }, kpiLocal: { amount: 47240000, currency: 'KRW' }, kpiTotal: { amount: 118540000, currency: 'KRW' }, delta: { value: 12.6, period: '7월 대비', good: 'up', digits: 1 }, totalCaption: '내부거래 제외 · 마진율 14.8%', settledValue: '41 / 41', settledCaption: augState === 'reopened' ? '재개방 중 · 수정 가능' : '마감 · 수정 잠김', tableCaption: '41건 중 6건 표시 · 마감된 달은 금액을 직접 고칠 수 없습니다',
        rows, totals: { label: '표시 6건', sales: sum((e) => e.S), cost: sum((e) => e.A), korea: sum(k), local: sum(m), total: sum(k) + sum(m) }
      },
      blockers: [
        { axis: 'risk', status: 'duplicate', title: '중복 청구 후보 1건', detail: 'MN2609-033 · 09.24 고비 오아시스 캠프 저녁 525,000 MNT', blocking: '마감 전 처리', link: '비용 검토', href: 'Approvals.dc.html' },
        { axis: 'cost', status: 'reviewing', title: '승인 대기 비용 3건 · 1,395,000 MNT', detail: 'MN2609-033 2건, MN2609-038 1건', blocking: '마감 전 처리', link: '비용 승인', href: 'Approvals.dc.html' },
        { axis: 'risk', status: 'missing-proof', title: '증빙 누락 2건 · 610,000 MNT', detail: 'MN2609-031 유류 · 09.30 가이드에게 보완 요청', blocking: '마감 전 처리', link: '보완 현황', href: 'Approvals.dc.html' },
        { axis: 'remit', status: 'approved', title: '승인 후 미송금 1건 · 10,500,000 MNT', detail: 'RM2609-021-2 · 송금증·실제 환율 입력 필요', blocking: '마감 전 처리', link: '송금 처리', href: 'Remittance.dc.html' },
        { axis: 'payment', status: 'overdue', title: '연체 미수 1건 · 12,400,000 KRW', detail: 'MN2609-031 다온여행사 잔금 · 기한 09.30', blocking: '마감 가능 · 이월', link: '입금 원장', href: 'Receipts.dc.html' }
      ],
      cols: [
        { key: 'code', label: '행사코드', type: 'code' },
        { key: 'who', label: '여행사 / 상품', type: 'stack' },
        { key: 'sales', label: '판매금액', type: 'money', currency: 'KRW' },
        { key: 'cost', label: '실제 지상비', type: 'money', currency: 'MNT' },
        { key: 'korea', label: '한국 마진', type: 'money', currency: 'KRW', lossTone: true },
        { key: 'local', label: '현지 수익', type: 'money', currency: 'KRW', lossTone: true },
        { key: 'total', label: '통합 손익', type: 'money', currency: 'KRW', lossTone: true },
        { key: 'rate', label: '마진율', type: 'percent', lossTone: true },
        { key: 'st', label: '정산', type: 'status', axis: 'settle' },
        { key: 'flags', label: '검토 후보', type: 'flags' }
      ],
      aug: {
        label: augState === 'closed' ? '마감' : augState === 'requested' ? '재개방 요청 중' : '재개방',
        tone: augState === 'closed' ? 'neutral' : 'attention',
        form: augState === 'requested' ? 'dashed' : 'solid',
        text: AUG_TEXT[augState],
        locked: augState !== 'reopened',
        adjHelp: augState === 'reopened' ? '바꾸면 다시 마감할 때 이력에 남습니다' : '마감된 자료입니다. 재개방 승인 후 수정할 수 있습니다.',
        whyHelp: augState === 'reopened' ? '조정 근거를 남깁니다' : '마감된 자료입니다.',
        canRequest: augState === 'closed' && role === '회계' && !s.reopenForm,
        canApprove: augState === 'requested' && role === '대표',
        canReclose: augState === 'reopened' && role === '회계',
        reqTitle: `박서연 재개방 요청 · ${s.req ? s.req.target : ''}`,
        reqBody: s.req ? `사유: ${s.req.reason}${s.req.impact ? ` · 예상 영향: ${s.req.impact}` : ''}` : ''
      },
      adj: s.adj,
      setAdj: (e) => set({ adj: e.target.value }),
      adjWhy: s.adjWhy,
      setAdjWhy: (e) => set({ adjWhy: e.target.value }),
      reopenForm: !!s.reopenForm && s.augState === 'closed',
      openReopen: () => set({ reopenForm: true }),
      closeReopen: () => set({ reopenForm: false, rfError: '' }),
      reopenTargets: ['MN2608-019 · 누리투어 인센티브', '8월 전체'],
      rf,
      onRf: { target: (e) => set({ rf: { ...s.rf, target: e.target.value } }), impact: (e) => set({ rf: { ...s.rf, impact: e.target.value } }), reason: (e) => set({ rf: { ...s.rf, reason: e.target.value }, rfError: '' }) },
      rfError: s.rfError || '',
      sendReopen: () => {
        if (!rf.reason.trim()) { set({ rfError: '재개방 사유는 꼭 남겨야 합니다.' }); return; }
        this.setState({ augState: 'requested', reopenForm: false, req: { ...rf }, log: [{ at: NOW, zone: 'KST', actor: '박서연', role: '회계', action: '8월 재개방 요청', field: rf.target, before: '마감', after: '재개방 요청', reason: rf.reason.trim() }].concat(log), notice: { tone: 'progress', title: '이도윤 대표에게 재개방 승인을 요청했습니다', body: '승인되면 알림이 오고, 그때부터 8월 자료를 고칠 수 있습니다. 보기 권한을 대표로 바꾸면 승인 화면을 볼 수 있습니다.' } });
      },
      approveReopen: () => this.setState({ augState: 'reopened', log: [{ at: NOW, zone: 'KST', actor: '이도윤', role: '대표', action: '8월 재개방 승인', field: s.req.target, before: '재개방 요청', after: '재개방', approver: '이도윤' }].concat(log), notice: { tone: 'attention', title: '8월을 재개방했습니다', body: '회계가 조정 후 다시 마감할 때까지 8월 보고서에는 「재개방 중」이 표시됩니다.' } }),
      denyReopen: () => this.setState({ augState: 'closed', log: [{ at: NOW, zone: 'KST', actor: '이도윤', role: '대표', action: '8월 재개방 반려', field: s.req.target, before: '재개방 요청', after: '마감 유지' }].concat(log), notice: { tone: 'critical', title: '재개방 요청을 반려했습니다', body: '8월은 마감 상태로 유지됩니다. 반려 사실이 요청자에게 전달됐습니다.' } }),
      reclose: () => this.setState({ augState: 'closed', req: null, log: [{ at: NOW, zone: 'KST', actor: '박서연', role: '회계', action: '8월 다시 마감', field: 'MN2608-019 정산 조정액', before: '0', after: `${s.adj} KRW`, reason: s.adjWhy, approver: '이도윤' }].concat(log), notice: { tone: 'positive', title: '8월을 다시 마감했습니다', body: '조정 전후 값과 사유가 마감 이력에 남았습니다.' } }),
      history: log,'''

state = '''{ role: '회계', month: '2026년 9월', augState: 'closed', reopenForm: false, req: null, rfError: '', notice: null, adj: '0', adjWhy: '',
      rf: { target: 'MN2608-019 · 누리투어 인센티브', impact: '', reason: '' },
      log: [
        { at: '2026-09-13T10:10', zone: 'KST', actor: '박서연', role: '회계', action: '8월 다시 마감', field: '8월 정산', before: '재개방', after: '마감', approver: '이도윤' },
        { at: '2026-09-12T16:40', zone: 'KST', actor: '이도윤', role: '대표', action: '8월 재개방 승인', field: '8월 정산', before: '마감', after: '재개방', reason: '한빛투어 과입금 1,200,000 KRW 상계 누락' },
        { at: '2026-09-05T18:00', zone: 'KST', actor: '박서연', role: '회계', action: '8월 마감', field: '8월 정산', before: '정산 확정', after: '마감', approver: '이도윤' }
      ] }'''
admin('Settlement.dc.html', '정산·마감', 'settlement', None, body, pre=pre, vals=vals, state=state, height=1620)
print('Settlement written')
