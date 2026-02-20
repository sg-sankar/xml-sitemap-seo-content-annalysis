import streamlit as st
import pandas as pd
import plotly.express as px
import advertools as adv
import requests, re, time
from urllib.parse import urlparse
from collections import Counter
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

PHOTO_B64 = "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"

st.set_page_config(
    page_title="Sitemap Copilot",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #ffffff !important;
    color: #111827 !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
}
[data-testid="stHeader"] { background: transparent !important; display: none; }
[data-testid="stSidebar"] { display: none; }
section[data-testid="stMain"] { padding: 0 !important; }
.block-container { padding: 0 2rem 4rem !important; max-width: 1280px !important; margin: 0 auto !important; }

/* Top nav bar */
.topbar {
    background: #fff;
    border-bottom: 1px solid #e5e7eb;
    padding: 0.75rem 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
    margin: 0 -2rem 2rem;
}
.topbar-logo {
    font-size: 1rem;
    font-weight: 700;
    color: #111827;
    letter-spacing: -0.02em;
}
.topbar-logo span { color: #2563eb; }
.topbar-author {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.8rem;
    color: #6b7280;
}
.topbar-author img {
    width: 28px; height: 28px;
    border-radius: 50%;
    object-fit: cover;
    border: 1px solid #e5e7eb;
}
.topbar-author a { color: #2563eb; text-decoration: none; font-weight: 500; }

/* Metric cards */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: #e5e7eb;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 2rem;
}
.metric-card {
    background: #fff;
    padding: 1.25rem 1.5rem;
}
.metric-val {
    font-size: 1.75rem;
    font-weight: 700;
    color: #111827;
    letter-spacing: -0.03em;
    line-height: 1;
}
.metric-val.big { font-size: 2.5rem; color: #2563eb; }
.metric-lbl {
    font-size: 0.72rem;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 0.3rem;
    font-weight: 500;
}
.metric-sub { font-size: 0.75rem; color: #d1d5db; margin-top: 0.2rem; }

/* Section headers */
.sec-hdr {
    font-size: 0.8rem;
    font-weight: 600;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 2rem 0 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #f3f4f6;
}
.insight {
    background: #eff6ff;
    border-left: 3px solid #2563eb;
    padding: 0.75rem 1rem;
    border-radius: 0 8px 8px 0;
    font-size: 0.82rem;
    color: #1e40af;
    margin: 0.5rem 0 1rem;
    line-height: 1.5;
}
.warn {
    background: #fff7ed;
    border-left: 3px solid #f59e0b;
    padding: 0.75rem 1rem;
    border-radius: 0 8px 8px 0;
    font-size: 0.82rem;
    color: #92400e;
    margin: 0.5rem 0 1rem;
    line-height: 1.5;
}

/* Input */
.stTextInput > div > div > input {
    background: #f9fafb !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 8px !important;
    color: #111827 !important;
    font-size: 0.9rem !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.65rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
    background: #fff !important;
}

/* Button */
.stButton > button {
    background: #2563eb !important;
    color: #fff !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.5rem !important;
    width: 100% !important;
    transition: background 0.15s !important;
}
.stButton > button:hover { background: #1d4ed8 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #e5e7eb !important;
    gap: 0 !important;
    padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    color: #6b7280 !important;
    border-radius: 0 !important;
    padding: 0.6rem 1rem !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #2563eb !important;
    border-bottom: 2px solid #2563eb !important;
    background: transparent !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: #f9fafb !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
}

/* Download button */
.stDownloadButton > button {
    background: #fff !important;
    color: #2563eb !important;
    border: 1px solid #2563eb !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
}

/* Expander */
.streamlit-expanderHeader {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    color: #111827 !important;
    background: #f9fafb !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 8px !important;
}
.streamlit-expanderContent {
    border: 1px solid #e5e7eb !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    background: #fff !important;
}

/* Dataframe */
[data-testid="stDataFrame"] { border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden; }

/* Progress */
.stProgress > div > div { background: #2563eb !important; }

/* Number input */
.stNumberInput > div > div > input {
    background: #f9fafb !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
}

/* Slider */
.stSlider > div > div > div > div { background: #2563eb !important; }

footer { display: none !important; }

/* Fix expander to light theme */
.streamlit-expanderHeader {
    background: #f9fafb !important;
    color: #111827 !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 8px !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
}
.streamlit-expanderHeader:hover {
    background: #f3f4f6 !important;
}
.streamlit-expanderContent {
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
}
[data-testid="stExpander"] {
    border: none !important;
    background: transparent !important;
}
[data-testid="stExpander"] summary {
    background: #f9fafb !important;
    color: #111827 !important;
}

/* Fix dataframe/table text to be dark on light */
[data-testid="stDataFrame"] * {
    color: #111827 !important;
}
.stDataFrame th {
    background: #f9fafb !important;
    color: #374151 !important;
}

/* Fix selectbox dropdown text */
[data-baseweb="select"] * { color: #111827 !important; }
[data-baseweb="popover"] * { color: #111827 !important; background: #fff !important; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ──────────────────────────────────────────────────────────────
PCFG = dict(
    paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
    font_color="#374151", font_family="Inter",
    title_font_family="Inter", title_font_size=13,
    title_font_color="#111827",
    colorway=["#2563eb","#10b981","#f59e0b","#ef4444","#8b5cf6","#06b6d4"],
)

def ap(fig, legend=False):
    fig.update_layout(**PCFG, showlegend=legend, margin=dict(t=40,b=20,l=10,r=10))
    fig.update_xaxes(gridcolor="#f3f4f6", linecolor="#e5e7eb", zeroline=False)
    fig.update_yaxes(gridcolor="#f3f4f6", linecolor="#e5e7eb", zeroline=False)
    return fig

def sh(text, sub=None, insight=None, warn=None):
    st.markdown(f'<div class="sec-hdr">{text}</div>', unsafe_allow_html=True)
    if sub: st.caption(sub)
    if insight: st.markdown(f'<div class="insight">💡 {insight}</div>', unsafe_allow_html=True)
    if warn: st.markdown(f'<div class="warn">⚠️ {warn}</div>', unsafe_allow_html=True)

def tokenize(slug):
    s = re.sub(r"[-_]", " ", str(slug).lower())
    s = re.sub(r"[^a-z0-9 ]", "", s)
    return [t for t in s.split() if len(t) > 1]

def build_ngrams(token_lists, max_n=5):
    labels = {1:"Unigrams", 2:"Bigrams", 3:"Trigrams", 4:"4-grams", 5:"5-grams"}
    out = {}
    for n in range(1, max_n+1):
        grams = []
        for toks in token_lists:
            grams.extend([" ".join(toks[i:i+n]) for i in range(len(toks)-n+1)])
        out[labels[n]] = pd.DataFrame(Counter(grams).most_common(30), columns=["ngram","count"])
    return out

def clean_df(d):
    return d.loc[:, ~d.columns.duplicated()].copy()

def display_cols(d):
    want = ["loc","lastmod","changefreq","priority","url_depth","freshness","url_length"]
    dc = clean_df(d)
    return [c for c in want if c in dc.columns]

# ── Top nav ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="topbar">
  <div class="topbar-logo">Sitemap<span>Copilot</span></div>
  <div class="topbar-author">
    <img src="data:image/png;base64,{PHOTO_B64}" alt="Sankar">
    <span>Built by <a href="https://www.linkedin.com/in/sankar-gurumurthy-a1044a136/" target="_blank">Sankar Gurumurthy</a>
    &nbsp;·&nbsp; <a href="https://github.com/sg-sankar" target="_blank">GitHub</a></span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── URL Input ─────────────────────────────────────────────────────────────
c1, c2 = st.columns([5, 1])
with c1:
    input_url = st.text_input("", placeholder="Paste robots.txt or sitemap.xml URL…", label_visibility="collapsed", key="input_url")
with c2:
    run = st.button("Analyse →")

if not run and "df" not in st.session_state:
    st.markdown("""
    <div style="text-align:center;padding:5rem 1rem;color:#9ca3af">
      <div style="font-size:2rem;margin-bottom:1rem">🛸</div>
      <div style="font-size:1rem;font-weight:600;color:#374151;margin-bottom:0.5rem">Analyse any competitor sitemap instantly</div>
      <div style="font-size:0.85rem">Supports robots.txt · sitemap.xml · sitemap index · nested & gzipped sitemaps</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Fetch & cache in session_state ────────────────────────────────────────
def extract_robots(url):
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent":"SitemapCopilot/1.0"})
        r.raise_for_status()
        return [s.strip() for s in re.findall(r"(?i)^Sitemap:\s*(.+)", r.text, re.MULTILINE)]
    except: return []

def fetch_one(url):
    for attempt in range(3):
        try:
            return adv.sitemap_to_df(url), None
        except Exception as e:
            if "429" in str(e) and attempt < 2:
                time.sleep(3 + attempt * 2)
            else:
                return None, str(e)
    return None, "Max retries"

if run and input_url.strip():
    sitemap_urls = extract_robots(input_url.strip()) if "robots.txt" in input_url.lower() else [input_url.strip()]
    if not sitemap_urls:
        st.error("No sitemaps found."); st.stop()

    pb = st.progress(0, text="Scanning…")
    all_dfs, errs = [], []
    total = len(sitemap_urls)
    for idx, su in enumerate(sitemap_urls):
        pb.progress(max(1, int(idx/total*100)), text=f"Fetching {idx+1} of {total}…")
        dfp, err = fetch_one(su)
        if dfp is not None: all_dfs.append(dfp)
        else: errs.append(f"{su}: {err}")
        if idx < total-1: time.sleep(0.8)
    pb.progress(100, text="Done!"); time.sleep(0.3); pb.empty()

    if not all_dfs: st.error("Failed.\n"+"\n".join(errs)); st.stop()

    df = pd.concat(all_dfs, ignore_index=True)
    df = clean_df(df)
    if "loc" not in df.columns: st.error("No URLs found."); st.stop()
    df = df.drop_duplicates("loc")
    df = df[df["loc"].notna() & df["loc"].str.startswith("http")].reset_index(drop=True)
    df["lastmod_dt"] = pd.to_datetime(df.get("lastmod", pd.Series(dtype=str)), errors="coerce", utc=True)
    df["url_parts"]  = df["loc"].apply(lambda u: [p for p in urlparse(u).path.rstrip("/").split("/") if p])
    df["url_depth"]  = df["url_parts"].apply(len)
    df["last_slug"]  = df["url_parts"].apply(lambda x: x[-1] if x else "")
    df["domain"]     = df["loc"].apply(lambda u: urlparse(u).netloc)
    df["url_length"] = df["loc"].apply(len)
    df["slug_words"] = df["last_slug"].apply(lambda s: len(re.findall(r"[a-zA-Z0-9]+", str(s))))
    md = int(df["url_depth"].max()) if len(df) else 1
    for i in range(1, min(md+1, 9)):
        df[f"dir_{i}"] = df["url_parts"].apply(lambda x, i=i: x[i-1] if len(x) >= i else None)

    now = pd.Timestamp.now(tz="UTC")
    def fb(dt):
        if pd.isna(dt): return "No Date"
        lw=now-timedelta(days=7); lm=now-timedelta(days=30)
        lq=now-timedelta(days=90); ly=now-timedelta(days=365)
        if dt>=lw: return "Last Week"
        if dt>=lm: return "Last Month"
        if dt>=lq: return "Last Quarter"
        if dt>=ly: return "Last Year"
        return "Older than 1 Year"
    df["freshness"] = df["lastmod_dt"].apply(fb)

    st.session_state["df"] = df
    st.session_state["errs"] = errs

if "df" not in st.session_state: st.stop()

df = st.session_state["df"]
errs = st.session_state.get("errs", [])

now = pd.Timestamp.now(tz="UTC")
lw=now-timedelta(days=7); lm=now-timedelta(days=30)
lq=now-timedelta(days=90); ly=now-timedelta(days=365)
n_total = len(df)
n_dates = int(df["lastmod_dt"].notna().sum())
n_week  = int((df["lastmod_dt"]>=lw).sum())
n_month = int((df["lastmod_dt"]>=lm).sum())
n_quarter = int((df["lastmod_dt"]>=lq).sum())
n_year  = int((df["lastmod_dt"]>=ly).sum())
avg_depth = round(df["url_depth"].mean(), 1)
max_depth = int(df["url_depth"].max())
domain_name = df["domain"].iloc[0] if len(df) else "Unknown"

# ── Metrics ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="metrics-row">
  <div class="metric-card" style="grid-column:span 2">
    <div class="metric-val big">{n_total:,}</div>
    <div class="metric-lbl">Total URLs · {domain_name}</div>
    <div class="metric-sub">Avg depth {avg_depth} · Max depth {max_depth}</div>
  </div>
  <div class="metric-card"><div class="metric-val">{n_dates:,}</div><div class="metric-lbl">Have Dates</div></div>
  <div class="metric-card"><div class="metric-val">{n_week:,}</div><div class="metric-lbl">Last Week</div></div>
  <div class="metric-card"><div class="metric-val">{n_month:,}</div><div class="metric-lbl">Last Month</div></div>
  <div class="metric-card"><div class="metric-val">{n_quarter:,}</div><div class="metric-lbl">Last Quarter</div></div>
  <div class="metric-card"><div class="metric-val">{n_year:,}</div><div class="metric-lbl">Last Year</div></div>
  <div class="metric-card"><div class="metric-val">{round(df["url_length"].mean(),0):.0f}</div><div class="metric-lbl">Avg URL Length</div></div>
</div>
""", unsafe_allow_html=True)

if errs:
    with st.expander(f"⚠️ {len(errs)} sitemap(s) failed"):
        for e in errs: st.text(e)

tabs = st.tabs(["URL Structure", "Site Hierarchy", "N-Grams", "Temporal", "Advanced EDA", "Raw Data", "Export"])

# ═══════════════════════════════════════
# TAB 1 — URL STRUCTURE
# ═══════════════════════════════════════
with tabs[0]:
    try:
        sh("Depth Distribution")
        dc = df["url_depth"].value_counts().sort_index().reset_index()
        dc.columns = ["Depth","URL Count"]
        dc["% of Total"] = (dc["URL Count"]/n_total*100).round(2).astype(str)+"%"
        dc["Cumulative %"] = (dc["URL Count"].cumsum()/n_total*100).round(1).astype(str)+"%"
        c1,c2 = st.columns([2,3])
        with c1: st.dataframe(dc, use_container_width=True, hide_index=True)
        with c2:
            fig = px.bar(dc, x="Depth", y="URL Count", text="URL Count",
                         color="URL Count", color_continuous_scale="Blues", title="URLs by Depth")
            fig.update_traces(textposition="outside", marker_line_width=0)
            fig.update_layout(coloraxis_showscale=False, xaxis=dict(tickmode="linear"))
            ap(fig); st.plotly_chart(fig, use_container_width=True)

        sh("URL Length Analysis")
        ul=df["url_length"]; sw=df["slug_words"]
        c1,c2,c3 = st.columns(3)
        with c1:
            st.markdown("**Character Length**")
            st.dataframe(pd.DataFrame({"Stat":["Min","Max","Mean","Median","Std"],
                "Value":[int(ul.min()),int(ul.max()),round(ul.mean(),1),round(ul.median(),1),round(ul.std(),1)]}),
                use_container_width=True, hide_index=True)
        with c2:
            st.markdown("**Slug Word Count**")
            st.dataframe(pd.DataFrame({"Stat":["Min","Max","Mean","Median","Std"],
                "Value":[int(sw.min()),int(sw.max()),round(sw.mean(),1),round(sw.median(),1),round(sw.std(),1)]}),
                use_container_width=True, hide_index=True)
        with c3:
            st.markdown("**Length Buckets**")
            bins=[0,30,50,70,100,9999]; lb=["<30","30-50","50-70","70-100",">100"]
            df["ul_b"] = pd.cut(df["url_length"], bins=bins, labels=lb)
            bc = df["ul_b"].value_counts().reindex(lb,fill_value=0).reset_index()
            bc.columns=["Range","Count"]; bc["%"]=(bc["Count"]/n_total*100).round(1).astype(str)+"%"
            st.dataframe(bc, use_container_width=True, hide_index=True)
        c1,c2 = st.columns(2)
        with c1:
            fig=px.histogram(df,x="url_length",nbins=40,title="URL Length Distribution",color_discrete_sequence=["#2563eb"])
            fig.update_layout(xaxis_title="Chars",yaxis_title="Count"); ap(fig); st.plotly_chart(fig,use_container_width=True)
        with c2:
            fig=px.histogram(df,x="slug_words",nbins=20,title="Slug Word Count",color_discrete_sequence=["#10b981"])
            fig.update_layout(xaxis_title="Words",yaxis_title="Count"); ap(fig); st.plotly_chart(fig,use_container_width=True)

        sh("Site Structure Summary", insight="Each section's total URLs, freshness, depth and top sub-sections at a glance.")
        if "dir_1" in df.columns and df["dir_1"].notna().sum()>0:
            ss = df["dir_1"].value_counts().reset_index()
            ss.columns=["Section","URLs"]
            ss["% Share"]=(ss["URLs"]/n_total*100).round(2).astype(str)+"%"
            ad = df[df["dir_1"].notna()].groupby("dir_1")["url_depth"].mean().round(1).reset_index()
            ad.columns=["Section","Avg Depth"]
            ss = ss.merge(ad,on="Section",how="left")
            ss["Top Freshness"] = ss["Section"].apply(lambda d1: df[df["dir_1"]==d1]["freshness"].value_counts().index[0] if len(df[df["dir_1"]==d1])>0 else "—")
            if "dir_2" in df.columns:
                def get_top_sub(d1):
                    subs = df[df["dir_1"]==d1]["dir_2"].dropna().value_counts().head(3)
                    return ", ".join([f"{k}({v})" for k,v in subs.items()]) if len(subs)>0 else "—"
                ss["Top Sub-sections"] = ss["Section"].apply(get_top_sub)
            st.dataframe(ss, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"URL Structure error: {e}")

# ═══════════════════════════════════════
# TAB 2 — SITE HIERARCHY (proper nested expanders)
# ═══════════════════════════════════════
with tabs[1]:
    try:
        sh("Site Hierarchy",
           insight="Wide shallow trees = topic authority play. Deep narrow trees = long-tail strategy. Click ▶ to expand any section.")

        @st.cache_data(show_spinner=False)
        def build_tree(parts_tuple):
            tree = {"__count__": len(parts_tuple), "__urls__": []}
            for parts in parts_tuple:
                node = tree
                for part in parts:
                    if part not in node:
                        node[part] = {"__count__": 0, "__urls__": []}
                    node[part]["__count__"] += 1
                    node = node[part]
            return tree

        @st.cache_data(show_spinner=False)
        def attach_urls(parts_tuple, locs_tuple):
            """Attach actual URLs to leaf nodes."""
            tree = build_tree(parts_tuple)
            for parts, loc in zip(parts_tuple, locs_tuple):
                node = tree
                for part in parts:
                    node = node[part]
                node["__urls__"].append(loc)
            return tree

        def get_children(node, min_c=1):
            ch = [(k,v) for k,v in node.items()
                  if k not in ("__count__","__urls__") and isinstance(v,dict) and v.get("__count__",0)>=min_c]
            return sorted(ch, key=lambda x: x[1].get("__count__",0), reverse=True)

        def is_leaf(node):
            """No sub-directory children."""
            return len(get_children(node, 1)) == 0

        def row_html(name, count, pct, indent=0, is_url=False):
            pad = indent * 1.5
            icon = "🔗" if is_url else ("📁" if indent==0 else "📂")
            color = "#2563eb" if is_url else "#111827"
            return f'''<div style="display:flex;align-items:center;gap:0.5rem;padding:0.35rem 0.75rem;
            margin-left:{pad}rem;border-radius:6px;font-size:0.84rem;color:{color}">
            <span>{icon}</span>
            <span style="flex:1;font-weight:{"600" if indent==0 else "400"}">{name}</span>
            <span style="color:#6b7280;font-size:0.78rem">{count:,} URLs</span>
            <span style="color:#9ca3af;font-size:0.75rem;margin-left:0.5rem">{pct}%</span>
            </div>'''

        parts_tuple = tuple(map(tuple, df["url_parts"].tolist()))
        locs_tuple  = tuple(df["loc"].tolist())
        tree = attach_urls(parts_tuple, locs_tuple)

        min_c = st.number_input("Min URLs per node", min_value=1, value=1, step=1, key="hier_min")
        mc = int(min_c)

        # Root
        root_count = tree.get("__count__", n_total)
        st.markdown(f'''<div style="font-size:0.95rem;font-weight:700;color:#111827;padding:0.75rem 1rem;
        background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;margin-bottom:0.75rem">
        🌐 {domain_name} &nbsp;—&nbsp; <span style="color:#2563eb">{root_count:,} URLs</span> &nbsp;·&nbsp; 100%
        </div>''', unsafe_allow_html=True)

        level1 = get_children(tree, mc)

        for sec, sec_node in level1:
            sec_count = sec_node.get("__count__", 0)
            sec_pct   = round(sec_count/n_total*100, 2)
            level2    = get_children(sec_node, mc)

            if not level2:
                # Single URL or leaf at level 1 — show URLs directly
                urls = sec_node.get("__urls__", [])
                st.markdown(row_html(sec, sec_count, sec_pct, 0, is_url=len(urls)<=1), unsafe_allow_html=True)
                if urls:
                    for u in urls[:5]:
                        st.markdown(f'&nbsp;&nbsp;&nbsp;&nbsp;<a href="{u}" target="_blank" style="font-size:0.78rem;color:#2563eb">{u}</a>', unsafe_allow_html=True)
            else:
                with st.expander(f"📁  {sec}   —   {sec_count:,} URLs  ({sec_pct}%)"):
                    for sub, sub_node in level2:
                        sub_count = sub_node.get("__count__", 0)
                        sub_pct   = round(sub_count/n_total*100, 2)
                        level3    = get_children(sub_node, mc)

                        if not level3:
                            # Leaf at level 2 — show as plain row + URLs
                            urls2 = sub_node.get("__urls__", [])
                            st.markdown(row_html(sub, sub_count, sub_pct, 1, is_url=len(urls2)<=1), unsafe_allow_html=True)
                            if urls2 and len(urls2) <= 3:
                                for u in urls2:
                                    st.markdown(f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="{u}" target="_blank" style="font-size:0.76rem;color:#2563eb">{u}</a>', unsafe_allow_html=True)
                        else:
                            with st.expander(f"📂  {sub}   —   {sub_count:,} URLs  ({sub_pct}%)"):
                                for sub2, sub2_node in level3:
                                    sub2_count = sub2_node.get("__count__", 0)
                                    sub2_pct   = round(sub2_count/n_total*100, 2)
                                    level4     = get_children(sub2_node, mc)

                                    if not level4:
                                        # Leaf at level 3 — show URLs
                                        urls3 = sub2_node.get("__urls__", [])
                                        st.markdown(row_html(sub2, sub2_count, sub2_pct, 2, is_url=len(urls3)<=1), unsafe_allow_html=True)
                                        if urls3 and len(urls3) <= 3:
                                            for u in urls3:
                                                st.markdown(f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="{u}" target="_blank" style="font-size:0.74rem;color:#2563eb">{u}</a>', unsafe_allow_html=True)
                                    else:
                                        with st.expander(f"📄  {sub2}   —   {sub2_count:,} URLs  ({sub2_pct}%)"):
                                            rows = []
                                            for k, v in level4:
                                                cnt  = v.get("__count__", 0)
                                                pct2 = round(cnt/n_total*100, 3)
                                                leaf_urls = v.get("__urls__", [])
                                                url_str = leaf_urls[0] if len(leaf_urls)==1 else f"{cnt} URLs"
                                                rows.append({"Name": k, "URLs": cnt, "%": f"{pct2}%", "URL": url_str})
                                            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Hierarchy error: {e}")

# ═══════════════════════════════════════
# TAB 3 — N-GRAMS
# ═══════════════════════════════════════
with tabs[2]:
    try:
        full_tok = df["loc"].apply(lambda u: tokenize(urlparse(u).path)).tolist()
        slug_tok = df["last_slug"].apply(tokenize).tolist()
        ng_f = build_ngrams(full_tok)
        ng_s = build_ngrams(slug_tok)
        t1, t2 = st.tabs(["Full URL Path", "Last Slug Only"])
        for tab_obj, ng_dict, lbl in [(t1,ng_f,"Full URL"), (t2,ng_s,"Last Slug")]:
            with tab_obj:
                st.caption(f"Most frequent words/phrases in {lbl}s — reveals content strategy and topic clusters")
                for ng_lbl, ngdf in ng_dict.items():
                    if ngdf.empty: continue
                    sh(ng_lbl)
                    top = ngdf.head(20).copy()
                    top["%"] = (top["count"]/top["count"].sum()*100).round(1).astype(str)+"%"
                    c1,c2 = st.columns([3,2])
                    with c1:
                        fig = px.bar(top.sort_values("count", ascending=True),
                                     x="count", y="ngram", orientation="h",
                                     color="count", color_continuous_scale="Blues",
                                     title=f"Top 20 {ng_lbl}")
                        fig.update_layout(coloraxis_showscale=False, height=max(300,min(len(top)*30,520)))
                        ap(fig); st.plotly_chart(fig, use_container_width=True)
                    with c2:
                        st.dataframe(top, use_container_width=True, hide_index=True, height=max(300,min(len(top)*35,520)))
    except Exception as e:
        st.error(f"N-gram error: {e}")

# ═══════════════════════════════════════
# TAB 4 — TEMPORAL
# ═══════════════════════════════════════
with tabs[3]:
    try:
        if n_dates == 0:
            st.info("No lastmod dates found.")
        else:
            dated = df[df["lastmod_dt"].notna()].copy()
            dated["year"]  = dated["lastmod_dt"].dt.year.astype(int)
            dated["month"] = dated["lastmod_dt"].dt.to_period("M").astype(str)
            dated["quarter"]   = dated["lastmod_dt"].dt.to_period("Q").astype(str)
            dated["month_num"] = dated["lastmod_dt"].dt.month

            sh("Publishing Velocity", insight="Compare their monthly publishing pace to yours. Publish fresh content during their quiet months — same demand, less competition.")
            monthly = dated.groupby("month").size().reset_index(name="Count").sort_values("month")
            fig = px.line(monthly,x="month",y="Count",markers=True,title="Monthly Publishing Velocity",color_discrete_sequence=["#2563eb"])
            fig.update_traces(line_width=2.5,marker_size=5); ap(fig); st.plotly_chart(fig,use_container_width=True)

            c1,c2 = st.columns(2)
            with c1:
                sh("By Year")
                yearly = dated.groupby("year").size().reset_index(name="Count"); yearly["year"]=yearly["year"].astype(str)
                fig=px.bar(yearly,x="year",y="Count",text="Count",color="Count",color_continuous_scale="Blues",title="Per Year")
                fig.update_traces(textposition="outside",marker_line_width=0); fig.update_layout(coloraxis_showscale=False)
                ap(fig); st.plotly_chart(fig,use_container_width=True); st.dataframe(yearly,use_container_width=True,hide_index=True)
            with c2:
                sh("By Quarter (Last 12)")
                quarterly = dated.groupby("quarter").size().reset_index(name="Count").sort_values("quarter").tail(12)
                fig=px.bar(quarterly,x="quarter",y="Count",text="Count",color="Count",color_continuous_scale="Blues",title="Per Quarter")
                fig.update_traces(textposition="outside",marker_line_width=0); fig.update_layout(coloraxis_showscale=False)
                ap(fig); st.plotly_chart(fig,use_container_width=True); st.dataframe(quarterly,use_container_width=True,hide_index=True)

            sh("Freshness Breakdown", insight="If >50% content is older than 1 year, publish fresher content on same topics to outrank.")
            fo=["Last Week","Last Month","Last Quarter","Last Year","Older than 1 Year","No Date"]
            fc=df["freshness"].value_counts().reindex(fo,fill_value=0).reset_index()
            fc.columns=["Bucket","Count"]; fc["%"]=(fc["Count"]/n_total*100).round(1).astype(str)+"%"
            c1,c2=st.columns([3,2])
            with c1:
                fig=px.bar(fc,x="Bucket",y="Count",text="Count",color="Bucket",title="Freshness Distribution",
                           color_discrete_sequence=["#10b981","#2563eb","#6366f1","#f59e0b","#ef4444","#d1d5db"])
                fig.update_traces(textposition="outside",marker_line_width=0,showlegend=False)
                ap(fig); st.plotly_chart(fig,use_container_width=True)
            with c2: st.dataframe(fc,use_container_width=True,hide_index=True)

            sh("Publishing Heatmap", insight="Dark months = competitor doesn't publish. Publish then — same demand, less noise.")
            hm=dated.groupby(["year","month_num"]).size().reset_index(name="count")
            hp=hm.pivot(index="year",columns="month_num",values="count").fillna(0)
            mn=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
            hp.columns=[mn[int(c)-1] for c in hp.columns]; hp.index=hp.index.astype(str)
            fig=px.imshow(hp,color_continuous_scale="Blues",title="Heatmap (Year × Month)",aspect="auto",text_auto=True)
            ap(fig); st.plotly_chart(fig,use_container_width=True)

            if "dir_1" in df.columns and df["dir_1"].notna().sum()>0:
                sh("Section Publishing Velocity")
                d2=dated[dated["dir_1"].notna()].copy()
                top8=d2["dir_1"].value_counts().head(8).index.tolist()
                d2=d2[d2["dir_1"].isin(top8)]
                dm=d2.groupby(["dir_1","month"]).size().reset_index(name="Count").sort_values("month")
                fig=px.bar(dm,x="month",y="Count",color="dir_1",barmode="stack",title="Top 8 Sections — Monthly Activity")
                ap(fig,True); st.plotly_chart(fig,use_container_width=True)
                piv=dm.pivot_table(index="month",columns="dir_1",values="Count",fill_value=0).sort_index().tail(12)
                st.dataframe(piv,use_container_width=True)
    except Exception as e:
        st.error(f"Temporal error: {e}")

# ═══════════════════════════════════════
# TAB 5 — ADVANCED EDA
# ═══════════════════════════════════════
with tabs[4]:
    try:
        # 1. Depth vs Recency
        sh("URL Depth vs Content Recency",
           insight="Pages deeper than level 3 AND older than 365 days are ignored by both the site owner and Google. Create shallower, fresher versions of the same content.")
        if n_dates > 0:
            d2 = df[df["lastmod_dt"].notna()].copy()
            d2["days_ago"] = (now - d2["lastmod_dt"]).dt.days
            rec = d2.groupby("url_depth")["days_ago"].mean().round(0).reset_index()
            rec.columns = ["url_depth","Avg Days Since Update"]
            tot = df.groupby("url_depth").size().reset_index(name="Total URLs")
            rec = rec.merge(tot, on="url_depth", how="outer").fillna(0)
            rec["Avg Days Since Update"] = rec["Avg Days Since Update"].astype(int)
            rec = rec.sort_values("url_depth")
            rec["SEO Risk"] = rec.apply(
                lambda r: "🔴 Stale+Deep" if r["url_depth"]>=3 and r["Avg Days Since Update"]>365
                else ("🟡 Monitor" if r["Avg Days Since Update"]>180 else "🟢 Fresh"), axis=1)
            rec = rec.rename(columns={"url_depth":"Depth"})
            c1,c2 = st.columns([2,3])
            with c1: st.dataframe(rec, use_container_width=True, hide_index=True)
            with c2:
                fig=px.bar(rec,x="Depth",y="Avg Days Since Update",text="Avg Days Since Update",
                           color="Avg Days Since Update",color_continuous_scale="RdYlGn_r",
                           title="Avg Days Since Update by Depth",hover_data=["Total URLs"])
                fig.update_traces(textposition="outside",marker_line_width=0,textfont_color="#111827")
                fig.update_layout(coloraxis_showscale=False,xaxis=dict(tickmode="linear"))
                ap(fig); st.plotly_chart(fig,use_container_width=True)

        # 2. URL Length vs Depth
        sh("URL Length vs Depth",
           insight="Shallow pages (depth ≤2) with URLs longer than 70 chars = possible keyword stuffing. Google recommends short, descriptive URLs.")
        risky = df[(df["url_depth"]<=2) & (df["url_length"]>70)]
        if len(risky)>0:
            st.markdown(f'<div class="warn">⚠️ {len(risky):,} shallow pages (depth ≤2) have URLs longer than 70 chars</div>', unsafe_allow_html=True)
        c1,c2 = st.columns([3,2])
        with c1:
            fig=px.box(df,x="url_depth",y="url_length",title="URL Length by Depth",color_discrete_sequence=["#2563eb"])
            fig.update_layout(xaxis=dict(tickmode="linear")); ap(fig); st.plotly_chart(fig,use_container_width=True)
        with c2:
            dl=df.groupby("url_depth")["url_length"].agg(["mean","median","min","max","count"]).round(1).reset_index()
            dl.columns=["Depth","Avg","Median","Min","Max","Count"]
            st.dataframe(dl,use_container_width=True,hide_index=True)

        # 3. Content Gap Opportunities
        if "dir_1" in df.columns and df["dir_1"].notna().sum()>0 and n_dates>0:
            sh("Content Gap Opportunities",
               insight="High Opportunity Score = many URLs + high stale % = competitor invested here but stopped. Publish fresher, deeper content on the same topics to outrank them.")
            two_yrs = now - timedelta(days=730)
            df_g = df.copy()
            df_g["is_stale"] = (df_g["lastmod_dt"]<two_yrs) | df_g["lastmod_dt"].isna()
            d3 = df_g[df_g["dir_1"].notna() & df_g["lastmod_dt"].notna()].copy()
            d3["days_ago"] = (now - d3["lastmod_dt"]).dt.days
            avgd = d3.groupby("dir_1")["days_ago"].mean().round(0).reset_index()
            avgd.columns = ["dir_1","Avg Days Since Update"]
            sd = df_g[df_g["dir_1"].notna()].groupby("dir_1").agg(Total=("loc","count"),Stale=("is_stale","sum")).reset_index()
            sd["Stale %"] = (sd["Stale"]/sd["Total"]*100).round(1)
            sd = sd.merge(avgd, on="dir_1", how="left")
            sd["Opportunity Score"] = (sd["Stale %"]*sd["Total"]/100).round(0).astype(int)
            sd = sd.sort_values("Opportunity Score", ascending=False).head(20)
            sd.columns = ["Section","Total URLs","Stale URLs","Stale %","Avg Days Since Update","Opportunity Score"]
            st.dataframe(sd, use_container_width=True, hide_index=True)

        # 4. Section × Freshness
        if "dir_1" in df.columns and df["dir_1"].notna().sum()>0:
            sh("Section × Freshness",
               insight="Blue/Green = competitor actively investing — hard to beat now. Red = abandoned territory — your easy wins. Focus content budget on the red sections.")
            top10 = df["dir_1"].value_counts().head(10).index
            mv = df[df["dir_1"].isin(top10)].groupby(["dir_1","freshness"]).size().reset_index(name="Count")
            fo2 = ["Last Week","Last Month","Last Quarter","Last Year","Older than 1 Year","No Date"]
            mv["freshness"] = pd.Categorical(mv["freshness"], categories=fo2, ordered=True)
            mv = mv.sort_values(["dir_1","freshness"])
            fig = px.bar(mv, x="dir_1", y="Count", color="freshness", barmode="stack",
                         title="Top 10 Sections — Freshness Breakdown",
                         color_discrete_map={"Last Week":"#10b981","Last Month":"#2563eb",
                                             "Last Quarter":"#6366f1","Last Year":"#f59e0b",
                                             "Older than 1 Year":"#ef4444","No Date":"#e5e7eb"})
            fig.update_layout(xaxis_title="Section", height=420)
            ap(fig, True); st.plotly_chart(fig, use_container_width=True)
            pv = mv.pivot_table(index="dir_1", columns="freshness", values="Count", fill_value=0)
            st.dataframe(pv, use_container_width=True)

    except Exception as e:
        st.error(f"Advanced EDA error: {e}")

# ═══════════════════════════════════════
# TAB 6 — RAW DATA (session_state filters)
# ═══════════════════════════════════════
with tabs[5]:
    try:
        sh("Raw Data")

        # Init session state for filters
        if "raw_search" not in st.session_state: st.session_state["raw_search"] = ""
        if "raw_fresh" not in st.session_state: st.session_state["raw_fresh"] = "All"
        if "raw_dir" not in st.session_state: st.session_state["raw_dir"] = "All"
        if "raw_depth" not in st.session_state: st.session_state["raw_depth"] = "All"

        c1,c2,c3,c4 = st.columns(4)
        with c1: search_term = st.text_input("Search URLs", value=st.session_state["raw_search"], placeholder="e.g. blog", key="raw_search")
        with c2:
            fo = ["All"] + df["freshness"].value_counts().index.tolist()
            fresh_f = st.selectbox("Freshness", fo, index=fo.index(st.session_state["raw_fresh"]) if st.session_state["raw_fresh"] in fo else 0, key="raw_fresh")
        with c3:
            if "dir_1" in df.columns:
                do = ["All"] + df["dir_1"].dropna().value_counts().index.tolist()
                dir_f = st.selectbox("Section", do, index=do.index(st.session_state["raw_dir"]) if st.session_state["raw_dir"] in do else 0, key="raw_dir")
            else: dir_f = "All"
        with c4:
            dpo = ["All"] + [str(x) for x in sorted(df["url_depth"].unique().tolist())]
            dep_f = st.selectbox("Depth", dpo, index=dpo.index(st.session_state["raw_depth"]) if st.session_state["raw_depth"] in dpo else 0, key="raw_depth")

        filtered = df.copy()
        if search_term: filtered = filtered[filtered["loc"].str.contains(search_term, case=False, na=False)]
        if fresh_f != "All": filtered = filtered[filtered["freshness"]==fresh_f]
        if dir_f != "All" and "dir_1" in filtered.columns: filtered = filtered[filtered["dir_1"]==dir_f]
        if dep_f != "All": filtered = filtered[filtered["url_depth"]==int(dep_f)]

        st.caption(f"Showing {len(filtered):,} of {n_total:,} URLs")
        dcols = display_cols(filtered)
        st.dataframe(clean_df(filtered)[dcols], use_container_width=True, height=480)
        st.download_button("⬇ Download CSV", clean_df(filtered)[dcols].to_csv(index=False).encode("utf-8"),
                           f"sitemap_{domain_name.replace('.','_')}.csv", "text/csv")

        sh("Summary")
        st.dataframe(pd.DataFrame({"Metric":["Total URLs","Avg Depth","Max Depth","Avg URL Length",
                                              "With Dates","Last Week","Last Month","Last Quarter","Last Year"],
                                   "Value":[f"{n_total:,}",avg_depth,max_depth,round(df["url_length"].mean(),1),
                                            f"{n_dates:,}",f"{n_week:,}",f"{n_month:,}",f"{n_quarter:,}",f"{n_year:,}"]}),
                     use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Raw data error: {e}")

# ═══════════════════════════════════════
# TAB 7 — EXPORT (summary only, no slugs)
# ═══════════════════════════════════════
with tabs[6]:
    try:
        sh("Export Report")

        def make_report():
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

            # Depth table
            dc2 = df["url_depth"].value_counts().sort_index().reset_index()
            dc2.columns=["Depth","URL Count"]; dc2["%"]=(dc2["URL Count"]/n_total*100).round(2).astype(str)+"%"

            # Structure (dir_1 only — no slugs)
            struct_html = ""
            if "dir_1" in df.columns and df["dir_1"].notna().sum()>0:
                vc = df["dir_1"].value_counts().reset_index()
                vc.columns=["Section","URLs"]; vc["%"]=(vc["URLs"]/n_total*100).round(2).astype(str)+"%"
                # Add dir_2 summary inside each section
                rows_html = ""
                for _, row in vc.iterrows():
                    rows_html += f"<tr><td><strong>{row['Section']}</strong></td><td>{row['URLs']:,}</td><td>{row['%']}</td></tr>"
                    if "dir_2" in df.columns:
                        subs = df[df["dir_1"]==row["Section"]]["dir_2"].dropna().value_counts().head(5)
                        for sub_k, sub_v in subs.items():
                            rows_html += f"<tr><td style='padding-left:2rem;color:#6b7280'>↳ {sub_k}</td><td style='color:#6b7280'>{sub_v:,}</td><td style='color:#6b7280'>{round(sub_v/n_total*100,2)}%</td></tr>"
                struct_html = f"<table class='dt'><tr><th>Section</th><th>URLs</th><th>%</th></tr>{rows_html}</table>"

            # N-grams slug only
            ng_html = ""
            for lbl, ngdf in build_ngrams(df["last_slug"].apply(tokenize).tolist()).items():
                if ngdf.empty: continue
                ng_html += f"<h3>{lbl}</h3>" + ngdf.head(15).to_html(index=False, classes="dt", border=0)

            fo3=["Last Week","Last Month","Last Quarter","Last Year","Older than 1 Year","No Date"]
            fc2=df["freshness"].value_counts().reindex(fo3,fill_value=0).reset_index()
            fc2.columns=["Bucket","Count"]; fc2["%"]=(fc2["Count"]/n_total*100).round(1).astype(str)+"%"

            # Gaps
            gap_html = ""
            if "dir_1" in df.columns and n_dates>0:
                two_yrs=now-timedelta(days=730)
                df_g2=clean_df(df).copy()
                df_g2["is_stale"]=(df_g2["lastmod_dt"]<two_yrs)|df_g2["lastmod_dt"].isna()
                sg=df_g2[df_g2["dir_1"].notna()].groupby("dir_1").agg(Total=("loc","count"),Stale=("is_stale","sum")).reset_index()
                sg["Stale%"]=(sg["Stale"]/sg["Total"]*100).round(1)
                sg["Score"]=(sg["Stale%"]*sg["Total"]/100).round(0).astype(int)
                sg=sg.sort_values("Score",ascending=False).head(15)
                sg.columns=["Section","Total","Stale","Stale %","Opportunity Score"]
                gap_html=sg.to_html(index=False,classes="dt",border=0)

            return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>Sitemap Copilot — {domain_name}</title>
<style>
body{{font-family:'Inter',-apple-system,sans-serif;background:#fff;color:#111827;max-width:1000px;margin:0 auto;padding:2rem 1.5rem;font-size:14px}}
.hdr{{display:flex;align-items:center;gap:1rem;border-bottom:2px solid #2563eb;padding-bottom:1rem;margin-bottom:1.5rem}}
.hdr img{{width:48px;height:48px;border-radius:50%;object-fit:cover;border:2px solid #e5e7eb}}
.brand{{font-size:1.4rem;font-weight:700;letter-spacing:-0.02em}}
.brand span{{color:#2563eb}}
.an{{font-weight:600;font-size:0.9rem}}
.ar{{color:#2563eb;font-size:0.78rem}}
.al a{{color:#6b7280;font-size:0.75rem;margin-right:0.8rem;text-decoration:none}}
.meta{{color:#6b7280;font-size:0.82rem;margin-bottom:2rem;padding:0.75rem 1rem;background:#f9fafb;border-radius:8px;border:1px solid #e5e7eb}}
h2{{font-size:1rem;font-weight:700;color:#111827;margin:2rem 0 0.75rem;padding-bottom:0.4rem;border-bottom:1px solid #e5e7eb;text-transform:uppercase;letter-spacing:0.05em;font-size:0.78rem;color:#6b7280}}
h3{{font-size:0.88rem;font-weight:600;color:#374151;margin:1.2rem 0 0.4rem}}
table.dt{{width:100%;border-collapse:collapse;margin:0.5rem 0;font-size:0.84rem}}
table.dt th{{background:#f9fafb;color:#374151;padding:0.45rem 0.75rem;text-align:left;font-weight:600;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.04em;border-bottom:1px solid #e5e7eb}}
table.dt td{{padding:0.4rem 0.75rem;border-bottom:1px solid #f3f4f6}}
table.dt tr:hover td{{background:#f9fafb}}
.footer{{margin-top:3rem;padding-top:1rem;border-top:1px solid #e5e7eb;color:#9ca3af;font-size:0.75rem;text-align:center}}
.footer a{{color:#6b7280;text-decoration:none}}
</style></head><body>
<div class="hdr">
  <div><div class="brand">Sitemap<span>Copilot</span></div></div>
  <div style="margin-left:auto;display:flex;align-items:center;gap:0.8rem">
    <img src="data:image/png;base64,{PHOTO_B64}" alt="Sankar">
    <div><div class="an">Sankar Gurumurthy</div>
    <div class="ar">Head of AI SEO &amp; Marketing Data Scientist</div>
    <div class="al"><a href="https://www.linkedin.com/in/sankar-gurumurthy-a1044a136/">LinkedIn</a><a href="https://github.com/sg-sankar">GitHub</a></div></div>
  </div>
</div>
<div class="meta">Domain: <strong>{domain_name}</strong> &nbsp;·&nbsp; Generated: {now_str} &nbsp;·&nbsp; Total URLs: <strong>{n_total:,}</strong> &nbsp;·&nbsp; Avg Depth: <strong>{avg_depth}</strong></div>
<h2>Overview</h2>
<table class="dt"><tr><th>Metric</th><th>Value</th></tr>
{"".join(f"<tr><td>{k}</td><td><strong>{v}</strong></td></tr>" for k,v in [("Total URLs",f"{n_total:,}"),("Avg Depth",avg_depth),("Max Depth",max_depth),("With Dates",f"{n_dates:,}"),("Last Week",f"{n_week:,}"),("Last Month",f"{n_month:,}"),("Last Quarter",f"{n_quarter:,}"),("Last Year",f"{n_year:,}")])}
</table>
<h2>URL Depth Distribution</h2>{dc2.to_html(index=False,classes="dt",border=0)}
<h2>Site Structure (Section → Sub-section)</h2>{struct_html}
<h2>N-Gram Analysis</h2>{ng_html}
<h2>Content Freshness</h2>{fc2.to_html(index=False,classes="dt",border=0)}
<h2>Content Gap Opportunities</h2>{gap_html}
<div class="footer">Built by <a href="https://www.linkedin.com/in/sankar-gurumurthy-a1044a136/">Sankar Gurumurthy</a> · <a href="https://github.com/sg-sankar">github.com/sg-sankar</a> · Sitemap Copilot · Open source &amp; free forever</div>
</body></html>"""

        html_out = make_report()
        c1,c2 = st.columns(2)
        with c1:
            st.download_button("⬇ Download HTML Report", html_out.encode("utf-8"),
                               f"sitemap_copilot_{domain_name.replace('.','_')}.html", "text/html")
            st.caption("Open in Chrome → Cmd+P → Save as PDF")
        # CSV removed — use Raw Data tab for full URL list

        st.markdown("---")
        st.markdown("""**Report includes:**
- Overview metrics
- URL depth distribution  
- Site structure with top sub-sections
- N-gram analysis (slug keywords)
- Content freshness breakdown
- Content gap opportunities (attack zones)
""")

    except Exception as e:
        st.error(f"Export error: {e}")

# ── Footer ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;padding:2rem 0 1rem;color:#9ca3af;font-size:0.78rem;border-top:1px solid #f3f4f6;margin-top:3rem">
  Sitemap Copilot · Built by
  <a href="https://www.linkedin.com/in/sankar-gurumurthy-a1044a136/" target="_blank" style="color:#6b7280;text-decoration:none">Sankar Gurumurthy</a>
  · <a href="https://github.com/sg-sankar" target="_blank" style="color:#6b7280;text-decoration:none">github.com/sg-sankar</a>
  · Open source · Free forever
</div>
""", unsafe_allow_html=True)
