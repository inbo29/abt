# Artboard generator helpers for the ABT Ops canvas. Bodies are literal x-dc markup; {{holes}} pass through untouched.
import json, os

# Screens are written to <repo>/screens (override with ABT_SCREENS_DIR).
OUT = os.environ.get('ABT_SCREENS_DIR') or os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'screens'))

FONTS = 'https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&amp;family=IBM+Plex+Sans+KR:wght@400;500;600;700&amp;family=IBM+Plex+Sans:wght@400;500;600;700&amp;display=swap'

LINKS_JS = """{ dashboard: 'Main.dc.html', alerts: 'Alerts.dc.html', reports: 'Reports.dc.html', events: 'Events.dc.html', schedule: 'Schedule.dc.html', field: 'FieldReports.dc.html', claims: 'Claims.dc.html', receipts: 'Receipts.dc.html', costs: 'Approvals.dc.html', remit: 'Remittance.dc.html', balance: 'Balance.dc.html', settlement: 'Settlement.dc.html', agencies: 'Agencies.dc.html', products: 'Products.dc.html', partners: 'Partners.dc.html', resources: 'Resources.dc.html', manuals: 'Manuals.dc.html', users: 'Users.dc.html', audit: 'Audit.dc.html' }"""
NAVC_JS = """{ alerts: 5, field: 2, claims: { n: 2, tone: 'critical' }, receipts: { n: 1, tone: 'critical' }, costs: { n: 7, tone: 'attention' }, remit: 3 }"""
TAB_LINKS_JS = """{ today: 'GuideToday.dc.html', schedule: 'GuideSchedule.dc.html', add: 'GuideAdd.dc.html', settle: 'GuideSettle.dc.html', notice: 'GuideNotice.dc.html' }"""

USERS = {
    'ceo': "{ name: '이도윤', role: '대표' }",
    'ops': "{ name: '김지훈', role: '운영관리자' }",
    'acc': "{ name: '박서연', role: '회계담당자' }",
}


def head(title):
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
<link rel="stylesheet" href="ds/abt/tokens.css">
<link rel="stylesheet" href="ds/abt/components/bundle.css">
<script src="ds/abt/components/bundle.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="{FONTS}">
<style>
body{{margin:0}}
a{{color:inherit}}a:hover{{color:inherit}}
</style>
</helmet>
'''


def header(title, caption, actions=''):
    return f'''<header style="display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 16px">
<div style="display: flex; flex-direction: column; gap: 4px">
<h1 class="title-1" style="margin: 0">{title}</h1>
<p class="caption" style="margin: 0; color: var(--ink-muted)">{caption}</p>
</div>
<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px">
{actions}
</div>
</header>
'''


PANEL = '<section style="display: flex; flex-direction: column; gap: 12px; padding: 20px; background: var(--surface); border: 1px solid var(--line); border-radius: 6px">'
PANEL_TIGHT = '<section style="display: flex; flex-direction: column; gap: 4px; padding: 4px 20px; background: var(--surface); border: 1px solid var(--line); border-radius: 6px">'


def panel_title(title, caption=''):
    cap = f'\n<p class="caption" style="margin: 0; color: var(--ink-muted)">{caption}</p>' if caption else ''
    return f'''<div style="display: flex; flex-wrap: wrap; align-items: baseline; justify-content: space-between; gap: 12px">
<h2 class="title-2" style="margin: 0">{title}</h2>{cap}
</div>
'''


def script(width, height, state, pre, vals, user=None, mobile=False):
    st = state if state else '{}'
    userline = f"      user: {USERS[user]},\n" if user else ''
    common = (f"      links: LINKS,\n      navCounts: {NAVC_JS},\n{userline}" if not mobile else f"      tabLinks: {TAB_LINKS_JS},\n      badges: {{ notice: 3 }},\n")
    return f'''<script type="text/x-dc" data-dc-script data-props='{{"theme":{{"editor":"enum","options":["dark","light"],"default":"dark","section":"화면"}},"$preview":{{"width":{width},"height":{height}}}}}'>
class Component extends DCLogic {{
  constructor(props) {{
    super(props);
    this.abtStore = {{
      get: (k, d) => {{ try {{ const v = window.localStorage.getItem('abt:' + k); return v == null ? d : JSON.parse(v); }} catch (e) {{ return d; }} }},
      put: (k, v) => {{ try {{ window.localStorage.setItem('abt:' + k, JSON.stringify(v)); }} catch (e) {{}} }}
    }};
    let saved;
    try {{ saved = window.localStorage.getItem('abt-theme') || undefined; }} catch (e) {{ saved = undefined; }}
    this.state = Object.assign({{ theme: saved }}, {st});
  }}
  componentDidMount() {{
    this._onStorage = (e) => {{ if (!e || !e.key) return; if (e.key === 'abt-theme' && (e.newValue === 'dark' || e.newValue === 'light')) this.setState({{ theme: e.newValue }}); else if (e.key.indexOf('abt:') === 0) {{ const k = e.key.slice(4); const map = (this.state && this.state.__sync) || {{}}; const patch = {{ storeRev: Date.now() }}; if (map[k]) {{ let v = null; try {{ v = e.newValue == null ? null : JSON.parse(e.newValue); }} catch (x) {{ v = null; }} patch[map[k][0]] = v == null ? map[k][1] : v; }} this.setState(patch); }} }};
    try {{ window.addEventListener('storage', this._onStorage); }} catch (e) {{}}
  }}
  componentWillUnmount() {{
    try {{ window.removeEventListener('storage', this._onStorage); }} catch (e) {{}}
  }}
  renderVals() {{
    const LINKS = {LINKS_JS};
    const s = this.state;
    const set = (patch) => this.setState(patch);
    const store = this.abtStore;
    const fmt = (n, d) => new Intl.NumberFormat('ko-KR', {{ minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }}).format(n);
    const fin = (w) => {{ const c = String(w).charCodeAt(String(w).length - 1); return c >= 0xAC00 && c <= 0xD7A3 ? (c - 0xAC00) % 28 : -1; }};
    const ro = (w) => w + (fin(w) === 0 || fin(w) === 8 || fin(w) === -1 ? '로' : '으로');
    const eul = (w) => w + (fin(w) > 0 ? '을' : '를');
    const say = (tone, title, body, action) => this.setState({{ notice: {{ tone, title, body: body || '', action: action || null }} }});
{pre}
    return {{
      theme: s.theme || this.props.theme || 'dark',
      themeOptions: [{{ value: 'dark', label: '다크' }}, {{ value: 'light', label: '라이트' }}],
      setTheme: (v) => {{ try {{ window.localStorage.setItem('abt-theme', v); }} catch (e) {{}} this.setState({{ theme: v }}); }},
      yes: true,
      no: false,
      two: 2,
      three: 3,
      hasNotice: !!s.notice,
      notice: s.notice || {{ tone: 'positive', title: '', body: '' }},
      noticeAction: s.notice && s.notice.action ? s.notice.action : {{ label: '닫기', onClick: () => this.setState({{ notice: null }}) }},
{common}{vals}
    }};
  }}
}}
</script>
</body>
</html>
'''


def admin(file, title, active, user, body, pre='', vals='', state=None, height=1100):
    html = head(title)
    html += f'''<div data-theme="{{{{theme}}}}" class="abt-root" style="display: grid; grid-template-columns: 232px minmax(0, 1fr); min-height: 100vh; background: var(--bg); color: var(--ink); font-family: var(--font-sans)">
<div style="position: sticky; top: 0; align-self: start; height: 100vh">
<x-import component-from-global-scope="Abt.SideNav" active="{active}" org="ABT 한국·몽골 통합" links="{{{{links}}}}" counts="{{{{navCounts}}}}" user="{{{{user}}}}" logout="Login.dc.html" theme="{{{{theme}}}}" on-theme-change="{{{{setTheme}}}}" style="display: block; height: 100%"></x-import>
</div>
<main style="min-width: 0; display: flex; flex-direction: column; gap: 20px; padding: 28px 32px 48px">
'''
    html += body.strip('\n') + '\n'
    html += '</main>\n</div>\n</x-dc>\n'
    html += script(1440, height, state, pre, vals, user=user)
    open(os.path.join(OUT, file), 'w', encoding='utf-8', newline='\n').write(html)
    return file


def mobile(file, title, active, body, pre='', vals='', state=None):
    html = head(title)
    html += f'''<div data-theme="{{{{theme}}}}" class="abt-root abt-mobile" style="position: relative; width: 390px; height: 844px; overflow: hidden; display: flex; flex-direction: column; background: var(--bg); color: var(--ink); font-family: var(--font-sans)">
<div style="flex-shrink: 0; display: flex; align-items: center; justify-content: space-between; gap: 8px; padding: 8px 16px; border-bottom: 1px solid var(--line); background: var(--surface)">
<span style="font: 700 15px/20px var(--font-sans)">ABT 가이드</span>
<x-import component-from-global-scope="Abt.Segmented" size="sm" options="{{{{themeOptions}}}}" value="{{{{theme}}}}" on-change="{{{{setTheme}}}}" aria-label="화면 테마"></x-import>
</div>
<div style="flex: 1; min-height: 0; overflow-y: auto; display: flex; flex-direction: column; gap: 16px; padding: 16px 16px 24px">
'''
    html += body.strip('\n') + '\n'
    html += f'''</div>
<x-import component-from-global-scope="Abt.MobileTabBar" active="{active}" links="{{{{tabLinks}}}}" badges="{{{{badges}}}}" style="display: block; flex-shrink: 0"></x-import>
</div>
</x-dc>
'''
    html += script(390, 844, state, pre, vals, mobile=True)
    open(os.path.join(OUT, file), 'w', encoding='utf-8', newline='\n').write(html)
    return file


def mhead(title, back='GuideToday.dc.html', back_label='오늘로 돌아가기', code=None, caption=None):
    code_html = f'\n<x-import component-from-global-scope="Abt.EventCode" code="{code}"></x-import>' if code else ''
    cap = f'\n<p class="m-caption" style="margin: 0; color: var(--ink-muted)">{caption}</p>' if caption else ''
    backlink = f'<a href="{back}" class="m-label" style="align-self: flex-start; min-height: 44px; display: inline-flex; align-items: center; color: var(--ink-muted); text-decoration: underline; text-underline-offset: 3px">{back_label}</a>\n' if back else ''
    return f'''<header style="display: flex; flex-direction: column; gap: 8px">
{backlink}<div style="display: flex; align-items: center; justify-content: space-between; gap: 8px">
<h1 class="m-title" style="margin: 0">{title}</h1>{code_html}
</div>{cap}
</header>
'''

MCARD = '<section style="display: flex; flex-direction: column; gap: 10px; padding: 16px; background: var(--surface); border: 1px solid var(--line); border-radius: 12px">'


NOTICE = """<sc-if value="{{hasNotice}}" hint-placeholder-val="{{false}}">
<x-import component-from-global-scope="Abt.Alert" tone="{{notice.tone}}" title="{{notice.title}}" action="{{noticeAction}}">{{notice.body}}</x-import>
</sc-if>
"""


def dl(rows, label_w=96, mobile=False):
    lab = 'm-caption' if mobile else 'label'
    fs = '15px; line-height: 22px' if mobile else '13px; line-height: 20px'
    out = f'<dl style="display: grid; grid-template-columns: {label_w}px minmax(0, 1fr); gap: 8px 12px; margin: 0; font-size: {fs}">\n'
    for l, v in rows:
        out += f'<dt class="{lab}" style="color: var(--ink-muted); line-height: 20px">{l}</dt>\n<dd style="margin: 0; min-width: 0">{v}</dd>\n'
    return out + '</dl>\n'


def field_grid(min_w=220):
    return f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min({min_w}px, 100%), 1fr)); gap: 12px 16px; align-items: start">'


TWO_PANE = '<div style="display: grid; grid-template-columns: minmax(0, 1.35fr) minmax(360px, 1fr); gap: 16px; align-items: start">'
SIDE_PANEL = '<section style="position: sticky; top: 16px; display: flex; flex-direction: column; gap: 16px; padding: 20px; background: var(--surface); border: 1px solid var(--line); border-radius: 6px; min-width: 0">'
