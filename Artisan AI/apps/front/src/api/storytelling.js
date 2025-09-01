// front/src/api/marketing.js
const BASE = import.meta.env.VITE_API_BASE || "http://localhost:8080";

// Small helper to fetch+parse and surface API errors nicely
async function request(path, init = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "content-type": "application/json", ...(init.headers || {}) },
    ...init,
  });
  const text = await res.text();
  const isJSON = (res.headers.get("content-type") || "").includes("application/json");
  const body = isJSON && text ? JSON.parse(text) : (text || null);
  if (!res.ok) {
    const msg = body?.detail || body?.message || `${res.status} ${res.statusText}`;
    throw new Error(msg);
  }
  return body;
}

/**
 * GET /v1/marketing/suggest
 * Query: product_id, channel, lang
 * Returns hashtags + best_time
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
 * POST /v1/marketing/{product_id}/post
 * Query: channel, lang, tone
 * Body: array of strings (extra tags) or null
 *
 * Example:
 *   await createPost({
 *     productId: "p1",
 *     channel: "instagram",
 *     lang: "en",
 *     tone: "friendly",
 *     extraTags: ["handmade", "supportlocal"]
 *   })
 */
export async function createPost({
  productId,
  channel = "instagram",
  lang = "en",
  tone = "friendly",
  extraTags = null, // array of strings or null
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
