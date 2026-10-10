<!--
  ZZ // CONTROL PLANE
  Every image below is rendered by scripts/generate_profile.py.
  Numbers come from the public GitHub API, refreshed weekly by .github/workflows/update-profile.yml.
  Edit the script, not the SVGs.
-->

<img src="assets/hero.svg" width="100%" alt="Zayd Zaari. Small systems with hard edges. Agent tooling, control planes, local inference, applied research. A diagram shows six projects inside a trust boundary with one authenticated way in and one outbound-only way out.">

<sub><code>00 / HANDSHAKE</code></sub>

Student developer in Morocco. Most of what I build sits between something powerful and something that shouldn't get full access to it: an AI agent and a video, Google Home and a Windows PC, a web dashboard and a Linux server.

I keep those systems narrow on purpose. A fixed list of actions, one worker, one SSH boundary. I try to keep my claims the same size: the headline result of my forest-loss study is that it found no clear effect.

<br>

<sub><code>01 / PLANES</code>&nbsp; three control planes, each with the things it refuses to do</sub>

<a href="https://github.com/zaydzaari/linkscribe"><img src="assets/planes/plane-linkscribe.svg" width="100%" alt="LinkScribe, released v0.1.2. Hands coding agents an English transcript of a public YouTube, TikTok or Instagram link; transcription runs locally on a 2-core ARM VPS. Pipeline: agent, FastAPI queue, yt-dlp, FFmpeg, whisper.cpp. Boundaries: one worker, no LLM on the VPS, media deleted after every job."></a>
<sub>&nbsp;&nbsp;<a href="https://github.com/zaydzaari/linkscribe">repo</a> · <a href="https://51-170-131-7.sslip.io/">live service</a> · <a href="https://github.com/zaydzaari/linkscribe/releases/tag/v0.1.2">release v0.1.2</a></sub>

<a href="https://github.com/zaydzaari/HomePC"><img src="assets/planes/plane-homepc.svg" width="100%" alt="HomePC, v2 private test. Turns a Windows PC into Google Home switches without opening an inbound port. Google Home talks to a Cloudflare Worker and Durable Object; a .NET agent on the PC dials out over WSS to a fixed action registry. Boundaries: no inbound port or remote shell, a fixed allow-list of actions, power actions off by default."></a>
<sub>&nbsp;&nbsp;<a href="https://github.com/zaydzaari/HomePC">repo</a> · <a href="https://github.com/zaydzaari/HomePC/releases">releases</a></sub>

<a href="https://github.com/zaydzaari/RemoteCraft"><img src="assets/planes/plane-remotecraft.svg" width="100%" alt="RemoteCraft, alpha. Runs Vanilla Minecraft servers on a Linux VPS from a web dashboard without handing anyone a terminal. Dashboard, FastAPI, validated operations, SSH with known_hosts, screen and java. Boundaries: no general-purpose shell, unknown SSH hosts rejected, every server JAR checked against Mojang's SHA-1."></a>
<sub>&nbsp;&nbsp;<a href="https://github.com/zaydzaari/RemoteCraft">repo</a></sub>

<br>

<sub><code>02 / FIELD STUDY</code>&nbsp; 642 models trained to answer one narrow question</sub>

<a href="https://github.com/zaydzaari/geographic-training-diversity-forest-loss"><img src="assets/planes/study-forest-loss.svg" width="100%" alt="Field study, manuscript in preparation. Under a fixed data budget, does multispectral Sentinel-2 keep its edge over RGB as forest-loss models train on more regions of the Brazilian Amazon? 107 configurations, 642 models, 2,568 zero-shot evaluations, 48 patches per model. The F1 interaction slope's 95% bootstrap interval crosses zero: no clear evidence the advantage changes with region count."></a>
<sub>&nbsp;&nbsp;<a href="https://github.com/zaydzaari/geographic-training-diversity-forest-loss">code, configs and frozen results</a> · <a href="https://orcid.org/0009-0007-5967-1692">ORCID</a></sub>

<br>

<sub><code>03 / BENCH</code>&nbsp; one shipped product, one lab run</sub>

<a href="https://github.com/zaydzaari/studymaster-ai"><img src="assets/planes/bench-studymaster.svg" width="100%" alt="StudyMaster AI, live on Vercel. Turns study material into summaries, quizzes, mind maps, spaced repetition and an AI tutor that can read PDFs. React, Express, Gemini API."></a>
<sub>&nbsp;&nbsp;<a href="https://github.com/zaydzaari/studymaster-ai">repo</a> · <a href="https://studymaster-ai-two.vercel.app">open the app</a></sub>

<a href="https://github.com/zaydzaari/trident-fps"><img src="assets/planes/bench-trident.svg" width="100%" alt="TRIDENT, lab. A browser 3D tactical shooter built as an agentic-coding benchmark run in Google Antigravity, with an authoritative WebSocket server, four agents and a round economy. TypeScript, Three.js, React."></a>
<sub>&nbsp;&nbsp;<a href="https://github.com/zaydzaari/trident-fps">repo</a></sub>

<br>

<sub><code>04 / TOPOLOGY</code>&nbsp; how the projects relate, and what they share</sub>

<img src="assets/constellation.svg" width="100%" alt="Constellation of original repositories. Angle groups them by theme, distance from the centre is age, and recently pushed projects glow. Links: LinkScribe and RemoteCraft share FastAPI; RemoteCraft and HomePC share allow-listed actions; HomePC and TRIDENT share WebSockets; TRIDENT and StudyMaster share React; LinkScribe and the forest-loss study share model inference; StudyMaster and LinkScribe share LLM tooling.">

<br>

<sub><code>05 / TOOLCHAIN</code>&nbsp; grouped by what it's for; every row traces back to a repo</sub>

<img src="assets/toolchain.svg" width="100%" alt="Toolchain. Build: Python, TypeScript, JavaScript, C# and .NET 8. Serve: FastAPI, Express, SQLite job queues, WebSockets, Cloudflare Workers and Durable Objects. Infer: whisper.cpp, FFmpeg, yt-dlp, PyTorch, Gemini and OpenRouter. Guard: bearer tokens, OAuth 2.0, SSH known_hosts, DPAPI, rate limits, checksums. Run: Linux, ARM64, systemd, Nginx and certbot, Vercel. Prove: pytest, Vitest, GitHub Actions CI, fixed seeds.">

<br>

<sub><code>06 / TELEMETRY</code>&nbsp; measured, not claimed</sub>

<img src="assets/telemetry.svg" width="100%" alt="GitHub telemetry: original repositories, forks, stars, languages and contributions from the public API, with each language's share of code bytes.">

<img src="assets/signal.svg" width="100%" alt="Daily contributions over the last twelve months, drawn as a signal trace. Activity arrives in short bursts, and most bursts line up with a new repository being created.">

<br>

<sub><code>07 / EGRESS</code></sub>

Open to collaborating on agent tooling, self-hosted infrastructure and applied ML research. The fastest route is an issue or discussion on any of the repos above.

<sub><a href="https://github.com/zaydzaari">github.com/zaydzaari</a> · <a href="https://orcid.org/0009-0007-5967-1692">orcid.org/0009-0007-5967-1692</a> · <a href="https://studymaster-ai-two.vercel.app">studymaster-ai-two.vercel.app</a></sub>

<img src="assets/footer.svg" width="100%" alt="Session closed. Inbound ports opened: zero.">
