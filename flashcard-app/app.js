(() => {
  "use strict";

  const STORAGE_KEY = "wortkarte.progress.v1";
  const DELETED_KEY = "wortkarte.deleted.v1";
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

  function normalizeSeedWords() {
    const seeds = Array.isArray(window.SEED_WORDS) ? window.SEED_WORDS : [];
    return seeds
      .filter((word) => word && typeof word === "object" && word.id && word.german)
      .map((word) => ({
        id: String(word.id),
        german: String(word.german),
        english: String(word.english || ""),
        exampleDe: String(word.exampleDe || word.german),
        exampleEn: String(word.exampleEn || word.english || ""),
      }));
  }

  function buildCards() {
    const progress = loadProgress();
    const deleted = loadDeleted();
    const seeds = normalizeSeedWords();

    return seeds
      .filter((word) => !deleted.has(word.id))
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

  function deleteCards(ids) {
    if (!ids.length) return;
    const deleted = loadDeleted();
    const progress = loadProgress();
    ids.forEach((id) => {
      deleted.add(id);
      delete progress[id];
    });
    saveDeleted(deleted);
    saveProgress(progress);
    ids.forEach((id) => state.selectedIds.delete(id));
    refreshCards();
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

    if (!state.cards.length) {
      return `
        <section class="panel empty-state">
          <h2>No words in Browse</h2>
          <p>All cards have been deleted. Refresh the page after clearing site data to restore the seed vocabulary.</p>
        </section>
      `;
    }

    return `
      <section class="panel browse-shell">
        <div class="browse-toolbar">
          <p class="meta-text">${state.cards.length} words · alphabetical</p>
          <div class="browse-toolbar-actions">
            <button type="button" class="btn btn-secondary" data-action="select-all">
              ${selectedCount === state.cards.length ? "Clear selection" : "Select all"}
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
        <ul class="word-list">${rows}</ul>
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

  function init() {
    try {
      refreshCards();
      bindEvents();
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
