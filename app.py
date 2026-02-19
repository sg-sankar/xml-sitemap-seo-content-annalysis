import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import advertools as adv
import requests
import re
from urllib.parse import urlparse
from collections import Counter
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sitemap Intelligence",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    color: #e8e6e0;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 20%, #1a1035 0%, #0a0a0f 50%, #0d1a0d 100%);
    min-height: 100vh;
}

h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif;
    letter-spacing: -0.02em;
}

/* Hero */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.5rem, 6vw, 5rem);
    font-weight: 800;
    background: linear-gradient(135deg, #a8ff78 0%, #78ffd6 50%, #7affb2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.05;
    margin-bottom: 0.5rem;
}
.hero-sub {
    font-size: 1.1rem;
    color: #888;
    font-weight: 300;
    margin-bottom: 2rem;
}

/* Metric cards */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}
.metric-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.25rem 1rem;
    text-align: center;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: rgba(168,255,120,0.3); }
.metric-num {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #a8ff78;
    line-height: 1;
}
.metric-label {
    font-size: 0.78rem;
    color: #777;
    margin-top: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Section headers */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #e8e6e0;
    margin: 2rem 0 1rem;
    padding-left: 0.75rem;
    border-left: 3px solid #a8ff78;
}

/* Input styling */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    color: #e8e6e0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #a8ff78 !important;
    box-shadow: 0 0 0 2px rgba(168,255,120,0.15) !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #a8ff78, #78ffd6) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2.5rem !important;
    transition: opacity 0.2s, transform 0.1s !important;
    width: 100% !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    color: #888 !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.25rem !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(168,255,120,0.15) !important;
    color: #a8ff78 !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* Download button */
.stDownloadButton > button {
    background: rgba(168,255,120,0.1) !important;
    color: #a8ff78 !important;
    border: 1px solid rgba(168,255,120,0.3) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
}

/* Divider */
hr { border-color: rgba(255,255,255,0.06) !important; }

/* Plotly chart backgrounds override */
.js-plotly-plot { border-radius: 12px; overflow: hidden; }

/* Info boxes */
.stAlert { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────

PLOT_THEME = dict(
    paper_bgcolor='rgba(20,18,30,0.0)',
    plot_bgcolor='rgba(20,18,30,0.0)',
    font_color='#b0ae9e',
    font_family='DM Sans',
    colorway=['#a8ff78','#78ffd6','#ff7eb3','#ffd278','#7eb8ff','#ff9f7e'],
    xaxis=dict(gridcolor='rgba(255,255,255,0.06)', linecolor='rgba(255,255,255,0.1)'),
    yaxis=dict(gridcolor='rgba(255,255,255,0.06)', linecolor='rgba(255,255,255,0.1)'),
    title_font_family='Syne',
    title_font_size=15,
)

def apply_theme(fig):
    fig.update_layout(**PLOT_THEME)
    fig.update_xaxes(gridcolor='rgba(255,255,255,0.06)', linecolor='rgba(255,255,255,0.1)')
    fig.update_yaxes(gridcolor='rgba(255,255,255,0.06)', linecolor='rgba(255,255,255,0.1)')
    return fig


def extract_sitemaps_from_robots(robots_url):
    """Parse robots.txt and return all Sitemap: entries."""
    try:
        r = requests.get(robots_url, timeout=15, headers={'User-Agent': 'SitemapAnalyzer/1.0'})
        r.raise_for_status()
        sitemaps = re.findall(r'(?i)^Sitemap:\s*(.+)', r.text, re.MULTILINE)
        return [s.strip() for s in sitemaps]
    except Exception as e:
        return []


def fetch_sitemap_df(url):
    """Fetch sitemap(s) into a DataFrame using advertools."""
    return adv.sitemap_to_df(url)


def get_url_parts(url):
    parsed = urlparse(url)
    path = parsed.path.rstrip('/')
    parts = [p for p in path.split('/') if p]
    return parts


def get_ngrams(tokens, n):
    return [' '.join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]


def tokenize_slug(slug):
    """Split a URL slug into tokens."""
    slug = slug.lower()
    slug = re.sub(r'[_\-]', ' ', slug)
    slug = re.sub(r'[^a-z0-9 ]', '', slug)
    return [t for t in slug.split() if t and len(t) > 1]


def build_ngram_df(all_tokens, max_n=5):
    results = {}
    for n in range(1, max_n+1):
        ngrams = []
        for tokens in all_tokens:
            ngrams.extend(get_ngrams(tokens, n))
        c = Counter(ngrams)
        label = {1:'Unigrams',2:'Bigrams',3:'Trigrams',4:'4-grams',5:'5-grams'}[n]
        results[label] = pd.DataFrame(c.most_common(30), columns=['ngram','count'])
    return results


# ── Main App ──────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero">
  <div class="hero-title">Sitemap Intelligence</div>
  <div class="hero-sub">Professional SEO competitor analysis — paste a URL, get deep insights instantly</div>
</div>
""", unsafe_allow_html=True)

col_inp, col_btn = st.columns([5, 1])
with col_inp:
    input_url = st.text_input(
        "",
        placeholder="Paste robots.txt or sitemap URL — e.g. https://example.com/robots.txt",
        label_visibility="collapsed"
    )
with col_btn:
    st.markdown("<div style='padding-top:0.2rem'></div>", unsafe_allow_html=True)
    run = st.button("Analyse →")

if not run or not input_url:
    st.markdown("""
    <div style='text-align:center; padding: 3rem; color: #444; font-size:0.9rem;'>
        Supports <b style='color:#666'>robots.txt</b> · <b style='color:#666'>sitemap.xml</b> · <b style='color:#666'>sitemap index files</b> · <b style='color:#666'>nested sitemaps</b>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Fetch Data ────────────────────────────────────────────────────────────────
with st.spinner("🔍 Fetching and parsing sitemap data…"):
    sitemap_urls = []

    if 'robots.txt' in input_url.lower():
        sitemap_urls = extract_sitemaps_from_robots(input_url)
        if not sitemap_urls:
            st.error("Could not find any Sitemap: entries in robots.txt. Please check the URL.")
            st.stop()
    else:
        sitemap_urls = [input_url]

    all_dfs = []
    errors = []
    for surl in sitemap_urls:
        try:
            df_temp = fetch_sitemap_df(surl)
            all_dfs.append(df_temp)
        except Exception as e:
            errors.append(f"{surl}: {e}")

    if not all_dfs:
        st.error(f"Failed to fetch any sitemaps. Errors: {errors}")
        st.stop()

    df = pd.concat(all_dfs, ignore_index=True)
    if 'loc' not in df.columns:
        st.error("No URLs found in sitemap.")
        st.stop()

    df = df.drop_duplicates(subset='loc')
    df = df[df['loc'].notna() & df['loc'].str.startswith('http')]
    df = df.reset_index(drop=True)

    # Parse lastmod
    if 'lastmod' in df.columns:
        df['lastmod_dt'] = pd.to_datetime(df['lastmod'], errors='coerce', utc=True)
    else:
        df['lastmod_dt'] = pd.NaT

    # Parse URL parts
    df['url_parts'] = df['loc'].apply(get_url_parts)
    df['url_depth'] = df['url_parts'].apply(len)
    df['last_slug'] = df['url_parts'].apply(lambda x: x[-1] if x else '')
    df['domain'] = df['loc'].apply(lambda u: urlparse(u).netloc)

    for i in range(1, 8):
        df[f'dir_{i}'] = df['url_parts'].apply(lambda x: x[i-1] if len(x) >= i else None)

# ── Overview Metrics ──────────────────────────────────────────────────────────
now = pd.Timestamp.now(tz='UTC')
last_week = now - timedelta(days=7)
last_month = now - timedelta(days=30)
last_quarter = now - timedelta(days=90)
last_year = now - timedelta(days=365)

n_total = len(df)
n_with_date = df['lastmod_dt'].notna().sum()
n_week = (df['lastmod_dt'] >= last_week).sum() if n_with_date else 0
n_month = (df['lastmod_dt'] >= last_month).sum() if n_with_date else 0
n_quarter = (df['lastmod_dt'] >= last_quarter).sum() if n_with_date else 0
n_year = (df['lastmod_dt'] >= last_year).sum() if n_with_date else 0
avg_depth = df['url_depth'].mean()
max_depth = df['url_depth'].max()

st.markdown(f"""
<div class="metric-grid">
  <div class="metric-card"><div class="metric-num">{n_total:,}</div><div class="metric-label">Total URLs</div></div>
  <div class="metric-card"><div class="metric-num">{avg_depth:.1f}</div><div class="metric-label">Avg URL Depth</div></div>
  <div class="metric-card"><div class="metric-num">{max_depth}</div><div class="metric-label">Max Depth</div></div>
  <div class="metric-card"><div class="metric-num">{n_week:,}</div><div class="metric-label">Updated Last Week</div></div>
  <div class="metric-card"><div class="metric-num">{n_month:,}</div><div class="metric-label">Updated Last Month</div></div>
  <div class="metric-card"><div class="metric-num">{n_quarter:,}</div><div class="metric-label">Updated Last Quarter</div></div>
  <div class="metric-card"><div class="metric-num">{n_year:,}</div><div class="metric-label">Updated Last Year</div></div>
  <div class="metric-card"><div class="metric-num">{n_with_date:,}</div><div class="metric-label">Have Dates</div></div>
</div>
""", unsafe_allow_html=True)

if errors:
    with st.expander(f"⚠️ {len(errors)} sitemap(s) had errors"):
        for e in errors:
            st.text(e)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs(["🏗 URL Structure", "📝 N-Gram Analysis", "📅 Temporal Analysis", "🔬 Advanced EDA", "📋 Raw Data", "📥 Export"])

# ════════════════════════════════════════════════════════════════════
# TAB 1 — URL STRUCTURE
# ════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-header">URL Depth Distribution</div>', unsafe_allow_html=True)

    depth_counts = df['url_depth'].value_counts().sort_index().reset_index()
    depth_counts.columns = ['depth','count']
    depth_counts['pct'] = (depth_counts['count'] / n_total * 100).round(1)

    col1, col2 = st.columns([3, 2])
    with col1:
        fig = px.bar(depth_counts, x='depth', y='count',
                     text='count', title='URLs by Depth Level',
                     color='count', color_continuous_scale='Teal')
        fig.update_traces(textposition='outside', marker_line_width=0)
        fig.update_layout(coloraxis_showscale=False, xaxis_title='Depth', yaxis_title='URL Count')
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.dataframe(depth_counts.style.format({'pct': '{:.1f}%'}), use_container_width=True, height=350)

    # Directory level analysis
    for level in range(1, min(max_depth+1, 8)):
        col_name = f'dir_{level}'
        if df[col_name].notna().sum() == 0:
            break
        st.markdown(f'<div class="section-header">Directory Level {level}</div>', unsafe_allow_html=True)
        vc = df[col_name].value_counts().head(25).reset_index()
        vc.columns = [f'dir_{level}', 'count']
        vc['pct'] = (vc['count'] / n_total * 100).round(1)

        col1, col2 = st.columns([3, 2])
        with col1:
            fig = px.bar(vc, x='count', y=vc.columns[0], orientation='h',
                         title=f'Top Values at Directory Level {level}',
                         color='count', color_continuous_scale='Teal')
            fig.update_layout(yaxis={'categoryorder': 'total ascending'}, coloraxis_showscale=False)
            apply_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.dataframe(vc.style.format({'pct': '{:.1f}%'}), use_container_width=True, height=350)

    # URL length analysis
    st.markdown('<div class="section-header">URL Length Analysis</div>', unsafe_allow_html=True)
    df['url_length'] = df['loc'].apply(len)
    df['slug_word_count'] = df['last_slug'].apply(lambda s: len(re.findall(r'[a-zA-Z0-9]+', str(s))))

    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(df, x='url_length', nbins=50, title='URL Character Length Distribution',
                           color_discrete_sequence=['#a8ff78'])
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.histogram(df, x='slug_word_count', nbins=20, title='Last Slug Word Count Distribution',
                           color_discrete_sequence=['#78ffd6'])
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Sunburst for URL hierarchy (top 2 levels)
    st.markdown('<div class="section-header">URL Hierarchy Sunburst (Top 2 Levels)</div>', unsafe_allow_html=True)
    sun_df = df[df['dir_1'].notna()].copy()
    sun_df['dir_2_filled'] = sun_df['dir_2'].fillna('[leaf]')
    sun_agg = sun_df.groupby(['dir_1','dir_2_filled']).size().reset_index(name='count')
    sun_agg = sun_agg[sun_agg['dir_1'].isin(sun_agg.groupby('dir_1')['count'].sum().nlargest(20).index)]

    fig = px.sunburst(sun_agg, path=['dir_1','dir_2_filled'], values='count',
                      color='count', color_continuous_scale='Teal',
                      title='URL Structure — Top 20 First-Level Directories')
    fig.update_layout(coloraxis_showscale=False)
    apply_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

    # Treemap
    st.markdown('<div class="section-header">URL Treemap</div>', unsafe_allow_html=True)
    tree_df = df[df['dir_1'].notna()].copy()
    tree_df['dir_2_filled'] = tree_df['dir_2'].fillna('[leaf]')
    tree_agg = tree_df.groupby(['dir_1','dir_2_filled']).size().reset_index(name='count')
    top_dirs = tree_agg.groupby('dir_1')['count'].sum().nlargest(15).index
    tree_agg = tree_agg[tree_agg['dir_1'].isin(top_dirs)]

    fig = px.treemap(tree_agg, path=['dir_1','dir_2_filled'], values='count',
                     color='count', color_continuous_scale='Teal',
                     title='URL Structure Treemap')
    apply_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════════════
# TAB 2 — N-GRAM ANALYSIS
# ════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-header">N-Gram Analysis — Full URL Slugs</div>', unsafe_allow_html=True)

    # Full URL token analysis
    all_tokens_full = df['loc'].apply(lambda u: tokenize_slug(urlparse(u).path)).tolist()
    ngram_full = build_ngram_df(all_tokens_full)

    # Last slug only
    all_tokens_slug = df['last_slug'].apply(tokenize_slug).tolist()
    ngram_slug = build_ngram_df(all_tokens_slug)

    subtabs = st.tabs(["Full URL Path", "Last Slug Only"])

    for tab_obj, ngram_dict, label in [(subtabs[0], ngram_full, 'Full URL'), (subtabs[1], ngram_slug, 'Last Slug')]:
        with tab_obj:
            for ngram_label, ngram_df_item in ngram_dict.items():
                if ngram_df_item.empty:
                    continue
                st.markdown(f'<div class="section-header">{ngram_label} — {label}</div>', unsafe_allow_html=True)
                top = ngram_df_item.head(20)
                col1, col2 = st.columns([3, 2])
                with col1:
                    fig = px.bar(top, x='count', y='ngram', orientation='h',
                                 title=f'Top 20 {ngram_label}',
                                 color='count', color_continuous_scale='Teal')
                    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, coloraxis_showscale=False)
                    apply_theme(fig)
                    st.plotly_chart(fig, use_container_width=True)
                with col2:
                    st.dataframe(top, use_container_width=True, height=350)


# ════════════════════════════════════════════════════════════════════
# TAB 3 — TEMPORAL ANALYSIS
# ════════════════════════════════════════════════════════════════════
with tabs[2]:
    if n_with_date == 0:
        st.info("No lastmod dates found in this sitemap. Temporal analysis not available.")
    else:
        dated = df[df['lastmod_dt'].notna()].copy()
        dated['year'] = dated['lastmod_dt'].dt.year
        dated['month'] = dated['lastmod_dt'].dt.to_period('M').astype(str)
        dated['yearweek'] = dated['lastmod_dt'].dt.to_period('W').astype(str)
        dated['quarter'] = dated['lastmod_dt'].dt.to_period('Q').astype(str)

        st.markdown('<div class="section-header">Publishing Velocity Over Time (Monthly)</div>', unsafe_allow_html=True)
        monthly = dated.groupby('month').size().reset_index(name='count')
        monthly = monthly.sort_values('month')
        fig = px.line(monthly, x='month', y='count', title='Monthly Content Publishing Velocity',
                      markers=True, color_discrete_sequence=['#a8ff78'])
        fig.update_traces(line_width=2.5, marker_size=6)
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-header">By Year</div>', unsafe_allow_html=True)
            yearly = dated.groupby('year').size().reset_index(name='count')
            fig = px.bar(yearly, x='year', y='count', title='URLs Updated Per Year',
                         color='count', color_continuous_scale='Teal', text='count')
            fig.update_traces(textposition='outside', marker_line_width=0)
            fig.update_layout(coloraxis_showscale=False)
            apply_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.markdown('<div class="section-header">By Quarter</div>', unsafe_allow_html=True)
            quarterly = dated.groupby('quarter').size().reset_index(name='count')
            quarterly = quarterly.sort_values('quarter').tail(12)
            fig = px.bar(quarterly, x='quarter', y='count', title='URLs Updated Per Quarter (Last 12)',
                         color='count', color_continuous_scale='Teal', text='count')
            fig.update_traces(textposition='outside', marker_line_width=0)
            fig.update_layout(coloraxis_showscale=False)
            apply_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

        # Temporal buckets
        st.markdown('<div class="section-header">Content Freshness Buckets</div>', unsafe_allow_html=True)
        def freshness_bucket(dt):
            if pd.isna(dt): return 'No Date'
            if dt >= last_week: return 'Last Week'
            elif dt >= last_month: return 'Last Month'
            elif dt >= last_quarter: return 'Last Quarter'
            elif dt >= last_year: return 'Last Year'
            else: return 'Older than 1 Year'

        df['freshness'] = df['lastmod_dt'].apply(freshness_bucket)
        fresh_order = ['Last Week','Last Month','Last Quarter','Last Year','Older than 1 Year','No Date']
        fresh_counts = df['freshness'].value_counts().reindex(fresh_order, fill_value=0).reset_index()
        fresh_counts.columns = ['bucket','count']
        fresh_counts['pct'] = (fresh_counts['count'] / n_total * 100).round(1)

        col1, col2 = st.columns([3, 2])
        with col1:
            fig = px.bar(fresh_counts, x='bucket', y='count', text='count',
                         title='Content Freshness Distribution',
                         color='bucket',
                         color_discrete_sequence=['#a8ff78','#78ffd6','#7eb8ff','#ffd278','#ff7eb3','#888'])
            fig.update_traces(textposition='outside', marker_line_width=0, showlegend=False)
            apply_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.dataframe(fresh_counts.style.format({'pct': '{:.1f}%'}), use_container_width=True, height=300)

        # Heatmap: month x year
        st.markdown('<div class="section-header">Publishing Activity Heatmap</div>', unsafe_allow_html=True)
        dated['month_num'] = dated['lastmod_dt'].dt.month
        heatmap_df = dated.groupby(['year','month_num']).size().reset_index(name='count')
        heatmap_pivot = heatmap_df.pivot(index='year', columns='month_num', values='count').fillna(0)
        month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        heatmap_pivot.columns = [month_names[c-1] for c in heatmap_pivot.columns]

        fig = px.imshow(heatmap_pivot, color_continuous_scale='Teal',
                        title='Publishing Heatmap (Year × Month)',
                        aspect='auto')
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

        # Temporal + directory cross analysis
        if df['dir_1'].notna().sum() > 0:
            st.markdown('<div class="section-header">Directory vs Update Frequency (Bivariate)</div>', unsafe_allow_html=True)
            dated_dir = dated[dated['dir_1'].notna()].copy()
            top_dirs_list = dated_dir['dir_1'].value_counts().head(10).index
            dated_dir = dated_dir[dated_dir['dir_1'].isin(top_dirs_list)]
            dir_month = dated_dir.groupby(['dir_1','month']).size().reset_index(name='count')
            dir_month = dir_month.sort_values('month')
            fig = px.line(dir_month, x='month', y='count', color='dir_1',
                          title='Top 10 Directories — Publishing Velocity Over Time')
            apply_theme(fig)
            st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════════════
# TAB 4 — ADVANCED EDA
# ════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-header">URL Depth vs Update Frequency (Bivariate)</div>', unsafe_allow_html=True)
    if n_with_date > 0:
        depth_fresh = df.groupby('url_depth')['lastmod_dt'].count().reset_index()
        depth_fresh.columns = ['depth','updated_count']
        depth_total = df.groupby('url_depth').size().reset_index(name='total')
        depth_merge = depth_fresh.merge(depth_total, on='depth')
        depth_merge['update_rate'] = (depth_merge['updated_count'] / depth_merge['total'] * 100).round(1)

        col1, col2 = st.columns(2)
        with col1:
            fig = px.scatter(depth_merge, x='depth', y='update_rate', size='total',
                             title='URL Depth vs Update Rate %',
                             color='update_rate', color_continuous_scale='Teal',
                             hover_data=['total'])
            apply_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.bar(depth_merge, x='depth', y='update_rate',
                         title='Update Rate by Depth Level',
                         color='update_rate', color_continuous_scale='Teal', text='update_rate')
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside', marker_line_width=0)
            fig.update_layout(coloraxis_showscale=False)
            apply_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

    # URL length vs depth (bivariate)
    st.markdown('<div class="section-header">URL Length vs Depth (Bivariate)</div>', unsafe_allow_html=True)
    fig = px.box(df, x='url_depth', y='url_length', title='URL Character Length Distribution by Depth',
                 color='url_depth', color_discrete_sequence=px.colors.sequential.Teal)
    fig.update_layout(showlegend=False)
    apply_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

    # Stale content by directory
    if df['dir_1'].notna().sum() > 0 and n_with_date > 0:
        st.markdown('<div class="section-header">Stale Content by Directory (2+ Years Old)</div>', unsafe_allow_html=True)
        two_years_ago = now - timedelta(days=730)
        df['is_stale'] = (df['lastmod_dt'] < two_years_ago) | df['lastmod_dt'].isna()
        stale_by_dir = df[df['dir_1'].notna()].groupby('dir_1').agg(
            total=('loc','count'),
            stale=('is_stale','sum')
        ).reset_index()
        stale_by_dir['stale_pct'] = (stale_by_dir['stale'] / stale_by_dir['total'] * 100).round(1)
        stale_by_dir = stale_by_dir.sort_values('stale_pct', ascending=False).head(20)

        col1, col2 = st.columns([3, 2])
        with col1:
            fig = px.bar(stale_by_dir, x='stale_pct', y='dir_1', orientation='h',
                         title='Stale Content % by Directory (Top 20)',
                         color='stale_pct', color_continuous_scale='RdYlGn_r',
                         hover_data=['total','stale'])
            fig.update_layout(yaxis={'categoryorder':'total ascending'}, coloraxis_showscale=False)
            apply_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.dataframe(stale_by_dir.style.format({'stale_pct': '{:.1f}%'}), use_container_width=True)

    # Multivariate: depth + directory + freshness
    if df['dir_1'].notna().sum() > 0 and n_with_date > 0:
        st.markdown('<div class="section-header">Multivariate: Directory × Depth × Freshness</div>', unsafe_allow_html=True)
        top10 = df['dir_1'].value_counts().head(10).index
        mv_df = df[df['dir_1'].isin(top10)].copy()
        mv_agg = mv_df.groupby(['dir_1','url_depth','freshness']).size().reset_index(name='count')
        fig = px.sunburst(mv_agg, path=['dir_1','freshness'], values='count',
                          color='url_depth', color_continuous_scale='Teal',
                          title='Directory → Freshness (colored by avg depth)')
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Priority analysis if available
    if 'priority' in df.columns and df['priority'].notna().sum() > 0:
        st.markdown('<div class="section-header">Priority Distribution</div>', unsafe_allow_html=True)
        df['priority_num'] = pd.to_numeric(df['priority'], errors='coerce')
        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(df, x='priority_num', nbins=20,
                               title='Priority Value Distribution',
                               color_discrete_sequence=['#a8ff78'])
            apply_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            if df['dir_1'].notna().sum() > 0:
                prio_dir = df[df['dir_1'].notna()].groupby('dir_1')['priority_num'].mean().reset_index()
                prio_dir.columns = ['dir_1','avg_priority']
                prio_dir = prio_dir.sort_values('avg_priority', ascending=False).head(20)
                fig = px.bar(prio_dir, x='avg_priority', y='dir_1', orientation='h',
                             title='Avg Priority by Directory',
                             color='avg_priority', color_continuous_scale='Teal')
                fig.update_layout(yaxis={'categoryorder':'total ascending'}, coloraxis_showscale=False)
                apply_theme(fig)
                st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════════════
# TAB 5 — RAW DATA
# ════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-header">Raw Sitemap Data</div>', unsafe_allow_html=True)
    display_cols = [c for c in ['loc','lastmod','changefreq','priority','url_depth','freshness'] if c in df.columns]
    st.dataframe(df[display_cols], use_container_width=True, height=500)

    csv = df[display_cols].to_csv(index=False).encode('utf-8')
    st.download_button("⬇ Download CSV", csv, "sitemap_data.csv", "text/csv")


# ════════════════════════════════════════════════════════════════════
# TAB 6 — EXPORT
# ════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-header">Export Report</div>', unsafe_allow_html=True)
    st.info("📄 A full HTML report with all charts and tables can be generated below. Open it in any browser or print to PDF.")

    # Build HTML report
    def make_html_report():
        domain_name = df['domain'].iloc[0] if 'domain' in df.columns else 'Unknown'
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M')

        sections = []
        sections.append(f"""
        <h1>Sitemap Intelligence Report</h1>
        <p class="meta">Domain: <strong>{domain_name}</strong> &nbsp;|&nbsp; Generated: {now_str} &nbsp;|&nbsp; Total URLs: <strong>{n_total:,}</strong></p>
        """)

        # Metrics table
        sections.append("""<h2>Overview Metrics</h2><table>
        <tr><th>Metric</th><th>Value</th></tr>""")
        metrics = [
            ('Total URLs', f"{n_total:,}"),
            ('Avg URL Depth', f"{avg_depth:.1f}"),
            ('Max URL Depth', str(max_depth)),
            ('URLs with Dates', f"{n_with_date:,}"),
            ('Updated Last Week', f"{n_week:,}"),
            ('Updated Last Month', f"{n_month:,}"),
            ('Updated Last Quarter', f"{n_quarter:,}"),
            ('Updated Last Year', f"{n_year:,}"),
        ]
        for k, v in metrics:
            sections.append(f"<tr><td>{k}</td><td><strong>{v}</strong></td></tr>")
        sections.append("</table>")

        # Directory tables
        sections.append("<h2>Directory Level Analysis</h2>")
        for level in range(1, min(max_depth+1, 8)):
            col_name = f'dir_{level}'
            if df[col_name].notna().sum() == 0:
                break
            vc = df[col_name].value_counts().head(20).reset_index()
            vc.columns = ['directory','count']
            vc['pct'] = (vc['count'] / n_total * 100).round(1)
            sections.append(f"<h3>Level {level} Directories</h3>")
            sections.append(vc.to_html(index=False, classes='data-table'))

        # N-grams
        sections.append("<h2>N-Gram Analysis (Full URL Path)</h2>")
        for label, ng_df in build_ngram_df(all_tokens_full).items():
            if ng_df.empty: continue
            sections.append(f"<h3>{label}</h3>")
            sections.append(ng_df.head(20).to_html(index=False, classes='data-table'))

        # Freshness
        if n_with_date > 0 and 'freshness' in df.columns:
            sections.append("<h2>Content Freshness</h2>")
            fresh_counts2 = df['freshness'].value_counts().reset_index()
            fresh_counts2.columns = ['bucket','count']
            fresh_counts2['pct'] = (fresh_counts2['count'] / n_total * 100).round(1)
            sections.append(fresh_counts2.to_html(index=False, classes='data-table'))

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sitemap Intelligence Report — {domain_name}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');
  body {{ font-family: 'DM Sans', sans-serif; background: #0a0a0f; color: #e8e6e0; max-width: 1100px; margin: 0 auto; padding: 2rem; }}
  h1 {{ font-family: 'Syne', sans-serif; font-size: 2.5rem; background: linear-gradient(135deg,#a8ff78,#78ffd6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:0.25rem; }}
  h2 {{ font-family: 'Syne', sans-serif; font-size: 1.4rem; color: #a8ff78; border-left: 3px solid #a8ff78; padding-left: 0.75rem; margin-top: 2.5rem; }}
  h3 {{ font-family: 'Syne', sans-serif; font-size: 1.1rem; color: #78ffd6; margin-top: 1.5rem; }}
  .meta {{ color: #888; font-size: 0.9rem; margin-bottom: 2rem; }}
  table.data-table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: 0.9rem; }}
  table.data-table th {{ background: rgba(168,255,120,0.12); color: #a8ff78; padding: 0.6rem 0.75rem; text-align: left; font-family: 'Syne', sans-serif; font-size: 0.85rem; letter-spacing: 0.04em; }}
  table.data-table td {{ padding: 0.5rem 0.75rem; border-bottom: 1px solid rgba(255,255,255,0.06); }}
  table.data-table tr:hover td {{ background: rgba(255,255,255,0.03); }}
  @media print {{ body {{ background: white; color: black; }} h1,h2,h3 {{ -webkit-text-fill-color: unset; color: #1a1a2e; }} table.data-table th {{ background: #1a1a2e; color: white; }} }}
</style>
</head>
<body>
{''.join(sections)}
<footer style="margin-top:3rem; color:#444; font-size:0.8rem; text-align:center;">Generated by Sitemap Intelligence · github.com/yourusername/sitemap-intelligence</footer>
</body>
</html>"""
        return html

    html_report = make_html_report()
    st.download_button(
        "⬇ Download HTML Report (open in browser / print to PDF)",
        html_report.encode('utf-8'),
        "sitemap_intelligence_report.html",
        "text/html"
    )
    st.markdown("""
    <div style='color:#666; font-size:0.88rem; margin-top:0.5rem;'>
    💡 <strong>To convert to PDF:</strong> Open the downloaded HTML file in Chrome → File → Print → Save as PDF
    </div>
    """, unsafe_allow_html=True)
