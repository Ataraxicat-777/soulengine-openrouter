self.addEventListener("install", (event) => {
  console.log("[ServiceWorker] Install");
  self.skipWaiting(); // Activate immediately
});

self.addEventListener("activate", (event) => {
  console.log("[ServiceWorker] Activated");
});

self.addEventListener("fetch", (event) => {
  // Log all fetches (optional: add caching logic here)
  console.log("[ServiceWorker] Fetching:", event.request.url);
});
