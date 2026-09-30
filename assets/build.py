#!/usr/bin/env python3
"""Build the profile README's SVG cards, section headings and link buttons.

Every graphic is written twice, as *-light.svg and *-dark.svg, and the README
switches between them with <picture> + prefers-color-scheme. Edit the data
below and run `python3 assets/build.py`; output goes to assets/ui/.

SVG has no text wrapping, so descriptions are given as explicit lines
(keep each one under ~46 characters).
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent / "ui"
FONT = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, "
        "'PingFang SC', 'Microsoft YaHei', 'Noto Sans CJK SC', sans-serif")

THEMES = {
    "light": dict(bg="#FFFFFF", border="#E1ECF2", title="#243D50", text="#547082",
                  muted="#7794A5", chip="#F2F7FA", gold="#E7B844", link="#33536A"),
    "dark": dict(bg="#0D1117", border="#30363D", title="#E6EDF3", text="#9DB1BF",
                 muted="#7D93A3", chip="#161D26", gold="#E7B844", link="#9CC9DF"),
}

# name: (light accent, light tint, dark accent, dark tint)
ACCENTS = {
    "blue":   ("#2F86B4", "#E3F2F9", "#6CC0E6", "#12303F"),
    "gold":   ("#C98E10", "#FCF1D6", "#F0C24E", "#3A2E10"),
    "green":  ("#2E9A68", "#E1F4EA", "#5FD19A", "#0F3324"),
    "clay":   ("#C95C34", "#FBE8DF", "#F08A62", "#3D1F14"),
    "slate":  ("#4A6A85", "#E7EEF4", "#9AB6CE", "#1C2A36"),
    "violet": ("#6D5DC4", "#EEEBFA", "#A597F2", "#262045"),
}

# 24x24 stroke icons (Lucide-style). "{a}" is replaced by the accent colour.
ICONS = {
    "book": '<path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z"/>'
            '<path d="M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z"/>',
    "film": '<rect x="2" y="4" width="20" height="16" rx="3"/>'
            '<path d="M10 9l5 3-5 3z" fill="{a}"/>',
    "shuttle": '<circle cx="12" cy="18.5" r="2.8"/>'
               '<path d="M9.8 16.6 6 4.5M12 15.7V3.5M14.2 16.6 18 4.5M7.3 9h9.4"/>'
               '<path d="M6 4.5Q12 2.4 18 4.5"/>',
    "core": '<circle cx="12" cy="12" r="9.5"/><circle cx="12" cy="12" r="5.6" stroke-opacity=".45"/>'
            '<circle cx="12" cy="12" r="2.2" fill="{a}"/><path d="M12 2.5v5.4" stroke-dasharray="1.4 1.8"/>',
    "server": '<rect x="3" y="3" width="18" height="7.5" rx="2"/><rect x="3" y="13.5" width="18" height="7.5" rx="2"/>'
              '<path d="M7 6.75h.01M7 17.25h.01" stroke-width="2.6"/>',
    "clipboard": '<rect x="8" y="2" width="8" height="4" rx="1"/>'
                 '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>'
                 '<path d="m9 14 2 2 4-4"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/>'
             '<path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "pen": '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "page": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
            '<path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>',
}

PROJECTS = [
    dict(slug="ai-course", icon="book", accent="blue", title="AI Full-Stack Course",
         kicker="Tutorial · 254 chapters · in Chinese",
         lines=["An illustrated deep dive into LLM training,",
                "agent engineering, RAG and Transformers."],
         chips=["HTML", "PyTorch", "LLM", "RAG"]),
    dict(slug="ai-history", icon="film", accent="gold", title="The History of AI",
         kicker="Films rendered entirely from code",
         lines=["Canvas animation and a synthesized score,",
                "in 2-minute and 5-minute bilingual cuts."],
         chips=["JavaScript", "Canvas", "Python"]),
    dict(slug="bad-buddies", icon="shuttle", accent="green", title="BAD球友",
         kicker="WeChat mini-program · live",
         lines=["Runs amateur badminton meetups: sign-ups,",
                "auto pairings, live scoring, skill ratings."],
         chips=["Spring Boot", "WeChat", "MySQL"]),
    dict(slug="earthcore", icon="core", accent="clay", title="Earthcore Clicker",
         kicker="Browser game · play online",
         lines=["An original incremental game: start with a",
                "spoon and dig all the way to the core."],
         chips=["TypeScript", "Vite"]),
    dict(slug="tinysc", icon="server", accent="slate", title="tinysc",
         kicker="Servlet container · alpha",
         lines=["A lightweight Servlet container built for",
                "single-WAR deployment on Java 8."],
         chips=["Java 8", "Servlet 3.1", "Maven"]),
    dict(slug="quarantine-quiz", icon="clipboard", accent="violet", title="Quarantine Inspector Quiz",
         kicker="Exam prep · web app",
         lines=["Practice by module and sit mock exams for",
                "the cattle & sheep quarantine inspector exam."],
         chips=["HTML", "JavaScript"]),
]

SECTIONS = {"projects": "Featured projects", "stack": "Tech stack", "activity": "GitHub activity"}

LINKS = [("site", "globe", "carljings.top"), ("blog", "pen", "Blog"),
         ("email", "mail", "Email"), ("csdn", "page", "CSDN")]


def icon(name, colour, x, y, size=24, width=2):
    s = size / 24
    body = ICONS[name].replace("{a}", colour)
    return (f'<g transform="translate({x} {y}) scale({s:g})" fill="none" stroke="{colour}" '
            f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round">{body}</g>')


def svg(w, h, label, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(label)}">\n'
            f'<g font-family="{FONT}">\n{body}\n</g>\n</svg>\n')


# Helvetica/Arial advance widths in 1/1000 em (regular weight), used to size
# pills and place rules. Viewers' fonts differ a little, so text in pills is
# centred and never stretched.
_W = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
              [667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833,
               722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611]))
_W.update(zip("abcdefghijklmnopqrstuvwxyz",
              [556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833,
               556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500]))
_W.update({c: 556 for c in "0123456789"})
_W.update({" ": 278, ".": 278, ",": 278, ":": 278, "·": 278, "-": 333, "&": 667, "@": 1015})


def text_width(s, px, bold=False):
    em = sum(1000 if ord(c) > 0x2E80 else _W.get(c, 556) for c in s) / 1000
    return em * px * (1.07 if bold else 1)


def project_card(p, mode):
    t = THEMES[mode]
    la, lt, da, dt = ACCENTS[p["accent"]]
    accent, tint = (la, lt) if mode == "light" else (da, dt)
    W, H = 400, 164          # card size; the canvas adds a 10px gutter right and below
    parts = [
        f'<defs><clipPath id="c"><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16"/></clipPath></defs>',
        f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="{t["bg"]}"/>',
        f'<g clip-path="url(#c)"><circle cx="{W-18}" cy="14" r="46" fill="none" stroke="{tint}" stroke-width="12"/></g>',
        f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{t["border"]}"/>',
        f'<path d="M{W-34} 30l8-8M{W-32.5} 22H{W-26}v6.5" fill="none" stroke="{t["muted"]}" '
        f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<rect x="22" y="22" width="42" height="42" rx="12" fill="{tint}"/>',
        icon(p["icon"], accent, 31, 31),
        f'<text x="78" y="41" font-size="18" font-weight="700" fill="{t["title"]}">{escape(p["title"])}</text>',
        f'<text x="78" y="60" font-size="12.5" fill="{t["muted"]}">{escape(p["kicker"])}</text>',
    ]
    for i, line in enumerate(p["lines"]):
        parts.append(f'<text x="22" y="{92 + 19 * i}" font-size="14" fill="{t["text"]}">{escape(line)}</text>')
    x = 22
    for chip in p["chips"]:
        w = text_width(chip, 11) + 20
        parts.append(f'<rect x="{x:.1f}" y="124" width="{w:.1f}" height="19" rx="9.5" fill="{t["chip"]}"/>')
        parts.append(f'<text x="{x + w / 2:.1f}" y="137.5" font-size="11" text-anchor="middle" '
                     f'fill="{t["text"]}">{escape(chip)}</text>')
        x += w + 6
    label = f'{p["title"]}: {p["kicker"]}. {" ".join(p["lines"])}'
    return svg(W + 10, H + 10, label, "\n".join(parts))


def section(title, mode):
    t = THEMES[mode]
    W, H = 822, 40          # matches the width of the two-card grid on the profile page
    label = title.upper()
    tl = text_width(label, 15, bold=True) + 2.5 * (len(label) - 1)   # 2.5px letter spacing
    end = 38 + tl
    body = "\n".join([
        f'<rect x="0" y="22" width="26" height="3" rx="1.5" fill="{t["gold"]}"/>',
        f'<text x="38" y="28" font-size="15" font-weight="700" textLength="{tl:.1f}" lengthAdjust="spacing" fill="{t["title"]}">{escape(label)}</text>',
        f'<path d="M{end + 16:.0f} 23.5H{W}" stroke="{t["border"]}"/>',
    ])
    return svg(W, H, title, body)


def link_button(icon_name, label, mode):
    t = THEMES[mode]
    H = 32
    W = round(38 + text_width(label, 13, bold=True) + 16)
    body = "\n".join([
        f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="{H/2 - .5}" fill="{t["bg"]}" stroke="{t["border"]}"/>',
        icon(icon_name, t["link"], 15, 9, size=14, width=2.2),
        f'<text x="38" y="20.5" font-size="13" font-weight="600" fill="{t["link"]}">{escape(label)}</text>',
    ])
    return svg(W + 6, H, label, body)


def main():
    OUT.mkdir(exist_ok=True)
    for mode in THEMES:
        for p in PROJECTS:
            (OUT / f'project-{p["slug"]}-{mode}.svg').write_text(project_card(p, mode), encoding="utf-8")
        for slug, title in SECTIONS.items():
            (OUT / f"section-{slug}-{mode}.svg").write_text(section(title, mode), encoding="utf-8")
        for slug, icon_name, label in LINKS:
            (OUT / f"link-{slug}-{mode}.svg").write_text(link_button(icon_name, label, mode), encoding="utf-8")
    print(f"wrote {len(list(OUT.glob('*.svg')))} files to {OUT}")


if __name__ == "__main__":
    main()
