# branding/_original.com/

The original studio home page, taken apart into named blocks so it can be built
back up — here, or in a client site that wants one of its pieces.

This directory is `_`-prefixed, so it is a parked reference and never an active
client: `lib/branding.js` and every generator skip it, and nothing in it reaches
a build. Copying a file out of here into `src/` is what puts it on a site.

## How it is organized

Two levels, one for each half of a block's name:

    blocks/<role>/<pattern>.njk    the markup
    blocks/<role>/<pattern>.css    the styles that block owns
    blocks/_shared/*.css           what every block assumes

The **role** is what a block does for a reader — Statement, Credibility,
Catalogue, Position, Method, Endorsement, Feed, Conversion. The **pattern** is
how it is built and how it behaves — `hero-split`, `metric-row`, `card-grid`,
`step-list`. Role is the reason a block is on a page; pattern is what you get
when you drop it in. A role can hold more than one pattern, which is how
Credibility ends up with a counted metric row and a looping logo strip.

Each top-level directory in a branding directory is a kind of client-owned
material, named for what it is rather than for where it ends up: `content/` is
ingressed into `src/content/`, `assets/` is published at `/assets/`, and
`blocks/` is copied into `src/_includes/blocks/`. The tooling knows the
destinations, so a client directory says what it holds rather than mirroring the
repository's shape.

## The blocks

| Role | Pattern | Does | Acts |
| --- | --- | --- | --- |
| Statement | `hero-split` | Opens with the claim and the two primary actions | Animates on load, not on scroll |
| Statement | `spec-list` | States the operating facts: status, base, hours, response | Static; a fragment of `hero-split` |
| Credibility | `proof-band` | Numbers and client marks, in one ruled band | Both behaviours below |
| Credibility | `metric-row` | Counts the headline numbers | Counts up when scrolled into view |
| Credibility | `logo-marquee` | Shows the client logos | Loops for 40s, pauses on hover |
| Catalogue | `card-grid` | Lists what a visitor can buy | Reveals in a staggered grid |
| Position | `split-pillars` | Argues why this studio, in three pillars | Reveals; the page's one dark block |
| Method | `step-list` | Walks through how the work runs | Reveals step by step, each with a duration |
| Endorsement | `quote-block` | Lets a third party vouch | Reveals |
| Feed | `post-grid` | Surfaces recent writing | Reveals |
| Conversion | `cta-band` | Makes the closing ask | Reveals; already shared across five pages |

Every file's header records the role, the surface it paints, the motion it
carries, the data keys it reads, the anchor it answers to, its known issues, and
the exact source file and line range it was copied from.

`_shared/` holds what the blocks are written against and cannot be dropped
without: `foundations.css` (reset, `.container`, `.eyebrow`, buttons, arrow
links, headings), `section.css` (`.sec`, `.sec-head`, `.section-title`),
`motion.css` (`.reveal` and its delays), `reduced-motion.css`, and
`responsive.css` — one media-query stack that covers several blocks at once and
cannot be split per block without dividing selectors by hand.

## Using one

1. Copy the `.njk` into `src/_includes/blocks/<role>/` and include it from a
   page: `{% include "blocks/method/step-list.njk" %}`.
2. Copy the `.css` into `src/css/blocks/` and add it to that page's `css:` list
   in front matter, together with the `_shared/` files it names.
3. Supply the copy. Blocks read locale bundle keys (`t.home.process.s1Title`),
   so the keys have to exist in `src/_locales/<locale>.json` for every locale, or
   the page renders blank strings. A block's header lists exactly which keys.
4. Check the block's motion still works: `.reveal`, `.count` and `.marquee` are
   driven by `src/js/main.js`, which is already on every page.

Blocks are copies, not a framework. Nothing imports them and nothing keeps them
in step with `src/` — `npm run check:blocks` re-reads each header and reports any
file that has drifted from the lines it claims to be a copy of.

## What is not here yet

Only the home page has been taken apart. Five more patterns live on the other
pages and have not been extracted: the image band (`showcase` on services and
contact, `aband` on free-audit), the featured post card on the blog index, the
package price grid, the FAQ list, and the subscribe capture form. The heroes on
those pages are `hero--page` variants of `statement/hero-split`.

Nor is the copy here. A block ships its markup and its styles; the words it
renders still live in `src/_locales/`, and the images it points at still live in
an active client's `assets/`.
