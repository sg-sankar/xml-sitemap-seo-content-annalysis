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

st.set_page_config(page_title="Sitemap Copilot · Sankar Gurumurthy", page_icon="🛸", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');
*,*::before,*::after{box-sizing:border-box}
html,body,[data-testid="stAppViewContainer"]{background:#080810;color:#e2e0f0;font-family:'Inter',sans-serif}
[data-testid="stAppViewContainer"]{background:radial-gradient(ellipse 80% 50% at 10% 0%,rgba(99,60,255,0.15) 0%,transparent 60%),radial-gradient(ellipse 60% 40% at 90% 10%,rgba(0,200,150,0.1) 0%,transparent 50%),#080810}
[data-testid="stHeader"]{background:transparent}
h1,h2,h3,h4{font-family:'Syne',sans-serif}
.hero{text-align:center;padding:2.5rem 1rem 1rem}
.hero-eyebrow{font-size:0.75rem;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:#7c6aff;background:rgba(124,106,255,0.1);border:1px solid rgba(124,106,255,0.25);display:inline-block;padding:0.3rem 1rem;border-radius:100px;margin-bottom:1rem}
.hero-title{font-family:'Syne',sans-serif;font-size:clamp(3rem,7vw,6rem);font-weight:800;line-height:1;letter-spacing:-0.03em;margin-bottom:0.5rem;background:linear-gradient(135deg,#ffffff 0%,#a78bfa 40%,#34d399 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero-tagline{font-size:1.1rem;color:#6b7280;font-weight:400;max-width:500px;margin:0 auto 2rem;line-height:1.6}
.author-card{display:inline-flex;align-items:center;gap:1rem;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);backdrop-filter:blur(20px);border-radius:100px;padding:0.6rem 1.2rem 0.6rem 0.6rem;margin-bottom:2rem}
.author-photo{width:44px;height:44px;border-radius:50%;border:2px solid rgba(124,106,255,0.4);object-fit:cover;flex-shrink:0}
.author-name{font-family:'Syne',sans-serif;font-size:0.92rem;font-weight:700;color:#e2e0f0}
.author-role{font-size:0.72rem;color:#7c6aff}
.author-links{display:flex;gap:0.4rem;margin-top:0.25rem}
.author-links a{font-size:0.68rem;color:#6b7280;text-decoration:none;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.08);padding:0.15rem 0.5rem;border-radius:100px}
.metric-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:0.75rem;margin:1.5rem 0}
.metric-card{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.2rem;position:relative;overflow:hidden}
.metric-card::before{content:"";position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(124,106,255,0.3),transparent)}
.metric-num{font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:#a78bfa;line-height:1}
.metric-label{font-size:0.7rem;color:#4b5563;text-transform:uppercase;letter-spacing:0.08em;margin-top:0.3rem}
.metric-sub{font-size:0.72rem;color:#374151;margin-top:0.2rem}
.section-hdr{font-family:'Syne',sans-serif;font-size:1.15rem;font-weight:700;color:#e2e0f0;margin:1.8rem 0 0.3rem;display:flex;align-items:center;gap:0.6rem}
.section-hdr::before{content:"";display:inline-block;width:3px;height:1.1rem;background:linear-gradient(180deg,#7c6aff,#34d399);border-radius:2px;flex-shrink:0}
.section-sub{font-size:0.78rem;color:#4b5563;margin:0 0 0.8rem 0.9rem;font-style:italic}
.insight-box{background:rgba(52,211,153,0.06);border:1px solid rgba(52,211,153,0.2);border-radius:12px;padding:0.8rem 1rem;margin:0.5rem 0 1rem;font-size:0.82rem;color:#34d399}
.warning-box{background:rgba(239,68,68,0.06);border:1px solid rgba(239,68,68,0.2);border-radius:12px;padding:0.8rem 1rem;margin:0.5rem 0 1rem;font-size:0.82rem;color:#ef4444}
.stTextInput>div>div>input{background:rgba(255,255,255,0.04)!important;border:1px solid rgba(255,255,255,0.1)!important;border-radius:14px!important;color:#e2e0f0!important;font-size:0.95rem!important;padding:0.75rem 1.1rem!important}
.stTextInput>div>div>input:focus{border-color:rgba(124,106,255,0.5)!important;box-shadow:0 0 0 3px rgba(124,106,255,0.1)!important}
.stButton>button{background:linear-gradient(135deg,#7c6aff,#4f46e5)!important;color:#fff!important;font-family:'Syne',sans-serif!important;font-weight:700!important;font-size:0.9rem!important;border:none!important;border-radius:14px!important;padding:0.75rem 1.5rem!important;width:100%!important;box-shadow:0 4px 20px rgba(124,106,255,0.3)!important}
.stTabs [data-baseweb="tab-list"]{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:14px;padding:4px;gap:2px}
.stTabs [data-baseweb="tab"]{font-family:'Syne',sans-serif!important;font-weight:600!important;color:#4b5563!important;border-radius:10px!important;padding:0.4rem 1rem!important;font-size:0.85rem!important}
.stTabs [aria-selected="true"]{background:rgba(124,106,255,0.15)!important;color:#a78bfa!important}
.stDownloadButton>button{background:rgba(52,211,153,0.08)!important;color:#34d399!important;border:1px solid rgba(52,211,153,0.2)!important;font-family:'Syne',sans-serif!important;font-weight:600!important;border-radius:10px!important}
.footer{text-align:center;padding:3rem 1rem 1.5rem;color:#1f2937;font-size:0.78rem;border-top:1px solid rgba(255,255,255,0.04);margin-top:4rem}
.footer a{color:#374151;text-decoration:none}
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────
PCFG = dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
            font_color="#6b7280",font_family="Inter",
            title_font_family="Syne",title_font_size=13,title_font_color="#e2e0f0",
            colorway=["#7c6aff","#34d399","#f59e0b","#ef4444","#3b82f6","#ec4899"])

def ap(fig,legend=False):
    fig.update_layout(**PCFG,showlegend=legend)
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.04)",linecolor="rgba(255,255,255,0.06)",zeroline=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.04)",linecolor="rgba(255,255,255,0.06)",zeroline=False)
    return fig

def sh(text,sub=None,insight=None,warning=None):
    st.markdown(f'<div class="section-hdr">{text}</div>',unsafe_allow_html=True)
    if sub: st.markdown(f'<div class="section-sub">{sub}</div>',unsafe_allow_html=True)
    if insight: st.markdown(f'<div class="insight-box">💡 {insight}</div>',unsafe_allow_html=True)
    if warning: st.markdown(f'<div class="warning-box">⚠️ {warning}</div>',unsafe_allow_html=True)

def tokenize(slug):
    s=re.sub(r"[_\-]"," ",str(slug).lower())
    s=re.sub(r"[^a-z0-9 ]","",s)
    return [t for t in s.split() if t and len(t)>1]

def build_ngrams(all_tokens,max_n=5):
    labels={1:"Unigrams",2:"Bigrams",3:"Trigrams",4:"4-grams",5:"5-grams"}
    out={}
    for n in range(1,max_n+1):
        grams=[]
        for toks in all_tokens:
            grams.extend([" ".join(toks[i:i+n]) for i in range(len(toks)-n+1)])
        out[labels[n]]=pd.DataFrame(Counter(grams).most_common(30),columns=["ngram","count"])
    return out

def clean_df(df_in):
    return df_in.loc[:,~df_in.columns.duplicated()].copy()

def get_display_cols(df_in):
    wanted=["loc","lastmod","changefreq","priority","url_depth","freshness","url_length"]
    df_c=clean_df(df_in)
    return [c for c in wanted if c in df_c.columns]

# ── Hero ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-eyebrow">AI-Powered SEO Intelligence</div>
  <div class="hero-title">Sitemap Copilot</div>
  <div class="hero-tagline">See everything your competitor is hiding in plain sight</div>
  <div class="author-card">
    <img class="author-photo" src="data:image/png;base64,{PHOTO_B64}" alt="Sankar">
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
""",unsafe_allow_html=True)

c1,c2=st.columns([5,1])
with c1:
    input_url=st.text_input("",placeholder="Paste robots.txt or sitemap.xml URL…",label_visibility="collapsed")
with c2:
    st.markdown("<div style='padding-top:0.1rem'></div>",unsafe_allow_html=True)
    run=st.button("Analyse →")

if not run or not input_url.strip():
    st.markdown("<div style='text-align:center;padding:4rem;color:#1f2937;font-size:0.85rem'>Supports <b style='color:#374151'>robots.txt</b> · <b style='color:#374151'>sitemap.xml</b> · <b style='color:#374151'>sitemap index</b> · <b style='color:#374151'>nested &amp; gzipped</b></div>",unsafe_allow_html=True)
    st.stop()

# ── Fetch with rate-limit protection ─────────────────────────────────
def extract_sitemaps_from_robots(url):
    try:
        r=requests.get(url,timeout=15,headers={"User-Agent":"SitemapCopilot/1.0"})
        r.raise_for_status()
        return [s.strip() for s in re.findall(r"(?i)^Sitemap:\s*(.+)",r.text,re.MULTILINE)]
    except: return []

def fetch_one(url):
    for attempt in range(3):
        try:
            return adv.sitemap_to_df(url),None
        except Exception as e:
            if "429" in str(e) and attempt<2:
                time.sleep(3+attempt*2)
            else:
                return None,str(e)
    return None,"Max retries exceeded"

sitemap_urls=extract_sitemaps_from_robots(input_url.strip()) if "robots.txt" in input_url.lower() else [input_url.strip()]
if not sitemap_urls: st.error("No sitemaps found."); st.stop()

progress_bar=st.progress(0,text="🛸 Copilot scanning…")
all_dfs,errors=[],[]
total=len(sitemap_urls)

for idx,su in enumerate(sitemap_urls):
    progress_bar.progress(max(1,int(idx/total*100)),text=f"🛸 Fetching {idx+1} of {total}…")
    df_part,err=fetch_one(su)
    if df_part is not None: all_dfs.append(df_part)
    else: errors.append(f"{su}: {err}")
    if idx<total-1: time.sleep(1)

progress_bar.progress(100,text="✅ Done!")
time.sleep(0.4)
progress_bar.empty()

if not all_dfs: st.error("Failed to fetch.\n"+"\n".join(errors)); st.stop()

df=pd.concat(all_dfs,ignore_index=True)
df=clean_df(df)
if "loc" not in df.columns: st.error("No URLs found."); st.stop()
df=df.drop_duplicates("loc")
df=df[df["loc"].notna()&df["loc"].str.startswith("http")].reset_index(drop=True)
df["lastmod_dt"]=pd.to_datetime(df.get("lastmod",pd.Series(dtype=str)),errors="coerce",utc=True)
df["url_parts"]=df["loc"].apply(lambda u:[p for p in urlparse(u).path.rstrip("/").split("/") if p])
df["url_depth"]=df["url_parts"].apply(len)
df["last_slug"]=df["url_parts"].apply(lambda x:x[-1] if x else "")
df["domain"]=df["loc"].apply(lambda u:urlparse(u).netloc)
df["url_length"]=df["loc"].apply(len)
df["slug_words"]=df["last_slug"].apply(lambda s:len(re.findall(r"[a-zA-Z0-9]+",str(s))))
max_depth=int(df["url_depth"].max()) if len(df) else 1
for i in range(1,min(max_depth+1,9)):
    df[f"dir_{i}"]=df["url_parts"].apply(lambda x,i=i:x[i-1] if len(x)>=i else None)

now=pd.Timestamp.now(tz="UTC")
lw=now-timedelta(days=7);lm=now-timedelta(days=30)
lq=now-timedelta(days=90);ly=now-timedelta(days=365)
n_total=len(df);n_dates=int(df["lastmod_dt"].notna().sum())
n_week=int((df["lastmod_dt"]>=lw).sum());n_month=int((df["lastmod_dt"]>=lm).sum())
n_quarter=int((df["lastmod_dt"]>=lq).sum());n_year=int((df["lastmod_dt"]>=ly).sum())
avg_depth=round(df["url_depth"].mean(),1);domain_name=df["domain"].iloc[0] if len(df) else "Unknown"

def fb(dt):
    if pd.isna(dt): return "No Date"
    if dt>=lw: return "Last Week"
    if dt>=lm: return "Last Month"
    if dt>=lq: return "Last Quarter"
    if dt>=ly: return "Last Year"
    return "Older than 1 Year"
df["freshness"]=df["lastmod_dt"].apply(fb)

# ── Metric cards ──────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;color:#374151;font-size:0.78rem;margin-bottom:0.5rem">
🛸 Analysing: <strong style="color:#4b5563">{domain_name}</strong>
</div>
<div class="metric-grid">
  <div class="metric-card" style="grid-column:span 2">
    <div class="metric-label">Total URLs Discovered</div>
    <div class="metric-num" style="font-size:3rem;color:#34d399">{n_total:,}</div>
    <div class="metric-sub">Avg depth {avg_depth} · Max depth {max_depth}</div>
  </div>
  <div class="metric-card"><div class="metric-label">Have Dates</div><div class="metric-num">{n_dates:,}</div></div>
  <div class="metric-card"><div class="metric-label">Last Week</div><div class="metric-num">{n_week:,}</div></div>
  <div class="metric-card"><div class="metric-label">Last Month</div><div class="metric-num">{n_month:,}</div></div>
  <div class="metric-card"><div class="metric-label">Last Quarter</div><div class="metric-num">{n_quarter:,}</div></div>
  <div class="metric-card"><div class="metric-label">Last Year</div><div class="metric-num">{n_year:,}</div></div>
  <div class="metric-card"><div class="metric-label">Avg URL Length</div><div class="metric-num">{round(df["url_length"].mean(),0):.0f}</div><div class="metric-sub">characters</div></div>
</div>
""",unsafe_allow_html=True)

if errors:
    with st.expander(f"⚠️ {len(errors)} sitemap(s) had errors"):
        for e in errors: st.text(e)

tabs=st.tabs(["🏗 URL Structure","🌳 Site Hierarchy","📝 N-Grams","📅 Temporal","🔬 Advanced EDA","📋 Raw Data","📥 Export"])

# ═══════════════════════════════════════════════
# TAB 1  URL STRUCTURE
# ═══════════════════════════════════════════════
with tabs[0]:
    try:
        sh("URL Depth Distribution","How many directory levels deep are the pages?")
        dc=df["url_depth"].value_counts().sort_index().reset_index()
        dc.columns=["Depth Level","URL Count"]
        dc["% of Total"]=(dc["URL Count"]/n_total*100).round(2).astype(str)+"%"
        dc["Cumulative %"]=(dc["URL Count"].cumsum()/n_total*100).round(1).astype(str)+"%"
        c1,c2=st.columns([2,3])
        with c1:
            st.dataframe(dc,use_container_width=True,hide_index=True)
        with c2:
            fig=px.bar(dc,x="Depth Level",y="URL Count",text="URL Count",color="URL Count",
                       color_continuous_scale="Purp",title="URLs by Depth Level")
            fig.update_traces(textposition="outside",marker_line_width=0)
            fig.update_layout(coloraxis_showscale=False,xaxis=dict(tickmode="linear"))
            ap(fig,False);st.plotly_chart(fig,use_container_width=True)

        sh("URL Length Analysis","Shorter URLs are cleaner for SEO. Long slugs dilute keyword signal.")
        c1,c2,c3=st.columns(3)
        ul=df["url_length"];sw=df["slug_words"]
        with c1:
            st.markdown("**URL Character Length**")
            st.dataframe(pd.DataFrame({"Metric":["Min","Max","Mean","Median","Std"],
                "Value":[int(ul.min()),int(ul.max()),round(ul.mean(),1),round(ul.median(),1),round(ul.std(),1)]}),
                use_container_width=True,hide_index=True)
        with c2:
            st.markdown("**Last Slug Word Count**")
            st.dataframe(pd.DataFrame({"Metric":["Min","Max","Mean","Median","Std"],
                "Value":[int(sw.min()),int(sw.max()),round(sw.mean(),1),round(sw.median(),1),round(sw.std(),1)]}),
                use_container_width=True,hide_index=True)
        with c3:
            st.markdown("**URL Length Buckets**")
            bins=[0,30,50,70,100,9999];lb=["<30","30-50","50-70","70-100",">100"]
            df["ul_b"]=pd.cut(df["url_length"],bins=bins,labels=lb)
            bc=df["ul_b"].value_counts().reindex(lb,fill_value=0).reset_index()
            bc.columns=["Length Range","Count"]
            bc["% of Total"]=(bc["Count"]/n_total*100).round(1).astype(str)+"%"
            st.dataframe(bc,use_container_width=True,hide_index=True)

        c1,c2=st.columns(2)
        with c1:
            fig=px.histogram(df,x="url_length",nbins=40,title="URL Character Length Distribution",
                             color_discrete_sequence=["#7c6aff"])
            fig.update_layout(xaxis_title="Characters",yaxis_title="# URLs")
            ap(fig,False);st.plotly_chart(fig,use_container_width=True)
        with c2:
            fig=px.histogram(df,x="slug_words",nbins=20,title="Last Slug Word Count Distribution",
                             color_discrete_sequence=["#34d399"])
            fig.update_layout(xaxis_title="Word Count",yaxis_title="# URLs")
            ap(fig,False);st.plotly_chart(fig,use_container_width=True)

        sh("Site Structure Summary","Top sections ranked by URL count with freshness and depth")
        if "dir_1" in df.columns and df["dir_1"].notna().sum()>0:
            top_s=df["dir_1"].value_counts().reset_index()
            top_s.columns=["Section","Total URLs"]
            top_s["% Share"]=(top_s["Total URLs"]/n_total*100).round(2).astype(str)+"%"
            avg_d=df[df["dir_1"].notna()].groupby("dir_1")["url_depth"].mean().round(1).reset_index()
            avg_d.columns=["Section","Avg Depth"]
            top_s=top_s.merge(avg_d,on="Section",how="left")
            def dom_fresh(d1):
                sub=df[df["dir_1"]==d1]["freshness"]
                return sub.value_counts().index[0] if len(sub)>0 else "—"
            top_s["Dominant Freshness"]=top_s["Section"].apply(dom_fresh)
            if "dir_2" in df.columns:
                def top_sub(d1):
                    sub=df[df["dir_1"]==d1]["dir_2"].dropna().value_counts().head(3)
                    return ", ".join([f"{k}({v})" for k,v in sub.items()]) if len(sub)>0 else "leaf pages"
                top_s["Top Sub-sections"]=top_s["Section"].apply(top_sub)
            st.dataframe(top_s,use_container_width=True,hide_index=True)

    except Exception as e:
        st.error(f"URL Structure error: {e}")

# ═══════════════════════════════════════════════
# TAB 2  SITE HIERARCHY TREE
# ═══════════════════════════════════════════════
with tabs[1]:
    try:
        sh("Site Hierarchy Tree",
           "Root → Section → Sub-section → Slug with URL counts at every level",
           insight="Wide shallow trees = topic authority strategy. Deep narrow trees = long-tail SEO strategy. Compare this to your own site architecture.")

        @st.cache_data(show_spinner=False)
        def build_tree(parts_tuple):
            tree={"__count__":len(parts_tuple)}
            for parts in parts_tuple:
                node=tree
                for part in parts:
                    if part not in node:
                        node[part]={"__count__":0}
                    node[part]["__count__"]+=1
                    node=node[part]
            return tree

        parts_tuple=tuple(map(tuple,df["url_parts"].tolist()))
        tree=build_tree(parts_tuple)

        def render_tree(node,prefix="",depth=0,max_d=8,min_c=1):
            rows=[]
            children=[(k,v) for k,v in node.items() if k!="__count__"]
            children.sort(key=lambda x:x[1].get("__count__",0),reverse=True)
            for i,(key,val) in enumerate(children):
                count=val.get("__count__",0)
                if count<min_c: continue
                pct=round(count/n_total*100,2)
                is_last=(i==len([c for c in children if c[1].get("__count__",0)>=min_c])-1)
                connector="└── " if is_last else "├── "
                sub_children=[(k,v) for k,v in val.items() if k!="__count__"]
                icon="📄" if not sub_children else ("📁" if depth==0 else "📂")
                rows.append({"Tree":f"{prefix}{connector}{icon} {key}",
                              "URLs":f"{count:,}","% of Site":f"{pct}%",
                              "_depth":depth,"_count":count})
                if depth<max_d and sub_children:
                    child_prefix=prefix+("    " if is_last else "│   ")
                    rows.extend(render_tree(val,child_prefix,depth+1,max_d,min_c))
            return rows

        c1,c2,c3=st.columns(3)
        with c1: max_d=st.slider("Max depth",1,min(max_depth,8),min(4,max_depth))
        with c2: min_c=st.number_input("Min URLs per node",min_value=1,value=1,step=1)
        with c3: search_tree=st.text_input("🔍 Filter",placeholder="e.g. blog")

        root_count=tree.get("__count__",n_total)
        st.markdown(f'<div style="font-family:monospace;font-size:0.85rem;padding:0.4rem 0.5rem;color:#34d399;font-weight:700">🌐 {domain_name} — {root_count:,} URLs (100%)</div>',unsafe_allow_html=True)

        rows=render_tree(tree,"",0,int(max_d),int(min_c))
        if search_tree:
            rows=[r for r in rows if search_tree.lower() in r["Tree"].lower()]

        if rows:
            tree_df=pd.DataFrame(rows)[["Tree","URLs","% of Site"]]
            st.dataframe(tree_df,use_container_width=True,hide_index=True,height=600)
            st.markdown(f"<div style='color:#4b5563;font-size:0.78rem'>Showing {len(rows):,} nodes · Depth ≤{max_d} · Min {min_c} URL(s) per node</div>",unsafe_allow_html=True)
        else:
            st.info("No nodes match your filter.")

    except Exception as e:
        st.error(f"Hierarchy error: {e}")

# ═══════════════════════════════════════════════
# TAB 3  N-GRAMS
# ═══════════════════════════════════════════════
with tabs[2]:
    try:
        full_tokens=df["loc"].apply(lambda u:tokenize(urlparse(u).path)).tolist()
        slug_tokens=df["last_slug"].apply(tokenize).tolist()
        ng_full=build_ngrams(full_tokens)
        ng_slug=build_ngrams(slug_tokens)
        st2=st.tabs(["Full URL Path","Last Slug Only"])
        for tab_obj,ng_dict,lbl in [(st2[0],ng_full,"Full URL"),(st2[1],ng_slug,"Last Slug")]:
            with tab_obj:
                st.markdown(f'<div class="section-sub">Most frequent words and phrases in {lbl}s — reveals competitor content strategy and topic clusters</div>',unsafe_allow_html=True)
                for ng_lbl,ng_df_item in ng_dict.items():
                    if ng_df_item.empty: continue
                    sh(ng_lbl)
                    top=ng_df_item.head(20).copy()
                    top["%"]=(top["count"]/top["count"].sum()*100).round(1).astype(str)+"%"
                    c1,c2=st.columns([3,2])
                    with c1:
                        # Sort ascending so largest bar is at TOP (matches table row 1)
                        fig=px.bar(top.sort_values("count",ascending=True),
                                   x="count",y="ngram",orientation="h",
                                   title=f"Top 20 {ng_lbl}",
                                   color="count",color_continuous_scale="Purp")
                        fig.update_layout(coloraxis_showscale=False,
                                          height=max(300,min(len(top)*30,550)))
                        ap(fig,False);st.plotly_chart(fig,use_container_width=True)
                    with c2:
                        st.dataframe(top,use_container_width=True,hide_index=True,
                                     height=max(300,min(len(top)*35,550)))
    except Exception as e:
        st.error(f"N-gram error: {e}")

# ═══════════════════════════════════════════════
# TAB 4  TEMPORAL
# ═══════════════════════════════════════════════
with tabs[3]:
    try:
        if n_dates==0:
            st.info("No lastmod dates found. Temporal analysis not available.")
        else:
            dated=df[df["lastmod_dt"].notna()].copy()
            dated["year"]=dated["lastmod_dt"].dt.year.astype(int)
            dated["month"]=dated["lastmod_dt"].dt.to_period("M").astype(str)
            dated["quarter"]=dated["lastmod_dt"].dt.to_period("Q").astype(str)
            dated["month_num"]=dated["lastmod_dt"].dt.month

            sh("Publishing Velocity (Monthly)","Spikes = campaign bursts. Gaps = neglect = your opportunity.",
               insight="Compare their publishing pace to yours. If they publish 50/month and you publish 5, hyper-focus on their weakest/stalest sections instead of competing head-on.")
            monthly=dated.groupby("month").size().reset_index(name="URLs Updated").sort_values("month")
            fig=px.line(monthly,x="month",y="URLs Updated",title="Monthly Publishing Velocity",
                        markers=True,color_discrete_sequence=["#7c6aff"])
            fig.update_traces(line_width=2.5,marker_size=5)
            ap(fig,False);st.plotly_chart(fig,use_container_width=True)

            c1,c2=st.columns(2)
            with c1:
                sh("By Year")
                yearly=dated.groupby("year").size().reset_index(name="Count")
                yearly["year"]=yearly["year"].astype(str)
                fig=px.bar(yearly,x="year",y="Count",text="Count",color="Count",
                           color_continuous_scale="Purp",title="URLs Updated Per Year")
                fig.update_traces(textposition="outside",marker_line_width=0)
                fig.update_layout(coloraxis_showscale=False)
                ap(fig,False);st.plotly_chart(fig,use_container_width=True)
                st.dataframe(yearly,use_container_width=True,hide_index=True)
            with c2:
                sh("By Quarter (Last 12)")
                quarterly=dated.groupby("quarter").size().reset_index(name="Count")
                quarterly=quarterly.sort_values("quarter").tail(12)
                fig=px.bar(quarterly,x="quarter",y="Count",text="Count",color="Count",
                           color_continuous_scale="Purp",title="URLs Per Quarter")
                fig.update_traces(textposition="outside",marker_line_width=0)
                fig.update_layout(coloraxis_showscale=False)
                ap(fig,False);st.plotly_chart(fig,use_container_width=True)
                st.dataframe(quarterly,use_container_width=True,hide_index=True)

            sh("Content Freshness Breakdown","What % of their site is stale?",
               insight="If >50% of their content is older than 1 year, Google may be deprioritising their freshness signals. Publish fresher content on the same topics to outrank them.")
            fo=["Last Week","Last Month","Last Quarter","Last Year","Older than 1 Year","No Date"]
            fc=df["freshness"].value_counts().reindex(fo,fill_value=0).reset_index()
            fc.columns=["Freshness Bucket","URL Count"]
            fc["% of Total"]=(fc["URL Count"]/n_total*100).round(1).astype(str)+"%"
            c1,c2=st.columns([3,2])
            with c1:
                fig=px.bar(fc,x="Freshness Bucket",y="URL Count",text="URL Count",
                           title="Content Freshness Distribution",color="Freshness Bucket",
                           color_discrete_sequence=["#34d399","#7c6aff","#3b82f6","#f59e0b","#ef4444","#374151"])
                fig.update_traces(textposition="outside",marker_line_width=0,showlegend=False)
                ap(fig,False);st.plotly_chart(fig,use_container_width=True)
            with c2:
                st.dataframe(fc,use_container_width=True,hide_index=True)

            sh("Publishing Heatmap","Seasonal patterns and editorial calendar revealed",
               insight="Dark months = competitor doesn't publish then. That's when YOU should publish — same search demand, less competition.")
            hm=dated.groupby(["year","month_num"]).size().reset_index(name="count")
            hpivot=hm.pivot(index="year",columns="month_num",values="count").fillna(0)
            mn=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
            hpivot.columns=[mn[int(c)-1] for c in hpivot.columns]
            hpivot.index=hpivot.index.astype(str)
            fig=px.imshow(hpivot,color_continuous_scale="Purp",
                          title="Publishing Heatmap (Year × Month)",aspect="auto",text_auto=True)
            ap(fig,False);st.plotly_chart(fig,use_container_width=True)

            if "dir_1" in df.columns and df["dir_1"].notna().sum()>0:
                sh("Section Publishing Velocity","Which sections are growing vs abandoned?")
                d2=dated[dated["dir_1"].notna()].copy()
                top8=d2["dir_1"].value_counts().head(8).index.tolist()
                d2=d2[d2["dir_1"].isin(top8)]
                dm=d2.groupby(["dir_1","month"]).size().reset_index(name="Count").sort_values("month")
                fig=px.bar(dm,x="month",y="Count",color="dir_1",barmode="stack",
                           title="Top 8 Sections — Monthly Update Activity")
                ap(fig,True);st.plotly_chart(fig,use_container_width=True)
                piv=dm.pivot_table(index="month",columns="dir_1",values="Count",fill_value=0).sort_index().tail(12)
                st.dataframe(piv,use_container_width=True)

    except Exception as e:
        st.error(f"Temporal error: {e}")

# ═══════════════════════════════════════════════
# TAB 5  ADVANCED EDA
# ═══════════════════════════════════════════════
with tabs[4]:
    try:
        # URL Depth vs Content Recency
        sh("URL Depth vs Content Recency",
           "How stale are pages at each depth level?",
           insight="Pages deeper than level 3 AND older than 365 days are being ignored by both the site owner and Google. Create shallower, fresher versions of the same content to outrank them.")
        if n_dates>0:
            dated2=df[df["lastmod_dt"].notna()].copy()
            dated2["days_ago"]=(now-dated2["lastmod_dt"]).dt.days
            rec=dated2.groupby("url_depth")["days_ago"].mean().round(0).reset_index()
            rec.columns=["Depth Level","Avg Days Since Update"]
            tot=df.groupby("url_depth").size().reset_index(name="Total URLs")
            rec=rec.merge(tot,on="Depth Level",how="outer").fillna(0)
            rec["Avg Days Since Update"]=rec["Avg Days Since Update"].astype(int)
            rec=rec.sort_values("Depth Level")
            rec["SEO Risk"]=rec.apply(
                lambda r:"🔴 Stale+Deep — easy target" if r["Depth Level"]>=3 and r["Avg Days Since Update"]>365
                else("🟡 Monitor" if r["Avg Days Since Update"]>180 else "🟢 Fresh"),axis=1)
            c1,c2=st.columns([2,3])
            with c1:
                st.dataframe(rec,use_container_width=True,hide_index=True)
            with c2:
                fig=px.bar(rec,x="Depth Level",y="Avg Days Since Update",
                           title="Avg Days Since Update by Depth (Higher = More Stale)",
                           color="Avg Days Since Update",color_continuous_scale="RdYlGn_r",
                           text="Avg Days Since Update",hover_data=["Total URLs"])
                fig.update_traces(textposition="outside",marker_line_width=0)
                fig.update_layout(coloraxis_showscale=False,xaxis=dict(tickmode="linear"))
                ap(fig,False);st.plotly_chart(fig,use_container_width=True)

        # URL Length vs Depth
        sh("URL Length vs Depth",
           "Does URL length grow with depth?",
           insight="Pages at depth 1-2 with URLs longer than 70 characters = possible keyword stuffing or poor URL hygiene. Google recommends short descriptive URLs — these may be suppressed in rankings.")
        risky=df[(df["url_depth"]<=2)&(df["url_length"]>70)]
        if len(risky)>0:
            st.markdown(f'<div class="warning-box">⚠️ {len(risky):,} shallow pages (depth ≤2) have URLs longer than 70 chars — potential keyword stuffing or poor URL hygiene</div>',unsafe_allow_html=True)
        c1,c2=st.columns([3,2])
        with c1:
            fig=px.box(df,x="url_depth",y="url_length",
                       title="URL Length Distribution by Depth Level",
                       color_discrete_sequence=["#7c6aff"])
            fig.update_layout(xaxis=dict(tickmode="linear"))
            ap(fig,False);st.plotly_chart(fig,use_container_width=True)
        with c2:
            dl=df.groupby("url_depth")["url_length"].agg(["mean","median","min","max","count"]).round(1).reset_index()
            dl.columns=["Depth","Avg","Median","Min","Max","Count"]
            st.dataframe(dl,use_container_width=True,hide_index=True)

        # Content Gap Opportunities
        if "dir_1" in df.columns and df["dir_1"].notna().sum()>0 and n_dates>0:
            sh("Content Gap Opportunities",
               "Where is your competitor sleeping?",
               insight="High Opportunity Score = many URLs + high stale % = competitor invested here but stopped maintaining. Publish fresher, deeper content on the same topics to outrank them.")
            two_yrs=now-timedelta(days=730)
            df_gap=df.copy()
            df_gap["is_stale"]=(df_gap["lastmod_dt"]<two_yrs)|df_gap["lastmod_dt"].isna()
            dated3=df_gap[df_gap["dir_1"].notna()&df_gap["lastmod_dt"].notna()].copy()
            dated3["days_ago"]=(now-dated3["lastmod_dt"]).dt.days
            avg_days=dated3.groupby("dir_1")["days_ago"].mean().round(0).reset_index()
            avg_days.columns=["dir_1","Avg Days Since Update"]
            sd=df_gap[df_gap["dir_1"].notna()].groupby("dir_1").agg(
                Total=("loc","count"),Stale=("is_stale","sum")).reset_index()
            sd["Stale %"]=(sd["Stale"]/sd["Total"]*100).round(1)
            sd=sd.merge(avg_days,on="dir_1",how="left")
            sd["Opportunity Score"]=(sd["Stale %"]*sd["Total"]/100).round(0).astype(int)
            sd=sd.sort_values("Opportunity Score",ascending=False).head(20)
            sd.columns=["Section","Total URLs","Stale URLs","Stale %","Avg Days Since Update","Opportunity Score"]
            st.dataframe(sd,use_container_width=True,hide_index=True)

        # Section × Freshness
        if "dir_1" in df.columns and df["dir_1"].notna().sum()>0:
            sh("Section × Freshness Breakdown",
               "Full freshness status across all major sections",
               insight="Green = competitor actively investing here — hard to beat now. Red = competitor abandoned this territory — easy wins. Focus your content budget on the red sections.")
            top10=df["dir_1"].value_counts().head(10).index
            mv=df[df["dir_1"].isin(top10)].groupby(["dir_1","freshness"]).size().reset_index(name="Count")
            fo2=["Last Week","Last Month","Last Quarter","Last Year","Older than 1 Year","No Date"]
            mv["freshness"]=pd.Categorical(mv["freshness"],categories=fo2,ordered=True)
            mv=mv.sort_values(["dir_1","freshness"])
            fig=px.bar(mv,x="dir_1",y="Count",color="freshness",barmode="stack",
                       title="Top 10 Sections — Freshness Breakdown",
                       color_discrete_map={"Last Week":"#34d399","Last Month":"#7c6aff",
                                           "Last Quarter":"#3b82f6","Last Year":"#f59e0b",
                                           "Older than 1 Year":"#ef4444","No Date":"#1f2937"})
            fig.update_layout(xaxis_title="Section",height=450)
            ap(fig,True);st.plotly_chart(fig,use_container_width=True)
            pv=mv.pivot_table(index="dir_1",columns="freshness",values="Count",fill_value=0)
            st.dataframe(pv,use_container_width=True)

    except Exception as e:
        st.error(f"Advanced EDA error: {e}")

# ═══════════════════════════════════════════════
# TAB 6  RAW DATA — FIXED duplicate columns
# ═══════════════════════════════════════════════
with tabs[5]:
    try:
        sh("Raw Sitemap Data","Search and filter every URL discovered")
        c1,c2,c3,c4=st.columns(4)
        with c1:
            search_term=st.text_input("🔍 Search URLs",placeholder="e.g. blog…",key="rs")
        with c2:
            fresh_opts=["All"]+df["freshness"].value_counts().index.tolist()
            fresh_filter=st.selectbox("📅 Freshness",fresh_opts,key="rf")
        with c3:
            if "dir_1" in df.columns:
                dir_opts=["All"]+df["dir_1"].dropna().value_counts().index.tolist()
                dir_filter=st.selectbox("📁 Section",dir_opts,key="rd")
            else: dir_filter="All"
        with c4:
            depth_opts=["All"]+[str(x) for x in sorted(df["url_depth"].unique().tolist())]
            depth_filter=st.selectbox("📊 Depth",depth_opts,key="rdp")

        filtered=df.copy()
        if search_term: filtered=filtered[filtered["loc"].str.contains(search_term,case=False,na=False)]
        if fresh_filter!="All": filtered=filtered[filtered["freshness"]==fresh_filter]
        if dir_filter!="All" and "dir_1" in filtered.columns: filtered=filtered[filtered["dir_1"]==dir_filter]
        if depth_filter!="All": filtered=filtered[filtered["url_depth"]==int(depth_filter)]

        st.markdown(f"<div style='color:#4b5563;font-size:0.82rem;margin-bottom:0.5rem'>Showing <strong style='color:#7c6aff'>{len(filtered):,}</strong> of {n_total:,} URLs</div>",unsafe_allow_html=True)

        display_cols=get_display_cols(filtered)
        st.dataframe(clean_df(filtered)[display_cols],use_container_width=True,height=480)
        st.download_button("⬇ Download Filtered CSV",
                           clean_df(filtered)[display_cols].to_csv(index=False).encode("utf-8"),
                           f"sitemap_{domain_name.replace('.','_')}.csv","text/csv")

        sh("Summary Statistics")
        summary=pd.DataFrame({
            "Metric":["Total URLs","Avg URL Depth","Max URL Depth","Avg URL Length",
                      "URLs with Dates","Updated Last Week","Updated Last Month",
                      "Updated Last Quarter","Updated Last Year"],
            "Value":[f"{n_total:,}",avg_depth,max_depth,round(df["url_length"].mean(),1),
                     f"{n_dates:,}",f"{n_week:,}",f"{n_month:,}",f"{n_quarter:,}",f"{n_year:,}"]})
        st.dataframe(summary,use_container_width=True,hide_index=True)

    except Exception as e:
        st.error(f"Raw data error: {e}")

# ═══════════════════════════════════════════════
# TAB 7  EXPORT — FIXED unhashable dict
# ═══════════════════════════════════════════════
with tabs[6]:
    try:
        sh("Export Report","Download as HTML → open in Chrome → Cmd+P → Save as PDF")

        def make_html_report():
            now_str=datetime.now().strftime("%Y-%m-%d %H:%M")

            overview_rows="".join(f"<tr><td>{k}</td><td><strong>{v}</strong></td></tr>" for k,v in [
                ("Total URLs",f"{n_total:,}"),("Avg Depth",str(avg_depth)),("Max Depth",str(max_depth)),
                ("URLs with Dates",f"{n_dates:,}"),("Updated Last Week",f"{n_week:,}"),
                ("Updated Last Month",f"{n_month:,}"),("Updated Last Quarter",f"{n_quarter:,}"),
                ("Updated Last Year",f"{n_year:,}")])

            struct_html=""
            if "dir_1" in df.columns and df["dir_1"].notna().sum()>0:
                vc=df["dir_1"].value_counts().reset_index()
                vc.columns=["Section","URL Count"]
                vc["% of Total"]=(vc["URL Count"]/n_total*100).round(2).astype(str)+"%"
                struct_html=vc.to_html(index=False,classes="dt",border=0)

            ng_html=""
            slug_tok=df["last_slug"].apply(tokenize).tolist()
            for lbl,ngdf in build_ngrams(slug_tok).items():
                if ngdf.empty: continue
                ng_html+=f"<h3>{lbl}</h3>"+ngdf.head(20).to_html(index=False,classes="dt",border=0)

            fo3=["Last Week","Last Month","Last Quarter","Last Year","Older than 1 Year","No Date"]
            fc2=df["freshness"].value_counts().reindex(fo3,fill_value=0).reset_index()
            fc2.columns=["Bucket","Count"]
            fc2["%"]=(fc2["Count"]/n_total*100).round(1).astype(str)+"%"

            gap_html=""
            if "dir_1" in df.columns and n_dates>0:
                two_yrs=now-timedelta(days=730)
                df_g=clean_df(df).copy()
                df_g["is_stale"]=(df_g["lastmod_dt"]<two_yrs)|df_g["lastmod_dt"].isna()
                sg=df_g[df_g["dir_1"].notna()].groupby("dir_1").agg(
                    Total=("loc","count"),Stale=("is_stale","sum")).reset_index()
                sg["Stale_pct"]=(sg["Stale"]/sg["Total"]*100).round(1)
                sg["Opp"]=(sg["Stale_pct"]*sg["Total"]/100).round(0).astype(int)
                sg=sg.sort_values("Opp",ascending=False).head(15)
                sg.columns=["Section","Total","Stale","Stale %","Opportunity Score"]
                gap_html=sg.to_html(index=False,classes="dt",border=0)

            return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<title>Sitemap Copilot — {domain_name}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@300;400;500&display=swap');
body{{font-family:'Inter',sans-serif;background:#080810;color:#e2e0f0;max-width:1100px;margin:0 auto;padding:2rem 1.5rem}}
.ab{{display:flex;align-items:center;gap:1rem;background:rgba(124,106,255,0.06);border:1px solid rgba(124,106,255,0.15);border-radius:16px;padding:1rem 1.4rem;margin-bottom:1.5rem}}
.ab img{{width:56px;height:56px;border-radius:50%;border:2px solid rgba(124,106,255,0.4);object-fit:cover}}
.an{{font-family:'Syne',sans-serif;font-weight:700;font-size:1.05rem}}
.ar{{color:#7c6aff;font-size:0.8rem;margin:0.1rem 0 0.3rem}}
.al a{{color:#4b5563;font-size:0.78rem;margin-right:0.8rem;text-decoration:none}}
h1{{font-family:'Syne',sans-serif;font-size:2.5rem;background:linear-gradient(135deg,#fff,#a78bfa,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:0.2rem}}
h2{{font-family:'Syne',sans-serif;font-size:1.2rem;color:#7c6aff;border-left:3px solid #7c6aff;padding-left:0.7rem;margin-top:2.5rem}}
h3{{font-family:'Syne',sans-serif;font-size:1rem;color:#34d399;margin-top:1.4rem}}
.meta{{color:#4b5563;font-size:0.85rem;margin-bottom:2rem}}
table.dt{{width:100%;border-collapse:collapse;margin:0.7rem 0;font-size:0.85rem}}
table.dt th{{background:rgba(124,106,255,0.12);color:#a78bfa;padding:0.5rem 0.7rem;text-align:left;font-family:'Syne',sans-serif;font-size:0.78rem;letter-spacing:0.04em}}
table.dt td{{padding:0.42rem 0.7rem;border-bottom:1px solid rgba(255,255,255,0.04)}}
table.dt tr:nth-child(even) td{{background:rgba(255,255,255,0.02)}}
.footer{{margin-top:3rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,0.05);color:#1f2937;font-size:0.76rem;text-align:center}}
.footer a{{color:#374151;text-decoration:none}}
@media print{{body{{background:#fff;color:#000}}h1{{-webkit-text-fill-color:unset;color:#1a1a2e}}h2{{color:#4f46e5;border-color:#4f46e5}}h3{{color:#059669}}.ab{{background:#f5f5ff;border:1px solid #e0e0ff}}table.dt th{{background:#4f46e5;color:#fff}}}}
</style></head><body>
<div class="ab">
  <img src="data:image/png;base64,{PHOTO_B64}" alt="Sankar">
  <div><div class="an">Sankar Gurumurthy</div>
  <div class="ar">Head of AI SEO &amp; Marketing Data Scientist</div>
  <div class="al">
    <a href="https://www.linkedin.com/in/sankar-gurumurthy-a1044a136/">🔗 LinkedIn</a>
    <a href="https://github.com/sg-sankar">🐙 github.com/sg-sankar</a>
  </div></div>
</div>
<h1>Sitemap Copilot</h1>
<p class="meta">Domain: <strong>{domain_name}</strong> &nbsp;|&nbsp; Generated: {now_str} &nbsp;|&nbsp; See everything your competitor is hiding in plain sight</p>
<h2>Overview Metrics</h2>
<table class="dt"><tr><th>Metric</th><th>Value</th></tr>{overview_rows}</table>
<h2>Site Structure</h2>{struct_html}
<h2>N-Gram Analysis (Slug)</h2>{ng_html}
<h2>Content Freshness</h2>{fc2.to_html(index=False,classes="dt",border=0)}
<h2>Content Gap Opportunities</h2>{gap_html}
<div class="footer">Built by <a href="https://www.linkedin.com/in/sankar-gurumurthy-a1044a136/">Sankar Gurumurthy</a> · <a href="https://github.com/sg-sankar">github.com/sg-sankar</a> · Sitemap Copilot · Open source &amp; free</div>
</body></html>"""

        html_out=make_html_report()
        st.download_button("⬇ Download HTML Report",
                           html_out.encode("utf-8"),
                           f"sitemap_copilot_{domain_name.replace('.','_')}.html",
                           "text/html")
        st.markdown("<div style='color:#4b5563;font-size:0.82rem;margin-top:0.4rem'>💡 Chrome → Cmd+P → Save as PDF</div>",unsafe_allow_html=True)
        st.markdown("---")
        display_cols2=get_display_cols(df)
        st.download_button("⬇ Download Full CSV",
                           clean_df(df)[display_cols2].to_csv(index=False).encode("utf-8"),
                           f"sitemap_{domain_name.replace('.','_')}.csv","text/csv")

    except Exception as e:
        st.error(f"Export error: {e}")

# ── Footer ────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Sitemap Copilot · Built by
  <a href="https://www.linkedin.com/in/sankar-gurumurthy-a1044a136/" target="_blank">Sankar Gurumurthy</a>
  &nbsp;·&nbsp; Head of AI SEO &amp; Marketing Data Scientist
  &nbsp;·&nbsp; <a href="https://github.com/sg-sankar" target="_blank">github.com/sg-sankar</a>
  <br><span style="color:#111;margin-top:0.25rem;display:block">Open source · Free forever · Powered by advertools + Streamlit</span>
</div>
""",unsafe_allow_html=True)
