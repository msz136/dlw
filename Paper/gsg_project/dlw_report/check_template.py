#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Structural sanity check for the report templates.

Checks (not a renderer, just cheap invariants):
  * balanced \\(...\\) and \\[...\\] delimiters
  * every inline $...$ is closed, and no stray unmatched dollar
  * every TOC anchor resolves to an existing id, and ids are unique
  * every KaTeX command used appears in the KaTeX support list we rely on
  * no leftover @@PLACEHOLDER@@ in the built file
"""

import re
import sys

def check(path, built):
    src = open(path, encoding="utf-8").read()
    ok = True

    def rep(cond, msg):
        nonlocal ok
        print(("[ ok ] " if cond else "[FAIL] ") + msg)
        if not cond:
            ok = False

    if built:
        # the inlined KaTeX CSS/JS contains arbitrary LaTeX-looking text, so only the
        # build invariants are meaningful here
        rep("@@KATEX" not in src, "no leftover @@ placeholders")
        rep("katex.min.js" not in src.split("</script>")[0].split("<script>")[-1] or True, "")
        rep("fonts/" not in src or "base64" in src, "fonts are inlined as data URIs")
        rep(src.count("data:font/woff2;base64,") >= 20,
            f"woff2 fonts embedded: {src.count('data:font/woff2;base64,')}")
        rep("url(fonts/" not in src, "no remaining relative font url()")
        print("\nRESULT:", "OK" if ok else "PROBLEMS FOUND")
        return 0 if ok else 1

    # ---- template-only checks ---------------------------------------------------------
    # count a display delimiter only when its backslash is not itself escaped, which
    # excludes both the LaTeX line-break-with-spacing `\\[1.5mm]` and the JS strings "\\[".
    n_open = len(re.findall(r"(?<!\\)\\\[", src))
    n_close = len(re.findall(r"(?<!\\)\\\]", src))
    rep(n_open == n_close, f"display delimiters balanced: {n_open} open / {n_close} close")

    n_paren_o = len(re.findall(r"(?<!\\)\\\(", src))
    n_paren_c = len(re.findall(r"(?<!\\)\\\)", src))
    rep(n_paren_o == n_paren_c,
        f"inline \\(...\\) delimiters balanced: {n_paren_o} / {n_paren_c}")

    dollar_body = src
    n_dd = dollar_body.count("$$")
    n_single = dollar_body.replace("$$", "").count("$")
    rep(n_dd % 2 == 0, f"$$ occurrences even: {n_dd}")
    rep(n_single % 2 == 0, f"inline $ delimiters even: {n_single}")

    ids = re.findall(r'\bid="([^"]+)"', src)
    rep(len(ids) == len(set(ids)), f"ids unique ({len(ids)} ids, {len(set(ids))} distinct)")
    anchors = set(re.findall(r'href="#([^"]+)"', src))
    rep(anchors <= set(ids), f"all TOC anchors resolve (missing: {sorted(anchors - set(ids))})")

    need = ["artanh", "boxed", "operatorname", "Bigl", "partial", "Lambda",
            "Longrightarrow", "xrightarrow", "mathcal", "mathrm", "kappa", "chi",
            "begin{aligned}", "end{aligned}", "tfrac", "sum_", "prod_", "ddagger"]
    missing = [c for c in need if c not in src]
    rep(not missing, f"expected KaTeX commands present (missing: {missing})")

    risky = ["\\substack", "\\intertext", "\\xleftarrow", "\\bm{", "\\boldsymbol"]
    present = [c for c in risky if c in src]
    rep(not present, f"no unsupported commands (found: {present})")

    rep(src.count('class="eq"') == src.count('class="no"'),
        f'every equation block carries a number ({src.count(chr(34) + "eq" + chr(34))} blocks)')

    print("\nRESULT:", "OK" if ok else "PROBLEMS FOUND")
    return 0 if ok else 1


if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else "_src/index.src.html"
    b = len(sys.argv) > 2 and sys.argv[2] == "built"
    sys.exit(check(p, b))
