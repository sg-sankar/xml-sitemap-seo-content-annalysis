# 🛸 Sitemap Copilot

**See everything your competitor is hiding in plain sight.**

A free, open-source SEO intelligence tool that turns any sitemap into a full competitive analysis — in seconds. No login. No payment. No fluff.

[![Live App](https://img.shields.io/badge/Live%20App-Streamlit-blue?style=flat-square&logo=streamlit)](https://xml-sitemap-seo-analysis-by-sankar-guru.streamlit.app)
[![Built by Sankar](https://img.shields.io/badge/Built%20by-Sankar%20Gurumurthy-2563eb?style=flat-square)](https://www.linkedin.com/in/sankar-gurumurthy-a1044a136/)
[![GitHub](https://img.shields.io/badge/GitHub-sg--sankar-111827?style=flat-square&logo=github)](https://github.com/sg-sankar)

---

## 🚀 Try it live

**[https://xml-sitemap-seo-analysis-by-sankar-guru.streamlit.app](https://xml-sitemap-seo-analysis-by-sankar-guru.streamlit.app)**

No signup. No install. Just paste a URL and go.

---

## What it does

Paste any `robots.txt` or `sitemap.xml` URL and get a complete breakdown of your competitor's content architecture:

- **Site Hierarchy** — expandable tree showing every section, sub-section and directory level with URL counts
- **URL Structure** — depth distribution, length analysis, slug word counts
- **N-Gram Analysis** — most frequent words and phrases across full URLs and slugs — reveals content strategy instantly
- **Temporal Analysis** — publishing velocity, freshness heatmap, seasonal patterns, section activity
- **Content Gap Opportunities** — which sections your competitor has abandoned (high stale % = your attack zone)
- **Advanced EDA** — depth vs recency, URL length hygiene, section × freshness breakdown with actionable SEO insights
- **Raw Data** — searchable, filterable table of every URL with CSV export
- **Export** — clean HTML report (print to PDF) with full analysis, no clutter

---

## Who it's for

SEO professionals who want to understand a competitor's content architecture without paying for expensive tools. This tells you:

- Where they're investing content budget right now
- Where they've stopped investing (your opportunity)
- How they structure their URLs and what keywords dominate their slugs
- How fresh vs stale their content is, section by section
- Their publishing patterns — when they're active and when they go quiet

---

## Supports

- `robots.txt` — auto-discovers all sitemaps
- `sitemap.xml` — direct sitemap files
- Sitemap index files — fetches all child sitemaps automatically
- Nested sitemaps — multi-level index files
- Gzipped sitemaps — `.xml.gz` format

Rate limiting handled automatically — large sites (100k+ URLs) fetched with intelligent delays to avoid 429 errors.

---

## Run locally

```bash
git clone https://github.com/sg-sankar/xml-sitemap-seo-content-analysis
cd xml-sitemap-seo-content-analysis
pip install -r requirements.txt
streamlit run app.py
```

---

## Stack

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io) | App framework |
| [advertools](https://github.com/eliasdabbas/advertools) | Sitemap parsing |
| [Plotly](https://plotly.com) | Charts |
| [pandas](https://pandas.pydata.org) | Data processing |

---

## Built by

**Sankar Gurumurthy** — Head of AI SEO & Marketing Data Scientist

[LinkedIn](https://www.linkedin.com/in/sankar-gurumurthy-a1044a136/) · [GitHub](https://github.com/sg-sankar)

---

*Open source · Free forever · No login required*
