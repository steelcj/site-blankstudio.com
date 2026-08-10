# Running the BLNK Studio site locally

Version 1.0.0 — Status: Stable

## Description

This guide walks through building the BLNK Studio site on your own machine and viewing it in a browser before anything is pushed to GitHub or published by Netlify.

The site is an [Eleventy](https://www.11ty.dev/) static site. Eleventy reads the `src/` folder and writes a finished, plain-HTML copy of the site into `_site/`. Nothing in `_site/` is written by hand — it is deleted and regenerated on every build.

There are two commands, and they serve different purposes:

- `npm start` runs a local web server that rebuilds the site every time you save a file. This is the default for day-to-day work, and it is what you want almost always.
- `npm run build` produces the `_site/` folder once and exits. Use it to check that a production build succeeds, which is the same thing Netlify runs on deploy.

Both are described below. Neither one publishes anything or touches the live site.

We do not commit `_site/` to the repository. It is listed in `.gitignore`, because Netlify rebuilds it from source on every push, and a committed copy would only ever be stale.

## Prerequisites

You need Node.js and npm available on your machine. Eleventy 3 requires Node.js 18 or newer, and `netlify.toml` pins the deploy environment to Node.js 20, so any version from 18 up will match production closely enough for local work.

Confirm both are installed:

```bash
node --version
npm --version
```

Captured output from a working machine:

```text
v22.14.0
10.9.2
```

If either command reports `command not found`, install Node.js from [nodejs.org](https://nodejs.org/) — npm is bundled with it — and run the checks again before continuing.

Run every command in this guide from the project root, the folder containing `package.json`:

```bash
cd /home/initial/2-areas/development/sites/site-blankstudio.com
```

## Install dependencies

Do this once after cloning the repository, and again whenever `package.json` changes.

```bash
npm install
```

Captured output:

```text
added 129 packages, and audited 130 packages in 2s

36 packages are looking for funding
  run `npm fund` for details

4 high severity vulnerabilities
```

This creates a `node_modules/` folder in the project root. It is gitignored and is never published.

### A note on the vulnerability warning

The `4 high severity vulnerabilities` line is expected on this project as of the version of Eleventy currently pinned. We do not run `npm audit fix` as part of local setup, for two reasons:

- Every advisory in this tree is a denial-of-service issue in a build-time package (`brace-expansion`, `js-yaml`, `linkify-it`, `liquidjs`). These packages run on your machine during the build. They are not shipped to visitors — the published site is static HTML, CSS, and images, and contains none of this code.
- `npm audit fix` can change dependency versions and cause the local build to diverge from what Netlify builds.

Upgrading these is a deliberate maintenance decision, not a setup step. If you want to see the current detail yourself, run `npm audit`.

## View the site with live preview

This is the normal way to work on the site.

```bash
npm start
```

Captured output, abbreviated — the full listing names every page it writes:

```text
[11ty] Writing ./_site/index.html from ./src/index.html
[11ty] Writing ./_site/blog.html from ./src/blog.njk
[11ty] Writing ./_site/blog/high-converting-homepage/index.html from ./src/content/blog/high-converting-homepage.md (njk)
[11ty] Copied 29 Wrote 19 files in 0.15 seconds (v3.1.6)
[11ty] Watching…
[11ty] Server at http://localhost:8081/
```

Read the `Server at` line and open exactly that address. Eleventy's default port is 8080, but it moves to the next free port if 8080 is already taken — in the captured run above it chose 8081, because another program held 8080. Do not assume the port; take it from the output.

The server keeps running and occupies the terminal. Leave it running while you work, and see [Stopping the server](#stopping-the-server) when you are finished.

### Verify the preview is serving

In a second terminal, check that the main routes respond. Replace `8081` with whatever port your own `Server at` line reported:

```bash
for path in / /blog.html /blog/high-converting-homepage/ /about.html /admin/; do
  printf "%-38s" "$path"
  curl -s -o /dev/null -w "%{http_code}\n" "http://localhost:8081$path"
done
```

Captured output:

```text
/                                     200
/blog.html                            200
/blog/high-converting-homepage/       200
/about.html                           200
/admin/                               200
```

Every line should read `200`. A `404` means that page did not build — check the terminal running the server for an Eleventy error. A `000` or a connection error means the server is not running, or you are checking the wrong port.

A `404` on an address that does not exist is correct behaviour, not a fault:

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8081/nope-does-not-exist
```

Captured output:

```text
404
```

### Edit a file and watch it rebuild

With the server running, open any file under `src/` in an editor, make a change, and save it. Eleventy notices the save, rebuilds, and refreshes the page in your browser.

Captured output from the server terminal, after saving a change to a blog post:

```text
[11ty] File changed: ./src/content/blog/rebrand-or-refine.md
[11ty] Copied 29 Wrote 19 files in 0.03 seconds (v3.1.6)
[11ty] Watching…
```

The `File changed:` line naming the file you just saved, followed by a fresh `Wrote 19 files` line, confirms the watcher is working. If you save a file and no new lines appear, the watcher is not picking up that path — confirm the file is inside `src/`, since nothing outside it is watched.

Edit files in `src/` only. Editing `_site/` appears to work for a moment and is then silently overwritten by the next rebuild.

## Build the finished site

Use this to confirm a clean production build succeeds — the same command Netlify runs, per `netlify.toml`.

```bash
npm run build
```

Captured output, abbreviated:

```text
> blnk-studio-site@1.0.0 build
> eleventy

[11ty] Writing ./_site/404.html from ./src/404.html
[11ty] Writing ./_site/index.html from ./src/index.html
[11ty] Writing ./_site/blog.html from ./src/blog.njk
[11ty] Copied 29 Wrote 19 files in 0.13 seconds (v3.1.6)
```

The command exits when it finishes; no server is started. `Copied 29 Wrote 19 files` with no error lines above it is a successful build. If Eleventy reports a template error, the build has failed and Netlify would fail the same way — fix it before pushing.

`Copied` counts the static files passed through untouched (`css/`, `js/`, `assets/`, `admin/`, `robots.txt`, `sitemap.xml`). `Wrote` counts the pages Eleventy generated from templates and Markdown.

### Preview the built output

`npm start` is sufficient for nearly all work. Serve `_site/` directly only when you specifically want to check the finished artefact — for example, to confirm an asset path resolves without the dev server's help.

```bash
cd _site && python3 -m http.server 8083
```

In a second terminal:

```bash
for path in / /blog.html /blog/high-converting-homepage/ /css/home.css /assets/favicon.png; do
  printf "%-38s" "$path"
  curl -s -o /dev/null -w "%{http_code}\n" "http://localhost:8083$path"
done
```

Captured output:

```text
/                                     200
/blog.html                            200
/blog/high-converting-homepage/       200
/css/home.css                         200
/assets/favicon.png                   200
```

This server has no rebuild and no live reload. It shows the bytes on disk from the last `npm run build`, which is the point of using it. Remember to stop it, and to `cd` back to the project root, when you are done.

## Troubleshooting

### The site is not at localhost:8080

Symptom: `npm start` runs without error, but `http://localhost:8080/` does not show the site. Requests to port 8080 return an unexpected status rather than a connection failure.

Captured output from probing port 8080 during a real run:

```text
HTTP/1.0 501 Unsupported method ('HEAD')
Server: BaseHTTP/0.6 Python/3.12.3
```

Cause: an unrelated program — in this case a Python `http.server` — already held port 8080. Eleventy does not fail on a busy port. It selects the next free one and reports it, which was `8081` in this run. The response you see on 8080 comes from that other program, not from Eleventy.

Fix: read the `Server at` line in the `npm start` output and use the address it prints. To find out what is holding 8080:

```bash
ss -ltnp | grep :8080
```

To choose a port explicitly instead of letting Eleventy pick:

```bash
npx @11ty/eleventy --serve --port=8085
```

## Stopping the server

`npm start` leaves a Node process running and a port bound until you stop it. Stop it before closing the terminal.

In the terminal running the server, press `Ctrl+C`.

### Confirm it stopped

If the terminal was closed without `Ctrl+C`, or you are unsure whether the process is gone, check for it by name:

```bash
ps -eo pid,args | grep eleventy | grep -v grep
```

Captured output from a live server:

```text
157092 node /home/initial/2-areas/development/sites/blnk-studio-site/node_modules/.bin/eleventy --serve
```

Stop it using the process ID from the first column, then re-run the check:

```bash
kill 157092
ps -eo pid,args | grep eleventy | grep -v grep
```

Captured output after a successful stop:

```text
no eleventy processes remaining
```

No output at all from the `ps` command means the same thing — nothing matched. Confirm the port is released as well, substituting your own port number:

```bash
curl -s -o /dev/null -w "%{http_code}\n" --max-time 3 http://localhost:8081/
```

Captured output once the port is free:

```text
000
```

A `000` here means the connection was refused, which is the result you want. A `200` means a server is still answering on that port.

### Removing build output

`_site/` and `node_modules/` are both gitignored, so neither will ever appear in `git status` and neither needs cleaning up for a commit. To reclaim the disk space or force a genuinely clean rebuild:

```bash
rm -rf _site
npm run build
```

## Verification status

Every command and every block labelled "Captured output" in this guide was run against this repository on 2026-08-07, on Node.js v22.14.0 with npm 10.9.2 and Eleventy 3.1.6, and the output reproduced here is what those runs printed. Output shown as "abbreviated" is a verbatim excerpt of a longer real listing, with lines omitted but none altered.

## Changelog

- 1.0.0 (2026-08-07) — Initial guide covering prerequisites, install, live preview, production build, the port-conflict failure, and server cleanup.
