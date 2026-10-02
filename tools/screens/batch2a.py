import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import *

# ------------------------------------------------------------------ EventNew (행사 등록)
SEC = '<section style="display: flex; flex-direction: column; gap: 16px; padding: 20px; background: var(--surface); border: 1px solid var(--line); border-radius: 6px">'

body = '<nav aria-label="경로" class="caption" style="display: flex; gap: 6px; color: var(--ink-muted)"><a href="Events.dc.html" style="color: var(--ink-muted)">행사</a><span aria-hidden="true">/</span><span style="color: var(--ink)">행사 등록</span></nav>\n'
body += header('행사 등록', '저장하면 행사코드가 부여되고 예약 상태로 시작합니다 · 금액은 원래 통화로 입력하고 환산액은 따로 저장합니다', '''<x-import component-from-global-scope="Abt.Button" variant="ghost" href="Events.dc.html">취소</x-import>
<x-import component-from-global-scope="Abt.Button" variant="secondary" on-click="{{saveDraft}}" disabled="{{saved}}">임시저장</x-import>
<x-import component-from-global-scope="Abt.Button" variant="primary" on-click="{{save}}" disabled="{{saved}}">{{saveLabel}}</x-import>''')
body += NOTICE
body += '''<div style="display: grid; grid-template-columns: minmax(0, 1fr) 360px; gap: 16px; align-items: start">
<div style="display: flex; flex-direction: column; gap: 16px; min-width: 0">
''' + SEC + panel_title('기본 정보') + field_grid() + '''
<x-import component-from-global-scope="Abt.Select" label="여행사" required="{{yes}}" options="{{agencyOptions}}" value="{{f.agency}}" on-change="{{on.agency}}" error="{{err.agency}}"></x-import>
<x-import component-from-global-scope="Abt.Select" label="상품" required="{{yes}}" options="{{productOptions}}" value="{{f.product}}" on-change="{{on.product}}" error="{{err.product}}" help="{{productHelp}}"></x-import>
<x-import component-from-global-scope="Abt.Select" label="담당자" required="{{yes}}" options="{{ownerOptions}}" value="{{f.owner}}" on-change="{{on.owner}}"></x-import>
</div>
</section>
''' + SEC + panel_title('기간·인원', '출국일은 상품 박수로 계산합니다') + field_grid(150) + '''
<x-import component-from-global-scope="Abt.TextField" label="입국일" type="date" required="{{yes}}" value="{{f.arrive}}" on-change="{{on.arrive}}" error="{{err.arrive}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="출국일" value="{{departLabel}}" read-only="{{yes}}" help="{{nightsHelp}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="여행객" required="{{yes}}" input-mode="numeric" align="end" suffix="명" value="{{f.pax}}" on-change="{{on.pax}}" error="{{err.pax}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="인솔자" input-mode="numeric" align="end" suffix="명" value="{{f.lead}}" on-change="{{on.lead}}"></x-import>
</div>
</section>
''' + SEC + panel_title('항공·픽업', '확정 전이면 비워 두고 나중에 입력해도 됩니다 · 시각은 현지(ULAT)') + field_grid(150) + '''
<x-import component-from-global-scope="Abt.TextField" label="입국편" placeholder="예: OM301" value="{{f.inFlight}}" on-change="{{on.inFlight}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="도착 시각" type="time" tag="ULAT" value="{{f.inTime}}" on-change="{{on.inTime}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="출국편" placeholder="예: OM302" value="{{f.outFlight}}" on-change="{{on.outFlight}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="출발 시각" type="time" tag="ULAT" value="{{f.outTime}}" on-change="{{on.outTime}}"></x-import>
</div>
<x-import component-from-global-scope="Abt.Select" label="픽업 장소" options="{{pickupOptions}}" value="{{f.pickup}}" on-change="{{on.pickup}}"></x-import>
</section>
''' + SEC + panel_title('판매 금액', '여행사에 청구할 금액입니다 · 실제 입금은 입금 화면에서 따로 기록합니다') + field_grid(200) + '''
<x-import component-from-global-scope="Abt.TextField" label="1인 판매가" required="{{yes}}" input-mode="numeric" align="end" suffix="KRW" value="{{f.price}}" on-change="{{on.price}}" error="{{err.price}}" help="{{priceHelp}}"></x-import>
<x-import component-from-global-scope="Abt.TextField" label="추가금·할인" input-mode="numeric" align="end" suffix="KRW" value="{{f.extra}}" on-change="{{on.extra}}" help="할인은 앞에 - 를 붙입니다"></x-import>
</div>
<x-import component-from-global-scope="Abt.Checkbox" label="인솔자는 과금하지 않음" description="{{leaderDesc}}" checked="{{f.leaderFree}}" on-change="{{on.leaderFree}}"></x-import>
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 12px">
<span class="label" style="color: var(--ink-muted)">계약금</span>
<x-import component-from-global-scope="Abt.Segmented" size="sm" options="{{depositOptions}}" value="{{f.deposit}}" on-change="{{on.deposit}}" aria-label="계약금 비율"></x-import>
<span class="caption" style="color: var(--ink-muted)">{{depositText}}</span>
</div>
</section>
''' + SEC + panel_title('요청사항') + '''<x-import component-from-global-scope="Abt.TextField" label="여행사 요청사항" multiline="{{yes}}" rows="{{three}}" value="{{f.memo}}" on-change="{{on.memo}}" help="고객 개인 특이사항(알레르기·이동 지원 등)은 저장 후 여행객 명단에 따로 입력합니다. 공통 매뉴얼에는 옮겨지지 않습니다."></x-import>
</section>
</div>

<aside style="position: sticky; top: 16px; display: flex; flex-direction: column; gap: 16px; padding: 20px; background: var(--surface); border: 1px solid var(--line); border-radius: 6px">
<div style="display: flex; flex-direction: column; gap: 6px">
<span class="label" style="color: var(--ink-muted)">행사코드</span>
<x-import component-from-global-scope="Abt.EventCode" code="{{code}}" size="md"></x-import>
<span class="caption" style="color: var(--ink-muted)">{{codeCaption}}</span>
</div>
''' + dl([('여행사', '{{sum.agency}}'), ('상품', '{{sum.product}}'), ('기간', '{{sum.period}}'), ('인원', '{{sum.people}}')], 64) + '''<div style="display: flex; flex-direction: column; gap: 12px; padding-top: 12px; border-top: 1px solid var(--line)">
<div style="display: flex; align-items: baseline; justify-content: space-between; gap: 8px"><span class="label" style="color: var(--ink-muted)">판매금액</span><x-import component-from-global-scope="Abt.Money" amount="{{sales}}" currency="KRW" kind="expected"></x-import></div>
<div style="display: flex; align-items: baseline; justify-content: space-between; gap: 8px"><span class="label" style="color: var(--ink-muted)">지상비 예산</span><x-import component-from-global-scope="Abt.Money" amount="{{cost}}" currency="MNT" kind="expected" converted="{{costConv}}"></x-import></div>
<p class="caption" style="margin: 0; color: var(--ink-muted)">{{costBasis}}</p>
<div style="display: flex; align-items: baseline; justify-content: space-between; gap: 8px; padding-top: 12px; border-top: 1px solid var(--line)"><span class="body-strong" style="font-size: 14px">예상 마진</span><x-import component-from-global-scope="Abt.Money" amount="{{margin}}" currency="KRW" kind="expected" loss-tone="{{yes}}" size="lg"></x-import></div>
<p class="caption" style="margin: 0; color: var(--ink-muted)">{{marginCaption}}</p>
</div>
<sc-if value="{{hasErrors}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.Alert" tone="critical" title="{{errorTitle}}">{{errorList}}</x-import>
</sc-if>
<sc-if value="{{saved}}" hint-placeholder-val="{{false}}">
<div style="display: flex; flex-direction: column; gap: 8px; padding-top: 12px; border-top: 1px solid var(--line)">
<span class="label" style="color: var(--ink-muted)">다음 단계</span>
<p class="caption" style="margin: 0; color: var(--ink-muted)">행사 목록 맨 위와 배정 캘린더 「미배정 행사」에 이 행사가 올라갔습니다.</p>
<x-import component-from-global-scope="Abt.Button" variant="primary" block="{{yes}}" href="Schedule.dc.html">가이드·차량 배정</x-import>
<x-import component-from-global-scope="Abt.Button" variant="secondary" block="{{yes}}" href="Events.dc.html">행사 목록에서 보기</x-import>
<x-import component-from-global-scope="Abt.Button" variant="ghost" block="{{yes}}" on-click="{{again}}">행사 하나 더 등록</x-import>
</div>
</sc-if>
</aside>
</div>
'''

pre = '''
    const R = 0.3985;
    const PRODUCTS = [
      { code: 'GOBI-56', name: '고비 사막 5박 6일', nights: 5, price: 1150000, per: 1800000, fixed: 9500000 },
      { code: 'TRJ-GOLF-34', name: '테를지 골프 3박 4일', nights: 3, price: 1600000, per: 2700000, fixed: 4200000 },
      { code: 'KHS-67', name: '홉스골 호수 6박 7일', nights: 6, price: 1350000, per: 2200000, fixed: 13400000 },
      { code: 'UB-CITY-34', name: '울란바토르 시티 3박 4일', nights: 3, price: 1100000, per: 1800000, fixed: 4500000 },
      { code: 'INC-45', name: '기업 인센티브 4박 5일', nights: 4, price: 1700000, per: 2900000, fixed: 13900000 },
      { code: 'TRJ-HORSE-23', name: '테를지 승마·게르 2박 3일', nights: 2, price: 1100000, per: 1700000, fixed: 4700000 }
    ];
    const f = s.f;
    const num = (v) => { const t = String(v == null ? '' : v).replace(/[^0-9-]/g, ''); const n = Number(t); return Number.isFinite(n) ? n : 0; };
    const DOW = ['일', '월', '화', '수', '목', '금', '토'];
    const pad = (n) => String(n).padStart(2, '0');
    const addDays = (iso, n) => { const [y, m, d] = iso.split('-').map(Number); return new Date(Date.UTC(y, m - 1, d + n)).toISOString().slice(0, 10); };
    const lab = (iso) => { if (!iso || iso.length < 10) return ''; const [y, m, d] = iso.split('-').map(Number); return `${pad(m)}.${pad(d)}(${DOW[new Date(Date.UTC(y, m - 1, d)).getUTCDay()]})`; };
    const p = PRODUCTS.find((x) => x.code === f.product);
    const pax = num(f.pax), lead = num(f.lead), price = num(f.price), extra = num(f.extra);
    const billedPax = f.leaderFree ? pax : pax + lead;
    const sales = price * billedPax + extra;
    const cost = p ? p.per * (pax + lead) + p.fixed : 0;
    const costKrw = Math.round(cost * R);
    const margin = sales - costKrw;
    const validArrive = /^\\d{4}-\\d{2}-\\d{2}$/.test(f.arrive || '');
    const depart = validArrive && p ? addDays(f.arrive, p.nights) : '';
    const mm = validArrive ? f.arrive.slice(5, 7) : '10';
    const SE = (() => { const v = store.get('events', null); return v == null ? s.localEvents : v; })();
    const BASE_SEQ = { '10': 24, '11': 2 };
    const seq = (BASE_SEQ[mm] || 0) + SE.filter((e) => e.code.slice(4, 6) === mm).length + (s.saved ? 0 : 1);
    const code = s.saved ? s.savedCode : `MN26${mm}-${String(seq).padStart(3, '0')}`;
    const SHORT = { 'GOBI-56': '고비', 'TRJ-GOLF-34': '테를지 골프', 'KHS-67': '홉스골', 'UB-CITY-34': 'UB 시티', 'INC-45': '인센티브', 'TRJ-HORSE-23': '테를지 승마' };
    const E = s.tried ? {
      agency: f.agency ? '' : '여행사를 고르세요.',
      product: f.product ? '' : '상품을 고르세요.',
      arrive: !validArrive ? '입국일을 입력하세요.' : f.arrive < '2026-10-01' ? '오늘(10.01) 이전 날짜입니다.' : '',
      pax: pax > 0 ? '' : '여행객 수를 1명 이상 입력하세요.',
      price: price > 0 ? '' : '1인 판매가를 입력하세요.'
    } : { agency: '', product: '', arrive: '', pax: '', price: '' };
    const errList = Object.values(E).filter(Boolean);
    const upd = (k) => (e) => set({ f: { ...s.f, [k]: e && e.target ? (e.target.type === 'checkbox' ? e.target.checked : e.target.value) : e } });
    const depRatio = f.deposit === '50%' ? 0.5 : f.deposit === '30%' ? 0.3 : 0;
    const NOW = '10.01(목) 15:42 KST';
'''
vals = '''      user: { name: '김지훈', role: '운영관리자' },
      f,
      on: { agency: upd('agency'), product: (e) => { const v = e.target.value; const np = PRODUCTS.find((x) => x.code === v); set({ f: { ...s.f, product: v, price: np && !s.f.priceTouched ? String(np.price) : s.f.price } }); }, owner: upd('owner'), arrive: upd('arrive'), pax: upd('pax'), lead: upd('lead'), inFlight: upd('inFlight'), inTime: upd('inTime'), outFlight: upd('outFlight'), outTime: upd('outTime'), pickup: upd('pickup'), price: (e) => set({ f: { ...s.f, price: e.target.value, priceTouched: true } }), extra: upd('extra'), leaderFree: upd('leaderFree'), deposit: upd('deposit'), memo: upd('memo') },
      err: E,
      agencyOptions: [{ value: '', label: '선택하세요' }, '푸른하늘여행', '한빛투어', '다온여행사', '누리투어', '제이원트래블', '솔빛여행'],
      productOptions: [{ value: '', label: '선택하세요' }].concat(PRODUCTS.map((x) => ({ value: x.code, label: `${x.code} · ${x.name}` }))),
      ownerOptions: ['김지훈', '정하린', '오세진'],
      pickupOptions: ['칭기즈칸 국제공항', '울란바토르 기차역', '호텔 로비(시내)'],
      depositOptions: ['30%', '50%', '없음'],
      productHelp: p ? `${p.nights}박 ${p.nights + 1}일 · 2026 동계 요금표(10.01–04.30) 적용` : '상품을 고르면 기본 판매가와 지상비 예산이 채워집니다.',
      departLabel: depart ? `${depart.replace(/-/g, '.')} ${lab(depart).slice(5)}` : '',
      nightsHelp: p ? `입국일 + ${p.nights}박` : '상품과 입국일을 고르면 계산됩니다',
      priceHelp: p ? `상품 기본가 ${fmt(p.price)} KRW` : '',
      leaderDesc: `과금 인원 ${billedPax}명 · 인솔자 ${lead}명`,
      depositText: depRatio ? `${fmt(Math.round(sales * depRatio))} KRW · 기한 10.08(목) · 잔금 기한 ${depart ? lab(addDays(f.arrive, -7)) : '입국 7일 전'}` : `전액 잔금 · 기한 ${validArrive ? lab(addDays(f.arrive, -7)) : '입국 7일 전'}`,
      code,
      codeCaption: s.saved ? `${NOW} 저장 · 예약 상태` : '저장할 때 확정됩니다',
      sum: { agency: f.agency || '—', product: p ? p.name : '—', period: validArrive ? `${lab(f.arrive)} – ${depart ? lab(depart) : '?'}` : '—', people: `${pax}명 + 인솔 ${lead}명` },
      sales,
      cost,
      costConv: { amount: costKrw, currency: 'KRW' },
      costBasis: p ? `요금표 기준 1인 ${fmt(p.per)} MNT × ${pax + lead}명 + 차량·가이드 ${fmt(p.fixed)} MNT · 환율 0.3985 (10.01)` : '상품을 고르면 요금표로 계산합니다.',
      margin,
      marginCaption: sales > 0 ? `마진율 ${(margin / sales * 100).toFixed(1)}% · 판매금액 − 지상비 예산(KRW 환산) · 확정 전 예상치` : '판매가를 입력하면 계산합니다.',
      hasErrors: errList.length > 0,
      errorTitle: `저장 전에 ${errList.length}곳을 확인하세요`,
      errorList: errList.join(' '),
      saved: !!s.saved,
      saveLabel: s.saved ? '저장됨' : '저장',
      saveDraft: () => say('progress', '임시저장했습니다', `${NOW} · 행사코드는 저장할 때 부여됩니다.`),
      save: () => {
        const bad = !f.agency || !f.product || !validArrive || f.arrive < '2026-10-01' || pax <= 0 || price <= 0;
        if (bad) { set({ tried: true, notice: null }); return; }
        const ev = { code, agency: f.agency, product: p.code, productName: p.name, short: SHORT[p.code] || p.name, nights: p.nights, arrive: f.arrive, depart, pax, lead, owner: f.owner, sales, cost, created: '10.02' };
        const next = SE.concat([ev]);
        store.put('events', next);
        this.setState({ tried: false, saved: true, savedCode: code, localEvents: next, notice: { tone: 'positive', title: `${code} 등록 완료`, body: `${f.agency} · ${p.name} · 예약 상태로 저장했습니다. 행사 목록에 들어갔고, 배정 캘린더 미배정 목록에 올라갔습니다.`, action: { label: '배정하러 가기', href: 'Schedule.dc.html' } } });
      },
      again: () => {
        this.setState({ saved: false, savedCode: null, tried: false, notice: null, f: { ...s.f, pax: '', inFlight: '', inTime: '', outFlight: '', outTime: '', memo: '' } });
      },'''

state = "{ f: { agency: '한빛투어', product: 'GOBI-56', owner: '김지훈', arrive: '2026-10-27', pax: '15', lead: '1', inFlight: '', inTime: '', outFlight: '', outTime: '', pickup: '칭기즈칸 국제공항', price: '1150000', extra: '0', leaderFree: true, deposit: '30%', memo: '2일차 별 관측 일정 포함 요청 · 단체 사진 촬영' }, tried: false, saved: false, savedCode: null, localEvents: [], notice: null }"
admin('EventNew.dc.html', '행사 등록', 'events', 'ops', body, pre=pre, vals=vals, state=state, height=1300)
print('EventNew written')
