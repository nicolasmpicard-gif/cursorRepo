const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...CORS },
  });
}

async function readStore(env) {
  if (env && env.PROFILES) {
    const raw = await env.PROFILES.get("profiles", { type: "json" });
    if (raw && Array.isArray(raw.profiles)) return raw;
  }
  // Cache API fallback store
  try {
    const cache = caches.default;
    const hit = await cache.match("https://wortkarte.internal/profiles");
    if (hit) return await hit.json();
  } catch (_) {}
  return { profiles: [] };
}

async function writeStore(env, data) {
  if (env && env.PROFILES) {
    await env.PROFILES.put("profiles", JSON.stringify(data));
  }
  try {
    const cache = caches.default;
    const res = new Response(JSON.stringify(data), {
      headers: { "Content-Type": "application/json", "Cache-Control": "max-age=31536000" },
    });
    await cache.put("https://wortkarte.internal/profiles", res);
  } catch (_) {}
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: CORS });
    }

    if (url.pathname === "/health") {
      return json({ ok: true });
    }

    if (url.pathname === "/profiles" && request.method === "GET") {
      const store = await readStore(env);
      return json({
        count: store.profiles.length,
        profiles: store.profiles.slice().sort((a, b) => (b.createdAt || 0) - (a.createdAt || 0)),
      });
    }

    if (url.pathname === "/profiles" && request.method === "POST") {
      let body = {};
      try {
        body = await request.json();
      } catch (_) {
        return json({ error: "Invalid JSON" }, 400);
      }
      const name = String(body.name || "").trim().slice(0, 80);
      if (!name) return json({ error: "name required" }, 400);

      const store = await readStore(env);
      const event = {
        id: `p_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
        name,
        createdAt: Date.now(),
        userAgent: String(body.userAgent || "").slice(0, 180),
        source: String(body.source || "share").slice(0, 40),
      };
      // De-dupe exact same name within 30s to reduce double-taps
      const recent = store.profiles.find(
        (p) => p.name.toLowerCase() === name.toLowerCase() && event.createdAt - (p.createdAt || 0) < 30000
      );
      if (!recent) {
        store.profiles.push(event);
        await writeStore(env, store);
      }
      return json({ ok: true, profile: event, count: store.profiles.length }, 201);
    }

    return json({ error: "Not found" }, 404);
  },
};
