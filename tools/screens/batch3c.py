import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import *

# ------------------------------------------------------------------ Approvals (비용 승인, 단계별 권한)
body = header('비용 승인', '비용 등록 → 운영 확인 → 회계 검토 → 권한자 승인 → 지급·정산 반영 · 300,000 MNT 미만은 회계 검토로 확정', '''<span class="label" style="color: var(--ink-muted)">보기 권한</span>
<x-import component-from-global-scope="Abt.Segmented" options="{{roleOptions}}" value="{{role}}" on-change="{{setRole}}" aria-label="보기 권한"></x-import>''')
body += NOTICE
body += '''<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px">
<x-import component-from-global-scope="Abt.Segmented" options="{{filterOptions}}" value="{{filter}}" on-change="{{setFilter}}" aria-label="처리 상태"></x-import>
<span class="caption" style="color: var(--ink-muted)">{{listCaption}}</span>
</div>
<div style="display: grid; grid-template-columns: minmax(0, 1.45fr) minmax(380px, 1fr); gap: 16px; align-items: start">
<x-import component-from-global-scope="Abt.DataTable" columns="{{cols}}" rows="{{rows}}" on-row-click="{{pick}}" caption="비용 승인 목록" empty="{{emptyText}}"></x-import>
''' + SIDE_PANEL + '''<div style="display: flex; flex-direction: column; gap: 8px">
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 8px">
<div style="display: flex; align-items: center; gap: 8px"><x-import component-from-global-scope="Abt.EventCode" code="{{cur.code}}" href="EventDetail.dc.html"></x-import><span style="font: 500 12px/18px var(--font-mono); color: var(--ink-muted)">{{cur.no}}</span></div>
<x-import component-from-global-scope="Abt.StatusBadge" axis="cost" status="{{cur.status}}" size="md"></x-import>
</div>
<h2 class="title-2" style="margin: 0">{{cur.cat}} · {{cur.desc}}</h2>
<x-import component-from-global-scope="Abt.Money" amount="{{cur.amt}}" currency="MNT" size="lg" align="start" converted="{{cur.converted}}" rate="{{cur.rate}}"></x-import>
</div>
''' + dl([('발생 일시', '<x-import component-from-global-scope="Abt.DateTime" value="{{cur.at}}" zone="{{cur.zone}}" other="{{yes}}"></x-import>'), ('수량·단가', '{{cur.unit}}'), ('계약 단가', '{{cur.contract}}'), ('지급 수단', '{{cur.pay}}'), ('입력', '{{cur.by}}')], 96) + '''<div style="display: grid; grid-template-columns: 96px minmax(0, 1fr); gap: 12px; align-items: center; font-size: 13px">
<span class="label" style="color: var(--ink-muted)">증빙</span>
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px">
<sc-if value="{{cur.missing}}" hint-placeholder-val="{{false}}"><x-import component-from-global-scope="Abt.Attachment" kind="receipt" missing="{{yes}}"></x-import></sc-if>
<sc-if value="{{cur.hasFile}}" hint-placeholder-val="{{true}}"><button type="button" onClick="{{togglePreview}}" aria-expanded="{{previewOpen}}" style="padding: 0; border: 0; background: transparent; cursor: pointer; font: inherit; color: inherit"><x-import component-from-global-scope="Abt.Attachment" kind="receipt" name="{{cur.file}}" meta="{{cur.fileMeta}}"></x-import></button><span class="caption" style="color: var(--ink-muted)">{{previewHint}}</span></sc-if>
</div>
</div>
<sc-if value="{{previewOpen}}" hint-placeholder-val="{{false}}">
<figure style="margin: 0; display: flex; flex-direction: column; gap: 8px">
<div style="align-self: center; width: 240px; padding: 16px 18px; background: #f4f1ea; color: #1d1d1b; border-radius: 4px; box-shadow: var(--shadow-sm); font: 400 12px/18px var(--font-mono)">
<div style="text-align: center; font-weight: 600; font-size: 13px">{{cur.rcpt.vendor}}</div>
<div style="text-align: center; color: #5b5853">{{cur.rcpt.when}}</div>
<div style="border-top: 1px dashed #8a867e; margin: 8px 0"></div>
<sc-for list="{{cur.rcpt.lines}}" as="l" hint-placeholder-count="2"><div style="display: flex; justify-content: space-between; gap: 8px"><span>{{l.k}}</span><span>{{l.v}}</span></div></sc-for>
<div style="border-top: 1px dashed #8a867e; margin: 8px 0"></div>
<div style="display: flex; justify-content: space-between; font-weight: 600"><span>합계</span><span>{{cur.rcpt.total}}</span></div>
</div>
<figcaption class="caption" style="text-align: center; color: var(--ink-muted)">{{cur.file}} · 원본은 권한이 있는 사람만 내려받을 수 있습니다</figcaption>
</figure>
</sc-if>
<sc-if value="{{cur.hasRisk}}" hint-placeholder-val="{{true}}">
<x-import component-from-global-scope="Abt.Alert" tone="attention" title="{{cur.riskTitle}}">{{cur.riskBody}}</x-import>
</sc-if>
<x-import component-from-global-scope="Abt.ApprovalSteps" steps="{{cur.steps}}" orientation="vertical"></x-import>
<sc-if value="{{act.decide}}" hint-placeholder-val="{{true}}">
<div style="display: flex; flex-direction: column; gap: 12px; padding-top: 12px; border-top: 1px solid var(--line)">
<x-import component-from-global-scope="Abt.TextField" label="{{act.noteLabel}}" multiline="{{yes}}" rows="{{two}}" placeholder="반려하거나 보완을 요청하면 이 내용이 입력자에게 전달됩니다." value="{{note}}" on-change="{{setNote}}" error="{{noteError}}"></x-import>
<div style="display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 8px">
<x-import component-from-global-scope="Abt.Button" variant="danger" on-click="{{reject}}">반려</x-import>
<sc-if value="{{act.canSupplement}}" hint-placeholder-val="{{true}}"><x-import component-from-global-scope="Abt.Button" variant="secondary" on-click="{{supplement}}">보완 요청</x-import></sc-if>
<x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{approve}}">{{act.passLabel}}</x-import>
</div>
</div>
</sc-if>
<sc-if value="{{act.info}}" hint-placeholder-val="{{false}}">
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 8px; padding-top: 12px; border-top: 1px solid var(--line)">
<span class="caption" style="color: var(--ink-muted); flex: 1; min-width: 200px">{{act.infoText}}</span>
<sc-if value="{{act.canRemind}}" hint-placeholder-val="{{false}}"><x-import component-from-global-scope="Abt.Button" size="sm" on-click="{{remind}}">다시 알림</x-import></sc-if>
</div>
</sc-if>
</section>
</div>
'''

pre = '''
    const R = 0.3985;
    const ROLES = { '운영 확인': { name: '김지훈', role: '운영관리자', stage: 'ops' }, '회계 검토': { name: '박서연', role: '회계담당자', stage: 'acc' }, '권한자 승인': { name: '이도윤', role: '대표', stage: 'boss' } };
    const LIMIT = 300000;
    const role = s.role;
    const me = ROLES[role];
    const NOW = { ops: '10.01 16:30 KST', acc: '10.01 16:32 KST', boss: '10.01 16:35 KST' };
    const base = s.items;
    const stepsOf = (i) => {
      const order = ['ops', 'acc', 'boss', 'pay'];
      const names = { ops: '운영 확인', acc: '회계 검토', boss: '권한자 승인', pay: '지급·정산 반영' };
      const small = i.amt < LIMIT;
      const list = [{ label: '비용 등록', state: 'done', actor: i.by.split(' ')[0], at: `${i.at.slice(5, 7)}.${i.at.slice(8, 10)} ${i.at.slice(11, 16)} ${i.zone}` }];
      const idx = i.stage === 'done' ? 4 : order.indexOf(i.stage === 'supplement' ? i.back : i.stage === 'rejected' ? i.back : i.stage);
      order.forEach((st, k) => {
        const log = (i.log || {})[st] || {};
        let state = k < idx ? 'done' : k === idx ? 'current' : 'pending';
        if (st === 'boss' && small) state = k < idx || i.stage === 'done' ? 'skipped' : 'skipped';
        if (i.stage === 'supplement' && k === idx) state = 'current';
        if (i.stage === 'rejected' && k === idx) state = 'rejected';
        if (i.stage === 'done') state = st === 'boss' && small ? 'skipped' : 'done';
        list.push({ label: names[st], state, actor: log.actor || (state === 'current' ? { ops: '김지훈', acc: '박서연', boss: '이도윤', pay: '' }[st] : undefined), at: log.at, note: st === 'boss' && small ? `${fmt(LIMIT)} MNT 미만 · 회계 검토로 확정` : log.note });
      });
      return list;
    };
    const statusOf = (i) => (i.stage === 'done' ? 'approved' : i.stage === 'rejected' ? 'rejected' : i.stage === 'supplement' ? 'supplement' : i.stage === 'ops' ? 'submitted' : 'reviewing');
    const items = base;
    const mineList = items.filter((i) => i.stage === me.stage);
    const backList = items.filter((i) => i.stage === 'supplement');
    const filter = s.filter;
    const list = filter === '내 차례' ? mineList : filter === '보완 요청' ? backList : filter === '처리 완료' ? items.filter((i) => i.stage === 'done' || i.stage === 'rejected') : items;
    const cur = items.find((i) => i.id === s.selected) || items[0];
    const total = list.reduce((a, i) => a + i.amt, 0);
    const selfBlock = cur.stage === me.stage && cur.by.startsWith(me.name);
    const canAct = cur.stage === me.stage && !selfBlock;
    const decide = (kind) => {
      const note = (s.note || '').trim();
      if ((kind === 'rejected' || kind === 'supplement') && !note) { set({ noteError: kind === 'rejected' ? '반려 사유를 입력해 주세요.' : '보완할 내용을 입력해 주세요.' }); return; }
      const st = cur.stage;
      let next = st;
      if (kind === 'pass') next = st === 'ops' ? 'acc' : st === 'acc' ? (cur.amt < LIMIT ? 'done' : 'boss') : 'done';
      if (kind === 'rejected') next = 'rejected';
      if (kind === 'supplement') next = 'supplement';
      const log = { ...(cur.log || {}), [st]: { actor: me.name, at: NOW[st], note: note || undefined } };
      if (next === 'done') log.pay = { actor: '시스템', at: NOW[st], note: '정산에 반영' };
      const prev = items;
      const msg = {
        pass: next === 'acc' ? ['운영 확인을 마쳤습니다', '회계 검토로 넘어갔습니다.'] : next === 'boss' ? ['회계 검토를 마쳤습니다', '권한자(이도윤) 승인을 기다립니다. 승인 전까지 정산에 반영되지 않습니다.'] : ['승인했습니다', '지급·정산에 반영됐습니다. 행사 손익이 다시 계산됩니다.'],
        rejected: ['반려했습니다', '사유가 입력자에게 전달됐습니다. 이 금액은 정산에 반영되지 않습니다.'],
        supplement: ['보완을 요청했습니다', '입력자가 영수증이나 사유를 보완하면 같은 단계로 돌아옵니다.']
      }[kind];
      this.setState({ items: items.map((i) => (i.id === cur.id ? { ...i, stage: next, back: kind === 'pass' ? i.back : st, log } : i)), note: '', noteError: '', previewOpen: false, notice: { tone: kind === 'pass' ? (next === 'done' ? 'positive' : 'progress') : kind === 'rejected' ? 'critical' : 'attention', title: `${cur.no} · ${msg[0]}`, body: msg[1], action: { label: '되돌리기', onClick: () => this.setState({ items: prev, notice: null }) } } });
    };
'''
vals = '''      user: { name: me.name, role: me.role },
      roleOptions: ['운영 확인', '회계 검토', '권한자 승인'],
      role,
      setRole: (v) => set({ role: v, filter: '내 차례', note: '', noteError: '' }),
      navCounts: { alerts: 5, field: 2, claims: { n: 2, tone: 'critical' }, receipts: { n: 1, tone: 'critical' }, costs: { n: items.filter((i) => ['ops', 'acc', 'boss'].includes(i.stage)).length, tone: 'attention' }, remit: 3 },
      filterOptions: [ { value: '내 차례', label: `내 차례 ${mineList.length}` }, { value: '보완 요청', label: `보완 요청 ${backList.length}` }, { value: '처리 완료', label: '처리 완료' }, { value: '전체', label: '전체' } ],
      filter,
      setFilter: (v) => set({ filter: v }),
      listCaption: `${filter} ${list.length}건 · ${fmt(total)} MNT · 행을 누르면 오른쪽에서 처리합니다`,
      emptyText: filter === '내 차례' ? `${role} 단계에서 처리할 비용이 없습니다.` : '해당하는 비용이 없습니다.',
      cols: [
        { key: 'code', label: '행사코드', type: 'code' },
        { key: 'what', label: '항목 / 내용', type: 'stack' },
        { key: 'amt', label: '금액', type: 'money', currency: 'MNT' },
        { key: 'status', label: '단계', type: 'status', axis: 'cost' },
        { key: 'flags', label: '검토 후보', type: 'flags' }
      ],
      rows: list.map((i) => ({ id: i.id, code: i.code, href: 'EventDetail.dc.html', what: { primary: i.cat, secondary: i.desc }, amt: i.amt, status: statusOf(i), flags: i.flags, selected: i.id === cur.id })),
      pick: (row) => set({ selected: row.id, note: '', noteError: '', previewOpen: false }),
      cur: { ...cur, status: statusOf(cur), steps: stepsOf(cur), converted: { amount: Math.round(cur.amt * R), currency: 'KRW' }, rate: { value: R, date: `${cur.at.slice(5, 7)}.${cur.at.slice(8, 10)}` }, hasRisk: !!cur.riskTitle, missing: !!cur.missing, hasFile: !cur.missing, file: cur.file || '', fileMeta: cur.fileMeta || '', rcpt: cur.rcpt || { vendor: '', when: '', lines: [], total: '' } },
      previewOpen: !!s.previewOpen,
      previewHint: s.previewOpen ? '누르면 닫힘' : '누르면 미리보기',
      togglePreview: () => set({ previewOpen: !s.previewOpen }),
      act: {
        decide: canAct,
        canSupplement: cur.stage !== 'boss',
        passLabel: cur.stage === 'ops' ? '운영 확인' : cur.stage === 'acc' ? (cur.amt < LIMIT ? '검토 완료 · 확정' : '검토 완료') : '승인',
        noteLabel: cur.stage === 'boss' ? '승인 의견' : '검토 의견',
        info: !canAct,
        infoText: selfBlock ? `본인(${me.name})이 등록한 비용은 직접 확인할 수 없습니다. 다른 운영관리자(정하린)에게 확인 요청이 갔습니다.` : cur.stage === 'supplement' ? '입력자의 보완을 기다립니다. 보완되면 요청한 단계로 돌아옵니다.' : cur.stage === 'done' ? '승인되어 정산에 반영됐습니다.' : cur.stage === 'rejected' ? '반려된 비용입니다. 정산에 반영되지 않습니다.' : `이 단계는 ${{ ops: '운영 확인(김지훈)', acc: '회계 검토(박서연)', boss: '권한자 승인(이도윤)' }[cur.stage]} 권한입니다. 지금 보기 권한: ${role}.`,
        canRemind: cur.stage === 'supplement' || selfBlock
      },
      remind: () => say('progress', `${cur.no} 다시 알렸습니다`, selfBlock ? '정하린에게 확인 요청 알림을 다시 보냈습니다.' : `${cur.by.split(' ')[0]}에게 보완 요청 알림을 다시 보냈습니다. 기한을 넘기면 운영관리자에게 보고됩니다.`),
      note: s.note,
      setNote: (e) => set({ note: e.target.value, noteError: '' }),
      noteError: s.noteError || '',
      approve: () => decide('pass'),
      reject: () => decide('rejected'),
      supplement: () => decide('supplement'),'''

ITEMS = '''[
        { id: 'q1', no: 'CO-0924-11', code: 'MN2609-033', cat: '식사', desc: '고비 오아시스 캠프 저녁(21인)', amt: 525000, by: '바트-에르덴 (가이드)', at: '2026-09-24T21:10', zone: 'ULAT', stage: 'acc', flags: ['duplicate'], unit: '21명 × 25,000 MNT', contract: '25,000 MNT (일치)', pay: '가이드 현금', file: 'IMG_4471.jpg', fileMeta: '1.4 MB', riskTitle: '중복 청구 후보', riskBody: 'CO-0924-07(09.24 21:02 입력, 승인됨)과 업체·날짜·금액이 같습니다. 같은 식사를 두 번 올렸는지 가이드에게 확인하세요. 자동으로 부정으로 판정하지 않습니다.', log: { ops: { actor: '김지훈', at: '09.25 09:30 KST' } }, rcpt: { vendor: 'GOBI OASIS CAMP', when: '2026-09-24 20:58', lines: [ { k: 'Dinner set × 21', v: '525,000' } ], total: '525,000 MNT' } },
        { id: 'q2', no: 'CO-0925-09', code: 'MN2609-033', cat: '차량·유류', desc: '유류 보충(달란자드가드)', amt: 780000, by: '바트-에르덴 (가이드)', at: '2026-09-25T18:40', zone: 'ULAT', stage: 'acc', flags: ['overrun'], unit: '260 L × 3,000 MNT', contract: '해당 없음', pay: '가이드 현금', file: 'IMG_4490.jpg', fileMeta: '1.1 MB', riskTitle: '예산 초과: 차량·유류 107%', riskBody: '사유: 도로 공사로 우회(+140 km). 운영 김지훈 확인함.', log: { ops: { actor: '김지훈', at: '09.26 10:05 KST' } }, rcpt: { vendor: 'PETROVIS DALANZADGAD', when: '2026-09-25 18:31', lines: [ { k: 'AI-92 260 L', v: '780,000' } ], total: '780,000 MNT' } },
        { id: 'q7', no: 'CO-1001-02', code: 'MN2610-002', cat: '차량·유류', desc: '푸르공 3대 × 6일', amt: 7560000, by: '김지훈 (운영)', at: '2026-10-01T07:50', zone: 'KST', stage: 'acc', flags: ['rate-diff'], unit: '3대 × 6일 × 420,000 MNT', contract: '400,000 MNT/일 (2026 동계 요금표)', pay: '협력업체 송금', file: '고비모터스_청구서.pdf', fileMeta: '220 KB', riskTitle: '단가 차이', riskBody: '청구 단가 420,000 MNT/일이 계약 단가 400,000 MNT/일보다 높습니다. 차액 360,000 MNT는 과입·차감 원장에 차감 후보로 올라가 있습니다.', log: { ops: { actor: '정하린', at: '10.01 09:10 KST', note: '본인 등록 건이라 정하린 확인' } }, rcpt: { vendor: 'GOBI MOTORS LLC', when: '2026-09-30 청구서', lines: [ { k: 'Furgon 3 × 6d', v: '420,000/d' } ], total: '7,560,000 MNT' } },
        { id: 'q10', no: 'CO-0925-14', code: 'MN2609-031', cat: '숙박', desc: '홉스골 숙소 추가 1박(온수 문제로 이동)', amt: 1850000, by: '간바타르 (가이드)', at: '2026-09-25T20:15', zone: 'ULAT', stage: 'boss', flags: ['overrun'], unit: '게르 7동 × 1박', contract: '265,000 MNT/동 (일치)', pay: '협력업체 송금', file: '하트갈_게스트하우스.pdf', fileMeta: '180 KB', riskTitle: '긴급 선집행 · 사후 승인', riskBody: '온수 문제로 일부 고객을 옮겨 먼저 결제했습니다. 사후 승인 기한 10.02.', log: { ops: { actor: '김지훈', at: '09.26 09:00 KST' }, acc: { actor: '박서연', at: '09.30 14:20 KST', note: '계약 단가 일치 확인' } }, rcpt: { vendor: 'KHATGAL GUESTHOUSE', when: '2026-09-25 20:02', lines: [ { k: 'Ger × 7 · 1 night', v: '1,855,000' }, { k: 'Discount', v: '−5,000' } ], total: '1,850,000 MNT' } },
        { id: 'q5', no: 'CO-0930-03', code: 'MN2609-040', cat: '관광·입장', desc: '국립박물관 입장(10인)', amt: 300000, by: '오윤치메그 (가이드)', at: '2026-09-30T16:20', zone: 'ULAT', stage: 'ops', flags: [], unit: '10명 × 30,000 MNT', contract: '30,000 MNT (일치)', pay: '가이드 현금', file: 'IMG_5102.jpg', fileMeta: '0.9 MB', rcpt: { vendor: 'NATIONAL MUSEUM OF MONGOLIA', when: '2026-09-30 16:12', lines: [ { k: 'Adult × 10', v: '300,000' } ], total: '300,000 MNT' } },
        { id: 'q6', no: 'CO-1001-01', code: 'MN2609-038', cat: '식사', desc: '테를지 리버 캠프 조식 추가(3인)', amt: 90000, by: '간바타르 (가이드)', at: '2026-10-01T08:15', zone: 'ULAT', stage: 'ops', flags: [], unit: '3명 × 30,000 MNT', contract: '30,000 MNT (일치)', pay: '가이드 현금', file: 'IMG_5133.jpg', fileMeta: '1.0 MB', rcpt: { vendor: 'TERELJ RIVER CAMP', when: '2026-10-01 07:58', lines: [ { k: 'Breakfast × 3', v: '90,000' } ], total: '90,000 MNT' } },
        { id: 'q8', no: 'CO-1001-03', code: 'MN2609-031', cat: '보상·기타', desc: 'CL2609-004 온수 미공급 보상', amt: 240000, by: '김지훈 (운영)', at: '2026-10-01T15:55', zone: 'KST', stage: 'ops', flags: [], unit: '1인 10,000 MNT × 24명', contract: '보상 기준표(숙소 시설)', pay: '여행사 정산 시 차감', file: '보상_합의서.pdf', fileMeta: '140 KB', rcpt: { vendor: '보상 합의서', when: '2026-10-01', lines: [ { k: '24명 × 10,000', v: '240,000' } ], total: '240,000 MNT' } },
        { id: 'q3', no: 'CO-0925-05', code: 'MN2609-031', cat: '차량·유류', desc: '유류(무릉)', amt: 340000, by: '간바타르 (가이드)', at: '2026-09-25T12:05', zone: 'ULAT', stage: 'supplement', back: 'acc', flags: ['missing-proof'], unit: '113 L × 3,000 MNT', contract: '해당 없음', pay: '가이드 현금', missing: true, riskTitle: '증빙 누락', riskBody: '영수증 사진이 없습니다. 09.30에 가이드에게 보완을 요청했습니다.', log: { ops: { actor: '김지훈', at: '09.27' }, acc: { actor: '박서연', at: '09.30', note: '영수증 보완 요청' } } },
        { id: 'q4', no: 'CO-0926-02', code: 'MN2609-031', cat: '차량·유류', desc: '유류(하트갈)', amt: 270000, by: '간바타르 (가이드)', at: '2026-09-26T09:30', zone: 'ULAT', stage: 'supplement', back: 'acc', flags: ['missing-proof'], unit: '90 L × 3,000 MNT', contract: '해당 없음', pay: '가이드 현금', missing: true, riskTitle: '증빙 누락', riskBody: '영수증 사진이 없습니다. 09.30에 가이드에게 보완을 요청했습니다.', log: { ops: { actor: '김지훈', at: '09.27' }, acc: { actor: '박서연', at: '09.30', note: '영수증 보완 요청' } } },
        { id: 'q9', no: 'CO-0926-03', code: 'MN2609-033', cat: '보상·기타', desc: '캠프 온수 고장 보상(1박 환불)', amt: 2260000, by: '김지훈 (운영)', at: '2026-09-26T09:15', zone: 'ULAT', stage: 'done', flags: [], unit: '1박 숙박비', contract: '보상 기준표(숙소 시설)', pay: '여행사 환불', file: '환불_확인서.pdf', fileMeta: '120 KB', log: { ops: { actor: '정하린', at: '09.26' }, acc: { actor: '박서연', at: '09.26' }, boss: { actor: '이도윤', at: '09.26' }, pay: { actor: '시스템', at: '09.26' } }, rcpt: { vendor: '환불 확인서', when: '2026-09-26', lines: [ { k: '1 night refund', v: '2,260,000' } ], total: '2,260,000 MNT' } }
      ]'''
state = "{ role: '회계 검토', filter: '내 차례', selected: 'q1', note: '', noteError: '', previewOpen: false, notice: null, items: " + ITEMS + " }"
admin('Approvals.dc.html', '비용 승인', 'costs', None, body, pre=pre, vals=vals, state=state, height=1300)
print('Approvals written')
