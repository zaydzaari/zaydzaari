<div align="center">

![Zayd Zaari - AI systems and product builder](https://capsule-render.vercel.app/api?type=waving&color=0:0F766E,48:2563EB,100:F59E0B&height=220&section=header&text=Zayd%20Zaari&fontSize=58&fontColor=FFFFFF&fontAlignY=36&desc=AI%20Systems%20%7C%20Agent%20Tooling%20%7C%20Product%20Builder&descAlignY=57&descSize=18&animation=fadeIn)

[![LinkScribe](https://img.shields.io/badge/Live-LinkScribe-0F766E?style=for-the-badge&logo=fastapi&logoColor=white)](https://51-170-131-7.sslip.io/)
[![StudyMaster AI](https://img.shields.io/badge/Launch-StudyMaster_AI-2563EB?style=for-the-badge&logo=vercel&logoColor=white)](https://studymaster-ai-two.vercel.app)
[![GitHub](https://img.shields.io/badge/Follow-@zaydzaari-181717?style=for-the-badge&logo=github)](https://github.com/zaydzaari?tab=followers)

</div>

## About me

I am a student developer from Morocco building practical AI tools and polished products. I am most interested in the engineering around AI: giving agents useful tools, running inference efficiently, designing reliable APIs, and turning experiments into software that people can actually use.

Right now I am focused on:

- agent tools for Codex, Claude Code, and custom GPTs
- local speech transcription and translation on resource-constrained hardware
- secure API design, background jobs, observability, and deployment
- accessible web and mobile products powered by AI

## Featured AI project

### [LinkScribe](https://github.com/zaydzaari/linkscribe)

**A self-hosted media understanding pipeline for AI agents.** LinkScribe accepts a public YouTube, TikTok, or Instagram URL, extracts only the audio, transcribes or translates it locally, and returns clean English text through an authenticated API. Codex, Claude Code, or a custom GPT can then reason over the video.

```text
Public media URL
      -> yt-dlp
      -> FFmpeg (16 kHz mono)
      -> whisper.cpp (local transcription + translation)
      -> FastAPI job queue
      -> Codex / Claude Code / custom GPT
```

- Runs on a 2-core ARM Oracle VPS with 12 GB RAM.
- Uses a single resource-aware worker so transcription cannot exhaust the server.
- Includes HTTPS, bearer authentication, rate limits, cleanup, and 24-hour job expiry.
- Ships ready-to-use Codex, Claude Code, and ChatGPT integrations.
- A 92-second spoken TikTok completed in about 36 seconds on the reference server.
- Verified by 39 tests with 84% coverage and a green GitHub Actions pipeline.

**[Repository](https://github.com/zaydzaari/linkscribe)** | **[Live service](https://51-170-131-7.sslip.io/)** | **[Demo video](https://github.com/zaydzaari/linkscribe/releases/download/v0.1.2/demo.mp4)** | **[Latest release](https://github.com/zaydzaari/linkscribe/releases/tag/v0.1.2)**

<div align="center">

![LinkScribe demo](https://raw.githubusercontent.com/zaydzaari/linkscribe/main/docs/demo.gif)

</div>

## Selected work

<div align="center">

<a href="https://github.com/zaydzaari/linkscribe">
  <img width="48%" src="./profile/linkscribe.svg" alt="LinkScribe repository card" />
</a>
<a href="https://github.com/zaydzaari/studymaster-ai">
  <img width="48%" src="./profile/studymaster-ai.svg" alt="StudyMaster AI repository card" />
</a>

</div>

| Project | What it demonstrates |
| --- | --- |
| [LinkScribe](https://github.com/zaydzaari/linkscribe) | Agent integrations, local inference, async APIs, ARM deployment, and production hardening |
| [StudyMaster AI](https://github.com/zaydzaari/studymaster-ai) | An AI-powered learning product with a live, user-facing web experience |
| [RemoteCraft](https://github.com/zaydzaari/RemoteCraft) | Remote Linux automation and server management over SSH |

## Technical focus

| Area | Tools and concepts |
| --- | --- |
| AI and agents | Codex skills, Claude Code skills, GPT Actions, whisper.cpp, tool calling, context handling |
| Backend | Python, FastAPI, SQLite, REST APIs, job queues, long polling, authentication |
| Media | yt-dlp, FFmpeg, speech transcription, multilingual translation |
| Infrastructure | Linux, ARM64, systemd, Nginx, Let's Encrypt, Oracle Cloud, GitHub Actions |
| Product | JavaScript, React, Expo, responsive UI, accessibility, deployment |

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=111111)
![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=111111)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)

</div>

## GitHub activity

<div align="center">

<img width="49%" src="./profile/stats.svg" alt="Zayd's GitHub statistics" />
<img width="49%" src="./profile/top-langs.svg" alt="Zayd's most-used public repository languages" />

</div>

## Connect

I am open to open-source collaboration, mentorship, hackathons, internships, and ambitious AI projects. If you are building something useful and need a motivated contributor, reach me through [GitHub](https://github.com/zaydzaari).

<div align="center">

![Footer](https://capsule-render.vercel.app/api?type=waving&color=0:F59E0B,48:2563EB,100:0F766E&height=110&section=footer)

</div>
