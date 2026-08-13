// Where the active client's branding lives, and what is inside it.
//
// A site is customised by one directory: branding/<client>/. Everything under
// it is client-owned — the palette, the fonts, the logos, and the seed content
// tree that declares which languages the site has and which sections it is
// made of. Directories starting with "_" are templates (branding/_template/)
// or parked clients, never the active one.
//
// Both the Eleventy config and src/_data/menu.js need to find that directory,
// and they must agree on which one it is, so the lookup lives here rather than
// being written twice.

const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const BRANDING_DIR = path.join(ROOT, "branding");

// The one active client directory name, or null if a checkout has none yet
// (the template repo before `npm run new-client`). Throws when more than one
// is present: the generators write a single brand.css and site.json, so two
// active clients would silently mean "whichever sorted first".
function activeClient() {
  if (!fs.existsSync(BRANDING_DIR)) return null;

  const clients = fs
    .readdirSync(BRANDING_DIR, { withFileTypes: true })
    .filter((d) => d.isDirectory() && !d.name.startsWith("_"))
    .map((d) => d.name);

  if (clients.length > 1) {
    throw new Error(
      `Multiple client branding directories (${clients.join(", ")}); exactly ` +
        "one un-prefixed branding/<client>/ is allowed."
    );
  }
  return clients[0] || null;
}

// Absolute path to a subdirectory of the active client, or null when either
// the client or that subdirectory is absent. `parts` is joined onto
// branding/<client>/, e.g. clientDir("content").
//
// Each top-level directory in there is a kind of client-owned material, named
// for what it is rather than for where it ends up: content/ is ingressed into
// src/content/, assets/ is published at /assets/, blocks/ is copied into
// src/_includes/blocks/. The tooling knows the destinations; the client
// directory does not have to mirror the repository's shape to say what it holds.
function clientDir(...parts) {
  const client = activeClient();
  if (!client) return null;
  const dir = path.join(BRANDING_DIR, client, ...parts);
  return fs.existsSync(dir) ? dir : null;
}

// The seed content tree: branding/<client>/content/. Its immediate children are
// locale directories — en-ca/ means the site has English (Canada) content,
// fr-ca/ means it has French (Canada) content — and the directories inside each
// of those are the site's sections.
function seedContentDir() {
  return clientDir("content");
}

module.exports = { ROOT, BRANDING_DIR, activeClient, clientDir, seedContentDir };
