/*
 * ABT Ops prototype — standalone runtime for screens/*.dc.html.
 *
 * The screens were written for the Claude design canvas, which provides its
 * own ./support.js. This file stands in for it outside the canvas (local
 * preview, GitHub Pages). It implements only what the screens use:
 *
 *   <x-dc> … </x-dc>                    template, rendered with React 18
 *   <helmet> … </helmet>                moved into <head>
 *   {{a.b}}                             binding in text and attributes
 *   <sc-for list="{{xs}}" as="x">       repeat
 *   <sc-if value="{{cond}}">            conditional
 *   <x-import component-from-global-scope="Abt.Name" kebab-prop="…">
 *                                       component; kebab props -> camelCase,
 *                                       `style` stays on the <x-import> wrapper
 *   <script type="text/x-dc" data-dc-script data-props='{…}'>
 *     class Component extends DCLogic { constructor, componentDidMount,
 *     componentWillUnmount, renderVals, this.setState(patch) }
 *
 * It must be loaded as a classic (blocking) script before bundle.js: it pulls
 * in React and ReactDOM from ./vendor/ so that bundle.js finds window.React.
 */
(function () {
  'use strict';

  // Props that override the screens' data-props defaults on this site.
  // The screens default to dark; the preview site opens in light.
  var SITE_DEFAULTS = { theme: 'light' };

  // Action results ("엑셀 파일을 만들었습니다", "송금 요청이 접수되었습니다") are inline
  // <sc-if> + Abt.Alert blocks in the screens, which push the page around when they
  // appear. On this site they show as toasts instead and clear themselves after
  // TOAST_MS by applying the given state patch. Alerts that describe data
  // (risk, missing proof, …) stay inline.
  var TOASTS = {
    hasNotice: { notice: null },   // every screen: say(tone, title, body, action)
    exported: { exported: false }  // Reports: 엑셀 다운로드
  };
  var TOAST_MS = 6000;

  var self = document.currentScript;
  var base = self && self.src ? self.src.replace(/[^/]*$/, '') : './';

  // Hide the raw template until it is rendered, and load React synchronously.
  document.write('<style>' +
    'x-dc{display:none!important}' +
    'html,body{overflow-x:clip}' +
    '.dc-toasts{position:fixed;right:24px;bottom:24px;z-index:1000;display:flex;flex-direction:column;gap:8px;' +
      'width:min(440px,calc(100vw - 32px));background:transparent!important;pointer-events:none}' +
    '.dc-toasts.is-mobile{position:absolute;left:16px;right:16px;bottom:calc(var(--tabbar-height,64px) + 12px);width:auto}' +
    '.dc-toast{pointer-events:auto;border-radius:var(--radius-md,6px);box-shadow:var(--shadow-lg)}' +
    '.dc-toast x-import{display:block}' +
  '</style>');
  if (!window.React) {
    document.write(
      '<script src="' + base + 'vendor/react.production.min.js"><\/script>' +
      '<script src="' + base + 'vendor/react-dom.production.min.js"><\/script>'
    );
  }

  // ---- DCLogic ------------------------------------------------------------

  function DCLogic(props) {
    this.props = props || {};
    this.state = {};
  }
  DCLogic.prototype.setState = function (patch) {
    if (typeof patch === 'function') patch = patch(this.state, this.props);
    if (patch == null) return;
    this.state = Object.assign({}, this.state, patch);
    if (this.__update) this.__update();
  };
  DCLogic.prototype.componentDidMount = function () {};
  DCLogic.prototype.componentWillUnmount = function () {};
  DCLogic.prototype.renderVals = function () { return {}; };
  window.DCLogic = DCLogic;

  // ---- Template compile (DOM -> plain tree) --------------------------------

  var BIND_ONE = /^\{\{\s*([^{}]+?)\s*\}\}$/;
  var BIND_ANY = /\{\{\s*([^{}]+?)\s*\}\}/g;

  function compile(node) {
    if (node.nodeType === 3) return { t: 'text', v: node.nodeValue };
    if (node.nodeType !== 1) return null;
    var attrs = [];
    for (var i = 0; i < node.attributes.length; i++) {
      attrs.push([node.attributes[i].name, node.attributes[i].value]);
    }
    var kids = [];
    for (var c = node.firstChild; c; c = c.nextSibling) {
      var k = compile(c);
      if (k) kids.push(k);
    }
    return { t: 'el', tag: node.tagName.toLowerCase(), attrs: attrs, kids: kids };
  }

  // ---- Binding resolution ---------------------------------------------------

  function lookup(scopes, expr) {
    if (expr === 'true') return true;
    if (expr === 'false') return false;
    if (expr === 'null') return null;
    if (/^-?\d+(\.\d+)?$/.test(expr)) return Number(expr);
    var path = expr.split('.');
    for (var i = scopes.length - 1; i >= 0; i--) {
      var s = scopes[i];
      if (s != null && Object.prototype.hasOwnProperty.call(s, path[0])) {
        var v = s[path[0]];
        for (var j = 1; j < path.length && v != null; j++) v = v[path[j]];
        return v;
      }
    }
    return undefined;
  }

  function evalStr(str, scopes) {
    var m = BIND_ONE.exec(str);
    if (m) return lookup(scopes, m[1]);
    if (str.indexOf('{{') < 0) return str;
    return str.replace(BIND_ANY, function (_, e) {
      var v = lookup(scopes, e);
      return v == null || v === false ? '' : String(v);
    });
  }

  // ---- Render (plain tree -> React elements) --------------------------------

  var h;
  var current = null;   // { inst } of the screen being rendered
  var toastHost = null; // DOM node the toasts are portalled into

  function Toast(p) {
    var clear = React.useRef(p.clear);
    clear.current = p.clear;
    var hover = React.useRef(false);
    React.useEffect(function () {
      var left = TOAST_MS;
      var id = setInterval(function () {
        if (hover.current) return;
        left -= 200;
        if (left <= 0) { clearInterval(id); clear.current(); }
      }, 200);
      return function () { clearInterval(id); };
    }, [p.sig]);
    return ReactDOM.createPortal(h('div', {
      className: 'dc-toast',
      onMouseEnter: function () { hover.current = true; },
      onMouseLeave: function () { hover.current = false; }
    }, p.children), toastHost);
  }
  var ATTR = {
    'class': 'className', 'for': 'htmlFor', tabindex: 'tabIndex', readonly: 'readOnly',
    maxlength: 'maxLength', minlength: 'minLength', autocomplete: 'autoComplete',
    autofocus: 'autoFocus', inputmode: 'inputMode', colspan: 'colSpan', rowspan: 'rowSpan',
    contenteditable: 'contentEditable', spellcheck: 'spellCheck', enterkeyhint: 'enterKeyHint',
    srcset: 'srcSet', crossorigin: 'crossOrigin', datetime: 'dateTime'
  };
  var EVENT = {
    onclick: 'onClick', onchange: 'onChange', oninput: 'onInput', onsubmit: 'onSubmit',
    onkeydown: 'onKeyDown', onkeyup: 'onKeyUp', onfocus: 'onFocus', onblur: 'onBlur',
    onmouseenter: 'onMouseEnter', onmouseleave: 'onMouseLeave', ondblclick: 'onDoubleClick'
  };
  var BOOL = { disabled: 1, checked: 1, hidden: 1, readonly: 1, required: 1, selected: 1, multiple: 1, autofocus: 1, open: 1 };

  function camel(s) { return s.replace(/-([a-z])/g, function (_, c) { return c.toUpperCase(); }); }

  function parseStyle(css) {
    var out = {};
    String(css).split(';').forEach(function (decl) {
      var i = decl.indexOf(':');
      if (i < 0) return;
      var k = decl.slice(0, i).trim();
      var v = decl.slice(i + 1).trim();
      if (!k || v === '') return;
      out[k.indexOf('--') === 0 ? k : camel(k)] = v;
    });
    return out;
  }

  function isHint(name) { return name.indexOf('hint-') === 0; }

  function nativeProps(node, scopes) {
    var p = {};
    var hasHandler = false;
    node.attrs.forEach(function (a) { if (a[0] === 'onchange' || a[0] === 'oninput') hasHandler = true; });
    node.attrs.forEach(function (a) {
      var name = a[0], v = evalStr(a[1], scopes);
      if (isHint(name)) return;
      if (EVENT[name] || name.indexOf('on') === 0) {
        if (typeof v === 'function') p[EVENT[name] || ('on' + name.charAt(2).toUpperCase() + name.slice(3))] = v;
        return;
      }
      if (name === 'style') { p.style = parseStyle(v); return; }
      if (BOOL[name]) {
        var b = v === '' ? true : !!v && v !== 'false';
        // Checkbox/input state without a handler stays uncontrolled.
        if ((name === 'checked') && !hasHandler) p.defaultChecked = b;
        else p[ATTR[name] || name] = b;
        return;
      }
      if (name === 'value' && node.tag === 'input' && !hasHandler) { p.defaultValue = v; return; }
      if (v == null || v === false && name.indexOf('aria-') !== 0) return;
      p[ATTR[name] || name] = v;
    });
    return p;
  }

  function importProps(node, scopes) {
    var p = {}, wrap = {}, comp = null;
    node.attrs.forEach(function (a) {
      var name = a[0];
      if (name === 'component-from-global-scope') { comp = a[1]; return; }
      if (isHint(name)) return;
      var v = evalStr(a[1], scopes);
      if (name === 'style') { wrap.style = parseStyle(v); return; }
      if (name === 'class') { wrap.className = v; return; }
      if (v === undefined) return;
      p[camel(name)] = v;
    });
    return { comp: comp, props: p, wrap: wrap };
  }

  function resolveGlobal(path) {
    var v = window;
    path.split('.').forEach(function (k) { v = v == null ? v : v[k]; });
    return v;
  }

  function renderKids(kids, scopes) {
    var out = [];
    for (var i = 0; i < kids.length; i++) {
      var r = renderNode(kids[i], scopes, i);
      if (r !== null && r !== undefined && r !== '') out.push(r);
    }
    return out;
  }

  function renderNode(node, scopes, key) {
    if (node.t === 'text') {
      var v = evalStr(node.v, scopes);
      if (v == null || v === false || v === true) return null;
      return typeof v === 'object' ? v : String(v);
    }
    var attr = function (n) {
      for (var i = 0; i < node.attrs.length; i++) if (node.attrs[i][0] === n) return node.attrs[i][1];
      return null;
    };
    switch (node.tag) {
      case 'helmet':
        return null;
      case 'sc-if': {
        var cond = attr('value') || '';
        if (!evalStr(cond, scopes)) return null;
        var m = BIND_ONE.exec(cond);
        var patch = m && TOASTS[m[1]];
        if (patch && toastHost && current) {
          var inst = current.inst;
          var sig = Object.keys(patch).map(function (k) { return inst.state[k]; })[0];
          return h(Toast, { key: key, sig: sig, clear: function () { inst.setState(patch); } }, renderKids(node.kids, scopes));
        }
        return h.apply(null, [React.Fragment, { key: key }].concat(renderKids(node.kids, scopes)));
      }
      case 'sc-for': {
        var list = evalStr(attr('list') || '', scopes);
        var as = attr('as') || 'item';
        if (!list || typeof list.map !== 'function') return null;
        var items = list.map(function (item, i) {
          var frame = {}; frame[as] = item;
          return h.apply(null, [React.Fragment, { key: i }].concat(renderKids(node.kids, scopes.concat([frame]))));
        });
        return h(React.Fragment, { key: key }, items);
      }
      case 'x-import': {
        var ip = importProps(node, scopes);
        var Comp = resolveGlobal(ip.comp);
        if (!Comp) {
          console.warn('[support.js] missing component', ip.comp);
          return null;
        }
        var children = renderKids(node.kids, scopes);
        var args = [Comp, ip.props].concat(children);
        ip.wrap.key = key;
        return h('x-import', ip.wrap, h.apply(null, args));
      }
      default: {
        var props = nativeProps(node, scopes);
        props.key = key;
        return h.apply(null, [node.tag, props].concat(renderKids(node.kids, scopes)));
      }
    }
  }

  // ---- Boot ---------------------------------------------------------------

  function propsFromScript(script) {
    var props = {};
    try {
      var spec = JSON.parse(script.getAttribute('data-props') || '{}');
      Object.keys(spec).forEach(function (k) {
        if (k.charAt(0) !== '$' && spec[k] && 'default' in spec[k]) props[k] = spec[k]['default'];
      });
      Object.assign(props, SITE_DEFAULTS);
      props.$preview = spec.$preview;
    } catch (e) {}
    return props;
  }

  function showError(err) {
    var pre = document.createElement('pre');
    pre.style.cssText = 'margin:16px;padding:16px;border:1px solid #c33;color:#c33;background:#fff;white-space:pre-wrap;font:12px/1.5 monospace';
    pre.textContent = '[support.js] ' + (err && err.stack || err);
    document.body.appendChild(pre);
  }

  function boot() {
    var tpl = document.querySelector('x-dc');
    var script = document.querySelector('script[data-dc-script]');
    if (!tpl || !script) return;
    if (!window.React || !window.ReactDOM) return showError('React 18 is not loaded (vendor/ missing?)');
    h = React.createElement;

    // <helmet> content goes to <head>.
    var helmet = tpl.querySelector('helmet');
    if (helmet) {
      while (helmet.firstChild) document.head.appendChild(helmet.firstChild);
      helmet.parentNode.removeChild(helmet);
    }

    var tree = [];
    for (var c = tpl.firstChild; c; c = c.nextSibling) {
      var k = compile(c);
      if (k) tree.push(k);
    }

    var Cls;
    try {
      Cls = new Function('DCLogic', 'React', script.textContent + '\n;return Component;')(DCLogic, React);
    } catch (e) { return showError(e); }

    var props = propsFromScript(script);

    function Host() {
      var ref = React.useRef(null);
      var force = React.useReducer(function (x) { return x + 1; }, 0)[1];
      if (!ref.current) ref.current = new Cls(props);
      var inst = ref.current;
      inst.__update = force;
      React.useEffect(function () {
        inst.componentDidMount();
        return function () { inst.componentWillUnmount(); };
      }, []);
      var vals = inst.renderVals();
      // Toasts sit outside the screen's [data-theme] root, so follow its theme.
      if (toastHost && vals.theme) toastHost.setAttribute('data-theme', vals.theme);
      current = { inst: inst };
      return h.apply(null, [React.Fragment, null].concat(renderKids(tree, [vals])));
    }

    // Phone-sized screens ($preview width <= 480) are centred like a device.
    var pv = props.$preview || {};
    var mobile = pv.width && pv.width <= 480;
    var frame = document.createElement('div');
    var root = document.createElement('div');
    root.id = 'dc-root';
    toastHost = document.createElement('div');
    toastHost.className = 'dc-toasts abt-root' + (mobile ? ' is-mobile abt-mobile' : '');
    toastHost.setAttribute('aria-live', 'polite');
    if (mobile) {
      document.documentElement.style.background = '#0a0d0f';
      document.body.style.cssText += ';margin:0;min-height:100vh;display:flex;align-items:flex-start;justify-content:center;padding:24px 0;box-sizing:border-box';
      frame.style.cssText = 'position:relative;width:' + pv.width + 'px;box-shadow:0 0 0 1px #2a3136,0 12px 40px rgba(0,0,0,.5);border-radius:12px;overflow:hidden';
    }
    frame.appendChild(root);
    frame.appendChild(toastHost);
    tpl.parentNode.insertBefore(frame, tpl);
    tpl.parentNode.removeChild(tpl);

    try {
      ReactDOM.createRoot(root).render(h(Host));
    } catch (e) { showError(e); }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
