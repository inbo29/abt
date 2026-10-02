// Theme toggle for the docs site. Uses the same 'abt-theme' key as the screens,
// so the choice carries over into the prototype.
(function () {
  var root = document.documentElement;
  var btn = document.getElementById('theme-toggle');
  function label() { btn.textContent = root.getAttribute('data-theme') === 'light' ? '다크' : '라이트'; }
  function set(t) {
    root.setAttribute('data-theme', t);
    try { localStorage.setItem('abt-theme', t); } catch (e) {}
    document.querySelectorAll('iframe').forEach(function (f) {
      try { f.contentWindow.postMessage({ abtTheme: t }, '*'); } catch (e) {}
    });
    label();
  }
  btn.addEventListener('click', function () { set(root.getAttribute('data-theme') === 'light' ? 'dark' : 'light'); });
  label();
})();
