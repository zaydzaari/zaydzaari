#!/usr/bin/env python3
"""
generate_profile.py  ·  renders every SVG on github.com/zaydzaari

One design system, one script. Curated content (what each project is and the
boundaries it keeps) lives in CONTENT below and was written from the projects'
own READMEs. Everything numeric (repo counts, stars, languages, push dates,
contributions) is fetched from the public GitHub API at run time; nothing is
hard-coded or estimated.

    python scripts/generate_profile.py                   # live (uses GITHUB_TOKEN if set)
    python scripts/generate_profile.py --snapshot x.json # offline, from a saved dataset

Standard library only. ~10 API requests per run.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import math
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

LOGIN = "zaydzaari"
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# ──────────────────────────────────────────────────────────── design tokens ──
BG, PANEL, EDGE, GRID = "#0a0a0c", "#0e0e11", "#24242a", "#17171b"
INK, INK2, DIM, FAINT = "#ede8e2", "#a7a29c", "#66625d", "#3a3836"
RED, RED_D, RED_G = "#c8102e", "#5e0a18", "#ff4058"
GLOW = 'filter="url(#glow)"'
MONO = "ui-monospace,'SFMono-Regular','JetBrains Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "'Inter','Helvetica Neue',-apple-system,'Segoe UI',Arial,sans-serif"
W = 1280  # every asset shares this width so they stack into one column

# Short IDs used everywhere (hero topology, cards, constellation, toolchain).
IDS = {
    "linkscribe": "LS", "HomePC": "HP", "RemoteCraft": "RC",
    "geographic-training-diversity-forest-loss": "FL",
    "studymaster-ai": "SM", "trident-fps": "TR",
}

# ─────────────────────────────────────────────── curated, sourced content ──
PLANES = [
    dict(
        repo="linkscribe", file="plane-linkscribe.svg", title="LinkScribe",
        kicker="PLANE 01 · AGENT INFRASTRUCTURE", status="RELEASED · v0.1.2",
        line="Hands coding agents an English transcript of a public YouTube, TikTok or "
             "Instagram link. Transcription runs locally on a 2-core ARM VPS.",
        flow=[("agent", ">"), ("FastAPI queue", ">"), ("yt-dlp", ">"),
              ("FFmpeg 16 kHz", ">"), ("whisper.cpp", "")],
        note="92 s clip → ~36 s on the reference box",
        boundary=["one worker, so no job can starve the server",
                  "no LLM runs on the VPS",
                  "media deleted after every job"],
        stack="Python · FastAPI · SQLite · whisper.cpp · systemd · Nginx · ARM64",
    ),
    dict(
        repo="HomePC", file="plane-homepc.svg", title="HomePC",
        kicker="PLANE 02 · DEVICE CONTROL", status="v2 · PRIVATE TEST",
        line="Turns a Windows PC into Google Home switches without opening a single "
             "inbound port on the machine.",
        flow=[("Google Home", ">"), ("CF Worker", ">"), ("Durable Object", "<"),
              (".NET agent", ">"), ("action registry", "")],
        note="the PC dials out over WSS; nothing dials in",
        boundary=["no inbound port, no remote shell",
                  "a fixed allow-list of actions",
                  "power actions disabled by default"],
        stack="C# · .NET 8 · TypeScript · Cloudflare Workers · OAuth 2.0 · DPAPI",
    ),
    dict(
        repo="RemoteCraft", file="plane-remotecraft.svg", title="RemoteCraft",
        kicker="PLANE 03 · SERVER CONTROL", status="ALPHA",
        line="Runs Vanilla Minecraft servers on a Linux VPS from a web dashboard, "
             "without handing anyone a terminal.",
        flow=[("dashboard", ">"), ("FastAPI", ">"), ("validated ops", ">"),
              ("SSH + known_hosts", ">"), ("screen · java", "")],
        note="structured operations in, quoted commands out",
        boundary=["no general-purpose shell, ever",
                  "unknown SSH hosts rejected",
                  "every JAR checked against Mojang's SHA-1"],
        stack="Python · FastAPI · Paramiko · Linux · GNU Screen · Bash",
    ),
]

STUDY = dict(
    repo="geographic-training-diversity-forest-loss", file="study-forest-loss.svg",
    kicker="FIELD STUDY · REMOTE SENSING", status="MANUSCRIPT IN PREPARATION",
    title="Geographic diversity × spectral modality",
    line="Under a fixed data budget, does multispectral Sentinel-2 keep its edge over RGB "
         "as forest-loss models train on more regions of the Brazilian Amazon?",
    figures=[("107", "configurations"), ("642", "models trained"),
             ("2,568", "zero-shot evaluations"), ("48", "patches per model, fixed")],
    # interaction slope per doubling of N, F1, with 95% percentile bootstrap interval
    ci=(0.0183423431, -0.0169627549, 0.0578745415),
    verdict="No clear evidence the advantage changes with region count.",
    boundary="test regions sealed until a single final evaluation",
    stack="Python · PyTorch · rasterio · Sentinel-2 · 3 seeds",
)

BENCH = [
    dict(repo="studymaster-ai", file="bench-studymaster.svg", title="StudyMaster AI",
         kicker="SHIPPED · PRODUCT", status="LIVE ON VERCEL",
         line="Turns study material into summaries, quizzes, mind maps and spaced "
              "repetition, with an AI tutor that can read your PDFs.",
         stack="React · Express · Gemini API · i18next"),
    dict(repo="trident-fps", file="bench-trident.svg", title="TRIDENT",
         kicker="LAB · AGENTIC-CODING BENCHMARK", status="LAB",
         line="A browser 3D tactical shooter built as a benchmark run in Google Antigravity: "
              "authoritative WebSocket server, four agents, round economy.",
         stack="TypeScript · Three.js · React · ws · Vitest"),
]

TOOLCHAIN = [
    ("BUILD", "Python · TypeScript · JavaScript · C# / .NET 8", "LS RC FL TR SM HP"),
    ("SERVE", "FastAPI · Express · SQLite job queues · WebSockets · Workers + Durable Objects", "LS RC SM TR HP"),
    ("INFER", "whisper.cpp · FFmpeg · yt-dlp · PyTorch · Gemini / OpenRouter", "LS FL SM"),
    ("GUARD", "bearer tokens · OAuth 2.0 · SSH known_hosts · DPAPI · rate limits · checksums", "LS RC HP SM"),
    ("RUN",   "Linux · ARM64 · systemd · Nginx + certbot · Vercel", "LS RC SM TR"),
    ("PROVE", "pytest · Vitest · GitHub Actions CI · fixed seeds", "LS RC HP TR FL"),
]

# Constellation: angle = theme, radius = age (newest nearest the core).
THEMES = {
    "linkscribe": ("AGENT INFRA", -90),
    "RemoteCraft": ("CONTROL PLANE", 180),
    "HomePC": ("CONTROL PLANE", -142),
    "geographic-training-diversity-forest-loss": ("RESEARCH", -28),
    "trident-fps": ("LAB", 22),
    "studymaster-ai": ("PRODUCT", 122),
}
LINKS = [  # (a, b, what they actually share)
    ("linkscribe", "RemoteCraft", "FastAPI", 0.3),
    ("RemoteCraft", "HomePC", "allow-listed actions"),
    ("HomePC", "trident-fps", "WebSockets"),
    ("trident-fps", "studymaster-ai", "React"),
    ("linkscribe", "geographic-training-diversity-forest-loss", "model inference"),
    ("studymaster-ai", "linkscribe", "LLM tooling"),
]


# ────────────────────────────────────────────────────────────── data layer ──
def _get(url: str, token: str | None, accept="application/vnd.github+json", data=None):
    req = urllib.request.Request(url, data=data, headers={
        "Accept": accept, "User-Agent": f"{LOGIN}-profile-generator",
        **({"Authorization": f"Bearer {token}"} if token else {}),
        **({"Content-Type": "application/json"} if data else {}),
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode()


def fetch_live() -> dict:
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    api = "https://api.github.com"
    user = json.loads(_get(f"{api}/users/{LOGIN}", tok))
    raw = json.loads(_get(f"{api}/users/{LOGIN}/repos?per_page=100&type=owner&sort=pushed", tok))
    repos = []
    for r in raw:
        langs = {} if r["fork"] else json.loads(_get(r["languages_url"], tok))
        repos.append(dict(name=r["name"], description=r["description"], language=r["language"],
                          stars=r["stargazers_count"], fork=r["fork"], archived=r["archived"],
                          created=r["created_at"], pushed=r["pushed_at"],
                          homepage=r["homepage"], languages=langs))
    return dict(user=dict(login=LOGIN, name=user.get("name"),
                          public_repos=user.get("public_repos"), followers=user.get("followers")),
                repos=repos, calendar=fetch_calendar(tok),
                now=dt.datetime.now(dt.timezone.utc).isoformat())


def fetch_calendar(tok: str | None) -> list | None:
    """Daily contributions for the past year. GraphQL first, public HTML fallback."""
    if tok:
        q = {"query": "query($l:String!){user(login:$l){contributionsCollection{contributionCalendar"
                      "{weeks{contributionDays{date contributionCount}}}}}}", "variables": {"l": LOGIN}}
        try:
            d = json.loads(_get("https://api.github.com/graphql", tok, data=json.dumps(q).encode()))
            weeks = d["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
            return [[x["date"], x["contributionCount"]] for w in weeks for x in w["contributionDays"]]
        except Exception as e:  # noqa: BLE001
            print(f"  graphql calendar unavailable ({e}); trying public page", file=sys.stderr)
    try:
        page = _get(f"https://github.com/users/{LOGIN}/contributions", None, accept="text/html")
    except Exception as e:  # noqa: BLE001
        print(f"  calendar unavailable ({e})", file=sys.stderr)
        return None
    ids = dict(re.findall(r'data-date="(\d{4}-\d\d-\d\d)"[^>]*?id="([^"]+)"', page))
    tips = dict(re.findall(r'<tool-tip[^>]*for="([^"]+)"[^>]*>\s*(No|\d+) contribution', page))
    if not ids:
        return None
    return sorted([d, 0 if tips.get(i, "No") == "No" else int(tips[i])] for d, i in ids.items())


def derive(data: dict) -> dict:
    now = dt.datetime.fromisoformat(data["now"].replace("Z", "+00:00"))
    repos = data["repos"]
    own = [r for r in repos if not r["fork"] and r["name"] != LOGIN]
    forks = [r for r in repos if r["fork"]]
    by = {r["name"]: r for r in repos}
    langs: dict[str, int] = {}
    used_in: dict[str, int] = {}
    for r in own:
        for k, v in r["languages"].items():
            langs[k] = langs.get(k, 0) + v
            used_in[k] = used_in.get(k, 0) + 1
    total = sum(langs.values()) or 1
    ranked = sorted(langs.items(), key=lambda kv: -kv[1])
    last = max(own, key=lambda r: r["pushed"]) if own else None
    cal = data.get("calendar")
    if cal:
        cutoff = (now.date() - dt.timedelta(days=364)).isoformat()
        cal = [c for c in cal if c[0] >= cutoff and c[0] <= now.date().isoformat()]
    return dict(
        now=now, own=own, forks=forks, by=by, cal=cal,
        n_own=len(own), n_forks=len(forks),
        stars=sum(r["stars"] for r in own),
        n_langs=len(langs),
        langs=[(k, v / total, used_in[k]) for k, v in ranked],
        last=last,
        contrib=sum(c[1] for c in cal) if cal else None,
        active_days=sum(1 for c in cal if c[1] > 0) if cal else None,
        peak=max(cal, key=lambda c: c[1]) if cal else None,
        week=f"{now.isocalendar()[0]}-W{now.isocalendar()[1]:02d}",
        build=now.strftime("%y.%m"),
    )


def age_days(iso: str, now: dt.datetime) -> float:
    t = dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return (now - t).total_seconds() / 86400


# ───────────────────────────────────────────────────────────── svg helpers ──
def esc(s) -> str:
    return html.escape(str(s), quote=True)


def text(x, y, s, size=14, fill=INK, font=MONO, weight=400, anchor="start", ls=0, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'letter-spacing="{ls}" xml:space="preserve" {extra}>{esc(s)}</text>')


def wrap(s: str, max_chars: int) -> list[str]:
    out, line = [], ""
    for w in s.split():
        if len(line) + len(w) + 1 > max_chars and line:
            out.append(line)
            line = w
        else:
            line = f"{line} {w}".strip()
    return out + [line] if line else out


def mono_w(s: str, size: float) -> float:
    return len(s) * size * 0.602


STYLE = f"""<style>
  @keyframes blink {{ 0%,49% {{ opacity:1 }} 50%,100% {{ opacity:0 }} }}
  @keyframes pulse {{ 0% {{ transform:scale(1); opacity:.6 }} 100% {{ transform:scale(2.8); opacity:0 }} }}
  .cursor {{ animation: blink 1.1s steps(1) infinite }}
  .pulse  {{ transform-box:fill-box; transform-origin:center; animation: pulse 2.6s ease-out infinite }}
  @media (prefers-reduced-motion: reduce) {{ .cursor, .pulse {{ animation: none }} }}
</style>"""


def svg(h: int, body: str, title: str, desc: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" '
            f'role="img" aria-labelledby="t d">\n<title id="t">{esc(title)}</title>\n'
            f'<desc id="d">{esc(desc)}</desc>\n{STYLE}\n'
            f'<defs><filter id="glow" filterUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{h}">'
            f'<feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/>'
            f'<feMergeNode in="SourceGraphic"/></feMerge></filter>'
            f'<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
            f'<circle cx="1" cy="1" r="1" fill="{GRID}"/></pattern></defs>\n'
            f'{body}\n</svg>\n')


def frame(h: int, left: str, right: str = "", dots=False) -> str:
    """Panel with hairline border, corner registration marks and a header rule."""
    p = [f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="14" fill="{BG}" stroke="{EDGE}"/>']
    if dots:
        p.append(f'<rect x="1" y="1" width="{W-2}" height="{h-2}" rx="14" fill="url(#dots)"/>')
    for cx, cy, sx, sy in [(16, 16, 1, 1), (W-16, 16, -1, 1), (16, h-16, 1, -1), (W-16, h-16, -1, -1)]:
        p.append(f'<path d="M{cx} {cy+10*sy} V{cy} H{cx+10*sx}" fill="none" stroke="{DIM}" stroke-width="1"/>')
    p.append(text(48, 44, left, 13, INK2, ls=1.6))
    if right:
        p.append(text(W-48, 44, right, 13, DIM, anchor="end", ls=1.6))
    p.append(f'<line x1="48" y1="58" x2="{W-48}" y2="58" stroke="{EDGE}"/>')
    p.append(f'<rect x="48" y="57" width="36" height="2" fill="{RED}"/>')
    return "\n".join(p)


def pill(x, y, label, color=RED, anchor="end"):
    w = mono_w(label, 11) + len(label) * 1.2 + 20
    x0 = x - w if anchor == "end" else x
    return (f'<rect x="{x0:.1f}" y="{y-14}" width="{w:.1f}" height="21" rx="3" fill="none" stroke="{color}"/>'
            + text(x0 + w / 2, y, label, 11, color, anchor="middle", ls=1.2))


# ─────────────────────────────────────────────────────────────────── hero ──
def hero(D) -> str:
    h = 460
    b = [frame(h, f"ZZ // CONTROL PLANE", f"PROFILE::PUBLIC  ·  BUILD {D['build']}  ·  32.24N 07.95W", dots=True)]
    # fade the dot grid out under the type
    b.append(f'<defs><linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{BG}" stop-opacity="1"/>'
             f'<stop offset=".55" stop-color="{BG}" stop-opacity=".85"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/>'
             f'</linearGradient></defs><rect x="30" y="60" width="760" height="{h-90}" fill="url(#fade)"/>')
    b.append(text(64, 212, "ZAYD ZAARI", 96, INK, SANS, 700, ls=-3))
    b.append(f'<rect x="66" y="242" width="6" height="26" fill="{RED}"/>')
    b.append(text(86, 264, "Small systems with hard edges.", 28, INK, SANS, 400, ls=-0.4))
    b.append(text(66, 304, "agent tooling · control planes · local inference · applied research", 15, INK2, ls=0.2))
    # terminal
    ty = 360
    b.append(text(66, ty, "$ whoami", 14, DIM))
    b.append(text(66, ty + 22, "student developer · morocco · builds in bursts, ships each one", 14, INK))
    b.append(text(66, ty + 52, "$ cat ./boundaries", 14, DIM))
    b.append(text(66, ty + 74, "outbound-only · allow-listed · one worker · sealed test set", 14, INK))
    cx = 66 + mono_w("outbound-only · allow-listed · one worker · sealed test set", 14) + 6
    b.append(f'<rect class="cursor" x="{cx:.1f}" y="{ty+62}" width="8" height="15" fill="{RED}"/>')

    # topology: a trust boundary with one way in and one way out
    x0, y0, x1, y1 = 820, 110, 1160, 380
    b.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="{PANEL}" fill-opacity=".7" '
             f'stroke="{INK2}" stroke-opacity=".5" stroke-dasharray="3 5"/>')
    b.append(text(x0, y0 - 10, "TRUST BOUNDARY", 12, DIM, ls=1.8))
    b.append(text(x1, y1 + 22, "6 SYSTEMS · 0 OPEN SHELLS", 12, DIM, anchor="end", ls=1.4))
    nodes = {"LS": (895, 190), "RC": (1010, 160), "HP": (1095, 245),
             "SM": (900, 315), "FL": (1015, 330), "TR": (990, 250)}
    edges = [("LS", "RC"), ("RC", "HP"), ("HP", "TR"), ("TR", "SM"), ("LS", "FL"), ("SM", "LS"), ("TR", "FL")]
    for a, c in edges:
        (ax, ay), (bx, by) = nodes[a], nodes[c]
        b.append(f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="{FAINT}"/>')
    # gates: bearer in (left, to LinkScribe), WSS out (right, from HomePC)
    gi, go = (x0, 190), (x1, 245)
    b.append(f'<line x1="750" y1="190" x2="{nodes["LS"][0]}" y2="190" stroke="{INK2}" stroke-dasharray="2 4"/>')
    b.append(f'<line x1="{nodes["HP"][0]}" y1="245" x2="1230" y2="245" stroke="{RED}" stroke-width="1.5" filter="url(#glow)"/>')
    b.append(f'<path d="M1222 240 L1230 245 L1222 250" fill="none" stroke="{RED}" stroke-width="1.5"/>')
    for gx, gy, lab, col in [(gi[0], gi[1], "bearer · in", INK2), (go[0], go[1], "wss · out", RED)]:
        b.append(f'<rect x="{gx-5}" y="{gy-5}" width="10" height="10" fill="{BG}" stroke="{col}"/>')
        b.append(text(gx, gy - 14, lab, 12, col, anchor="middle", ls=0.6))
    b.append(text(752, 214, "AGENT", 12, DIM, ls=1.4))
    b.append(text(1232, 270, "WAN", 12, DIM, anchor="end", ls=1.4))
    # freshest system pulses
    fresh = IDS.get(D["last"]["name"]) if D["last"] else None
    for k, (x, y) in nodes.items():
        hot = k == fresh
        if hot:
            b.append(f'<circle class="pulse" cx="{x}" cy="{y}" r="7" fill="none" stroke="{RED_G}"/>')
        b.append(f'<rect x="{x-6}" y="{y-6}" width="12" height="12" fill="{RED if hot else BG}" '
                 f'stroke="{RED if hot else INK}" {GLOW if hot else ""}/>')
        dx, dy = {"HP": (-8, 26)}.get(k, (14, 5))
        b.append(text(x + dx, y + dy, k, 14, INK if hot else INK2, ls=1))
    return svg(h, "\n".join(b), "Zayd Zaari — small systems with hard edges",
               "Hero banner. Zayd Zaari, student developer in Morocco: agent tooling, control planes, "
               "local inference and applied research. A diagram shows six projects inside a trust "
               "boundary with one authenticated way in and one outbound-only way out.")


# ───────────────────────────────────────────────────────────── plane card ──
def flow_row(x, y, steps, max_w):
    out, widths = [], [mono_w(s, 14) + 24 for s, _ in steps]
    gap = max(26, (max_w - sum(widths)) / max(1, len(steps) - 1))
    cx = x
    for i, ((label, arrow), w) in enumerate(zip(steps, widths)):
        last = i == len(steps) - 1
        col = RED if last else EDGE
        out.append(f'<rect x="{cx:.1f}" y="{y-17}" width="{w:.1f}" height="30" rx="2" fill="{PANEL}" stroke="{col}"/>')
        out.append(text(cx + w / 2, y + 3, label, 14, INK if last else INK2, anchor="middle"))
        if arrow:
            a, bx = cx + w + 4, cx + w + gap - 4
            out.append(f'<line x1="{a:.1f}" y1="{y-2}" x2="{bx:.1f}" y2="{y-2}" stroke="{DIM}"/>')
            tip, d = (bx, -1) if arrow == ">" else (a, 1)
            out.append(f'<path d="M{tip+6*d:.1f} {y-6} L{tip:.1f} {y-2} L{tip+6*d:.1f} {y+2}" fill="none" stroke="{DIM}"/>')
        cx += w + gap
    return "\n".join(out)


def plane(p, D) -> str:
    h = 336
    r = D["by"].get(p["repo"], {})
    pushed = r.get("pushed", "")[:10]
    b = [frame(h, f'{IDS[p["repo"]]}  ·  {p["kicker"]}', f"LAST PUSH {pushed}" if pushed else "")]
    b.append(text(48, 118, p["title"], 44, INK, SANS, 700, ls=-1.2))
    b.append(pill(808, 108, p["status"]))
    for i, ln in enumerate(wrap(p["line"], 78)):
        b.append(text(48, 158 + i * 27, ln, 19, INK2, SANS))
    b.append(flow_row(48, 238, p["flow"], 764))
    b.append(text(48, 278, f'↳ {p["note"]}', 13, DIM))
    # boundary column
    bx = 862
    b.append(f'<line x1="{bx-32}" y1="82" x2="{bx-32}" y2="{h-64}" stroke="{EDGE}"/>')
    b.append(text(bx, 100, "BOUNDARY", 12, RED, ls=2.4))
    for i, ln in enumerate(p["boundary"]):
        y = 136 + i * 38
        b.append(text(bx, y, "×", 16, RED))
        b.append(text(bx + 20, y, ln, 14, INK))
    b.append(f'<line x1="48" y1="{h-46}" x2="{W-48}" y2="{h-46}" stroke="{GRID}"/>')
    b.append(text(48, h - 21, p["stack"], 14, DIM, ls=0.2))
    b.append(text(W - 48, h - 22, f'github.com/{LOGIN}/{p["repo"]}  →', 14, INK2, anchor="end"))
    return svg(h, "\n".join(b), f'{p["title"]} — {p["kicker"].title()}',
               f'{p["title"]} ({p["status"]}). {p["line"]} Pipeline: '
               + " → ".join(s for s, _ in p["flow"]) + ". Boundaries: " + "; ".join(p["boundary"])
               + f'. Stack: {p["stack"]}.')


# ────────────────────────────────────────────────────────────── field study ──
def study(s, D) -> str:
    h = 384
    b = [frame(h, f'FL  ·  {s["kicker"]}', s["status"])]
    b.append(text(48, 112, s["title"], 34, INK, SANS, 700, ls=-0.8))
    for i, ln in enumerate(wrap(s["line"], 68)):
        b.append(text(48, 150 + i * 26, ln, 18, INK2, SANS))
    for i, (n, lab) in enumerate(s["figures"]):
        x = 48 + i * 182
        b.append(text(x, 264, n, 34, INK, SANS, 300, ls=-1))
        b.append(text(x, 288, lab, 12, DIM, ls=0.4))
    # result: interval of the interaction slope against zero
    est, lo, hi = s["ci"]
    gx0, gx1, gy = 840, 1222, 206
    lo_v, hi_v = -0.04, 0.08
    X = lambda v: gx0 + (v - lo_v) / (hi_v - lo_v) * (gx1 - gx0)
    b.append(f'<line x1="{gx0-32}" y1="82" x2="{gx0-32}" y2="{h-64}" stroke="{EDGE}"/>')
    b.append(text(gx0, 98, "RESULT", 11, RED, ls=2))
    b.append(text(gx0, 124, "F1 interaction slope per doubling of regions", 13, INK2))
    b.append(f'<line x1="{gx0}" y1="{gy}" x2="{gx1}" y2="{gy}" stroke="{EDGE}"/>')
    for v in (-0.04, -0.02, 0, 0.02, 0.04, 0.06, 0.08):
        b.append(f'<line x1="{X(v):.1f}" y1="{gy-4}" x2="{X(v):.1f}" y2="{gy+4}" stroke="{DIM}"/>')
        b.append(text(X(v), gy + 22, f"{v:+.2f}".replace("+0.00", "0"), 10, DIM, anchor="middle"))
    b.append(f'<line x1="{X(0):.1f}" y1="{gy-46}" x2="{X(0):.1f}" y2="{gy+6}" stroke="{INK}" stroke-dasharray="2 3"/>')
    b.append(text(X(0), gy - 52, "no effect", 10, INK, anchor="middle"))
    b.append(f'<line x1="{X(lo):.1f}" y1="{gy-16}" x2="{X(hi):.1f}" y2="{gy-16}" stroke="{RED}" stroke-width="3"/>')
    for v in (lo, hi):
        b.append(f'<line x1="{X(v):.1f}" y1="{gy-23}" x2="{X(v):.1f}" y2="{gy-9}" stroke="{RED}" stroke-width="2"/>')
    b.append(f'<circle cx="{X(est):.1f}" cy="{gy-16}" r="5" fill="{BG}" stroke="{RED}" stroke-width="2"/>')
    b.append(text(gx0, gy + 56, "95% bootstrap interval crosses zero", 13, INK2))
    for i, ln in enumerate(wrap(s["verdict"], 42)):
        b.append(text(gx0, gy + 82 + i * 22, ln, 16, INK, SANS, 600))
    b.append(f'<line x1="48" y1="{h-46}" x2="{W-48}" y2="{h-46}" stroke="{GRID}"/>')
    b.append(text(48, h - 21, f'{s["stack"]}   ·   × {s["boundary"]}', 14, DIM, ls=0.2))
    b.append(text(W - 48, h - 21, "repo →", 14, INK2, anchor="end"))
    return svg(h, "\n".join(b), "Field study — geographic diversity and spectral modality",
               f'{s["line"]} ' + ", ".join(f"{n} {l}" for n, l in s["figures"])
               + f'. Result: F1 interaction slope +0.018 per doubling, 95% interval −0.017 to +0.058. '
               f'{s["verdict"]} Status: manuscript in preparation.')


# ──────────────────────────────────────────────────────────────── bench ──
def bench(p, D) -> str:
    h = 232
    r = D["by"].get(p["repo"], {})
    pushed = r.get("pushed", "")[:10]
    b = [frame(h, f'{IDS[p["repo"]]}  ·  {p["kicker"]}', f"LAST PUSH {pushed}" if pushed else "")]
    b.append(text(48, 116, p["title"], 32, INK, SANS, 700, ls=-0.6))
    b.append(pill(48, 152, p["status"], color=RED if p["status"] != "LAB" else INK2, anchor="start"))
    for i, ln in enumerate(wrap(p["line"], 62)):
        b.append(text(540, 100 + i * 26, ln, 18, INK2, SANS))
    b.append(f'<line x1="48" y1="{h-46}" x2="{W-48}" y2="{h-46}" stroke="{GRID}"/>')
    b.append(text(48, h - 21, p["stack"], 14, DIM, ls=0.2))
    b.append(text(W - 48, h - 22, f'github.com/{LOGIN}/{p["repo"]}  →', 14, INK2, anchor="end"))
    return svg(h, "\n".join(b), f'{p["title"]} — {p["kicker"].title()}',
               f'{p["title"]} ({p["status"]}). {p["line"]} Stack: {p["stack"]}.')


# ──────────────────────────────────────────────────────────── constellation ──
def constellation(D) -> str:
    h, cx, cy = 640, 640, 330
    now = D["now"]
    own = [r for r in D["own"] if r["name"] in THEMES]
    amax = max((age_days(r["created"], now) for r in own), default=1)
    R = lambda a: 92 + 190 * math.sqrt(max(a, 0) / amax)
    b = [frame(h, "TOPOLOGY  ·  ANGLE = THEME  ·  DISTANCE = AGE  ·  GLOW = RECENT PUSH",
               f"SAMPLED {D['week']}")]
    # age rings, labelled along one quiet diagonal
    for months in (1, 3, 6, 12):
        days = months * 30.44
        if days > amax * 1.02:
            continue
        rr = R(days)
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{rr:.1f}" fill="none" stroke="{FAINT}" stroke-opacity=".55" '
                 f'stroke-dasharray="1 5"/>')
        t = math.radians(72)
        b.append(text(cx + rr * math.cos(t) + 6, cy + rr * math.sin(t), f"{months} mo", 10, FAINT))
    b.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{INK2}"/>')
    b.append(text(cx, cy + 18, "now", 10, DIM, anchor="middle", ls=1))
    pos = {}
    for r in own:
        _, ang = THEMES[r["name"]]
        rad, t = R(age_days(r["created"], now)), math.radians(ang)
        pos[r["name"]] = (cx + rad * math.cos(t), cy + rad * math.sin(t))
    for a_, c_, lab, *tt in LINKS:
        if a_ not in pos or c_ not in pos:
            continue
        (ax, ay), (bx, by) = pos[a_], pos[c_]
        b.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{FAINT}"/>')
        t_ = tt[0] if tt else 0.5
        mx, my, w = ax + (bx - ax) * t_, ay + (by - ay) * t_, mono_w(lab, 12) + 12
        b.append(f'<rect x="{mx - w/2:.1f}" y="{my-10:.1f}" width="{w:.1f}" height="18" rx="2" '
                 f'fill="{BG}" stroke="{GRID}"/>')
        b.append(text(mx, my + 3, lab, 12, INK2, anchor="middle"))
    biggest = max((sum(r["languages"].values()) for r in own), default=1)
    for r in own:
        x, y = pos[r["name"]]
        rad = 5 + 11 * math.sqrt(sum(r["languages"].values()) / biggest)
        since = age_days(r["pushed"], now)
        hot, warm = since <= 30, since <= 120
        if hot:
            b.append(f'<circle class="pulse" cx="{x:.1f}" cy="{y:.1f}" r="{rad:.1f}" fill="none" stroke="{RED_G}"/>')
        fill = RED if hot else (RED_D if warm else PANEL)
        stroke = RED if (hot or warm) else DIM
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.1f}" fill="{fill}" stroke="{stroke}" '
                 f'stroke-width="1.5" {GLOW if hot else ""}/>')
        right = x >= cx - 1
        lx, anc = x + (rad + 12) * (1 if right else -1), ("start" if right else "end")
        name = r["name"] if len(r["name"]) < 22 else "forest-loss study"
        b.append(text(lx, y - 21, THEMES[r["name"]][0], 11, RED, anchor=anc, ls=2))
        b.append(text(lx, y - 1, name, 17, INK, anchor=anc))
        b.append(text(lx, y + 17, f'{IDS[r["name"]]} · {r["language"] or "n/a"} · since {r["created"][:7]}',
                      12, DIM, anchor=anc))
    # footer: legend + honesty note about forks
    b.append(f'<line x1="48" y1="{h-50}" x2="{W-48}" y2="{h-50}" stroke="{GRID}"/>')
    note = "node size = code volume"
    if D["forks"]:
        note += f"   ·   {D['n_forks']} forks not plotted: " + ", ".join(f["name"] for f in D["forks"])
    b.append(text(48, h - 24, note, 10, DIM))
    x = W - 48
    for f, st, lab in reversed([(RED, RED, "pushed ≤ 30 d"), (RED_D, RED, "≤ 120 d"), (PANEL, DIM, "older")]):
        x -= mono_w(lab, 10)
        b.append(text(x, h - 24, lab, 10, DIM))
        b.append(f'<circle cx="{x-11:.1f}" cy="{h-28}" r="5" fill="{f}" stroke="{st}"/>')
        x -= 34
    return svg(h, "\n".join(b), "Project constellation",
               "Network of Zayd's original repositories. Angle groups them by theme (agent "
               "infrastructure, control planes, research, lab, product); distance from the centre is age; "
               "bright nodes were pushed recently. Links name what two projects share: "
               + "; ".join(f"{a} and {c}: {l[0]}" for a, c, *l in LINKS) + ".")


# ─────────────────────────────────────────────────────────────── toolchain ──
def toolchain(D) -> str:
    row_h = 46
    h = 112 + row_h * len(TOOLCHAIN) + 30
    b = [frame(h, "TOOLCHAIN  ·  GROUPED BY WHAT IT'S FOR", "EVIDENCE = REPO IDS")]
    for i, (verb, items, ev) in enumerate(TOOLCHAIN):
        y = 106 + i * row_h
        b.append(text(48, y, verb, 13, RED, ls=2.4))
        b.append(text(150, y, items, 19, INK, SANS))
        b.append(text(W - 48, y, ev, 13, DIM, anchor="end", ls=1))
        if i < len(TOOLCHAIN) - 1:
            b.append(f'<line x1="150" y1="{y+20}" x2="{W-48}" y2="{y+20}" stroke="{GRID}"/>')
    key = "  ".join(f"{v} {k if len(k) < 20 else 'forest-loss'}" for k, v in IDS.items())
    b.append(text(48, h - 24, key, 12, DIM))
    return svg(h, "\n".join(b), "Toolchain",
               "Tools grouped by use, each backed by repositories: "
               + " ".join(f"{v}: {i}." for v, i, _ in TOOLCHAIN))


# ─────────────────────────────────────────────────────────────── telemetry ──
def telemetry(D) -> str:
    h = 360
    b = [frame(h, "TELEMETRY  ·  PUBLIC GITHUB API", f"SAMPLED {D['week']}")]
    cells = [("ORIGINAL REPOS", D["n_own"]), ("FORKS", D["n_forks"]), ("STARS", D["stars"]),
             ("LANGUAGES", D["n_langs"])]
    if D["contrib"] is not None:
        cells += [("CONTRIBUTIONS · 1Y", D["contrib"]), ("ACTIVE DAYS · 1Y", D["active_days"])]
    for i, (lab, v) in enumerate(cells):
        x, y = 48 + (i % 2) * 210, 112 + (i // 2) * 72
        b.append(text(x, y, lab, 12, DIM, ls=1.4))
        b.append(text(x, y + 38, f"{v:02d}" if v < 100 else str(v), 36, INK, MONO, 300))
    b.append(f'<line x1="492" y1="82" x2="492" y2="{h-64}" stroke="{EDGE}"/>')
    b.append(text(524, 98, "SIGNAL STRENGTH  ·  SHARE OF CODE BYTES, ORIGINAL REPOS", 10, DIM, ls=1.4))
    cells_n, cw = 30, 12
    for i, (lang, share, n) in enumerate(D["langs"][:5]):
        y = 138 + i * 36
        b.append(text(524, y + 5, lang, 16, INK if i == 0 else INK2))
        on = max(1, round(share * cells_n))
        for k in range(cells_n):
            col = RED if (k < on and i == 0) else (INK2 if k < on else GRID)
            op = "" if k < on else ""
            b.append(f'<rect x="{660 + k*cw}" y="{y-8}" width="{cw-3}" height="12" fill="{col}" {op}/>')
        b.append(text(W - 48, y + 5, f"{share*100:4.1f}%  ·  {n} repo{'s' if n != 1 else ''}",
                      14, INK2 if i == 0 else DIM, anchor="end"))
    last = D["last"]
    b.append(f'<line x1="48" y1="{h-46}" x2="{W-48}" y2="{h-46}" stroke="{GRID}"/>')
    if last:
        b.append(text(48, h - 22, f'LAST SIGNAL  {last["pushed"][:10]}  /  {last["name"]}', 12, INK2, ls=0.6))
    b.append(text(W - 48, h - 22, "regenerated weekly by .github/workflows/update-profile.yml", 11, FAINT, anchor="end"))
    langs = ", ".join(f"{l} {s*100:.1f}%" for l, s, _ in D["langs"][:5])
    return svg(h, "\n".join(b), "GitHub telemetry",
               f'{D["n_own"]} original public repositories, {D["n_forks"]} forks, {D["stars"]} stars, '
               f'{D["n_langs"]} languages. '
               + (f'{D["contrib"]} contributions over {D["active_days"]} active days in the last year. '
                  if D["contrib"] is not None else "")
               + f"Code share: {langs}.")


# ──────────────────────────────────────────────────────────────── signal ──
def signal(D) -> str | None:
    cal = D["cal"]
    if not cal:
        return None
    h = 320
    x0, x1, base, top = 64, W - 64, 246, 130
    n = len(cal)
    X = lambda i: x0 + i * (x1 - x0) / max(1, n - 1)
    peak = max(c[1] for c in cal) or 1
    Y = lambda v: base - (math.sqrt(v / peak)) * (base - top)
    pk = D["peak"]
    b = [frame(h, "SIGNAL  ·  DAILY CONTRIBUTIONS, LAST 12 MONTHS",
               f"{D['contrib']} TOTAL · {D['active_days']} ACTIVE DAYS · PEAK {pk[1]} ON {pk[0]}")]
    # month ticks
    for i, (d, _) in enumerate(cal):
        if d.endswith("-01"):
            b.append(f'<line x1="{X(i):.1f}" y1="{base+6}" x2="{X(i):.1f}" y2="{base+12}" stroke="{DIM}"/>')
            b.append(text(X(i) + 3, base + 26, dt.date.fromisoformat(d).strftime("%b").upper(), 10, DIM, ls=1))
    b.append(f'<line x1="{x0}" y1="{base}" x2="{x1}" y2="{base}" stroke="{EDGE}"/>')
    # envelope: a soft trace through the daily values
    pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, (_, v) in enumerate(cal))
    b.append(f'<polyline points="{pts}" fill="none" stroke="{RED_D}" stroke-width="1"/>')
    for i, (_, v) in enumerate(cal):
        if v:
            b.append(f'<line x1="{X(i):.1f}" y1="{base}" x2="{X(i):.1f}" y2="{Y(v):.1f}" stroke="{RED}" '
                     f'stroke-width="2.4" filter="url(#glow)"/>')
    # launches: original repos created inside the window, staggered to avoid collisions
    idx = {d: i for i, (d, _) in enumerate(cal)}
    marks = sorted((idx[r["created"][:10]], r["name"]) for r in D["own"] if r["created"][:10] in idx)
    levels: list[float] = []
    for i, name in marks:
        x = X(i)
        label = IDS.get(name, name) + " " + (name if len(name) < 16 else "forest-loss")
        w = mono_w(label, 13)
        lvl = 0
        while lvl < len(levels) and levels[lvl] > x - 22:
            lvl += 1
        if lvl == len(levels):
            levels.append(0)
        levels[lvl] = x + w
        ly = 92 + lvl * 18
        b.append(f'<line x1="{x:.1f}" y1="{ly+4}" x2="{x:.1f}" y2="{base}" stroke="{DIM}" stroke-dasharray="1 3"/>')
        b.append(f'<path d="M{x:.1f} {base-4} L{x+4:.1f} {base} L{x:.1f} {base+4} L{x-4:.1f} {base} Z" fill="{INK}"/>')
        b.append(text(x + 4, ly, label, 13, INK2))
    b.append(f'<line x1="48" y1="{h-46}" x2="{W-48}" y2="{h-46}" stroke="{GRID}"/>')
    b.append(text(48, h - 21, "◆ repository created     │ contributions that day", 13, DIM))
    b.append(text(W - 48, h - 21, "work arrives in bursts; most bursts end in a new repo", 13, INK2, anchor="end"))
    return svg(h, "\n".join(b), "Contribution signal",
               f'Daily contributions over the last year: {D["contrib"]} in total across {D["active_days"]} '
               f'active days, peaking at {pk[1]} on {pk[0]}. Diamonds mark when each original repository '
               f'was created: ' + ", ".join(f"{n} ({cal[i][0]})" for i, n in marks) + ".")


# ──────────────────────────────────────────────────────────────── footer ──
def footer(D) -> str:
    h = 128
    b = [f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="14" fill="{BG}" stroke="{EDGE}"/>']
    b.append(text(48, 50, "$ exit", 16, DIM))
    b.append(text(48, 80, f"session closed · inbound ports opened: 0 · build {D['build']} · {D['week']}", 16, INK))
    cx = 48 + mono_w(f"session closed · inbound ports opened: 0 · build {D['build']} · {D['week']}", 16) + 8
    b.append(f'<rect class="cursor" x="{cx:.1f}" y="67" width="9" height="17" fill="{RED}"/>')
    b.append(text(W - 48, 80, "ZZ // CONTROL PLANE", 13, DIM, anchor="end", ls=2))
    b.append(f'<rect x="{W-48-36}" y="92" width="36" height="2" fill="{RED}"/>')
    return svg(h, "\n".join(b), "End of session", "Footer: session closed, zero inbound ports opened.")


# ────────────────────────────────────────────────────────────────── main ──
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", help="render from a saved dataset instead of the API")
    ap.add_argument("--out", default=str(ASSETS))
    a = ap.parse_args()
    try:
        data = json.loads(Path(a.snapshot).read_text()) if a.snapshot else fetch_live()
    except (urllib.error.URLError, KeyError, ValueError) as e:
        print(f"could not load data, leaving existing assets untouched: {e}", file=sys.stderr)
        return 1
    D = derive(data)
    out = Path(a.out)
    (out / "planes").mkdir(parents=True, exist_ok=True)
    files = {
        "hero.svg": hero(D),
        "constellation.svg": constellation(D),
        "toolchain.svg": toolchain(D),
        "telemetry.svg": telemetry(D),
        "signal.svg": signal(D),
        "footer.svg": footer(D),
        f"planes/{STUDY['file']}": study(STUDY, D),
        **{f"planes/{p['file']}": plane(p, D) for p in PLANES},
        **{f"planes/{p['file']}": bench(p, D) for p in BENCH},
    }
    for name, body in files.items():
        if body is None:
            print(f"  skip {name} (no data; previous version kept)")
            continue
        path = out / name
        if path.exists() and path.read_text() == body:
            print(f"  same {name}")
            continue
        path.write_text(body)
        print(f"  wrote {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
