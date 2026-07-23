# Wortkarte — German Flashcard App

A local web app for studying German vocabulary with flip cards, difficulty ratings, and a browseable word list.

## Run locally

```bash
cd flashcard-app
python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080) in your browser.

## Features

- **Study** — flip a card to see the English meaning and a sample sentence, then rate it: Forgot, Difficult, Easy, or Instant
- **Browse** — words listed in alphabetical order (German locale), each showing its latest rating status
- **Multi-select delete** — select one or many words in Browse and delete them from your deck
- Progress is saved in `localStorage` on your device

## Vocabulary

Seed words live in `flashcard-app/words.js`. Each entry includes:

- German term / phrase
- English definition
- Sample sentence (German + English)

## Notes

- Deleted words are remembered locally; clearing site data for this origin restores the seed deck
- Study mode rebuilds its queue safely when you enter the view, so empty decks and stale indices do not crash the page
