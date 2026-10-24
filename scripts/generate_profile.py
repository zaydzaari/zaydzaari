#!/usr/bin/env python3
"""Generate theme-aware SVGs with gentle, reduced-motion-aware animation.

The README and scientific figure stay independent of these illustrations.
No credentials, network requests, or third-party renderers are required.
"""
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
PALETTES = {
    "dark": ("#161b22", "#f0f6fc", "#b1bac4", "#30363d", "#82aaff"),
    "light": ("#f6f8fa", "#1f2328", "#59636e", "#d1d9e0", "#245cb1"),
}


def accent(theme: str) -> str:
    _, _, _, edge, color = PALETTES[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="18" viewBox="0 0 960 18" aria-hidden="true">
<style>
.highlight{{stroke-dasharray:64 1100;animation:drift 12s linear infinite;opacity:.7}}
@keyframes drift{{from{{stroke-dashoffset:70}}to{{stroke-dashoffset:-1094}}}}
@media(prefers-reduced-motion:reduce){{.highlight{{animation:none;opacity:0}}}}
</style>
<path d="M1 9H959" stroke="{edge}" stroke-width="1"/>
<path class="highlight" d="M1 9H959" stroke="{color}" stroke-width="2" stroke-linecap="round" fill="none"/>
</svg>
'''


def pipeline(theme: str, mobile: bool = False) -> str:
    bg, ink, muted, edge, color = PALETTES[theme]
    w, h = (380, 352) if mobile else (960, 168)
    axis = "Y" if mobile else "X"
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">LinkScribe pipeline</title>
<desc id="desc">A media URL enters a FastAPI queue, audio is processed locally, and English text is returned to an AI agent. Moving dots illustrate the flow, not live job status.</desc>
<style>
.packet{{opacity:0;animation:signal 8s ease-in-out infinite}}
.second{{animation-delay:3s}}
@keyframes signal{{0%,14%{{opacity:0;transform:translate{axis}(0)}}22%{{opacity:.85}}40%{{opacity:0;transform:translate{axis}(18px)}}100%{{opacity:0;transform:translate{axis}(18px)}}}}
@media(prefers-reduced-motion:reduce){{.packet{{animation:none;opacity:0}}}}
</style>''']
    labels = [
        ("Media URL", "FastAPI queue"),
        ("Local inference", "FFmpeg + whisper.cpp"),
        ("English text", "For the calling agent"),
    ]
    for i, (title, subtitle) in enumerate(labels):
        x, y, bw, bh = (8, 4 + i * 116, 364, 94) if mobile else (8 + i * 320, 8, 294, 144)
        parts.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="10" fill="{bg}" stroke="{edge}"/>')
        parts.append(f'<rect x="{x}" y="{y+16}" width="3" height="{bh-32}" rx="1.5" fill="{color}"/>')
        parts.append(f'<text x="{x+22}" y="{y+(38 if mobile else 60)}" font-family="Arial,sans-serif" font-size="{25 if mobile else 28}" font-weight="700" fill="{ink}">{title}</text>')
        parts.append(f'<text x="{x+22}" y="{y+(69 if mobile else 99)}" font-family="Arial,sans-serif" font-size="{20 if mobile else 22}" fill="{muted}">{subtitle}</text>')
        if i < 2:
            if mobile:
                line = f'M190 {y+bh+2}v18m-4-4 4 4 4-4'
                cx, cy = 190, y + bh + 2
            else:
                line = f'M{x+bw+2} 80h20m-5-5 5 5-5 5'
                cx, cy = x + bw + 2, 80
            parts.append(f'<path d="{line}" fill="none" stroke="{edge}" stroke-width="2"/>')
            parts.append(f'<circle class="packet {"second" if i else ""}" cx="{cx}" cy="{cy}" r="3" fill="{color}"/>')
    return "\n".join(parts) + "\n</svg>\n"


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for theme in PALETTES:
        (ASSETS / f"academic-accent-{theme}.svg").write_text(accent(theme), encoding="utf-8")
        for mobile in (False, True):
            suffix = "-mobile" if mobile else ""
            path = ASSETS / f"linkscribe-pipeline{suffix}-{theme}.svg"
            path.write_text(pipeline(theme, mobile), encoding="utf-8")
    print("Generated 6 SVGs with theme and reduced-motion support")


if __name__ == "__main__":
    main()
