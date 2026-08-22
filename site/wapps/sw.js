const CACHE_NAME = 'webapp-multitool-v1';
const ASSETS = [
  './icon-192.png',
  './icon-512.png',
  './wapp_multitool.html',
  './manifest.json'
];

// Install event: cache assets
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

// Fetch event: serve from cache if available
self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((response) => {
      return response || fetch(e.request);
    })
  );
});
