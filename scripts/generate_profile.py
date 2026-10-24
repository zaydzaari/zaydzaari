#!/usr/bin/env python3
"""Generate static, theme-aware profile banners. No network or credentials needed.

Project descriptions live in README.md as accessible GitHub Markdown.
Run: python scripts/generate_profile.py
"""
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
THEMES = {
    "dark": ("#0d1117", "#f0f6fc", "#58d5cf", "#172f37", "#30363d"),
    "light": ("#f6f8fa", "#17212b", "#087f8c", "#dfedf0", "#d0d7de"),
}


def banner(theme: str) -> str:
    background, ink, accent, soft, edge = THEMES[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="216" viewBox="0 0 1040 216" role="img" aria-labelledby="title">
  <title id="title">Zayd Zaari</title>
  <rect x="0.5" y="0.5" width="1039" height="215" rx="16" fill="{background}" stroke="{edge}"/>
  <rect x="40" y="57" width="5" height="102" rx="2.5" fill="{accent}"/>
  <text x="68" y="134" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif" font-size="80" font-weight="700" letter-spacing="-3" fill="{ink}">Zayd Zaari</text>
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <rect x="812" y="48" width="136" height="120" rx="24" fill="{soft}"/>
    <path d="M852 84 L828 108 L852 132 M908 84 L932 108 L908 132 M890 78 L870 138" stroke="{accent}" stroke-width="6"/>
    <path d="M772 108 H788 M972 108 H988" stroke="{accent}" stroke-width="3"/>
  </g>
</svg>
'''


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        path = ASSETS / f"header-{theme}.svg"
        path.write_text(banner(theme), encoding="utf-8")
        print(f"Generated {path.name}")


if __name__ == "__main__":
    main()
