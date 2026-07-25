# Wortkarte — Blank shareable deck

Empty copy of the German flashcard app for sharing with friends. No seed vocabulary included.

## Open / share

https://raw.githack.com/nicolasmpicard-gif/cursorRepo/gh-pages/share/index.html

## Run locally

```bash
cd flashcard-share
python3 -m http.server 8081
```

Open http://localhost:8081

## Notes

- Uses separate `localStorage` keys from the personal 83-word deck, so the two apps never overwrite each other
- Friends can import a list (`German – English`) or add words one by one in Browse
