# Abstract, Introduction and Conclusions — supplied text (v2, 2026-10-26)

The three blocks were replaced with the text supplied by the user (the "We study the integrable
semi-discretization…" abstract, the six-paragraph introduction and the five-paragraph
conclusions). Wording is unchanged; only markup, citation numbers and one added citation
sentence differ.

## Deviations from the supplied text

| Item | What was done |
|---|---|
| Math | every `$…$` segment converted to KaTeX inline math; 59 formulas, 0 render errors |
| Citations `[1]`, `[2]` | remapped to `[5]` (Sheng–Yu) and `[15]` (Hirota), matching the existing reference list; as written, `[1]` and `[2]` pointed at Boiti–Leon–Pempinelli and Wang–Zhou–Li |
| `[1,3,4]` | added after "compatible linear Lax problems" in ¶1 to keep refs 1–4 cited; written as `[1–4]` |
| Added material in ¶2 | the related-work material (refs 6–14) now sits directly after "…Darboux–Lax compatibility on a discrete grid", as "The same programme has been carried out for other integrable semi-discrete systems [6–9]…while the one-step integrators of Section 4 are classical [10]." The "Yet an important…" turn and the motivation sentence follow as in the supplied text |
| Dashes | the em dashes were converted to the `&mdash;` entity used elsewhere in the manuscript |

Everything else — sentence order, wording, the six-section roadmap — is verbatim.

## Verification (`validation.json`)

- Only `section#abstract`, `section#section-1`, `section#section-6` changed; 21 other sections
  byte-identical.
- 28 figures, 6 tables unchanged; 974 KaTeX spans overall (59 inside the three blocks), no
  `.katex-error`.
- References: all 15 cited again, 15 entries listed.
- Word counts: abstract 364, introduction 1047 in 6 paragraphs, conclusions 659 in 5.
- Seven literal phrases from the supplied text are asserted present.

## Files

- `publish_frontmatter_v2.py` — publisher, replays from `before/dlw-paper.html`.
- `verify_frontmatter_v2.py` — independent check.
- `manifest.json`, `validation.json`, `shot_top.png` (headless render of title + abstract).
- `before/dlw-paper.html` — previous state, `a8f88298…c22421f`.

Current manuscript: `38afe02b…a77b2ce`, 2,276,992 bytes.
