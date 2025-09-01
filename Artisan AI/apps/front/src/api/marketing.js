// front/src/api/marketing.js
const BASE = import.meta.env.VITE_API_BASE || "http://localhost:8080";

// --- internal fetch wrapper ---
async function request(path, init = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "content-type": "application/json", ...(init.headers || {}) },
    ...init,
  });
  const txt = await res.text();
  const isJSON = (res.headers.get("content-type") || "").includes("application/json");
  const body = isJSON && txt ? JSON.parse(txt) : (txt || null);
  if (!res.ok) {
    const msg = body?.detail || body?.message || `${res.status} ${res.statusText}`;
    throw new Error(msg);
  }
  return body;
}

/**
 * GET /v1/marketing/suggest?product_id=&channel=&lang=
 * -> { hashtags: string[], best_time: string, ... }
 */
export async function suggest({ productId, channel = "instagram", lang = "en", signal } = {}) {
  const qs = new URLSearchParams({
    product_id: String(productId),
    channel,
    lang,
  }).toString();
  return request(`/v1/marketing/suggest?${qs}`, { signal });
}

/**
 * POST /v1/marketing/{product_id}/post?channel=&lang=&tone=
 * Body: array of strings (extra tags) OR null
 * -> { ok: true, item: {...} }
 */
export async function createPost({
  productId,
  channel = "instagram",
  lang = "en",
  tone = "friendly",
  extraTags = null, // string[] | null
  signal,
} = {}) {
  const qs = new URLSearchParams({ channel, lang, tone }).toString();
  const body =
    extraTags === null ? "null" : JSON.stringify(Array.isArray(extraTags) ? extraTags : [String(extraTags)]);
  return request(`/v1/marketing/${encodeURIComponent(productId)}/post?${qs}`, {
    method: "POST",
    body,
    signal,
  });
}