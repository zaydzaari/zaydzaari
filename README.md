# Zayd Zaari

**High school student in Morocco · AI tooling & applied machine learning**

`Applied ML` · `AI systems` · `Reproducible experiments`

I build practical AI tools and explore how models generalize to unfamiliar data. My work brings together software engineering, self-hosted inference, and controlled experiments. I’m looking to deepen my research skills through mentorship and collaboration.

[Research](https://github.com/zaydzaari/geographic-training-diversity-forest-loss) · [LinkScribe](https://github.com/zaydzaari/linkscribe) · [ORCID](https://orcid.org/0009-0007-5967-1692)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/academic-accent-dark.svg">
  <img src="assets/academic-accent-light.svg" width="100%" alt="">
</picture>

## Research in focus

### [Forest-loss detection across geographic regions](https://github.com/zaydzaari/geographic-training-diversity-forest-loss)

**Question:** does training on more regions change the advantage of multispectral imagery over RGB, independently of total training-data volume?

<table>
<tr>
<td align="center" width="300"><h3>107</h3>Configs</td>
<td align="center" width="300"><h3>642</h3>Models</td>
<td align="center" width="300"><h3>2,568</h3>Evaluations</td>
</tr>
</table>

<a href="https://raw.githubusercontent.com/zaydzaari/geographic-training-diversity-forest-loss/master/figures/Figure_2_Performance_vs_Training_Regions.png"><img src="https://raw.githubusercontent.com/zaydzaari/geographic-training-diversity-forest-loss/master/figures/Figure_2_Performance_vs_Training_Regions.png" width="100%" alt="Figure 2 from the forest-loss study: model performance versus number of training regions. Open the original image for full detail."></a>

*Figure from the study repository: performance as geographic training diversity changes. Open the image for the full-resolution figure.*

> **What the evidence supports**
>
> Multispectral models outperformed RGB at every tested region count. The 95% bootstrap interval for the interaction slope included zero, so the study found no clear evidence that this advantage changed systematically with geographic training diversity.

**Research status:** manuscript in preparation; not yet published.

<details>
<summary><strong>Experimental design & reproducibility</strong></summary>

- Fixed total budget: **48 training patches per model**, redistributed across regions.
- **1, 2, 4, or 8** training regions, enumerating all 107 subsets of the eight-region roster.
- RGB and multispectral inputs use paired, deterministic patch sampling.
- Two modalities and three seeds: **107 × 2 × 3 = 642 models**.
- Two validation regions for model selection; four separate regions for final testing.
- Frozen configurations, normalization artifacts, checkpoint hashes, and final results are documented in the repository.

[Methods and reproduction guide](https://github.com/zaydzaari/geographic-training-diversity-forest-loss/blob/master/docs/reproduction_guide.md)

</details>

## Engineering evidence

<table>
<tr><td valign="top" width="50%">

### [LinkScribe](https://github.com/zaydzaari/linkscribe)

**AI tooling / local inference**

English transcripts from public video links, served to AI agents through an authenticated FastAPI queue. Speech recognition runs locally with whisper.cpp on an ARM VPS.

Python · FastAPI · SQLite · FFmpeg

[Architecture & demo](https://github.com/zaydzaari/linkscribe)

</td><td valign="top" width="50%">

### [HomePC](https://github.com/zaydzaari/HomePC)

**Device control / distributed systems**

Google Home controls for Windows. A .NET agent connects outward to Cloudflare and executes a defined set of actions without exposing a remote terminal.

C# · .NET · Cloudflare · TypeScript

[Architecture & setup](https://github.com/zaydzaari/HomePC)

</td></tr>
</table>

### LinkScribe / From URL to transcript

<picture>
  <source media="(max-width: 520px) and (prefers-color-scheme: dark)" srcset="assets/linkscribe-pipeline-mobile-dark.svg">
  <source media="(max-width: 520px) and (prefers-color-scheme: light)" srcset="assets/linkscribe-pipeline-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/linkscribe-pipeline-dark.svg">
  <img src="assets/linkscribe-pipeline-light.svg" width="100%" alt="LinkScribe sends a media URL through a FastAPI queue, processes audio locally with FFmpeg and whisper.cpp, and returns English text to an AI agent.">
</picture>

**Also built:** [RemoteCraft](https://github.com/zaydzaari/RemoteCraft), a Minecraft server dashboard, and [Lumen](https://github.com/zaydzaari/Lumen), a native Rust music player for Windows and Linux.

## What I want to learn next

How to design stronger model evaluations, distinguish data effects from model improvements, and make experiments easier to reproduce. I’m interested in research mentorship where I can build on both the software and experimental sides of my work.

**Tools used:** Python, PyTorch, rasterio, FastAPI, SQLite, Rust, C#, Linux, GitHub Actions.

[Research methods](https://github.com/zaydzaari/geographic-training-diversity-forest-loss) · [ORCID](https://orcid.org/0009-0007-5967-1692) · [All repositories](https://github.com/zaydzaari?tab=repositories)
