(function () {
  const STORAGE_KEY = 'gwo-lang';
  const DEFAULT_LANG = 'ko';
  const SUPPORTED = [
    { code: 'ko', label: '한국어', native: '한국어', flag: '🇰🇷', dir: 'ltr' },
    { code: 'si', label: 'Sri Lanka', native: 'සිංහල', flag: '🇱🇰', dir: 'ltr' },
    { code: 'en', label: 'English', native: 'English', flag: '🇬🇧', dir: 'ltr' },
    { code: 'zh', label: 'China', native: '中文', flag: '🇨🇳', dir: 'ltr' },
    { code: 'fil', label: 'Philippines', native: 'Filipino', flag: '🇵🇭', dir: 'ltr' },
    { code: 'th', label: 'Thailand', native: 'ไทย', flag: '🇹🇭', dir: 'ltr' },
    { code: 'ur', label: 'Pakistan', native: 'اردو', flag: '🇵🇰', dir: 'rtl' },
    { code: 'uz', label: 'Uzbekistan', native: 'Oʻzbek', flag: '🇺🇿', dir: 'ltr' },
    { code: 'ky', label: 'Kyrgyzstan', native: 'Кыргызча', flag: '🇰🇬', dir: 'ltr' }
  ];

  let cache = {};
  let currentLang = DEFAULT_LANG;
  let fallbackDict = null;

  function getPageId() {
    return document.body.dataset.page || 'index';
  }

  function getNested(obj, path) {
    return path.split('.').reduce((acc, key) => (acc && acc[key] != null ? acc[key] : null), obj);
  }

  function resolve(dict, key) {
    const page = getPageId();
    const candidates = [`pages.${page}.${key}`, `index.${key}`, `common.${key}`, key];
    for (const path of candidates) {
      const val = getNested(dict, path);
      if (val != null) return val;
    }
    if (fallbackDict && dict !== fallbackDict) {
      for (const path of candidates) {
        const val = getNested(fallbackDict, path);
        if (val != null) return val;
      }
    }
    return null;
  }

  function getElementScope(el) {
    if (el.dataset.i18nScope) return el.dataset.i18nScope;
    const scoped = el.closest('[data-i18n-scope]');
    if (scoped) return scoped.dataset.i18nScope;
    if (el.closest('[data-lang-fixed="ko"]')) return 'admin';
    return 'any';
  }

  function pickDict(el) {
    if (!fallbackDict) return cache[currentLang] || null;
    if (currentLang === 'ko') return fallbackDict;
    const scope = getElementScope(el);
    if (scope === 'admin' || el.closest('[data-lang-fixed="ko"]')) return fallbackDict;
    if (scope === 'worker' || el.closest('[data-i18n-scope="worker"]')) {
      return cache[currentLang] || fallbackDict;
    }
    return fallbackDict;
  }

  async function loadLocale(code) {
    if (cache[code]) return cache[code];
    const res = await fetch(`assets/locales/${code}.json`);
    if (!res.ok) throw new Error(`Locale ${code} not found`);
    const data = await res.json();
    cache[code] = data;
    return data;
  }

  function applyToElement(el, value, mode) {
    if (value == null) return;
    if (mode === 'html') el.innerHTML = value;
    else if (mode === 'placeholder') el.setAttribute('placeholder', value);
    else if (mode === 'aria') el.setAttribute('aria-label', value);
    else if (mode === 'title') document.title = value;
    else el.textContent = value;
  }

  function applyTranslations() {
    const all = document.querySelectorAll('[data-i18n], [data-i18n-html], [data-i18n-placeholder], [data-i18n-aria]');
    all.forEach(el => {
      const dict = pickDict(el);
      if (!dict) return;
      if (el.dataset.i18n) applyToElement(el, resolve(dict, el.dataset.i18n), el.dataset.i18nMode);
      if (el.dataset.i18nHtml) applyToElement(el, resolve(dict, el.dataset.i18nHtml), 'html');
      if (el.dataset.i18nPlaceholder) applyToElement(el, resolve(dict, el.dataset.i18nPlaceholder), 'placeholder');
      if (el.dataset.i18nAria) applyToElement(el, resolve(dict, el.dataset.i18nAria), 'aria');
    });

    if (getPageId() === 'index' && currentLang !== 'ko') {
      const t = resolve(cache[currentLang] || fallbackDict, 'meta.title');
      if (t) document.title = t;
    } else if (document.body.dataset.i18nTitle) {
      const dict = pickDict(document.body);
      applyToElement(document, resolve(dict, document.body.dataset.i18nTitle), 'title');
    }

    const langPill = document.querySelector('[data-lang-pill]');
    if (langPill) {
      const meta = SUPPORTED.find(l => l.code === currentLang);
      if (meta) langPill.textContent = meta.native;
    }

    document.body.classList.toggle('lang-worker-active', currentLang !== 'ko');
  }

  function setDocumentLang(code) {
    const meta = SUPPORTED.find(l => l.code === code) || SUPPORTED[0];
    document.documentElement.lang = code === 'ko' ? 'ko' : code;
    document.documentElement.dir = meta.dir;
    document.body.classList.toggle('is-rtl', meta.dir === 'rtl');
  }

  function closeLangMenu(menu, btn) {
    menu.hidden = true;
    btn.setAttribute('aria-expanded', 'false');
  }

  function renderLangSwitcher() {
    const mount = document.getElementById('lang-switcher');
    if (!mount) return;
    const current = SUPPORTED.find(l => l.code === currentLang) || SUPPORTED[0];
    mount.innerHTML = `
      <button class="lang-btn" id="lang-btn" type="button" aria-haspopup="listbox" aria-expanded="false" aria-label="${current.label}">
        <span class="lang-btn__flag">${current.flag}</span>
        <span class="lang-btn__text">${current.native}</span>
        <span class="lang-btn__caret">▾</span>
      </button>
      <ul class="lang-menu" id="lang-menu" role="listbox" hidden>
        ${SUPPORTED.map(l => `
          <li role="option" aria-selected="${l.code === currentLang}">
            <button type="button" class="lang-option${l.code === currentLang ? ' is-active' : ''}" data-lang="${l.code}">
              <span class="lang-option__flag">${l.flag}</span>
              <span class="lang-option__label"><b>${l.native}</b><small>${l.label}</small></span>
            </button>
          </li>`).join('')}
      </ul>`;

    const btn = document.getElementById('lang-btn');
    const menu = document.getElementById('lang-menu');
    if (!btn || !menu) return;
    btn.onclick = () => {
      const open = menu.hidden;
      menu.hidden = !open;
      btn.setAttribute('aria-expanded', String(open));
    };
    menu.querySelectorAll('[data-lang]').forEach(option => {
      option.onclick = async () => {
        const code = option.dataset.lang;
        closeLangMenu(menu, btn);
        if (code !== currentLang) await setLanguage(code);
      };
    });
    document.addEventListener('click', e => {
      if (!mount.contains(e.target)) closeLangMenu(menu, btn);
    }, { once: true });
  }

  async function setLanguage(code) {
    if (!SUPPORTED.some(l => l.code === code)) code = DEFAULT_LANG;
    currentLang = code;
    localStorage.setItem(STORAGE_KEY, code);
    setDocumentLang(code);
    if (!fallbackDict) fallbackDict = await loadLocale(DEFAULT_LANG);
    if (code !== DEFAULT_LANG) cache[code] = await loadLocale(code);
    applyTranslations();
    renderLangSwitcher();
    document.dispatchEvent(new CustomEvent('gwo:langchange', { detail: { lang: code } }));
  }

  window.GWO_I18N = {
    t(key) {
      const dict = currentLang === 'ko' ? fallbackDict : (cache[currentLang] || fallbackDict);
      return dict ? resolve(dict, key) : null;
    },
    getLang() { return currentLang; },
    isWorkerLang() { return currentLang !== 'ko'; },
    setLanguage,
    SUPPORTED
  };

  document.addEventListener('DOMContentLoaded', async () => {
    const saved = localStorage.getItem(STORAGE_KEY);
    currentLang = SUPPORTED.some(l => l.code === saved) ? saved : DEFAULT_LANG;
    try {
      fallbackDict = await loadLocale(DEFAULT_LANG);
      if (currentLang !== DEFAULT_LANG) cache[currentLang] = await loadLocale(currentLang);
      setDocumentLang(currentLang);
      applyTranslations();
      renderLangSwitcher();
    } catch (err) {
      console.warn('i18n load failed', err);
    }
  });
})();
