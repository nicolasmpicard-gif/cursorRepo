(() => {
  "use strict";

  const STORAGE_KEY = "wortkarte.progress.v1";
  const DELETED_KEY = "wortkarte.deleted.v1";
  const CUSTOM_KEY = "wortkarte.custom.v1";
  const STATUS_ORDER = ["forgot", "difficult", "easy", "instant"];
  const STATUS_LABELS = {
    forgot: "Forgot",
    difficult: "Difficult",
    easy: "Easy",
    instant: "Instant",
    none: "New",
  };

  const state = {
    view: "home",
    cards: [],
    studyQueue: [],
    studyIndex: 0,
    flipped: false,
    selectedIds: new Set(),
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
      // Custom entries can override seed entries with the same id.
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

    // If a word was previously deleted, importing it again restores it.
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
      if (customIds.has(id)) {
        // Drop custom words entirely.
        return;
      }
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

    // JSON array or { words: [...] }
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

  function studyPriority(status) {
    if (status === "forgot") return 0;
    if (status === "difficult") return 1;
    if (status === null) return 2;
    if (status === "easy") return 3;
    return 4;
  }

  function buildStudyQueue() {
    const prioritized = [...state.cards].sort((a, b) => {
      const diff = studyPriority(a.status) - studyPriority(b.status);
      if (diff !== 0) return diff;
      return (a.lastReviewedAt || 0) - (b.lastReviewedAt || 0);
    });

    // Keep weaker cards earlier, but mix within bands so sessions feel fresh.
    const bands = [[], [], [], [], []];
    prioritized.forEach((card) => {
      bands[studyPriority(card.status)].push(card);
    });
    return bands.flatMap((band) => shuffle(band));
  }

  function currentStudyCard() {
    if (!state.studyQueue.length) return null;
    if (state.studyIndex < 0 || state.studyIndex >= state.studyQueue.length) {
      return null;
    }
    return state.studyQueue[state.studyIndex] || null;
  }

  function startStudySession() {
    refreshCards();
    state.studyQueue = buildStudyQueue();
    state.studyIndex = 0;
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
    return STATUS_LABELS[status || "none"];
  }

  function setActiveNav(view) {
    els.navButtons.forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.view === view);
    });
  }

  function renderHome() {
    return `
      <section class="panel hero">
        <h1 class="hero-brand">Wortkarte</h1>
        <p class="hero-lead">
          Flip through German words, rate how well you know them, and keep tabs on every card in Browse.
        </p>
        <div class="cta-row">
          <button type="button" class="btn btn-primary" data-action="go-study">Start studying</button>
          <button type="button" class="btn btn-secondary" data-action="go-browse">Browse words</button>
        </div>
      </section>
    `;
  }

  function renderStudy() {
    const total = state.studyQueue.length;
    const card = currentStudyCard();

    if (!total) {
      return `
        <section class="panel empty-state">
          <h2>No cards to study</h2>
          <p>Your deck is empty. Add words back from Browse, or restore the seed list by clearing deleted cards in browser storage.</p>
          <button type="button" class="btn btn-secondary" data-action="go-browse">Open Browse</button>
        </section>
      `;
    }

    if (!card) {
      // Recover from an out-of-range index instead of crashing Study mode.
      state.studyIndex = 0;
      state.flipped = false;
      const recovered = currentStudyCard();
      if (!recovered) {
        return `
          <section class="panel error-state">
            <h2>Couldn’t load this card</h2>
            <p>Something went wrong while preparing the next flashcard. Reload the study session to continue.</p>
            <div class="cta-row">
              <button type="button" class="btn btn-primary" data-action="restart-study">Reload study</button>
              <button type="button" class="btn btn-secondary" data-action="go-home">Go back</button>
            </div>
          </section>
        `;
      }
    }

    const active = currentStudyCard();
    const progressLabel = `${Math.min(state.studyIndex + 1, total)} / ${total}`;
    const flipClass = state.flipped ? "is-flipped" : "";

    return `
      <section class="panel study-shell">
        <div class="study-meta">
          <p class="meta-text">Card ${escapeHtml(progressLabel)}</p>
          <button type="button" class="btn btn-ghost" data-action="restart-study">Shuffle again</button>
        </div>

        <button
          type="button"
          class="flashcard ${flipClass}"
          data-action="flip-card"
          aria-label="Flip flashcard"
        >
          <div class="flashcard-inner">
            <div class="face face-front">
              <p class="face-label">German</p>
              <h2 class="face-word">${escapeHtml(active.german)}</h2>
            </div>
            <div class="face face-back">
              <p class="face-label">Meaning</p>
              <p class="face-meaning">${escapeHtml(active.english)}</p>
              <div class="face-example">
                <strong>${escapeHtml(active.exampleDe)}</strong>
                <span>${escapeHtml(active.exampleEn)}</span>
              </div>
            </div>
          </div>
        </button>

        <p class="hint">${state.flipped ? "Rate this card to continue" : "Tap the card to reveal the meaning"}</p>

        <div class="rating-row" ${state.flipped ? "" : "hidden"}>
          <button type="button" class="rate-btn rate-forgot" data-action="rate" data-status="forgot">Forgot</button>
          <button type="button" class="rate-btn rate-difficult" data-action="rate" data-status="difficult">Difficult</button>
          <button type="button" class="rate-btn rate-easy" data-action="rate" data-status="easy">Easy</button>
          <button type="button" class="rate-btn rate-instant" data-action="rate" data-status="instant">Instant</button>
        </div>
      </section>
    `;
  }

  function renderBrowse() {
    const selectedCount = state.selectedIds.size;
    const notice = state.browseNotice
      ? `<p class="browse-notice" role="status">${escapeHtml(state.browseNotice)}</p>`
      : "";

    const rows = state.cards
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
              aria-label="Select ${escapeHtml(card.german)}"
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
          <p class="meta-text">${state.cards.length} words · alphabetical</p>
          <div class="browse-toolbar-actions">
            <button type="button" class="btn btn-secondary" data-action="export-words">Export</button>
            <button type="button" class="btn btn-secondary" data-action="select-all">
              ${state.cards.length && selectedCount === state.cards.length ? "Clear selection" : "Select all"}
            </button>
            <button
              type="button"
              class="btn btn-danger"
              data-action="delete-selected"
              ${selectedCount ? "" : "disabled"}
            >
              Delete${selectedCount ? ` (${selectedCount})` : ""}
            </button>
          </div>
        </div>

        ${notice}

        <details class="import-panel" open>
          <summary>Restore / add words</summary>
          <p class="import-help">
            Paste your older list (one per line as <code>German – English</code>), or add a single word below.
          </p>
          <label class="field-label" for="import-text">Import list</label>
          <textarea
            id="import-text"
            class="import-text"
            rows="6"
            placeholder="sich freuen – to be glad&#10;die Gelegenheit – opportunity&#10;abhängen von – to depend on"
          ></textarea>
          <div class="cta-row import-actions">
            <button type="button" class="btn btn-primary" data-action="import-words">Import into deck</button>
          </div>

          <div class="add-grid">
            <label class="field-label" for="add-german">German</label>
            <input id="add-german" class="field-input" type="text" autocomplete="off">
            <label class="field-label" for="add-english">English</label>
            <input id="add-english" class="field-input" type="text" autocomplete="off">
            <label class="field-label" for="add-example-de">Sample sentence (DE)</label>
            <input id="add-example-de" class="field-input" type="text" autocomplete="off">
            <label class="field-label" for="add-example-en">Sample sentence (EN)</label>
            <input id="add-example-en" class="field-input" type="text" autocomplete="off">
          </div>
          <div class="cta-row import-actions">
            <button type="button" class="btn btn-secondary" data-action="add-word">Add word</button>
          </div>
        </details>

        ${
          state.cards.length
            ? `<ul class="word-list">${rows}</ul>`
            : `<div class="empty-state"><h2>No words yet</h2><p>Import your previous list above to restore the full deck.</p></div>`
        }
      </section>
    `;
  }

  function renderError(message) {
    return `
      <section class="panel error-state">
        <h2>This page couldn’t load</h2>
        <p>${escapeHtml(message || "Reload to try again, or go back home.")}</p>
        <div class="cta-row">
          <button type="button" class="btn btn-primary" data-action="reload-view">Reload</button>
          <button type="button" class="btn btn-secondary" data-action="go-home">Go back</button>
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
      else html = renderError("Unknown view.");

      els.main.innerHTML = html;
      state.lastError = null;
    } catch (error) {
      console.error("Render failed:", error);
      state.lastError = error;
      els.main.innerHTML = renderError(
        "Something went wrong while rendering this screen. Reload to try again or go back."
      );
    }
  }

  function goTo(view) {
    state.view = view;
    state.lastError = null;

    if (view === "study") {
      // Always rebuild a safe queue when entering Study to avoid stale indices.
      startStudySession();
    }

    if (view === "browse") {
      refreshCards();
      // Drop selections that no longer exist.
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

    // Rebuild queue membership from refreshed cards, keep relative progress.
    const remainingIds = state.studyQueue
      .slice(state.studyIndex + 1)
      .map((item) => item.id)
      .filter((id) => state.cards.some((c) => c.id === id));

    const nextQueue = remainingIds
      .map((id) => state.cards.find((c) => c.id === id))
      .filter(Boolean);

    if (!nextQueue.length) {
      // Session complete — reshuffle for another round.
      startStudySession();
    } else {
      state.studyQueue = nextQueue;
      state.studyIndex = 0;
      state.flipped = false;
    }

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
        if (state.selectedIds.size === state.cards.length) {
          state.selectedIds.clear();
        } else {
          state.cards.forEach((card) => state.selectedIds.add(card.id));
        }
        render();
        break;
      }
      case "delete-selected": {
        const ids = [...state.selectedIds];
        if (!ids.length) return;
        const confirmed = window.confirm(
          `Delete ${ids.length} word${ids.length === 1 ? "" : "s"} from your deck?`
        );
        if (!confirmed) return;
        deleteCards(ids);
        state.browseNotice = `Deleted ${ids.length} word${ids.length === 1 ? "" : "s"}.`;
        render();
        break;
      }
      case "import-words": {
        const area = document.getElementById("import-text");
        const entries = parseImportText(area ? area.value : "");
        if (!entries.length) {
          state.browseNotice = "No words found. Use lines like: Wort – meaning";
          render();
          return;
        }
        const result = upsertCustomWords(entries);
        state.browseNotice = `Imported ${entries.length}: ${result.added} new, ${result.updated} updated.`;
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
          state.browseNotice = "Add both a German word and an English meaning.";
          render();
          return;
        }
        if (!entry.exampleDe) entry.exampleDe = entry.german;
        if (!entry.exampleEn) entry.exampleEn = entry.english;
        upsertCustomWords([entry]);
        state.browseNotice = `Added “${entry.german}”.`;
        render();
        break;
      }
      case "export-words": {
        const payload = state.cards.map(({ id, german, english, exampleDe, exampleEn }) => ({
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
        link.download = "wortkarte-words.json";
        link.click();
        URL.revokeObjectURL(url);
        state.browseNotice = `Exported ${payload.length} words.`;
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

      // Checkboxes also fire click; handle via change for toggle-select.
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
      // Surface a recoverable UI if an unexpected runtime error occurs mid-view.
      if (state.view === "study" && !state.lastError) {
        state.lastError = true;
        els.main.innerHTML = renderError(
          "Study mode hit an unexpected error. Reload the session or go back home."
        );
      }
    });
  }

  function registerServiceWorker() {
    if (!("serviceWorker" in navigator)) return;
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("./sw.js").catch((error) => {
        console.warn("Service worker registration failed:", error);
      });
    });
  }

  function init() {
    try {
      refreshCards();
      bindEvents();
      registerServiceWorker();
      goTo("home");
    } catch (error) {
      console.error("Init failed:", error);
      els.main.innerHTML = renderError(
        "The app failed to start. Reload the page to try again."
      );
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
