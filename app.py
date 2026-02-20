import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import advertools as adv
import requests
import re
from urllib.parse import urlparse
from collections import Counter
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

PHOTO_B64 = "data:image/png;base64,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"

st.set_page_config(
    page_title="Sitemap Copilot · Sankar Gurumurthy",
    page_icon="🛩️", layout="wide", initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cabinet+Grotesk:wght@400;500;700;800;900&family=Inter:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #080810;
    color: #e2e0f0;
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: -20%;
    left: -10%;
    width: 60%;
    height: 60%;
    background: radial-gradient(ellipse, rgba(99,51,255,0.12) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    bottom: -10%;
    right: -10%;
    width: 50%;
    height: 50%;
    background: radial-gradient(ellipse, rgba(0,210,150,0.08) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

[data-testid="stAppViewContainer"] > div { position: relative; z-index: 1; }

h1,h2,h3,h4 { font-family: 'Cabinet Grotesk', sans-serif; }

/* Hero */
.hero { text-align: center; padding: 3rem 1rem 2rem; }
.hero-eyebrow {
    display: inline-block;
    font-size: 0.72rem; font-weight: 500; letter-spacing: 0.12em;
    text-transform: uppercase; color: #00d296;
    background: rgba(0,210,150,0.08);
    border: 1px solid rgba(0,210,150,0.2);
    padding: 0.3rem 0.9rem; border-radius: 100px;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: clamp(3rem, 7vw, 6rem);
    font-weight: 900;
    color: #fff;
    line-height: 0.95;
    letter-spacing: -0.03em;
    margin-bottom: 0.6rem;
}
.hero-title span {
    background: linear-gradient(135deg, #00d296 0%, #6333ff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1.05rem; color: #6b6a80; font-weight: 400;
    max-width: 480px; margin: 0 auto 2rem;
    line-height: 1.6;
}

/* Author card — bento style */
.author-card {
    display: inline-flex; align-items: center; gap: 1rem;
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px; padding: 0.9rem 1.4rem;
    margin-bottom: 2rem;
}
.author-photo {
    width: 52px; height: 52px; border-radius: 14px;
    object-fit: cover;
    border: 1px solid rgba(0,210,150,0.3);
}
.author-name { font-family: 'Cabinet Grotesk', sans-serif; font-size: 1rem; font-weight: 700; color: #fff; }
.author-role { font-size: 0.75rem; color: #00d296; margin: 0.1rem 0 0.35rem; font-weight: 500; }
.author-links a {
    display: inline-flex; align-items: center; gap: 0.25rem;
    font-size: 0.73rem; color: #6b6a80;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 0.18rem 0.55rem; border-radius: 100px;
    text-decoration: none; margin-right: 0.35rem;
    transition: all 0.15s;
}
.author-links a:hover { color: #00d296; border-color: rgba(0,210,150,0.3); }

/* Bento metric grid */
.bento-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin: 1.5rem 0;
}
.bento-card {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 1.2rem 1rem;
    text-align: center;
    transition: border-color 0.2s, transform 0.2s;
    position: relative; overflow: hidden;
}
.bento-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,210,150,0.3), transparent);
}
.bento-card:hover { border-color: rgba(0,210,150,0.2); transform: translateY(-2px); }
.bento-num {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 2.1rem; font-weight: 900;
    background: linear-gradient(135deg, #fff 0%, #a0ffd8 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.bento-label {
    font-size: 0.68rem; color: #4a4860;
    margin-top: 0.25rem; text-transform: uppercase;
    letter-spacing: 0.08em; font-weight: 500;
}

/* Section headers */
.sec-head {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 1.2rem; font-weight: 800;
    color: #fff; margin: 2rem 0 0.3rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.sec-head::before {
    content: '';
    display: inline-block; width: 3px; height: 1.1em;
    background: linear-gradient(180deg, #00d296, #6333ff);
    border-radius: 2px;
}
.sec-sub { font-size: 0.8rem; color: #4a4860; margin: 0 0 1rem 0.8rem; font-style: italic; }

/* Input */
.stTextInput>div>div>input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important;
    color: #e2e0f0 !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1.1rem !important;
    backdrop-filter: blur(10px) !important;
}
.stTextInput>div>div>input:focus {
    border-color: rgba(0,210,150,0.5) !important;
    box-shadow: 0 0 0 3px rgba(0,210,150,0.08) !important;
}

/* Button */
.stButton>button {
    background: linear-gradient(135deg, #00d296, #6333ff) !important;
    color: #fff !important;
    font-family: 'Cabinet Grotesk', sans-serif !important;
    font-weight: 700 !important; font-size: 0.95rem !important;
    border: none !important; border-radius: 14px !important;
    padding: 0.75rem 1.5rem !important; width: 100% !important;
    letter-spacing: 0.01em !important;
    transition: opacity 0.15s, transform 0.1s !important;
}
.stButton>button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px; padding: 4px; gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Cabinet Grotesk', sans-serif !important;
    font-weight: 600 !important; font-size: 0.85rem !important;
    color: #4a4860 !important; border-radius: 10px !important;
    padding: 0.4rem 1rem !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(0,210,150,0.1) !important;
    color: #00d296 !important;
}

/* Download button */
.stDownloadButton>button {
    background: rgba(0,210,150,0.08) !important;
    color: #00d296 !important;
    border: 1px solid rgba(0,210,150,0.2) !important;
    font-family: 'Cabinet Grotesk', sans-serif !important;
    font-weight: 600 !important; border-radius: 10px !important;
}

/* Selectbox */
.stSelectbox>div>div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important; color: #e2e0f0 !important;
}

/* Dataframe */
[data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; }

/* Footer */
.footer {
    text-align: center; padding: 2rem 1rem;
    color: #2a2840; font-size: 0.78rem;
    border-top: 1px solid rgba(255,255,255,0.04);
    margin-top: 4rem;
}
.footer a { color: #3a3860; text-decoration: none; }

/* Tree view */
.tree-node {
    font-family: 'Inter', monospace; font-size: 0.82rem;
    padding: 0.3rem 0.5rem; border-radius: 6px;
    color: #a0ffd8;
}

/* Domain badge */
.domain-badge {
    display: inline-block;
    background: rgba(99,51,255,0.1);
    border: 1px solid rgba(99,51,255,0.2);
    color: #a08fff;
    font-size: 0.78rem; padding: 0.2rem 0.7rem;
    border-radius: 100px; margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── Helpers ──────────────────────────────────────────────────────────────────
PLOT_CFG = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font_color='#6b6a80', font_family='Inter',
    title_font_family='Cabinet Grotesk', title_font_size=14, title_font_color='#e2e0f0',
    colorway=['#00d296','#6333ff','#ff6b9d','#ffd166','#06d6f5','#ff9f43'],
)

def T(fig, legend=False):
    fig.update_layout(**PLOT_CFG, showlegend=legend)
    fig.update_xaxes(gridcolor='rgba(255,255,255,0.04)', linecolor='rgba(255,255,255,0.06)', zeroline=False)
    fig.update_yaxes(gridcolor='rgba(255,255,255,0.04)', linecolor='rgba(255,255,255,0.06)', zeroline=False)
    return fig

def sec(title, sub=None):
    st.markdown(f'<div class="sec-head">{title}</div>', unsafe_allow_html=True)
    if sub: st.markdown(f'<div class="sec-sub">{sub}</div>', unsafe_allow_html=True)

def extract_sitemaps_from_robots(url):
    try:
        r = requests.get(url, timeout=15, headers={'User-Agent':'SitemapCopilot/1.0'})
        r.raise_for_status()
        return [s.strip() for s in re.findall(r'(?i)^Sitemap:\s*(.+)', r.text, re.MULTILINE)]
    except: return []

def tokenize(slug):
    s = re.sub(r'[_\-]', ' ', str(slug).lower())
    s = re.sub(r'[^a-z0-9 ]', '', s)
    return [t for t in s.split() if t and len(t) > 1]

def ngrams(tokens, n):
    return [' '.join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def build_ngrams(all_tokens, max_n=5):
    labels = {1:'Unigrams',2:'Bigrams',3:'Trigrams',4:'4-grams',5:'5-grams'}
    out = {}
    for n in range(1, max_n+1):
        grams = []
        for t in all_tokens: grams.extend(ngrams(t, n))
        out[labels[n]] = pd.DataFrame(Counter(grams).most_common(30), columns=['ngram','count'])
    return out

def freshness_label(dt, w, m, q, y):
    if pd.isna(dt): return 'No Date'
    if dt >= w: return 'Last Week'
    if dt >= m: return 'Last Month'
    if dt >= q: return 'Last Quarter'
    if dt >= y: return 'Last Year'
    return 'Older than 1 Year'

def build_hierarchy(df):
    """Build nested directory structure with URL counts."""
    rows = []
    max_d = int(df['url_depth'].max())
    for d1 in df['dir_1'].dropna().unique():
        sub1 = df[df['dir_1']==d1]
        count1 = len(sub1)
        if 'dir_2' not in df.columns or sub1['dir_2'].isna().all():
            rows.append({'path': f'/{d1}', 'level': 1, 'parent': '/', 'urls': count1})
            continue
        rows.append({'path': f'/{d1}', 'level': 1, 'parent': '/', 'urls': count1})
        for d2 in sub1['dir_2'].dropna().unique():
            sub2 = sub1[sub1['dir_2']==d2]
            count2 = len(sub2)
            p2 = f'/{d1}/{d2}'
            if 'dir_3' not in df.columns or sub2['dir_3'].isna().all():
                rows.append({'path': p2, 'level': 2, 'parent': f'/{d1}', 'urls': count2})
                continue
            rows.append({'path': p2, 'level': 2, 'parent': f'/{d1}', 'urls': count2})
            for d3 in sub2['dir_3'].dropna().unique():
                sub3 = sub2[sub2['dir_3']==d3]
                count3 = len(sub3)
                p3 = f'/{d1}/{d2}/{d3}'
                rows.append({'path': p3, 'level': 3, 'parent': p2, 'urls': count3})
                if 'dir_4' in df.columns:
                    for d4 in sub3['dir_4'].dropna().unique():
                        sub4 = sub3[sub3['dir_4']==d4]
                        rows.append({'path': f'{p3}/{d4}', 'level': 4, 'parent': p3, 'urls': len(sub4)})
    return pd.DataFrame(rows)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-eyebrow">✦ AI-Powered SEO Intelligence</div>
  <div class="hero-title">Sitemap<br><span>Copilot</span></div>
  <div class="hero-sub">See everything your competitor is hiding in plain sight</div>
  <div class="author-card">
    <img class="author-photo" src="{PHOTO_B64}" alt="Sankar Gurumurthy">
    <div>
      <div class="author-name">Sankar Gurumurthy</div>
      <div class="author-role">Head of AI SEO &amp; Marketing Data Scientist</div>
      <div class="author-links">
        <a href="https://www.linkedin.com/in/sankar-gurumurthy-a1044a136/" target="_blank">🔗 LinkedIn</a>
        <a href="https://github.com/sg-sankar" target="_blank">🐙 GitHub</a>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([5,1])
with c1:
    input_url = st.text_input("", placeholder="Paste robots.txt or sitemap.xml URL…", label_visibility="collapsed")
with c2:
    run = st.button("Analyse →")

if not run or not input_url.strip():
    st.markdown("<div style='text-align:center;padding:2.5rem;color:#2a2840;font-size:0.85rem'>Supports <b style='color:#3a3860'>robots.txt</b> · <b style='color:#3a3860'>sitemap.xml</b> · <b style='color:#3a3860'>sitemap index</b> · <b style='color:#3a3860'>nested &amp; gzipped sitemaps</b></div>", unsafe_allow_html=True)
    st.stop()

# ── Fetch ─────────────────────────────────────────────────────────────────────
with st.spinner("🛩️ Copilot is scanning the sitemap…"):
    smap_urls = extract_sitemaps_from_robots(input_url.strip()) if 'robots.txt' in input_url.lower() else [input_url.strip()]
    if not smap_urls: st.error("No sitemaps found."); st.stop()

    all_dfs, errors = [], []
    for su in smap_urls:
        try: all_dfs.append(adv.sitemap_to_df(su))
        except Exception as e: errors.append(str(e))

    if not all_dfs: st.error("Failed to fetch sitemaps.\n" + "\n".join(errors)); st.stop()

    df = pd.concat(all_dfs, ignore_index=True)
    if 'loc' not in df.columns: st.error("No URLs found."); st.stop()

    df = df.drop_duplicates('loc')
    df = df[df['loc'].notna() & df['loc'].str.startswith('http')].reset_index(drop=True)
    df['lastmod_dt'] = pd.to_datetime(df.get('lastmod', pd.Series(dtype=str)), errors='coerce', utc=True)
    df['url_parts'] = df['loc'].apply(lambda u: [p for p in urlparse(u).path.rstrip('/').split('/') if p])
    df['url_depth'] = df['url_parts'].apply(len)
    df['last_slug'] = df['url_parts'].apply(lambda x: x[-1] if x else '')
    df['domain']    = df['loc'].apply(lambda u: urlparse(u).netloc)
    df['url_length'] = df['loc'].apply(len)
    df['slug_words'] = df['last_slug'].apply(lambda s: len(re.findall(r'[a-zA-Z0-9]+', str(s))))

    max_depth = int(df['url_depth'].max()) if len(df) else 1
    for i in range(1, min(max_depth+1, 9)):
        df[f'dir_{i}'] = df['url_parts'].apply(lambda x, i=i: x[i-1] if len(x)>=i else None)

now=pd.Timestamp.now(tz='UTC')
lw=now-timedelta(days=7); lm=now-timedelta(days=30)
lq=now-timedelta(days=90); ly=now-timedelta(days=365)
n_total=len(df); n_dates=int(df['lastmod_dt'].notna().sum())
n_week=int((df['lastmod_dt']>=lw).sum()); n_month=int((df['lastmod_dt']>=lm).sum())
n_quarter=int((df['lastmod_dt']>=lq).sum()); n_year=int((df['lastmod_dt']>=ly).sum())
avg_depth=round(df['url_depth'].mean(),1); domain_name=df['domain'].iloc[0] if len(df) else 'Unknown'
df['freshness']=df['lastmod_dt'].apply(lambda d: freshness_label(d,lw,lm,lq,ly))

if n_dates > 0:
    df['days_since_update'] = (now - df['lastmod_dt']).dt.days
else:
    df['days_since_update'] = None

# ── Metrics ───────────────────────────────────────────────────────────────────
st.markdown(f'<div class="domain-badge">🌐 {domain_name}</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="bento-grid">
  <div class="bento-card"><div class="bento-num">{n_total:,}</div><div class="bento-label">Total URLs</div></div>
  <div class="bento-card"><div class="bento-num">{avg_depth}</div><div class="bento-label">Avg Depth</div></div>
  <div class="bento-card"><div class="bento-num">{max_depth}</div><div class="bento-label">Max Depth</div></div>
  <div class="bento-card"><div class="bento-num">{n_dates:,}</div><div class="bento-label">Have Dates</div></div>
  <div class="bento-card"><div class="bento-num">{n_week:,}</div><div class="bento-label">Last Week</div></div>
  <div class="bento-card"><div class="bento-num">{n_month:,}</div><div class="bento-label">Last Month</div></div>
  <div class="bento-card"><div class="bento-num">{n_quarter:,}</div><div class="bento-label">Last Quarter</div></div>
  <div class="bento-card"><div class="bento-num">{n_year:,}</div><div class="bento-label">Last Year</div></div>
</div>
""", unsafe_allow_html=True)

if errors:
    with st.expander(f"⚠️ {len(errors)} error(s)"): 
        for e in errors: st.text(e)

tabs = st.tabs(["🏗 URL Structure","🌳 Site Hierarchy","📝 N-Grams","📅 Temporal","🔬 Advanced EDA","📋 Raw Data","📥 Export"])

# ═══════════════════════════════════════════
# TAB 1 — URL STRUCTURE
# ═══════════════════════════════════════════
with tabs[0]:
  try:
    sec("URL Depth Distribution", "How many directory levels deep are the pages?")
    dc=df['url_depth'].value_counts().sort_index().reset_index()
    dc.columns=['Depth','URL Count']; dc['%']=(dc['URL Count']/n_total*100).round(1).astype(str)+'%'
    c1,c2=st.columns([3,2])
    with c1:
        fig=px.bar(dc,x='Depth',y='URL Count',text='URL Count',color='URL Count',color_continuous_scale=[[0,'#6333ff'],[1,'#00d296']],title='URLs by Depth Level')
        fig.update_traces(textposition='outside',marker_line_width=0)
        fig.update_layout(coloraxis_showscale=False,xaxis=dict(tickmode='linear'))
        T(fig); st.plotly_chart(fig,use_container_width=True)
    with c2: st.dataframe(dc,use_container_width=True,hide_index=True)

    # Directory levels — sorted descending in BOTH chart and table
    for level in range(1, min(max_depth+1,9)):
        cn=f'dir_{level}'
        if cn not in df.columns: break
        valid=df[cn].dropna()
        if len(valid)==0: break
        sec(f"Directory Level {level}", f"Top values at directory position {level}")
        vc=valid.value_counts().reset_index()
        vc.columns=['Directory','URL Count']
        vc['%']=(vc['URL Count']/n_total*100).round(2).astype(str)+'%'
        # Both sorted descending (largest first)
        vc=vc.sort_values('URL Count',ascending=False)
        c1,c2=st.columns([3,2])
        with c1:
            fig=px.bar(vc.head(25),x='URL Count',y='Directory',orientation='h',
                       title=f'Top Directories — Level {level}',color='URL Count',
                       color_continuous_scale=[[0,'#6333ff'],[1,'#00d296']])
            # Reversed so largest is at TOP matching table
            fig.update_layout(yaxis={'categoryorder':'total ascending'},coloraxis_showscale=False,
                             height=max(300,min(len(vc.head(25))*28,520)))
            T(fig); st.plotly_chart(fig,use_container_width=True)
        with c2: st.dataframe(vc,use_container_width=True,hide_index=True,height=max(300,min(len(vc)*35,520)))

    # URL Length
    sec("URL Length Analysis","Shorter, keyword-focused URLs perform better in search")
    c1,c2,c3=st.columns(3)
    with c1:
        ul=df['url_length']
        st.markdown("**Character Length Stats**")
        st.dataframe(pd.DataFrame({'Metric':['Min','Max','Mean','Median','Std'],'Value':[int(ul.min()),int(ul.max()),round(ul.mean(),1),round(ul.median(),1),round(ul.std(),1)]}),use_container_width=True,hide_index=True)
    with c2:
        sw=df['slug_words']
        st.markdown("**Slug Word Count Stats**")
        st.dataframe(pd.DataFrame({'Metric':['Min','Max','Mean','Median','Std'],'Value':[int(sw.min()),int(sw.max()),round(sw.mean(),1),round(sw.median(),1),round(sw.std(),1)]}),use_container_width=True,hide_index=True)
    with c3:
        bins=[0,30,50,70,100,9999]; lbls=['<30','30-50','50-70','70-100','>100']
        df['url_len_bucket']=pd.cut(df['url_length'],bins=bins,labels=lbls)
        bc=df['url_len_bucket'].value_counts().reindex(lbls,fill_value=0).reset_index()
        bc.columns=['Range','Count']; st.markdown("**Length Buckets**")
        st.dataframe(bc,use_container_width=True,hide_index=True)
    c1,c2=st.columns(2)
    with c1:
        fig=px.histogram(df,x='url_length',nbins=40,title='URL Character Length Distribution',color_discrete_sequence=['#00d296'])
        fig.update_layout(xaxis_title='Characters',yaxis_title='# URLs'); T(fig); st.plotly_chart(fig,use_container_width=True)
    with c2:
        fig=px.histogram(df,x='slug_words',nbins=20,title='Last Slug Word Count',color_discrete_sequence=['#6333ff'])
        fig.update_layout(xaxis_title='Words',yaxis_title='# URLs'); T(fig); st.plotly_chart(fig,use_container_width=True)

    # Site Structure Executive Summary
    sec("Site Structure Overview","Executive summary — one table showing the full architecture at a glance")
    if 'dir_1' in df.columns and df['dir_1'].notna().sum()>0:
        top_s=df['dir_1'].value_counts().reset_index()
        top_s.columns=['Section','Total URLs']
        top_s['% Share']=(top_s['Total URLs']/n_total*100).round(1).astype(str)+'%'
        top_s['Avg Depth']=top_s['Section'].apply(lambda s: round(df[df['dir_1']==s]['url_depth'].mean(),1))
        if n_dates>0:
            top_s['Avg Days Since Update']=top_s['Section'].apply(
                lambda s: int(df[(df['dir_1']==s) & df['days_since_update'].notna()]['days_since_update'].mean()) if df[(df['dir_1']==s) & df['days_since_update'].notna()].shape[0]>0 else None)
        fo=['Last Week','Last Month','Last Quarter','Last Year','Older than 1 Year','No Date']
        top_s['Dominant Freshness']=top_s['Section'].apply(
            lambda s: df[df['dir_1']==s]['freshness'].value_counts().index[0] if len(df[df['dir_1']==s])>0 else '—')
        if 'dir_2' in df.columns:
            top_s['Top Sub-sections']=top_s['Section'].apply(
                lambda s: ', '.join([f"{k}({v})" for k,v in df[df['dir_1']==s]['dir_2'].value_counts().head(4).items()]) or '—')
        st.dataframe(top_s,use_container_width=True,hide_index=True)
  except Exception as e: st.error(f"URL Structure error: {e}")

# ═══════════════════════════════════════════
# TAB 2 — SITE HIERARCHY
# ═══════════════════════════════════════════
with tabs[1]:
  try:
    sec("Site Hierarchy Drill-Down","Full parent→child→grandchild→slug breakdown with URL counts at every level")
    if 'dir_1' not in df.columns or df['dir_1'].notna().sum()==0:
        st.info("No directory structure found.")
    else:
        hier_df=build_hierarchy(df)
        if not hier_df.empty:
            # Filter by top-level section
            top_sections=df['dir_1'].value_counts().index.tolist()
            selected=st.selectbox("🔍 Select top-level section to drill down:",["All"] + top_sections)
            if selected != "All":
                show_df=hier_df[hier_df['path'].str.startswith(f'/{selected}')]
            else:
                show_df=hier_df.copy()

            show_df=show_df.sort_values(['level','urls'],ascending=[True,False])

            # Indent display
            def indent_path(row):
                indent="  " * (row['level']-1)
                arrow = ["","├─ ","  ├─ ","    ├─ "][min(row['level']-1,3)]
                return f"{indent}{arrow}{row['path'].split('/')[-1] or row['path']}"

            show_df['Directory/Slug']=show_df.apply(indent_path,axis=1)
            show_df['Level']=show_df['level'].apply(lambda x: ['●','  ○','    ◦','      ·'][min(x-1,3)])
            display=show_df[['Level','Directory/Slug','path','urls']].copy()
            display.columns=['Level','Directory/Slug','Full Path','URL Count']
            display['% of Total']=(display['URL Count']/n_total*100).round(2).astype(str)+'%'
            st.dataframe(display,use_container_width=True,hide_index=True,height=500)

            # Visual — sunburst of selected or top sections
            sec("Hierarchy Visualisation","Interactive sunburst — click to drill into any section")
            if selected != "All":
                sb_data=hier_df[hier_df['path'].str.startswith(f'/{selected}')].copy()
            else:
                # Top 10 sections only to keep readable
                top10=df['dir_1'].value_counts().head(10).index
                sb_data=hier_df[hier_df['path'].apply(lambda p: p.split('/')[1] if len(p.split('/'))>1 else '').isin(top10)]

            if not sb_data.empty and len(sb_data)>1:
                fig=px.sunburst(sb_data,names='path',parents='parent',values='urls',
                               title='Site Hierarchy — Click to Drill Down',
                               color='urls',color_continuous_scale=[[0,'#6333ff'],[1,'#00d296']])
                fig.update_traces(textinfo='label+value')
                fig.update_layout(coloraxis_showscale=False,height=550)
                T(fig); st.plotly_chart(fig,use_container_width=True)
  except Exception as e: st.error(f"Hierarchy error: {e}")

# ═══════════════════════════════════════════
# TAB 3 — N-GRAMS
# ═══════════════════════════════════════════
with tabs[2]:
  try:
    full_tok=df['loc'].apply(lambda u: tokenize(urlparse(u).path)).tolist()
    slug_tok=df['last_slug'].apply(tokenize).tolist()
    ng_full=build_ngrams(full_tok); ng_slug=build_ngrams(slug_tok)
    st3=st.tabs(["Full URL Path","Last Slug Only"])
    for tab_obj,ng_dict,lbl in [(st3[0],ng_full,'Full URL'),(st3[1],ng_slug,'Last Slug')]:
        with tab_obj:
            st.markdown(f'<div class="sec-sub">Most frequent words/phrases in {lbl}s — reveals competitor content strategy</div>',unsafe_allow_html=True)
            for ng_lbl,ng_df in ng_dict.items():
                if ng_df.empty: continue
                sec(ng_lbl)
                top=ng_df.head(20).copy().sort_values('count',ascending=False)
                top['%']=(top['count']/top['count'].sum()*100).round(1).astype(str)+'%'
                c1,c2=st.columns([3,2])
                with c1:
                    fig=px.bar(top,x='count',y='ngram',orientation='h',title=f'Top 20 {ng_lbl}',
                               color='count',color_continuous_scale=[[0,'#6333ff'],[1,'#00d296']])
                    # category order ascending so largest appears at TOP of horizontal bar
                    fig.update_layout(yaxis={'categoryorder':'total ascending'},coloraxis_showscale=False,
                                     height=max(300,min(len(top)*28,550)))
                    T(fig); st.plotly_chart(fig,use_container_width=True)
                with c2: st.dataframe(top,use_container_width=True,hide_index=True,height=max(300,min(len(top)*35,550)))
  except Exception as e: st.error(f"N-gram error: {e}")

# ═══════════════════════════════════════════
# TAB 4 — TEMPORAL
# ═══════════════════════════════════════════
with tabs[3]:
  try:
    if n_dates==0:
        st.info("No lastmod dates found.")
    else:
        dated=df[df['lastmod_dt'].notna()].copy()
        dated['year']=dated['lastmod_dt'].dt.year.astype(int)
        dated['month']=dated['lastmod_dt'].dt.to_period('M').astype(str)
        dated['quarter']=dated['lastmod_dt'].dt.to_period('Q').astype(str)
        dated['month_num']=dated['lastmod_dt'].dt.month

        sec("Publishing Velocity","Spikes = campaign activity. Flat lines = stale strategy = your opportunity.")
        monthly=dated.groupby('month').size().reset_index(name='URLs Updated').sort_values('month')
        fig=px.line(monthly,x='month',y='URLs Updated',title='Monthly Publishing Velocity',markers=True,color_discrete_sequence=['#00d296'])
        fig.update_traces(line_width=2.5,marker_size=5); T(fig); st.plotly_chart(fig,use_container_width=True)

        c1,c2=st.columns(2)
        with c1:
            sec("By Year")
            yearly=dated.groupby('year').size().reset_index(name='Count'); yearly['year']=yearly['year'].astype(str)
            fig=px.bar(yearly,x='year',y='Count',text='Count',color='Count',color_continuous_scale=[[0,'#6333ff'],[1,'#00d296']],title='URLs Updated Per Year')
            fig.update_traces(textposition='outside',marker_line_width=0); fig.update_layout(coloraxis_showscale=False)
            T(fig); st.plotly_chart(fig,use_container_width=True)
            st.dataframe(yearly.sort_values('Count',ascending=False),use_container_width=True,hide_index=True)
        with c2:
            sec("By Quarter (Last 12)")
            quarterly=dated.groupby('quarter').size().reset_index(name='Count'); quarterly=quarterly.sort_values('quarter').tail(12)
            fig=px.bar(quarterly,x='quarter',y='Count',text='Count',color='Count',color_continuous_scale=[[0,'#6333ff'],[1,'#00d296']],title='URLs Updated Per Quarter')
            fig.update_traces(textposition='outside',marker_line_width=0); fig.update_layout(coloraxis_showscale=False)
            T(fig); st.plotly_chart(fig,use_container_width=True)
            st.dataframe(quarterly.sort_values('Count',ascending=False),use_container_width=True,hide_index=True)

        # Freshness — sorted to match table
        sec("Content Freshness","Large 'Older than 1 Year' = competitor sleeping = your content gap opportunity")
        fo=['Last Week','Last Month','Last Quarter','Last Year','Older than 1 Year','No Date']
        fc=df['freshness'].value_counts().reindex(fo,fill_value=0).reset_index()
        fc.columns=['Freshness','Count']; fc['%']=(fc['Count']/n_total*100).round(1).astype(str)+'%'
        c1,c2=st.columns([3,2])
        with c1:
            fig=px.bar(fc,x='Freshness',y='Count',text='Count',title='Content Freshness Distribution',
                       color='Freshness',color_discrete_sequence=['#00d296','#06d6f5','#6333ff','#ffd166','#ff6b9d','#333'])
            fig.update_traces(textposition='outside',marker_line_width=0,showlegend=False)
            T(fig); st.plotly_chart(fig,use_container_width=True)
        with c2: st.dataframe(fc,use_container_width=True,hide_index=True)

        # Heatmap
        sec("Publishing Heatmap","Which month/year combos are most active? Reveals seasonal editorial calendars.")
        hm=dated.groupby(['year','month_num']).size().reset_index(name='count')
        hp=hm.pivot(index='year',columns='month_num',values='count').fillna(0)
        mn=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        hp.columns=[mn[int(c)-1] for c in hp.columns]; hp.index=hp.index.astype(str)
        fig=px.imshow(hp,color_continuous_scale=[[0,'#1a1040'],[0.5,'#6333ff'],[1,'#00d296']],
                     title='Publishing Activity Heatmap',aspect='auto',text_auto=True)
        T(fig); st.plotly_chart(fig,use_container_width=True)

        # Directory velocity
        if 'dir_1' in df.columns and df['dir_1'].notna().sum()>0:
            sec("Directory Publishing Velocity","Which sections are actively growing vs abandoned?")
            d2=dated[dated['dir_1'].notna()].copy()
            top8=d2['dir_1'].value_counts().head(8).index.tolist()
            d2=d2[d2['dir_1'].isin(top8)]
            dm=d2.groupby(['dir_1','month']).size().reset_index(name='Count').sort_values('month')
            fig=px.bar(dm,x='month',y='Count',color='dir_1',barmode='stack',title='Top 8 Dirs — Monthly Activity')
            T(fig,True); st.plotly_chart(fig,use_container_width=True)
            piv=dm.pivot_table(index='month',columns='dir_1',values='Count',fill_value=0).sort_index().tail(12)
            st.markdown("**Last 12 Months per Directory**"); st.dataframe(piv,use_container_width=True)
  except Exception as e: st.error(f"Temporal error: {e}")

# ═══════════════════════════════════════════
# TAB 5 — ADVANCED EDA
# ═══════════════════════════════════════════
with tabs[4]:
  try:
    # URL Depth vs Content Recency (FIXED — avg days since last update)
    sec("URL Depth vs Content Recency","Average days since last update per depth level — deeper = more neglected?")
    if n_dates>0 and 'days_since_update' in df.columns:
        dr=df[df['days_since_update'].notna()].groupby('url_depth')['days_since_update'].agg(['mean','median','count']).round(1).reset_index()
        dr.columns=['Depth','Avg Days Since Update','Median Days','URL Count']
        dr=dr.sort_values('Depth')
        c1,c2=st.columns([3,2])
        with c1:
            fig=px.bar(dr,x='Depth',y='Avg Days Since Update',text='Avg Days Since Update',
                      title='Avg Days Since Last Update by Depth',
                      color='Avg Days Since Update',color_continuous_scale=[[0,'#00d296'],[1,'#ff6b9d']])
            fig.update_traces(texttemplate='%{text:.0f}d',textposition='outside',marker_line_width=0)
            fig.update_layout(coloraxis_showscale=False,xaxis=dict(tickmode='linear'))
            T(fig); st.plotly_chart(fig,use_container_width=True)
        with c2:
            disp=dr.copy(); disp['Avg Days Since Update']=disp['Avg Days Since Update'].astype(str)+' days'
            disp['Median Days']=disp['Median Days'].astype(str)+' days'
            st.dataframe(disp,use_container_width=True,hide_index=True)

    # URL Length vs Depth
    sec("URL Length vs Depth","Unusually long shallow URLs = keyword stuffing risk")
    c1,c2=st.columns([3,2])
    with c1:
        fig=px.box(df,x='url_depth',y='url_length',title='URL Length Distribution by Depth',color_discrete_sequence=['#00d296'])
        fig.update_layout(xaxis=dict(tickmode='linear')); T(fig); st.plotly_chart(fig,use_container_width=True)
    with c2:
        dl=df.groupby('url_depth')['url_length'].agg(['mean','median','min','max','count']).round(1).reset_index()
        dl.columns=['Depth','Avg','Median','Min','Max','Count']
        st.dataframe(dl,use_container_width=True,hide_index=True)

    # Content Gap Opportunities (formerly Stale Content)
    if 'dir_1' in df.columns and df['dir_1'].notna().sum()>0 and n_dates>0:
        sec("Content Gap Opportunities","Sections where competitor is sleeping — high % not updated in 12+ months = attack these topics")
        one_year=now-timedelta(days=365)
        df['is_opportunity']=((df['lastmod_dt']<one_year)|df['lastmod_dt'].isna())
        sd=df[df['dir_1'].notna()].groupby('dir_1').agg(
            Total=('loc','count'),
            Opportunity=('is_opportunity','sum'),
            Avg_Days=('days_since_update','mean')).reset_index()
        sd['Opportunity %']=(sd['Opportunity']/sd['Total']*100).round(1)
        sd['Avg Days Since Update']=sd['Avg_Days'].round(0).fillna(0).astype(int)
        # Opportunity score = % old * log(total urls) — bigger section + more stale = bigger opportunity
        import math
        sd['Opportunity Score']=((sd['Opportunity %']/100) * sd['Total'].apply(lambda x: math.log(x+1)*10)).round(1)
        sd=sd[['dir_1','Total','Opportunity','Opportunity %','Avg Days Since Update','Opportunity Score']]
        sd.columns=['Directory','Total URLs','Stale URLs','Stale %','Avg Days Since Update','Opportunity Score']
        sd=sd.sort_values('Opportunity Score',ascending=False).head(20)
        c1,c2=st.columns([3,2])
        with c1:
            fig=px.bar(sd,x='Opportunity Score',y='Directory',orientation='h',
                      title='Content Gap Opportunity Score by Section',
                      color='Opportunity Score',color_continuous_scale=[[0,'#6333ff'],[1,'#00d296']],
                      text='Opportunity Score',hover_data=['Total URLs','Stale %','Avg Days Since Update'])
            fig.update_traces(textposition='outside')
            fig.update_layout(yaxis={'categoryorder':'total ascending'},coloraxis_showscale=False,height=500)
            T(fig); st.plotly_chart(fig,use_container_width=True)
        with c2:
            disp=sd.copy(); disp['Stale %']=disp['Stale %'].astype(str)+'%'
            st.dataframe(disp,use_container_width=True,hide_index=True)

    # Directory × Freshness
    if 'dir_1' in df.columns and df['dir_1'].notna().sum()>0:
        sec("Directory × Freshness","Full freshness breakdown per section — see who's growing, stable, or stagnating")
        top10=df['dir_1'].value_counts().head(10).index
        mv=df[df['dir_1'].isin(top10)].groupby(['dir_1','freshness']).size().reset_index(name='Count')
        fo2=['Last Week','Last Month','Last Quarter','Last Year','Older than 1 Year','No Date']
        mv['freshness']=pd.Categorical(mv['freshness'],categories=fo2,ordered=True)
        mv=mv.sort_values(['dir_1','freshness'])
        fig=px.bar(mv,x='dir_1',y='Count',color='freshness',barmode='stack',
                  title='Top 10 Sections — Freshness Breakdown',
                  color_discrete_map={'Last Week':'#00d296','Last Month':'#06d6f5','Last Quarter':'#6333ff',
                                      'Last Year':'#ffd166','Older than 1 Year':'#ff6b9d','No Date':'#222'})
        fig.update_layout(xaxis_title='Section',height=420); T(fig,True); st.plotly_chart(fig,use_container_width=True)
        pv=mv.pivot_table(index='dir_1',columns='freshness',values='Count',fill_value=0)
        st.markdown("**Directory × Freshness Table**"); st.dataframe(pv,use_container_width=True)

    # Priority
    if 'priority' in df.columns and df['priority'].notna().sum()>0:
        sec("Priority Distribution")
        df['priority_num']=pd.to_numeric(df['priority'],errors='coerce')
        c1,c2=st.columns(2)
        with c1:
            fig=px.histogram(df,x='priority_num',nbins=20,title='Priority Distribution',color_discrete_sequence=['#00d296'])
            T(fig); st.plotly_chart(fig,use_container_width=True)
        with c2:
            p=df['priority_num']
            st.dataframe(pd.DataFrame({'Metric':['Min','Max','Mean','Median'],'Value':[p.min(),p.max(),round(p.mean(),2),round(p.median(),2)]}),use_container_width=True,hide_index=True)
  except Exception as e: st.error(f"Advanced EDA error: {e}")

# ═══════════════════════════════════════════
# TAB 6 — RAW DATA
# ═══════════════════════════════════════════
with tabs[5]:
  try:
    sec("Raw Sitemap Data","Search and filter all URLs")
    display_cols=[c for c in ['loc','lastmod','changefreq','priority','url_depth','freshness','url_length'] if c in df.columns]
    
    # Filters
    fc1,fc2,fc3,fc4=st.columns(4)
    with fc1:
        search=st.text_input("🔍 Search URL",placeholder="e.g. blog, product…",key="search_raw")
    with fc2:
        fresh_opts=['All']+['Last Week','Last Month','Last Quarter','Last Year','Older than 1 Year','No Date']
        fresh_filter=st.selectbox("📅 Freshness",fresh_opts,key="fresh_filter")
    with fc3:
        if 'dir_1' in df.columns:
            dir_opts=['All']+df['dir_1'].dropna().value_counts().index.tolist()
            dir_filter=st.selectbox("📁 Section (Dir 1)",dir_opts,key="dir_filter")
        else: dir_filter='All'
    with fc4:
        depth_opts=['All']+sorted(df['url_depth'].unique().tolist())
        depth_filter=st.selectbox("📊 Depth",depth_opts,key="depth_filter")

    filtered=df[display_cols+['freshness','dir_1','url_depth']].copy() if 'dir_1' in df.columns else df[display_cols+['freshness','url_depth']].copy()
    if search: filtered=filtered[filtered['loc'].str.contains(search,case=False,na=False)]
    if fresh_filter!='All': filtered=filtered[filtered['freshness']==fresh_filter]
    if dir_filter!='All' and 'dir_1' in filtered.columns: filtered=filtered[filtered['dir_1']==dir_filter]
    if depth_filter!='All': filtered=filtered[filtered['url_depth']==depth_filter]

    st.markdown(f"<div style='color:#6b6a80;font-size:0.82rem;margin-bottom:0.5rem'>Showing <b style='color:#00d296'>{len(filtered):,}</b> of <b>{n_total:,}</b> URLs</div>",unsafe_allow_html=True)
    st.dataframe(filtered[display_cols],use_container_width=True,height=480)
    st.download_button("⬇ Download Filtered CSV",filtered[display_cols].to_csv(index=False).encode(),f"sitemap_{domain_name.replace('.','_')}.csv","text/csv")

    sec("Summary Statistics")
    summary=pd.DataFrame({'Metric':['Total URLs','Unique Domains','Avg URL Depth','Max URL Depth','Avg URL Length','URLs with Dates','Updated Last Week','Updated Last Month','Updated Last Quarter','Updated Last Year'],
                           'Value':[f"{n_total:,}",df['domain'].nunique(),avg_depth,max_depth,round(df['url_length'].mean(),1),f"{n_dates:,}",f"{n_week:,}",f"{n_month:,}",f"{n_quarter:,}",f"{n_year:,}"]})
    st.dataframe(summary,use_container_width=True,hide_index=True)
  except Exception as e: st.error(f"Raw data error: {e}")

# ═══════════════════════════════════════════
# TAB 7 — EXPORT
# ═══════════════════════════════════════════
with tabs[6]:
  try:
    sec("Export Report","Download as HTML → open in Chrome → Cmd+P → Save as PDF")
    
    def make_html():
        now_str=datetime.now().strftime('%Y-%m-%d %H:%M')
        # Overview metrics
        metrics_rows=''
        for k,v in [('Total URLs',f"{n_total:,}"),('Avg Depth',avg_depth),('Max Depth',max_depth),
                    ('URLs with Dates',f"{n_dates:,}"),('Updated Last Week',f"{n_week:,}"),
                    ('Updated Last Month',f"{n_month:,}"),('Updated Last Quarter',f"{n_quarter:,}"),
                    ('Updated Last Year',f"{n_year:,}")]:
            metrics_rows+=f"<tr><td>{k}</td><td><strong>{v}</strong></td></tr>"
        
        # Dir tables
        dir_html=""
        for level in range(1, min(max_depth+1,9)):
            cn=f'dir_{level}'
            if cn not in df.columns: break
            valid=df[cn].dropna()
            if len(valid)==0: break
            vc=valid.value_counts().reset_index(); vc.columns=['Directory','URL Count']
            vc['%']=(vc['URL Count']/n_total*100).round(2).astype(str)+'%'
            dir_html+=f"<h3>Level {level}</h3>"+vc.head(20).to_html(index=False,classes='dt')

        # Ngrams
        ng_html=""
        all_tok=df['loc'].apply(lambda u: tokenize(urlparse(u).path)).tolist()
        for lbl,ngdf in build_ngrams(all_tok).items():
            if ngdf.empty: continue
            ng_html+=f"<h3>{lbl}</h3>"+ngdf.head(20).to_html(index=False,classes='dt')

        # Freshness
        fo=['Last Week','Last Month','Last Quarter','Last Year','Older than 1 Year','No Date']
        fc2=df['freshness'].value_counts().reindex(fo,fill_value=0).reset_index()
        fc2.columns=['Bucket','Count']; fc2['%']=(fc2['Count']/n_total*100).round(1).astype(str)+'%'

        return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<title>Sitemap Copilot Report — {domain_name}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Cabinet+Grotesk:wght@700;800;900&family=Inter:wght@300;400;500&display=swap');
body{{font-family:'Inter',sans-serif;background:#080810;color:#e2e0f0;max-width:1100px;margin:0 auto;padding:2rem 1.5rem}}
.author-block{{display:flex;align-items:center;gap:1rem;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:1rem 1.4rem;margin-bottom:1.5rem}}
.author-block img{{width:54px;height:54px;border-radius:12px;object-fit:cover;border:1px solid rgba(0,210,150,0.3)}}
.author-name{{font-family:'Cabinet Grotesk',sans-serif;font-weight:800;font-size:1rem;color:#fff}}
.author-role{{color:#00d296;font-size:0.78rem;margin:0.1rem 0 0.3rem}}
.author-links a{{color:#6b6a80;font-size:0.75rem;margin-right:0.7rem;text-decoration:none}}
h1{{font-family:'Cabinet Grotesk',sans-serif;font-size:2.5rem;font-weight:900;color:#fff;letter-spacing:-0.03em;margin-bottom:0.2rem}}
h1 span{{background:linear-gradient(135deg,#00d296,#6333ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
h2{{font-family:'Cabinet Grotesk',sans-serif;font-size:1.2rem;color:#00d296;border-left:3px solid #00d296;padding-left:0.7rem;margin-top:2.5rem;font-weight:800}}
h3{{font-family:'Cabinet Grotesk',sans-serif;font-size:0.95rem;color:#6333ff;margin-top:1.3rem;font-weight:700}}
.meta{{color:#4a4860;font-size:0.82rem;margin-bottom:1.8rem}}
table.dt{{width:100%;border-collapse:collapse;margin:0.6rem 0;font-size:0.84rem}}
table.dt th{{background:rgba(0,210,150,0.08);color:#00d296;padding:0.5rem 0.7rem;text-align:left;font-family:'Cabinet Grotesk',sans-serif;font-size:0.78rem;letter-spacing:0.06em;text-transform:uppercase}}
table.dt td{{padding:0.4rem 0.7rem;border-bottom:1px solid rgba(255,255,255,0.04)}}
table.dt tr:nth-child(even) td{{background:rgba(255,255,255,0.02)}}
.footer{{margin-top:3rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,0.05);color:#2a2840;font-size:0.76rem;text-align:center}}
.footer a{{color:#3a3860;text-decoration:none}}
@media print{{body{{background:#fff;color:#111}}h1 span{{-webkit-text-fill-color:#6333ff}}h2{{color:#00b880;border-color:#00b880}}h3{{color:#6333ff}}.author-block{{background:#f5f5f5;border:1px solid #ddd}}table.dt th{{background:#080810;color:#fff}}}}
</style></head><body>
<div class="author-block">
  <img src="{PHOTO_B64}" alt="Sankar">
  <div><div class="author-name">Sankar Gurumurthy</div>
  <div class="author-role">Head of AI SEO &amp; Marketing Data Scientist</div>
  <div class="author-links">
    <a href="https://www.linkedin.com/in/sankar-gurumurthy-a1044a136/">🔗 LinkedIn</a>
    <a href="https://github.com/sg-sankar">🐙 github.com/sg-sankar</a>
  </div></div>
</div>
<h1>Sitemap <span>Copilot</span></h1>
<p class="meta">Domain: <strong style="color:#a0ffd8">{domain_name}</strong> &nbsp;·&nbsp; Generated: {now_str} &nbsp;·&nbsp; See everything your competitor is hiding in plain sight</p>
<h2>Overview Metrics</h2>
<table class="dt"><tr><th>Metric</th><th>Value</th></tr>{metrics_rows}</table>
<h2>URL Depth Distribution</h2>
{df['url_depth'].value_counts().sort_index().reset_index().rename(columns={{'url_depth':'Depth','count':'URL Count'}}).to_html(index=False,classes='dt')}
<h2>Directory Level Analysis</h2>{dir_html}
<h2>N-Gram Analysis (Full URL Path)</h2>{ng_html}
<h2>Content Freshness</h2>{fc2.to_html(index=False,classes='dt')}
<div class="footer">Built by <a href="https://www.linkedin.com/in/sankar-gurumurthy-a1044a136/">Sankar Gurumurthy</a> · <a href="https://github.com/sg-sankar">github.com/sg-sankar</a> · Sitemap Copilot · Free &amp; Open Source</div>
</body></html>"""

    html_out=make_html()
    st.download_button("⬇ Download HTML Report",html_out.encode('utf-8'),f"sitemap_copilot_{domain_name.replace('.','_')}.html","text/html")
    st.markdown("<div style='color:#4a4860;font-size:0.82rem;margin-top:0.4rem'>💡 Open in Chrome → Cmd+P → Save as PDF</div>",unsafe_allow_html=True)
    st.markdown("---")
    display_cols2=[c for c in ['loc','lastmod','changefreq','priority','url_depth','freshness','url_length'] if c in df.columns]
    st.download_button("⬇ Download CSV",df[display_cols2].to_csv(index=False).encode(),f"sitemap_{domain_name.replace('.','_')}.csv","text/csv")
  except Exception as e: st.error(f"Export error: {e}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  Sitemap Copilot · Built by <a href="https://www.linkedin.com/in/sankar-gurumurthy-a1044a136/" target="_blank">Sankar Gurumurthy</a>
  &nbsp;·&nbsp; Head of AI SEO &amp; Marketing Data Scientist
  &nbsp;·&nbsp; <a href="https://github.com/sg-sankar" target="_blank">github.com/sg-sankar</a>
  <br><span style="color:#1a1830;margin-top:0.2rem;display:block">Open source · Free forever · Powered by advertools + Streamlit</span>
</div>
""", unsafe_allow_html=True)
