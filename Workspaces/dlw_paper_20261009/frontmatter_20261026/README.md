# Front matter: Abstract, Introduction, Conclusions (2026-10-26)

Rewrite of the three missing text blocks of `dlw-paper.html`, taken from the earlier
draft `report/dlw_paper_draft.html` and aligned with the present manuscript. Sections
4.4, 5.5 and Appendices A–D are deliberately untouched (still placeholders).

## What changed

| Block | Source | Change |
|---|---|---|
| `section#abstract` | composed (the draft has no abstract) | new, 240 words |
| `section#section-1` | draft `en-intro`, six paragraphs | kept verbatim except the roadmap paragraph and the naming |
| `section#section-6` | draft `en-conclusion`, five paragraphs | kept in structure; PE/PF claims and percentages replaced by the present results |
| `section#references` | draft reference list | 2 entries → 15 |
| `section-2.1/2.2/2.4` | in-text citations | `[1]`→`[5]` (Sheng–Yu), `[2]`→`[15]` (Hirota) |
| `appendix-G` | editorial guide | status note appended |

Naming: PE → Endpoint-SD, PF → Centered-SD, direct finite difference → collocated FD.
The draft's claim that "PE attains smaller maximum errors in both fields throughout the
four tests" is false for the present data and was replaced (5.2: Centered-SD is best in
`v` in all four tests; the `u` ordering is profile dependent).

## Numbers carried over from Section 5

60–87 (Endpoint/Centered `v`), 1.7–3.5 (FD/Centered `v`), 2.8 (soliton `u`), 7.3e-3
(CN vs RK4), 11.7/17.4 % and 6.0/5.6 % (adaptive mesh), 1.1 percentage points (frozen
control). No new computation; every number is quoted from Tables 2–5.

## Verification (`validation.json`)

- 26 sections; 21 byte-identical; changed = abstract, 1, 6, references, appendix-G,
  parent `section-2`, and the three citation-only sections 2.1/2.2/2.4.
- Citation-only sections differ in nothing but the citation number (checked after
  normalising `[n]`).
- 28 figures, 5 tables, 818 KaTeX spans (790 + 32 new), no `.katex-error`.
- Every reference 1–15 is cited in the body and present in the list.
- 4.4, 5.5 and Appendices A–D contain no `<p>`, figure, table or div.

## Files

- `publish_frontmatter.py` — publisher (replays from `before/dlw-paper.html`).
- `verify_frontmatter.py` — independent check.
- `manifest.json`, `validation.json` — hashes, counts.
- `before/dlw-paper.html` — pre-edit manuscript, `fd9cec1f…e583a1`.
- `shot_top.png` — headless Chrome render of the title, abstract and contents.

After this publication the manuscript hash is `65cf4aa7…b43af` (2,011,530 bytes).

## Open items (not part of this round)

- Section 4 is titled "Numerical formulation and linear stability" but 4.4 is empty;
  5.5 is empty. Either fill both, or drop the headings and adjust that title.
- Appendices A–D are empty and referenced nowhere.
- No author/affiliation/keywords block yet.
- Appendix G must be removed before submission.
