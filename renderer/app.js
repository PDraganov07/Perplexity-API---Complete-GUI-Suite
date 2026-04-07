const API = 'http://127.0.0.1:3000';

const $ = (id) => document.getElementById(id);

const TRANSLATIONS = {
  en: {
    app_title: "Perplexity — AI Search",
    sidebar_toggle: "Collapse sidebar",
    status_connecting: "Connecting…",
    status_offline: "Backend offline",
    status_online: "localhost:3000 · v",
    setting_model: "🤖 Model",
    setting_search_mode: "🔍 Search Mode",
    setting_research_effort: "🧠 Research Effort",
    setting_temperature: "🌡️ Temperature",
    setting_max_tokens: "✂️ Max Tokens",
    setting_recency: "📅 Recency Filter",
    setting_language: "🌐 Language",
    check_images: "📷 Return Images",
    check_videos: "🎥 Return Videos",
    check_related: "❓ Related Questions",
    check_history: "💬 Keep History",
    setting_system_prompt: "⚙️ System Prompt",
    setting_domain_filter: "🌐 Domain Filter",
    placeholder_max_tokens: "Default (no limit)",
    placeholder_system_prompt: "Optional system instructions…",
    placeholder_domain_filter: "arxiv.org, nature.com",
    btn_api_key: "🔑 API Key",
    btn_api_docs: "📚 API Docs",
    btn_export: "💾 Export Chat",
    btn_clear_history: "🗑️ Clear History",
    btn_new_chat: "✦ New Chat",
    new_chat_title: "New conversation",
    welcome_title: "Ask anything",
    welcome_sub: "AI-powered answers with cited sources",
    chip_breakthroughs: "🤖 AI breakthroughs 2026",
    chip_quantum: "⚛️ Quantum computing",
    chip_fusion: "🔥 Fusion energy",
    chip_languages: "💻 Top languages 2026",
    input_placeholder: "Ask anything… (Enter to send, Shift+Enter for newline)",
    input_hint: "Enter to send · Shift+Enter for new line",
    modal_api_title: "🔐 Connect API Key",
    modal_api_sub: "Encrypted with your machine ID and stored locally",
    btn_save: "Save Key",
    btn_cancel: "Cancel",
    btn_remove_key: "Remove saved key",
    searching: "Searching",
    error_api: "API error",
    error_network: "Network error",
    error_connect: "⚠️ Could not connect to Python backend",
    msg_you: "You",
    msg_perplexity: "Perplexity",
    related_qs: "Related questions",
    tokens: "Tokens",
    chat_exported: "Chat exported as Markdown ✓",
    nothing_export: "Nothing to export",
    new_chat_started: "New conversation started",
    history_cleared: "History cleared",
    enter_api_key: "Please enter an API key",
    api_key_saved: "API key saved & encrypted ✓",
    api_key_fail: "Failed to save key",
    api_key_removed: "API key removed",
    confirm_remove_key: "Remove saved API key?",
    confirm_key_format: "Key doesn't start with 'pplx-'. Continue anyway?",
    lang_en: "English",
    lang_bg: "Български",
    lang_ru: "Русский",
    lang_de: "Deutsch",
  },
  bg: {
    app_title: "Perplexity — AI търсене",
    sidebar_toggle: "Свиване на лентата",
    status_connecting: "Свързване…",
    status_offline: "Backend офлайн",
    status_online: "localhost:3000 · v",
    setting_model: "🤖 Модел",
    setting_search_mode: "🔍 Реж. търсене",
    setting_research_effort: "🧠 Проучване",
    setting_temperature: "🌡️ Температура",
    setting_max_tokens: "✂️ Макс. токени",
    setting_recency: "📅 Актуалност",
    setting_language: "🌐 Език",
    check_images: "📷 Изображения",
    check_videos: "🎥 Видеа",
    check_related: "❓ Свързани въпроси",
    check_history: "💬 История",
    setting_system_prompt: "⚙️ Промпт",
    setting_domain_filter: "🌐 Домейни",
    placeholder_max_tokens: "Без лимит",
    placeholder_system_prompt: "Инструкции…",
    placeholder_domain_filter: "arxiv.org, nature.com",
    btn_api_key: "🔑 API ключ",
    btn_api_docs: "📚 API документи",
    btn_export: "💾 Експорт",
    btn_clear_history: "🗑️ Изчистване",
    btn_new_chat: "✦ Нов чат",
    new_chat_title: "Нов разговор",
    welcome_title: "Попитай всичко",
    welcome_sub: "Отговори от AI с цитирани източници",
    chip_breakthroughs: "🤖 AI пробиви 2026",
    chip_quantum: "⚛️ Квантови компютри",
    chip_fusion: "🔥 Термоядрен синтез",
    chip_languages: "💻 Топ езици 2026",
    input_placeholder: "Попитай всичко… (Enter за пращане)",
    input_hint: "Enter за пращане · Shift+Enter за нов ред",
    modal_api_title: "🔐 API ключ",
    modal_api_sub: "Записан локално",
    btn_save: "Запазване",
    btn_cancel: "Отказ",
    btn_remove_key: "Изтриване",
    searching: "Търсене",
    error_api: "API грешка",
    error_network: "Мрежова грешка",
    error_connect: "⚠️ Няма връзка с Python",
    msg_you: "Вие",
    msg_perplexity: "Perplexity",
    related_qs: "Свързани въпроси",
    tokens: "Токени",
    chat_exported: "Експортирано ✓",
    nothing_export: "Няма за експорт",
    new_chat_started: "Нов разговор",
    history_cleared: "Изчистено",
    enter_api_key: "Въведете ключ",
    api_key_saved: "Запазено ✓",
    api_key_fail: "Грешка при запис",
    api_key_removed: "Ключът е изтрит",
    confirm_remove_key: "Изтриване на ключа?",
    confirm_key_format: "Невалиден формат. Продължаване?",
    lang_en: "English",
    lang_bg: "Български",
    lang_ru: "Русский",
    lang_de: "Deutsch",
  },
  ru: {
    app_title: "Perplexity — AI Поиск",
    sidebar_toggle: "Свернуть панель",
    status_connecting: "Подключение…",
    status_offline: "Backend офлайн",
    status_online: "localhost:3000 · v",
    setting_model: "🤖 Модель",
    setting_search_mode: "🔍 Поиск",
    setting_research_effort: "🧠 Анализ",
    setting_temperature: "🌡️ Температура",
    setting_max_tokens: "✂️ Макс. токенов",
    setting_recency: "📅 Актуальность",
    setting_language: "🌐 Язык",
    check_images: "📷 Картинки",
    check_videos: "🎥 Видео",
    check_related: "❓ Вопросы",
    check_history: "💬 История",
    setting_system_prompt: "⚙️ Промпт",
    setting_domain_filter: "🌐 Домены",
    placeholder_max_tokens: "Без лимита",
    placeholder_system_prompt: "Инструкции…",
    placeholder_domain_filter: "arxiv.org, nature.com",
    btn_api_key: "🔑 API ключ",
    btn_api_docs: "📚 Документация",
    btn_export: "💾 Экспорт",
    btn_clear_history: "🗑️ Очистить",
    btn_new_chat: "✦ Новый чат",
    new_chat_title: "Новый чат",
    welcome_title: "Спрашивайте",
    welcome_sub: "Ответы AI с цитатами",
    chip_breakthroughs: "🤖 AI 2026",
    chip_quantum: "⚛️ Кванты",
    chip_fusion: "🔥 Синтез",
    chip_languages: "💻 Языки 2026",
    input_placeholder: "Спрашивайте… (Enter)",
    input_hint: "Enter - отправить · Shift+Enter - переход",
    modal_api_title: "🔐 API ключ",
    modal_api_sub: "Хранится локально",
    btn_save: "Сохранить",
    btn_cancel: "Отмена",
    btn_remove_key: "Удалить",
    searching: "Поиск",
    error_api: "Ошибка API",
    error_network: "Ошибка сети",
    error_connect: "⚠️ Ошибка связи с Python",
    msg_you: "Вы",
    msg_perplexity: "Perplexity",
    related_qs: "Вопросы",
    tokens: "Токены",
    chat_exported: "Экспорт завершен ✓",
    nothing_export: "Нечего экспортировать",
    new_chat_started: "Начат новый чат",
    history_cleared: "История очищена",
    enter_api_key: "Введите API ключ",
    api_key_saved: "Ключ сохранен ✓",
    api_key_fail: "Ошибка записи",
    api_key_removed: "Ключ удален",
    confirm_remove_key: "Удалить API ключ?",
    confirm_key_format: "Неверный формат. Продолжить?",
    lang_en: "English",
    lang_bg: "Български",
    lang_ru: "Русский",
    lang_de: "Deutsch",
  },
  de: {
    app_title: "Perplexity — AI Suche",
    sidebar_toggle: "Sidebar einklappen",
    status_connecting: "Verbinden…",
    status_offline: "Backend offline",
    status_online: "localhost:3000 · v",
    setting_model: "🤖 Modell",
    setting_search_mode: "🔍 Suche",
    setting_research_effort: "🧠 Forschung",
    setting_temperature: "🌡️ Temperatur",
    setting_max_tokens: "✂️ Max. Tokens",
    setting_recency: "📅 Aktualität",
    setting_language: "🌐 Sprache",
    check_images: "📷 Bilder",
    check_videos: "🎥 Videos",
    check_related: "❓ Fragen",
    check_history: "💬 Verlauf",
    setting_system_prompt: "⚙️ Prompt",
    setting_domain_filter: "🌐 Domains",
    placeholder_max_tokens: "Ohne Limit",
    placeholder_system_prompt: "Anweisungen…",
    placeholder_domain_filter: "arxiv.org, nature.com",
    btn_api_key: "🔑 API-Key",
    btn_api_docs: "📚 Dokumentation",
    btn_export: "💾 Export",
    btn_clear_history: "🗑️ Löschen",
    btn_new_chat: "✦ Neuer Chat",
    new_chat_title: "Neuer Chat",
    welcome_title: "Frag alles",
    welcome_sub: "KI-Antworten mit Quellen",
    chip_breakthroughs: "🤖 KI 2026",
    chip_quantum: "⚛️ Quanten",
    chip_fusion: "🔥 Fusion",
    chip_languages: "💻 Sprachen 2026",
    input_placeholder: "Frag alles… (Enter)",
    input_hint: "Enter zum Senden · Shift+Enter für Umbruch",
    modal_api_title: "🔐 API-Key",
    modal_api_sub: "Lokal verschlüsselt gespeichert",
    btn_save: "Speichern",
    btn_cancel: "Abbrechen",
    btn_remove_key: "Entfernen",
    searching: "Suche läuft",
    error_api: "API-Fehler",
    error_network: "Netzwerkfehler",
    error_connect: "⚠️ Keine Verbindung zum Backend",
    msg_you: "Du",
    msg_perplexity: "Perplexity",
    related_qs: "Fragen",
    tokens: "Tokens",
    chat_exported: "Exportiert ✓",
    nothing_export: "Nichts zu exportieren",
    new_chat_started: "Neuer Chat",
    history_cleared: "Gelöscht",
    enter_api_key: "Key eingeben",
    api_key_saved: "Gespeichert ✓",
    api_key_fail: "Fehler",
    api_key_removed: "Entfernt",
    confirm_remove_key: "Key entfernen?",
    confirm_key_format: "Falsches Format. Fortfahren?",
    lang_en: "English",
    lang_bg: "Български",
    lang_ru: "Русский",
    lang_de: "Deutsch",
  }
};

let currentLang = localStorage.getItem('appLang') || 'en';

function i18n(key) {
  return TRANSLATIONS[currentLang] && TRANSLATIONS[currentLang][key] || TRANSLATIONS['en'][key] || key;
}

function updateUI() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    el.textContent = i18n(key);
  });
  document.querySelectorAll('[data-i18n-title]').forEach(el => {
    const key = el.getAttribute('data-i18n-title');
    el.title = i18n(key);
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    el.placeholder = i18n(key);
  });

  const flag = $('currentLangFlag');
  if (flag) {
    flag.className = `flag-icon flag-${currentLang}`;
  }
  const name = $('currentLangName');
  if (name) {
    name.textContent = i18n(`lang_${currentLang}`);
  }
  document.title = i18n('app_title');
}

function setLanguage(lang) {
  if (!TRANSLATIONS[lang]) return;
  console.log('Setting language to:', lang);
  currentLang = lang;
  localStorage.setItem('appLang', lang);
  updateUI();
  const lp = $('langPicker');
  if (lp) lp.classList.remove('open');
}

const statusDot        = $('statusDot');
const statusText       = $('statusText');
const chatWrap         = $('chatWrap');
const messagesEl       = $('messages');
const welcomeScreen    = $('welcomeScreen');
const chatInput        = $('chatInput');
const sendBtn          = $('sendBtn');
const currentModelBadge= $('currentModelBadge');

const modelSelect      = $('modelSelect');
const searchModeSelect = $('searchModeSelect');
const researchEffort   = $('researchEffort');
const tempSlider       = $('tempSlider');
const tempVal          = $('tempVal');
const maxTokensInput   = $('maxTokens');
const recencyFilter    = $('recencyFilter');
const languageSelect   = $('languageSelect');
const chkImages        = $('chkImages');
const chkVideos        = $('chkVideos');
const chkRelated       = $('chkRelated');
const chkHistory       = $('chkHistory');
const systemPrompt     = $('systemPrompt');
const domainFilter     = $('domainFilter');

const sidebarToggle    = $('sidebarToggle');
const sidebar          = $('sidebar');

const apiKeyModal      = $('apiKeyModal');
const apiKeyInput      = $('apiKeyInput');
const docsModal        = $('docsModal');

const toastEl          = $('toast');

let isThinking   = false;
let hasMessages  = false;
let toastTimer   = null;

function showToast(msg, type = 'info', duration = 3000) {
  if (!toastEl) return;
  toastEl.textContent = msg;
  toastEl.className   = `toast show ${type}`;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { toastEl.className = 'toast'; }, duration);
}

function openModal(el)  { if (el) el.classList.add('open'); }
function closeModal(el) { if (el) el.classList.remove('open'); }

if (sidebarToggle) {
  sidebarToggle.addEventListener('click', () => {
    const collapsed = sidebar.classList.toggle('collapsed');
    sidebarToggle.textContent = collapsed ? '›' : '‹';
  });
}

if (tempSlider) {
  tempSlider.addEventListener('input', () => {
    const v = parseFloat(tempSlider.value);
    if (tempVal) tempVal.textContent = v.toFixed(1);
    const pct = (v / 2) * 100;
    tempSlider.style.setProperty('--pct', pct + '%');
  });
  const v = parseFloat(tempSlider.value);
  tempSlider.style.setProperty('--pct', (v/2*100)+'%');
}

if (modelSelect) {
  modelSelect.addEventListener('change', () => {
    if (currentModelBadge) currentModelBadge.textContent = modelSelect.value;
  });
}

const langBtn = $('langBtn');
if (langBtn) {
  langBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    $('langPicker').classList.toggle('open');
  });
}

document.addEventListener('click', (e) => {
  const lp = $('langPicker');
  if (lp && !lp.contains(e.target)) {
    lp.classList.remove('open');
  }
});

function attachLangListeners() {
  document.querySelectorAll('.lang-opt').forEach(opt => {
    opt.onclick = (e) => {
      e.preventDefault();
      e.stopPropagation();
      const lang = opt.getAttribute('data-lang');
      setLanguage(lang);
    };
  });
}

async function boot() {
  updateUI();
  attachLangListeners();
  try {
    const [healthRes, modelsRes] = await Promise.all([
      fetch(`${API}/api/health`),
      fetch(`${API}/api/models`),
    ]);

    if (healthRes.ok) {
      const h = await healthRes.json();
      if (statusDot) statusDot.className  = 'status-dot ok';
      if (statusText) statusText.textContent = `${i18n('status_online')}${h.version}`;
      const av = $('appVersion');
      if (av) av.textContent = `v${h.version}`;
      const vh = $('versionHint');
      if (vh) vh.textContent = h.version;

      if (!h.has_key) {
        setTimeout(() => openModal(apiKeyModal), 800);
      }
    }

    if (modelsRes.ok) {
      const d = await modelsRes.json();
      if (modelSelect) populateSelect(modelSelect, d.models, 'sonar-pro');
      if (languageSelect) populateSelect(languageSelect, d.languages, 'none');
    }
  } catch {
    if (statusDot) statusDot.className = 'status-dot err';
    if (statusText) statusText.textContent = i18n('status_offline');
    showToast(i18n('error_connect'), 'error', 6000);
  }
}

function populateSelect(sel, options, defaultVal) {
  if (!sel) return;
  sel.innerHTML = '';
  options.forEach(opt => {
    const o = document.createElement('option');
    o.value = opt; o.textContent = opt;
    if (opt === defaultVal) o.selected = true;
    sel.appendChild(o);
  });
  if (sel === modelSelect && currentModelBadge) currentModelBadge.textContent = sel.value;
}

async function sendMessage(promptOverride) {
  if (isThinking) return;

  const prompt = (promptOverride || chatInput.value).trim();
  if (!prompt) return;

  if (!hasMessages) {
    if (welcomeScreen) welcomeScreen.style.display = 'none';
    hasMessages = true;
  }

  if (chatInput) chatInput.value = '';
  resizeTextarea();

  appendUserMessage(prompt);

  const thinkingEl = appendThinking();

  isThinking = true;
  if (sendBtn) sendBtn.disabled = true;

  const body = {
    prompt,
    model:                   modelSelect ? modelSelect.value : 'sonar-pro',
    search_mode:             searchModeSelect ? searchModeSelect.value : 'web',
    research_effort:         researchEffort ? researchEffort.value : 'medium',
    temperature:             tempSlider ? parseFloat(tempSlider.value) : 0.7,
    return_images:           chkImages ? chkImages.checked : false,
    return_videos:           chkVideos ? chkVideos.checked : false,
    return_related_questions: chkRelated ? chkRelated.checked : false,
    use_conversation_history: chkHistory ? chkHistory.checked : false,
  };

  if (systemPrompt && systemPrompt.value.trim()) body.system_prompt = systemPrompt.value.trim();
  if (maxTokensInput && parseInt(maxTokensInput.value) > 0) body.max_tokens = parseInt(maxTokensInput.value);
  if (recencyFilter && recencyFilter.value !== 'none') body.search_recency_filter = recencyFilter.value;
  if (languageSelect && languageSelect.value !== 'none') body.language = languageSelect.value;
  if (domainFilter && domainFilter.value.trim()) body.search_domain_filter = domainFilter.value.trim().split(',').map(d => d.trim()).filter(Boolean);

  try {
    const res  = await fetch(`${API}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    if (thinkingEl) thinkingEl.remove();

    if (!res.ok) {
      const err = await res.json().catch(() => ({ error: res.statusText }));
      appendError(err.error || i18n('error_api'));
    } else {
      const data = await res.json();
      appendAIMessage(data);
    }
  } catch (e) {
    if (thinkingEl) thinkingEl.remove();
    appendError(e.message || i18n('error_network'));
  } finally {
    isThinking       = false;
    if (sendBtn) sendBtn.disabled = false;
    if (chatInput) chatInput.focus();
  }
}

function appendUserMessage(text) {
  const row = document.createElement('div');
  row.className = 'message-row';
  row.innerHTML = `
    <div class="msg-header">
      <div class="msg-avatar user">👤</div>
      <span class="msg-role">${i18n('msg_you')}</span>
      <span class="msg-time">${now()}</span>
    </div>
    <div class="msg-body">${escapeHtml(text)}</div>
  `;
  if (messagesEl) messagesEl.appendChild(row);
  scrollToBottom();
}

function appendAIMessage(data) {
  const choice  = data.choices?.[0];
  const content = choice?.message?.content || '(empty response)';
  const citations   = data.citations   || [];
  const images      = data.images      || [];
  const relatedQs   = data.related_questions || choice?.message?.related_questions || [];
  const usage       = data.usage || {};

  const row = document.createElement('div');
  row.className = 'message-row';

  const html = marked.parse(content);

  let inner = `
    <div class="msg-header">
      <div class="msg-avatar ai">⚡</div>
      <span class="msg-role">${i18n('msg_perplexity')}</span>
      <span class="msg-time">${now()}</span>
    </div>
    <div class="msg-body">${html}</div>
  `;

  if (citations.length) {
    inner += `<div class="citations">`;
    citations.forEach((url, i) => {
      const domain = safeDomain(url);
      inner += `
        <a class="citation-chip" href="#" data-url="${url}" title="${url}">
          <span class="citation-num">${i + 1}</span>${domain}
        </a>`;
    });
    inner += `</div>`;
  }

  if (images.length) {
    inner += `<div class="citations">`;
    images.forEach(img => {
      const imgUrl = typeof img === 'string' ? img : img.url || '';
      if (imgUrl) inner += `<a class="citation-chip" href="#" data-url="${imgUrl}">🖼️ Image</a>`;
    });
    inner += `</div>`;
  }

  if (relatedQs.length) {
    inner += `
      <div class="related-questions">
        <div class="related-label">${i18n('related_qs')}</div>
        <div class="related-list">
          ${relatedQs.map(q => `<button class="related-chip" data-q="${escapeAttr(q)}">${escapeHtml(q)}</button>`).join('')}
        </div>
      </div>`;
  }

  if (usage.total_tokens) {
    inner += `
      <div class="usage-bar">
        <span class="usage-text">${i18n('tokens')}</span>
        <span class="usage-badge">prompt: ${usage.prompt_tokens ?? '–'}</span>
        <span class="usage-badge">completion: ${usage.completion_tokens ?? '–'}</span>
        <span class="usage-badge">total: ${usage.total_tokens}</span>
      </div>`;
  }

  row.innerHTML = inner;

  row.querySelectorAll('[data-url]').forEach(el => {
    el.addEventListener('click', e => {
      e.preventDefault();
      const url = el.dataset.url;
      if (window.electronAPI) window.electronAPI.openExternal(url);
      else window.open(url, '_blank');
    });
  });

  row.querySelectorAll('.related-chip').forEach(btn => {
    btn.addEventListener('click', () => sendMessage(btn.dataset.q));
  });

  if (messagesEl) messagesEl.appendChild(row);
  scrollToBottom();
}

function appendThinking() {
  if (!messagesEl) return null;
  const el = document.createElement('div');
  el.className = 'thinking';
  el.innerHTML = `
    <div class="msg-avatar ai" style="width:28px;height:28px;border-radius:8px;background:var(--accent-dim);display:flex;align-items:center;justify-content:center;font-size:14px;">⚡</div>
    <span>${i18n('searching')}</span>
    <div class="thinking-dots"><span></span><span></span><span></span></div>
  `;
  messagesEl.appendChild(el);
  scrollToBottom();
  return el;
}

function appendError(msg) {
  const el = document.createElement('div');
  el.className = 'error-row';
  el.textContent = `⚠️  ${msg}`;
  if (messagesEl) messagesEl.appendChild(el);
  scrollToBottom();
  showToast(msg, 'error');
}

function now() {
  return new Date().toLocaleTimeString([], { hour:'2-digit', minute:'2-digit' });
}

function escapeHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function escapeAttr(s) {
  return s.replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}

function safeDomain(url) {
  try { return new URL(url).hostname.replace('www.',''); }
  catch { return url.slice(0, 30); }
}

function scrollToBottom() {
  if (chatWrap) chatWrap.scrollTop = chatWrap.scrollHeight;
}

function resizeTextarea() {
  if (chatInput) {
    chatInput.style.height = 'auto';
    chatInput.style.height = Math.min(chatInput.scrollHeight, 200) + 'px';
  }
}

if (chatInput) {
  chatInput.addEventListener('input', resizeTextarea);
  chatInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
}

if (sendBtn) sendBtn.addEventListener('click', () => sendMessage());

document.querySelectorAll('.chip').forEach(chip => {
  chip.addEventListener('click', () => sendMessage(chip.dataset.q));
});

const bnc = $('btnNewChat');
if (bnc) {
  bnc.addEventListener('click', async () => {
    await fetch(`${API}/api/history/clear`, { method: 'POST' }).catch(() => {});
    if (messagesEl) messagesEl.innerHTML  = '';
    if (welcomeScreen) welcomeScreen.style.display = '';
    hasMessages = false;
    showToast(i18n('new_chat_started'), 'success');
  });
}

const bch = $('btnClearHistory');
if (bch) {
  bch.addEventListener('click', async () => {
    await fetch(`${API}/api/history/clear`, { method: 'POST' }).catch(() => {});
    if (messagesEl) messagesEl.innerHTML = '';
    if (welcomeScreen) welcomeScreen.style.display = '';
    hasMessages = false;
    showToast(i18n('history_cleared'), 'success');
  });
}

const bex = $('btnExport');
if (bex) {
  bex.addEventListener('click', () => {
    if (!messagesEl) return;
    const rows = messagesEl.querySelectorAll('.message-row');
    if (!rows.length) { showToast(i18n('nothing_export'), 'error'); return; }

    let md = `# Perplexity Chat Export\n_${new Date().toLocaleString()}_\n\n---\n\n`;
    rows.forEach(row => {
      const role = row.querySelector('.msg-role')?.textContent || '';
      const body = row.querySelector('.msg-body')?.innerText || '';
      md += `**${role}**\n\n${body}\n\n---\n\n`;
    });

    const blob = new Blob([md], { type: 'text/markdown' });
    const a    = document.createElement('a');
    a.href     = URL.createObjectURL(blob);
    a.download = `perplexity_${Date.now()}.md`;
    a.click();
    showToast(i18n('chat_exported'), 'success');
  });
}

const bak = $('btnApiKey');
if (bak) bak.addEventListener('click', () => openModal(apiKeyModal));
const akc = $('apiKeyCancel');
if (akc) akc.addEventListener('click', () => closeModal(apiKeyModal));

if (apiKeyModal) {
  apiKeyModal.addEventListener('click', e => {
    if (e.target === apiKeyModal) closeModal(apiKeyModal);
  });
}

const aks = $('apiKeySave');
if (aks) {
  aks.addEventListener('click', async () => {
    if (!apiKeyInput) return;
    const key = apiKeyInput.value.trim();
    if (!key) { showToast(i18n('enter_api_key'), 'error'); return; }

    if (!key.startsWith('pplx-')) {
      const ok = confirm(i18n('confirm_key_format'));
      if (!ok) return;
    }

    try {
      const res = await fetch(`${API}/api/config/key`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ api_key: key }),
      });
      if (res.ok) {
        showToast(i18n('api_key_saved'), 'success');
        if (statusDot) statusDot.className = 'status-dot ok';
        apiKeyInput.value = '';
        closeModal(apiKeyModal);
      } else {
        const e = await res.json();
        showToast(e.error || i18n('api_key_fail'), 'error');
      }
    } catch { showToast(i18n('status_offline'), 'error'); }
  });
}

const akd = $('apiKeyDelete');
if (akd) {
  akd.addEventListener('click', async () => {
    const ok = confirm(i18n('confirm_remove_key'));
    if (!ok) return;
    await fetch(`${API}/api/config/key`, { method: 'DELETE' }).catch(() => {});
    showToast(i18n('api_key_removed'), 'success');
    closeModal(apiKeyModal);
  });
}

const bdc = $('btnDocs');
if (bdc) {
  bdc.addEventListener('click', () => {
    const db = $('docsBody');
    if (db) db.innerHTML = buildDocs();
    openModal(docsModal);
  });
}

const dcl = $('docsClose');
if (dcl) dcl.addEventListener('click', () => closeModal(docsModal));

if (docsModal) {
  docsModal.addEventListener('click', e => { if (e.target === docsModal) closeModal(docsModal); });
}

function buildDocs() {
  return `
    <div class="docs-section">
      <h3>🌐 Base URL</h3>
      <pre>http://localhost:3000</pre>
    </div>
    <div class="docs-section">
      <h3>GET /api/health</h3>
      <pre>curl http://localhost:3000/api/health</pre>
    </div>
  `;
}

boot();
if (chatInput) chatInput.focus();
