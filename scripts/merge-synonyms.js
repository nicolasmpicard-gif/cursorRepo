#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const wordsPath = path.join(__dirname, "..", "flashcard-app", "words.js");
global.window = {};
eval(fs.readFileSync(wordsPath, "utf8"));
let words = window.SEED_WORDS.map((w) => ({ ...w }));

const DELETE_IDS = new Set([
  "schlussendlich",
  "rechnen",
  "erledigen",
  "zur-verfuegung-stellen",
  "wir-machen-weiter",
  "befuerchten",
  "ablehnend",
  "ich-bin-es-nicht-gewohnt",
]);

words = words.filter((w) => !DELETE_IDS.has(w.id));

// Keep endlich after removing schlussendlich / endlich merge
if (!words.some((w) => w.id === "endlich" || w.german === "endlich")) {
  words.push({
    id: "endlich",
    german: "endlich",
    english: "finally",
    exampleDe: "Endlich ist das Projekt fertig.",
    exampleEn: "The project is finally finished.",
  });
}

function findBy(...preds) {
  return words.find((w) => preds.some((p) => p(w))) || null;
}

function takeIds(...candidates) {
  const found = [];
  for (const c of candidates) {
    let w = null;
    if (typeof c === "string") {
      w = words.find((x) => x.id === c) || null;
    } else if (c instanceof RegExp) {
      w = words.find((x) => c.test(x.id) || c.test(x.german)) || null;
    } else if (typeof c === "function") {
      w = words.find(c) || null;
    }
    if (w && !found.includes(w.id)) found.push(w.id);
  }
  return found;
}

function applyMerge({ newId, matchers, german, english, exampleDe, exampleEn }) {
  const ids = takeIds(...matchers);
  if (!ids.length) {
    console.warn("SKIP merge (none found):", newId);
    return;
  }
  const primary = words.find((w) => w.id === ids[0]);
  const merged = {
    id: newId,
    german,
    english,
    exampleDe,
    exampleEn,
  };
  // Remove all matched cards, then insert merged
  words = words.filter((w) => !ids.includes(w.id));
  words.push(merged);
  console.log("MERGED", newId, "from", ids.join(", "));
}

const merges = [
  {
    newId: "kriegen-bekommen-erhalten",
    matchers: ["kriegen", "erhalten", (w) => w.german === "bekommen"],
    german:
      'kriegen (informal "to get") / bekommen (neutral everyday "to get / receive") / erhalten (more formal "to receive / obtain")',
    english: "to get / receive",
    exampleDe:
      "Kriegst du das bis morgen hin?\nIch bekomme morgen die Unterlagen.\nHaben Sie meine E-Mail erhalten?",
    exampleEn:
      "Can you get that done by tomorrow?\nI will get the documents tomorrow.\nDid you receive my email?",
  },
  {
    newId: "anstellen-einstellen",
    matchers: ["anstellen", "einstellen"],
    german:
      'anstellen (everyday "to hire") / einstellen (formal/HR "to hire"; also "to adjust / set")',
    english: "to hire / employ (einstellen also: adjust / set)",
    exampleDe:
      "Wir wollen zwei neue Kollegen anstellen.\nWir stellen nächstes Jahr neue Mitarbeiter ein.",
    exampleEn:
      "We want to hire two new colleagues.\nWe are hiring new employees next year.",
  },
  {
    newId: "noetig-notwendig-unverzichtbar",
    matchers: ["noetig", "notwendig", "unverzichtbar"],
    german:
      "nötig (necessary) / notwendig (necessary) / unverzichtbar (indispensable / essential)",
    english: "necessary / essential",
    exampleDe:
      "Ist das wirklich nötig?\nEine schnelle Antwort ist notwendig.\nGute Kommunikation ist unverzichtbar.",
    exampleEn:
      "Is that really necessary?\nA quick reply is necessary.\nGood communication is indispensable.",
  },
  {
    newId: "ausfuehrlich-detailliert-eingehend",
    matchers: ["ausfuehrlich", "detailliert", "eingehend"],
    german:
      "ausführlich (detailed / thorough) / detailliert (detailed) / eingehend (in-depth / thorough)",
    english: "detailed / thorough",
    exampleDe:
      "Bitte beschreiben Sie das Problem ausführlich.\nBitte senden Sie mir eine detaillierte Übersicht.\nWir brauchen eine eingehende Prüfung.",
    exampleEn:
      "Please describe the problem in detail.\nPlease send me a detailed overview.\nWe need a thorough review.",
  },
  {
    newId: "verlaesslich-zuverlaessig",
    matchers: [
      (w) => /^verlässlich/.test(w.german) || w.id.startsWith("verlaess"),
      (w) => w.german === "zuverlässig" || w.id === "zuverlaessig",
    ],
    german: "verlässlich (reliable) / zuverlässig (reliable / trustworthy)",
    english: "reliable",
    exampleDe:
      "Wir brauchen verlässliche Informationen.\nEr ist ein zuverlässiger Kollege.",
    exampleEn: "We need reliable information.\nHe is a reliable colleague.",
  },
  {
    newId: "kundschaft-stammkundschaft",
    matchers: ["kundschaft", "die-stammkundschaft"],
    german:
      "die Kundschaft (customers / clientele) / die Stammkundschaft (regular customers)",
    english: "customers / clientele",
    exampleDe:
      "Unsere Kundschaft schätzt guten Service.\nDie Stammkundschaft kommt jede Woche.",
    exampleEn:
      "Our customers appreciate good service.\nThe regular customers come every week.",
  },
  {
    newId: "besprechen-diskutieren",
    matchers: ["besprechen", "diskutieren-ueber"],
    german: 'besprechen (to discuss) / diskutieren über (to discuss / debate)',
    english: "to discuss",
    exampleDe:
      "Können wir das morgen besprechen?\nWir diskutieren über den neuen Zeitplan.",
    exampleEn:
      "Can we discuss that tomorrow?\nWe are discussing the new schedule.",
  },
  {
    newId: "aussuchen-auswaehlen",
    matchers: ["aussuchen", "auswaehlen"],
    german: 'aussuchen (to pick out / choose) / auswählen (to select / choose)',
    english: "to choose / select",
    exampleDe:
      "Such dir bitte ein Geschenk aus.\nBitte wählen Sie eine Option aus.",
    exampleEn: "Please pick out a gift.\nPlease select an option.",
  },
  {
    newId: "zuversichtlich-selbstbewusst",
    matchers: ["zuversichtlich", "selbstbewusst"],
    german:
      'zuversichtlich (confident / optimistic about an outcome) / selbstbewusst (self-confident)',
    english: "confident",
    exampleDe:
      "Ich bin zuversichtlich, dass wir das schaffen.\nSie wirkt sehr selbstbewusst.",
    exampleEn:
      "I am confident that we can do it.\nShe seems very self-confident.",
  },
  {
    newId: "unbedingt-auf-jeden-fall",
    matchers: ["unbedingt", "auf-jeden-fall"],
    german:
      'unbedingt (definitely / by all means) / auf jeden Fall (in any case / definitely)',
    english: "definitely",
    exampleDe:
      "Du musst unbedingt Bescheid sagen.\nAuf jeden Fall komme ich morgen.",
    exampleEn:
      "You must definitely let us know.\nI am definitely coming tomorrow.",
  },
  {
    newId: "zeitnah-umgehend-rechtzeitig",
    matchers: ["zeitnah", "umgehend", "rechtzeitig"],
    german:
      'zeitnah (promptly / in a timely manner) / umgehend (immediately) / rechtzeitig (on time / in good time)',
    english: "promptly / on time / immediately",
    exampleDe:
      "Bitte antworten Sie zeitnah auf die Anfrage.\nBitte antworten Sie umgehend.\nBitte kommen Sie rechtzeitig.",
    exampleEn:
      "Please reply to the request promptly.\nPlease reply immediately.\nPlease arrive on time.",
  },
  {
    newId: "ich-vermute-gehe-davon-aus",
    matchers: ["ich-vermute", "ich-gehe-davon-aus"],
    german:
      'ich vermute (I suspect / I guess) / ich gehe davon aus (I assume / I\'m proceeding on the assumption that)',
    english: "I assume / I suspect",
    exampleDe:
      "Ich vermute, dass er später kommt.\nIch gehe davon aus, dass der Plan funktioniert.",
    exampleEn:
      "I suspect that he will come later.\nI assume that the plan will work.",
  },
  {
    newId: "entschaedigung-wiedergutmachung-erstattung",
    matchers: ["die-entschaedigung", "die-wiedergutmachung", "erstattung"],
    german:
      "die Entschädigung (compensation) / die Wiedergutmachung (reparation / making amends) / die Erstattung (refund / reimbursement)",
    english: "compensation / refund",
    exampleDe:
      "Die Kunden fordern eine Entschädigung.\nEr hat Wiedergutmachung für den Fehler angeboten.\nIch bitte um eine Erstattung des Kaufpreises.",
    exampleEn:
      "The customers are demanding compensation.\nHe offered to make amends for the mistake.\nI am requesting a refund of the purchase price.",
  },
  {
    newId: "zwischenzeitlich-mittlerweile",
    matchers: ["zwischenzeitlich", "mittlerweile"],
    german:
      "zwischenzeitlich (in the meantime / interim) / mittlerweile (meanwhile / by now)",
    english: "meanwhile / in the meantime",
    exampleDe:
      "Zwischenzeitlich haben wir eine Lösung gefunden.\nMittlerweile ist das Problem gelöst.",
    exampleEn:
      "In the meantime we have found a solution.\nBy now the problem is solved.",
  },
  {
    newId: "auffallen-herausstechen",
    matchers: ["auffallen", "herausstechen"],
    german:
      "auffallen (to be noticeable / catch one's attention) / herausstechen (to stand out)",
    english: "to stand out / be noticeable",
    exampleDe:
      "Sein Akzent ist mir sofort aufgefallen.\nIhre Ideen stechen aus der Menge heraus.",
    exampleEn:
      "I noticed his accent immediately.\nHer ideas stand out from the crowd.",
  },
  {
    newId: "beteiligen-teilnehmen",
    matchers: ["sich-beteiligen-an", "teilnehmen-an"],
    german:
      "sich beteiligen an (to take part / be involved in) / teilnehmen an (to participate in)",
    english: "to take part in / participate in",
    exampleDe:
      "Möchten Sie sich an dem Projekt beteiligen?\nMöchten Sie an dem Kurs teilnehmen?",
    exampleEn:
      "Would you like to take part in the project?\nWould you like to take part in the course?",
  },
  {
    newId: "aufpassen-achten",
    matchers: ["aufpassen", "achten-auf"],
    german:
      "aufpassen auf (to watch out for / look after) / achten auf (to pay attention to)",
    english: "to watch out for / pay attention to",
    exampleDe: "Pass auf die Kinder auf.\nBitte achten Sie auf die Deadline.",
    exampleEn: "Look after the children.\nPlease pay attention to the deadline.",
  },
  {
    newId: "erlebnis-erleben",
    matchers: ["das-erlebnis", "erleben"],
    german:
      "das Erlebnis (a memorable experience / event) / erleben (to experience / live through)",
    english: "experience / to experience",
    exampleDe:
      "Der Ausflug war ein schönes Erlebnis.\nDas habe ich noch nie erlebt.",
    exampleEn:
      "The trip was a lovely experience.\nI have never experienced that.",
  },
  {
    newId: "nachvollziehen-nachvollziehbarkeit",
    matchers: ["nachvollziehen", "nachvollziehbarkeit"],
    german:
      "nachvollziehen (to understand / follow logically) / die Nachvollziehbarkeit (comprehensibility / traceability)",
    english: "to understand / comprehensibility",
    exampleDe:
      "Ihre Entscheidung kann ich gut nachvollziehen.\nFür die Nachvollziehbarkeit dokumentieren wir jeden Schritt.",
    exampleEn:
      "I can understand your decision well.\nFor traceability, we document every step.",
  },
  {
    newId: "foerdern-gefoerdert-foerderungen",
    matchers: [
      "foerdern",
      (w) => w.german === "gefördert" || w.id.includes("gefoerder"),
      "die-foerderungen",
    ],
    german:
      "fördern (to promote / support / fund) / gefördert (funded / supported) / die Förderungen (funding / grants)",
    english: "to promote / fund / funding",
    exampleDe:
      "Das Programm soll junge Talente fördern.\nDas ist ein gefördertes Projekt.\nEs gibt neue Förderungen für Start-ups.",
    exampleEn:
      "The program is meant to promote young talent.\nThat is a funded project.\nThere is new funding for start-ups.",
  },
  {
    newId: "aergern-nervig-aergernis",
    matchers: ["sich-aergern", "nervig", "das-aergernis"],
    german:
      "sich ärgern über (to get annoyed about) / nervig (annoying) / das Ärgernis (nuisance / annoyance)",
    english: "annoyance / to get annoyed",
    exampleDe:
      "Ich ärgere mich über den Stau.\nDer Alarmton ist echt nervig.\nDer Lärm ist ein großes Ärgernis.",
    exampleEn:
      "I get annoyed about the traffic jam.\nThe alarm sound is really annoying.\nThe noise is a big nuisance.",
  },
  {
    newId: "benoetigen-bedarf",
    matchers: ["benoetigen", "der-bedarf-an"],
    german:
      "benötigen (to need / require) / der Bedarf (need / demand) / der Bedarf an (need for / demand for)",
    english: "to need / need / demand",
    exampleDe:
      "Wir benötigen mehr Informationen.\nDer Bedarf ist gestiegen.\nDer Bedarf an Fachkräften steigt.",
    exampleEn:
      "We need more information.\nDemand has risen.\nThe need for skilled workers is rising.",
  },
  {
    newId: "erstellen-entwerfen-gestalten",
    matchers: ["erstellen", "entwerfen", "gestalten"],
    german:
      'erstellen (to create / produce) / entwerfen (to design / draft) / gestalten (to shape / design)',
    english: "to create / design",
    exampleDe:
      "Ich erstelle gerade eine Präsentation.\nSie entwirft ein neues Logo für die Firma.\nWir wollen den Prozess neu gestalten.",
    exampleEn:
      "I am creating a presentation right now.\nShe is designing a new logo for the company.\nWe want to reshape the process.",
  },
  {
    newId: "erlaeutern-eingehen",
    matchers: ["erlaeutern", "eingehen-auf"],
    german:
      "erläutern (to explain / clarify) / eingehen auf (to address / go into)",
    english: "to explain / address",
    exampleDe:
      "Können Sie den Vorschlag bitte näher erläutern?\nKönnen wir näher auf Ihre Frage eingehen?",
    exampleEn:
      "Can you please explain the suggestion in more detail?\nCan we go into your question in more detail?",
  },
  {
    newId: "geschehen-entstehen",
    matchers: ["geschehen", "entstehen"],
    german:
      "geschehen (to happen / occur) / entstehen (to arise / come into being)",
    english: "to happen / arise",
    exampleDe:
      "Wie konnte das geschehen?\nSo können Missverständnisse entstehen.",
    exampleEn:
      "How could that happen?\nThat is how misunderstandings can arise.",
  },
  {
    newId: "derzeitig-zurzeit",
    matchers: [
      (w) => /derzeitig/.test(w.german) || w.id.startsWith("derzeitig"),
      "zurzeit",
    ],
    german:
      "derzeitig (current / present) / zurzeit (currently / at the moment)",
    english: "current / currently",
    exampleDe:
      "Das ist unsere derzeitige Situation.\nZurzeit arbeite ich von zu Hause.",
    exampleEn:
      "That is our current situation.\nI am currently working from home.",
  },
  {
    newId: "voraussichtlich-vermutlich",
    matchers: ["voraussichtlich", "vermutlich"],
    german:
      "voraussichtlich (expected / presumably) / vermutlich (probably / presumably)",
    english: "presumably / probably",
    exampleDe:
      "Voraussichtlich kommt er morgen an.\nVermutlich kommt er später.",
    exampleEn:
      "He is expected to arrive tomorrow.\nHe will probably come later.",
  },
  {
    newId: "wecken-aufwachen",
    matchers: ["jmdn-wecken", "aufwachen"],
    german:
      "jmdn. wecken (to wake someone up) / aufwachen (to wake up)",
    english: "to wake (someone) up",
    exampleDe:
      "Kannst du mich um 7 Uhr wecken?\nIch wache jeden Tag um sechs Uhr auf.",
    exampleEn: "Can you wake me up at 7?\nI wake up at six every day.",
  },
  {
    newId: "einbeziehen-umfassen",
    matchers: ["einbeziehen-in", "umfassen"],
    german:
      "einbeziehen in (to include / involve in) / umfassen (to include / comprise)",
    english: "to include",
    exampleDe:
      "Bitte beziehen Sie alle Kollegen in die Planung ein.\nDas Angebot umfasst drei Module.",
    exampleEn:
      "Please include all colleagues in the planning.\nThe offer includes three modules.",
  },
  {
    newId: "anbieten-angebot-unterbreiten",
    matchers: ["anbieten", "ein-angebot-unterbreiten"],
    german:
      "anbieten (to offer) / ein Angebot unterbreiten (to make / submit an offer)",
    english: "to offer",
    exampleDe:
      "Darf ich Ihnen etwas zu trinken anbieten?\nDarf ich Ihnen ein Angebot unterbreiten?",
    exampleEn:
      "May I offer you something to drink?\nMay I submit an offer to you?",
  },
  {
    newId: "unterstuetzen-betreuung",
    matchers: ["unterstuetzen-bei", "betreuung"],
    german:
      "unterstützen bei (to support with) / die Betreuung (care / support / supervision)",
    english: "to support / support",
    exampleDe:
      "Ich unterstütze dich bei der Vorbereitung.\nDie Betreuung der Kunden ist sehr gut.",
    exampleEn:
      "I support you with the preparation.\nThe customer support is very good.",
  },
  {
    newId: "zeitplan-ablauf",
    matchers: ["zeitplan", "ablauf"],
    german:
      "der Zeitplan (schedule / timetable) / der Ablauf (process / sequence / course of events)",
    english: "schedule / process",
    exampleDe:
      "Der Zeitplan ist sehr eng.\nKönnen Sie mir den Ablauf erklären?",
    exampleEn:
      "The schedule is very tight.\nCan you explain the process to me?",
  },
];

for (const m of merges) applyMerge(m);

// Ensure bekommen is present via the kriegen merge (matcher may have missed if not in deck)
if (!words.some((w) => w.id === "kriegen-bekommen-erhalten")) {
  console.warn("get/receive merge missing — adding fresh card");
  words.push({
    id: "kriegen-bekommen-erhalten",
    german:
      'kriegen (informal "to get") / bekommen (neutral everyday "to get / receive") / erhalten (more formal "to receive / obtain")',
    english: "to get / receive",
    exampleDe:
      "Kriegst du das bis morgen hin?\nIch bekomme morgen die Unterlagen.\nHaben Sie meine E-Mail erhalten?",
    exampleEn:
      "Can you get that done by tomorrow?\nI will get the documents tomorrow.\nDid you receive my email?",
  });
} else {
  // Remove leftover bare erhalten/kriegen if any
  words = words.filter(
    (w) =>
      !(w.id === "kriegen" || w.id === "erhalten" || w.german === "bekommen")
  );
}

// Confirm non-merges still separate
for (const g of ["das Verhalten", "der Umgang mit", "fordern", "der Anspruch auf"]) {
  const hit = words.find((w) => w.german === g || w.german.startsWith(g));
  console.log("KEEP SEPARATE", g, hit ? "ok" : "MISSING");
}

// Dedupe ids
const seen = new Set();
words = words.filter((w) => {
  if (seen.has(w.id)) return false;
  seen.add(w.id);
  return true;
});

function esc(s) {
  return String(s)
    .replace(/\\/g, "\\\\")
    .replace(/"/g, '\\"')
    .replace(/\n/g, "\\n")
    .replace(/\r/g, "\\r");
}

let out = `/**
 * Seed vocabulary for the German flashcard app.
 * Progress (status / lastReviewedAt) is stored separately in localStorage.
 * Custom/imported words are stored under wortkarte.custom.v1.
 *
 * Near-synonyms are stored on one card as:
 *   term A (nuance) / term B (nuance)
 * with one example sentence per term (newline-separated).
 * When adding new vocabulary, check whether a new word belongs on an
 * existing near-synonym card before creating a separate entry.
 */
window.SEED_WORDS = [
`;

for (const w of words) {
  out += `  {\n`;
  out += `    id: "${esc(w.id)}",\n`;
  out += `    german: "${esc(w.german)}",\n`;
  out += `    english: "${esc(w.english)}",\n`;
  out += `    exampleDe: "${esc(w.exampleDe)}",\n`;
  out += `    exampleEn: "${esc(w.exampleEn)}",\n`;
  out += `  },\n`;
}
out += `];\n`;

fs.writeFileSync(wordsPath, out);
console.log("wrote", words.length, "cards");
