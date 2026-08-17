# Wortkarte — Classroom share deck (free)

Blank flashcard app your classmates can each use to build their own word bank.

## Share this link

https://raw.githack.com/nicolasmpicard-gif/cursorRepo/gh-pages/share/index.html

## How it works (free hosting)

- Hosted as a static site (no paid backend)
- Each classmate opens the link on their phone/laptop
- They create a **profile with their name**
- Words and study progress stay in that browser (`localStorage`)
- Profiles on the same device stay separate; different phones never share data

## Tips for class

1. Send everyone the link above
2. Each person taps **Create my deck** and enters their name
3. Add words in Browse (`German – English` import works too)
4. Use **Export** occasionally so clearing browser data doesn’t lose the deck

## Limits

- Free and private to the device/browser — there is no cloud sync or shared class server
- To move words to another phone, Export on one device and Import on the other

## Run locally

```bash
cd flashcard-share
python3 -m http.server 8081
```
