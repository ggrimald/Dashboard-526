import streamlit as st
import requests
import pandas as pd
import numpy as np
import os
import warnings
import base64
warnings.filterwarnings("ignore")


# PAGE CONFIG
st.set_page_config(
	page_title="PROTOCOL : RECHARGE",
	layout="wide",
	initial_sidebar_state="collapsed",
)

#  GLOBAL CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #f4f1eb !important;
}
.stApp { background-color: #f4f1eb !important; }

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1400px; }

/* ── HEADER ── */
.dash-header {
    border-bottom: 2px solid #1a1814;
    padding-bottom: 18px;
    margin-bottom: 28px;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
}
.dash-title {
    font-family: 'Syne', sans-serif;
    font-size: 38px;
    font-weight: 800;
    color: #1a1814;
    letter-spacing: -1px;
    line-height: 1;
}
.dash-title span { color: #007a52; }
.dash-sub {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #8c8070;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 6px;
}
.dash-meta {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #8c8070;
    text-align: right;
    line-height: 1.9;
}

/* ── KPI CARDS ── */
.kpi-card {
    background: #ffffff;
    border: 1.5px solid #d8d2c4;
    border-radius: 6px;
    padding: 22px 24px 20px;
    position: relative;
    overflow: hidden;
    transition: box-shadow .2s;
}
.kpi-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,.07); border-color: #c0b9a8; }
.kpi-accent {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
}
.kpi-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #8c8070;
    margin-bottom: 10px;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 44px;
    font-weight: 800;
    letter-spacing: -1px;
    line-height: 1;
}
.kpi-ghost {
    position: absolute;
    right: 14px; top: 50%;
    transform: translateY(-50%);
    font-family: 'Syne', sans-serif;
    font-size: 60px;
    font-weight: 800;
    opacity: .04;
    color: #1a1814;
    user-select: none;
    pointer-events: none;
}

/* ── SECTION CARDS ── */
.sec-card {
    background: #ffffff;
    border: 1.5px solid #d8d2c4;
    border-radius: 6px;
    padding: 20px 22px 18px;
    margin-bottom: 18px;
    transition: box-shadow .2s;
}
.sec-card:hover { box-shadow: 0 2px 14px rgba(0,0,0,.05); }
.sec-header {
    display: flex;
    align-items: baseline;
    gap: 10px;
    margin-bottom: 4px;
}
.sec-tag {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    background: #ede9e0;
    color: #8c8070;
    border: 1px solid #d8d2c4;
    border-radius: 3px;
    padding: 2px 7px;
    letter-spacing: 1px;
}
.sec-title {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    font-weight: 500;
    color: #3d3830;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

/* ── INSIGHT BOX ── */
.insight {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #3d3830;
    line-height: 1.6;
    padding: 8px 12px;
    border-radius: 0 4px 4px 0;
    margin-top: 10px;
}
.insight-amber { background: #fdf0d6; border-left: 3px solid #b06800; }
.insight-blue  { background: #dceeff; border-left: 3px solid #1a5fa8; }
.insight-red   { background: #fde8e6; border-left: 3px solid #c0392b; }

/* ── HEATMAP BOXES ── */
.heatmap-wrap {
    border: 1.5px solid #d8d2c4;
    border-radius: 6px;
    overflow: hidden;
    background: #e6e1d6;
}
.heatmap-wrap img {
    width: 100%;
    height: 320px;
    object-fit: cover;
    display: block;
}
.heatmap-footer {
    background: #ffffff;
    border-top: 1px solid #d8d2c4;
    padding: 8px 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.heatmap-name {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #3d3830;
    letter-spacing: 1px;
}
.badge {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    border-radius: 3px;
    padding: 2px 7px;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.badge-green  { background: #d6f0e6; color: #007a52; border: 1px solid #007a52; }
.badge-amber  { background: #fdf0d6; color: #b06800; border: 1px solid #b06800; }
.badge-blue   { background: #dceeff; color: #1a5fa8; border: 1px solid #1a5fa8; }

/* ── LEGEND ── */
.legend-row {
    display: flex;
    gap: 18px;
    margin-top: 8px;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #8c8070;
}
.leg { display: flex; align-items: center; gap: 6px; }
.leg-dot { width: 10px; height: 10px; border-radius: 2px; display: inline-block; }

/* Streamlit plot background override */
.stPlotlyChart, .element-container { background: transparent !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  1. LOAD DATA FROM FIREBASE
# ─────────────────────────────────────────────
FIREBASE_URL = "https://mygame1-cfc60-default-rtdb.firebaseio.com/.json"

@st.cache_data(ttl=300)
def load_data():
    # Fetch data from Firebase with timeout handling
    try:

        resp = requests.get(FIREBASE_URL, timeout=10)

    except Exception as e:

        st.error(f"Firebase request error: {e}")

        return pd.DataFrame()

    # Validate HTTP response

    if resp.status_code != 200:

        st.error(f"Firebase request failed with status {resp.status_code}")

        return pd.DataFrame()

    raw = resp.json()

    # Validate response structure

    if not raw or not isinstance(raw, dict):

        st.warning("Firebase returned empty or invalid data")

        return pd.DataFrame()

    rows = []

    # Iterate through sessions

    for session_id, session_data in raw.items():

        if not isinstance(session_data, dict):

            continue

        # Iterate through event types

        for event_type, event_data in session_data.items():

            # Normalize event_data to list (handle both list and dict)

            if isinstance(event_data, list):

                events = event_data

            elif isinstance(event_data, dict):

                events = [event_data]

            else:

                continue

            # Extract individual events

            for i, event in enumerate(events):

                if not isinstance(event, dict):

                    continue

                row = {

                    "session_id": session_id,

                    "event_type": str(event_type),

                    "index": i

                }

                row.update(event)

                rows.append(row)

    # Return empty DataFrame if no valid rows

    if not rows:

        return pd.DataFrame()

    df = pd.DataFrame(rows)

    # Safely convert numeric columns

    numeric_cols = [

        "m_NewValue", "m_OldValue", "m_LevelTime",

        "m_PositionX", "m_PositionY", "m_PositionZ"

    ]

    for col in numeric_cols:

        if col in df.columns:

            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Convert list-type values to tuples (required for Streamlit cache hashing)

    for col in df.columns:

        if df[col].apply(lambda x: isinstance(x, list)).any():

            df[col] = df[col].apply(

                lambda x: tuple(x) if isinstance(x, list) else x

            )

    return df

# ─────────────────────────────────────────────
#  2. COMPUTE ALL METRICS
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def compute_metrics(df: pd.DataFrame):
    df = df.copy()
    if "m_NewValue" in df.columns:
        df["m_NewValue"] = pd.to_numeric(df["m_NewValue"], errors="coerce")
    if "m_OldValue" in df.columns:
        df["m_OldValue"] = pd.to_numeric(df["m_OldValue"], errors="coerce")
    if "m_LevelTime" in df.columns:
        df["m_LevelTime"] = pd.to_numeric(df["m_LevelTime"], errors="coerce")

    df["delta"] = df["m_NewValue"] - df["m_OldValue"]

    df["m_LevelName"] = df["m_LevelName"].replace({
        "BetaTutorialLevel": "Tutorial - V2",
        "TutorialLevel":     "Tutorial - V1",
        "BuildingScene":     "Level 1",
    }) if "m_LevelName" in df.columns else df.get("m_LevelName", "Unknown")

    # ── KPIs ──────────────────────────────────────────────────────────
    total_sessions = df["session_id"].nunique()

    death_df   = df[df["event_type"] == "PlayerDeathEvent"]
    total_deaths = len(death_df)

    death_counts = death_df["m_InstigatorClassName"].value_counts() \
        if "m_InstigatorClassName" in death_df.columns else pd.Series(dtype=int)

    shoot_df  = df[df["event_type"] == "PlayerHipFireStart"]
    reload_df = df[df["event_type"] == "PlayerReloadStart"]

    total_shots   = len(shoot_df)
    total_reloads = len(reload_df)
    ratio_str = f"{total_shots / total_reloads:.1f}×" if total_reloads > 0 else "N/A"

    # ── M1  Energy change by source ───────────────────────────────────
    energy_df = df[df["event_type"] == "PlayerHealthUpdate"].copy()

    energy_by_source = (
        energy_df.groupby("m_InstigatorClassName")["delta"]
        .sum()
        .drop("Player_V2", errors="ignore")
        .sort_values()
    ) if "m_InstigatorClassName" in energy_df.columns else pd.Series(dtype=float)

    # ── M3  Shooting by level ─────────────────────────────────────────
    shoot_df2 = df[df['event_type'].isin(['PlayerHipFireStart','PlayerReloadStart'])].copy()

    if "m_LevelName" in shoot_df2.columns:
        shoot_df2['level_group'] = shoot_df2['m_LevelName'].replace({
            'Tutorial - V1': 'Tutorial',
            'Tutorial - V2': 'Tutorial',
            'Level 1': 'Level 1'
        })

        shooting_by_level = (
            shoot_df2.groupby(['level_group','event_type'])
            .size()
            .unstack(fill_value=0)
            .reindex(['Tutorial','Level 1'])
        )

        shooting_by_level = shooting_by_level.rename(columns={
            'PlayerHipFireStart':'Shots',
            'PlayerReloadStart':'Reloads'
        })

    else:
        shooting_by_level = pd.DataFrame(columns=["Shots","Reloads"])

    # ── Issue 1  Aiming ───────────────────────────────────────────────
    damage_df = energy_df[energy_df["delta"] < 0].copy()

    if "m_InstigatorClassName" in damage_df.columns:
        damage_df = damage_df[damage_df["m_InstigatorClassName"] != "EnergyDoor"]

    damage_df["damageTaken"] = -damage_df["delta"]

    total_damage = damage_df["damageTaken"].sum()

    aiming_pct = total_shots / (total_shots + total_damage) \
        if (total_shots + total_damage) > 0 else 0

    inefficiency = total_damage / total_shots if total_shots > 0 else 0

    # ── Issue 2  Progress efficiency ──────────────────────────────────
    pickup_df = energy_df[energy_df["delta"] > 0].copy()

    progress_norm = pd.Series(dtype=float)

    if "m_LevelName" in pickup_df.columns and "session_id" in pickup_df.columns:

        pkps = pickup_df.groupby(["session_id","m_LevelName"]).size().reset_index(name="pickups")
        avg_pkps = pkps.groupby("m_LevelName")["pickups"].mean()

        if "m_LevelTime" in df.columns:
            t_sess = df.groupby(["session_id","m_LevelName"])["m_LevelTime"].max().reset_index()
            avg_t  = t_sess.groupby("m_LevelName")["m_LevelTime"].mean()
            pkpm   = avg_pkps / (avg_t / 60).replace(0, np.nan)
        else:
            pkpm = avg_pkps

        baseline = pkpm.get("Tutorial - V1") or pkpm.get("Tutorial - V2") or pkpm.iloc[0] \
            if len(pkpm) else 1

        progress_norm = (pkpm / baseline).dropna() if baseline else pkpm

    # ── Issue 3  Enemy inefficiency ───────────────────────────────────
    enemy_ineff = pd.Series(dtype=float)

    if "m_InstigatorClassName" in damage_df.columns and "session_id" in damage_df.columns:

        dmg_sess = damage_df.groupby(
            ["session_id","m_InstigatorClassName"]
        )["damageTaken"].sum().reset_index()

        dmg_avg = dmg_sess.groupby("m_InstigatorClassName")["damageTaken"].mean()

        avg_shots_per_sess = shoot_df.groupby("session_id").size().mean() \
            if not shoot_df.empty else 1

        enemy_ineff = (dmg_avg / avg_shots_per_sess).sort_values(ascending=False)

        enemy_ineff = enemy_ineff[
            enemy_ineff.index.isin([
                "EnemyPatrolZone",
                "EnemyStalker"
            ])
        ]

    # ── ROUNDING ─────────────────────────────────────────
    aiming_pct = round(aiming_pct, 2)
    inefficiency = round(inefficiency, 2)

    if not progress_norm.empty:
        progress_norm = progress_norm.round(2)

    if not enemy_ineff.empty:
        enemy_ineff = enemy_ineff.round(2)

    if not shooting_by_level.empty:
        shooting_by_level = shooting_by_level.round(2)

    return dict(
        total_sessions=total_sessions,
        total_deaths=total_deaths,
        ratio_str=ratio_str,
        energy_by_source=energy_by_source,
        death_counts=death_counts,
        shooting_by_level=shooting_by_level,
        aiming_pct=aiming_pct,
        inefficiency=inefficiency,
        progress_norm=progress_norm,
        enemy_ineff=enemy_ineff,
    )

# ─────────────────────────────────────────────
#  3. PLOTLY CHART HELPERS
# ─────────────────────────────────────────────
try:
    import plotly.graph_objects as go
    import plotly.express as px
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# Colour palette
C = dict(
    green="#007a52", green_lt="#d6f0e6",
    red="#c0392b",   red_lt="#fde8e6",
    amber="#b06800", amber_lt="#fdf0d6",
    blue="#1a5fa8",  blue_lt="#dceeff",
    purple="#5a3fa8",purple_lt="#ebe6ff",
    ink="#1a1814",   muted="#8c8070",
    bg="#f4f1eb",    white="#ffffff",
    border="#d8d2c4",
)
MONO = "DM Mono, monospace"
HEAD = "Syne, sans-serif"

# Base layout — never pass this directly with **; always use L() below
_BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#ffffff",
    font=dict(family=MONO, color=C["ink"], size=11),
    margin=dict(l=10, r=10, t=10, b=10),
    showlegend=False,
    xaxis=dict(showgrid=False, zeroline=False,
               linecolor=C["border"], tickfont=dict(color=C["muted"], size=10)),
    yaxis=dict(gridcolor=C["border"], gridwidth=0.7,
               zerolinecolor=C["border"], tickfont=dict(color=C["muted"], size=10)),
)

def L(**overrides):
    """Merge _BASE_LAYOUT with per-chart overrides safely (no duplicate keys)."""
    result = dict(_BASE_LAYOUT)
    result.update(overrides)
    return result


def make_energy_chart(energy_by_source):
    colors    = [C["green"] if v >= 0 else C["red"]    for v in energy_by_source.values]
    lt_colors = [C["green_lt"] if v >= 0 else C["red_lt"] for v in energy_by_source.values]

    fig = go.Figure(go.Bar(
        x=list(energy_by_source.index),
        y=list(energy_by_source.values),
        marker=dict(color=lt_colors, line=dict(color=colors, width=1.8)),
        width=0.5,
        text=[f"{int(v):+d}" for v in energy_by_source.values],
        textposition="outside",
        textfont=dict(family=MONO, size=11, color=colors),
    ))
    fig.update_layout(**L(
        height=220,
        yaxis=dict(gridcolor=C["border"], gridwidth=0.7,
                   zeroline=True, zerolinecolor=C["ink"], zerolinewidth=1.2,
                   tickfont=dict(color=C["muted"], size=10)),
    ))
    return fig


def make_donut_chart(death_counts, total_deaths):
    pal    = [C["red"], C["amber"], C["purple"], C["muted"], C["blue"], C["green"]]
    pal_lt = [C["red_lt"], C["amber_lt"], C["purple_lt"], "#f4f1eb", C["blue_lt"], C["green_lt"]]
    n      = len(death_counts)

    fig = go.Figure(go.Pie(
        labels=list(death_counts.index),
        values=list(death_counts.values),
        hole=0.58,
        marker=dict(colors=pal_lt[:n], line=dict(color=pal[:n], width=2)),
        textinfo="percent",
        textfont=dict(family=MONO, size=11, color=C["ink"]),
        insidetextorientation="radial",
    ))
    fig.add_annotation(text=f"<b>{total_deaths}</b>",
                       x=0.5, y=0.55, showarrow=False,
                       font=dict(family=HEAD, size=30, color=C["red"]))
    fig.add_annotation(text="TOTAL DEATHS",
                       x=0.5, y=0.4, showarrow=False,
                       font=dict(family=MONO, size=9, color=C["muted"]))
    fig.update_layout(**L(
        height=235,
        showlegend=True,
        legend=dict(font=dict(family=MONO, size=10, color=C["muted"]),
                    bgcolor="rgba(0,0,0,0)", x=1.02, y=0.5, xanchor="left"),
    ))
    return fig


def make_grouped_bar(shooting_by_level):
    lvls    = list(shooting_by_level.index)
    shots   = list(shooting_by_level.get("Shots",   pd.Series([0]*len(lvls))).values)
    reloads = list(shooting_by_level.get("Reloads", pd.Series([0]*len(lvls))).values)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Shots", x=lvls, y=shots, width=0.3,
        marker=dict(color=C["purple_lt"], line=dict(color=C["purple"], width=1.8)),
        text=shots, textposition="outside",
        textfont=dict(family=MONO, size=11, color=C["purple"]),
        offset=-0.17,
    ))
    fig.add_trace(go.Bar(
        name="Reloads", x=lvls, y=reloads, width=0.3,
        marker=dict(color=C["amber_lt"], line=dict(color=C["amber"], width=1.8)),
        text=reloads, textposition="outside",
        textfont=dict(family=MONO, size=11, color=C["amber"]),
        offset=0.17,
    ))
    fig.update_layout(**L(
        height=235,
        barmode="overlay",
        showlegend=True,
        legend=dict(font=dict(family=MONO, size=10, color=C["muted"]),
                    bgcolor="rgba(0,0,0,0)", orientation="h", x=0, y=1.08),
    ))
    return fig


def make_aiming_chart(aiming_pct, inefficiency):
    vals   = [aiming_pct, inefficiency]
    names  = ["Aiming %", "Inefficiency"]
    colors = [C["blue"], C["red"]]
    lts    = [C["blue_lt"], C["red_lt"]]

    fig = go.Figure(go.Bar(
        x=names, y=vals,
        marker=dict(color=lts, line=dict(color=colors, width=1.8)),
        width=0.4,
        text=[
            f"{aiming_pct*100:.0f}%",
            f"{inefficiency:.1f}×"
        ],
        textposition="outside",
        textfont=dict(family=MONO, size=12, color=colors),
    ))

    fig.add_annotation(
        text="Aiming = shots / (shots + damage) | Inefficiency = damage / shots",
        x=0.5, y=-0.3,
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(size=10, color=C["muted"])
    )

    fig.update_layout(**L(height=220))
    return fig


def make_progress_chart(progress_norm):
    if progress_norm.empty:
        return go.Figure()

    lvls = list(progress_norm.index)
    vals = list(progress_norm.values)

    fig = go.Figure(go.Bar(
        x=lvls, y=vals,
        marker=dict(color=C["green_lt"], line=dict(color=C["green"], width=1.8)),
        width=0.4,
        text=[f"{v:.2f}" for v in vals],
        textposition="outside",
        textfont=dict(family=MONO, size=12, color=C["green"]),
    ))

    fig.add_hline(y=1.0, line_dash="dash",
        line_color=C["green"],
        annotation_text="baseline"
    )

    fig.add_annotation(
        text="Normalized pickups per minute (1.0 = expected baseline)",
        x=0.5, y=-0.3,
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(size=10, color=C["muted"])
    )

    fig.update_layout(**L(height=220))
    return fig


def make_enemy_chart(enemy_ineff):
    if enemy_ineff.empty:
        return go.Figure()

    names = list(enemy_ineff.index)
    vals  = list(enemy_ineff.values)

    fig = go.Figure(go.Bar(
        x=names, y=vals,
        marker=dict(color=C["amber_lt"], line=dict(color=C["amber"], width=1.8)),
        width=0.5,
        text=[f"{v:.2f}" for v in vals],
        textposition="outside",
        textfont=dict(family=MONO, size=12, color=C["amber"]),
    ))

    avg = np.mean(vals)
    fig.add_hline(y=avg, line_dash="dash",
        line_color=C["amber"],
        annotation_text="avg"
    )

    fig.add_annotation(
        text="Damage taken per shot (lower is better)",
        x=0.5, y=-0.3,
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(size=10, color=C["muted"])
    )

    fig.update_layout(**L(height=220))
    return fig


# ─────────────────────────────────────────────
#  4.  HEATMAP HELPER
# ─────────────────────────────────────────────
def show_heatmap(path: str, title: str, badge_class: str, badge_text: str):
    if os.path.exists(path):
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        ext = path.rsplit(".", 1)[-1].lower()
        mime = "image/png" if ext == "png" else "image/jpeg"
        img_html = f'<img src="data:{mime};base64,{b64}" style="width:100%;height:320px;object-fit:cover;display:block;">'
    else:
        img_html = f"""
        <div style="width:100%;height:320px;background:#e6e1d6;
            background-image:repeating-linear-gradient(45deg,transparent,
            transparent 12px,rgba(0,0,0,.025) 12px,rgba(0,0,0,.025) 13px);
            display:flex;flex-direction:column;align-items:center;
            justify-content:center;gap:8px;">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none"
                stroke="#8c8070" stroke-width="1.2">
                <rect x="3" y="3" width="18" height="18" rx="2"/>
                <circle cx="12" cy="10" r="3"/>
                <path d="M5 20 Q12 13 19 20"/>
            </svg>
            <span style="font-family:'DM Mono',monospace;font-size:10px;
                color:#8c8070;letter-spacing:1px;">{path}</span>
        </div>"""

    st.markdown(f"""
    {img_html}
    <div class="heatmap-footer">
        <span class="heatmap-name">{title}</span>
        <span class="badge {badge_class}">{badge_text}</span>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  5.  RENDER DASHBOARD
# ─────────────────────────────────────────────
with st.spinner("Loading analytics data..."):
    df = load_data()
    m  = compute_metrics(df)

# ── HEADER ───────────────────────────────────
st.markdown(f"""
<div class="dash-header">
  <div>
    <div class="dash-title">PROTOCOL<span> : </span>RECHARGE</div>
    <div class="dash-sub">Game Analytics Dashboard &nbsp;·&nbsp; Session Telemetry</div>
  </div>
  <div class="dash-meta">
    <strong style="font-size:10px;letter-spacing:1px;color:#3d3830;">DATA SOURCE</strong><br>
    Firebase Realtime Database<br>
    analytics_clean.parquet
  </div>
</div>""", unsafe_allow_html=True)

# ── KPIs ─────────────────────────────────────
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Sessions</div>
        <div class="kpi-value" style="color:#007a52">{m['total_sessions']}</div>
        <div class="kpi-ghost">S</div>
        <div class="kpi-accent" style="background:#007a52"></div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Deaths</div>
        <div class="kpi-value" style="color:#c0392b">{m['total_deaths']}</div>
        <div class="kpi-ghost">D</div>
        <div class="kpi-accent" style="background:#c0392b"></div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Shot / Reload Ratio</div>
        <div class="kpi-value" style="color:#b06800">{m['ratio_str']}</div>
        <div class="kpi-ghost">R</div>
        <div class="kpi-accent" style="background:#b06800"></div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

# ── M1  ENERGY ───────────────────────────────
st.markdown("""
<div class="sec-card">
  <div class="sec-header">
    <span class="sec-tag">M1</span>
    <span class="sec-title">Energy Change by Source</span>
  </div>
</div>""", unsafe_allow_html=True)

if not m["energy_by_source"].empty and HAS_PLOTLY:
    st.plotly_chart(make_energy_chart(m["energy_by_source"]),
                    use_container_width=True, config={"displayModeBar": False})
    st.markdown("""
    <div class="legend-row">
        <div class="leg"><div class="leg-dot" style="background:#007a52"></div>Energy gain</div>
        <div class="leg"><div class="leg-dot" style="background:#c0392b"></div>Energy loss</div>
    </div>""", unsafe_allow_html=True)
else:
    st.info("No energy data available.")

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ── M2 + M3 ──────────────────────────────────
col_m2, col_m3 = st.columns(2)

with col_m2:
    st.markdown("""
    <div class="sec-card">
      <div class="sec-header">
        <span class="sec-tag">M2</span>
        <span class="sec-title">Player Death Causes</span>
      </div>
    </div>""", unsafe_allow_html=True)
    if not m["death_counts"].empty and HAS_PLOTLY:
        st.plotly_chart(make_donut_chart(m["death_counts"], m["total_deaths"]),
                        use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No death data available.")

with col_m3:
    st.markdown("""
    <div class="sec-card">
      <div class="sec-header">
        <span class="sec-tag">M3</span>
        <span class="sec-title">Shooting Activity by Level</span>
      </div>
    </div>""", unsafe_allow_html=True)
    if not m["shooting_by_level"].empty and HAS_PLOTLY:
        st.plotly_chart(make_grouped_bar(m["shooting_by_level"]),
                        use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No shooting data available.")

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ── ISSUES 1 · 2 · 3 ─────────────────────────
i1, i2, i3 = st.columns(3)

with i1:
    st.markdown("""
    <div class="sec-card">
      <div class="sec-header">
        <span class="sec-tag" style="background:#dceeff;color:#1a5fa8;border-color:#1a5fa8">I1</span>
        <span class="sec-title">Aiming Effectiveness</span>
      </div>
    </div>""", unsafe_allow_html=True)
    if HAS_PLOTLY:
        st.plotly_chart(make_aiming_chart(m["aiming_pct"], m["inefficiency"]),
                        use_container_width=True, config={"displayModeBar": False})
    st.markdown("""
    <div class="insight insight-blue">
                Aiming % represents the proportion of effective shots.
                Inefficiency represents damage taken per shot fired.
                Higher aiming is better.
                Lower inefficiency is better.
    </div>""", unsafe_allow_html=True)

with i2:
    st.markdown("""
    <div class="sec-card">
      <div class="sec-header">
        <span class="sec-tag" style="background:#fdf0d6;color:#b06800;border-color:#b06800">I2</span>
        <span class="sec-title">Progress Efficiency</span>
      </div>
    </div>""", unsafe_allow_html=True)
    if not m["progress_norm"].empty and HAS_PLOTLY:
        st.plotly_chart(make_progress_chart(m["progress_norm"]),
                        use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No progress data available.")
    st.markdown("""
    <div class="insight insight-amber">
                Progress efficiency represents pickups per minute normalized against the tutorial baseline (1.0).
                Values below 1 indicate slower progression.
                Values above 1 indicate faster progression.
    </div>""", unsafe_allow_html=True)

with i3:
    st.markdown("""
    <div class="sec-card">
      <div class="sec-header">
        <span class="sec-tag" style="background:#fde8e6;color:#c0392b;border-color:#c0392b">I3</span>
        <span class="sec-title">Combat Inefficiency by Enemy</span>
      </div>
    </div>""", unsafe_allow_html=True)
    if not m["enemy_ineff"].empty and HAS_PLOTLY:
        st.plotly_chart(make_enemy_chart(m["enemy_ineff"]),
                        use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No enemy data available.")
    st.markdown("""
    <div class="insight insight-red">
        Inefficiency represents damage taken per shot when facing each enemy type.
        Higher values indicate worse performance.
        Lower values indicate better performance.
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ── M4  HEATMAPS ─────────────────────────────
st.markdown("""
<div class="sec-card">
  <div class="sec-header">
    <span class="sec-tag">M4</span>
    <span class="sec-title">Spatial Combat Heatmaps — Damage vs Shooting</span>
  </div>
  <div class="legend-row" style="margin-bottom:14px">
    <div class="leg"><div class="leg-dot" style="background:#1a5fa8"></div>Shooting events</div>
    <div class="leg"><div class="leg-dot" style="background:#c0392b"></div>Damage taken</div>
    <div class="leg"><div class="leg-dot" style="background:#5a3fa8"></div>Overlap zones</div>
  </div>
</div>""", unsafe_allow_html=True)

hm1, hm2, hm3 = st.columns(3)
with hm1:
    st.markdown('<div class="heatmap-wrap">', unsafe_allow_html=True)
    show_heatmap("Tutorial-Level-Alpha.png", "TUTORIAL — ALPHA", "badge-green", "ALPHA")
    st.markdown("</div>", unsafe_allow_html=True)
with hm2:
    st.markdown('<div class="heatmap-wrap">', unsafe_allow_html=True)
    show_heatmap("Tutorial-Level-Beta.png", "TUTORIAL — BETA", "badge-amber", "BETA")
    st.markdown("</div>", unsafe_allow_html=True)
with hm3:
    st.markdown('<div class="heatmap-wrap">', unsafe_allow_html=True)
    show_heatmap("Level-1.png", "LEVEL 1 — BUILDING", "badge-blue", "LVL 1")
    st.markdown("</div>", unsafe_allow_html=True)

# ── FOOTER ───────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:40px;padding-top:16px;
    border-top:1px solid #d8d2c4;font-family:'DM Mono',monospace;
    font-size:9px;color:#8c8070;letter-spacing:2px;">
  PROTOCOL : RECHARGE
</div>""", unsafe_allow_html=True)
