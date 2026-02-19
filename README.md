# 🗺️ Sitemap Intelligence

> **Professional SEO competitor analysis — paste a URL, get deep insights instantly.**

A powerful, free Streamlit app that turns any sitemap or robots.txt URL into a comprehensive SEO intelligence report. Built for SEO professionals who want real data, not guesswork.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

---

## ✨ What It Does

Paste any competitor's `robots.txt` or `sitemap.xml` URL and instantly get:

### 🏗 URL Structure Analysis
- Total URL count
- URL depth distribution (how deep is their site?)
- Directory level breakdown — 1st, 2nd, 3rd... all levels
- URL length analysis
- Sunburst + Treemap visualizations of site hierarchy

### 📝 N-Gram Analysis (1 to 5-grams)
- Unigrams, Bigrams, Trigrams, 4-grams, 5-grams
- Across the **full URL path**
- Across the **last slug only** (actual page identifier)

### 📅 Temporal Analysis
- Publishing velocity over time (monthly trend line)
- Heatmap of publishing activity (year × month)
- Content freshness buckets:
  - Updated Last Week
  - Updated Last Month
  - Updated Last Quarter
  - Updated Last Year
  - Older than 1 Year

### 🔬 Advanced EDA
- **Univariate**: URL depth, length, priority distributions
- **Bivariate**: Depth vs update rate, URL length vs depth
- **Multivariate**: Directory × Freshness × Depth sunburst
- Stale content analysis by directory
- Priority distribution (if available)

### 📥 Export
- Download full HTML report (open in browser → print to PDF)
- Download raw data as CSV

---

## 🚀 How to Use (No Installation Needed)

**Option 1: Use the live app**
👉 [Click here to open the app](https://your-app-url.streamlit.app)

**Option 2: Run locally**
```bash
git clone https://github.com/yourusername/sitemap-intelligence
cd sitemap-intelligence
pip install -r requirements.txt
streamlit run app.py
```

---

## 🌐 Supported Input Formats

| Input | Example |
|-------|---------|
| robots.txt URL | `https://example.com/robots.txt` |
| Direct sitemap | `https://example.com/sitemap.xml` |
| Sitemap index | `https://example.com/sitemap_index.xml` |
| Nested sitemaps | Handled automatically |
| Gzipped sitemaps | `.xml.gz` files supported |

---

## 🛠 Tech Stack

- **[Streamlit](https://streamlit.io)** — Web interface
- **[advertools](https://advertools.readthedocs.io)** — Sitemap parsing
- **[Plotly](https://plotly.com)** — Interactive charts
- **[Pandas](https://pandas.pydata.org)** — Data processing

---

## 📦 Deploy Your Own (Free)

1. Fork this repo on GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repo → `app.py`
5. Click Deploy — done! 🎉

---

## 🤝 Contributing

Pull requests welcome! Ideas for new analyses, better visualizations, or bug fixes are all appreciated.

---

## 📄 License

MIT License — use it however you want.

---

*Built with ❤️ for SEO professionals who want real data.*
