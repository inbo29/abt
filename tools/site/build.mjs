// Builds a static preview site of the design system and the 32 screens into _site/
// (GitHub Pages or any static server). Sources in design-system/ and screens/ are
// copied as-is; only the component previews get the <head> tags the canvas used to
// inject (tokens, bundle, React).
//
//   node tools/site/build.mjs            -> _site/
//   node tools/site/build.mjs --serve    -> _site/ + http://localhost:4173
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const TOOLS = path.resolve(HERE, '..');
const ROOT = path.resolve(TOOLS, '..');
const OUT = path.join(ROOT, '_site');
const DS = path.join(ROOT, 'design-system');
const SCREENS = path.join(ROOT, 'screens');

const read = (p) => fs.readFileSync(p, 'utf8');
const write = (p, s) => { fs.mkdirSync(path.dirname(p), { recursive: true }); fs.writeFileSync(p, s); };
const copy = (a, b) => { fs.mkdirSync(path.dirname(b), { recursive: true }); fs.copyFileSync(a, b); };
const copyDir = (a, b) => fs.cpSync(a, b, { recursive: true });
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

// Relative .md links inside READMEs point at repo files; keep them working on the site.
marked.use({ renderer: { link({ href, text }) {
  if (href && /^(\.\.\/)*[A-Za-z]+\/README\.md$/.test(href)) href = 'components.html#' + href.split('/').slice(-2)[0];
  return `<a href="${esc(href)}">${text}</a>`;
} } });

const FONTS = 'https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap';
const REACT = ['react.production.min.js', 'react-dom.production.min.js'];

fs.rmSync(OUT, { recursive: true, force: true });

// ---- shared assets ----------------------------------------------------------
copy(path.join(SCREENS, 'ds/abt/tokens.css'), path.join(OUT, 'ds/tokens.css'));
copy(path.join(DS, 'components/bundle.css'), path.join(OUT, 'ds/bundle.css'));
copy(path.join(DS, 'components/bundle.js'), path.join(OUT, 'ds/bundle.js'));
copy(path.join(DS, 'tokens.json'), path.join(OUT, 'ds/tokens.json'));
copy(path.join(TOOLS, 'node_modules/react/umd', REACT[0]), path.join(OUT, 'vendor', REACT[0]));
copy(path.join(TOOLS, 'node_modules/react-dom/umd', REACT[1]), path.join(OUT, 'vendor', REACT[1]));
copy(path.join(HERE, 'site.css'), path.join(OUT, 'site.css'));
copy(path.join(HERE, 'site.js'), path.join(OUT, 'site.js'));

// ---- screens: copied unchanged + the standalone runtime ---------------------
copyDir(SCREENS, path.join(OUT, 'screens'));
copy(path.join(HERE, 'support.js'), path.join(OUT, 'screens/support.js'));
copyDir(path.join(OUT, 'vendor'), path.join(OUT, 'screens/vendor'));

// ---- component previews: inject what the canvas used to provide -------------
const compDir = path.join(DS, 'components');
// Cover is the design system's title card, not a component.
const comps = fs.readdirSync(compDir).filter((d) => d !== 'Cover' && fs.existsSync(path.join(compDir, d, 'preview.html')));
const order = ['Icon', 'Button', 'StatusBadge', 'Money', 'EventCode', 'DateTime', 'KpiTile', 'DataTable', 'BudgetBar', 'ApprovalSteps', 'AuditLog', 'Alert', 'ScheduleGrid', 'Tabs', 'Segmented', 'TextField', 'Select', 'MoneyField', 'Checkbox', 'Attachment', 'SideNav', 'MobileTabBar'];
comps.sort((a, b) => (order.indexOf(a) + 1 || 99) - (order.indexOf(b) + 1 || 99));

const inject = `<link rel="stylesheet" href="../../../ds/tokens.css">
<link rel="stylesheet" href="../../../ds/bundle.css">
<script src="../../../vendor/${REACT[0]}"></script>
<script src="../../../vendor/${REACT[1]}"></script>
<script src="../../../ds/bundle.js"></script>
<script>
// Follow the theme of the page that embeds this preview.
(function () {
  function apply(t) { document.documentElement.setAttribute('data-theme', t); if (document.body) document.body.setAttribute('data-theme', t); }
  var t = 'light'; try { t = parent.document.documentElement.getAttribute('data-theme') || t; } catch (e) {}
  apply(t);
  document.addEventListener('DOMContentLoaded', function () { apply(t); });
  window.addEventListener('message', function (e) { if (e.data && e.data.abtTheme) apply(e.data.abtTheme); });
})();
</script>
</head>`;

const cards = comps.map((name) => {
  const src = read(path.join(compDir, name, 'preview.html'));
  const meta = /@dsCard([^>]*)-->/.exec(src)?.[1] || '';
  const attr = (k) => new RegExp(`${k}="?([^"\\s]+)"?`).exec(meta)?.[1];
  write(path.join(OUT, 'design-system/components', name, 'preview.html'), src.replace('</head>', inject));
  const readme = path.join(compDir, name, 'README.md');
  return {
    name,
    group: attr('group') || '기타',
    height: Number(attr('height') || 200),
    width: Number(attr('width') || 0),
    doc: fs.existsSync(readme) ? marked.parse(read(readme).replace(/^# .*\n/, '')) : '',
  };
});

// ---- page shell ---------------------------------------------------------------
const NAV = [['guide.html', '소개'], ['foundations.html', '토큰'], ['components.html', '컴포넌트'], ['screens.html', '화면']];
const page = (file, title, body, toc = '') => `<!doctype html>
<html lang="ko" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)} · ABT Ops 디자인 시스템</title>
<link rel="icon" href="data:,">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="${FONTS}">
<link rel="stylesheet" href="ds/tokens.css">
<link rel="stylesheet" href="ds/bundle.css">
<link rel="stylesheet" href="site.css">
<script>try{var t=localStorage.getItem('abt-theme');if(t)document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>
</head>
<body class="abt-root">
<header class="site-head">
  <a class="site-logo" href="guide.html">ABT Ops</a>
  <nav class="site-nav">${NAV.map(([h, l]) => `<a href="${h}"${h === file ? ' aria-current="page"' : ''}>${l}</a>`).join('')}</nav>
  <button type="button" class="site-theme" id="theme-toggle" aria-label="테마 전환">라이트</button>
</header>
<div class="site-body${toc ? ' has-toc' : ''}">
${toc ? `<aside class="site-toc">${toc}</aside>` : ''}
<main class="site-main">
${body}
</main>
</div>
<script src="site.js"></script>
</body>
</html>
`;

// ---- index: brand book ------------------------------------------------------
const brand = read(path.join(DS, 'README.md'));
const brandHtml = marked.parse(brand);
const h2s = [...brand.matchAll(/^## (.+)$/gm)].map((m) => m[1]);
let n = 0;
const brandWithIds = brandHtml.replace(/<h2>/g, () => `<h2 id="s${n++}">`);
write(path.join(OUT, 'guide.html'), page('guide.html', '소개', `
<section class="hero">
  <p class="caption muted">ABT 한국·몽골 여행 운영·정산 통합 관리</p>
  <h1 class="hero-title">ABT Ops 디자인 시스템</h1>
  <p class="body muted">관리자 웹 22개 화면(1440px)과 가이드 모바일 웹 10개 화면(390×844)의 디자인 시스템과 동작하는 프로토타입입니다. 모든 이름·금액·날짜는 예시 데이터입니다.</p>
  <div class="hero-links">
    <a class="abt-btn abt-btn--primary" href="screens/Login.dc.html">프로토타입 시작</a>
    <a class="abt-btn" href="components.html">컴포넌트 ${cards.length}개</a>
    <a class="abt-btn" href="screens.html">화면 32개</a>
  </div>
</section>
<article class="prose">${brandWithIds}</article>
`, `<p class="label muted">브랜드북</p>${h2s.map((t, i) => `<a href="#s${i}">${esc(t)}</a>`).join('')}`));

// ---- foundations: tokens ----------------------------------------------------
const tok = JSON.parse(read(path.join(DS, 'tokens.json')));
const swatch = (t) => `<tr>
  <td><code>--${esc(t.name)}</code></td>
  <td><span class="sw" style="background: var(--${esc(t.name)})"></span></td>
  <td class="mono muted">${esc(t.value.dark)}</td><td class="mono muted">${esc(t.value.light)}</td>
  <td>${esc(t.usage || '')}</td></tr>`;
const simple = (group, demo) => `<table class="tok"><thead><tr><th>토큰</th><th>값</th><th></th><th>용도</th></tr></thead><tbody>${group.tokens.map((t) => `<tr>
  <td><code>--${esc(t.name)}</code></td>
  <td class="mono muted">${esc(typeof t.value === 'object' ? `${t.value.dark} / ${t.value.light}` : t.value)}</td>
  <td>${demo(t)}</td><td>${esc(t.usage || '')}</td></tr>`).join('')}</tbody></table>`;
const typeRows = (tok.type.groups || []).map((g) => `<h3>${esc(g.name)}</h3><p class="caption muted">${esc(g.note || '')}</p>
<table class="tok"><thead><tr><th>스타일</th><th>견본</th><th>크기</th><th>용도</th></tr></thead><tbody>${(g.styles || []).map((s) => `<tr>
  <td><code>.${esc(s.name)}</code></td>
  <td><span class="${esc(s.name)}">행사 정산 4,820만 KRW</span></td>
  <td class="mono muted">${esc(s.fontSize)}/${esc(s.lineHeight)} ${esc(s.fontWeight || '')}</td>
  <td>${esc(s.usage || '')}</td></tr>`).join('')}</tbody></table>`).join('');
write(path.join(OUT, 'foundations.html'), page('foundations.html', '토큰', `
<h1 class="title-1">토큰</h1>
<p class="caption muted">원본: design-system/tokens.json · 오른쪽 위에서 다크·라이트를 바꾸면 견본이 함께 바뀝니다.</p>
<h2 id="color">색</h2>
<table class="tok"><thead><tr><th>토큰</th><th></th><th>다크</th><th>라이트</th><th>용도</th></tr></thead><tbody>${tok.color.tokens.map(swatch).join('')}</tbody></table>
<h2 id="type">글꼴</h2>${typeRows}
<h2 id="spacing">간격</h2><p class="caption muted">${esc(tok.spacing.note || '')}</p>
${simple(tok.spacing, (t) => `<span class="bar" style="width: var(--${esc(t.name)})"></span>`)}
<h2 id="radius">모서리</h2>${simple(tok.radius, (t) => `<span class="rad" style="border-radius: var(--${esc(t.name)})"></span>`)}
<h2 id="shadow">그림자</h2>${simple(tok.shadow, (t) => `<span class="shd" style="box-shadow: var(--${esc(t.name)})"></span>`)}
<h2 id="size">치수</h2>${simple(tok.size, () => '')}
`, `<p class="label muted">토큰</p><a href="#color">색</a><a href="#type">글꼴</a><a href="#spacing">간격</a><a href="#radius">모서리</a><a href="#shadow">그림자</a><a href="#size">치수</a>`));

// ---- components ---------------------------------------------------------------
const groups = [...new Set(cards.map((c) => c.group))];
write(path.join(OUT, 'components.html'), page('components.html', '컴포넌트', `
<h1 class="title-1">컴포넌트</h1>
<p class="caption muted">window.Abt 의 React 18 컴포넌트 ${cards.length}개. 미리보기는 design-system/components/&lt;이름&gt;/preview.html 을 그대로 띄운 것입니다.</p>
${groups.map((g) => `<h2>${esc(g)}</h2>${cards.filter((c) => c.group === g).map((c) => `
<section class="comp" id="${c.name}">
  <div class="comp-head"><h3>${c.name}</h3><a class="caption muted" href="design-system/components/${c.name}/preview.html" target="_blank" rel="noopener">새 창에서 열기</a></div>
  <div class="comp-frame"><iframe src="design-system/components/${c.name}/preview.html" title="${c.name} 미리보기" loading="lazy" style="height: ${c.height + 2}px${c.width ? `; min-width: ${Math.min(c.width, 1200)}px` : ''}"></iframe></div>
  <div class="prose">${c.doc}</div>
</section>`).join('')}`).join('')}
`, groups.map((g) => `<p class="label muted">${esc(g)}</p>${cards.filter((c) => c.group === g).map((c) => `<a href="#${c.name}">${c.name}</a>`).join('')}`).join('')));

// ---- screens -----------------------------------------------------------------
const canvas = JSON.parse(read(path.join(SCREENS, 'canvas.json')));
const rows = Object.values(canvas.notes).filter((x) => x.kind === 'title1').sort((a, b) => a.y - b.y);
const rowOf = (b) => [...rows].reverse().find((r) => r.y <= b.y) || rows[0];
const screenDocs = read(path.join(ROOT, 'docs/screens.md'));
const summary = (file) => {
  // docs/screens.md rows: | `File.dc.html` | 화면 | 하는 일 | 이동 | 저장 데이터 |
  const line = screenDocs.split('\n').find((l) => l.startsWith(`| \`${file}\``));
  const text = line ? (line.split('|')[3] || '').replace(/\*\*|`/g, '').trim() : '';
  return text.length > 110 ? text.slice(0, 108) + '…' : text;
};
const boards = canvas.order.map((f) => ({ file: f, ...canvas.boards[f] }));
const about = canvas.notes.about?.text || '';
write(path.join(OUT, 'screens.html'), page('screens.html', '화면', `
<h1 class="title-1">화면</h1>
<p class="caption muted">각 화면은 실제로 동작합니다. 메뉴·행사코드·표의 행·버튼을 누르면 다음 화면으로 이어집니다. 입력한 내용은 이 브라우저의 localStorage 에만 저장됩니다.</p>
<div class="note">${esc(about).replace(/\n\n/g, '</p><p>').replace(/^/, '<p>')}</p></div>
${rows.map((r, ri) => `<h2 id="r${ri}">${esc(r.text)}</h2><div class="screen-grid">${boards.filter((b) => rowOf(b) === r).map((b) => `
<a class="screen-card${b.w <= 480 ? ' is-mobile' : ''}" href="screens/${b.file}">
  <span class="title-3">${esc(b.title)}</span>
  <span class="caption muted">${esc(summary(b.file))}</span>
  <span class="caption mono muted">${b.file} · ${b.w}×${b.h}</span>
</a>`).join('')}</div>`).join('')}
`, `<p class="label muted">영역</p>${rows.map((r, i) => `<a href="#r${i}">${esc(r.text)}</a>`).join('')}`));

// The site opens on the prototype's login screen; the docs live at guide.html.
write(path.join(OUT, 'index.html'), `<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>ABT Ops</title>
<meta http-equiv="refresh" content="0; url=screens/Login.dc.html">
<script>location.replace('screens/Login.dc.html' + location.hash);</script>
</head>
<body><a href="screens/Login.dc.html">로그인 화면으로 이동</a></body>
</html>
`);
write(path.join(OUT, '.nojekyll'), '');
write(path.join(OUT, 'favicon.ico'), ''); // screens are copied as-is and have no icon link
console.log(`_site/: ${cards.length} components, ${boards.length} screens`);

// ---- optional local server ------------------------------------------------------
if (process.argv.includes('--serve')) {
  const port = Number(process.env.PORT || 4173);
  const types = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png' };
  http.createServer((req, res) => {
    let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    if (p.endsWith('/')) p += 'index.html';
    const file = path.join(OUT, p);
    if (!file.startsWith(OUT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); return res.end('not found'); }
    res.writeHead(200, { 'content-type': types[path.extname(file)] || 'application/octet-stream' });
    fs.createReadStream(file).pipe(res);
  }).listen(port, () => console.log(`http://localhost:${port}/`));
}
