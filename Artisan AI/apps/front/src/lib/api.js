// front/src/lib/api.js
const RAW_BASE =
  import.meta.env.VITE_API_BASE_URL ||
  import.meta.env.VITE_API_BASE ||
  'http://localhost:8080';

// normalize: no trailing slash
const BASE = RAW_BASE.replace(/\/+$/, '');

/** Internal: parse response safely (JSON if content-type says so). */
async function parseResponse(res) {
  const ct = res.headers.get('content-type') || '';
  const text = await res.text();
  const isJSON = ct.includes('application/json');
  try {
    return isJSON && text ? JSON.parse(text) : (text || null);
  } catch {
    return text || null;
  }
}

/** Core API call */
export async function api(path, init = {}) {
  const url = `${BASE}${path.startsWith('/') ? path : `/${path}`}`;

  const hasBody = init.body !== undefined && init.body !== null;
  const method = (init.method || 'GET').toUpperCase();

  // Auto-stringify JSON bodies
  let body = init.body;
  if (hasBody && typeof body === 'object' && !(body instanceof FormData) && !(body instanceof Blob)) {
    body = JSON.stringify(body);
  }

  // Only set content-type for JSON bodies (and not for FormData)
  const headers = {
    ...(hasBody && typeof init.body === 'object' && !(init.body instanceof FormData)
      ? { 'content-type': 'application/json' }
      : {}),
    ...(init.headers || {}),
  };

  const res = await fetch(url, { ...init, method, headers, body });
  const data = await parseResponse(res);

  if (!res.ok) {
    const msg = (data && (data.detail || data.message)) || `${res.status} ${res.statusText}`;
    const err = new Error(msg);
    err.status = res.status;
    err.data = data;
    throw err;
  }
  return data;
}

/** Convenience helpers */
export const apiGet   = (path, opts={}) => api(path, { ...opts, method: 'GET' });
export const apiPost  = (path, body, opts={}) => api(path, { ...opts, method: 'POST', body });
export const apiPatch = (path, body, opts={}) => api(path, { ...opts, method: 'PATCH', body });
export const apiDel   = (path, opts={}) => api(path, { ...opts, method: 'DELETE' });

/**
 * NDJSON/SSE reader (yield {delta|text|json} per line)
 * Usage:
 *   for await (const chunk of stream('/v1/marketing/taglines', { method:'POST', body:{...} })) { ... }
 */
export async function* stream(path, init = {}) {
  const url = `${BASE}${path.startsWith('/') ? path : `/${path}`}`;

  const hasBody = init.body !== undefined && init.body !== null;
  let body = init.body;
  if (hasBody && typeof body === 'object' && !(body instanceof FormData) && !(body instanceof Blob)) {
    body = JSON.stringify(body);
  }
  const headers = {
    ...(hasBody && typeof init.body === 'object' && !(init.body instanceof FormData)
      ? { 'content-type': 'application/json' }
      : {}),
    ...(init.headers || {}),
  };

  const res = await fetch(url, { ...init, headers, body });
  if (!res.ok || !res.body) {
    const data = await parseResponse(res);
    const msg = (data && (data.detail || data.message)) || `${res.status} ${res.statusText}`;
    throw new Error(msg);
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buf = '';

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });

    const lines = buf.split('\n');
    buf = lines.pop() ?? '';

    for (let raw of lines) {
      const line = raw.trim();
      if (!line) continue;

      // handle SSE "data: ..."
      const payload = line.startsWith('data:') ? line.slice(5).trim() : line;

      // try JSON first
      try {
        const obj = JSON.parse(payload);
        if (obj.delta)      yield { delta: obj.delta };
        else if (obj.text)  yield { text: obj.text };
        else                yield { json: obj };
        continue;
      } catch { /* not JSON */ }

      yield { text: payload };
    }
  }
}

