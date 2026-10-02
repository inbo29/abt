import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import *
from shared_data import MANUALS_BASE_JS

H2 = '<h2 class="m-label" style="margin: 0; font-weight: 600">{}</h2>'
BTN2 = 'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px'

# ------------------------------------------------------------------ GuideToday (오늘)
body = '''<header style="display: flex; align-items: flex-end; justify-content: space-between; gap: 12px">
<div style="display: flex; flex-direction: column; gap: 2px">
<h1 class="m-title" style="margin: 0">오늘</h1>
<p class="m-caption" style="margin: 0; color: var(--ink-muted)">10.01(목) 14:40 ULAT</p>
</div>
<p class="m-label" style="margin: 0; color: var(--ink-muted)">간바타르 가이드</p>
</header>
''' + NOTICE + MCARD + '''
<div style="display: flex; align-items: center; justify-content: space-between; gap: 8px">
<x-import component-from-global-scope="Abt.EventCode" code="MN2609-038"></x-import>
<x-import component-from-global-scope="Abt.StatusBadge" axis="event" status="in-progress" size="md"></x-import>
</div>
<h2 class="m-body" style="margin: 0; font-weight: 600">제이원트래블 · 테를지 승마·게르 2박 3일</h2>
<p class="m-label" style="margin: 0; color: var(--ink-muted); font-weight: 400">3일차 · 마지막 날 · 14+1명 · 기사 바트볼드(25인승 버스)</p>
<div style="''' + BTN2 + '''; padding-top: 4px">
<div style="display: flex; flex-direction: column; gap: 2px; padding: 10px 12px; background: var(--surface-sunken); border-radius: 6px"><span class="m-caption" style="color: var(--ink-muted)">공항 도착</span><span class="m-body" style="font-weight: 600">19:10</span></div>
<div style="display: flex; flex-direction: column; gap: 2px; padding: 10px 12px; background: var(--surface-sunken); border-radius: 6px"><span class="m-caption" style="color: var(--ink-muted)">출국 OM302</span><span class="m-body" style="font-weight: 600">21:40</span></div>
</div>
<x-import component-from-global-scope="Abt.Button" size="lg" block="{{yes}}" href="GuideBriefing.dc.html">브리핑 보기</x-import>
</section>

<x-import component-from-global-scope="Abt.Alert" tone="critical" title="견과류 알레르기 1명 · 채식 2명">공항 가는 길 저녁 도시락 주문에 반영했는지 확인하세요.</x-import>

''' + MCARD + '''
<div style="display: flex; align-items: baseline; justify-content: space-between; gap: 8px">''' + H2.format('일정 체크') + '''<span class="m-caption" style="color: var(--ink-muted)">{{checkCaption}}</span></div>
<sc-if value="{{hasCurrent}}" hint-placeholder-val="{{true}}">
<p class="m-body" style="margin: 0; font-weight: 600">{{curStop}}</p>
<x-import component-from-global-scope="Abt.TextField" label="확인 인원" size="lg" input-mode="numeric" suffix="명 / 15명" align="end" value="{{head}}" on-change="{{setHead}}" error="{{headError}}"></x-import>
<sc-if value="{{missing}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.TextField" label="불참·변경 사유" size="lg" placeholder="예: 1명 컨디션 난조로 버스 대기" value="{{why}}" on-change="{{setWhy}}"></x-import>
</sc-if>
<x-import component-from-global-scope="Abt.Button" size="lg" variant="primary" block="{{yes}}" on-click="{{done}}">방문 완료</x-import>
</sc-if>
<sc-if value="{{allDone}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.Alert" tone="positive" title="오늘 일정을 모두 체크했습니다" action="{{reportAction}}">출국 뒤 완료 보고를 제출하세요.</x-import>
</sc-if>
<x-import component-from-global-scope="Abt.ApprovalSteps" steps="{{plan}}" orientation="vertical"></x-import>
</section>

<section style="display: flex; flex-direction: column; gap: 10px">
''' + H2.format('현장 등록') + '''
<div style="''' + BTN2 + '''">
<x-import component-from-global-scope="Abt.Button" size="lg" href="GuideExpense.dc.html">현장 비용</x-import>
<x-import component-from-global-scope="Abt.Button" size="lg" href="GuideOption.dc.html">옵션 판매</x-import>
<x-import component-from-global-scope="Abt.Button" size="lg" href="GuideIncident.dc.html">사고·클레임 보고</x-import>
<x-import component-from-global-scope="Abt.Button" size="lg" href="GuideReport.dc.html">완료 보고</x-import>
</div>
</section>

<section style="display: flex; flex-direction: column; padding: 4px 16px; background: var(--surface); border: 1px solid var(--line); border-radius: 12px">
<sc-for list="{{contacts}}" as="c" hint-placeholder-count="2">
<div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; min-height: 64px; border-top: {{c.border}}">
<div style="display: flex; flex-direction: column; gap: 2px"><span class="m-body" style="font-weight: 600">{{c.name}}</span><span class="m-caption" style="color: var(--ink-muted)">{{c.meta}}</span></div>
<x-import component-from-global-scope="Abt.Button" on-click="{{c.call}}">{{c.label}}</x-import>
</div>
</sc-for>
</section>
'''
pre = '''
    const PLAN = [
      { label: '07:30 조식', actor: '테를지 리버 캠프' },
      { label: '09:00 승마 체험 2시간', actor: '옵션 추가 3명 판매' },
      { label: '12:30 점심', actor: '캠프 식당' },
      { label: '15:00 거북바위 · 아리야발 사원', note: '사원 계단 108개 · 70대 2명은 아래 전망대 안내' },
      { label: '17:00 울란바토르로 출발', note: '시간 변경됨 · 17:30 → 17:00' },
      { label: '19:10 칭기즈칸 국제공항', note: '출국 OM302 21:40' }
    ];
    const idx = s.idx;
    const logs = s.logs;
    const head = s.head;
    const n = Number(String(head).replace(/[^0-9]/g, '')) || 0;
'''
vals = '''      checkCaption: idx < PLAN.length ? `${idx + 1}/${PLAN.length} 일정` : '모두 완료',
      hasCurrent: idx < PLAN.length,
      allDone: idx >= PLAN.length,
      curStop: idx < PLAN.length ? `지금: ${PLAN[idx].label}` : '',
      head,
      setHead: (e) => set({ head: e.target.value, headError: '' }),
      headError: s.headError || '',
      missing: n > 0 && n < 15,
      why: s.why,
      setWhy: (e) => set({ why: e.target.value }),
      done: () => {
        if (!n) { set({ headError: '확인한 인원을 적어 주세요.' }); return; }
        if (n < 15 && !s.why.trim()) { set({ headError: '불참 사유를 함께 남겨 주세요.' }); return; }
        const t = ['15:42', '17:02', '19:12'][Math.min(idx - 3, 2)] || '15:42';
        this.setState({ idx: idx + 1, logs: { ...logs, [idx]: `${t} 완료 · ${n}명${n < 15 ? ' · ' + s.why.trim() : ''}` }, head: '15', why: '', notice: { tone: n < 15 ? 'attention' : 'positive', title: `${PLAN[idx].label.slice(6)} · 체크 완료`, body: n < 15 ? `${15 - n}명 불참을 운영팀에 알렸습니다.` : '인원 15명 확인 · 운영팀 화면에 바로 보입니다.' } });
      },
      reportAction: { label: '완료 보고', href: 'GuideReport.dc.html' },
      plan: PLAN.map((p, i) => ({ label: p.label, state: i < idx ? 'done' : i === idx ? 'current' : 'pending', actor: logs[i] || p.actor, note: i >= idx ? p.note : undefined })),
      contacts: [
        { name: '기사 바트볼드', meta: s.call === 'd' ? '+976 9922-1810 · 전화 앱으로 연결합니다' : '25인승 버스 · 15-88 УБЕ', label: s.call === 'd' ? '전화 거는 중' : '전화', call: () => set({ call: 'd' }), border: '0' },
        { name: '운영 김지훈', meta: s.call === 'o' ? '+82 10-4471-2741 · 전화 앱으로 연결합니다' : '긴급 연락 · 한국 시간 +1시간', label: s.call === 'o' ? '전화 거는 중' : '전화', call: () => set({ call: 'o' }), border: '1px solid var(--line)' }
      ],'''
state = "{ idx: 3, logs: { 0: '07:35 완료 · 15명', 1: '11:05 완료 · 15명 · 옵션 3명', 2: '13:20 완료 · 15명' }, head: '15', why: '', headError: '', call: null, notice: null }"
mobile('GuideToday.dc.html', '가이드 오늘', 'today', body, pre=pre, vals=vals, state=state)
print('GuideToday written')


# ------------------------------------------------------------------ GuideSchedule (내 일정)
body = mhead('내 일정', back=None, caption='간바타르 · 배정 변경은 확인을 눌러야 운영팀에 전달됩니다') + NOTICE + '''
<x-import component-from-global-scope="Abt.Segmented" options="{{viewOptions}}" value="{{view}}" on-change="{{setView}}" aria-label="보기"></x-import>
<sc-for list="{{asks}}" as="a" hint-placeholder-count="1">
<x-import component-from-global-scope="Abt.Alert" tone="attention" title="{{a.title}}" action="{{a.action}}">{{a.body}}</x-import>
</sc-for>
<sc-if value="{{isList}}" hint-placeholder-val="{{true}}">
<section style="display: flex; flex-direction: column; gap: 10px">
<sc-for list="{{items}}" as="i" hint-placeholder-count="4">
''' + MCARD + '''
<div style="display: flex; align-items: center; justify-content: space-between; gap: 8px"><span class="m-label" style="font-weight: 600">{{i.when}}</span><x-import component-from-global-scope="Abt.StatusBadge" tone="{{i.tone}}" form="{{i.form}}">{{i.stLabel}}</x-import></div>
<span class="m-body">{{i.title}}</span>
<span class="m-caption" style="color: var(--ink-muted)">{{i.meta}}</span>
<sc-if value="{{i.ask}}" hint-placeholder-val="{{false}}">
<div style="''' + BTN2 + '''"><x-import component-from-global-scope="Abt.Button" size="lg" block="{{yes}}" on-click="{{i.decline}}">어려움</x-import><x-import component-from-global-scope="Abt.Button" size="lg" variant="primary" block="{{yes}}" on-click="{{i.accept}}">배정 수락</x-import></div>
</sc-if>
</section>
</sc-for>
</section>
</sc-if>
<sc-if value="{{isMonth}}" hint-placeholder-val="{{false}}">
''' + MCARD + '''
<div style="display: flex; justify-content: space-between"><span class="m-label" style="font-weight: 600">2026년 10월</span><span class="m-caption" style="color: var(--ink-muted)">배정 {{monthCount}}일 · 불가 {{offCount}}일</span></div>
<div style="display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 4px">
<sc-for list="{{dows}}" as="d" hint-placeholder-count="7"><span class="m-caption" style="text-align: center; color: var(--ink-muted)">{{d}}</span></sc-for>
<sc-for list="{{cells}}" as="c" hint-placeholder-count="35"><span style="box-sizing: border-box; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 6px; font: 500 14px/1 var(--font-sans); background: {{c.bg}}; border: {{c.border}}; color: {{c.color}}">{{c.label}}</span></sc-for>
</div>
<div style="display: flex; flex-wrap: wrap; gap: 12px"><span class="m-caption" style="display: inline-flex; align-items: center; gap: 6px"><span style="width: 14px; height: 14px; border-radius: 3px; background: var(--surface-selected); border: 1px solid var(--line-strong)"></span>배정</span><span class="m-caption" style="display: inline-flex; align-items: center; gap: 6px"><span style="width: 14px; height: 14px; border-radius: 3px; border: 1px dashed var(--line-strong)"></span>가배정</span><span class="m-caption" style="display: inline-flex; align-items: center; gap: 6px"><span style="width: 14px; height: 14px; border-radius: 3px; background: repeating-linear-gradient(135deg, var(--surface-sunken) 0 4px, var(--line) 4px 5px)"></span>배정 불가</span></div>
</section>
</sc-if>
''' + MCARD + H2.format('배정 불가일 등록') + '''
<div style="''' + BTN2 + '''">
<x-import component-from-global-scope="Abt.TextField" label="시작" type="date" value="{{off.from}}" on-change="{{onOff.from}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="끝" type="date" value="{{off.to}}" on-change="{{onOff.to}}" error="{{offError}}"></x-import>
</div>
<x-import component-from-global-scope="Abt.Select" label="사유" size="lg" options="{{reasonOptions}}" value="{{off.why}}" on-change="{{onOff.why}}" help="사유는 운영관리자만 봅니다"></x-import>
<x-import component-from-global-scope="Abt.Button" size="lg" block="{{yes}}" on-click="{{addOff}}">등록</x-import>
</section>
'''
pre = '''
    const OFFS = (() => { const v = store.get('offs', null); return v == null ? s.localOffs : v; })();
    const RE = (() => { const v = store.get('guideReplies', null); return v == null ? s.localReplies : v; })();
    const codeOf = (a) => a.title.split(' · ')[0];
    const mine = (OFFS.g3 || []).map((o, k) => ({ id: 'so' + k, from: o.from, to: o.to, title: `배정 불가 · ${o.why}`, meta: '배정 캘린더에 표시됨 · 이 기간에는 배정 후보에서 빠집니다', st: 'off' }));
    const A = s.items.map((a) => (a.st === 'ask' && RE[codeOf(a)] ? { ...a, st: RE[codeOf(a)] } : a)).concat(mine).sort((x, y) => (x.from < y.from ? -1 : 1));
    const reply = (a, v, notice) => { const next = { ...RE, [codeOf(a)]: v }; store.put('guideReplies', next); this.setState({ localReplies: next, notice }); };
    const lab = (iso) => `${iso.slice(5, 7)}.${iso.slice(8, 10)}`;
    const ST = { progress: ['진행 중', 'progress', 'solid'], ask: ['가배정 · 확인 요청', 'neutral', 'dashed'], ok: ['가이드 확인', 'positive', 'solid'], off: ['배정 불가', 'neutral', 'dashed'], declined: ['어려움 전달', 'attention', 'solid'] };
    const inRange = (d, a) => d >= a.from && d <= a.to;
    const off = s.off;
'''
vals = '''      viewOptions: ['목록', '월'],
      view: s.view,
      setView: (v) => set({ view: v }),
      isList: s.view === '목록',
      isMonth: s.view === '월',
      asks: s.changeAcked ? [] : [{ title: '변경 확인 필요: MN2610-012 집합 시간', body: '10.08 호텔 집합 07:30 → 06:30 · 운영 김지훈 10.01 13:10', action: { label: '확인함', onClick: () => set({ changeAcked: true, notice: { tone: 'positive', title: '변경을 확인했습니다', body: '운영팀 화면에 확인 시각이 남았습니다.' } }) } }],
      items: A.map((a) => ({ when: a.from === a.to ? lab(a.from) : `${lab(a.from)} – ${lab(a.to)}`, title: a.title, meta: a.meta, stLabel: ST[a.st][0], tone: ST[a.st][1], form: ST[a.st][2], ask: a.st === 'ask', accept: () => reply(a, 'ok', { tone: 'positive', title: `${codeOf(a)} 배정을 수락했습니다`, body: '운영팀 배정 캘린더에서 가이드 확인(실선)으로 바뀝니다.' }), decline: () => reply(a, 'declined', { tone: 'attention', title: '어렵다고 전달했습니다', body: '운영팀 배정 캘린더에 「어려움 전달」로 표시됩니다. 운영관리자가 다른 가이드를 찾습니다.' }) })),
      dows: ['일', '월', '화', '수', '목', '금', '토'],
      cells: Array.from({ length: 4 }, () => ({ label: '', bg: 'transparent', border: '0', color: 'var(--ink)' })).concat(Array.from({ length: 31 }, (_, i) => { const d = `2026-10-${String(i + 1).padStart(2, '0')}`; const a = A.find((x) => inRange(d, x)); const today = i === 0; const bg = !a ? 'transparent' : a.st === 'off' ? 'repeating-linear-gradient(135deg, var(--surface-sunken) 0 4px, var(--line) 4px 5px)' : a.st === 'ask' ? 'transparent' : 'var(--surface-selected)'; const border = today ? '2px solid var(--ink)' : a && a.st === 'ask' ? '1px dashed var(--line-strong)' : a && a.st !== 'off' ? '1px solid var(--line-strong)' : '1px solid transparent'; return { label: String(i + 1), bg, border, color: a && a.st === 'off' ? 'var(--ink-muted)' : 'var(--ink)' }; })),
      monthCount: A.filter((a) => a.st !== 'off' && a.st !== 'declined').reduce((n, a) => n + (Number(a.to.slice(8)) - Number(a.from.slice(8)) + 1), 0),
      offCount: A.filter((a) => a.st === 'off').reduce((n, a) => n + (Number(a.to.slice(8)) - Number(a.from.slice(8)) + 1), 0),
      reasonOptions: ['연차', '개인 일정', '교육', '건강'],
      off,
      onOff: { from: (e) => set({ off: { ...s.off, from: e.target.value }, offError: '' }), to: (e) => set({ off: { ...s.off, to: e.target.value }, offError: '' }), why: (e) => set({ off: { ...s.off, why: e.target.value } }) },
      offError: s.offError || '',
      addOff: () => {
        if (!off.from || !off.to || off.to < off.from) { set({ offError: '끝 날짜가 시작보다 빠릅니다.' }); return; }
        const clash = A.find((a) => a.st !== 'off' && a.st !== 'declined' && !(off.to < a.from || off.from > a.to));
        if (clash) { set({ offError: `${clash.title.split(' · ')[0]} 배정과 겹칩니다. 운영팀에 먼저 전화하세요.` }); return; }
        const next = { ...OFFS, g3: (OFFS.g3 || []).concat([{ from: off.from, to: off.to, why: off.why }]) };
        store.put('offs', next);
        this.setState({ localOffs: next, notice: { tone: 'positive', title: `${lab(off.from)} – ${lab(off.to)} 배정 불가일을 등록했습니다`, body: '운영팀 배정 캘린더와 가이드·차량 화면에 바로 표시됩니다.' } });
      },'''
state = '''{ view: '목록', changeAcked: false, offError: '', notice: null, localOffs: {}, localReplies: {}, off: { from: '2026-10-20', to: '2026-10-21', why: '개인 일정' },
      items: [
        { id: 'a1', from: '2026-09-29', to: '2026-10-01', title: 'MN2609-038 · 테를지 승마·게르 2박 3일', meta: '제이원트래블 · 14+1명 · 오늘 21:40 출국', st: 'progress' },
        { id: 'a2', from: '2026-10-02', to: '2026-10-03', title: '휴무', meta: '등록 09.20 · 승인됨', st: 'off' },
        { id: 'a3', from: '2026-10-08', to: '2026-10-12', title: 'MN2610-012 · 기업 인센티브 4박 5일', meta: '누리투어 · 32+2명 · 가이드 2명 중 리드 · 집합 06:30', st: 'ask' },
        { id: 'a4', from: '2026-10-22', to: '2026-10-25', title: 'MN2610-024 · 울란바토르 시티', meta: '여행사 취소로 배정 해제됨(09.29)', st: 'declined' }
      ] }'''
mobile('GuideSchedule.dc.html', '가이드 내 일정', 'schedule', body, pre=pre, vals=vals, state=state)
print('GuideSchedule written')


# ------------------------------------------------------------------ GuideAdd (현장 등록 선택)
body = mhead('현장 등록', back=None, code='MN2609-038', caption='무엇을 등록할까요? 통신이 끊겨도 임시저장해 두면 이어서 제출할 수 있습니다') + '''
<section style="display: flex; flex-direction: column; gap: 10px">
<sc-for list="{{kinds}}" as="k" hint-placeholder-count="5">
<a href="{{k.href}}" style="display: flex; flex-direction: column; gap: 4px; padding: 16px; min-height: 72px; box-sizing: border-box; background: var(--surface); border: 1px solid {{k.border}}; border-radius: 12px; text-decoration: none; color: var(--ink)">
<span class="m-body" style="font-weight: 600">{{k.title}}</span>
<span class="m-caption" style="color: var(--ink-muted)">{{k.desc}}</span>
</a>
</sc-for>
</section>
''' + MCARD + H2.format('임시저장 2건') + '''
<sc-for list="{{drafts}}" as="d" hint-placeholder-count="2">
<a href="{{d.href}}" style="display: flex; align-items: center; justify-content: space-between; gap: 12px; min-height: 52px; border-top: 1px solid var(--line); text-decoration: none; color: var(--ink)"><span style="display: flex; flex-direction: column; gap: 2px"><span class="m-body">{{d.title}}</span><span class="m-caption" style="color: var(--ink-muted)">{{d.meta}}</span></span><x-import component-from-global-scope="Abt.StatusBadge" axis="cost" status="draft"></x-import></a>
</sc-for>
</section>
'''
vals = '''      kinds: [
        { title: '사고·클레임 보고', desc: '긴급이면 운영 책임자에게 바로 전화·알림이 갑니다', href: 'GuideIncident.dc.html', border: 'var(--critical)' },
        { title: '현장 비용', desc: '사용처·금액·통화·영수증 사진', href: 'GuideExpense.dc.html', border: 'var(--line)' },
        { title: '옵션 판매', desc: '옵션·인원·단가·수금·취소', href: 'GuideOption.dc.html', border: 'var(--line)' },
        { title: '일정 체크', desc: '인원 확인·방문 완료·불참 기록', href: 'GuideToday.dc.html', border: 'var(--line)' },
        { title: '완료 보고', desc: '실제 인원·변경·비용·미해결 사항', href: 'GuideReport.dc.html', border: 'var(--line)' }
      ],
      drafts: [
        { title: '저녁 도시락(15인) · 270,000 MNT', meta: '현장 비용 · 10.01 14:20 저장', href: 'GuideExpense.dc.html' },
        { title: 'MN2609-038 완료 보고', meta: '완료 보고 · 10.01 13:40 저장', href: 'GuideReport.dc.html' }
      ],'''
mobile('GuideAdd.dc.html', '가이드 현장 등록', 'add', body, vals=vals)
print('GuideAdd written')


# ------------------------------------------------------------------ GuideOption (옵션 판매)
body = mhead('옵션 판매', back='GuideAdd.dc.html', back_label='현장 등록으로', code='MN2609-038', caption='판매액과 실제 받은 돈을 따로 적습니다') + NOTICE + '''
<section style="display: flex; flex-direction: column; gap: 14px">
<x-import component-from-global-scope="Abt.Select" label="옵션" size="lg" options="{{optionList}}" value="{{opt}}" on-change="{{setOpt}}"></x-import>
<div style="display: flex; flex-direction: column; gap: 6px">
<span class="m-label" style="color: var(--ink-muted)">인원</span>
<div style="display: grid; grid-template-columns: 56px minmax(0, 1fr) 56px; gap: 8px; align-items: center">
<x-import component-from-global-scope="Abt.Button" size="lg" on-click="{{minus}}">−</x-import>
<span style="text-align: center; font: 600 22px/28px var(--font-sans)">{{pax}}명</span>
<x-import component-from-global-scope="Abt.Button" size="lg" on-click="{{plus}}">+</x-import>
</div>
</div>
<div style="display: flex; align-items: baseline; justify-content: space-between; padding: 12px 14px; background: var(--surface); border: 1px solid var(--line); border-radius: 12px"><span class="m-label" style="color: var(--ink-muted)">판매액 {{unitText}}</span><x-import component-from-global-scope="Abt.Money" amount="{{sale}}" currency="MNT" size="lg"></x-import></div>
<x-import component-from-global-scope="Abt.TextField" label="실제 받은 금액" size="lg" input-mode="numeric" align="end" suffix="MNT" value="{{paid}}" on-change="{{setPaid}}" help="{{paidHelp}}"></x-import>
<x-import component-from-global-scope="Abt.Select" label="결제 수단" size="lg" options="{{payOptions}}" value="{{pay}}" on-change="{{setPay}}"></x-import>
<x-import component-from-global-scope="Abt.Button" size="lg" variant="primary" block="{{yes}}" on-click="{{submit}}">판매 등록</x-import>
</section>
''' + MCARD + H2.format('오늘 판매') + '''
<sc-for list="{{sold}}" as="o" hint-placeholder-count="2">
<div style="display: flex; flex-direction: column; gap: 6px; padding: 12px 0; border-top: 1px solid var(--line)">
<div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 12px"><span style="display: flex; flex-direction: column; gap: 2px"><span class="m-body" style="font-weight: 600">{{o.title}}</span><span class="m-caption" style="color: var(--ink-muted)">{{o.meta}}</span></span><x-import component-from-global-scope="Abt.StatusBadge" tone="{{o.tone}}" form="{{o.form}}">{{o.stLabel}}</x-import></div>
<sc-if value="{{o.canRefund}}" hint-placeholder-val="{{false}}"><x-import component-from-global-scope="Abt.Button" on-click="{{o.refund}}">취소·환불</x-import></sc-if>
</div>
</sc-for>
<p class="m-caption" style="margin: 0; color: var(--ink-muted)">배분: 회사 70% · 가이드 30% · 내 정산에 자동 반영</p>
</section>
'''
pre = '''
    const OPTS = { '승마 1시간': 60000, '활쏘기 체험': 30000, '전통 공연 관람': 45000 };
    const unit = OPTS[s.opt];
    const sale = unit * s.pax;
    const paid = Number(String(s.paid).replace(/[^0-9]/g, '')) || 0;
    const S = s.sold;
'''
vals = '''      optionList: Object.keys(OPTS),
      opt: s.opt,
      setOpt: (e) => set({ opt: e.target.value, paid: String(OPTS[e.target.value] * s.pax) }),
      pax: s.pax,
      minus: () => { const p = Math.max(1, s.pax - 1); set({ pax: p, paid: String(unit * p) }); },
      plus: () => { const p = Math.min(15, s.pax + 1); set({ pax: p, paid: String(unit * p) }); },
      unitText: `${fmt(unit)} × ${s.pax}명`,
      sale,
      paid: s.paid,
      setPaid: (e) => set({ paid: e.target.value }),
      paidHelp: paid < sale ? `미수 ${fmt(sale - paid)} MNT · 받을 때까지 미수로 남습니다` : paid > sale ? '판매액보다 많습니다 · 거스름돈을 확인하세요' : '전액 받음',
      payOptions: ['현금 MNT', '현금 USD', '카드(현지 단말기)'],
      pay: s.pay,
      setPay: (e) => set({ pay: e.target.value }),
      submit: () => {
        const it = { id: 'o' + (S.length + 1), title: `${s.opt} ${s.pax}명`, sale, paid, at: '14:46', pay: s.pay, st: paid < sale ? 'part' : 'ok' };
        this.setState({ sold: [it].concat(S), notice: { tone: paid < sale ? 'attention' : 'positive', title: `${s.opt} ${s.pax}명 · ${fmt(sale)} MNT 등록`, body: paid < sale ? `미수 ${fmt(sale - paid)} MNT가 남았습니다.` : '운영팀 화면과 내 정산에 바로 반영됩니다.' } });
      },
      sold: S.map((o) => ({ title: o.title, meta: `${o.at} · 판매 ${fmt(o.sale)} · 받음 ${fmt(o.paid)} MNT · ${o.pay}`, stLabel: o.st === 'refund' ? '환불' : o.st === 'part' ? '일부 수금' : '수금 완료', tone: o.st === 'refund' ? 'neutral' : o.st === 'part' ? 'attention' : 'positive', form: o.st === 'refund' ? 'dashed' : 'solid', canRefund: o.st !== 'refund', refund: () => this.setState({ sold: S.map((x) => (x.id === o.id ? { ...x, st: 'refund' } : x)), notice: { tone: 'progress', title: `${o.title} 취소·환불`, body: `${fmt(o.paid)} MNT 환불로 기록했습니다. 판매액에서 빠집니다.` } }) })),'''
state = "{ opt: '승마 1시간', pax: 3, paid: '180000', pay: '현금 MNT', notice: null, sold: [ { id: 'o1', title: '승마 1시간 3명', sale: 180000, paid: 180000, at: '09:05', pay: '현금 MNT', st: 'ok' } ] }"
mobile('GuideOption.dc.html', '가이드 옵션 판매', 'add', body, pre=pre, vals=vals, state=state)
print('GuideOption written')


# ------------------------------------------------------------------ GuideIncident (사고·클레임 보고)
body = mhead('사고·클레임 보고', back='GuideAdd.dc.html', back_label='현장 등록으로', code='MN2609-038', caption='사람이 다쳤거나 위험하면 먼저 112·103에 연락한 뒤 등록하세요') + NOTICE + '''
<sc-if value="{{editing}}" hint-placeholder-val="{{true}}">
<section style="display: flex; flex-direction: column; gap: 14px">
<div style="display: flex; flex-direction: column; gap: 6px"><span class="m-label" style="color: var(--ink-muted)">긴급도</span><x-import component-from-global-scope="Abt.Segmented" options="{{urgencyOptions}}" value="{{f.urgency}}" on-change="{{onF.urgency}}" aria-label="긴급도"></x-import></div>
<sc-if value="{{isUrgent}}" hint-placeholder-val="{{false}}"><x-import component-from-global-scope="Abt.Alert" tone="critical" title="긴급 보고는 운영 책임자에게 바로 갑니다">등록과 동시에 김지훈에게 전화·알림이 가고, 대표에게도 보고됩니다.</x-import></sc-if>
<x-import component-from-global-scope="Abt.Select" label="유형" size="lg" options="{{typeOptions}}" value="{{f.type}}" on-change="{{onF.type}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="발생 장소" size="lg" value="{{f.place}}" on-change="{{onF.place}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="발생 시각" size="lg" type="time" tag="ULAT" value="{{f.time}}" on-change="{{onF.time}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="내용" size="lg" required="{{yes}}" multiline="{{yes}}" rows="{{three}}" placeholder="무슨 일이 있었는지, 고객 상태와 반응" value="{{f.desc}}" on-change="{{onF.desc}}" error="{{descError}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="초기 조치" size="lg" multiline="{{yes}}" rows="{{two}}" value="{{f.action}}" on-change="{{onF.action}}"></x-import>
<div style="display: flex; flex-direction: column; gap: 8px"><span class="m-label" style="color: var(--ink-muted)">지원 요청</span>
<x-import component-from-global-scope="Abt.Checkbox" label="운영팀 전화 요청" checked="{{f.call}}" on-change="{{onF.call}}"></x-import>
<x-import component-from-global-scope="Abt.Checkbox" label="대체 차량" checked="{{f.car}}" on-change="{{onF.car}}"></x-import>
<x-import component-from-global-scope="Abt.Checkbox" label="병원·의료 지원" checked="{{f.med}}" on-change="{{onF.med}}"></x-import>
</div>
<div style="display: flex; flex-direction: column; gap: 8px"><span class="m-label" style="color: var(--ink-muted)">사진</span>
<sc-if value="{{noPhoto}}" hint-placeholder-val="{{true}}"><button type="button" onClick="{{addPhoto}}" style="min-height: 72px; display: flex; align-items: center; justify-content: center; padding: 12px; background: transparent; color: var(--ink); border: 1px dashed var(--line-strong); border-radius: 12px; font: 600 16px/24px var(--font-sans); cursor: pointer">사진 추가</button></sc-if>
<sc-if value="{{hasPhoto}}" hint-placeholder-val="{{false}}"><x-import component-from-global-scope="Abt.Attachment" kind="photo" name="IMG_5210.jpg" meta="2.1 MB"></x-import></sc-if>
</div>
<div style="''' + BTN2 + '''"><x-import component-from-global-scope="Abt.Button" size="lg" block="{{yes}}" on-click="{{saveDraft}}">임시저장</x-import><x-import component-from-global-scope="Abt.Button" size="lg" variant="{{submitVariant}}" block="{{yes}}" on-click="{{submit}}">{{submitLabel}}</x-import></div>
</section>
</sc-if>
<sc-if value="{{sent}}" hint-placeholder-val="{{false}}">
''' + MCARD + '''<div style="display: flex; align-items: center; justify-content: space-between; gap: 8px"><span class="m-label" style="font-weight: 600">{{receipt.no}}</span><x-import component-from-global-scope="Abt.StatusBadge" axis="claim" status="{{receipt.status}}"></x-import></div>
<span class="m-body">{{receipt.title}}</span>
<x-import component-from-global-scope="Abt.ApprovalSteps" steps="{{receipt.steps}}" orientation="vertical"></x-import>
<x-import component-from-global-scope="Abt.Button" size="lg" block="{{yes}}" on-click="{{again}}">다른 건 보고</x-import>
</section>
</sc-if>
'''
pre = '''
    const f = s.f;
    const urgent = f.urgency === '긴급';
    const upd = (k) => (e) => set({ f: { ...s.f, [k]: e && e.target ? (e.target.type === 'checkbox' ? e.target.checked : e.target.value) : e }, descError: '' });
'''
vals = '''      editing: !s.sent,
      sent: !!s.sent,
      urgencyOptions: ['보통', '긴급'],
      typeOptions: ['안전사고', '건강·부상', '차량', '숙소 시설', '식사', '분실', '일정', '기타'],
      f,
      onF: { urgency: upd('urgency'), type: upd('type'), place: upd('place'), time: upd('time'), desc: upd('desc'), action: upd('action'), call: upd('call'), car: upd('car'), med: upd('med') },
      isUrgent: urgent,
      descError: s.descError || '',
      noPhoto: !s.photo,
      hasPhoto: !!s.photo,
      addPhoto: () => set({ photo: true }),
      submitVariant: urgent ? 'danger' : 'primary',
      submitLabel: urgent ? '긴급 보고' : '보고 제출',
      saveDraft: () => say('progress', '임시저장했습니다', '통신이 돌아오면 이어서 제출할 수 있습니다. 임시저장한 보고는 회사에 보이지 않습니다.'),
      submit: () => {
        if (!f.desc.trim()) { set({ descError: '내용을 적어 주세요.' }); return; }
        this.setState({ sent: true, notice: urgent ? { tone: 'critical', title: '긴급 보고를 보냈습니다', body: '운영 책임자 김지훈에게 전화가 연결됩니다. 대표에게도 보고됐습니다.' } : { tone: 'positive', title: '보고를 제출했습니다', body: '운영팀이 확인하면 클레임 처리 단계가 이 화면과 알림에 보입니다.' } });
      },
      receipt: { no: 'FR-1003 → CL2610-003', status: urgent ? 'urgent' : 'received', title: `${f.type} · ${f.place}`, steps: [ { label: '접수', state: 'done', actor: '간바타르', at: `10.01 ${f.time || '14:48'} ULAT` }, { label: '조사', state: 'current', actor: '김지훈', note: urgent ? '전화 연결 중' : '확인 대기' }, { label: '조치', state: 'pending' }, { label: '해결 확인', state: 'pending' }, { label: '종결', state: 'pending' } ] },
      again: () => set({ sent: false, photo: false, notice: null, f: { urgency: '보통', type: '안전사고', place: '', time: '', desc: '', action: '', call: false, car: false, med: false } }),'''
state = "{ sent: false, photo: false, descError: '', notice: null, f: { urgency: '보통', type: '건강·부상', place: '아리야발 사원 계단', time: '14:45', desc: '', action: '그늘에서 쉬게 하고 물 제공', call: true, car: false, med: false } }"
mobile('GuideIncident.dc.html', '가이드 사고 보고', 'add', body, pre=pre, vals=vals, state=state)
print('GuideIncident written')


# ------------------------------------------------------------------ GuideReport (완료 보고)
body = mhead('완료 보고', back='GuideAdd.dc.html', back_label='현장 등록으로', code='MN2609-038', caption='출국 뒤 제출합니다 · 미리 써 두고 임시저장할 수 있습니다') + NOTICE + '''
<sc-if value="{{editing}}" hint-placeholder-val="{{true}}">
<section style="display: flex; flex-direction: column; gap: 14px">
<div style="''' + BTN2 + '''">
<x-import component-from-global-scope="Abt.TextField" label="실제 여행객" size="lg" input-mode="numeric" align="end" suffix="명" value="{{f.pax}}" on-change="{{onF.pax}}" help="예정 14명"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="인솔자" size="lg" input-mode="numeric" align="end" suffix="명" value="{{f.lead}}" on-change="{{onF.lead}}" help="예정 1명"></x-import>
</div>
<x-import component-from-global-scope="Abt.TextField" label="변경 사항" size="lg" multiline="{{yes}}" rows="{{two}}" value="{{f.changes}}" on-change="{{onF.changes}}"></x-import>
''' + MCARD + H2.format('돈과 증빙 · 자동 집계') + '''
<sc-for list="{{sums}}" as="m" hint-placeholder-count="4">
<div style="display: flex; align-items: baseline; justify-content: space-between; gap: 12px; padding: 6px 0; border-top: 1px solid var(--line)"><span class="m-caption" style="color: var(--ink-muted)">{{m.k}}</span><span class="m-label" style="font-weight: 600; text-align: right">{{m.v}}</span></div>
</sc-for>
</section>
<x-import component-from-global-scope="Abt.TextField" label="실제 반납 현금" size="lg" input-mode="numeric" align="end" suffix="MNT" value="{{f.cash}}" on-change="{{onF.cash}}" help="{{cashHelp}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="미해결 사항" size="lg" multiline="{{yes}}" rows="{{two}}" placeholder="없으면 비워 두세요" value="{{f.open}}" on-change="{{onF.open}}"></x-import>
<x-import component-from-global-scope="Abt.Checkbox" label="영수증 원본 18장을 운영팀에 넘길 준비가 됐습니다" checked="{{f.receipts}}" on-change="{{onF.receipts}}"></x-import>
<div style="''' + BTN2 + '''"><x-import component-from-global-scope="Abt.Button" size="lg" block="{{yes}}" on-click="{{saveDraft}}">임시저장</x-import><x-import component-from-global-scope="Abt.Button" size="lg" variant="primary" block="{{yes}}" on-click="{{submit}}">제출</x-import></div>
</section>
</sc-if>
<sc-if value="{{sent}}" hint-placeholder-val="{{false}}">
''' + MCARD + '''<div style="display: flex; align-items: center; justify-content: space-between; gap: 8px"><span class="m-label" style="font-weight: 600">FR-1004 · 완료 보고</span><x-import component-from-global-scope="Abt.StatusBadge" axis="report" status="submitted"></x-import></div>
<x-import component-from-global-scope="Abt.ApprovalSteps" steps="{{steps}}" orientation="vertical"></x-import>
<x-import component-from-global-scope="Abt.Button" size="lg" block="{{yes}}" href="GuideSettle.dc.html">내 정산 보기</x-import>
</section>
</sc-if>
'''
pre = '''
    const f = s.f;
    const cash = Number(String(f.cash).replace(/[^0-9]/g, '')) || 0;
    const expectCash = 450000;
    const upd = (k) => (e) => set({ f: { ...s.f, [k]: e.target.type === 'checkbox' ? e.target.checked : e.target.value } });
'''
vals = '''      editing: !s.sent,
      sent: !!s.sent,
      f,
      onF: { pax: upd('pax'), lead: upd('lead'), changes: upd('changes'), cash: upd('cash'), open: upd('open'), receipts: upd('receipts') },
      sums: [
        { k: '옵션 판매', v: '승마 3명 180,000 MNT · 전액 수금' },
        { k: '현장 비용', v: '12건 1,230,000 MNT · 운영 확인 대기 1건' },
        { k: '선지급 현금', v: '1,500,000 MNT · 사용 1,230,000' },
        { k: '반납할 현금', v: '남은 선지급 270,000 + 옵션 수금 180,000 = 450,000 MNT' }
      ],
      cashHelp: cash === expectCash ? '계산과 같습니다' : `계산(450,000)과 ${fmt(Math.abs(cash - expectCash))} MNT 차이 · 미해결 사항에 이유를 적어 주세요`,
      saveDraft: () => say('progress', '임시저장했습니다', '10.01 14:50 · 출국 뒤 이어서 제출하세요.'),
      submit: () => {
        if (!f.receipts) { say('attention', '영수증 원본 확인이 필요합니다', '원본을 넘길 준비가 됐는지 체크한 뒤 제출하세요.'); return; }
        this.setState({ sent: true, notice: { tone: 'positive', title: '완료 보고를 제출했습니다', body: '운영팀 현장 보고에 「확인 필요」로 올라갔습니다. 확인되면 알림이 옵니다.' } });
      },
      steps: [ { label: '현장 작성', state: 'done', actor: '간바타르', at: '10.01 ULAT' }, { label: '제출', state: 'done' }, { label: '운영 확인', state: 'current', actor: '김지훈' } ],'''
state = "{ sent: false, notice: null, f: { pax: '14', lead: '1', changes: '3일차 공항 출발 17:30 → 17:00(운영 지시) · 승마 옵션 3명 추가', cash: '450000', open: '', receipts: false } }"
mobile('GuideReport.dc.html', '가이드 완료 보고', 'add', body, pre=pre, vals=vals, state=state)
print('GuideReport written')


# ------------------------------------------------------------------ GuideSettle (내 정산)
body = mhead('내 정산', back=None, caption='가이드비·수당·옵션 배분·선지급·환급 · 회사 마진과 다른 가이드 정보는 보이지 않습니다') + NOTICE + '''
<x-import component-from-global-scope="Abt.Segmented" options="{{monthOptions}}" value="{{month}}" on-change="{{setMonth}}" aria-label="정산 월"></x-import>
''' + MCARD + '''
<div style="display: flex; align-items: center; justify-content: space-between; gap: 8px"><span class="m-label" style="color: var(--ink-muted)">{{m.title}}</span><x-import component-from-global-scope="Abt.StatusBadge" tone="{{m.tone}}" form="{{m.form}}">{{m.state}}</x-import></div>
<x-import component-from-global-scope="Abt.Money" amount="{{m.total}}" currency="MNT" size="lg" align="start" kind="{{m.kind}}"></x-import>
<span class="m-caption" style="color: var(--ink-muted)">{{m.caption}}</span>
</section>
''' + MCARD + H2.format('내역') + '''
<sc-for list="{{m.lines}}" as="l" hint-placeholder-count="5">
<div style="display: flex; align-items: baseline; justify-content: space-between; gap: 12px; padding: 8px 0; border-top: 1px solid var(--line)"><span style="display: flex; flex-direction: column; gap: 2px"><span class="m-body" style="font-size: 15px">{{l.k}}</span><span class="m-caption" style="color: var(--ink-muted)">{{l.sub}}</span></span><x-import component-from-global-scope="Abt.Money" amount="{{l.v}}" currency="MNT" sign="{{l.sign}}"></x-import></div>
</sc-for>
</section>
<sc-if value="{{m.hasHold}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.Alert" tone="attention" title="환급 보류 610,000 MNT" action="{{holdAction}}">유류 영수증 2건(MN2609-031)이 없어 현장 비용 환급을 보류했습니다. 영수증을 올리면 다음 지급에 들어갑니다.</x-import>
</sc-if>
'''
pre = '''
    const M = {
      '9월': { title: '9월 지급 예정 · 10.05(월)', state: '지급 예정', tone: 'progress', form: 'dashed', kind: 'expected', total: 4736000, caption: '회계 확정 09.30 · 지급 계좌 칸은행 ****1182', hasHold: true, lines: [ { k: '가이드비', sub: '20일 × 220,000', v: 4400000 }, { k: '추가 수당', sub: '야간 이동 2회', v: 120000 }, { k: '옵션 배분 30%', sub: '승마·공연 720,000의 30%', v: 216000 }, { k: '현장 비용 환급', sub: '보류 610,000 · 증빙 누락 2건', v: 0 } ] },
      '8월': { title: '8월 지급 완료 · 09.05(토)', state: '지급 완료', tone: 'positive', form: 'solid', kind: 'actual', total: 4180000, caption: '칸은행 ****1182 · 이체 확인증 보관', hasHold: false, lines: [ { k: '가이드비', sub: '18일 × 220,000', v: 3960000 }, { k: '추가 수당', sub: '야간 이동 1회', v: 60000 }, { k: '옵션 배분 30%', sub: '공연 534,000의 30%', v: 160000 } ] },
      '10월': { title: '10월 진행 중', state: '집계 중', tone: 'neutral', form: 'dashed', kind: 'expected', total: 1034000, caption: '확정 전 · 행사가 끝나고 회계 확인 뒤 바뀔 수 있습니다', hasHold: false, lines: [ { k: '가이드비', sub: '1일 × 220,000 (10.01)', v: 220000 }, { k: '가배정 예정', sub: 'MN2610-012 · 5일 × 220,000(수락 전)', v: 1100000 }, { k: '옵션 배분 30%', sub: '승마 180,000의 30% · 10.01', v: 54000 }, { k: '선지급', sub: '현금 1,500,000 · 반납 정산 후 0', v: 0 } ] }
    };
    const m = M[s.month];
'''
vals = '''      monthOptions: ['10월', '9월', '8월'],
      month: s.month,
      setMonth: (v) => set({ month: v }),
      m: { ...m, total: m.total, lines: m.lines.map((l) => ({ ...l, sign: l.sign || undefined })) },
      holdAction: { label: '영수증 추가', href: 'GuideExpense.dc.html' },'''
state = "{ month: '9월', notice: null }"
mobile('GuideSettle.dc.html', '가이드 내 정산', 'settle', body, pre=pre, vals=vals, state=state)
print('GuideSettle written')


# ------------------------------------------------------------------ GuideNotice (알림)
body = mhead('알림', back=None, caption='읽음과 확인을 따로 기록합니다 · 확인이 필요한 건은 끝까지 남습니다') + NOTICE + '''
<div style="display: flex; align-items: center; justify-content: space-between; gap: 8px"><x-import component-from-global-scope="Abt.Segmented" options="{{filterOptions}}" value="{{filter}}" on-change="{{setFilter}}" aria-label="알림 구분"></x-import><x-import component-from-global-scope="Abt.Button" variant="ghost" on-click="{{readAll}}">모두 읽음</x-import></div>
<section style="display: flex; flex-direction: column; gap: 10px">
<sc-for list="{{items}}" as="n" hint-placeholder-count="5">
<div style="display: flex; flex-direction: column; gap: 8px; padding: 14px 16px; background: var(--surface); border: 1px solid {{n.border}}; border-radius: 12px">
<div style="display: flex; align-items: center; justify-content: space-between; gap: 8px"><x-import component-from-global-scope="Abt.StatusBadge" tone="{{n.tone}}" form="{{n.form}}">{{n.kind}}</x-import><span class="m-caption" style="color: var(--ink-muted)">{{n.at}}</span></div>
<span class="m-body" style="font-weight: {{n.weight}}">{{n.title}}</span>
<span class="m-caption" style="color: var(--ink-muted)">{{n.body}}</span>
<div style="display: flex; gap: 8px">
<sc-if value="{{n.hasLink}}" hint-placeholder-val="{{false}}"><x-import component-from-global-scope="Abt.Button" href="{{n.href}}">{{n.linkLabel}}</x-import></sc-if>
<sc-if value="{{n.needAck}}" hint-placeholder-val="{{false}}"><x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{n.ack}}">확인함</x-import></sc-if>
<sc-if value="{{n.acked}}" hint-placeholder-val="{{false}}"><span class="m-caption" style="align-self: center; color: var(--ink-muted)">확인 완료</span></sc-if>
</div>
</div>
</sc-for>
<sc-if value="{{empty}}" hint-placeholder-val="{{false}}"><p class="m-body" style="margin: 0; padding: 24px 0; text-align: center; color: var(--ink-muted)">새 알림이 없습니다.</p></sc-if>
</section>
'''
pre = '''
    const N = [
      { id: 'n1', kind: '배정 변경', tone: 'attention', at: '13:10', title: 'MN2610-012 집합 시간 07:30 → 06:30', body: '10.08 호텔 로비 · 운영 김지훈', ack: true, href: 'GuideSchedule.dc.html', linkLabel: '내 일정' },
      { id: 'n2', kind: '배정 요청', tone: 'neutral', form: 'dashed', at: '11:00', title: 'MN2610-012 기업 인센티브 리드 가이드 요청', body: '10.08–10.12 · 32+2명 · 수락하면 배정 확정', href: 'GuideSchedule.dc.html', linkLabel: '수락·거절' },
      { id: 'n3', kind: '비용 보완', tone: 'attention', at: '09.30', title: '유류 영수증 2건 보완 요청', body: '회계 박서연 · MN2609-031 무릉·하트갈 · 환급 보류 중', href: 'GuideExpense.dc.html', linkLabel: '영수증 추가' },
      { id: 'n4', kind: '매뉴얼', tone: 'neutral', at: '10.01', title: '고비 오아시스 캠프 매뉴얼 v4 재확인', body: '온수 고장 주의사항 추가 · 다음 고비 행사 전 확인', ack: true },
      { id: 'n5', kind: '운영 지시', tone: 'neutral', at: '09.30', title: '10.02 테를지 진입로 도로 통제', body: '06:00–18:00 · 테를지 일정은 시내로 대체', ack: false }
    ];
    const read = s.read, acked = s.acked;
    const list = s.filter === '확인 필요' ? N.filter((n) => n.ack && !acked[n.id]) : N;
    const unread = N.filter((n) => !read[n.id]).length;
'''
vals = '''      badges: { notice: unread || undefined },
      filterOptions: ['전체', '확인 필요'],
      filter: s.filter,
      setFilter: (v) => set({ filter: v }),
      readAll: () => set({ read: Object.fromEntries(N.map((n) => [n.id, true])) }),
      items: list.map((n) => ({ ...n, form: n.form || 'solid', weight: read[n.id] ? 400 : 600, border: read[n.id] ? 'var(--line)' : 'var(--line-strong)', hasLink: !!n.href, needAck: !!n.ack && !acked[n.id], acked: !!n.ack && !!acked[n.id], ack: () => set({ acked: { ...acked, [n.id]: true }, read: { ...read, [n.id]: true }, notice: { tone: 'positive', title: '확인했습니다', body: `${n.title} · 운영팀에 확인 시각이 남았습니다.` } }) })),
      empty: list.length === 0,'''
state = "{ filter: '전체', read: { n5: true, n4: true }, acked: {}, notice: null }"
mobile('GuideNotice.dc.html', '가이드 알림', 'notice', body, pre=pre, vals=vals, state=state)
print('GuideNotice written')


# ------------------------------------------------------------------ GuideExpense (현장 비용)
body = mhead('현장 비용 등록', back='GuideAdd.dc.html', back_label='현장 등록으로', code='MN2609-038') + NOTICE + '''
<section style="display: flex; flex-direction: column; gap: 14px">
<x-import component-from-global-scope="Abt.Select" label="항목" size="lg" options="{{categories}}" required="{{yes}}" value="{{f.cat}}" on-change="{{onF.cat}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="사용처" size="lg" required="{{yes}}" value="{{f.where}}" on-change="{{onF.where}}" error="{{err.where}}"></x-import>
<x-import component-from-global-scope="Abt.MoneyField" label="금액" size="lg" amount="{{amount}}" currency="MNT" rate="{{rate}}" required="{{yes}}" on-amount-change="{{onAmount}}"></x-import>
<x-import component-from-global-scope="Abt.Select" label="지급 수단" size="lg" options="{{payments}}" value="{{f.pay}}" on-change="{{onF.pay}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="지출 사유" size="lg" multiline="{{yes}}" rows="{{two}}" value="{{f.why}}" on-change="{{onF.why}}"></x-import>
<div style="display: flex; flex-direction: column; gap: 8px">
<span class="m-label" style="color: var(--ink-muted)">영수증</span>
<sc-if value="{{noReceipt}}" hint-placeholder-val="{{true}}">
<button type="button" onClick="{{addReceipt}}" style="min-height: 88px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; padding: 12px; background: transparent; color: var(--ink); border: 1px dashed var(--line-strong); border-radius: 12px; font: 600 16px/24px var(--font-sans); cursor: pointer">영수증 사진 추가<span class="m-caption" style="color: var(--ink-muted); font-weight: 400">카메라로 찍거나 앨범에서 고르기</span></button>
</sc-if>
<sc-if value="{{hasReceipt}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.Attachment" kind="receipt" name="IMG_5201.jpg" meta="1.3 MB"></x-import>
</sc-if>
</div>
<p class="m-caption" style="margin: 0; color: var(--ink-muted)">제출하면 운영 확인 → 회계 검토 → 승인 순서로 처리됩니다. 승인 전 금액은 정산에 들어가지 않습니다.</p>
<div style="''' + BTN2 + '''">
<x-import component-from-global-scope="Abt.Button" size="lg" block="{{yes}}" on-click="{{saveDraft}}">임시저장</x-import>
<x-import component-from-global-scope="Abt.Button" size="lg" variant="primary" block="{{yes}}" on-click="{{submit}}" disabled="{{busy}}">제출</x-import>
</div>
</section>

<section style="display: flex; flex-direction: column; gap: 4px; padding: 4px 16px 8px; background: var(--surface); border: 1px solid var(--line); border-radius: 12px">
<h2 class="m-label" style="margin: 12px 0 4px; font-weight: 600">내가 등록한 비용</h2>
<sc-for list="{{mine}}" as="c" hint-placeholder-count="4">
<div style="display: flex; flex-direction: column; gap: 8px; padding: 12px 0; border-top: 1px solid var(--line)">
<div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 12px">
<div style="display: flex; flex-direction: column; gap: 2px; min-width: 0"><span class="m-body" style="font-weight: 600">{{c.title}}</span><span class="m-caption" style="color: var(--ink-muted)">{{c.meta}}</span></div>
<x-import component-from-global-scope="Abt.StatusBadge" axis="cost" status="{{c.status}}"></x-import>
</div>
<sc-if value="{{c.needsFix}}" hint-placeholder-val="{{false}}">
<p class="m-caption" style="margin: 0; color: var(--attention)">{{c.fix}}</p>
<x-import component-from-global-scope="Abt.Button" on-click="{{c.attach}}">영수증 추가</x-import>
</sc-if>
</div>
</sc-for>
</section>
'''
pre = '''
    const f = s.f;
    const BASE = [
      { id: 'm1', title: '조식 추가(3인)', meta: '10.01 08:15 · 90,000 MNT', status: 'submitted' },
      { id: 'm2', title: '주차비', meta: '09.30 16:05 · 15,000 MNT', status: 'approved' },
      { id: 'm3', title: '유류(하트갈) · MN2609-031', meta: '09.26 09:30 · 270,000 MNT', status: 'supplement', fix: '회계 박서연: 영수증 사진을 추가해 주세요.' },
      { id: 'm4', title: '유류(무릉) · MN2609-031', meta: '09.25 12:05 · 340,000 MNT', status: 'supplement', fix: '회계 박서연: 영수증 사진을 추가해 주세요.' }
    ];
    const fixed = s.fixed;
    const upd = (k) => (e) => set({ f: { ...s.f, [k]: e.target.value }, err: {} });
    const amt = Number(String(s.amount).replace(/[^0-9]/g, '')) || 0;
'''
vals = '''      categories: ['식사', '차량·유류', '숙박', '관광·입장', '기타'],
      payments: ['가이드 현금', '회사 카드', '가이드 개인 카드'],
      f,
      onF: { cat: upd('cat'), where: upd('where'), pay: upd('pay'), why: upd('why') },
      err: s.err || {},
      amount: 270000,
      onAmount: (v) => set({ amount: v }),
      rate: { value: 0.3985, base: 'KRW', date: '10.01' },
      noReceipt: !s.receipt,
      hasReceipt: !!s.receipt,
      addReceipt: () => set({ receipt: true }),
      busy: false,
      saveDraft: () => this.setState({ added: [{ id: 'n' + s.added.length, title: `${f.where || '이름 없음'}`, meta: `10.01 14:52 · ${fmt(amt)} MNT`, status: 'draft' }].concat(s.added), notice: { tone: 'progress', title: '임시저장했습니다', body: '통신이 돌아오면 이어서 제출할 수 있습니다. 임시저장한 비용은 회사에 보이지 않습니다.' } }),
      submit: () => {
        if (!f.where.trim()) { set({ err: { where: '사용처를 적어 주세요.' } }); return; }
        if (s.added.some((a) => a.title === f.where && a.status === 'submitted')) { set({ notice: { tone: 'attention', title: '같은 비용을 이미 제출했습니다', body: '중복 제출을 막았습니다. 다른 비용이면 사용처를 다르게 적어 주세요.' } }); return; }
        this.setState({ added: [{ id: 'n' + s.added.length, title: f.where, meta: `10.01 14:52 · ${fmt(amt)} MNT${s.receipt ? '' : ' · 영수증 없음'}`, status: 'submitted' }].concat(s.added), notice: s.receipt ? { tone: 'positive', title: '제출했습니다', body: '운영 확인을 기다립니다. 승인 전 금액은 정산에 들어가지 않습니다.' } : { tone: 'attention', title: '영수증 없이 제출했습니다', body: '회계에서 보완을 요청할 수 있습니다. 영수증을 받으면 이 비용에 추가하세요.' } });
      },
      mine: s.added.concat(BASE.map((b) => (fixed[b.id] ? { ...b, status: 'reviewing', meta: b.meta + ' · 영수증 추가됨' } : b))).map((c) => ({ ...c, needsFix: c.status === 'supplement', attach: () => this.setState({ fixed: { ...fixed, [c.id]: true }, notice: { tone: 'positive', title: '영수증을 추가했습니다', body: `${c.title} · 회계 검토로 돌아갔습니다. 확인되면 환급 보류가 풀립니다.` } }) })),'''
state = "{ receipt: false, amount: '270000', added: [], fixed: {}, err: {}, notice: null, f: { cat: '식사', where: '노민 마트 도시락(15인)', pay: '가이드 현금', why: '공항 가는 길 저녁 · 일정표 포함 식사(계약 단가 18,000 MNT)' } }"
mobile('GuideExpense.dc.html', '가이드 현장 비용', 'add', body, pre=pre, vals=vals, state=state)
print('GuideExpense written')


# ------------------------------------------------------------------ GuideBriefing (브리핑)
body = mhead('브리핑', code='MN2609-038', caption='제이원트래블 · 테를지 승마·게르 2박 3일 · 14+1명') + NOTICE + '''
<sc-if value="{{needsAck}}" hint-placeholder-val="{{true}}">
<x-import component-from-global-scope="Abt.Alert" tone="attention" title="변경 확인 필요: 공항 출발 시각" action="{{ackAction}}">17:30 → 17:00으로 앞당겨졌습니다. 운영 김지훈, 10.01 11:20 KST.</x-import>
</sc-if>
<sc-if value="{{acked}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.Alert" tone="positive" title="변경을 확인했습니다">공항 출발 17:00 · 운영팀에 확인 기록이 남았습니다.</x-import>
</sc-if>

<section style="display: flex; flex-direction: column; gap: 10px; padding: 16px; background: var(--critical-soft); border-radius: 12px">
<h2 class="m-body" style="margin: 0; font-weight: 700; color: var(--critical)">꼭 지킬 것</h2>
<ul style="margin: 0; padding: 0 0 0 18px; display: flex; flex-direction: column; gap: 6px">
<li class="m-body">견과류 알레르기 1명 · 박○○ (12번)</li>
<li class="m-body">채식 2명 · 계란·유제품은 먹음</li>
<li class="m-body">70대 2명 · 계단과 긴 도보는 대안 안내</li>
</ul>
<p class="m-caption" style="margin: 0">요약과 별도로 항상 맨 위에 보입니다. 고객 정보는 행사가 끝나면 볼 수 없습니다.</p>
</section>

<section style="display: flex; flex-direction: column; gap: 8px; padding: 16px; background: var(--surface); border: 1px solid var(--line); border-radius: 12px">
''' + H2.format('오늘 일정별 주의사항') + '''
<sc-for list="{{notes}}" as="n" hint-placeholder-count="3">
<div style="display: flex; flex-direction: column; gap: 2px; padding: 8px 0; border-top: 1px solid var(--line)"><span class="m-body" style="font-weight: 600">{{n.place}}</span><span class="m-body" style="color: var(--ink-muted); font-size: 15px; line-height: 22px">{{n.text}}</span></div>
</sc-for>
</section>

<section style="display: flex; flex-direction: column; gap: 8px; padding: 16px; background: var(--surface); border: 1px solid var(--line); border-radius: 12px">
''' + H2.format('여행사 요청 · 제이원트래블') + '''
<ul style="margin: 0; padding: 0 0 0 18px; display: flex; flex-direction: column; gap: 6px">
<li class="m-body" style="font-size: 15px; line-height: 22px">승마 경험 수준별로 조 나누기 · 초보는 별도 조</li>
<li class="m-body" style="font-size: 15px; line-height: 22px">매일 저녁 다음 날 일정을 단체 대화방에 공지</li>
<li class="m-body" style="font-size: 15px; line-height: 22px">마지막 날 단체 사진을 1장 이상 공유</li>
</ul>
</section>

''' + MCARD + '''
<div style="display: flex; align-items: baseline; justify-content: space-between; gap: 8px">''' + H2.format('연결된 매뉴얼') + '''<span class="m-caption" style="color: var(--ink-muted)">{{manCount}}건</span></div>
<p class="m-caption" style="margin: 0; color: var(--ink-muted)">공통 문화 · 이 상품 · 제이원트래블 · 방문 장소에 연결된 게시 매뉴얼</p>
<sc-for list="{{mans}}" as="m" hint-placeholder-count="2">
<div style="display: flex; flex-direction: column; gap: 8px; padding-top: 12px; border-top: 1px solid var(--line)">
<div style="display: flex; flex-direction: column; gap: 2px"><span class="m-body" style="font-weight: 600">{{m.title}}</span><span class="m-caption" style="color: var(--ink-muted)">{{m.meta}}</span></div>
<sc-if value="{{m.hasPins}}" hint-placeholder-val="{{true}}">
<div style="display: flex; flex-direction: column; gap: 4px; padding: 10px 12px; border: 1px solid var(--attention); border-radius: 8px; background: var(--attention-soft)">
<sc-for list="{{m.pins}}" as="p" hint-placeholder-count="1"><span class="m-body" style="font-size: 15px; line-height: 22px">{{p}}</span></sc-for>
</div>
</sc-if>
<sc-for list="{{m.sections}}" as="x" hint-placeholder-count="1">
<div style="display: flex; flex-direction: column; gap: 2px"><span class="m-label" style="font-weight: 600">{{x.h}}</span><span class="m-body" style="font-size: 15px; line-height: 22px; color: var(--ink-muted); white-space: pre-line">{{x.b}}</span></div>
</sc-for>
<sc-if value="{{m.needAck}}" hint-placeholder-val="{{true}}"><x-import component-from-global-scope="Abt.Button" size="lg" block="{{yes}}" on-click="{{m.ack}}">읽었습니다</x-import></sc-if>
<sc-if value="{{m.acked}}" hint-placeholder-val="{{false}}"><span class="m-caption" style="color: var(--ink-muted)">확인함 · 운영팀 매뉴얼 화면에 기록됐습니다</span></sc-if>
</div>
</sc-for>
<sc-if value="{{noMans}}" hint-placeholder-val="{{false}}"><p class="m-body" style="margin: 0; color: var(--ink-muted)">연결된 게시 매뉴얼이 없습니다.</p></sc-if>
</section>

<section style="display: flex; flex-direction: column; gap: 8px; padding: 16px; background: var(--surface); border: 1px solid var(--line); border-radius: 12px">
''' + H2.format('인수인계') + '''
<p class="m-body" style="margin: 0; font-size: 15px; line-height: 22px">테를지 입구 검문소에서 단체 명단 사본을 요구합니다. 출력본 2부를 준비하세요.</p>
<p class="m-caption" style="margin: 0; color: var(--ink-muted)">뭉흐-오치르 · 09.20 · 검토 김지훈</p>
</section>

<section style="display: flex; flex-direction: column; gap: 12px; padding: 16px; background: var(--surface); border: 1px solid var(--line); border-radius: 12px">
<div style="display: flex; justify-content: space-between">''' + H2.format('오늘 체크리스트') + '''<span class="m-caption" style="color: var(--ink-muted)">{{doneCount}}/4</span></div>
<sc-for list="{{checks}}" as="c" hint-placeholder-count="4">
<x-import component-from-global-scope="Abt.Checkbox" label="{{c.label}}" description="{{c.desc}}" checked="{{c.on}}" on-change="{{c.toggle}}"></x-import>
</sc-for>
<x-import component-from-global-scope="Abt.Button" size="lg" block="{{yes}}" href="GuideReport.dc.html">완료 보고 쓰기</x-import>
</section>
'''
pre = '''
    const C = [
      { id: 'c1', label: '옵션 판매 정산 · 승마 추가 3명', desc: '' },
      { id: 'c2', label: '출국 전 인원 확인 · 14+1명', desc: '' },
      { id: 'c3', label: '남은 현금과 영수증 반납 준비', desc: '' },
      { id: 'c4', label: '완료 보고 제출', desc: '실제 인원, 변경 사항, 비용, 미해결 사항' }
    ];
    const on = s.checks;
    const MB = ''' + MANUALS_BASE_JS + ''';
    const MAN = (() => { const v = store.get('manuals', null); return v == null ? (s.localManuals || MB) : v; })();
    const LINKED = ['모든 행사', '테를지 승마·게르 2박 3일', '제이원트래블', '테를지 리버 캠프', '칭기즈칸 국제공항'];
    const viewOf = (m) => (m.status === 'published' ? m : m.live ? { ...m, ...m.live } : null);
    const MANS = MAN.filter((m) => LINKED.includes(m.link)).map((m) => ({ src: m, v: viewOf(m) })).filter((x) => x.v);
'''
vals = '''      needsAck: !s.acked,
      acked: !!s.acked,
      ackAction: { label: '확인함', onClick: () => set({ acked: true }) },
      notes: [
        { place: '거북바위', text: '바위 위로 올라가지 않도록 먼저 안내합니다.' },
        { place: '아리야발 사원', text: '계단 108개. 70대 고객은 아래 전망대에서 기다리도록 안내합니다.' },
        { place: '칭기즈칸 국제공항', text: '출국 3시간 전 도착. 라이터·보조배터리 규정을 버스에서 다시 안내합니다.' }
      ],
      checks: C.map((c) => ({ ...c, desc: c.desc || undefined, on: !!on[c.id], toggle: (e) => set({ checks: { ...on, [c.id]: e.target.checked } }) })),
      doneCount: C.filter((c) => on[c.id]).length,
      mans: MANS.map(({ src, v }) => { const done = src.acked.includes('간바타르'); return { title: v.title, meta: `${src.id} · ${src.cat} · v${v.ver} · 게시 ${v.updated}`, pins: v.pins, hasPins: v.pins.length > 0, sections: v.sections, needAck: !done, acked: done, ack: () => { const next = MAN.map((x) => (x.id === src.id ? { ...x, acked: x.acked.concat(['간바타르']) } : x)); store.put('manuals', next); this.setState({ localManuals: next, notice: { tone: 'positive', title: `${v.title} v${v.ver} 확인`, body: '운영팀 매뉴얼 화면의 가이드 확인에 간바타르로 기록됐습니다.' } }); } }; }),
      manCount: MANS.length,
      noMans: !MANS.length,'''
state = "{ acked: false, checks: { c1: true }, localManuals: null, notice: null }"
mobile('GuideBriefing.dc.html', '가이드 브리핑', 'today', body, pre=pre, vals=vals, state=state)
print('GuideBriefing written')
