// Minimal static file server for the built Vite frontend (frontend/dist),
// used when deploying the frontend as its own Catalyst AppSail app.
//
// Why this exists: AppSail apps are long-running processes, not "static
// hosting" — something has to actually listen on a port and serve the
// files. This has zero npm dependencies on purpose, so there's nothing
// extra to install at runtime beyond what `npm run build` already needs.
//
// It also does SPA fallback (unknown paths -> index.html) so client-side
// routes like /dashboard or /cases/123 don't 404 on refresh.
//
// It ALSO reverse-proxies /api/* to the backend AppSail app server-side
// (see proxyApi below). That's not stylistic — Catalyst's edge (ZGS / the
// Zoho ALB in front of AppSail) answers cross-origin OPTIONS preflights
// itself with a bare 200 and no Access-Control-Allow-Origin header, before
// the request ever reaches the FastAPI container. No CORSMiddleware config
// on the backend can fix that, because the backend never sees the
// preflight. Routing /api/* through this same-origin proxy means the
// browser never issues a cross-origin request in the first place, so
// there's no preflight for the edge to swallow.

import http from "node:http";
import https from "node:https";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DIST_DIR = path.join(__dirname, "dist");

// Catalyst injects the port to listen on via X_ZOHO_CATALYST_LISTEN_PORT.
// Fall back to 3000 for local testing (`node server.js`).
const PORT = process.env.X_ZOHO_CATALYST_LISTEN_PORT || process.env.PORT || 3000;

// Backend origin to proxy /api/* to. Set via app-config.json / AppSail env
// vars. Falls back to the known dev backend URL so local `node server.js`
// testing still works without extra setup.
const API_PROXY_TARGET =
  process.env.API_PROXY_TARGET ||
  "https://ksp-crime-ai-backe-50043881632.development.catalystappsail.in";

/**
 * Forwards a request under /api/* to API_PROXY_TARGET, server-side.
 * Server-to-server requests aren't subject to browser CORS at all, so the
 * edge's OPTIONS-swallowing behavior never comes into play here — this
 * process is the one making (and awaiting) the real request.
 */
function proxyApi(req, res) {
  const target = new URL(API_PROXY_TARGET);
  const upstreamHeaders = { ...req.headers, host: target.host };
  // Let Node/https compute its own content-length for what actually goes
  // out, rather than trusting the inbound value.
  delete upstreamHeaders["content-length"];

  const proxyReq = https.request(
    {
      protocol: target.protocol,
      hostname: target.hostname,
      port: target.port || 443,
      path: req.url, // includes /api/v1/... plus query string
      method: req.method,
      headers: upstreamHeaders,
    },
    (proxyRes) => {
      res.writeHead(proxyRes.statusCode || 502, proxyRes.headers);
      proxyRes.pipe(res);
    }
  );

  proxyReq.on("error", (err) => {
    console.error("Upstream API proxy error:", err.message);
    if (!res.headersSent) {
      res.writeHead(502, { "Content-Type": "application/json" });
    }
    res.end(JSON.stringify({ error: "Bad gateway", detail: err.message }));
  });

  req.pipe(proxyReq);
}

const MIME_TYPES = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".webp": "image/webp",
  ".ico": "image/x-icon",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
  ".ttf": "font/ttf",
  ".txt": "text/plain; charset=utf-8",
  ".map": "application/json; charset=utf-8",
};

function safeJoin(base, target) {
  const targetPath = path.posix.normalize("/" + target);
  return path.join(base, targetPath);
}

const server = http.createServer((req, res) => {
  const urlPath = decodeURIComponent((req.url || "/").split("?")[0]);

  if (urlPath.startsWith("/api/")) {
    proxyApi(req, res);
    return;
  }

  let filePath = safeJoin(DIST_DIR, urlPath === "/" ? "index.html" : urlPath);

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      // SPA fallback: unknown routes serve index.html so react-router
      // can take over client-side.
      filePath = path.join(DIST_DIR, "index.html");
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || "application/octet-stream";

    fs.readFile(filePath, (readErr, data) => {
      if (readErr) {
        res.writeHead(500, { "Content-Type": "text/plain" });
        res.end("Internal Server Error");
        return;
      }
      res.writeHead(200, { "Content-Type": contentType });
      res.end(data);
    });
  });
});

server.listen(PORT, () => {
  console.log(`Frontend static server listening on port ${PORT}`);
  console.log(`Serving directory: ${DIST_DIR}`);
});
