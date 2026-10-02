import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import *

# ------------------------------------------------------------------ FieldReports (현장 보고)
body = header('현장 보고', '가이드가 제출한 일정 체크·변경·옵션·사고·완료 보고를 운영팀이 확인합니다 · 현장 비용은 비용 승인에서 따로 검토합니다',
              '<x-import component-from-global-scope="Abt.Segmented" options="{{filterOptions}}" value="{{filter}}" on-change="{{setFilter}}" aria-label="확인 상태"></x-import>')
body += NOTICE
body += TWO_PANE + '''
<section style="display: flex; flex-direction: column; gap: 10px; min-width: 0">
<p class="caption" style="margin: 0; color: var(--ink-muted)">{{listCaption}}</p>
<x-import component-from-global-scope="Abt.DataTable" columns="{{cols}}" rows="{{rows}}" on-row-click="{{pick}}" caption="현장 보고 목록" empty="이 상태의 보고가 없습니다."></x-import>
</section>
''' + SIDE_PANEL + '''<div style="display: flex; flex-direction: column; gap: 8px">
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 8px">
<div style="display: flex; align-items: center; gap: 8px"><span style="font: 500 13px/20px var(--font-mono)">{{cur.id}}</span><x-import component-from-global-scope="Abt.StatusBadge" tone="neutral">{{cur.type}}</x-import></div>
<x-import component-from-global-scope="Abt.StatusBadge" axis="report" status="{{cur.status}}" size="md"></x-import>
</div>
<h2 class="title-2" style="margin: 0">{{cur.title}}</h2>
<div style="display: flex; align-items: center; gap: 8px"><x-import component-from-global-scope="Abt.EventCode" code="{{cur.code}}" href="EventDetail.dc.html"></x-import><span class="caption" style="color: var(--ink-muted)">{{cur.byline}}</span></div>
</div>
<x-import component-from-global-scope="Abt.ApprovalSteps" steps="{{cur.steps}}"></x-import>
<sc-for list="{{cur.blocks}}" as="b" hint-placeholder-count="2">
<div style="display: flex; flex-direction: column; gap: 6px; padding-top: 12px; border-top: 1px solid var(--line)">
<span class="label" style="color: var(--ink-muted)">{{b.head}}</span>
<sc-for list="{{b.rows}}" as="r" hint-placeholder-count="3">
<div style="display: grid; grid-template-columns: 104px minmax(0, 1fr); gap: 12px; font-size: 13px; line-height: 20px"><span style="color: var(--ink-muted)">{{r.k}}</span><span>{{r.v}}</span></div>
</sc-for>
</div>
</sc-for>
<div style="display: flex; flex-wrap: wrap; gap: 8px">
<sc-for list="{{cur.files}}" as="f" hint-placeholder-count="2">
<x-import component-from-global-scope="Abt.Attachment" kind="{{f.kind}}" name="{{f.name}}" meta="{{f.meta}}"></x-import>
</sc-for>
</div>
<sc-if value="{{cur.hasLink}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.Alert" tone="{{cur.linkTone}}" title="{{cur.linkTitle}}" action="{{cur.linkAction}}">{{cur.linkBody}}</x-import>
</sc-if>
<sc-if value="{{showDecision}}" hint-placeholder-val="{{true}}">
<div style="display: flex; flex-direction: column; gap: 12px; padding-top: 12px; border-top: 1px solid var(--line)">
<sc-if value="{{cur.isChange}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.Checkbox" label="여행사(솔빛여행)에 변경 안내 보내기" description="확인과 함께 담당자 이메일로 변경 전후 일정이 나갑니다" checked="{{notify}}" on-change="{{toggleNotify}}"></x-import>
</sc-if>
<x-import component-from-global-scope="Abt.TextField" label="확인 의견" multiline="{{yes}}" rows="{{two}}" placeholder="보완을 요청하면 이 내용이 가이드 앱 알림으로 갑니다." value="{{note}}" on-change="{{setNote}}" error="{{noteError}}"></x-import>
<div style="display: flex; justify-content: flex-end; gap: 8px">
<x-import component-from-global-scope="Abt.Button" variant="secondary" on-click="{{supplement}}">보완 요청</x-import>
<x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{confirm}}">확인 완료</x-import>
</div>
</div>
</sc-if>
</section>
</div>
'''

pre = '''
    const BASE = [
      { id: 'FR-1002', type: '일정 변경', code: 'MN2609-040', by: '오윤치메그', at: '2026-10-01T09:30', status: 'submitted', title: '10.02 테를지 국립공원 → 시내 대체 일정',
        blocks: [
          { head: '변경 내용', rows: [ { k: '변경 전', v: '10.02(금) 테를지 국립공원 · 거북바위 · 게르 점심' }, { k: '변경 후', v: '울란바토르 시내 · 간단 사원 · 자이승 전망대 · 시내 점심' }, { k: '사유', v: '테를지 진입로 도로 통제(10.02 06:00–18:00, 경찰 통보)' } ] },
          { head: '영향 비용', rows: [ { k: '취소', v: '테를지 입장료·게르 점심 −420,000 MNT (업체 환불 요청 예정)' }, { k: '추가', v: '시내 점심 +360,000 MNT · 비용은 가이드가 현장 비용으로 따로 등록' }, { k: '고객 안내', v: '10.01 저녁 브리핑에서 9명 전원 안내 · 이의 없음' } ] }
        ],
        files: [ { kind: 'photo', name: '도로통제_안내.jpg', meta: '0.8 MB' } ] },
      { id: 'FR-1001', type: '완료 보고', code: 'MN2609-031', by: '간바타르', at: '2026-09-30T18:20', status: 'submitted', title: '홉스골 호수 6박 7일 완료 보고',
        blocks: [
          { head: '행사 결과', rows: [ { k: '실제 인원', v: '24+1명 (예정과 같음)' }, { k: '일정 변경', v: '4일차 숙소 온수 미공급 · CL2609-004로 처리 중' }, { k: '제출', v: '행사 종료(09.26) 후 4일 · 기준 2일보다 늦음' } ] },
          { head: '돈과 증빙', rows: [ { k: '옵션 판매', v: '승마 12명 × 60,000 = 720,000 MNT · 전액 수금' }, { k: '현장 비용', v: '38건 9,850,000 MNT · 보완 요청 2건(유류 영수증 없음)' }, { k: '현금', v: '선지급 3,000,000 − 사용 2,760,000 = 반납 240,000 MNT' }, { k: '미해결', v: 'CL2609-004 보상 협의 · 유류 영수증 2건' } ] }
        ],
        files: [ { kind: 'doc', name: '완료보고_MN2609-031.pdf', meta: '1.2 MB' }, { kind: 'photo', name: '현금반납_확인.jpg', meta: '0.6 MB' } ] },
      { id: 'FR-0999', type: '옵션 판매', code: 'MN2609-040', by: '오윤치메그', at: '2026-09-30T20:15', status: 'confirmed', title: '전통 공연 관람 7명',
        blocks: [ { head: '판매', rows: [ { k: '옵션', v: '투멘 에흐 전통 공연 · 09.30 18:00' }, { k: '인원·단가', v: '7명 × 45,000 MNT = 315,000 MNT' }, { k: '수금', v: '현금 315,000 MNT · 미수 없음' }, { k: '배분', v: '회사 70% 220,500 · 가이드 30% 94,500 MNT' } ] } ],
        files: [ { kind: 'receipt', name: '공연티켓_7매.jpg', meta: '0.9 MB' } ] },
      { id: 'FR-0998', type: '완료 보고', code: 'MN2609-033', by: '바트-에르덴', at: '2026-09-27T20:05', status: 'confirmed', title: '고비 사막 5박 6일 완료 보고',
        blocks: [ { head: '행사 결과', rows: [ { k: '실제 인원', v: '20+1명 (예정과 같음)' }, { k: '일정 변경', v: '4일차 우회 도로 +140 km · 캠프 온수 고장(CL2609-003)' }, { k: '현장 비용', v: '31건 · 증빙 31건 첨부' }, { k: '현금', v: '반납 없음(정산 완료)' } ] } ],
        files: [ { kind: 'doc', name: '완료보고_MN2609-033.pdf', meta: '1.0 MB' } ] },
      { id: 'FR-0996', type: '일정 체크', code: 'MN2609-038', by: '간바타르', at: '2026-10-01T08:10', status: 'confirmed', title: '3일차 출발 인원 확인',
        blocks: [ { head: '체크', rows: [ { k: '인원', v: '14+1명 확인 · 불참 없음' }, { k: '방문', v: '테를지 승마 체험 완료 · 공항 이동 19:10 도착 예정' } ] } ],
        files: [] },
      { id: 'FR-0995', type: '사고·클레임', code: 'MN2609-031', by: '간바타르', at: '2026-09-24T21:30', status: 'confirmed', title: '홉스골 숙소 온수 미공급',
        blocks: [ { head: '보고', rows: [ { k: '발생', v: '09.24 19:00 ULAT · 홉스골 호숫가 게르 캠프' }, { k: '긴급도', v: '보통 · 안전 문제 없음' }, { k: '초기 조치', v: '캠프에 수리 요청 · 고객에게 인근 샤워 시설 안내' }, { k: '지원 요청', v: '보상 기준 안내 요청' } ] } ],
        files: [ { kind: 'photo', name: '보일러_고장.jpg', meta: '1.1 MB' } ] }
    ];
    const D = s.decisions;
    const NOW = '10.01 15:50 KST';
    const items = BASE.map((b) => (D[b.id] ? { ...b, status: D[b.id].kind === 'confirmed' ? 'confirmed' : 'draft', dec: D[b.id] } : b));
    const group = (i) => (i.status === 'submitted' ? '확인 필요' : i.status === 'confirmed' ? '확인 완료' : '보완 요청');
    const counts = { need: items.filter((i) => group(i) === '확인 필요').length, done: items.filter((i) => group(i) === '확인 완료').length, back: items.filter((i) => group(i) === '보완 요청').length };
    const filter = s.filter;
    const list = filter === '전체' ? items : items.filter((i) => group(i) === filter);
    const cur = items.find((i) => i.id === s.selected) || items[0];
    const at = (iso) => `${iso.slice(5, 7)}.${iso.slice(8, 10)} ${iso.slice(11, 16)} ULAT`;
    const stepsOf = (i) => [
      { label: '현장 작성', state: 'done', actor: i.by, at: at(i.at) },
      { label: '제출', state: 'done' },
      i.status === 'confirmed' ? { label: '운영 확인', state: 'done', actor: '김지훈', at: i.dec ? NOW : undefined } : i.status === 'draft' ? { label: '운영 확인', state: 'rejected', actor: '김지훈', note: '보완 요청: ' + i.dec.note } : { label: '운영 확인', state: 'current', actor: '김지훈' }
    ];
    const decide = (kind) => {
      const note = (s.note || '').trim();
      if (kind === 'back' && !note) { set({ noteError: '보완할 내용을 적어 주세요. 가이드에게 그대로 전달됩니다.' }); return; }
      const msgs = {
        confirmed: cur.type === '일정 변경' ? ['일정 변경을 확인했습니다', `행사 상세 일정 탭에 반영했습니다.${s.notify ? ' 솔빛여행에 변경 안내를 보냈습니다.' : ' 여행사 안내는 아직 보내지 않았습니다.'}`] : cur.type === '완료 보고' ? ['완료 보고를 확인했습니다', '현금 반납 240,000 MNT는 회계 확인으로 넘어갔고, 미해결 2건은 각 화면에 남습니다.'] : ['보고를 확인했습니다', ''],
        back: ['보완을 요청했습니다', '가이드 앱 알림으로 의견이 전달됐습니다. 다시 제출하면 확인 필요로 돌아옵니다.']
      };
      const m = msgs[kind];
      this.setState({ decisions: { ...D, [cur.id]: { kind, note } }, note: '', noteError: '', notice: { tone: kind === 'confirmed' ? 'positive' : 'attention', title: `${cur.id} · ${m[0]}`, body: m[1], action: { label: '되돌리기', onClick: () => { const d = { ...this.state.decisions }; delete d[cur.id]; this.setState({ decisions: d, notice: null }); } } } });
    };
    const linkFor = (i) => {
      if (i.type === '사고·클레임') return { hasLink: true, linkTone: 'progress', linkTitle: '클레임 CL2609-004로 접수됨', linkBody: '처리 기한 09.28을 넘겨 조치 중입니다.', linkAction: { label: '클레임 보기', href: 'Claims.dc.html' } };
      if (i.id === 'FR-1001') return { hasLink: true, linkTone: 'attention', linkTitle: '증빙 누락 2건이 남아 있습니다', linkBody: '유류 영수증 2건은 비용 승인에서 보완 요청 상태입니다.', linkAction: { label: '비용 승인', href: 'Approvals.dc.html' } };
      return { hasLink: false };
    };
'''
vals = '''      navCounts: { alerts: 5, field: counts.need || undefined, claims: { n: 2, tone: 'critical' }, receipts: { n: 1, tone: 'critical' }, costs: { n: 7, tone: 'attention' }, remit: 3 },
      filterOptions: [ { value: '확인 필요', label: `확인 필요 ${counts.need}` }, { value: '보완 요청', label: `보완 요청 ${counts.back}` }, { value: '확인 완료', label: `확인 완료 ${counts.done}` }, { value: '전체', label: '전체' } ],
      filter,
      setFilter: (v) => set({ filter: v }),
      listCaption: `${filter} ${list.length}건 · 시각은 현지(ULAT) · 행을 누르면 오른쪽에서 확인합니다`,
      cols: [
        { key: 'what', label: '보고', type: 'stack' },
        { key: 'code', label: '행사코드', type: 'code' },
        { key: 'title', label: '내용', type: 'strong', wrap: true },
        { key: 'by', label: '가이드', type: 'muted' },
        { key: 'at', label: '제출', type: 'datetime', zone: 'ULAT' },
        { key: 'status', label: '상태', type: 'status', axis: 'report' }
      ],
      rows: list.map((i) => ({ id: i.id, what: { primary: i.type, secondary: i.id }, code: i.code, title: i.title, by: i.by, at: { value: i.at, showZone: false }, status: i.status, selected: i.id === cur.id })),
      pick: (row) => set({ selected: row.id, note: '', noteError: '', notify: true }),
      cur: { ...cur, byline: `${cur.by} · ${at(cur.at)} 제출`, steps: stepsOf(cur), isChange: cur.type === '일정 변경', ...linkFor(cur) },
      showDecision: cur.status === 'submitted',
      notify: s.notify,
      toggleNotify: (e) => set({ notify: e.target.checked }),
      note: s.note,
      setNote: (e) => set({ note: e.target.value, noteError: '' }),
      noteError: s.noteError || '',
      confirm: () => decide('confirmed'),
      supplement: () => decide('back'),'''

state = "{ filter: '확인 필요', selected: 'FR-1002', decisions: {}, note: '', noteError: '', notify: true, notice: null }"
admin('FieldReports.dc.html', '현장 보고', 'field', 'ops', body, pre=pre, vals=vals, state=state, height=1040)
print('FieldReports written')


# ------------------------------------------------------------------ Claims (클레임)
body = header('클레임', '접수 → 조사 → 조치 → 해결 확인 → 종결 · 처리 기한을 넘기면 운영 책임자에게 다시 알립니다 · 접수 건과 책임이 확인된 건을 따로 셉니다',
              '<x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{toggleNew}}">{{newLabel}}</x-import>')
body += NOTICE
body += '''<section aria-label="클레임 지표" style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px">
<x-import component-from-global-scope="Abt.KpiTile" label="미해결" value="{{kpi.open}}" unit="건" state="{{kpi.openState}}" state-label="{{kpi.overdueLabel}}"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="보상 예정" money="{{kpi.comp}}" caption="미해결 건 기준 · 승인 전"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="최근 30일 접수" value="{{kpi.month}}" unit="건" caption="{{kpi.respCaption}}"></x-import>
<x-import component-from-global-scope="Abt.KpiTile" label="평균 처리 기간" value="2.4" unit="일" caption="종결 기준 · 목표 3일"></x-import>
</section>
<x-import component-from-global-scope="Abt.Alert" tone="attention" title="반복 문제: 고비 오아시스 캠프 90일간 클레임 3건" action="{{partnerAction}}">이용 9건 중 3건(책임 확인 1건) · 온수·식사 관련 · 거래 조건 검토 대상입니다.</x-import>

<sc-if value="{{creating}}" hint-placeholder-val="{{false}}">
''' + PANEL + panel_title('클레임 접수', '긴급 안전사고는 일반 클레임과 따로 표시하고 운영 책임자에게 바로 알립니다') + field_grid(200) + '''
<x-import component-from-global-scope="Abt.Select" label="행사" required="{{yes}}" options="{{eventOptions}}" value="{{nf.code}}" on-change="{{onNf.code}}" error="{{nfErr.code}}"></x-import>
<x-import component-from-global-scope="Abt.Select" label="유형" options="{{typeOptions}}" value="{{nf.type}}" on-change="{{onNf.type}}"></x-import>
<x-import component-from-global-scope="Abt.Select" label="접수 경로" options="{{sourceOptions}}" value="{{nf.source}}" on-change="{{onNf.source}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="발생 장소" value="{{nf.place}}" on-change="{{onNf.place}}"></x-import>
</div>
<div style="display: flex; align-items: center; gap: 12px"><span class="label" style="color: var(--ink-muted)">긴급도</span><x-import component-from-global-scope="Abt.Segmented" size="sm" options="{{urgencyOptions}}" value="{{nf.urgency}}" on-change="{{onNf.urgency}}" aria-label="긴급도"></x-import></div>
<x-import component-from-global-scope="Abt.TextField" label="내용" required="{{yes}}" multiline="{{yes}}" rows="{{two}}" placeholder="무슨 일이 언제 어디서 있었는지, 고객 반응과 초기 조치를 적습니다" value="{{nf.desc}}" on-change="{{onNf.desc}}" error="{{nfErr.desc}}"></x-import>
<div style="display: flex; justify-content: flex-end; gap: 8px">
<x-import component-from-global-scope="Abt.Button" variant="ghost" on-click="{{toggleNew}}">취소</x-import>
<x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{submitNew}}">접수</x-import>
</div>
</section>
</sc-if>

<div style="display: flex; align-items: center; justify-content: space-between; gap: 12px">
<x-import component-from-global-scope="Abt.Segmented" options="{{filterOptions}}" value="{{filter}}" on-change="{{setFilter}}" aria-label="처리 상태"></x-import>
<span class="caption" style="color: var(--ink-muted)">행을 누르면 오른쪽에서 다음 단계를 처리합니다</span>
</div>
''' + TWO_PANE + '''
<x-import component-from-global-scope="Abt.DataTable" columns="{{cols}}" rows="{{rows}}" on-row-click="{{pick}}" caption="클레임 목록" empty="이 상태의 클레임이 없습니다."></x-import>
''' + SIDE_PANEL + '''<div style="display: flex; flex-direction: column; gap: 8px">
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px">
<span style="font: 500 13px/20px var(--font-mono)">{{cur.id}}</span>
<x-import component-from-global-scope="Abt.StatusBadge" axis="claim" status="{{cur.stage}}" size="md"></x-import>
<sc-if value="{{cur.isOverdue}}" hint-placeholder-val="{{false}}"><x-import component-from-global-scope="Abt.StatusBadge" axis="claim" status="overdue" size="md"></x-import></sc-if>
<sc-if value="{{cur.isUrgent}}" hint-placeholder-val="{{false}}"><x-import component-from-global-scope="Abt.StatusBadge" axis="claim" status="urgent" size="md"></x-import></sc-if>
</div>
<h2 class="title-2" style="margin: 0">{{cur.title}}</h2>
<div style="display: flex; align-items: center; gap: 8px"><x-import component-from-global-scope="Abt.EventCode" code="{{cur.code}}" href="EventDetail.dc.html"></x-import><span class="caption" style="color: var(--ink-muted)">{{cur.agency}}</span></div>
</div>
''' + dl([('유형·긴급도', '{{cur.type}} · {{cur.urgency}}'), ('발생', '{{cur.place}}'), ('접수', '{{cur.received}}'), ('내용', '{{cur.desc}}'), ('처리 기한', '{{cur.dueText}}')], 88) + '''<x-import component-from-global-scope="Abt.ApprovalSteps" steps="{{cur.steps}}" orientation="vertical"></x-import>
<sc-if value="{{cur.isOpen}}" hint-placeholder-val="{{true}}">
<div style="display: flex; flex-direction: column; gap: 12px; padding-top: 12px; border-top: 1px solid var(--line)">
''' + field_grid(140) + '''
<x-import component-from-global-scope="Abt.Select" label="담당" options="{{ownerOptions}}" value="{{cur.owner}}" on-change="{{onCur.owner}}"></x-import>
<x-import component-from-global-scope="Abt.Select" label="책임 확인" options="{{respOptions}}" value="{{cur.resp}}" on-change="{{onCur.resp}}" error="{{err.resp}}"></x-import>
</div>
<x-import component-from-global-scope="Abt.TextField" label="조치 내용" multiline="{{yes}}" rows="{{two}}" value="{{cur.action}}" on-change="{{onCur.action}}" error="{{err.action}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="보상" input-mode="numeric" align="end" suffix="MNT" value="{{cur.compText}}" on-change="{{onCur.comp}}" help="{{cur.compNote}}"></x-import>
<sc-if value="{{cur.showPrevent}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.TextField" label="재발 방지" multiline="{{yes}}" rows="{{two}}" placeholder="원인과 개선 조치, 완료 기한" value="{{cur.prevent}}" on-change="{{onCur.prevent}}" error="{{err.prevent}}"></x-import>
<x-import component-from-global-scope="Abt.Checkbox" label="장소별 매뉴얼에 반영" description="매뉴얼 담당자에게 검토 요청이 갑니다 · 고객 개인정보는 옮기지 않습니다" checked="{{cur.manual}}" on-change="{{onCur.manual}}"></x-import>
</sc-if>
<div style="display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 8px">
<sc-if value="{{cur.canComp}}" hint-placeholder-val="{{true}}"><x-import component-from-global-scope="Abt.Button" variant="secondary" on-click="{{requestComp}}">보상 승인 요청</x-import></sc-if>
<x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{advance}}">{{cur.nextLabel}}</x-import>
</div>
</div>
</sc-if>
<sc-if value="{{cur.isClosed}}" hint-placeholder-val="{{false}}">
<p class="caption" style="margin: 0; padding-top: 12px; border-top: 1px solid var(--line); color: var(--ink-muted)">{{cur.closedText}}</p>
</sc-if>
</section>
</div>
'''

pre = '''
    const ORDER = ['received', 'investigating', 'acting', 'resolved', 'closed'];
    const LABEL = ['접수', '조사', '조치', '해결 확인', '종결'];
    const NEXT = { received: '조사 시작', investigating: '조치 단계로', acting: '해결 확인', resolved: '종결' };
    const C = s.claims;
    const cur = C.find((c) => c.id === s.selected) || C[0];
    const isOpenC = (c) => c.stage !== 'resolved' && c.stage !== 'closed';
    const filter = s.filter;
    const list = C.filter((c) => (filter === '미해결' ? isOpenC(c) : filter === '해결·종결' ? !isOpenC(c) : true));
    const open = C.filter(isOpenC);
    const overdue = open.filter((c) => c.overdueDays > 0);
    const compOpen = open.reduce((a, c) => a + (Number(c.comp) || 0), 0);
    const upd = (patch) => set({ claims: C.map((c) => (c.id === cur.id ? { ...c, ...patch } : c)), errs: {} });
    const E = s.errs || {};
    const NOW = '10.01 15:55 KST';
    const stepsOf = (c) => ORDER.map((st, i) => {
      const idx = ORDER.indexOf(c.stage);
      const log = (c.log || {})[st] || {};
      const state = i < idx || c.stage === 'closed' ? 'done' : i === idx ? (c.stage === 'resolved' && i === 3 ? 'done' : 'current') : 'pending';
      const fixed = c.stage === 'resolved' && i === 4 ? 'current' : state;
      return { label: LABEL[i], state: fixed, actor: log.actor, at: log.at, note: log.note };
    });
    const nf = s.nf;
    const EV = [
      { value: '', label: '선택하세요' },
      { value: 'MN2609-038', label: 'MN2609-038 · 제이원트래블 (진행 중)' },
      { value: 'MN2609-040', label: 'MN2609-040 · 솔빛여행 (진행 중)' },
      { value: 'MN2610-002', label: 'MN2610-002 · 푸른하늘여행 (10.02 출발)' },
      { value: 'MN2609-031', label: 'MN2609-031 · 다온여행사 (완료)' },
      { value: 'MN2609-033', label: 'MN2609-033 · 푸른하늘여행 (완료)' }
    ];
    const AG = { 'MN2609-038': '제이원트래블', 'MN2609-040': '솔빛여행', 'MN2610-002': '푸른하늘여행', 'MN2609-031': '다온여행사', 'MN2609-033': '푸른하늘여행' };
'''
vals = '''      navCounts: { alerts: 5, field: 2, claims: { n: open.length, tone: overdue.length ? 'critical' : 'attention' }, receipts: { n: 1, tone: 'critical' }, costs: { n: 7, tone: 'attention' }, remit: 3 },
      kpi: { open: open.length, openState: overdue.length ? 'critical' : undefined, overdueLabel: overdue.length ? `기한 초과 ${overdue.length}건` : '', comp: { amount: compOpen, currency: 'MNT', compact: false }, month: C.filter((c) => c.recent).length, respCaption: `책임 확인 ${C.filter((c) => c.recent && c.resp !== '확인 전').length}건 · 이용 41건 대비` },
      partnerAction: { label: '협력업체 보기', href: 'Partners.dc.html' },
      creating: !!s.creating,
      newLabel: s.creating ? '접수 닫기' : '클레임 접수',
      toggleNew: () => set({ creating: !s.creating, nfErr: {} }),
      eventOptions: EV,
      typeOptions: ['숙소 시설', '차량', '식사', '가이드', '일정', '안전사고', '기타'],
      sourceOptions: ['가이드 현장 보고', '여행사', '고객 직접'],
      urgencyOptions: ['보통', '긴급'],
      nf,
      onNf: { code: (e) => set({ nf: { ...s.nf, code: e.target.value } }), type: (e) => set({ nf: { ...s.nf, type: e.target.value } }), source: (e) => set({ nf: { ...s.nf, source: e.target.value } }), place: (e) => set({ nf: { ...s.nf, place: e.target.value } }), urgency: (v) => set({ nf: { ...s.nf, urgency: v } }), desc: (e) => set({ nf: { ...s.nf, desc: e.target.value } }) },
      nfErr: s.nfErr || {},
      submitNew: () => {
        const er = { code: nf.code ? '' : '행사를 고르세요.', desc: nf.desc.trim() ? '' : '내용을 적어 주세요.' };
        if (er.code || er.desc) { set({ nfErr: er }); return; }
        const urgent = nf.urgency === '긴급';
        const c = { id: 'CL2610-002', code: nf.code, agency: AG[nf.code], title: nf.desc.trim().slice(0, 28), type: nf.type, urgency: nf.urgency, place: nf.place || '—', received: `${NOW} · ${nf.source}`, desc: nf.desc.trim(), owner: '김지훈', due: '10.04(일)', dueText: '10.04(일) · 3일 남음', stage: 'received', overdueDays: 0, resp: '확인 전', comp: '', compNote: '보상이 정해지면 금액을 적고 승인 요청합니다', action: '', prevent: '', manual: false, recent: true, urgent, log: { received: { actor: '김지훈', at: NOW } } };
        this.setState({ claims: [c].concat(C), selected: c.id, creating: false, filter: '미해결', nf: { code: '', type: '숙소 시설', source: '가이드 현장 보고', place: '', urgency: '보통', desc: '' }, notice: urgent ? { tone: 'critical', title: 'CL2610-002 긴급 건으로 접수했습니다', body: '운영 책임자(김지훈)와 대표(이도윤)에게 바로 알렸습니다. 처리 기한 10.04(일).' } : { tone: 'positive', title: 'CL2610-002 접수했습니다', body: '담당 김지훈 · 처리 기한 10.04(일). 다음 단계는 조사입니다.' } });
      },
      filterOptions: [ { value: '미해결', label: `미해결 ${open.length}` }, { value: '해결·종결', label: `해결·종결 ${C.length - open.length}` }, { value: '전체', label: '전체' } ],
      filter,
      setFilter: (v) => set({ filter: v }),
      cols: [
        { key: 'what', label: '클레임', type: 'stack' },
        { key: 'code', label: '행사', type: 'code' },
        { key: 'title', label: '내용', type: 'strong', wrap: true },
        { key: 'due', label: '기한', type: 'stack' },
        { key: 'status', label: '상태', type: 'status', axis: 'claim' }
      ],
      rows: list.map((c) => ({ id: c.id, what: { primary: c.id, secondary: c.type }, code: c.code, title: c.title, due: { primary: c.due, secondary: c.overdueDays > 0 && isOpenC(c) ? `${c.overdueDays}일 초과` : c.owner }, status: c.urgent && isOpenC(c) ? 'urgent' : c.overdueDays > 0 && isOpenC(c) ? 'overdue' : c.stage, selected: c.id === cur.id })),
      pick: (row) => set({ selected: row.id, errs: {} }),
      ownerOptions: ['김지훈', '정하린', '오세진'],
      respOptions: ['확인 전', '업체 책임', '회사 책임', '가이드 책임', '고객 사유', '불가항력'],
      cur: { ...cur, isOverdue: cur.overdueDays > 0 && isOpenC(cur), isUrgent: !!cur.urgent, steps: stepsOf(cur), isOpen: cur.stage !== 'closed', isClosed: cur.stage === 'closed', nextLabel: NEXT[cur.stage] || '', showPrevent: cur.stage === 'resolved', canComp: cur.stage !== 'received' && cur.stage !== 'closed' && !cur.compRequested, compText: cur.comp === '' || cur.comp == null ? '' : String(cur.comp), dueText: cur.dueText || `${cur.due}${cur.overdueDays > 0 && isOpenC(cur) ? ` · ${cur.overdueDays}일 초과 · 운영관리자 재알림 2회` : ''}`, closedText: cur.closedText || '종결된 클레임입니다. 처리 단계와 보상 내역은 그대로 남습니다.' },
      onCur: { owner: (e) => upd({ owner: e.target.value }), resp: (e) => upd({ resp: e.target.value }), action: (e) => upd({ action: e.target.value }), comp: (e) => upd({ comp: e.target.value.replace(/[^0-9]/g, '') }), prevent: (e) => upd({ prevent: e.target.value }), manual: (e) => upd({ manual: e.target.checked }) },
      err: { resp: E.resp || '', action: E.action || '', prevent: E.prevent || '' },
      requestComp: () => {
        const amt = Number(cur.comp) || 0;
        if (!amt) { set({ notice: { tone: 'attention', title: '보상 금액을 먼저 적어 주세요', body: '보상 비용은 비용 승인(운영 확인 → 회계 검토 → 권한자 승인)을 거칩니다.' } }); return; }
        set({ claims: C.map((c) => (c.id === cur.id ? { ...c, compRequested: true, compNote: `${fmt(amt)} MNT 승인 요청됨 · ${NOW}` } : c)), notice: { tone: 'progress', title: `${cur.id} 보상 ${fmt(amt)} MNT 승인 요청`, body: '비용 승인 화면의 보상·기타 항목으로 올라갔습니다. 승인 전에는 정산에 반영되지 않습니다.', action: { label: '비용 승인', href: 'Approvals.dc.html' } } });
      },
      advance: () => {
        const st = cur.stage;
        const er = {};
        if (st === 'investigating' && !cur.action.trim()) er.action = '어떤 조치를 했는지 적어야 다음 단계로 갑니다.';
        if (st === 'acting' && cur.resp === '확인 전') er.resp = '책임 확인 결과를 고르세요.';
        if (st === 'acting' && !cur.action.trim()) er.action = '조치 내용을 적어 주세요.';
        if (st === 'resolved' && !cur.prevent.trim()) er.prevent = '종결 전에 재발 방지 내용을 적어 주세요.';
        if (Object.keys(er).length) { set({ errs: er }); return; }
        const nextStage = ORDER[ORDER.indexOf(st) + 1];
        const log = { ...(cur.log || {}), [nextStage]: { actor: cur.owner, at: NOW, note: nextStage === 'acting' ? cur.action : nextStage === 'resolved' ? `책임: ${cur.resp}` : nextStage === 'closed' ? cur.prevent : undefined } };
        set({ claims: C.map((c) => (c.id === cur.id ? { ...c, stage: nextStage, log, overdueDays: nextStage === 'resolved' || nextStage === 'closed' ? c.overdueDays : c.overdueDays } : c)), notice: { tone: 'positive', title: nextStage === 'closed' ? `${cur.id} · 종결했습니다` : `${cur.id} · ${LABEL[ORDER.indexOf(nextStage)]} 단계로 옮겼습니다`, body: nextStage === 'closed' ? `미해결에서 빠졌습니다.${cur.manual ? ' 매뉴얼 반영 요청을 보냈습니다.' : ''}` : '처리 이력에 담당자와 시각이 남았습니다.' } });
      },'''

state = '''{ filter: '미해결', selected: 'CL2609-004', creating: false, errs: {}, nfErr: {}, notice: null,
      nf: { code: '', type: '숙소 시설', source: '가이드 현장 보고', place: '', urgency: '보통', desc: '' },
      claims: [
        { id: 'CL2609-004', code: 'MN2609-031', agency: '다온여행사', title: '홉스골 숙소 온수 미공급', type: '숙소 시설', urgency: '보통', place: '09.24(목) 19:00 ULAT · 홉스골 호숫가 게르 캠프', received: '09.24 21:30 ULAT · 가이드 간바타르 현장 보고(FR-0995)', desc: '게르 6동 온수 이틀간 미공급 · 고객 12명 불편 · 여행사 공식 항의(09.26)', owner: '김지훈', due: '09.28(월)', stage: 'acting', overdueDays: 3, resp: '확인 전', comp: '240000', compNote: '1인 10,000 MNT × 24명 · 캠프에 청구 예정', action: '캠프와 보상 협의 중 · 여행사에 사과 공문(09.29)', prevent: '', manual: false, recent: true, log: { received: { actor: '간바타르', at: '09.24 21:30 ULAT' }, investigating: { actor: '김지훈', at: '09.25 10:10 KST', note: '캠프 보일러 고장 확인' }, acting: { actor: '김지훈', at: '09.29 11:00 KST', note: '사과 공문 · 보상 협의 시작' } } },
        { id: 'CL2610-001', code: 'MN2609-040', agency: '솔빛여행', title: '스타렉스 에어컨 고장', type: '차량', urgency: '보통', place: '10.01(목) 08:20 ULAT · 울란바토르 시내 이동 중', received: '10.01 08:40 ULAT · 가이드 오윤치메그', desc: '이동 중 에어컨 고장 · 고객 2명 멀미 호소 · 오후 일정은 정상 진행', owner: '김지훈', due: '10.04(일)', stage: 'investigating', overdueDays: 0, resp: '확인 전', comp: '80000', compNote: '음료·휴식 비용', action: '', prevent: '', manual: false, recent: true, log: { received: { actor: '오윤치메그', at: '10.01 08:40 ULAT' }, investigating: { actor: '김지훈', at: '10.01 10:05 KST', note: '기사 바타에게 수리 일정 확인 중' } } },
        { id: 'CL2609-003', code: 'MN2609-033', agency: '푸른하늘여행', title: '고비 오아시스 캠프 온수 고장', type: '숙소 시설', urgency: '보통', place: '09.25(금) 21:30 ULAT · 고비 오아시스 캠프', received: '09.25 22:10 ULAT · 가이드 바트-에르덴', desc: '온수 공급 약 10시간 중단 · 고객 8명 불편 호소', owner: '김지훈', due: '09.28(월)', stage: 'resolved', overdueDays: 0, resp: '업체 책임', comp: '2260000', compNote: '1박 숙박비 환불 · 09.26 이도윤 승인', compRequested: true, action: '1박 숙박비 환불', prevent: '', manual: false, recent: true, log: { received: { actor: '바트-에르덴', at: '09.25 22:10 ULAT' }, investigating: { actor: '김지훈', at: '09.26 08:30 KST' }, acting: { actor: '김지훈', at: '09.26 09:15 KST', note: '1박 환불 · 이도윤 승인' }, resolved: { actor: '푸른하늘여행 최민정', at: '09.27 18:00 KST' } } },
        { id: 'CL2609-002', code: 'MN2609-029', agency: '한빛투어', title: '골프장 티오프 40분 지연', type: '일정', urgency: '보통', place: '09.14(월) 07:20 ULAT · 스카이 리조트 골프장', received: '09.14 08:10 ULAT · 여행사', desc: '앞 팀 지연으로 티오프 40분 늦어짐 · 점심 일정 조정', owner: '정하린', due: '09.17(목)', stage: 'closed', overdueDays: 0, resp: '업체 책임', comp: '', compNote: '보상 없음 · 골프장 음료 제공', compRequested: true, action: '골프장 음료 제공 · 오후 일정 조정', prevent: '티오프 2시간 전 재확인 · 상품별 매뉴얼(골프)에 반영', manual: true, recent: false, closedText: '09.16 종결 · 상품별 매뉴얼(골프)에 반영했습니다.', log: { received: { actor: '한빛투어', at: '09.14 08:10' }, investigating: { actor: '정하린', at: '09.14 09:00' }, acting: { actor: '정하린', at: '09.14 10:30' }, resolved: { actor: '한빛투어', at: '09.15 17:00' }, closed: { actor: '정하린', at: '09.16 11:00' } } },
        { id: 'CL2609-001', code: 'MN2609-021', agency: '누리투어', title: '푸르공 3호차 엔진 고장', type: '차량', urgency: '긴급', place: '09.08(화) 14:10 ULAT · 테를지 진입로', received: '09.08 14:20 ULAT · 가이드 간바타르', desc: '이동 중 엔진 과열로 정차 · 대체 차량 50분 후 도착 · 부상 없음', owner: '김지훈', due: '09.11(금)', stage: 'closed', overdueDays: 0, resp: '업체 책임', comp: '', compNote: '보상 없음', compRequested: true, action: '대체 차량 투입 · 업체 정비 기록 요청', prevent: '출발 전 차량 점검표 제출 의무화', manual: true, recent: false, closedText: '09.12 종결 · 장소별 매뉴얼(테를지 이동)에 반영했습니다.', log: { received: { actor: '간바타르', at: '09.08 14:20' }, investigating: { actor: '김지훈', at: '09.08 15:00' }, acting: { actor: '김지훈', at: '09.08 15:10' }, resolved: { actor: '누리투어', at: '09.10 10:00' }, closed: { actor: '김지훈', at: '09.12 09:00' } } }
      ] }'''
admin('Claims.dc.html', '클레임', 'claims', 'ops', body, pre=pre, vals=vals, state=state, height=1400)
print('Claims written')
