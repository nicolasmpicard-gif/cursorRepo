/* Network-first for vocabulary so phone caches pick up new words. */
const CACHE = "wortkarte-v8";
const ASSETS = [
  "./",
  "./index.html",
  "./styles.css?v=165",
  "./app.js?v=165",
  "./words.js?v=165",
  "./manifest.webmanifest",
  "./icon-192.png",
  "./icon-512.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key)))
    ).then(() => self.clients.claim())
  );
});

function isVocabularyRequest(url) {
  return /\/words\.js(?:$|\?)/.test(url.pathname + url.search) ||
    /\/app\.js(?:$|\?)/.test(url.pathname + url.search) ||
    /\/index\.html(?:$|\?)/.test(url.pathname + url.search) ||
    url.pathname.endsWith("/");
}

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;

  const url = new URL(request.url);

  // Always try network first for deck/app updates; fall back to cache offline.
  if (isVocabularyRequest(url) || request.mode === "navigate") {
    event.respondWith(
      fetch(request)
        .then((response) => {
          if (response && response.ok) {
            const copy = response.clone();
            caches.open(CACHE).then((cache) => cache.put(request, copy));
          }
          return response;
        })
        .catch(() => caches.match(request))
    );
    return;
  }

  event.respondWith(
    caches.match(request).then((cached) => {
      const network = fetch(request)
        .then((response) => {
          if (response && response.ok) {
            const copy = response.clone();
            caches.open(CACHE).then((cache) => cache.put(request, copy));
          }
          return response;
        })
        .catch(() => cached);

      return cached || network;
    })
  );
});
