(() => {
  "use strict";

  const STORAGE_KEY = "wortkarte.progress.v1";
  const DELETED_KEY = "wortkarte.deleted.v1";
  const CUSTOM_KEY = "wortkarte.custom.v1";
  const PREFS_KEY = "wortkarte.prefs.v1";
  const STATUS_ORDER = ["forgot", "difficult", "easy", "instant"];
  const ALL_STATUSES = ["new", "forgot", "difficult", "easy", "instant"];
  const STATUS_LABELS = {
    forgot: "Vergessen",
    difficult: "Schwer",
    easy: "Leicht",
    instant: "Sofort",
    new: "Neu",
    none: "Neu",
  };
  const DIRECTION_LABELS = {
    "de-en": "Deutsch → Englisch",
    "en-de": "Englisch → Deutsch",
    mixed: "Gemischt",
  };

  const state = {
    view: "home",
    cards: [],
    studyQueue: [],
    studyIndex: 0,
    sessionTotal: 0,
    sessionRated: 0,
    flipped: false,
    selectedIds: new Set(),
    browseFilters: new Set(ALL_STATUSES),
    studyStatuses: new Set(["new", "forgot", "difficult"]),
    studyDirection: "de-en",
    lastError: null,
    browseNotice: "",
  };

  const els = {
    main: document.getElementById("main"),
    brandBtn: document.getElementById("brand-btn"),
    navButtons: Array.from(document.querySelectorAll(".nav-btn")),
  };

  function safeParse(json, fallback) {
    try {
      const value = JSON.parse(json);
      return value ?? fallback;
    } catch {
      return fallback;
    }
  }

  function loadPrefs() {
    const prefs = safeParse(localStorage.getItem(PREFS_KEY), {});
    if (prefs && typeof prefs === "object") {
      if (["de-en", "en-de", "mixed"].includes(prefs.studyDirection)) {
        state.studyDirection = prefs.studyDirection;
      }
      if (Array.isArray(prefs.studyStatuses) && prefs.studyStatuses.length) {
        state.studyStatuses = new Set(prefs.studyStatuses.filter((s) => ALL_STATUSES.includes(s)));
      }
      if (Array.isArray(prefs.browseFilters) && prefs.browseFilters.length) {
        state.browseFilters = new Set(prefs.browseFilters.filter((s) => ALL_STATUSES.includes(s)));
      }
    }
  }

  function savePrefs() {
    localStorage.setItem(
      PREFS_KEY,
      JSON.stringify({
        studyDirection: state.studyDirection,
        studyStatuses: [...state.studyStatuses],
        browseFilters: [...state.browseFilters],
      })
    );
  }

  function loadProgress() {
    return safeParse(localStorage.getItem(STORAGE_KEY), {});
  }

  function saveProgress(progress) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  }

  function loadDeleted() {
    const deleted = safeParse(localStorage.getItem(DELETED_KEY), []);
    return new Set(Array.isArray(deleted) ? deleted : []);
  }

  function saveDeleted(deletedSet) {
    localStorage.setItem(DELETED_KEY, JSON.stringify([...deletedSet]));
  }

  function loadCustomWords() {
    const custom = safeParse(localStorage.getItem(CUSTOM_KEY), []);
    return Array.isArray(custom) ? custom : [];
  }

  function saveCustomWords(words) {
    localStorage.setItem(CUSTOM_KEY, JSON.stringify(words));
  }

  function slugify(text) {
    return String(text)
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/ß/g, "ss")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 60) || `word-${Date.now()}`;
  }

  function normalizeWord(word, fallbackId) {
    if (!word || typeof word !== "object") return null;
    const german = String(word.german || word.de || word.front || "").trim();
    const english = String(word.english || word.en || word.back || word.definition || "").trim();
    if (!german || !english) return null;
    const id = String(word.id || fallbackId || slugify(german));
    return {
      id,
      german,
      english,
      exampleDe: String(word.exampleDe || word.example_de || word.example || german).trim(),
      exampleEn: String(word.exampleEn || word.example_en || english).trim(),
      custom: Boolean(word.custom || fallbackId),
    };
  }

  function normalizeSeedWords() {
    const seeds = Array.isArray(window.SEED_WORDS) ? window.SEED_WORDS : [];
    return seeds.map((word) => normalizeWord(word)).filter(Boolean);
  }

  function cardStatusKey(card) {
    return card.status || "new";
  }

  function buildCards() {
    const progress = loadProgress();
    const deleted = loadDeleted();
    const seeds = normalizeSeedWords();
    const custom = loadCustomWords()
      .map((word) => normalizeWord({ ...word, custom: true }))
      .filter(Boolean);

    const byId = new Map();
    [...seeds, ...custom].forEach((word) => {
      if (deleted.has(word.id)) return;
      byId.set(word.id, word);
    });

    return [...byId.values()]
      .map((word) => {
        const saved = progress[word.id] || {};
        const status = STATUS_ORDER.includes(saved.status) ? saved.status : null;
        return {
          ...word,
          status,
          lastReviewedAt: typeof saved.lastReviewedAt === "number" ? saved.lastReviewedAt : null,
        };
      })
      .sort((a, b) => a.german.localeCompare(b.german, "de", { sensitivity: "base" }));
  }

  function refreshCards() {
    state.cards = buildCards();
  }

  function setCardStatus(cardId, status) {
    const progress = loadProgress();
    progress[cardId] = {
      status,
      lastReviewedAt: Date.now(),
    };
    saveProgress(progress);
    refreshCards();
  }

  function upsertCustomWords(entries) {
    const custom = loadCustomWords();
    const byId = new Map(custom.map((word) => [word.id, word]));
    const normalizedEntries = [];
    let added = 0;
    let updated = 0;

    entries.forEach((entry) => {
      const normalized = normalizeWord({ ...entry, custom: true });
      if (!normalized) return;
      normalizedEntries.push(normalized);
      if (byId.has(normalized.id)) updated += 1;
      else added += 1;
      byId.set(normalized.id, normalized);
    });

    saveCustomWords([...byId.values()]);

    const deleted = loadDeleted();
    let restored = 0;
    normalizedEntries.forEach((entry) => {
      if (deleted.has(entry.id)) {
        deleted.delete(entry.id);
        restored += 1;
      }
    });
    if (restored) saveDeleted(deleted);

    refreshCards();
    return { added, updated, restored };
  }

  function deleteCards(ids) {
    if (!ids.length) return;
    const deleted = loadDeleted();
    const progress = loadProgress();
    const custom = loadCustomWords();
    const customIds = new Set(custom.map((word) => word.id));

    ids.forEach((id) => {
      if (customIds.has(id)) return;
      deleted.add(id);
      delete progress[id];
    });

    saveCustomWords(custom.filter((word) => !ids.includes(word.id)));
    saveDeleted(deleted);
    saveProgress(progress);
    ids.forEach((id) => state.selectedIds.delete(id));
    refreshCards();
  }

  function parseImportText(raw) {
    const text = String(raw || "").trim();
    if (!text) return [];

    if (text.startsWith("[") || text.startsWith("{")) {
      const parsed = safeParse(text, null);
      const list = Array.isArray(parsed)
        ? parsed
        : Array.isArray(parsed && parsed.words)
          ? parsed.words
          : [];
      return list.map((item) => normalizeWord(item)).filter(Boolean);
    }

    return text
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter((line) => line && !line.startsWith("#"))
      .map((line) => {
        const parts = line.split(/\s+[–—\-:]\s+|\t+/);
        if (parts.length < 2) return null;
        const german = parts[0].trim();
        const english = parts.slice(1).join(" - ").trim();
        return normalizeWord({ german, english, custom: true });
      })
      .filter(Boolean);
  }

  function shuffle(items) {
    const copy = [...items];
    for (let i = copy.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
  }

  function studyPriority(statusKey) {
    if (statusKey === "forgot") return 0;
    if (statusKey === "difficult") return 1;
    if (statusKey === "new") return 2;
    if (statusKey === "easy") return 3;
    return 4;
  }

  function pickDirection() {
    if (state.studyDirection === "mixed") {
      return Math.random() < 0.5 ? "de-en" : "en-de";
    }
    return state.studyDirection;
  }

  function cardsForStudy() {
    return state.cards.filter((card) => state.studyStatuses.has(cardStatusKey(card)));
  }

  function buildStudyQueue() {
    const filtered = cardsForStudy();
    const prioritized = [...filtered].sort((a, b) => {
      const diff = studyPriority(cardStatusKey(a)) - studyPriority(cardStatusKey(b));
      if (diff !== 0) return diff;
      return (a.lastReviewedAt || 0) - (b.lastReviewedAt || 0);
    });

    const bands = [[], [], [], [], []];
    prioritized.forEach((card) => {
      bands[studyPriority(cardStatusKey(card))].push(card);
    });

    return bands.flatMap((band) =>
      shuffle(band).map((card) => ({
        ...card,
        direction: pickDirection(),
      }))
    );
  }

  function currentStudyCard() {
    if (!state.studyQueue.length) return null;
    if (state.studyIndex < 0 || state.studyIndex >= state.studyQueue.length) return null;
    return state.studyQueue[state.studyIndex] || null;
  }

  function startStudySession() {
    refreshCards();
    state.studyQueue = buildStudyQueue();
    state.studyIndex = 0;
    state.sessionTotal = state.studyQueue.length;
    state.sessionRated = 0;
    state.flipped = false;
    state.lastError = null;
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  function statusClass(status) {
    return status ? `status-${status}` : "status-none";
  }

  function statusLabel(status) {
    return STATUS_LABELS[status || "new"];
  }

  function setActiveNav(view) {
    els.navButtons.forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.view === view);
    });
  }

  function renderFilterChips(selectedSet, actionPrefix, options = ALL_STATUSES) {
    return options
      .map((key) => {
        const active = selectedSet.has(key) ? "is-active" : "";
        return `
          <button
            type="button"
            class="filter-chip ${active}"
            data-action="${actionPrefix}"
            data-status="${key}"
          >${escapeHtml(STATUS_LABELS[key])}</button>
        `;
      })
      .join("");
  }

  function renderHome() {
    const count = Array.isArray(window.SEED_WORDS) ? window.SEED_WORDS.length : state.cards.length;
    return `
      <section class="panel hero">
        <h1 class="hero-brand">Wortkarte</h1>
        <p class="hero-lead">
          Lerne deutsche Wörter mit Karteikarten, bewerte dein Wissen und behalte den Überblick unter Wörter.
        </p>
        <p class="meta-text">Kartenstapel: ${count} Wörter</p>
        <div class="cta-row">
          <button type="button" class="btn btn-primary" data-action="go-study">Lernen starten</button>
          <button type="button" class="btn btn-secondary" data-action="go-browse">Wörter ansehen</button>
        </div>
      </section>
    `;
  }

  function renderStudy() {
    const total = state.sessionTotal;
    const card = currentStudyCard();

    const controls = `
      <div class="study-controls">
        <div class="control-block">
          <p class="control-label">Richtung</p>
          <div class="chip-row">
            ${["de-en", "en-de", "mixed"]
              .map(
                (dir) => `
              <button
                type="button"
                class="filter-chip ${state.studyDirection === dir ? "is-active" : ""}"
                data-action="set-direction"
                data-direction="${dir}"
              >${escapeHtml(DIRECTION_LABELS[dir])}</button>`
              )
              .join("")}
          </div>
        </div>
        <div class="control-block">
          <p class="control-label">Welche Wörter?</p>
          <div class="chip-row">
            ${renderFilterChips(state.studyStatuses, "toggle-study-status")}
          </div>
          <button type="button" class="btn btn-secondary btn-small" data-action="restart-study">Sitzung starten / neu mischen</button>
        </div>
      </div>
    `;

    if (!state.studyStatuses.size) {
      return `
        <section class="panel study-shell">
          ${controls}
          <div class="empty-state">
            <h2>Keine Filter gewählt</h2>
            <p>Wähle mindestens einen Status (z. B. Neu, Vergessen, Schwer).</p>
          </div>
        </section>
      `;
    }

    if (!total) {
      return `
        <section class="panel study-shell">
          ${controls}
          <div class="empty-state">
            <h2>Keine Karten für diese Auswahl</h2>
            <p>Es gibt keine Wörter mit den gewählten Statusfiltern. Passe die Auswahl an oder füge Wörter hinzu.</p>
            <button type="button" class="btn btn-secondary" data-action="go-browse">Zu Wörter</button>
          </div>
        </section>
      `;
    }

    if (!card) {
      if (state.sessionRated >= state.sessionTotal && state.sessionTotal > 0) {
        return `
          <section class="panel study-shell">
            ${controls}
            <div class="empty-state">
              <h2>Sitzung fertig</h2>
              <p>Du hast ${state.sessionRated} / ${state.sessionTotal} Karten bewertet.</p>
              <button type="button" class="btn btn-primary" data-action="restart-study">Nochmal lernen</button>
            </div>
          </section>
        `;
      }
      state.studyIndex = 0;
      state.flipped = false;
      const recovered = currentStudyCard();
      if (!recovered) {
        return `
          <section class="panel error-state">
            <h2>Karte konnte nicht geladen werden</h2>
            <p>Beim Laden der nächsten Karte ist etwas schiefgelaufen.</p>
            <div class="cta-row">
              <button type="button" class="btn btn-primary" data-action="restart-study">Lernen neu laden</button>
              <button type="button" class="btn btn-secondary" data-action="go-home">Zurück</button>
            </div>
          </section>
        `;
      }
    }

    const active = currentStudyCard();
    const progressLabel = `${Math.min(state.sessionRated + 1, Math.max(state.sessionTotal, 1))} / ${state.sessionTotal}`;
    const flipClass = state.flipped ? "is-flipped" : "";
    const direction = active.direction || "de-en";
    const frontLabel = direction === "en-de" ? "Englisch" : "Deutsch";
    const backLabel = direction === "en-de" ? "Deutsch" : "Bedeutung";
    const frontText = direction === "en-de" ? active.english : active.german;
    const backMeaning = direction === "en-de" ? active.german : active.english;

    return `
      <section class="panel study-shell">
        <div class="study-meta">
          <p class="meta-text">Karte ${escapeHtml(progressLabel)}</p>
          <p class="meta-text">${escapeHtml(DIRECTION_LABELS[direction === "mixed" ? state.studyDirection : direction])}</p>
        </div>

        ${controls}

        <button
          type="button"
          class="flashcard ${flipClass}"
          data-action="flip-card"
          aria-label="Karteikarte umdrehen"
        >
          <div class="flashcard-inner">
            <div class="face face-front">
              <p class="face-label">${escapeHtml(frontLabel)}</p>
              <h2 class="face-word">${escapeHtml(frontText)}</h2>
            </div>
            <div class="face face-back">
              <p class="face-label">${escapeHtml(backLabel)}</p>
              <p class="face-meaning">${escapeHtml(backMeaning)}</p>
              <div class="face-example">
                <strong>${escapeHtml(active.exampleDe)}</strong>
                <span>${escapeHtml(active.exampleEn)}</span>
              </div>
            </div>
          </div>
        </button>

        <p class="hint">${
          state.flipped
            ? "Bewerte diese Karte, um weiterzumachen"
            : "Tippe auf die Karte, um die Antwort zu sehen"
        }</p>

        <div class="rating-row" ${state.flipped ? "" : "hidden"}>
          <button type="button" class="rate-btn rate-forgot" data-action="rate" data-status="forgot">Vergessen</button>
          <button type="button" class="rate-btn rate-difficult" data-action="rate" data-status="difficult">Schwer</button>
          <button type="button" class="rate-btn rate-easy" data-action="rate" data-status="easy">Leicht</button>
          <button type="button" class="rate-btn rate-instant" data-action="rate" data-status="instant">Sofort</button>
        </div>
      </section>
    `;
  }

  function filteredBrowseCards() {
    return state.cards.filter((card) => state.browseFilters.has(cardStatusKey(card)));
  }

  function renderBrowse() {
    const visible = filteredBrowseCards();
    const selectedCount = [...state.selectedIds].filter((id) =>
      visible.some((card) => card.id === id)
    ).length;

    const notice = state.browseNotice
      ? `<p class="browse-notice" role="status">${escapeHtml(state.browseNotice)}</p>`
      : "";

    const rows = visible
      .map((card, index) => {
        const checked = state.selectedIds.has(card.id) ? "checked" : "";
        const selectedClass = state.selectedIds.has(card.id) ? "is-selected" : "";
        return `
          <li class="word-item ${selectedClass}" style="animation-delay: ${Math.min(index, 12) * 25}ms">
            <input
              class="word-check"
              type="checkbox"
              data-action="toggle-select"
              data-id="${escapeHtml(card.id)}"
              ${checked}
              aria-label="${escapeHtml(card.german)} auswählen"
            >
            <div class="word-main">
              <h3 class="word-de">${escapeHtml(card.german)}</h3>
              <p class="word-en">${escapeHtml(card.english)}</p>
              <p class="word-example">${escapeHtml(card.exampleDe)}</p>
            </div>
            <span class="status-pill ${statusClass(card.status)}">${escapeHtml(statusLabel(card.status))}</span>
          </li>
        `;
      })
      .join("");

    return `
      <section class="panel browse-shell">
        <div class="browse-toolbar">
          <p class="meta-text">${visible.length} / ${state.cards.length} Wörter · alphabetisch</p>
          <div class="browse-toolbar-actions">
            <button type="button" class="btn btn-secondary" data-action="export-words">Exportieren</button>
            <button type="button" class="btn btn-secondary" data-action="select-all">
              ${visible.length && selectedCount === visible.length ? "Auswahl aufheben" : "Alle auswählen"}
            </button>
            <button
              type="button"
              class="btn btn-danger"
              data-action="delete-selected"
              ${selectedCount ? "" : "disabled"}
            >
              Löschen${selectedCount ? ` (${selectedCount})` : ""}
            </button>
          </div>
        </div>

        <div class="control-block">
          <p class="control-label">Filter</p>
          <div class="chip-row">
            ${renderFilterChips(state.browseFilters, "toggle-browse-filter")}
          </div>
        </div>

        ${notice}

        <details class="import-panel">
          <summary>Wörter wiederherstellen / hinzufügen</summary>
          <p class="import-help">
            Ältere Liste einfügen (eine Zeile: <code>Deutsch – Englisch</code>) oder unten ein einzelnes Wort hinzufügen.
          </p>
          <label class="field-label" for="import-text">Liste importieren</label>
          <textarea
            id="import-text"
            class="import-text"
            rows="6"
            placeholder="sich freuen – to be glad&#10;die Gelegenheit – opportunity"
          ></textarea>
          <div class="cta-row import-actions">
            <button type="button" class="btn btn-primary" data-action="import-words">In den Stapel importieren</button>
          </div>

          <div class="add-grid">
            <label class="field-label" for="add-german">Deutsch</label>
            <input id="add-german" class="field-input" type="text" autocomplete="off">
            <label class="field-label" for="add-english">Englisch</label>
            <input id="add-english" class="field-input" type="text" autocomplete="off">
            <label class="field-label" for="add-example-de">Beispielsatz (DE)</label>
            <input id="add-example-de" class="field-input" type="text" autocomplete="off">
            <label class="field-label" for="add-example-en">Beispielsatz (EN)</label>
            <input id="add-example-en" class="field-input" type="text" autocomplete="off">
          </div>
          <div class="cta-row import-actions">
            <button type="button" class="btn btn-secondary" data-action="add-word">Wort hinzufügen</button>
          </div>
        </details>

        ${
          visible.length
            ? `<ul class="word-list">${rows}</ul>`
            : `<div class="empty-state"><h2>Keine Wörter</h2><p>Keine Einträge für die aktuellen Filter. Filter anpassen oder Wörter hinzufügen.</p></div>`
        }
      </section>
    `;
  }

  function renderError(message) {
    return `
      <section class="panel error-state">
        <h2>Seite konnte nicht geladen werden</h2>
        <p>${escapeHtml(message || "Neu laden oder zurück zur Startseite.")}</p>
        <div class="cta-row">
          <button type="button" class="btn btn-primary" data-action="reload-view">Neu laden</button>
          <button type="button" class="btn btn-secondary" data-action="go-home">Zurück</button>
        </div>
      </section>
    `;
  }

  function render() {
    setActiveNav(state.view);

    try {
      let html = "";
      if (state.view === "home") html = renderHome();
      else if (state.view === "study") html = renderStudy();
      else if (state.view === "browse") html = renderBrowse();
      else html = renderError("Unbekannte Ansicht.");

      els.main.innerHTML = html;
      state.lastError = null;
    } catch (error) {
      console.error("Render failed:", error);
      state.lastError = error;
      els.main.innerHTML = renderError(
        "Beim Anzeigen dieser Seite ist etwas schiefgelaufen. Neu laden oder zurück."
      );
    }
  }

  function goTo(view) {
    state.view = view;
    state.lastError = null;

    if (view === "study") {
      startStudySession();
    }

    if (view === "browse") {
      refreshCards();
      [...state.selectedIds].forEach((id) => {
        if (!state.cards.some((card) => card.id === id)) {
          state.selectedIds.delete(id);
        }
      });
    }

    render();
  }

  function advanceAfterRating(status) {
    const card = currentStudyCard();
    if (!card) {
      startStudySession();
      render();
      return;
    }

    setCardStatus(card.id, status);
    state.sessionRated += 1;
    state.flipped = false;

    // Keep remaining unrated cards in queue order, without resetting session totals.
    const remaining = state.studyQueue.slice(state.studyIndex + 1);
    state.studyQueue = remaining;
    state.studyIndex = 0;

    render();
  }

  function onAction(action, target) {
    switch (action) {
      case "go-home":
        goTo("home");
        break;
      case "go-study":
        goTo("study");
        break;
      case "go-browse":
        goTo("browse");
        break;
      case "restart-study":
        startStudySession();
        render();
        break;
      case "reload-view":
        goTo(state.view === "study" ? "study" : state.view || "home");
        break;
      case "set-direction": {
        const direction = target.dataset.direction;
        if (!["de-en", "en-de", "mixed"].includes(direction)) return;
        state.studyDirection = direction;
        savePrefs();
        startStudySession();
        render();
        break;
      }
      case "toggle-study-status": {
        const status = target.dataset.status;
        if (!ALL_STATUSES.includes(status)) return;
        if (state.studyStatuses.has(status)) state.studyStatuses.delete(status);
        else state.studyStatuses.add(status);
        savePrefs();
        startStudySession();
        render();
        break;
      }
      case "toggle-browse-filter": {
        const status = target.dataset.status;
        if (!ALL_STATUSES.includes(status)) return;
        if (state.browseFilters.has(status)) state.browseFilters.delete(status);
        else state.browseFilters.add(status);
        savePrefs();
        render();
        break;
      }
      case "flip-card":
        state.flipped = !state.flipped;
        render();
        break;
      case "rate": {
        const status = target.dataset.status;
        if (!STATUS_ORDER.includes(status)) return;
        advanceAfterRating(status);
        break;
      }
      case "toggle-select": {
        const id = target.dataset.id;
        if (!id) return;
        if (target.checked) state.selectedIds.add(id);
        else state.selectedIds.delete(id);
        render();
        break;
      }
      case "select-all": {
        const visible = filteredBrowseCards();
        const allSelected = visible.every((card) => state.selectedIds.has(card.id));
        if (allSelected) {
          visible.forEach((card) => state.selectedIds.delete(card.id));
        } else {
          visible.forEach((card) => state.selectedIds.add(card.id));
        }
        render();
        break;
      }
      case "delete-selected": {
        const visibleIds = new Set(filteredBrowseCards().map((card) => card.id));
        const ids = [...state.selectedIds].filter((id) => visibleIds.has(id));
        if (!ids.length) return;
        const confirmed = window.confirm(
          `${ids.length} Wort${ids.length === 1 ? "" : "e"} aus dem Stapel löschen?`
        );
        if (!confirmed) return;
        deleteCards(ids);
        state.browseNotice = `${ids.length} Wort${ids.length === 1 ? "" : "e"} gelöscht.`;
        render();
        break;
      }
      case "import-words": {
        const area = document.getElementById("import-text");
        const entries = parseImportText(area ? area.value : "");
        if (!entries.length) {
          state.browseNotice = "Keine Wörter gefunden. Format: Wort – Bedeutung";
          render();
          return;
        }
        const result = upsertCustomWords(entries);
        state.browseNotice = `${entries.length} importiert: ${result.added} neu, ${result.updated} aktualisiert.`;
        render();
        break;
      }
      case "add-word": {
        const german = document.getElementById("add-german");
        const english = document.getElementById("add-english");
        const exampleDe = document.getElementById("add-example-de");
        const exampleEn = document.getElementById("add-example-en");
        const entry = normalizeWord({
          german: german ? german.value : "",
          english: english ? english.value : "",
          exampleDe: exampleDe ? exampleDe.value : "",
          exampleEn: exampleEn ? exampleEn.value : "",
          custom: true,
        });
        if (!entry) {
          state.browseNotice = "Bitte Deutsch und Englisch ausfüllen.";
          render();
          return;
        }
        if (!entry.exampleDe) entry.exampleDe = entry.german;
        if (!entry.exampleEn) entry.exampleEn = entry.english;
        upsertCustomWords([entry]);
        state.browseNotice = `„${entry.german}“ hinzugefügt.`;
        render();
        break;
      }
      case "export-words": {
        const payload = filteredBrowseCards().map(({ id, german, english, exampleDe, exampleEn }) => ({
          id,
          german,
          english,
          exampleDe,
          exampleEn,
        }));
        const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = "wortkarte-woerter.json";
        link.click();
        URL.revokeObjectURL(url);
        state.browseNotice = `${payload.length} Wörter exportiert.`;
        render();
        break;
      }
      default:
        break;
    }
  }

  function bindEvents() {
    els.brandBtn.addEventListener("click", () => goTo("home"));

    els.navButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const view = btn.dataset.view;
        if (view) goTo(view);
      });
    });

    els.main.addEventListener("click", (event) => {
      const target = event.target.closest("[data-action]");
      if (!target || !els.main.contains(target)) return;
      if (target.dataset.action === "toggle-select") return;
      onAction(target.dataset.action, target);
    });

    els.main.addEventListener("change", (event) => {
      const target = event.target;
      if (!(target instanceof HTMLInputElement)) return;
      if (target.dataset.action !== "toggle-select") return;
      onAction("toggle-select", target);
    });

    window.addEventListener("error", () => {
      if (state.view === "study" && !state.lastError) {
        state.lastError = true;
        els.main.innerHTML = renderError(
          "Im Lernmodus ist ein Fehler aufgetreten. Sitzung neu laden oder zurück."
        );
      }
    });
  }

  function registerServiceWorker() {
    if (!("serviceWorker" in navigator)) return;
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("./sw.js?v=208").catch((error) => {
        console.warn("Service worker registration failed:", error);
      });
    });
  }

  function init() {
    try {
      loadPrefs();
      refreshCards();
      bindEvents();
      registerServiceWorker();
      goTo("home");
    } catch (error) {
      console.error("Init failed:", error);
      els.main.innerHTML = renderError("Die App konnte nicht gestartet werden. Seite neu laden.");
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
