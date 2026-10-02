import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import *
from shared_data import MANUALS_BASE_JS

ROW = 'display: grid; grid-template-columns: minmax(0, 1fr) auto; align-items: center; gap: 12px; padding: 8px 0; border-top: 1px solid var(--line); font-size: 13px; line-height: 20px'
SUB = '<span class="label" style="color: var(--ink-muted); padding-top: 4px">{}</span>'

# ------------------------------------------------------------------ Resources (가이드·차량) — master list that feeds the assignment calendar
body = header('가이드·차량', '배정 캘린더의 가이드·차량 명단은 이 화면에서 옵니다 · 등록하면 바로 배정 후보가 되고, 여기서 넣은 불가일은 캘린더에 회색으로 표시됩니다', '''<x-import component-from-global-scope="Abt.Segmented" options="{{kindOptions}}" value="{{kind}}" on-change="{{setKind}}" aria-label="구분"></x-import>
<x-import component-from-global-scope="Abt.Button" variant="ghost" href="Schedule.dc.html">배정 캘린더</x-import>
<x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{toggleNew}}">{{addLabel}}</x-import>''')
body += NOTICE
body += '''<sc-if value="{{newGuide}}" hint-placeholder-val="{{false}}">
''' + PANEL + panel_title('가이드 등록', '저장하면 배정 캘린더 가이드 명단과 배정 후보에 바로 들어갑니다') + field_grid(200) + '''
<x-import component-from-global-scope="Abt.TextField" label="이름" required="{{yes}}" value="{{gf.name}}" on-change="{{onG.name}}" error="{{gErr.name}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="연락처" required="{{yes}}" placeholder="+976 0000-0000" value="{{gf.phone}}" on-change="{{onG.phone}}" error="{{gErr.phone}}"></x-import>
<x-import component-from-global-scope="Abt.Select" label="언어" options="{{langOptions}}" value="{{gf.lang}}" on-change="{{onG.lang}}"></x-import>
<x-import component-from-global-scope="Abt.Select" label="전문 상품" options="{{specOptions}}" value="{{gf.spec}}" on-change="{{onG.spec}}"></x-import>
<x-import component-from-global-scope="Abt.Select" label="계약" options="{{contractOptions}}" value="{{gf.contract}}" on-change="{{onG.contract}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="가이드비(일)" input-mode="numeric" align="end" suffix="MNT" value="{{gf.rate}}" on-change="{{onG.rate}}"></x-import>
</div>
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 12px 20px">
<div style="display: flex; align-items: center; gap: 10px"><span class="label" style="color: var(--ink-muted)">등급</span><x-import component-from-global-scope="Abt.Segmented" size="sm" options="{{gradeOptions}}" value="{{gf.grade}}" on-change="{{onG.grade}}" aria-label="등급"></x-import></div>
<x-import component-from-global-scope="Abt.Checkbox" label="가이드 앱 초대 문자 보내기" description="사용자·권한에 가이드 역할로 추가되고, 본인 배정 행사만 봅니다" checked="{{gf.invite}}" on-change="{{onG.invite}}"></x-import>
</div>
<div style="display: flex; justify-content: flex-end; gap: 8px"><x-import component-from-global-scope="Abt.Button" variant="ghost" on-click="{{toggleNew}}">취소</x-import><x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{saveGuide}}">가이드 등록</x-import></div>
</section>
</sc-if>
<sc-if value="{{newVehicle}}" hint-placeholder-val="{{false}}">
''' + PANEL + panel_title('차량 등록', '저장하면 배정 캘린더 차량 명단에 들어가고, 정원으로 좌석을 계산합니다') + field_grid(200) + '''
<x-import component-from-global-scope="Abt.Select" label="차종" options="{{typeOptions}}" value="{{vf.type}}" on-change="{{onV.type}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="표시 이름" value="{{vf.name}}" on-change="{{onV.name}}" error="{{vErr.name}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="차량번호" required="{{yes}}" placeholder="예: 21-52 УБА" value="{{vf.plate}}" on-change="{{onV.plate}}" error="{{vErr.plate}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="정원(기사 제외)" input-mode="numeric" align="end" suffix="석" value="{{vf.cap}}" on-change="{{onV.cap}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="기사" required="{{yes}}" value="{{vf.driver}}" on-change="{{onV.driver}}" error="{{vErr.driver}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="기사 연락처" placeholder="+976 0000-0000" value="{{vf.phone}}" on-change="{{onV.phone}}"></x-import>
<x-import component-from-global-scope="Abt.Select" label="소속" options="{{ownerOptions}}" value="{{vf.owner}}" on-change="{{onV.owner}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="보험 만료" type="date" value="{{vf.insurance}}" on-change="{{onV.insurance}}"></x-import>
</div>
<p class="caption" style="margin: 0; color: var(--ink-muted)">{{fuelText}}</p>
<div style="display: flex; justify-content: flex-end; gap: 8px"><x-import component-from-global-scope="Abt.Button" variant="ghost" on-click="{{toggleNew}}">취소</x-import><x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{saveVehicle}}">차량 등록</x-import></div>
</section>
</sc-if>
''' + TWO_PANE + '''
<x-import component-from-global-scope="Abt.DataTable" columns="{{cols}}" rows="{{rows}}" on-row-click="{{pick}}" caption="{{kind}} 목록"></x-import>
''' + SIDE_PANEL + '''<div style="display: flex; flex-direction: column; gap: 6px">
<div style="display: flex; align-items: center; justify-content: space-between; gap: 8px"><span class="caption" style="color: var(--ink-muted)">{{cur.sub}}</span><x-import component-from-global-scope="Abt.StatusBadge" tone="{{cur.tone}}" form="{{cur.form}}" size="md">{{cur.stLabel}}</x-import></div>
<h2 class="title-2" style="margin: 0">{{cur.name}}</h2>
</div>
<sc-for list="{{cur.facts}}" as="f" hint-placeholder-count="5">
<div style="display: grid; grid-template-columns: 88px minmax(0, 1fr); gap: 12px; font-size: 13px; line-height: 20px"><span class="label" style="color: var(--ink-muted); line-height: 20px">{{f.k}}</span><span>{{f.v}}</span></div>
</sc-for>
<div style="display: flex; flex-direction: column">
''' + SUB.format('{{cur.offTitle}}') + '''
<sc-for list="{{cur.offs}}" as="o" hint-placeholder-count="2">
<div style="''' + ROW + '''"><span>{{o.range}}</span><span class="caption" style="color: var(--ink-muted)">{{o.why}}</span></div>
</sc-for>
<sc-if value="{{cur.noOffs}}" hint-placeholder-val="{{false}}"><p class="caption" style="margin: 0; padding: 8px 0; border-top: 1px solid var(--line); color: var(--ink-muted)">등록된 날이 없습니다.</p></sc-if>
</div>
<div style="display: flex; flex-direction: column; gap: 10px; padding-top: 12px; border-top: 1px solid var(--line)">
<span class="body-strong" style="font-size: 13px">{{cur.addTitle}}</span>
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px">
<x-import component-from-global-scope="Abt.TextField" label="시작" type="date" size="sm" value="{{off.from}}" on-change="{{onOff.from}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="끝" type="date" size="sm" value="{{off.to}}" on-change="{{onOff.to}}" error="{{offError}}"></x-import>
</div>
<x-import component-from-global-scope="Abt.Select" label="사유" size="sm" options="{{reasonOptions}}" value="{{off.why}}" on-change="{{onOff.why}}"></x-import>
<div style="display: flex; justify-content: flex-end; gap: 8px"><x-import component-from-global-scope="Abt.Button" size="sm" href="Schedule.dc.html">배정 캘린더에서 보기</x-import><x-import component-from-global-scope="Abt.Button" size="sm" variant="primary" on-click="{{addOff}}">등록</x-import></div>
</div>
</section>
</div>
'''
pre = '''
    const kind = s.kind;
    const isG = kind === '가이드';
    const shared = (k, local) => { const v = store.get(k, null); return v == null ? local : v; };
    const share = (k, v, localKey) => { store.put(k, v); set({ [localKey]: v }); };
    const SG = shared('guides', s.localGuides);
    const SV = shared('vehicles', s.localVehicles);
    const OFFS = shared('offs', s.localOffs);
    const lab = (iso) => (iso ? `${iso.slice(5, 7)}.${iso.slice(8, 10)}` : '');
    const KIND = { '푸르공(UAZ-452)': { cap: 8, fuel: 18, base: '푸르공' }, '랜드크루저': { cap: 6, fuel: 14, base: '랜드크루저' }, '스타렉스': { cap: 11, fuel: 11, base: '스타렉스' }, '25인승 버스': { cap: 25, fuel: 27, base: '25인승 버스' }, '45인승 버스': { cap: 45, fuel: 30, base: '45인승 버스' } };
    const newG = SG.map((g) => ({ id: g.id, name: g.name, sub: `${g.lang} · ${g.spec} · 새로 등록`, lang: g.lang, days: 0, claims: 0, state: 'free', stText: '배정 가능', jobs: [], facts: [ { k: '연락처', v: g.phone }, { k: '등급', v: `${g.grade} · ${g.contract}` }, { k: '가이드비', v: `일 ${fmt(Number(g.rate) || 0)} MNT` }, { k: '가이드 앱', v: g.invite ? '초대 문자 보냄(10.02)' : '아직 초대하지 않음' } ], offs: [] }));
    const newV = SV.map((v) => ({ id: v.id, name: v.name, sub: `${v.type} · ${v.plate} · 새로 등록`, driver: v.driver, cap: v.cap, fuel: `${v.fuel} L/100km`, state: 'free', stText: '배정 가능', jobs: [], facts: [ { k: '차량번호', v: v.plate }, { k: '기사', v: `${v.driver}${v.phone ? ' · ' + v.phone : ''}` }, { k: '소속', v: v.owner }, { k: '보험', v: v.insurance ? `${v.insurance.replace(/-/g, '.')}까지` : '확인 필요' } ], offs: [] }));
    const withOffs = (x) => ({ ...x, offs: x.offs.concat((OFFS[x.id] || []).map((o) => ({ range: `${lab(o.from)} – ${lab(o.to)}`, why: o.why }))) });
    const G = s.guides.concat(newG).map(withOffs);
    const V = s.vehicles.concat(newV).map(withOffs);
    const list = isG ? G : V;
    const cur = list.find((x) => x.id === s.selected) || list[0];
    const off = s.off;
    const gf = s.gf, vf = s.vf;
    const nextName = (t) => { const base = KIND[t].base; if (base !== '푸르공' && base !== '랜드크루저') return base + (V.some((x) => x.name.indexOf(base) === 0) ? ` ${V.filter((x) => x.name.indexOf(base) === 0).length + 1}호` : ''); const k = V.filter((x) => x.name.indexOf(base) === 0).length + 1; return base === '푸르공' ? `푸르공 ${k}호차` : `랜드크루저 ${k}호`; };
'''
vals = '''      kindOptions: ['가이드', '차량·기사'],
      kind,
      setKind: (v) => set({ kind: v, selected: v === '가이드' ? 'g1' : 'v1', adding: false }),
      addLabel: s.adding ? '등록 닫기' : isG ? '가이드 등록' : '차량 등록',
      toggleNew: () => set({ adding: !s.adding, gErr: {}, vErr: {}, vf: s.adding ? s.vf : { ...s.vf, name: nextName(s.vf.type) } }),
      newGuide: !!s.adding && isG,
      newVehicle: !!s.adding && !isG,
      langOptions: ['한국어', '한국어·영어', '한국어·일본어', '한국어·러시아어', '한국어·중국어'],
      specOptions: ['고비·사막', '홉스골', '골프', '시티', '기업 단체', '승마·체험'],
      contractOptions: ['프리랜서', '정규'],
      gradeOptions: ['A', 'B', 'C'],
      gf,
      onG: { name: (e) => set({ gf: { ...s.gf, name: e.target.value }, gErr: {} }), phone: (e) => set({ gf: { ...s.gf, phone: e.target.value }, gErr: {} }), lang: (e) => set({ gf: { ...s.gf, lang: e.target.value } }), spec: (e) => set({ gf: { ...s.gf, spec: e.target.value } }), contract: (e) => set({ gf: { ...s.gf, contract: e.target.value } }), rate: (e) => set({ gf: { ...s.gf, rate: e.target.value } }), grade: (v) => set({ gf: { ...s.gf, grade: v } }), invite: (e) => set({ gf: { ...s.gf, invite: e.target.checked } }) },
      gErr: s.gErr || {},
      saveGuide: () => {
        const name = gf.name.trim();
        const er = { name: !name ? '이름을 입력하세요.' : G.some((x) => x.name === name) ? '같은 이름의 가이드가 있습니다. 구분할 수 있게 적어 주세요.' : '', phone: gf.phone.trim() ? '' : '연락처를 입력하세요.' };
        if (er.name || er.phone) { set({ gErr: er }); return; }
        const g = { id: 'gx' + Date.now().toString(36), name, phone: gf.phone.trim(), lang: gf.lang, spec: gf.spec, contract: gf.contract, rate: String(gf.rate).replace(/[^0-9]/g, '') || '0', grade: gf.grade, invite: gf.invite };
        const next = SG.concat([g]);
        store.put('guides', next);
        this.setState({ localGuides: next, adding: false, selected: g.id, gf: { name: '', phone: '', lang: '한국어', spec: '고비·사막', contract: '프리랜서', rate: '200000', grade: 'C', invite: true }, notice: { tone: 'positive', title: `${name} 가이드를 등록했습니다`, body: `배정 캘린더 가이드 명단과 배정 후보에 바로 들어갔습니다.${g.invite ? ' 가이드 앱 초대 문자를 보냈습니다.' : ''}`, action: { label: '배정 캘린더', href: 'Schedule.dc.html' } } });
      },
      typeOptions: Object.keys(KIND),
      ownerOptions: ['고비모터스', '자사 차량', '울란바토르 렌터카'],
      vf,
      onV: { type: (e) => { const t = e.target.value; set({ vf: { ...s.vf, type: t, cap: String(KIND[t].cap), name: nextName(t) } }); }, name: (e) => set({ vf: { ...s.vf, name: e.target.value }, vErr: {} }), plate: (e) => set({ vf: { ...s.vf, plate: e.target.value }, vErr: {} }), cap: (e) => set({ vf: { ...s.vf, cap: e.target.value } }), driver: (e) => set({ vf: { ...s.vf, driver: e.target.value }, vErr: {} }), phone: (e) => set({ vf: { ...s.vf, phone: e.target.value } }), owner: (e) => set({ vf: { ...s.vf, owner: e.target.value } }), insurance: (e) => set({ vf: { ...s.vf, insurance: e.target.value } }) },
      vErr: s.vErr || {},
      fuelText: `연비 기준 ${KIND[vf.type].fuel} L/100km(차종 기본값) · 유류비 예상은 협력업체·요금표에서 이 값으로 계산합니다`,
      saveVehicle: () => {
        const er = { name: vf.name.trim() ? (V.some((x) => x.name === vf.name.trim()) ? '같은 이름의 차량이 있습니다.' : '') : '표시 이름을 입력하세요.', plate: vf.plate.trim() ? '' : '차량번호를 입력하세요.', driver: vf.driver.trim() ? '' : '기사 이름을 입력하세요.' };
        if (er.name || er.plate || er.driver) { set({ vErr: er }); return; }
        const cap = Number(String(vf.cap).replace(/[^0-9]/g, '')) || KIND[vf.type].cap;
        const v = { id: 'vx' + Date.now().toString(36), name: vf.name.trim(), type: vf.type, plate: vf.plate.trim(), cap, driver: vf.driver.trim(), phone: vf.phone.trim(), owner: vf.owner, insurance: vf.insurance, fuel: KIND[vf.type].fuel };
        const next = SV.concat([v]);
        store.put('vehicles', next);
        this.setState({ localVehicles: next, adding: false, selected: v.id, vf: { type: '푸르공(UAZ-452)', name: '', plate: '', cap: '8', driver: '', phone: '', owner: '고비모터스', insurance: '' }, notice: { tone: 'positive', title: `${v.name}(${cap}석)을 등록했습니다`, body: '배정 캘린더 차량 명단에 들어갔고, 좌석 계산에 바로 쓰입니다.', action: { label: '배정 캘린더', href: 'Schedule.dc.html' } } });
      },
      cols: isG ? [
        { key: 'name', label: '가이드', type: 'stack' },
        { key: 'lang', label: '언어', type: 'muted' },
        { key: 'days', label: '10월 가동', type: 'number', suffix: '일' },
        { key: 'claims', label: '클레임(90일)', type: 'number', suffix: '건' },
        { key: 'st', label: '상태', type: 'status' }
      ] : [
        { key: 'name', label: '차량', type: 'stack' },
        { key: 'driver', label: '기사', type: 'muted' },
        { key: 'cap', label: '정원', type: 'number', suffix: '석' },
        { key: 'fuel', label: '연비 기준', type: 'muted' },
        { key: 'st', label: '상태', type: 'status' }
      ],
      rows: list.map((x) => ({ id: x.id, name: { primary: x.name, secondary: x.sub }, lang: x.lang, days: x.days, claims: x.claims, driver: x.driver, cap: x.cap, fuel: x.fuel, st: x.state === 'off' ? { tone: 'neutral', form: 'dashed', status: x.stText } : x.state === 'busy' ? { tone: 'progress', status: x.stText } : { tone: 'neutral', status: x.stText }, selected: x.id === cur.id })),
      pick: (row) => set({ selected: row.id, offError: '' }),
      cur: { ...cur, tone: cur.state === 'busy' ? 'progress' : 'neutral', form: cur.state === 'off' ? 'dashed' : 'solid', stLabel: cur.stText, offTitle: isG ? '배정 불가일' : '정비·운행 불가일', addTitle: isG ? '배정 불가일 등록' : '정비 일정 등록', noOffs: !cur.offs.length },
      reasonOptions: isG ? ['연차', '개인 일정', '교육', '건강'] : ['정기 정비', '수리', '검사'],
      off,
      onOff: { from: (e) => set({ off: { ...s.off, from: e.target.value }, offError: '' }), to: (e) => set({ off: { ...s.off, to: e.target.value }, offError: '' }), why: (e) => set({ off: { ...s.off, why: e.target.value } }) },
      offError: s.offError || '',
      addOff: () => {
        if (!off.from || !off.to || off.to < off.from) { set({ offError: '끝 날짜가 시작보다 빠릅니다.' }); return; }
        const clash = (cur.jobs || []).find((j) => !(off.to < j.from || off.from > j.to));
        const range = `${lab(off.from)} – ${lab(off.to)}`;
        const next = { ...OFFS, [cur.id]: (OFFS[cur.id] || []).concat([{ from: off.from, to: off.to, why: off.why + (clash ? ' · 배정과 겹침' : '') }]) };
        share('offs', next, 'localOffs');
        set({ notice: clash ? { tone: 'critical', title: `${cur.name} · ${range} 불가일이 배정과 겹칩니다`, body: `${clash.code}(${lab(clash.from)}–${lab(clash.to)})에 이미 배정돼 있습니다. 배정 캘린더에 충돌로 표시되니 교체하세요.`, action: { label: '배정 캘린더', href: 'Schedule.dc.html' } } : { tone: 'positive', title: `${cur.name} · ${range} ${off.why} 등록`, body: '배정 캘린더에 회색 막대로 표시되고, 이 기간에는 배정 후보에서 빠집니다.', action: { label: '배정 캘린더', href: 'Schedule.dc.html' } } });
      },'''
state = '''{ kind: '가이드', selected: 'g1', adding: false, offError: '', gErr: {}, vErr: {}, notice: null, off: { from: '2026-10-08', to: '2026-10-09', why: '연차' },
      localGuides: [], localVehicles: [], localOffs: {},
      gf: { name: '', phone: '', lang: '한국어', spec: '고비·사막', contract: '프리랜서', rate: '200000', grade: 'C', invite: true },
      vf: { type: '푸르공(UAZ-452)', name: '', plate: '', cap: '8', driver: '', phone: '', owner: '고비모터스', insurance: '' },
      guides: [
        { id: 'g1', name: '바트-에르덴', sub: '한국어 · 고비 전문 · 7년', lang: '한국어·몽골어', days: 12, claims: 0, state: 'busy', stText: '행사 중 10.02–10.07', jobs: [ { code: 'MN2610-002', from: '2026-10-02', to: '2026-10-07' } ], facts: [ { k: '연락처', v: '+976 9911-4527 · 카카오톡 연결' }, { k: '등급', v: 'A · 고비·사막 리드' }, { k: '역량', v: '응급처치 자격(2025) · 4WD 운전' }, { k: '9월 실적', v: '행사 4건 · 22일 · 클레임 0' }, { k: '정산', v: '가이드비 일 220,000 MNT · 수당 별도' } ], offs: [ { range: '10.20 – 10.22', why: '개인 일정' } ] },
        { id: 'g2', name: '오윤치메그', sub: '한국어 · 골프 · 5년', lang: '한국어·영어', days: 9, claims: 0, state: 'busy', stText: '일정 충돌 10.03', jobs: [ { code: 'MN2609-040', from: '2026-09-30', to: '2026-10-03' }, { code: 'MN2610-005', from: '2026-10-03', to: '2026-10-06' } ], facts: [ { k: '연락처', v: '+976 9900-3312' }, { k: '등급', v: 'A · 골프 운영' }, { k: '역량', v: '골프 룰 교육 이수' }, { k: '9월 실적', v: '행사 5건 · 18일' }, { k: '정산', v: '가이드비 일 200,000 MNT' } ], offs: [] },
        { id: 'g3', name: '간바타르', sub: '한국어·영어 · 6년', lang: '한국어·영어·몽골어', days: 8, claims: 1, state: 'busy', stText: '행사 중 · 오늘 출국', jobs: [ { code: 'MN2610-012', from: '2026-10-08', to: '2026-10-12' } ], facts: [ { k: '연락처', v: '+976 8800-7741' }, { k: '등급', v: 'A · 대형 단체' }, { k: '역량', v: '영어 통역 · 인센티브 진행' }, { k: '9월 실적', v: '행사 5건 · 20일 · 클레임 1' }, { k: '확인 필요', v: '증빙 누락 2건 · 완료 보고 지연' } ], offs: [ { range: '10.02 – 10.03', why: '휴무' } ] },
        { id: 'g4', name: '사롤', sub: '한국어 · 신입 · 1년', lang: '한국어', days: 4, claims: 0, state: 'free', stText: '배정 가능', jobs: [ { code: 'MN2610-014', from: '2026-10-10', to: '2026-10-13' } ], facts: [ { k: '연락처', v: '+976 9455-0193' }, { k: '등급', v: 'C · 수습' }, { k: '교육', v: '안전 교육 이수(09.18) · 브리핑 확인률 100%' }, { k: '9월 실적', v: '행사 2건 · 9일' } ], offs: [] },
        { id: 'g5', name: '뭉흐-오치르', sub: '한국어 · 홉스골 전문 · 9년', lang: '한국어·러시아어', days: 7, claims: 0, state: 'off', stText: '휴무 10.01–10.05', jobs: [ { code: 'MN2610-021', from: '2026-10-18', to: '2026-10-24' } ], facts: [ { k: '연락처', v: '+976 9988-2201' }, { k: '등급', v: 'A · 홉스골 리드' }, { k: '역량', v: '보트 운항 보조 · 승마' } ], offs: [ { range: '10.01 – 10.05', why: '연차' } ] },
        { id: 'g6', name: '에르덴체첵', sub: '한국어·일본어 · 4년', lang: '한국어·일본어', days: 4, claims: 0, state: 'free', stText: '배정 가능', jobs: [ { code: 'MN2610-019', from: '2026-10-16', to: '2026-10-19' } ], facts: [ { k: '연락처', v: '+976 9191-0277' }, { k: '등급', v: 'B · 골프' }, { k: '역량', v: '일본어 통역' } ], offs: [] },
        { id: 'g7', name: '토야', sub: '한국어 · 신입 · 1년', lang: '한국어', days: 0, claims: 0, state: 'free', stText: '배정 가능', jobs: [], facts: [ { k: '연락처', v: '+976 8611-3092' }, { k: '등급', v: 'C · 수습' }, { k: '교육', v: '안전 교육 10.06–10.07 예정' } ], offs: [ { range: '10.06 – 10.07', why: '안전 교육' } ] },
        { id: 'g8', name: '체렌돌람', sub: '한국어 · 고비 · 3년', lang: '한국어', days: 0, claims: 0, state: 'free', stText: '배정 가능', jobs: [], facts: [ { k: '연락처', v: '+976 8855-6620' }, { k: '등급', v: 'B' }, { k: '역량', v: '사막 트레킹' } ], offs: [] }
      ],
      vehicles: [
        { id: 'v1', name: '푸르공 1호차', sub: 'UAZ-452 · 21-45 УБА', driver: '강톨가', cap: 8, fuel: '18 L/100km', state: 'busy', stText: '운행 중 10.02–10.07', jobs: [ { code: 'MN2610-002', from: '2026-10-02', to: '2026-10-07' } ], facts: [ { k: '차량번호', v: '21-45 УБА' }, { k: '기사', v: '강톨가 · +976 8800-1123' }, { k: '소속', v: '고비모터스' }, { k: '보험', v: '2027.03까지 · 승객 배상' } ], offs: [] },
        { id: 'v2', name: '푸르공 2호차', sub: 'UAZ-452 · 21-46 УБА', driver: '도르지', cap: 8, fuel: '18 L/100km', state: 'busy', stText: '운행 중 10.02–10.07', jobs: [ { code: 'MN2610-002', from: '2026-10-02', to: '2026-10-07' } ], facts: [ { k: '차량번호', v: '21-46 УБА' }, { k: '기사', v: '도르지 · +976 8800-2245' }, { k: '소속', v: '고비모터스' } ], offs: [] },
        { id: 'v3', name: '푸르공 3호차', sub: 'UAZ-452 · 21-47 УБА', driver: '바야르', cap: 8, fuel: '18 L/100km', state: 'busy', stText: '반복 클레임 2건', jobs: [ { code: 'MN2610-002', from: '2026-10-02', to: '2026-10-07' } ], facts: [ { k: '차량번호', v: '21-47 УБА' }, { k: '기사', v: '바야르 · +976 8800-3390' }, { k: '확인 필요', v: '90일 클레임 2건(엔진 과열·에어컨) · 정비 이력 요청' } ], offs: [ { range: '10.08 – 10.09', why: '정기 정비' } ] },
        { id: 'v4', name: '랜드크루저 1호', sub: '랜드크루저 200 · 19-02 УНА', driver: '아마르', cap: 6, fuel: '14 L/100km', state: 'busy', stText: '운행 중 10.03–10.06', jobs: [ { code: 'MN2610-005', from: '2026-10-03', to: '2026-10-06' } ], facts: [ { k: '차량번호', v: '19-02 УНА' }, { k: '기사', v: '아마르 · +976 9900-7781' }, { k: '소속', v: '고비모터스' } ], offs: [] },
        { id: 'v5', name: '랜드크루저 2호', sub: '랜드크루저 200 · 19-03 УНА', driver: '수흐바타르', cap: 6, fuel: '14 L/100km', state: 'busy', stText: '운행 중 10.03–10.06', jobs: [ { code: 'MN2610-005', from: '2026-10-03', to: '2026-10-06' } ], facts: [ { k: '차량번호', v: '19-03 УНА' }, { k: '기사', v: '수흐바타르 · +976 9900-7782' }, { k: '소속', v: '고비모터스' } ], offs: [] },
        { id: 'v6', name: '스타렉스', sub: '현대 스타렉스 · 33-12 УНЕ', driver: '바타', cap: 11, fuel: '11 L/100km', state: 'busy', stText: '에어컨 수리 필요', jobs: [ { code: 'MN2609-040', from: '2026-09-30', to: '2026-10-03' } ], facts: [ { k: '차량번호', v: '33-12 УНЕ' }, { k: '기사', v: '바타 · +976 9111-0457' }, { k: '확인 필요', v: 'CL2610-001 에어컨 고장 · 수리 일정 확인 중' } ], offs: [] },
        { id: 'v7', name: '25인승 버스', sub: '대우 BS106 · 15-88 УБЕ', driver: '바트볼드', cap: 25, fuel: '27 L/100km', state: 'free', stText: '정원 초과 배정 1건', jobs: [ { code: 'MN2610-012', from: '2026-10-08', to: '2026-10-12' } ], facts: [ { k: '차량번호', v: '15-88 УБЕ' }, { k: '기사', v: '바트볼드 · +976 9922-1810' } ], offs: [] },
        { id: 'v8', name: '45인승 버스', sub: '유니버스 · 15-90 УБЕ', driver: '냠도르지', cap: 45, fuel: '30 L/100km', state: 'free', stText: '배정 가능', jobs: [], facts: [ { k: '차량번호', v: '15-90 УБЕ' }, { k: '기사', v: '냠도르지 · +976 9922-1844' } ], offs: [ { range: '10.13 – 10.14', why: '정기 정비' } ] }
      ] }'''
admin('Resources.dc.html', '가이드·차량', 'resources', 'ops', body, pre=pre, vals=vals, state=state, height=1080)
print('Resources written')


# ------------------------------------------------------------------ Manuals (매뉴얼) — write, edit, review, publish
body = header('매뉴얼', '공통 문화·장소별·상품별·여행사별 매뉴얼과 가이드 인수인계 · 작성 → 검토 → 게시 · 게시되면 연결된 행사의 가이드 브리핑에 붙습니다', '''<div style="width: 220px"><x-import component-from-global-scope="Abt.TextField" size="sm" placeholder="제목·태그 검색" aria-label="매뉴얼 검색" value="{{q}}" on-change="{{setQ}}"></x-import></div>
<x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{newManual}}" disabled="{{editing}}">새 매뉴얼 작성</x-import>''')
body += NOTICE
body += '''<sc-if value="{{editing}}" hint-placeholder-val="{{false}}">
<div style="display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(340px, 1fr); gap: 16px; align-items: start">
''' + PANEL + '''<div style="display: flex; align-items: center; justify-content: space-between; gap: 12px"><h2 class="title-2" style="margin: 0">{{ed.heading}}</h2><span class="caption" style="color: var(--ink-muted)">{{ed.verText}}</span></div>
<x-import component-from-global-scope="Abt.TextField" label="제목" required="{{yes}}" placeholder="예: 테를지 리버 캠프" value="{{ed.title}}" on-change="{{onEd.title}}" error="{{edErr.title}}"></x-import>
''' + field_grid(180) + '''
<x-import component-from-global-scope="Abt.Select" label="구분" options="{{catOptions}}" value="{{ed.cat}}" on-change="{{onEd.cat}}"></x-import>
<x-import component-from-global-scope="Abt.Select" label="연결 대상" options="{{linkOptions}}" value="{{ed.link}}" on-change="{{onEd.link}}" help="연결된 행사의 브리핑에 자동으로 붙습니다"></x-import>
</div>
<x-import component-from-global-scope="Abt.TextField" label="태그" placeholder="쉼표로 구분 · 예: 고비, 숙소, 온수" value="{{ed.tags}}" on-change="{{onEd.tags}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="항상 보이는 핵심 주의사항" multiline="{{yes}}" rows="{{three}}" placeholder="한 줄에 하나씩 · 안전·알레르기처럼 요약과 상관없이 맨 위에 고정할 내용" value="{{ed.pins}}" on-change="{{onEd.pins}}"></x-import>
<div style="display: flex; flex-direction: column; gap: 10px">
<div style="display: flex; align-items: center; justify-content: space-between"><span class="label" style="color: var(--ink-muted)">본문</span><x-import component-from-global-scope="Abt.Button" size="sm" on-click="{{addSection}}">섹션 추가</x-import></div>
<sc-for list="{{edSections}}" as="x" hint-placeholder-count="2">
<div style="display: flex; flex-direction: column; gap: 8px; padding: 12px; border: 1px solid var(--line); border-radius: 6px">
<div style="display: grid; grid-template-columns: minmax(0, 1fr) auto; align-items: end; gap: 8px">
<x-import component-from-global-scope="Abt.TextField" label="{{x.label}}" size="sm" placeholder="소제목 · 예: 이동·화장실" value="{{x.h}}" on-change="{{x.onH}}"></x-import>
<x-import component-from-global-scope="Abt.Button" size="sm" variant="ghost" on-click="{{x.remove}}">삭제</x-import>
</div>
<x-import component-from-global-scope="Abt.TextField" aria-label="{{x.bodyLabel}}" multiline="{{yes}}" rows="{{three}}" placeholder="가이드가 현장에서 바로 따라 할 수 있게 적습니다" value="{{x.b}}" on-change="{{x.onB}}"></x-import>
</div>
</sc-for>
<sc-if value="{{edErr.body}}" hint-placeholder-val="{{false}}"><p class="caption" style="margin: 0; color: var(--critical)">{{edErr.body}}</p></sc-if>
</div>
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px">
<sc-for list="{{edPhotos}}" as="p" hint-placeholder-count="1"><x-import component-from-global-scope="Abt.Attachment" kind="photo" name="{{p}}" meta="방금 추가"></x-import></sc-for>
<x-import component-from-global-scope="Abt.Button" size="sm" on-click="{{addPhoto}}">사진 추가</x-import>
</div>
<sc-if value="{{privacyWarn}}" hint-placeholder-val="{{false}}"><x-import component-from-global-scope="Abt.Alert" tone="attention" title="개인 정보로 보이는 내용이 있습니다">{{privacyWarnText}}</x-import></sc-if>
<x-import component-from-global-scope="Abt.Checkbox" label="고객 이름·연락처·건강 정보 같은 개인 정보를 넣지 않았습니다" description="행사별 고객 특이사항은 행사 브리핑에만 두고, 매뉴얼에는 옮기지 않습니다" checked="{{ed.privacy}}" on-change="{{onEd.privacy}}"></x-import>
<sc-if value="{{edErr.privacy}}" hint-placeholder-val="{{false}}"><p class="caption" style="margin: 0; color: var(--critical)">{{edErr.privacy}}</p></sc-if>
<div style="display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 8px; padding-top: 4px">
<x-import component-from-global-scope="Abt.Button" variant="ghost" on-click="{{cancelEdit}}">취소</x-import>
<x-import component-from-global-scope="Abt.Button" on-click="{{saveDraft}}">임시저장</x-import>
<x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{requestReview}}">저장하고 검토 요청</x-import>
</div>
</section>
<section style="position: sticky; top: 16px; display: flex; flex-direction: column; gap: 12px; padding: 20px; background: var(--surface-sunken); border: 1px solid var(--line); border-radius: 6px">
<span class="label" style="color: var(--ink-muted)">가이드 앱에서 보이는 모습</span>
<h3 class="title-3" style="margin: 0">{{pv.title}}</h3>
<span class="caption" style="color: var(--ink-muted)">{{pv.meta}}</span>
<sc-if value="{{pv.hasPins}}" hint-placeholder-val="{{true}}">
<div style="display: flex; flex-direction: column; gap: 6px; padding: 12px 14px; border: 1px solid var(--attention); border-radius: 6px; background: var(--attention-soft)">
<span class="label" style="color: var(--attention)">꼭 지킬 것</span>
<sc-for list="{{pv.pins}}" as="p" hint-placeholder-count="2"><span style="font-size: 13px; line-height: 20px">{{p}}</span></sc-for>
</div>
</sc-if>
<sc-for list="{{pv.sections}}" as="x" hint-placeholder-count="2">
<div style="display: flex; flex-direction: column; gap: 4px"><span class="body-strong" style="font-size: 13px">{{x.h}}</span><span class="body" style="font-size: 13px; line-height: 20px; color: var(--ink-muted); white-space: pre-line">{{x.b}}</span></div>
</sc-for>
<span class="caption" style="color: var(--ink-muted)">{{pv.tags}}</span>
</section>
</div>
</sc-if>

<sc-if value="{{notEditing}}" hint-placeholder-val="{{true}}">
<x-import component-from-global-scope="Abt.Tabs" items="{{tabs}}" value="{{cat}}" on-change="{{setCat}}" aria-label="매뉴얼 구분"></x-import>
''' + TWO_PANE + '''
<x-import component-from-global-scope="Abt.DataTable" columns="{{cols}}" rows="{{rows}}" on-row-click="{{pick}}" caption="매뉴얼 목록" empty="찾는 매뉴얼이 없습니다."></x-import>
''' + SIDE_PANEL + '''<div style="display: flex; flex-direction: column; gap: 6px">
<div style="display: flex; align-items: center; justify-content: space-between; gap: 8px"><span class="caption" style="color: var(--ink-muted)">{{cur.id}} · {{cur.cat}} · v{{cur.ver}}</span><x-import component-from-global-scope="Abt.StatusBadge" tone="{{cur.tone}}" form="{{cur.form}}" size="md">{{cur.stLabel}}</x-import></div>
<h2 class="title-2" style="margin: 0">{{cur.title}}</h2>
<span class="caption" style="color: var(--ink-muted)">작성 {{cur.author}} · 검토 {{cur.reviewer}} · 최종 수정 {{cur.updated}} · 연결: {{cur.link}}</span>
</div>
<sc-if value="{{cur.hasPins}}" hint-placeholder-val="{{true}}">
<div style="display: flex; flex-direction: column; gap: 6px; padding: 12px 14px; border: 1px solid var(--attention); border-radius: 6px; background: var(--attention-soft)">
<span class="label" style="color: var(--attention)">항상 보이는 핵심 주의사항</span>
<sc-for list="{{cur.pins}}" as="p" hint-placeholder-count="2"><span style="font-size: 13px; line-height: 20px; color: var(--ink)">{{p}}</span></sc-for>
</div>
</sc-if>
<sc-for list="{{cur.sections}}" as="x" hint-placeholder-count="2">
<div style="display: flex; flex-direction: column; gap: 4px"><span class="body-strong" style="font-size: 13px">{{x.h}}</span><span class="body" style="font-size: 13px; line-height: 20px; color: var(--ink-muted); white-space: pre-line">{{x.b}}</span></div>
</sc-for>
<sc-if value="{{cur.hasChange}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.Alert" tone="progress" title="{{cur.changeTitle}}">{{cur.changeBody}}</x-import>
</sc-if>
<div style="display: flex; flex-direction: column">
<div style="display: flex; justify-content: space-between; gap: 8px; padding-bottom: 4px"><span class="label" style="color: var(--ink-muted)">가이드 확인</span><span class="caption" style="color: var(--ink-muted)">{{cur.ackText}}</span></div>
<div style="display: flex; flex-wrap: wrap; gap: 6px">
<sc-for list="{{cur.acks}}" as="a" hint-placeholder-count="8"><x-import component-from-global-scope="Abt.StatusBadge" tone="{{a.tone}}" form="{{a.form}}">{{a.name}}</x-import></sc-for>
</div>
</div>
<div style="display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 8px">
<sc-if value="{{cur.canRemind}}" hint-placeholder-val="{{true}}"><x-import component-from-global-scope="Abt.Button" size="sm" on-click="{{remind}}">미확인 가이드에게 알림</x-import></sc-if>
<sc-if value="{{cur.canEdit}}" hint-placeholder-val="{{true}}"><x-import component-from-global-scope="Abt.Button" size="sm" on-click="{{editCur}}">수정</x-import></sc-if>
<sc-if value="{{cur.canSendBack}}" hint-placeholder-val="{{false}}"><x-import component-from-global-scope="Abt.Button" size="sm" on-click="{{sendBack}}">작성자에게 돌려보내기</x-import></sc-if>
<x-import component-from-global-scope="Abt.Button" size="sm" variant="primary" on-click="{{next}}">{{cur.nextLabel}}</x-import>
</div>
</section>
</div>
</sc-if>
'''
pre = '''
    const BASE = ''' + MANUALS_BASE_JS + ''';
    const M = (() => { const v = store.get('manuals', null); return v == null ? (s.localManuals || BASE) : v; })();
    const saveAll = (list, extra) => { store.put('manuals', list); this.setState({ localManuals: list, ...(extra || {}) }); };
    const GUIDES = ['바트-에르덴', '오윤치메그', '간바타르', '사롤', '뭉흐-오치르', '에르덴체첵', '토야', '체렌돌람'];
    const cat = s.cat;
    const q = (s.q || '').trim();
    const list = M.filter((m) => (cat === '전체' || m.cat === cat) && (!q || m.title.includes(q) || m.tags.some((t) => t.includes(q))));
    const cur = M.find((m) => m.id === s.selected) || M[0];
    const ST = { draft: ['작성 중', 'neutral', 'dashed'], review: ['검토 중', 'progress', 'dashed'], published: ['게시', 'positive', 'solid'] };
    const NEXT = { draft: '검토 요청', review: '게시', published: '새 버전 작성' };
    const count = (c) => (c === '전체' ? M.length : M.filter((m) => m.cat === c).length);
    const where = (l) => (l === '모든 행사' ? '모든 행사의 가이드 브리핑' : `「${l}」 연결 행사의 가이드 브리핑`);
    const LINKOPTS = { '공통 문화': ['모든 행사'], '장소별': ['고비 오아시스 캠프', '홉스골 호숫가 게르 캠프', '테를지 리버 캠프', '국립박물관', '칭기즈칸 국제공항'], '상품별': ['고비 사막 5박 6일', '테를지 골프 3박 4일', '홉스골 호수 6박 7일', '울란바토르 시티 3박 4일', '기업 인센티브 4박 5일', '테를지 승마·게르 2박 3일'], '여행사별': ['푸른하늘여행', '한빛투어', '다온여행사', '누리투어', '제이원트래블', '솔빛여행'], '인수인계': ['고비 사막 5박 6일', '테를지 골프 3박 4일', '홉스골 호수 6박 7일', '울란바토르 시티 3박 4일', '기업 인센티브 4박 5일', '테를지 승마·게르 2박 3일'] };
    const ed = s.edit;
    const toEdit = (m, bump) => ({ id: m ? m.id : null, title: m ? m.title : '', cat: m ? m.cat : (cat === '전체' ? '장소별' : cat), link: m ? m.link : LINKOPTS[cat === '전체' ? '장소별' : cat][0], tags: m ? m.tags.join(', ') : '', pins: m ? m.pins.join('\\n') : '', sections: m ? m.sections.map((x) => ({ ...x })) : [ { h: '', b: '' } ], photos: m ? (m.photos || []).slice() : [], privacy: false, ver: m ? m.ver + (bump ? 1 : 0) : 1, bump: !!bump });
    const updEd = (patch) => set({ edit: { ...s.edit, ...patch }, edErr: {} });
    const allText = ed ? [ed.title, ed.pins, ed.tags].concat(ed.sections.map((x) => x.h + ' ' + x.b)).join(' ') : '';
    const phoneLike = /(\\+?\\d{2,4}[- ]\\d{3,4}[- ]\\d{4})|010-?\\d{3,4}/.test(allText);
    const nameLike = /[가-힣]○○|고객 [가-힣]{2,3}님/.test(allText);
    const build = (status) => {
      const pins = ed.pins.split('\\n').map((x) => x.trim()).filter(Boolean);
      const sections = ed.sections.filter((x) => x.h.trim() || x.b.trim()).map((x) => ({ h: x.h.trim() || '내용', b: x.b.trim() }));
      const tags = ed.tags.split(',').map((x) => x.trim()).filter(Boolean);
      const prev = ed.id ? M.find((m) => m.id === ed.id) : null;
      const live = prev ? (prev.status === 'published' ? { ver: prev.ver, title: prev.title, pins: prev.pins, sections: prev.sections, updated: prev.updated } : prev.live || null) : null;
      const id = ed.id || 'MA-0' + (60 + M.length);
      const m = { ...(prev || { acked: [], reviewer: '—', author: '김지훈' }), id, title: ed.title.trim(), cat: ed.cat, link: ed.link, tags, pins, sections, photos: ed.photos, ver: ed.ver, status, updated: '10.02', live, change: status === 'review' ? { title: '검토 요청됨', body: `${ed.bump ? `v${ed.ver} 새 버전 · ` : ''}운영관리자가 검토한 뒤 게시합니다. 게시되면 ${where(ed.link)}에 붙습니다.` } : { title: `v${ed.ver} 작성 중`, body: prev && prev.status === 'published' ? `게시 전까지 가이드에게는 v${prev.ver}이 계속 보입니다.` : '임시저장했습니다. 아직 가이드에게 보이지 않습니다.' } };
      return { m, isNew: !ed.id };
    };
    const validate = (forReview) => {
      const er = {};
      if (!ed.title.trim()) er.title = '제목을 입력하세요.';
      if (forReview && !ed.sections.some((x) => x.b.trim())) er.body = '본문을 한 섹션 이상 적어 주세요.';
      if (forReview && !ed.privacy) er.privacy = '개인 정보가 없는지 확인하고 체크해야 검토를 요청할 수 있습니다.';
      return er;
    };
'''
vals = '''      q: s.q,
      setQ: (e) => set({ q: e.target.value }),
      editing: !!ed,
      notEditing: !ed,
      tabs: ['전체', '공통 문화', '장소별', '상품별', '여행사별', '인수인계'].map((c) => ({ id: c, label: c, count: count(c) })),
      cat,
      setCat: (id) => set({ cat: id }),
      cols: [
        { key: 'title', label: '제목 / 태그', type: 'stack' },
        { key: 'cat', label: '구분', type: 'muted' },
        { key: 'ver', label: '버전', type: 'muted' },
        { key: 'ack', label: '확인', type: 'muted' },
        { key: 'st', label: '상태', type: 'status' }
      ],
      rows: list.map((m) => ({ id: m.id, title: { primary: m.title, secondary: m.tags.length ? m.tags.map((t) => '#' + t).join(' ') : '태그 없음' }, cat: m.cat, ver: m.live ? `v${m.ver} · 게시 v${m.live.ver}` : `v${m.ver}`, ack: m.status === 'published' ? `${m.acked.length}/8` : '—', st: { tone: ST[m.status][1], form: ST[m.status][2], status: ST[m.status][0] }, selected: m.id === cur.id })),
      pick: (row) => set({ selected: row.id }),
      cur: { ...cur, hasPins: cur.pins.length > 0, stLabel: ST[cur.status][0], tone: ST[cur.status][1], form: ST[cur.status][2], nextLabel: NEXT[cur.status], canRemind: cur.status === 'published' && cur.acked.length < 8, canEdit: cur.status !== 'published', canSendBack: cur.status === 'review', ackText: cur.status === 'published' ? `${cur.acked.length}/8명 확인 · 중요 변경은 재확인 대상` : cur.acked.length ? `이전 버전 확인 ${cur.acked.length}/8 · 게시하면 다시 받습니다` : '게시 후 확인을 받습니다', acks: GUIDES.map((g) => ({ name: g, tone: cur.acked.includes(g) ? 'positive' : 'neutral', form: cur.acked.includes(g) ? 'solid' : 'dashed' })), hasChange: !!cur.change, changeTitle: cur.change ? cur.change.title : '', changeBody: cur.change ? cur.change.body : '' },
      remind: () => say('progress', `${cur.title} · 미확인 ${8 - cur.acked.length}명에게 알렸습니다`, '가이드 앱 알림으로 확인 요청이 갔습니다. 출발 전까지 확인하지 않으면 운영관리자에게 보고됩니다.'),
      editCur: () => set({ edit: toEdit(cur, false), edErr: {}, notice: null }),
      sendBack: () => saveAll(M.map((m) => (m.id === cur.id ? { ...m, status: 'draft', change: { title: '작성자에게 돌려보냈습니다', body: '검토 의견: 사진을 추가하고 대체 일정을 구체적으로 적어 주세요.' } } : m)), { notice: { tone: 'attention', title: `${cur.title} · 작성자에게 돌려보냈습니다`, body: '작성 중 상태로 돌아갔습니다. 고친 뒤 다시 검토를 요청합니다.' } }),
      next: () => {
        const st = cur.status;
        if (st === 'draft') { saveAll(M.map((m) => (m.id === cur.id ? { ...m, status: 'review', updated: '10.02', change: { title: '검토 요청됨', body: '운영관리자가 검토한 뒤 게시합니다. 고객 개인 정보가 들어가지 않았는지 함께 확인합니다.' } } : m)), { notice: { tone: 'progress', title: `${cur.title} · 검토를 요청했습니다`, body: '' } }); return; }
        if (st === 'review') { saveAll(M.map((m) => (m.id === cur.id ? { ...m, status: 'published', acked: [], reviewer: '김지훈', updated: '10.02', live: null, change: { title: `v${cur.ver} 게시 · 확인 받는 중`, body: `가이드 8명에게 확인 요청을 보냈습니다. ${where(cur.link)}에 자동으로 붙습니다.` } } : m)), { notice: { tone: 'positive', title: `${cur.title} · 게시했습니다`, body: '' } }); return; }
        set({ edit: toEdit(cur, true), edErr: {}, notice: null });
      },
      newManual: () => set({ edit: toEdit(null, false), edErr: {}, notice: null }),
      ed: ed ? { ...ed, heading: ed.id ? (ed.bump ? `새 버전 작성 · ${ed.title}` : `매뉴얼 수정 · ${ed.title}`) : '새 매뉴얼 작성', verText: ed.id ? `v${ed.ver}${ed.bump ? ' · 게시 전까지 이전 버전이 보입니다' : ''}` : 'v1 · 작성자 김지훈' } : {},
      catOptions: ['공통 문화', '장소별', '상품별', '여행사별', '인수인계'],
      linkOptions: ed ? LINKOPTS[ed.cat] : [],
      onEd: { title: (e) => updEd({ title: e.target.value }), cat: (e) => updEd({ cat: e.target.value, link: LINKOPTS[e.target.value][0] }), link: (e) => updEd({ link: e.target.value }), tags: (e) => updEd({ tags: e.target.value }), pins: (e) => updEd({ pins: e.target.value }), privacy: (e) => updEd({ privacy: e.target.checked }) },
      edErr: s.edErr || {},
      edSections: ed ? ed.sections.map((x, i) => ({ h: x.h, b: x.b, label: `섹션 ${i + 1} 소제목`, bodyLabel: `섹션 ${i + 1} 내용`, onH: (e) => updEd({ sections: s.edit.sections.map((y, j) => (j === i ? { ...y, h: e.target.value } : y)) }), onB: (e) => updEd({ sections: s.edit.sections.map((y, j) => (j === i ? { ...y, b: e.target.value } : y)) }), remove: () => updEd({ sections: s.edit.sections.length > 1 ? s.edit.sections.filter((_, j) => j !== i) : [ { h: '', b: '' } ] }) })) : [],
      addSection: () => updEd({ sections: s.edit.sections.concat([ { h: '', b: '' } ]) }),
      edPhotos: ed ? ed.photos : [],
      addPhoto: () => updEd({ photos: s.edit.photos.concat([`IMG_60${s.edit.photos.length + 11}.jpg`]) }),
      privacyWarn: !!ed && (phoneLike || nameLike),
      privacyWarnText: phoneLike ? '연락처처럼 보이는 숫자가 있습니다. 업체 대표번호가 아니라면 지워 주세요.' : '고객 이름으로 보이는 표현이 있습니다. 고객 특이사항은 행사 브리핑에만 둡니다.',
      pv: ed ? { title: ed.title || '제목 없음', meta: `${ed.cat} · ${ed.link}`, pins: ed.pins.split('\\n').map((x) => x.trim()).filter(Boolean), hasPins: ed.pins.trim().length > 0, sections: ed.sections.filter((x) => x.h.trim() || x.b.trim()).map((x) => ({ h: x.h.trim() || '내용', b: x.b })), tags: ed.tags.split(',').map((x) => x.trim()).filter(Boolean).map((t) => '#' + t).join(' ') } : { pins: [], sections: [] },
      cancelEdit: () => set({ edit: null, edErr: {} }),
      saveDraft: () => {
        const er = validate(false);
        if (Object.keys(er).length) { set({ edErr: er }); return; }
        const { m, isNew } = build('draft');
        const next = isNew ? [m].concat(M) : M.map((x) => (x.id === m.id ? m : x));
        saveAll(next, { edit: null, selected: m.id, cat: '전체', notice: { tone: 'progress', title: `${m.title} · 임시저장했습니다`, body: '작성 중 상태라 아직 가이드에게 보이지 않습니다. 다 쓰면 검토를 요청하세요.' } });
      },
      requestReview: () => {
        const er = validate(true);
        if (Object.keys(er).length) { set({ edErr: er }); return; }
        const { m, isNew } = build('review');
        const next = isNew ? [m].concat(M) : M.map((x) => (x.id === m.id ? m : x));
        saveAll(next, { edit: null, selected: m.id, cat: '전체', notice: { tone: 'positive', title: `${m.title} · 검토를 요청했습니다`, body: `운영관리자가 검토하고 게시하면 ${where(m.link)}에 붙습니다.` } });
      },'''
state = "{ cat: '전체', q: '', selected: 'MA-014', edit: null, edErr: {}, localManuals: null, notice: null }"
admin('Manuals.dc.html', '매뉴얼', 'manuals', 'ops', body, pre=pre, vals=vals, state=state, height=1180)
print('Manuals written')


# ------------------------------------------------------------------ Users (사용자·권한)
body = header('사용자·권한', '역할별 메뉴 권한(조회·등록·수정·승인·다운로드)과 데이터 범위 · 퇴사·계약 종료 시 바로 접근을 막습니다 · 관리자·회계 계정은 2단계 인증 필수', '''<x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{invite}}">사용자 초대</x-import>''')
body += NOTICE
body += '''<x-import component-from-global-scope="Abt.Tabs" items="{{tabs}}" value="{{tab}}" on-change="{{setTab}}" aria-label="사용자·권한"></x-import>
<sc-if value="{{isUsers}}" hint-placeholder-val="{{true}}">
''' + TWO_PANE + '''
<x-import component-from-global-scope="Abt.DataTable" columns="{{cols}}" rows="{{rows}}" on-row-click="{{pick}}" caption="사용자 목록"></x-import>
''' + SIDE_PANEL + '''<div style="display: flex; flex-direction: column; gap: 6px">
<div style="display: flex; align-items: center; justify-content: space-between; gap: 8px"><span class="caption" style="color: var(--ink-muted)">{{cur.email}}</span><x-import component-from-global-scope="Abt.StatusBadge" tone="{{cur.tone}}" form="{{cur.form}}" size="md">{{cur.stLabel}}</x-import></div>
<h2 class="title-2" style="margin: 0">{{cur.name}}</h2>
<span class="caption" style="color: var(--ink-muted)">{{cur.org}} · 최근 접속 {{cur.last}}</span>
</div>
<x-import component-from-global-scope="Abt.Select" label="역할" options="{{roleOptions}}" value="{{cur.role}}" on-change="{{changeRole}}" disabled="{{cur.blocked}}" help="{{cur.scope}}"></x-import>
''' + dl([('2단계 인증', '{{cur.mfa}}'), ('담당 범위', '{{cur.events}}')], 88) + '''<sc-if value="{{cur.hasWarn}}" hint-placeholder-val="{{false}}"><x-import component-from-global-scope="Abt.Alert" tone="attention" title="{{cur.warnTitle}}">{{cur.warnBody}}</x-import></sc-if>
<div style="display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 8px; padding-top: 12px; border-top: 1px solid var(--line)">
<sc-if value="{{cur.active}}" hint-placeholder-val="{{true}}">
<x-import component-from-global-scope="Abt.Button" size="sm" on-click="{{resetMfa}}">2단계 인증 초기화</x-import>
<x-import component-from-global-scope="Abt.Button" size="sm" on-click="{{lock}}">잠금</x-import>
<x-import component-from-global-scope="Abt.Button" size="sm" variant="danger" on-click="{{leave}}">퇴사·계약 종료</x-import>
</sc-if>
<sc-if value="{{cur.locked}}" hint-placeholder-val="{{false}}"><x-import component-from-global-scope="Abt.Button" size="sm" variant="primary" on-click="{{unlock}}">잠금 해제</x-import></sc-if>
</div>
</section>
</div>
</sc-if>
<sc-if value="{{isPerms}}" hint-placeholder-val="{{false}}">
''' + PANEL + '''<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px">
<div style="display: flex; align-items: center; gap: 12px"><span class="label" style="color: var(--ink-muted)">역할</span><x-import component-from-global-scope="Abt.Segmented" options="{{permRoles}}" value="{{permRole}}" on-change="{{setPermRole}}" aria-label="역할 선택"></x-import></div>
<div style="display: flex; align-items: center; gap: 8px"><span class="caption" style="color: var(--ink-muted)">{{dirtyText}}</span><x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{savePerms}}" disabled="{{clean}}">변경 저장</x-import></div>
</div>
<p class="caption" style="margin: 0; color: var(--ink-muted)">데이터 범위: {{scopeText}} · 화면 권한과 같은 규칙을 서버에서도 검사합니다</p>
<div role="table" aria-label="메뉴 권한" style="display: flex; flex-direction: column">
<div role="row" style="display: grid; grid-template-columns: minmax(0, 1.6fr) repeat(5, minmax(0, 1fr)); gap: 8px; padding: 8px 0; border-bottom: 1px solid var(--line-strong)">
<span role="columnheader" class="label" style="color: var(--ink-muted)">메뉴</span>
<sc-for list="{{actions}}" as="a" hint-placeholder-count="5"><span role="columnheader" class="label" style="color: var(--ink-muted); text-align: center">{{a}}</span></sc-for>
</div>
<sc-for list="{{matrix}}" as="r" hint-placeholder-count="12">
<div role="row" style="display: grid; grid-template-columns: minmax(0, 1.6fr) repeat(5, minmax(0, 1fr)); gap: 8px; align-items: center; padding: 6px 0; border-bottom: 1px solid var(--line)">
<span role="rowheader" style="font-size: 13px; line-height: 20px">{{r.menu}}</span>
<sc-for list="{{r.cells}}" as="c" hint-placeholder-count="5"><span role="cell" style="display: flex; justify-content: center"><input type="checkbox" aria-label="{{c.label}}" checked="{{c.on}}" disabled="{{c.fixed}}" onChange="{{c.toggle}}" style="width: 18px; height: 18px; accent-color: var(--ink)"></span></sc-for>
</div>
</sc-for>
</div>
<p class="caption" style="margin: 0; color: var(--ink-muted)">회색 칸은 고정 규칙입니다(예: 가이드는 회사 마진을 볼 수 없음, 입력자는 자기 비용을 최종 승인할 수 없음).</p>
</section>
</sc-if>
'''
pre = '''
    const U = s.users;
    const cur = U.find((u) => u.id === s.selected) || U[0];
    const ACTIONS = ['조회', '등록', '수정', '승인', '다운로드'];
    const MENUS = ['행사', '배정', '현장 보고', '클레임', '입금', '지상비·비용', '송금', '과입·차감', '정산·마감', '리포트', '기준정보', '사용자·권한'];
    const P = s.perms;
    const pr = s.permRole;
    const FIXED = { '가이드': ['정산·마감', '과입·차감', '입금', '송금', '사용자·권한', '리포트'], '외부 여행사': ['배정', '현장 보고', '지상비·비용', '송금', '과입·차감', '사용자·권한', '기준정보'] };
    const SCOPE = { '대표': '전체 행사·전체 금액', '운영관리자': '전체 운영 · 재무는 부여 범위만', '운영담당자': '담당 행사만 · 송금 완료와 정산 확정 제외', '회계담당자': '정산에 필요한 행사·재무 정보', '가이드': '본인 배정 행사·본인 지급 내역만', '외부 여행사': '자사 행사 중 공개 승인 항목만' };
    const STL = { active: ['사용 중', 'neutral', 'solid'], locked: ['잠김', 'attention', 'solid'], left: ['접근 차단', 'critical', 'solid'], invited: ['초대됨', 'neutral', 'dashed'] };
    const upd = (patch, notice) => this.setState({ users: U.map((u) => (u.id === cur.id ? { ...u, ...patch } : u)), notice });
'''
vals = '''      tabs: [ { id: 'users', label: '사용자', count: U.length }, { id: 'perms', label: '역할 권한' } ],
      tab: s.tab,
      setTab: (id) => set({ tab: id }),
      isUsers: s.tab === 'users',
      isPerms: s.tab === 'perms',
      cols: [
        { key: 'name', label: '사용자', type: 'stack' },
        { key: 'role', label: '역할', type: 'muted' },
        { key: 'org', label: '소속', type: 'muted' },
        { key: 'mfa', label: '2단계 인증', type: 'status' },
        { key: 'st', label: '상태', type: 'status' }
      ],
      rows: U.map((u) => ({ id: u.id, name: { primary: u.name, secondary: u.email }, role: u.role, org: u.org, mfa: u.mfa === '사용' ? { tone: 'neutral', status: '사용' } : u.mfa === '미설정' ? { tone: 'attention', status: '미설정' } : { tone: 'neutral', form: 'dashed', status: u.mfa }, st: { tone: STL[u.st][1], form: STL[u.st][2], status: STL[u.st][0] }, selected: u.id === cur.id, dim: u.st === 'left' })),
      pick: (row) => set({ selected: row.id }),
      roleOptions: ['대표', '운영관리자', '운영담당자', '회계담당자', '가이드', '외부 여행사'],
      cur: { ...cur, stLabel: STL[cur.st][0], tone: STL[cur.st][1], form: STL[cur.st][2], scope: `데이터 범위: ${SCOPE[cur.role]}`, active: cur.st === 'active' || cur.st === 'invited', locked: cur.st === 'locked', blocked: cur.st === 'left', hasWarn: !!cur.warn, warnTitle: cur.warn ? cur.warn.title : '', warnBody: cur.warn ? cur.warn.body : '' },
      changeRole: (e) => { const r = e.target.value; upd({ role: r, warn: ['대표', '운영관리자', '회계담당자'].includes(r) && cur.mfa !== '사용' ? { title: '2단계 인증이 필요합니다', body: `${r} 역할은 2단계 인증을 켜야 다음 로그인부터 쓸 수 있습니다.` } : cur.warn }, { tone: 'positive', title: `${cur.name} 역할을 ${r}(으)로 바꿨습니다`, body: `데이터 범위: ${SCOPE[r]} · 변경은 감사 로그에 남습니다.` }); },
      resetMfa: () => upd({ mfa: '재설정 대기' }, { tone: 'progress', title: `${cur.name} 2단계 인증을 초기화했습니다`, body: '다음 로그인 때 다시 등록합니다.' }),
      lock: () => upd({ st: 'locked' }, { tone: 'attention', title: `${cur.name} 계정을 잠갔습니다`, body: '열린 세션을 모두 끊었습니다. 잠금 해제 전까지 로그인할 수 없습니다.' }),
      unlock: () => upd({ st: 'active' }, { tone: 'positive', title: `${cur.name} 잠금을 풀었습니다`, body: '' }),
      leave: () => upd({ st: 'left', warn: { title: '담당 행사 인계 필요', body: cur.handover || '담당 중인 행사가 없습니다.' } }, { tone: 'critical', title: `${cur.name} 접근을 막았습니다`, body: '세션 종료 · 첨부 다운로드 링크 만료 · 담당 행사는 운영관리자에게 인계 요청이 갔습니다. 기록은 지워지지 않습니다.' }),
      invite: () => this.setState({ users: U.concat([{ id: 'u' + (U.length + 1), name: '새 사용자', email: 'invite@abt.example', role: '운영담당자', org: 'ABT 한국', mfa: '미설정', last: '—', st: 'invited', events: '담당 행사 없음' }]), selected: 'u' + (U.length + 1), tab: 'users', notice: { tone: 'progress', title: '초대 메일을 보냈습니다', body: '72시간 안에 비밀번호와 2단계 인증을 설정해야 합니다.' } }),
      permRoles: ['대표', '운영관리자', '운영담당자', '회계담당자', '가이드', '외부 여행사'],
      permRole: pr,
      setPermRole: (v) => set({ permRole: v }),
      actions: ACTIONS,
      scopeText: SCOPE[pr],
      matrix: MENUS.map((m) => ({ menu: m, cells: ACTIONS.map((a, i) => { const key = `${pr}|${m}|${a}`; const fixed = (FIXED[pr] || []).includes(m) || (pr === '대표' && m === '사용자·권한' && a === '조회'); const on = fixed ? false : !!P[key]; return { label: `${pr} ${m} ${a}`, on: fixed && pr === '대표' ? true : on, fixed, toggle: () => set({ perms: { ...P, [key]: !P[key] }, dirty: (s.dirty || 0) + 1 }) }; }) })),
      dirtyText: s.dirty ? `바뀐 칸 ${s.dirty}개 · 저장하면 다음 요청부터 적용` : '바뀐 칸 없음',
      clean: !s.dirty,
      savePerms: () => this.setState({ dirty: 0, notice: { tone: 'positive', title: `${pr} 권한을 저장했습니다`, body: '서버 권한 검사에도 바로 적용됩니다. 누가 무엇을 바꿨는지 감사 로그에 남았습니다.', action: { label: '감사 로그', href: 'Audit.dc.html' } } }),'''

# default permission map (true where allowed)
perm_default = {
    '대표': {m: ['조회', '등록', '수정', '승인', '다운로드'] for m in ['행사', '배정', '현장 보고', '클레임', '입금', '지상비·비용', '송금', '과입·차감', '정산·마감', '리포트', '기준정보', '사용자·권한']},
    '운영관리자': {'행사': ['조회', '등록', '수정', '승인', '다운로드'], '배정': ['조회', '등록', '수정', '승인'], '현장 보고': ['조회', '수정', '승인'], '클레임': ['조회', '등록', '수정', '승인'], '입금': ['조회'], '지상비·비용': ['조회', '등록', '승인'], '송금': ['조회', '승인'], '과입·차감': ['조회'], '정산·마감': ['조회'], '리포트': ['조회', '다운로드'], '기준정보': ['조회', '등록', '수정'], '사용자·권한': []},
    '운영담당자': {'행사': ['조회', '등록', '수정'], '배정': ['조회', '등록'], '현장 보고': ['조회'], '클레임': ['조회', '등록'], '지상비·비용': ['조회', '등록'], '리포트': ['조회'], '기준정보': ['조회']},
    '회계담당자': {'행사': ['조회'], '입금': ['조회', '등록', '수정', '다운로드'], '지상비·비용': ['조회', '승인', '다운로드'], '송금': ['조회', '등록', '수정', '다운로드'], '과입·차감': ['조회', '등록', '수정'], '정산·마감': ['조회', '등록', '수정', '다운로드'], '리포트': ['조회', '다운로드'], '기준정보': ['조회']},
    '가이드': {'행사': ['조회'], '배정': ['조회'], '현장 보고': ['조회', '등록'], '클레임': ['등록'], '지상비·비용': ['등록']},
    '외부 여행사': {'행사': ['조회'], '클레임': ['조회'], '입금': ['조회'], '정산·마감': [], '리포트': ['조회', '다운로드']},
}
pairs = []
for r, mm in perm_default.items():
    for m, acts in mm.items():
        for a in acts:
            pairs.append(f"'{r}|{m}|{a}': true")
perms_js = '{ ' + ', '.join(pairs) + ' }'

state = '''{ tab: 'users', selected: 'u4', permRole: '운영담당자', dirty: 0, notice: null, perms: ''' + perms_js + ''',
      users: [
        { id: 'u1', name: '이도윤', email: 'doyoon.lee@abt.example', role: '대표', org: 'ABT 한국', mfa: '사용', last: '10.01 09:02', st: 'active', events: '전체' },
        { id: 'u2', name: '김지훈', email: 'jihoon.kim@abt.example', role: '운영관리자', org: 'ABT 한국', mfa: '사용', last: '10.01 14:10', st: 'active', events: '전체 운영 · 담당 6건' },
        { id: 'u3', name: '정하린', email: 'harin.jung@abt.example', role: '운영관리자', org: 'ABT Mongolia', mfa: '사용', last: '10.01 13:55', st: 'active', events: '전체 운영 · 담당 4건' },
        { id: 'u4', name: '오세진', email: 'sejin.oh@abt.example', role: '운영담당자', org: 'ABT 한국', mfa: '미설정', last: '09.30 18:20', st: 'active', events: '담당 3건(MN2610-005·012·019)', warn: { title: '2단계 인증 미설정', body: '운영 계정도 10.15부터 2단계 인증이 필수입니다. 초대 메일을 다시 보낼 수 있습니다.' }, handover: 'MN2610-005·012·019 담당을 다른 운영담당자에게 넘겨야 합니다.' },
        { id: 'u5', name: '박서연', email: 'seoyeon.park@abt.example', role: '회계담당자', org: 'ABT 한국', mfa: '사용', last: '10.01 15:40', st: 'active', events: '정산에 필요한 범위' },
        { id: 'u6', name: '바트-에르덴', email: 'baterdene@abt.example', role: '가이드', org: 'ABT Mongolia', mfa: '휴대폰 인증', last: '10.01 07:30', st: 'active', events: '본인 배정 행사(MN2610-002)' },
        { id: 'u7', name: '최민정', email: 'mj.choi@bluesky-travel.example', role: '외부 여행사', org: '푸른하늘여행', mfa: '휴대폰 인증', last: '09.29 10:12', st: 'active', events: '자사 공개 항목만' },
        { id: 'u8', name: '김도현', email: 'dohyun.kim@abt.example', role: '운영담당자', org: 'ABT 한국', mfa: '사용', last: '09.14 18:00', st: 'left', events: '인계 완료(09.15)' }
      ] }'''
admin('Users.dc.html', '사용자·권한', 'users', 'ceo', body, pre=pre, vals=vals, state=state, height=1060)
print('Users written')


# ------------------------------------------------------------------ Audit (감사 로그)
body = header('감사 로그', '누가 언제 무엇을 바꾸고 승인했는지 · 변경 전후 값·사유·승인자 · 권한 밖 접근 시도와 다운로드도 남습니다 · 기록은 수정·삭제할 수 없습니다', '''<x-import component-from-global-scope="Abt.Button" variant="secondary" on-click="{{exportXls}}">내보내기</x-import>''')
body += NOTICE
body += '''<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px">
<x-import component-from-global-scope="Abt.Select" inline="{{yes}}" size="sm" label="기간" options="{{periodOptions}}" value="{{f.period}}" on-change="{{onF.period}}"></x-import>
<x-import component-from-global-scope="Abt.Select" inline="{{yes}}" size="sm" label="구분" options="{{kindOptions}}" value="{{f.kind}}" on-change="{{onF.kind}}"></x-import>
<x-import component-from-global-scope="Abt.Select" inline="{{yes}}" size="sm" label="사용자" options="{{userOptions}}" value="{{f.user}}" on-change="{{onF.user}}"></x-import>
<div style="width: 200px"><x-import component-from-global-scope="Abt.TextField" size="sm" placeholder="행사코드·문서번호" aria-label="검색" value="{{f.q}}" on-change="{{onF.q}}"></x-import></div>
<span class="caption" style="color: var(--ink-muted)">{{countText}}</span>
</div>
<section style="display: flex; flex-direction: column; padding: 4px 20px; background: var(--surface); border: 1px solid var(--line); border-radius: 6px">
<x-import component-from-global-scope="Abt.AuditLog" entries="{{entries}}"></x-import>
<sc-if value="{{empty}}" hint-placeholder-val="{{false}}"><p class="body" style="margin: 0; padding: 32px 0; text-align: center; color: var(--ink-muted)">조건에 맞는 기록이 없습니다.</p></sc-if>
</section>
'''
pre = '''
    const ALL = [
      { kind: '권한', at: '2026-10-01T15:02', zone: 'KST', actor: '간바타르', role: '가이드', action: '접근 차단', field: 'MN2609-031 정산 화면', before: '요청', after: '차단(권한 없음)', reason: '가이드는 회사 마진·정산을 볼 수 없음' },
      { kind: '금액', at: '2026-10-01T10:20', zone: 'KST', actor: '김지훈', role: '운영관리자', action: '송금 검토 완료', field: 'RM2610-003', before: '요청', after: '승인 대기 · 9,800,000 MNT', reason: '잔금 미입금 확인 · 선지급 동의' },
      { kind: '다운로드', at: '2026-10-01T09:48', zone: 'KST', actor: '박서연', role: '회계', action: '엑셀 내려받기', field: '9월 정산서', after: '권한 열 12개 · 워터마크' },
      { kind: '로그인', at: '2026-10-01T08:55', zone: 'KST', actor: '알 수 없음', role: '—', action: '로그인 실패 5회 · 계정 잠금', field: 'sejin.oh@abt.example', after: '15분 잠금', reason: 'IP 203.0.113.24' },
      { kind: '승인', at: '2026-09-29T11:00', zone: 'KST', actor: '이도윤', role: '대표', action: '비용 승인', field: 'CO-0926-03 보상·기타', before: '권한자 승인 대기', after: '승인 · 2,260,000 MNT' },
      { kind: '금액', at: '2026-09-28T10:42', zone: 'KST', actor: '박서연', role: '회계', action: '비용 검토 보류', field: 'CO-0924-11', before: '운영 확인', after: '회계 검토 중', reason: '중복 청구 후보 · 가이드에게 사실 확인 요청' },
      { kind: '금액', at: '2026-09-25T09:20', zone: 'KST', actor: '김지훈', role: '운영관리자', action: '예산 변경', field: 'MN2609-033 식사 예산', before: '7,800,000 MNT', after: '8,400,000 MNT', reason: '현지 식당 단가 인상(09.01 공지)', approver: '이도윤' },
      { kind: '권한', at: '2026-09-15T09:00', zone: 'KST', actor: '이도윤', role: '대표', action: '퇴사 처리 · 접근 차단', field: '김도현(운영담당자)', before: '사용 중', after: '접근 차단', reason: '퇴사 · 담당 행사 인계 완료' },
      { kind: '마감', at: '2026-09-12T16:40', zone: 'KST', actor: '이도윤', role: '대표', action: '8월 재개방 승인', field: '8월 정산', before: '마감', after: '재개방', reason: '한빛투어 과입금 1,200,000 KRW 상계 누락' },
      { kind: '승인', at: '2026-09-11T10:05', zone: 'KST', actor: '이도윤', role: '대표', action: '송금 반려', field: 'RM2609-016', before: '승인 대기', after: '반려 · 17,500,000 MNT', reason: '수취 계좌 확인서 누락' }
    ];
    const f = s.f;
    const q = (f.q || '').trim();
    const list = ALL.filter((e) => (f.kind === '전체' || e.kind === f.kind) && (f.user === '전체' || e.actor === f.user) && (f.period === '최근 30일' || e.at >= '2026-09-24') && (!q || (e.field + e.action).includes(q)));
    const onF = (k) => (e) => set({ f: { ...s.f, [k]: e.target.value } });
'''
vals = '''      user: { name: '이도윤', role: '대표' },
      periodOptions: ['최근 30일', '최근 7일'],
      kindOptions: ['전체', '금액', '승인', '마감', '권한', '로그인', '다운로드'],
      userOptions: ['전체', '이도윤', '김지훈', '박서연', '간바타르'],
      f,
      onF: { period: onF('period'), kind: onF('kind'), user: onF('user'), q: onF('q') },
      entries: list,
      empty: list.length === 0,
      countText: `${list.length}건 · 시각은 기록된 지역 기준(KST/ULAT)`,
      exportXls: () => say('positive', `감사 로그 ${list.length}건을 내보냈습니다`, '내보낸 사실도 감사 로그에 남습니다. 파일에는 열람자 이름이 워터마크로 들어갑니다.'),'''
state = "{ notice: null, f: { period: '최근 30일', kind: '전체', user: '전체', q: '' } }"
admin('Audit.dc.html', '감사 로그', 'audit', None, body, pre=pre, vals=vals, state=state, height=1100)
print('Audit written')
