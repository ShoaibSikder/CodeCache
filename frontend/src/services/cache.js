const memoryCache = new Map();

const DEFAULT_TTL = 5 * 60 * 1000;
const STORAGE_PREFIX = "codecache:";

function now() {
  return Date.now();
}

function readStorage(key) {
  try {
    const raw = sessionStorage.getItem(STORAGE_PREFIX + key);
    if (!raw) return null;
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function writeStorage(key, entry) {
  try {
    sessionStorage.setItem(STORAGE_PREFIX + key, JSON.stringify(entry));
  } catch {
    // Storage can fail in private mode or when quota is full; memory cache still works.
  }
}

export function getCached(key) {
  const memoryEntry = memoryCache.get(key);
  if (memoryEntry) return memoryEntry;

  const storageEntry = readStorage(key);
  if (storageEntry) {
    memoryCache.set(key, storageEntry);
    return storageEntry;
  }

  return null;
}

export function setCached(key, data, ttl = DEFAULT_TTL) {
  const entry = {
    data,
    expiresAt: now() + ttl,
    savedAt: now(),
  };
  memoryCache.set(key, entry);
  writeStorage(key, entry);
  return entry;
}

export function isFresh(entry) {
  return Boolean(entry && entry.expiresAt > now());
}

export async function cachedRequest(key, request, options = {}) {
  const ttl = options.ttl ?? DEFAULT_TTL;
  const cached = getCached(key);

  if (isFresh(cached)) {
    return { data: cached.data, fromCache: true };
  }

  const response = await request();
  setCached(key, response.data, ttl);
  return { data: response.data, fromCache: false };
}

export function revalidateCached(key, request, onData, options = {}) {
  const ttl = options.ttl ?? DEFAULT_TTL;

  request()
    .then((response) => {
      setCached(key, response.data, ttl);
      onData?.(response.data);
    })
    .catch(() => {});
}

export function clearCacheByPrefix(prefix) {
  for (const key of memoryCache.keys()) {
    if (key.startsWith(prefix)) memoryCache.delete(key);
  }

  try {
    Object.keys(sessionStorage)
      .filter((key) => key.startsWith(STORAGE_PREFIX + prefix))
      .forEach((key) => sessionStorage.removeItem(key));
  } catch {
    // Ignore storage access failures.
  }
}
