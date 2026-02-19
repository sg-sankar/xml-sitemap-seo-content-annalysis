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
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Sitemap Intelligence · Sankar Gurumurthy",
    page_icon="🗺️", layout="wide", initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');
html,body,[data-testid="stAppViewContainer"]{background:#06060f;color:#e8e6e0;font-family:'DM Sans',sans-serif}
[data-testid="stAppViewContainer"]{background:radial-gradient(ellipse at 15% 10%,#1a0e35 0%,#06060f 55%,#081508 100%)}
h1,h2,h3,h4{font-family:'Syne',sans-serif;letter-spacing:-0.02em}
.hero{text-align:center;padding:2.5rem 1rem 1.5rem}
.hero-title{font-family:'Syne',sans-serif;font-size:clamp(2.8rem,6vw,5.2rem);font-weight:800;background:linear-gradient(135deg,#a8ff78 0%,#78ffd6 60%,#7affb2 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.05;margin-bottom:0.4rem}
.hero-sub{font-size:1.05rem;color:#777;font-weight:300;margin-bottom:1.5rem}
.author-card{display:flex;align-items:center;gap:1.2rem;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.09);border-radius:18px;padding:1rem 1.4rem;margin:0 auto 1.5rem;max-width:520px}
.author-photo{width:58px;height:58px;border-radius:50%;border:2px solid rgba(168,255,120,0.5);object-fit:cover;flex-shrink:0}
.author-name{font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:700;color:#e8e6e0}
.author-role{font-size:0.8rem;color:#a8ff78;font-weight:500;margin:0.1rem 0 0.4rem}
.author-links a{display:inline-flex;align-items:center;gap:0.3rem;font-size:0.78rem;color:#888;text-decoration:none;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);padding:0.2rem 0.6rem;border-radius:20px;margin-right:0.4rem}
.author-links a:hover{color:#a8ff78;border-color:rgba(168,255,120,0.3)}
.metric-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:0.75rem;margin:1.2rem 0}
.metric-card{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:1rem 0.8rem;text-align:center}
.metric-num{font-family:'Syne',sans-serif;font-size:1.85rem;font-weight:700;color:#a8ff78;line-height:1}
.metric-label{font-size:0.72rem;color:#666;margin-top:0.2rem;text-transform:uppercase;letter-spacing:0.05em}
.section-header{font-family:'Syne',sans-serif;font-size:1.25rem;font-weight:700;color:#e8e6e0;margin:1.8rem 0 0.5rem;padding-left:0.7rem;border-left:3px solid #a8ff78}
.section-sub{font-size:0.82rem;color:#555;margin:-0.2rem 0 0.8rem 0.9rem;font-style:italic}
.stTextInput>div>div>input{background:rgba(255,255,255,0.05)!important;border:1px solid rgba(255,255,255,0.15)!important;border-radius:12px!important;color:#e8e6e0!important;font-size:1rem!important;padding:0.7rem 1rem!important}
.stTextInput>div>div>input:focus{border-color:#a8ff78!important;box-shadow:0 0 0 2px rgba(168,255,120,0.12)!important}
.stButton>button{background:linear-gradient(135deg,#a8ff78,#78ffd6)!important;color:#06060f!important;font-family:'Syne',sans-serif!important;font-weight:700!important;font-size:1rem!important;border:none!important;border-radius:12px!important;padding:0.7rem 2rem!important;width:100%!important}
.stTabs [data-baseweb="tab-list"]{background:rgba(255,255,255,0.03);border-radius:12px;padding:4px;gap:4px}
.stTabs [data-baseweb="tab"]{font-family:'Syne',sans-serif!important;font-weight:600!important;color:#777!important;border-radius:8px!important;padding:0.45rem 1.1rem!important}
.stTabs [aria-selected="true"]{background:rgba(168,255,120,0.13)!important;color:#a8ff78!important}
.stDownloadButton>button{background:rgba(168,255,120,0.08)!important;color:#a8ff78!important;border:1px solid rgba(168,255,120,0.25)!important;font-family:'Syne',sans-serif!important;font-weight:600!important;border-radius:10px!important}
.footer{text-align:center;padding:2.5rem 1rem 1rem;color:#333;font-size:0.8rem;border-top:1px solid rgba(255,255,255,0.05);margin-top:3rem}
.footer a{color:#555;text-decoration:none}
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
PLOT_CFG = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font_color='#999', font_family='DM Sans',
    title_font_family='Syne', title_font_size=14,
    colorway=['#a8ff78','#78ffd6','#ff7eb3','#ffd278','#7eb8ff','#ff9f7e','#c4b5fd'],
)
def apply_theme(fig, legend=False):
    fig.update_layout(**PLOT_CFG, showlegend=legend)
    fig.update_xaxes(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.08)', zeroline=False)
    fig.update_yaxes(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.08)', zeroline=False)
    return fig

def extract_sitemaps_from_robots(url):
    try:
        r = requests.get(url, timeout=15, headers={'User-Agent':'SitemapIntelligence/1.0'})
        r.raise_for_status()
        return [s.strip() for s in re.findall(r'(?i)^Sitemap:\s*(.+)', r.text, re.MULTILINE)]
    except: return []

def tokenize_slug(slug):
    s = re.sub(r'[_\-]',' ', str(slug).lower())
    s = re.sub(r'[^a-z0-9 ]','', s)
    return [t for t in s.split() if t and len(t)>1]

def get_ngrams(tokens, n):
    return [' '.join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def build_ngrams(all_tokens, max_n=5):
    out = {}
    labels = {1:'Unigrams',2:'Bigrams',3:'Trigrams',4:'4-grams',5:'5-grams'}
    for n in range(1, max_n+1):
        grams = []
        for toks in all_tokens: grams.extend(get_ngrams(toks, n))
        out[labels[n]] = pd.DataFrame(Counter(grams).most_common(30), columns=['ngram','count'])
    return out

def safe_depth_freshness(df):
    try:
        dated = df[df['lastmod_dt'].notna()].copy()
        f = dated.groupby('url_depth').size().reset_index(name='updated_count')
        t = df.groupby('url_depth').size().reset_index(name='total')
        m = f.merge(t, on='url_depth', how='outer').fillna(0).astype({'updated_count':int,'total':int})
        m['update_rate'] = (m['updated_count'] / m['total'] * 100).round(1)
        return m
    except: return pd.DataFrame()

# ── Hero + Author ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">Sitemap Intelligence</div>
  <div class="hero-sub">Professional SEO competitor analysis — paste a URL, get deep insights instantly</div>
  <div class="author-card">
    <img class="author-photo"
      src="https://media.licdn.com/dms/image/v2/D5603AQGhW9LkVEtd6A/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1707118558424?e=1747267200&v=beta&t=hQGM6jD4tCKJI1m8qjvMxBDt4S8wJ9c5MKlb0bBPMgE"
      onerror="this.src='https://ui-avatars.com/api/?name=Sankar+G&background=0d1a0d&color=a8ff78&size=58&bold=true'"
      alt="Sankar Gurumurthy">
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

col_inp, col_btn = st.columns([5,1])
with col_inp:
    input_url = st.text_input("", placeholder="Paste robots.txt or sitemap.xml URL here…", label_visibility="collapsed")
with col_btn:
    st.markdown("<div style='padding-top:0.15rem'></div>", unsafe_allow_html=True)
    run = st.button("Analyse →")

if not run or not input_url.strip():
    st.markdown("<div style='text-align:center;padding:3rem;color:#333;font-size:0.88rem'>Supports <b style='color:#444'>robots.txt</b> · <b style='color:#444'>sitemap.xml</b> · <b style='color:#444'>sitemap index</b> · <b style='color:#444'>nested & gzipped sitemaps</b></div>", unsafe_allow_html=True)
    st.stop()

# ── Fetch ─────────────────────────────────────────────────────────────────────
with st.spinner("🔍 Fetching and parsing…"):
    sitemap_urls = extract_sitemaps_from_robots(input_url.strip()) if 'robots.txt' in input_url.lower() else [input_url.strip()]
    if not sitemap_urls:
        st.error("No sitemaps found in robots.txt"); st.stop()

    all_dfs, errors = [], []
    for su in sitemap_urls:
        try: all_dfs.append(adv.sitemap_to_df(su))
        except Exception as e: errors.append(f"{su}: {e}")

    if not all_dfs: st.error("Failed to fetch any sitemaps.\n" + "\n".join(errors)); st.stop()

    df = pd.concat(all_dfs, ignore_index=True)
    if 'loc' not in df.columns: st.error("No URLs found."); st.stop()

    df = df.drop_duplicates('loc')
    df = df[df['loc'].notna() & df['loc'].str.startswith('http')].reset_index(drop=True)
    df['lastmod_dt'] = pd.to_datetime(df.get('lastmod', pd.Series(dtype=str)), errors='coerce', utc=True)
    df['url_parts']  = df['loc'].apply(lambda u: [p for p in urlparse(u).path.rstrip('/').split('/') if p])
    df['url_depth']  = df['url_parts'].apply(len)
    df['last_slug']  = df['url_parts'].apply(lambda x: x[-1] if x else '')
    df['domain']     = df['loc'].apply(lambda u: urlparse(u).netloc)
    df['url_length'] = df['loc'].apply(len)
    df['slug_words'] = df['last_slug'].apply(lambda s: len(re.findall(r'[a-zA-Z0-9]+', str(s))))

    max_depth = int(df['url_depth'].max()) if len(df) else 1
    for i in range(1, min(max_depth+1, 9)):
        df[f'dir_{i}'] = df['url_parts'].apply(lambda x, i=i: x[i-1] if len(x)>=i else None)

# ── Globals ───────────────────────────────────────────────────────────────────
now=pd.Timestamp.now(tz='UTC')
last_week=now-timedelta(days=7); last_month=now-timedelta(days=30)
last_quarter=now-timedelta(days=90); last_year=now-timedelta(days=365)
n_total=len(df); n_with_date=int(df['lastmod_dt'].notna().sum())
n_week=int((df['lastmod_dt']>=last_week).sum()); n_month=int((df['lastmod_dt']>=last_month).sum())
n_quarter=int((df['lastmod_dt']>=last_quarter).sum()); n_year=int((df['lastmod_dt']>=last_year).sum())
avg_depth=round(df['url_depth'].mean(),1); domain_name=df['domain'].iloc[0] if len(df) else 'Unknown'

def freshness_bucket(dt):
    if pd.isna(dt): return 'No Date'
    if dt>=last_week: return 'Last Week'
    if dt>=last_month: return 'Last Month'
    if dt>=last_quarter: return 'Last Quarter'
    if dt>=last_year: return 'Last Year'
    return 'Older than 1 Year'
df['freshness']=df['lastmod_dt'].apply(freshness_bucket)

# ── Metric Strip ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;color:#444;font-size:0.8rem;margin-bottom:0.4rem">Analysing: <strong style="color:#666">{domain_name}</strong></div>
<div class="metric-grid">
  <div class="metric-card"><div class="metric-num">{n_total:,}</div><div class="metric-label">Total URLs</div></div>
  <div class="metric-card"><div class="metric-num">{avg_depth}</div><div class="metric-label">Avg Depth</div></div>
  <div class="metric-card"><div class="metric-num">{max_depth}</div><div class="metric-label">Max Depth</div></div>
  <div class="metric-card"><div class="metric-num">{n_with_date:,}</div><div class="metric-label">Have Dates</div></div>
  <div class="metric-card"><div class="metric-num">{n_week:,}</div><div class="metric-label">Last Week</div></div>
  <div class="metric-card"><div class="metric-num">{n_month:,}</div><div class="metric-label">Last Month</div></div>
  <div class="metric-card"><div class="metric-num">{n_quarter:,}</div><div class="metric-label">Last Quarter</div></div>
  <div class="metric-card"><div class="metric-num">{n_year:,}</div><div class="metric-label">Last Year</div></div>
</div>
""", unsafe_allow_html=True)

if errors:
    with st.expander(f"⚠️ {len(errors)} sitemap(s) had errors"):
        for e in errors: st.text(e)

tabs = st.tabs(["🏗 URL Structure","📝 N-Grams","📅 Temporal","🔬 Advanced EDA","📋 Raw Data","📥 Export"])

# ═══════════════════════════════════════════════════════════════════════════
# TAB 1  URL STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════
with tabs[0]:
    try:
        # Depth
        st.markdown('<div class="section-header">URL Depth Distribution</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">How many directory levels deep are the pages?</div>', unsafe_allow_html=True)
        dc = df['url_depth'].value_counts().sort_index().reset_index()
        dc.columns=['Depth Level','URL Count']
        dc['% of Total']=(dc['URL Count']/n_total*100).round(1).astype(str)+'%'
        c1,c2=st.columns([3,2])
        with c1:
            fig=px.bar(dc,x='Depth Level',y='URL Count',text='URL Count',color='URL Count',color_continuous_scale='Teal',title='URLs by Depth Level')
            fig.update_traces(textposition='outside',marker_line_width=0)
            fig.update_layout(coloraxis_showscale=False,xaxis=dict(tickmode='linear'))
            apply_theme(fig,False); st.plotly_chart(fig,use_container_width=True)
        with c2:
            st.dataframe(dc,use_container_width=True,hide_index=True)

        # Directory levels
        for level in range(1, min(max_depth+1,9)):
            col_name=f'dir_{level}'
            if col_name not in df.columns: break
            valid=df[col_name].dropna()
            if len(valid)==0: break
            st.markdown(f'<div class="section-header">Directory Level {level}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="section-sub">Top values at directory position {level}</div>', unsafe_allow_html=True)
            vc=valid.value_counts().head(25).reset_index()
            vc.columns=['Directory','URL Count']
            vc['% of Total']=(vc['URL Count']/n_total*100).round(2).astype(str)+'%'
            c1,c2=st.columns([3,2])
            with c1:
                fig=px.bar(vc,x='URL Count',y='Directory',orientation='h',title=f'Top Directories — Level {level}',color='URL Count',color_continuous_scale='Teal')
                fig.update_layout(yaxis={'categoryorder':'total ascending'},coloraxis_showscale=False,height=max(300,min(len(vc)*28,520)))
                apply_theme(fig,False); st.plotly_chart(fig,use_container_width=True)
            with c2:
                st.dataframe(vc,use_container_width=True,hide_index=True,height=max(300,min(len(vc)*35,520)))

        # URL Length
        st.markdown('<div class="section-header">URL Length Analysis</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Shorter URLs are cleaner for SEO. Long slugs with many words can dilute keyword signal.</div>', unsafe_allow_html=True)
        c1,c2,c3=st.columns(3)
        with c1:
            st.markdown("**URL Character Length Stats**")
            ul=df['url_length']
            st.dataframe(pd.DataFrame({'Metric':['Min','Max','Mean','Median','Std'],'Value':[int(ul.min()),int(ul.max()),round(ul.mean(),1),round(ul.median(),1),round(ul.std(),1)]}),use_container_width=True,hide_index=True)
        with c2:
            st.markdown("**Last Slug Word Count Stats**")
            sw=df['slug_words']
            st.dataframe(pd.DataFrame({'Metric':['Min','Max','Mean','Median','Std'],'Value':[int(sw.min()),int(sw.max()),round(sw.mean(),1),round(sw.median(),1),round(sw.std(),1)]}),use_container_width=True,hide_index=True)
        with c3:
            st.markdown("**URL Length Buckets**")
            bins=[0,30,50,70,100,9999]; labels_b=['<30','30–50','50–70','70–100','>100']
            df['url_len_bucket']=pd.cut(df['url_length'],bins=bins,labels=labels_b)
            bc=df['url_len_bucket'].value_counts().reindex(labels_b,fill_value=0).reset_index()
            bc.columns=['Length Range','Count']
            st.dataframe(bc,use_container_width=True,hide_index=True)

        c1,c2=st.columns(2)
        with c1:
            fig=px.histogram(df,x='url_length',nbins=40,title='URL Character Length Distribution',color_discrete_sequence=['#a8ff78'])
            fig.update_layout(xaxis_title='Characters',yaxis_title='# URLs'); apply_theme(fig,False); st.plotly_chart(fig,use_container_width=True)
        with c2:
            fig=px.histogram(df,x='slug_words',nbins=20,title='Last Slug Word Count Distribution',color_discrete_sequence=['#78ffd6'])
            fig.update_layout(xaxis_title='Word Count',yaxis_title='# URLs'); apply_theme(fig,False); st.plotly_chart(fig,use_container_width=True)

        # Site structure overview — clear table + bar (replaces confusing sunburst/treemap)
        st.markdown('<div class="section-header">Site Structure Overview</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Top-level site sections ranked by URL count, with their top sub-sections shown</div>', unsafe_allow_html=True)
        if 'dir_1' in df.columns and df['dir_1'].notna().sum()>0:
            top_s=df['dir_1'].value_counts().head(15).reset_index()
            top_s.columns=['Section','Total URLs']
            top_s['% Share']=(top_s['Total URLs']/n_total*100).round(1).astype(str)+'%'
            if 'dir_2' in df.columns:
                subs=[]
                for d1 in top_s['Section']:
                    sub=df[df['dir_1']==d1]['dir_2'].value_counts().head(5)
                    subs.append(', '.join([f"{k}({v})" for k,v in sub.items()]) if len(sub)>0 else '—')
                top_s['Top Sub-sections']=subs
            st.dataframe(top_s,use_container_width=True,hide_index=True)
            fig=px.bar(top_s,x='Total URLs',y='Section',orientation='h',title='Top Site Sections by URL Count',color='Total URLs',color_continuous_scale='Teal',text='Total URLs')
            fig.update_layout(yaxis={'categoryorder':'total ascending'},coloraxis_showscale=False,height=500)
            apply_theme(fig,False); st.plotly_chart(fig,use_container_width=True)
    except Exception as e:
        st.error(f"URL Structure error: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# TAB 2  N-GRAM ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
with tabs[1]:
    try:
        full_tokens=df['loc'].apply(lambda u: tokenize_slug(urlparse(u).path)).tolist()
        slug_tokens=df['last_slug'].apply(tokenize_slug).tolist()
        ng_full=build_ngrams(full_tokens)
        ng_slug=build_ngrams(slug_tokens)
        st2=st.tabs(["Full URL Path","Last Slug Only"])
        for tab_obj,ng_dict,lbl in [(st2[0],ng_full,'Full URL'),(st2[1],ng_slug,'Last Slug')]:
            with tab_obj:
                st.markdown(f'<div class="section-sub">Words and phrases most common in {lbl}s — reveals competitor content strategy at a glance</div>', unsafe_allow_html=True)
                for ng_lbl,ng_df_item in ng_dict.items():
                    if ng_df_item.empty: continue
                    st.markdown(f'<div class="section-header">{ng_lbl}</div>', unsafe_allow_html=True)
                    top=ng_df_item.head(20).copy()
                    top['%']=(top['count']/top['count'].sum()*100).round(1).astype(str)+'%'
                    c1,c2=st.columns([3,2])
                    with c1:
                        fig=px.bar(top,x='count',y='ngram',orientation='h',title=f'Top 20 {ng_lbl} — {lbl}',color='count',color_continuous_scale='Teal')
                        fig.update_layout(yaxis={'categoryorder':'total ascending'},coloraxis_showscale=False,height=max(300,min(len(top)*28,550)))
                        apply_theme(fig,False); st.plotly_chart(fig,use_container_width=True)
                    with c2:
                        st.dataframe(top,use_container_width=True,hide_index=True,height=max(300,min(len(top)*35,550)))
    except Exception as e:
        st.error(f"N-gram error: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# TAB 3  TEMPORAL
# ═══════════════════════════════════════════════════════════════════════════
with tabs[2]:
    try:
        if n_with_date==0:
            st.info("No lastmod dates found in this sitemap. Temporal analysis not available.")
        else:
            dated=df[df['lastmod_dt'].notna()].copy()
            dated['year']=dated['lastmod_dt'].dt.year.astype(int)
            dated['month']=dated['lastmod_dt'].dt.to_period('M').astype(str)
            dated['quarter']=dated['lastmod_dt'].dt.to_period('Q').astype(str)
            dated['month_num']=dated['lastmod_dt'].dt.month

            st.markdown('<div class="section-header">Publishing Velocity (Monthly)</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-sub">Spikes reveal campaign activity. Flat lines reveal content stagnation — your opportunity.</div>', unsafe_allow_html=True)
            monthly=dated.groupby('month').size().reset_index(name='URLs Updated')
            monthly=monthly.sort_values('month')
            fig=px.line(monthly,x='month',y='URLs Updated',title='Monthly Publishing Velocity',markers=True,color_discrete_sequence=['#a8ff78'])
            fig.update_traces(line_width=2.5,marker_size=5); apply_theme(fig,False); st.plotly_chart(fig,use_container_width=True)

            c1,c2=st.columns(2)
            with c1:
                st.markdown('<div class="section-header">By Year</div>', unsafe_allow_html=True)
                yearly=dated.groupby('year').size().reset_index(name='Count'); yearly['year']=yearly['year'].astype(str)
                fig=px.bar(yearly,x='year',y='Count',text='Count',color='Count',color_continuous_scale='Teal',title='URLs Updated Per Year')
                fig.update_traces(textposition='outside',marker_line_width=0); fig.update_layout(coloraxis_showscale=False)
                apply_theme(fig,False); st.plotly_chart(fig,use_container_width=True)
                st.dataframe(yearly,use_container_width=True,hide_index=True)
            with c2:
                st.markdown('<div class="section-header">By Quarter (Last 12)</div>', unsafe_allow_html=True)
                quarterly=dated.groupby('quarter').size().reset_index(name='Count'); quarterly=quarterly.sort_values('quarter').tail(12)
                fig=px.bar(quarterly,x='quarter',y='Count',text='Count',color='Count',color_continuous_scale='Teal',title='URLs Updated Per Quarter')
                fig.update_traces(textposition='outside',marker_line_width=0); fig.update_layout(coloraxis_showscale=False)
                apply_theme(fig,False); st.plotly_chart(fig,use_container_width=True)
                st.dataframe(quarterly,use_container_width=True,hide_index=True)

            # Freshness
            st.markdown('<div class="section-header">Content Freshness Breakdown</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-sub">Large "Older than 1 Year" = stale competitor content = your content gap opportunity</div>', unsafe_allow_html=True)
            fo=['Last Week','Last Month','Last Quarter','Last Year','Older than 1 Year','No Date']
            fc=df['freshness'].value_counts().reindex(fo,fill_value=0).reset_index()
            fc.columns=['Freshness Bucket','URL Count']; fc['% of Total']=(fc['URL Count']/n_total*100).round(1).astype(str)+'%'
            c1,c2=st.columns([3,2])
            with c1:
                fig=px.bar(fc,x='Freshness Bucket',y='URL Count',text='URL Count',title='Content Freshness Distribution',
                           color='Freshness Bucket',color_discrete_sequence=['#a8ff78','#78ffd6','#7eb8ff','#ffd278','#ff7eb3','#555'])
                fig.update_traces(textposition='outside',marker_line_width=0,showlegend=False)
                apply_theme(fig,False); st.plotly_chart(fig,use_container_width=True)
            with c2:
                st.dataframe(fc,use_container_width=True,hide_index=True)

            # Heatmap
            st.markdown('<div class="section-header">Publishing Activity Heatmap</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-sub">Which month/year combinations are most active? Reveals seasonal editorial calendars.</div>', unsafe_allow_html=True)
            hm=dated.groupby(['year','month_num']).size().reset_index(name='count')
            hpivot=hm.pivot(index='year',columns='month_num',values='count').fillna(0)
            mn=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
            hpivot.columns=[mn[int(c)-1] for c in hpivot.columns]; hpivot.index=hpivot.index.astype(str)
            fig=px.imshow(hpivot,color_continuous_scale='Teal',title='Publishing Heatmap (Year × Month)',aspect='auto',text_auto=True)
            apply_theme(fig,False); st.plotly_chart(fig,use_container_width=True)

            # Directory velocity — stacked bar (clearer than spaghetti line)
            if 'dir_1' in df.columns and df['dir_1'].notna().sum()>0:
                st.markdown('<div class="section-header">Directory × Publishing Velocity</div>', unsafe_allow_html=True)
                st.markdown('<div class="section-sub">Which sections are actively growing vs. abandoned? Stacked monthly view by directory.</div>', unsafe_allow_html=True)
                d2=dated[dated['dir_1'].notna()].copy()
                top8=d2['dir_1'].value_counts().head(8).index.tolist()
                d2=d2[d2['dir_1'].isin(top8)]
                dm=d2.groupby(['dir_1','month']).size().reset_index(name='Count'); dm=dm.sort_values('month')
                fig=px.bar(dm,x='month',y='Count',color='dir_1',barmode='stack',title='Top 8 Directories — Monthly Update Activity')
                apply_theme(fig,True); st.plotly_chart(fig,use_container_width=True)
                piv=dm.pivot_table(index='month',columns='dir_1',values='Count',fill_value=0).sort_index().tail(12)
                st.markdown("**Last 12 Months — URLs Updated per Directory**")
                st.dataframe(piv,use_container_width=True)
    except Exception as e:
        st.error(f"Temporal error: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# TAB 4  ADVANCED EDA
# ═══════════════════════════════════════════════════════════════════════════
with tabs[3]:
    try:
        # Depth vs update rate — FIXED merge
        st.markdown('<div class="section-header">Depth vs Update Rate (Bivariate)</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Do deeper pages get updated less frequently? Indicates content maintenance patterns.</div>', unsafe_allow_html=True)
        if n_with_date>0:
            dm=safe_depth_freshness(df)
            if not dm.empty:
                dm=dm.rename(columns={'url_depth':'Depth','updated_count':'Updated','total':'Total','update_rate':'Update Rate %'})
                c1,c2=st.columns([3,2])
                with c1:
                    fig=px.bar(dm,x='Depth',y='Update Rate %',text='Update Rate %',title='Update Rate % by Depth Level',color='Update Rate %',color_continuous_scale='RdYlGn',hover_data=['Total','Updated'])
                    fig.update_traces(texttemplate='%{text:.0f}%',textposition='outside',marker_line_width=0)
                    fig.update_layout(coloraxis_showscale=False,xaxis=dict(tickmode='linear'))
                    apply_theme(fig,False); st.plotly_chart(fig,use_container_width=True)
                with c2:
                    disp=dm.copy(); disp['Update Rate %']=disp['Update Rate %'].astype(str)+'%'
                    st.dataframe(disp,use_container_width=True,hide_index=True)

        # URL Length vs Depth
        st.markdown('<div class="section-header">URL Length vs Depth (Bivariate)</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Unusually long shallow URLs may indicate keyword stuffing. Box plot shows spread at each level.</div>', unsafe_allow_html=True)
        c1,c2=st.columns([3,2])
        with c1:
            fig=px.box(df,x='url_depth',y='url_length',title='URL Length by Depth Level',color_discrete_sequence=['#a8ff78'])
            fig.update_layout(xaxis=dict(tickmode='linear')); apply_theme(fig,False); st.plotly_chart(fig,use_container_width=True)
        with c2:
            dl=df.groupby('url_depth')['url_length'].agg(['mean','median','min','max','count']).round(1).reset_index()
            dl.columns=['Depth','Avg','Median','Min','Max','Count']
            st.dataframe(dl,use_container_width=True,hide_index=True)

        # Stale content
        if 'dir_1' in df.columns and df['dir_1'].notna().sum()>0 and n_with_date>0:
            st.markdown('<div class="section-header">Stale Content by Directory</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-sub">Sections not updated in 2+ years = content gap opportunities for you to outrank</div>', unsafe_allow_html=True)
            two_yrs=now-timedelta(days=730)
            df['is_stale']=(df['lastmod_dt']<two_yrs)|df['lastmod_dt'].isna()
            sd=df[df['dir_1'].notna()].groupby('dir_1').agg(Total=('loc','count'),Stale=('is_stale','sum')).reset_index()
            sd['Stale %']=(sd['Stale']/sd['Total']*100).round(1); sd=sd.sort_values('Stale %',ascending=False).head(20)
            sd.columns=['Directory','Total URLs','Stale URLs','Stale %']
            c1,c2=st.columns([3,2])
            with c1:
                fig=px.bar(sd,x='Stale %',y='Directory',orientation='h',title='Stale Content % by Directory',color='Stale %',color_continuous_scale='RdYlGn_r',text='Stale %',hover_data=['Total URLs','Stale URLs'])
                fig.update_traces(texttemplate='%{text:.0f}%',textposition='outside')
                fig.update_layout(yaxis={'categoryorder':'total ascending'},coloraxis_showscale=False,height=500)
                apply_theme(fig,False); st.plotly_chart(fig,use_container_width=True)
            with c2:
                disp=sd.copy(); disp['Stale %']=disp['Stale %'].astype(str)+'%'
                st.dataframe(disp,use_container_width=True,hide_index=True)

        # Directory × Freshness multivariate
        if 'dir_1' in df.columns and df['dir_1'].notna().sum()>0:
            st.markdown('<div class="section-header">Directory × Freshness (Multivariate)</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-sub">Full freshness breakdown per directory — see which sections are growing, stable, or stagnating</div>', unsafe_allow_html=True)
            top10=df['dir_1'].value_counts().head(10).index
            mv=df[df['dir_1'].isin(top10)].groupby(['dir_1','freshness']).size().reset_index(name='Count')
            fo2=['Last Week','Last Month','Last Quarter','Last Year','Older than 1 Year','No Date']
            mv['freshness']=pd.Categorical(mv['freshness'],categories=fo2,ordered=True)
            mv=mv.sort_values(['dir_1','freshness'])
            fig=px.bar(mv,x='dir_1',y='Count',color='freshness',barmode='stack',title='Top 10 Directories — Freshness Breakdown',
                       color_discrete_map={'Last Week':'#a8ff78','Last Month':'#78ffd6','Last Quarter':'#7eb8ff','Last Year':'#ffd278','Older than 1 Year':'#ff7eb3','No Date':'#333'})
            fig.update_layout(xaxis_title='Directory',height=450); apply_theme(fig,True); st.plotly_chart(fig,use_container_width=True)
            pv=mv.pivot_table(index='dir_1',columns='freshness',values='Count',fill_value=0)
            st.markdown("**Directory × Freshness Table**"); st.dataframe(pv,use_container_width=True)

        # Priority
        if 'priority' in df.columns and df['priority'].notna().sum()>0:
            st.markdown('<div class="section-header">Priority Distribution</div>', unsafe_allow_html=True)
            df['priority_num']=pd.to_numeric(df['priority'],errors='coerce')
            c1,c2=st.columns(2)
            with c1:
                fig=px.histogram(df,x='priority_num',nbins=20,title='Priority Value Distribution',color_discrete_sequence=['#a8ff78'])
                apply_theme(fig,False); st.plotly_chart(fig,use_container_width=True)
            with c2:
                p=df['priority_num']
                st.dataframe(pd.DataFrame({'Metric':['Min','Max','Mean','Median'],'Value':[p.min(),p.max(),round(p.mean(),2),round(p.median(),2)]}),use_container_width=True,hide_index=True)
    except Exception as e:
        st.error(f"Advanced EDA error: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# TAB 5  RAW DATA
# ═══════════════════════════════════════════════════════════════════════════
with tabs[4]:
    try:
        st.markdown('<div class="section-header">Raw Sitemap Data</div>', unsafe_allow_html=True)
        display_cols=[c for c in ['loc','lastmod','changefreq','priority','url_depth','freshness','url_length'] if c in df.columns]
        st.dataframe(df[display_cols],use_container_width=True,height=480)
        st.download_button("⬇ Download CSV",df[display_cols].to_csv(index=False).encode('utf-8'),f"sitemap_{domain_name.replace('.','_')}.csv","text/csv")
        st.markdown('<div class="section-header">Summary Statistics</div>', unsafe_allow_html=True)
        summary=pd.DataFrame({'Metric':['Total URLs','Unique Domains','Avg URL Depth','Max URL Depth','Avg URL Length','URLs with Dates','Updated Last Week','Updated Last Month','Updated Last Quarter','Updated Last Year'],
                               'Value':[f"{n_total:,}",df['domain'].nunique(),avg_depth,max_depth,round(df['url_length'].mean(),1),f"{n_with_date:,}",f"{n_week:,}",f"{n_month:,}",f"{n_quarter:,}",f"{n_year:,}"]})
        st.dataframe(summary,use_container_width=True,hide_index=True)
    except Exception as e:
        st.error(f"Raw data error: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# TAB 6  EXPORT
# ═══════════════════════════════════════════════════════════════════════════
with tabs[5]:
    try:
        st.markdown('<div class="section-header">Download Report</div>', unsafe_allow_html=True)
        st.markdown("Download the HTML report → open in Chrome → **Cmd+P** → **Save as PDF**")

        def make_html():
            now_str=datetime.now().strftime('%Y-%m-%d %H:%M')
            rows_overview=''.join(f"<tr><td>{k}</td><td><strong>{v}</strong></td></tr>" for k,v in [
                ('Total URLs',f"{n_total:,}"),('Avg Depth',str(avg_depth)),('Max Depth',str(max_depth)),
                ('URLs with Dates',f"{n_with_date:,}"),('Updated Last Week',f"{n_week:,}"),
                ('Updated Last Month',f"{n_month:,}"),('Updated Last Quarter',f"{n_quarter:,}"),('Updated Last Year',f"{n_year:,}")])
            # Dir tables
            dir_html=""
            for level in range(1, min(max_depth+1,9)):
                col_name=f'dir_{level}'
                if col_name not in df.columns: break
                valid=df[col_name].dropna()
                if len(valid)==0: break
                vc=valid.value_counts().head(20).reset_index(); vc.columns=['Directory','URL Count']
                vc['% of Total']=(vc['URL Count']/n_total*100).round(2).astype(str)+'%'
                dir_html+=f"<h3>Level {level}</h3>"+vc.to_html(index=False,classes='data-table')
            # Ngrams
            ng_html=""
            all_tok=df['loc'].apply(lambda u: tokenize_slug(urlparse(u).path)).tolist()
            for lbl,ngdf in build_ngrams(all_tok).items():
                if ngdf.empty: continue
                ng_html+=f"<h3>{lbl}</h3>"+ngdf.head(20).to_html(index=False,classes='data-table')
            # Freshness
            fo3=['Last Week','Last Month','Last Quarter','Last Year','Older than 1 Year','No Date']
            fc2=df['freshness'].value_counts().reindex(fo3,fill_value=0).reset_index()
            fc2.columns=['Bucket','Count']; fc2['%']=(fc2['Count']/n_total*100).round(1).astype(str)+'%'

            return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sitemap Intelligence — {domain_name}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');
body{{font-family:'DM Sans',sans-serif;background:#06060f;color:#e8e6e0;max-width:1100px;margin:0 auto;padding:2rem 1.5rem}}
.author-block{{display:flex;align-items:center;gap:1rem;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.09);border-radius:14px;padding:1rem 1.2rem;margin-bottom:1.5rem}}
.author-block img{{width:56px;height:56px;border-radius:50%;border:2px solid rgba(168,255,120,0.5);object-fit:cover}}
.author-name{{font-family:'Syne',sans-serif;font-weight:700;font-size:1.05rem}}
.author-role{{color:#a8ff78;font-size:0.8rem;margin:0.15rem 0 0.3rem}}
.author-links a{{color:#888;font-size:0.78rem;margin-right:0.8rem;text-decoration:none}}
h1{{font-family:'Syne',sans-serif;font-size:2.2rem;background:linear-gradient(135deg,#a8ff78,#78ffd6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:0.2rem}}
h2{{font-family:'Syne',sans-serif;font-size:1.25rem;color:#a8ff78;border-left:3px solid #a8ff78;padding-left:0.7rem;margin-top:2.5rem}}
h3{{font-family:'Syne',sans-serif;font-size:1rem;color:#78ffd6;margin-top:1.4rem}}
.meta{{color:#555;font-size:0.85rem;margin-bottom:1.8rem}}
table.data-table{{width:100%;border-collapse:collapse;margin:0.7rem 0;font-size:0.86rem}}
table.data-table th{{background:rgba(168,255,120,0.1);color:#a8ff78;padding:0.5rem 0.7rem;text-align:left;font-family:'Syne',sans-serif;font-size:0.8rem;letter-spacing:0.04em}}
table.data-table td{{padding:0.42rem 0.7rem;border-bottom:1px solid rgba(255,255,255,0.05)}}
table.data-table tr:nth-child(even) td{{background:rgba(255,255,255,0.02)}}
.footer{{margin-top:3rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,0.06);color:#333;font-size:0.76rem;text-align:center}}
.footer a{{color:#444;text-decoration:none}}
@media print{{body{{background:#fff;color:#000}} h1,h2,h3{{-webkit-text-fill-color:unset;color:#1a1a2e}} .author-block{{background:#f5f5f5;border:1px solid #ddd}} table.data-table th{{background:#1a1a2e;color:#fff}}}}
</style></head><body>
<div class="author-block">
  <img src="https://media.licdn.com/dms/image/v2/D5603AQGhW9LkVEtd6A/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1707118558424?e=1747267200&v=beta&t=hQGM6jD4tCKJI1m8qjvMxBDt4S8wJ9c5MKlb0bBPMgE"
       onerror="this.src='https://ui-avatars.com/api/?name=SG&background=0d1a0d&color=a8ff78'" alt="Sankar">
  <div><div class="author-name">Sankar Gurumurthy</div>
  <div class="author-role">Head of AI SEO &amp; Marketing Data Scientist</div>
  <div class="author-links">
    <a href="https://www.linkedin.com/in/sankar-gurumurthy-a1044a136/">🔗 LinkedIn</a>
    <a href="https://github.com/sg-sankar">🐙 github.com/sg-sankar</a>
  </div></div>
</div>
<h1>Sitemap Intelligence Report</h1>
<p class="meta">Domain: <strong>{domain_name}</strong> &nbsp;|&nbsp; Generated: {now_str}</p>
<h2>Overview Metrics</h2>
<table class="data-table"><tr><th>Metric</th><th>Value</th></tr>{rows_overview}</table>
<h2>URL Depth Distribution</h2>
{df['url_depth'].value_counts().sort_index().reset_index().rename(columns={{'url_depth':'Depth Level','count':'URL Count'}}).to_html(index=False,classes='data-table')}
<h2>Directory Level Analysis</h2>{dir_html}
<h2>N-Gram Analysis (Full URL Path)</h2>{ng_html}
<h2>Content Freshness</h2>{fc2.to_html(index=False,classes='data-table')}
<div class="footer">Built by <a href="https://www.linkedin.com/in/sankar-gurumurthy-a1044a136/">Sankar Gurumurthy</a> · <a href="https://github.com/sg-sankar">github.com/sg-sankar</a> · Open source &amp; free forever</div>
</body></html>"""

        html_out=make_html()
        st.download_button("⬇ Download HTML Report",html_out.encode('utf-8'),f"sitemap_report_{domain_name.replace('.','_')}.html","text/html")
        st.markdown("<div style='color:#555;font-size:0.84rem;margin-top:0.4rem'>💡 Open in Chrome → Cmd+P → Save as PDF to get a PDF version</div>", unsafe_allow_html=True)
        st.markdown("---")
        display_cols2=[c for c in ['loc','lastmod','changefreq','priority','url_depth','freshness','url_length'] if c in df.columns]
        st.download_button("⬇ Download CSV",df[display_cols2].to_csv(index=False).encode('utf-8'),f"sitemap_{domain_name.replace('.','_')}.csv","text/csv")
    except Exception as e:
        st.error(f"Export error: {e}")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  Built by <a href="https://www.linkedin.com/in/sankar-gurumurthy-a1044a136/" target="_blank">Sankar Gurumurthy</a>
  &nbsp;·&nbsp; Head of AI SEO &amp; Marketing Data Scientist
  &nbsp;·&nbsp; <a href="https://github.com/sg-sankar" target="_blank">github.com/sg-sankar</a>
  <br><span style="color:#222;margin-top:0.25rem;display:block">Open source · Free forever · Powered by advertools + Streamlit</span>
</div>
""", unsafe_allow_html=True)
