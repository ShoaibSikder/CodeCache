// Memory Map + sessionStorage with a 5-minute TTL and stale revalidation (FR31).
const mem = new Map();
const TTL = 5 * 60 * 1000;
export async function cached(key, fetcher, ttl = TTL) {
  let hit = mem.get(key);
  if (!hit) { try { hit = JSON.parse(sessionStorage.getItem('cc:' + key)); } catch { /* ignore */ } }
  if (hit) {
    mem.set(key, hit);
    if (Date.now() - hit.t >= ttl) fetcher().then(v => store(key, v)).catch(() => {});
    return hit.v;
  }
  const v = await fetcher();
  store(key, v);
  return v;
}
function store(key, v) {
  const rec = { v, t: Date.now() };
  mem.set(key, rec);
  try { sessionStorage.setItem('cc:' + key, JSON.stringify(rec)); } catch { /* quota */ }
}
export function invalidate(prefix = '') {
  [...mem.keys()].filter(k => k.startsWith(prefix)).forEach(k => mem.delete(k));
  Object.keys(sessionStorage).filter(k => k.startsWith('cc:' + prefix)).forEach(k => sessionStorage.removeItem(k));
}
