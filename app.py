import html
import re
import tempfile
from pathlib import Path

import streamlit as st

from ai.decision_engine import analyze_business_decision
from business.profile import create_profile, save_profile
from rag.rag_engine import RAGEngine
from evidence.evidence_fusion import fuse_evidence

from web_intelligence.web_researcher import (
    research_business_market,
)

from web_intelligence.web_content import (
    extract_web_pages,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Business DecisionAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# PREMIUM CINEMATIC LIGHT UI
# =========================================================

st.markdown(
    """
<style>

@import url(
    'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap'
);


/* =====================================================
   HIDE STREAMLIT CHROME
===================================================== */

#MainMenu,
footer,
header {
    visibility: hidden;
}


/* =====================================================
   GLOBAL LIGHT BACKGROUND
===================================================== */

.stApp {

    position: relative;

    overflow-x: hidden;

    background:

        radial-gradient(
            circle at 8% 8%,
            rgba(99,102,241,.10),
            transparent 25%
        ),

        radial-gradient(
            circle at 92% 10%,
            rgba(6,182,212,.08),
            transparent 27%
        ),

        radial-gradient(
            circle at 85% 90%,
            rgba(236,72,153,.07),
            transparent 25%
        ),

        linear-gradient(
            135deg,
            #fbfdff 0%,
            #f8f6ff 46%,
            #f9fdff 100%
        );

    color:#172033;

    font-family:
        'DM Sans',
        'Manrope',
        sans-serif;
}


 .block-container {

    position: relative;

    z-index: 5;

    max-width:1280px;

    padding-top:1.5rem;

    padding-bottom:4rem;
}


/* =====================================================
   STREAMLIT CONTENT SAFETY LAYER
===================================================== */

[data-testid="stAppViewContainer"] {

    position:relative;

    z-index:1;
}

[data-testid="stMain"] {

    position:relative;

    z-index:10;
}

[data-testid="stHeader"] {

    z-index:20;
}


/* =====================================================
   TYPOGRAPHY
===================================================== */

h1,
h2,
h3,
p,
div,
span,
label,
button {

    font-family:
        'DM Sans',
        'Manrope',
        sans-serif;
}


/* =====================================================
   CINEMATIC BACKGROUND ANIMATIONS

   IMPORTANT:
   These animations are ONLY for decorative
   background shapes.

   UI ICONS DO NOT MOVE.
===================================================== */

@keyframes cinematicOrbOne {

    0% {
        transform:
            translate3d(0,0,0)
            rotate(0deg)
            scale(1);
    }

    35% {
        transform:
            translate3d(35px,-22px,0)
            rotate(5deg)
            scale(1.035);
    }

    70% {
        transform:
            translate3d(-20px,25px,0)
            rotate(-4deg)
            scale(.98);
    }

    100% {
        transform:
            translate3d(0,0,0)
            rotate(0deg)
            scale(1);
    }
}


@keyframes cinematicOrbTwo {

    0% {
        transform:
            translate3d(0,0,0)
            rotate(0deg)
            scale(1);
    }

    40% {
        transform:
            translate3d(-30px,24px,0)
            rotate(-6deg)
            scale(1.04);
    }

    75% {
        transform:
            translate3d(22px,-18px,0)
            rotate(5deg)
            scale(.97);
    }

    100% {
        transform:
            translate3d(0,0,0)
            rotate(0deg)
            scale(1);
    }
}


@keyframes cinematicOrbThree {

    0% {
        transform:
            translate3d(0,0,0)
            scale(1);
    }

    50% {
        transform:
            translate3d(18px,-30px,0)
            scale(1.08);
    }

    100% {
        transform:
            translate3d(0,0,0)
            scale(1);
    }
}


@keyframes cinematicOrbFour {

    0% {
        transform:
            translate3d(0,0,0)
            rotate(0deg);
    }

    50% {
        transform:
            translate3d(-24px,20px,0)
            rotate(8deg);
    }

    100% {
        transform:
            translate3d(0,0,0)
            rotate(0deg);
    }
}


/* =====================================================
   VERY SOFT LIGHT SHIMMER
===================================================== */

@keyframes softLight {

    0% {
        opacity:.45;
        filter:
            blur(0px)
            brightness(1);
    }

    50% {
        opacity:.72;
        filter:
            blur(1px)
            brightness(1.08);
    }

    100% {
        opacity:.45;
        filter:
            blur(0px)
            brightness(1);
    }
}


/* =====================================================
   HERO GRADIENT
===================================================== */

@keyframes iconShimmer {

    0%, 100% {
        filter:
            brightness(1)
            drop-shadow(0 0 0 rgba(99,102,241,0));
    }

    45% {
        filter:
            brightness(1.08)
            drop-shadow(0 0 7px rgba(99,102,241,.18));
    }

    60% {
        filter:
            brightness(1.16)
            drop-shadow(0 0 13px rgba(6,182,212,.25));
    }

    75% {
        filter:
            brightness(1.06)
            drop-shadow(0 0 7px rgba(236,72,153,.14));
    }
}


.stationary-shimmer {
    animation: iconShimmer 4.8s ease-in-out infinite;
}


/* =====================================================
   HERO GRADIENT
===================================================== */

@keyframes gradientMove {

    0% {
        background-position:0% 50%;
    }

    50% {
        background-position:100% 50%;
    }

    100% {
        background-position:0% 50%;
    }
}


/* =====================================================
   RESULT ANIMATION
===================================================== */

@keyframes slideUp {

    from {
        opacity:0;
        transform:translateY(18px);
    }

    to {
        opacity:1;
        transform:translateY(0);
    }
}


/* =====================================================
   ONLINE STATUS
===================================================== */

@keyframes pulseGlow {

    0% {
        box-shadow:
            0 0 0 0 rgba(34,197,94,.25);
    }

    70% {
        box-shadow:
            0 0 0 8px rgba(34,197,94,0);
    }

    100% {
        box-shadow:
            0 0 0 0 rgba(34,197,94,0);
    }
}


/* =====================================================
   CINEMATIC BACKGROUND SCENE
===================================================== */

.cinematic-scene {

    position:fixed;

    inset:0;

    width:100vw;

    height:100vh;

    overflow:hidden;

    pointer-events:none;

    z-index:0;

    user-select:none;

    isolation:isolate;
}


/* Large screenshot-style curved blob */

.cinematic-blob-main {

    position:absolute;

    top:-90px;

    right:7%;

    width:310px;

    height:310px;

    border-radius:
        22% 78% 55% 45%
        /
        28% 32% 68% 72%;

    background:
        linear-gradient(
            145deg,
            rgba(221,228,250,.68),
            rgba(231,236,250,.45)
        );

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.75);

    animation:
        cinematicOrbOne 22s ease-in-out infinite;
}


/* Soft lavender orb */

.cinematic-blob-lavender {

    position:absolute;

    top:24%;

    left:-120px;

    width:280px;

    height:280px;

    border-radius:50%;

    background:
        radial-gradient(
            circle,
            rgba(199,210,254,.24),
            rgba(224,231,255,.10) 55%,
            transparent 72%
        );

    filter:blur(4px);

    animation:
        cinematicOrbTwo 25s ease-in-out infinite;
}


/* Cyan soft light */

.cinematic-blob-cyan {

    position:absolute;

    right:-90px;

    top:42%;

    width:260px;

    height:260px;

    border-radius:
        65% 35% 45% 55%
        /
        45% 55% 45% 55%;

    background:
        radial-gradient(
            circle,
            rgba(165,243,252,.20),
            rgba(207,250,254,.08) 60%,
            transparent 75%
        );

    filter:blur(3px);

    animation:
        cinematicOrbThree 20s ease-in-out infinite;
}


/* Blush lower corner */

.cinematic-blob-pink {

    position:absolute;

    left:8%;

    bottom:-120px;

    width:300px;

    height:300px;

    border-radius:
        50% 50% 35% 65%;

    background:
        radial-gradient(
            circle,
            rgba(251,207,232,.18),
            rgba(253,242,248,.08) 60%,
            transparent 75%
        );

    filter:blur(5px);

    animation:
        cinematicOrbFour 24s ease-in-out infinite;
}


/* Tiny atmospheric light */

.cinematic-light-one {

    position:absolute;

    top:19%;

    left:38%;

    width:75px;

    height:75px;

    border-radius:50%;

    background:
        radial-gradient(
            circle,
            rgba(165,243,252,.16),
            transparent 70%
        );

    animation:
        softLight 8s ease-in-out infinite;
}


.cinematic-light-two {

    position:absolute;

    bottom:17%;

    right:30%;

    width:90px;

    height:90px;

    border-radius:50%;

    background:
        radial-gradient(
            circle,
            rgba(221,214,254,.18),
            transparent 70%
        );

    animation:
        softLight 10s ease-in-out infinite;
}


/* =====================================================
   INPUTS
===================================================== */

div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {

    background:
        rgba(255,255,255,.88) !important;

    border:
        1px solid rgba(148,163,184,.25) !important;

    border-radius:17px !important;

    box-shadow:
        0 8px 25px rgba(30,41,59,.055),
        inset 0 1px 0 rgba(255,255,255,.8);

    transition:
        border .2s ease,
        box-shadow .2s ease,
        transform .2s ease;
}


div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="textarea"] > div:focus-within {

    border:
        1px solid rgba(99,102,241,.65) !important;

    box-shadow:
        0 0 0 4px rgba(99,102,241,.08),
        0 12px 30px rgba(79,70,229,.08);

    transform:
        translateY(-1px);
}


div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {

    color:#172033 !important;

    font-size:15px !important;

    font-weight:500 !important;
}


div[data-baseweb="textarea"] textarea {

    min-height:150px !important;
}


label {

    color:#475569 !important;

    font-weight:700 !important;
}


/* =====================================================
   FILE UPLOADER
===================================================== */

[data-testid="stFileUploader"] {

    background:
        rgba(255,255,255,.88);

    border:
        1px solid rgba(148,163,184,.20);

    border-radius:19px;

    padding:8px;

    box-shadow:
        0 10px 30px rgba(15,23,42,.05);
}


[data-testid="stFileUploaderDropzone"] {

    background:
        linear-gradient(
            135deg,
            rgba(238,242,255,.70),
            rgba(236,254,255,.70)
        ) !important;

    border:
        1px dashed rgba(99,102,241,.35) !important;

    border-radius:15px !important;
}


/* =====================================================
   BUTTON
===================================================== */

.stButton > button {

    width:100%;

    min-height:58px;

    border:none !important;

    border-radius:17px !important;

    background:
        linear-gradient(
            110deg,
            #4338ca,
            #6366f1,
            #0891b2,
            #7c3aed
        ) !important;

    background-size:
        300% 300% !important;

    animation:
        gradientMove 7s ease infinite;

    color:white !important;

    font-size:16px !important;

    font-weight:800 !important;

    box-shadow:
        0 14px 32px rgba(79,70,229,.24),
        0 4px 10px rgba(6,182,212,.12);

    transition:
        transform .25s ease,
        box-shadow .25s ease;
}


.stButton > button:hover {

    transform:
        translateY(-3px)
        scale(1.01);

    box-shadow:
        0 20px 45px rgba(79,70,229,.30),
        0 8px 18px rgba(6,182,212,.18);
}


div[data-testid="stAlert"] {

    border-radius:15px !important;
}


div[data-testid="stSpinner"] {

    color:#4f46e5 !important;
}


/* =====================================================
   MOBILE
===================================================== */

@media (max-width: 768px) {

    .cinematic-blob-main {

        width:220px;

        height:220px;

        right:-70px;

        top:-50px;
    }

    .cinematic-blob-lavender {

        width:190px;

        height:190px;
    }

}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# CINEMATIC BACKGROUND OBJECTS
# =========================================================

st.html(
    """
<div class="cinematic-scene">

    <div class="cinematic-blob-main"></div>

    <div class="cinematic-blob-lavender"></div>

    <div class="cinematic-blob-cyan"></div>

    <div class="cinematic-blob-pink"></div>

    <div class="cinematic-light-one"></div>

    <div class="cinematic-light-two"></div>

</div>
"""
)


# =========================================================
# HELPERS
# =========================================================

def clean_text(value):

    if not value:
        return ""

    value = str(value).strip()

    value = re.sub(
        r"[\*\_\`#]+",
        "",
        value,
    )

    return value.strip()


def parse_ai_response(response):

    result = {
        "summary": "",
        "risk": "Unknown",
        "confidence": "—",
        "reasons": [],
        "recommendation": "",
    }

    if not response:
        return result

    text = str(response).replace(
        "\r\n",
        "\n",
    ).strip()

    patterns = {

        "summary":
            r"Decision Summary:\s*(.*?)(?=\n\s*Risk Level:|\Z)",

        "risk":
            r"Risk Level:\s*(.*?)(?=\n\s*Confidence:|\Z)",

        "confidence":
            r"Confidence:\s*(.*?)(?=\n\s*Reason:|\Z)",

        "reason":
            r"Reason:\s*(.*?)(?=\n\s*Recommendation:|\Z)",

        "recommendation":
            r"Recommendation:\s*(.*)",
    }

    for key, pattern in patterns.items():

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if not match:
            continue

        value = match.group(1).strip()

        if key == "reason":

            parts = re.split(
                r"(?:^|\n)\s*(?:\d+[\.\)]|[-•])\s*",
                value,
            )

            parts = [
                clean_text(part)
                for part in parts
                if clean_text(part)
            ]

            if not parts:

                parts = [
                    clean_text(line)
                    for line in value.split("\n")
                    if clean_text(line)
                ]

            result["reasons"] = parts

        else:

            result[key] = clean_text(value)

    return result


def confidence_number(value):

    match = re.search(
        r"\d+(?:\.\d+)?",
        str(value),
    )

    if match:
        return float(match.group(0))

    return 0


def risk_data(value):

    risk = str(value).lower()

    if "high" in risk:

        return (
            "HIGH",
            "#dc2626",
            "#fff1f2",
            "High attention required",
        )

    if "medium" in risk:

        return (
            "MEDIUM",
            "#d97706",
            "#fffbeb",
            "Moderate attention required",
        )

    if "low" in risk:

        return (
            "LOW",
            "#16a34a",
            "#f0fdf4",
            "Lower immediate risk",
        )

    return (
        "UNKNOWN",
        "#64748b",
        "#f8fafc",
        "More information required",
    )


# =========================================================
# TOP BRAND BAR
# =========================================================

st.html(
    """
<div style="
    position:relative;
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:16px 20px;
    margin-bottom:26px;
    background:rgba(255,255,255,.82);
    backdrop-filter:blur(20px);
    border:1px solid rgba(255,255,255,.85);
    border-radius:22px;
    box-shadow:
        0 16px 45px rgba(15,23,42,.07),
        inset 0 1px 0 rgba(255,255,255,.9);
">

    <div style="
        display:flex;
        align-items:center;
        gap:14px;
    ">

        <!-- STATIONARY MAIN ICON -->

        <div class="stationary-shimmer" style="
            width:53px;
            height:53px;
            display:flex;
            align-items:center;
            justify-content:center;
            border-radius:17px;
            background:
                linear-gradient(
                    135deg,
                    #4338ca,
                    #6366f1 50%,
                    #06b6d4
                );
            color:white;
            font-size:27px;
            box-shadow:
                0 12px 26px rgba(79,70,229,.25);
        ">
            🧠
        </div>

        <div>

            <div style="
                font-family:'Manrope',sans-serif;
                font-size:24px;
                font-weight:800;
                letter-spacing:-.6px;
                color:#172033;
            ">
                Business DecisionAI
            </div>

            <div style="
                color:#64748b;
                font-size:12px;
                margin-top:3px;
                font-weight:500;
            ">
                AI-powered business decision intelligence
            </div>

        </div>

    </div>


    <div style="
        display:flex;
        align-items:center;
        gap:8px;
        padding:9px 15px;
        border-radius:999px;
        background:rgba(240,253,244,.92);
        border:1px solid #bbf7d0;
        color:#15803d;
        font-size:11px;
        font-weight:800;
        letter-spacing:.4px;
    ">

        <span style="
            width:8px;
            height:8px;
            border-radius:50%;
            background:#22c55e;
            animation:pulseGlow 2s infinite;
        "></span>

        AI ONLINE

    </div>

</div>
"""
)


# =========================================================
# HERO
# =========================================================

st.html(
    """
<div style="
    position:relative;
    overflow:hidden;
    padding:50px 46px;
    border-radius:30px;
    margin-bottom:30px;
    background:
        linear-gradient(
            120deg,
            #eef2ff 0%,
            #f5f3ff 34%,
            #ecfeff 67%,
            #fdf2f8 100%
        );
    background-size:200% 200%;
    animation:gradientMove 14s ease infinite;
    border:1px solid rgba(255,255,255,.9);
    box-shadow:
        0 25px 70px rgba(79,70,229,.09),
        inset 0 1px 0 rgba(255,255,255,.9);
">


    <!-- LARGE MOVING CINEMATIC SPOT -->

    <div style="
        position:absolute;
        right:40px;
        top:-70px;
        width:245px;
        height:245px;
        border-radius:
            30% 70% 48% 52%
            /
            25% 38% 62% 75%;
        background:
            linear-gradient(
                145deg,
                rgba(218,226,248,.72),
                rgba(232,237,250,.42)
            );
        box-shadow:
            inset 0 1px 0 rgba(255,255,255,.75);
        animation:
            cinematicOrbOne 19s ease-in-out infinite;
    "></div>


    <!-- SECOND MOVING SPOT -->

    <div style="
        position:absolute;
        right:125px;
        bottom:-70px;
        width:135px;
        height:135px;
        border-radius:50%;
        background:
            radial-gradient(
                circle,
                rgba(236,72,153,.11),
                rgba(251,207,232,.05) 65%,
                transparent 75%
            );
        animation:
            cinematicOrbFour 17s ease-in-out infinite;
    "></div>


    <!-- SMALL MOVING LIGHT -->

    <div style="
        position:absolute;
        left:48%;
        bottom:22px;
        width:55px;
        height:55px;
        border-radius:50%;
        background:
            radial-gradient(
                circle,
                rgba(6,182,212,.12),
                transparent 70%
            );
        animation:
            cinematicOrbThree 13s ease-in-out infinite;
    "></div>


    <div style="
        position:relative;
        z-index:2;
    ">

        <div style="
            display:inline-flex;
            align-items:center;
            gap:7px;
            padding:7px 12px;
            border-radius:999px;
            background:rgba(255,255,255,.75);
            border:1px solid rgba(99,102,241,.13);
            color:#4f46e5;
            font-size:11px;
            font-weight:850;
            letter-spacing:1.2px;
        ">
            ✦ DECISION INTELLIGENCE PLATFORM
        </div>


        <div style="
            margin-top:17px;
            font-family:'Manrope',sans-serif;
            font-size:44px;
            line-height:1.10;
            letter-spacing:-1.8px;
            font-weight:800;
            color:#172033;
            max-width:750px;
        ">
            Turn business uncertainty
            into confident decisions.
        </div>


        <div style="
            max-width:720px;
            margin-top:16px;
            color:#64748b;
            font-size:16px;
            line-height:1.8;
            font-weight:500;
        ">
            Evaluate business decisions through AI-assisted
            risk analysis, confidence scoring, reasoning
            and actionable recommendations.
        </div>


        <div style="
            display:flex;
            flex-wrap:wrap;
            gap:9px;
            margin-top:23px;
        ">

            <!-- STATIONARY ICON CHIP -->

            <span class="stationary-shimmer" style="
                padding:8px 13px;
                border-radius:999px;
                background:#ffffff;
                color:#4338ca;
                border:1px solid #e0e7ff;
                font-size:12px;
                font-weight:750;
                box-shadow:
                    0 5px 15px rgba(79,70,229,.06);
            ">
                🧠 Generative AI
            </span>


            <!-- STATIONARY ICON CHIP -->

            <span style="
                padding:8px 13px;
                border-radius:999px;
                background:#ffffff;
                color:#0e7490;
                border:1px solid #cffafe;
                font-size:12px;
                font-weight:750;
                box-shadow:
                    0 5px 15px rgba(6,182,212,.06);
            ">
                📊 Risk Intelligence
            </span>


            <!-- STATIONARY ICON CHIP -->

            <span style="
                padding:8px 13px;
                border-radius:999px;
                background:#ffffff;
                color:#be185d;
                border:1px solid #fce7f3;
                font-size:12px;
                font-weight:750;
                box-shadow:
                    0 5px 15px rgba(236,72,153,.06);
            ">
                🎯 Actionable Insights
            </span>

        </div>

    </div>

</div>
"""
)


# =========================================================
# PIPELINE
# =========================================================

st.html(
    """
<div style="
    margin-top:32px;
    margin-bottom:15px;
">

    <div style="
        font-family:'Manrope',sans-serif;
        font-size:20px;
        font-weight:800;
        color:#172033;
    ">
        How the AI thinks
    </div>

    <div style="
        margin-top:4px;
        font-size:13px;
        color:#64748b;
    ">
        A layered decision workflow designed for business analysis.
    </div>

</div>
"""
)


p1, p2, p3, p4 = st.columns(
    4,
    gap="small",
)


pipeline = [

    (
        p1,
        "01",
        "Context",
        "Business information",
        "#eef2ff",
        "#4338ca",
        "🏢",
    ),

    (
        p2,
        "02",
        "Reasoning",
        "AI evaluation",
        "#ecfeff",
        "#0e7490",
        "🧠",
    ),

    (
        p3,
        "03",
        "Risk",
        "Risk & confidence",
        "#fff7ed",
        "#c2410c",
        "📊",
    ),

    (
        p4,
        "04",
        "Action",
        "Recommended step",
        "#fdf2f8",
        "#be185d",
        "🎯",
    ),
]


for column, number, title, subtitle, bg, color, icon in pipeline:

    with column:

        st.html(
            f"""
<div style="
    position:relative;
    min-height:115px;
    padding:18px;
    border-radius:19px;
    background:rgba(255,255,255,.86);
    border:1px solid rgba(226,232,240,.9);
    box-shadow:
        0 12px 30px rgba(15,23,42,.05);
">

    <div style="
        display:flex;
        align-items:center;
        justify-content:space-between;
    ">

        <!-- STATIONARY PIPELINE ICON -->

        <div style="
            width:34px;
            height:34px;
            display:flex;
            align-items:center;
            justify-content:center;
            border-radius:11px;
            background:{bg};
            color:{color};
            font-size:17px;
        ">
            {icon}
        </div>

        <div style="
            color:#cbd5e1;
            font-size:10px;
            font-weight:800;
        ">
            {number}
        </div>

    </div>

    <div style="
        margin-top:14px;
        color:#334155;
        font-size:14px;
        font-weight:800;
    ">
        {title}
    </div>

    <div style="
        margin-top:4px;
        color:#94a3b8;
        font-size:11px;
        font-weight:500;
    ">
        {subtitle}
    </div>

</div>
"""
        )


# =========================================================
# BUSINESS CONTEXT
# =========================================================

st.html(
    """
<div style="
    margin-top:38px;
    margin-bottom:14px;
">

    <div style="
        font-family:'Manrope',sans-serif;
        font-size:21px;
        font-weight:800;
        color:#172033;
    ">
        🏢 Business Context
    </div>

    <div style="
        margin-top:5px;
        color:#64748b;
        font-size:13px;
    ">
        Tell the AI who you are and what business you operate.
    </div>

</div>
"""
)


c1, c2, c3 = st.columns(
    [1.25, 1, .8],
    gap="medium",
)


with c1:

    company_name = st.text_input(
        "Company",
        placeholder="e.g. Reliance Pvt Ltd",
    )


with c2:

    industry = st.text_input(
        "Industry",
        placeholder="e.g. Automotive",
    )


with c3:

    market = st.text_input(
        "Market",
        placeholder="e.g. India",
    )


# =========================================================
# PRIVATE COMPANY INTELLIGENCE
# =========================================================

st.html(
    """
<div style="
    margin-top:28px;
    margin-bottom:14px;
">

    <div style="
        font-family:'Manrope',sans-serif;
        font-size:21px;
        font-weight:800;
        color:#172033;
    ">
        📁 Private Company Intelligence
    </div>

    <div style="
        margin-top:5px;
        color:#64748b;
        font-size:13px;
    ">
        Upload internal company information so the AI can
        use your own business knowledge during analysis.
    </div>

</div>
"""
)


upload_col1, upload_col2 = st.columns(
    [1.7, 1],
    gap="medium",
)


with upload_col1:

    uploaded_files = st.file_uploader(
        "Upload Company Data",
        type=["pdf", "txt", "csv"],
        accept_multiple_files=True,
        help=(
            "Upload company documents or business data "
            "for private AI analysis."
        ),
    )


with upload_col2:

    st.html(
        """
<div style="
    margin-top:30px;
    padding:19px;
    border-radius:19px;
    background:
        linear-gradient(
            135deg,
            rgba(238,242,255,.90),
            rgba(236,254,255,.90)
        );
    border:1px solid #e0e7ff;
    box-shadow:
        0 12px 30px rgba(79,70,229,.06);
">

    <div style="
        color:#4338ca;
        font-size:12px;
        font-weight:850;
        letter-spacing:.8px;
    ">
        🔐 PRIVATE KNOWLEDGE
    </div>

    <div style="
        margin-top:7px;
        color:#64748b;
        font-size:12px;
        line-height:1.65;
    ">
        Documents are associated with the selected
        company and ingested into its private
        knowledge base.
    </div>

    <div style="
        margin-top:10px;
        color:#0891b2;
        font-size:11px;
        font-weight:750;
    ">
        PDF • TXT • CSV
    </div>

</div>
"""
    )


if uploaded_files:

    st.html(
        f"""
<div style="
    margin-top:12px;
    padding:13px 17px;
    border-radius:15px;
    background:#f0fdf4;
    border:1px solid #bbf7d0;
    color:#15803d;
    font-size:12px;
    font-weight:750;
">
    ✓ {len(uploaded_files)} company document(s) ready
    for private knowledge ingestion.
</div>
"""
    )


# =========================================================
# DECISION INPUT
# =========================================================

st.html(
    """
<div style="
    margin-top:25px;
    margin-bottom:14px;
">

    <div style="
        font-family:'Manrope',sans-serif;
        font-size:21px;
        font-weight:800;
        color:#172033;
    ">
        💡 What decision are you considering?
    </div>

    <div style="
        margin-top:5px;
        color:#64748b;
        font-size:13px;
    ">
        Be specific so the AI can evaluate the decision properly.
    </div>

</div>
"""
)


decision = st.text_area(
    "Business Decision",
    height=155,
    label_visibility="collapsed",
    placeholder=(
        "Example:\n"
        "Should I increase my investment in motor "
        "inventory by 10% this year?"
    ),
)


st.markdown(
    "<div style='height:8px'></div>",
    unsafe_allow_html=True,
)


analyze = st.button(
    "🚀  Analyze My Business Decision",
    use_container_width=True,
)

company_id = None
decision_for_ai = ""


# =========================================================
# ANALYSIS
# =========================================================

if analyze:

    if not decision.strip():

        st.warning(
            "Please describe your business decision first."
        )

    else:

        # -------------------------------------------------
        # COMPANY PROFILE
        # -------------------------------------------------

        company_id = None

        if company_name.strip():

            try:

                profile = create_profile(
                    company_name=company_name.strip(),
                    industry=industry.strip(),
                    market=market.strip(),
                )

                save_profile(profile)

                company_id = profile.company_id

            except Exception as profile_error:

                st.warning(
                    "Company profile could not be saved: "
                    f"{profile_error}"
                )


        # -------------------------------------------------
        # INTERNAL DOCUMENT INGESTION
        # -------------------------------------------------

        if uploaded_files:

            if not company_id:

                st.warning(
                    "Please enter a company name before "
                    "uploading internal company documents."
                )

            else:

                rag_engine = RAGEngine()

                successful_uploads = 0

                with st.spinner(
                    "📁 Processing private company documents..."
                ):

                    for uploaded_file in uploaded_files:

                        temp_path = None

                        suffix = Path(
                            uploaded_file.name
                        ).suffix.lower()

                        try:

                            with tempfile.NamedTemporaryFile(
                                delete=False,
                                suffix=suffix,
                            ) as temp_file:

                                temp_file.write(
                                    uploaded_file.getvalue()
                                )

                                temp_path = temp_file.name


                            rag_engine.ingest_document(
                                company_id=company_id,
                                file_path=temp_path,
                            )

                            successful_uploads += 1

                        except Exception as upload_error:

                            st.warning(
                                f"Could not process "
                                f"{uploaded_file.name}: "
                                f"{upload_error}"
                            )

                        finally:

                            if temp_path:

                                try:

                                    Path(
                                        temp_path
                                    ).unlink(
                                        missing_ok=True
                                    )

                                except Exception:

                                    pass


                if successful_uploads:

                    st.success(
                        f"✓ {successful_uploads} document(s) "
                        "added to the private company knowledge base."
                    )


        # -------------------------------------------------
        # EXISTING DECISION FLOW
        # -------------------------------------------------

        context_parts = []


        if company_name.strip():

            context_parts.append(
                f"Company: {company_name.strip()}"
            )


        if industry.strip():

            context_parts.append(
                f"Industry: {industry.strip()}"
            )


        if market.strip():

            context_parts.append(
                f"Market: {market.strip()}"
            )


        context_parts.append(
            f"Business Decision: {decision.strip()}"
        )


        decision_for_ai = "\n".join(
            context_parts
        )


# -------------------------------------------------
# INTELLIGENCE RETRIEVAL
# -------------------------------------------------

private_documents = []

public_pages = []

evidence_context = ""


# =================================================
# PRIVATE COMPANY RAG
# =================================================

if company_id and uploaded_files:

    try:

        rag_engine = RAGEngine()

        private_documents = rag_engine.retrieve(
            company_id=company_id,
            query=decision.strip(),
            k=4,
        )

    except Exception as rag_error:

        st.warning(
            "Private company knowledge could not be "
            f"retrieved: {rag_error}"
        )


# =================================================
# PUBLIC WEB INTELLIGENCE
# =================================================

try:

    web_research = research_business_market(
        company_name=company_name.strip(),
        industry=industry.strip(),
        market=market.strip(),
        business_decision=decision.strip(),
        max_results_per_query=2,
    )

    web_results = web_research.get(
        "results",
        [],
    )

    if web_results:

        web_urls = [
            result.url
            for result in web_results
            if getattr(result, "url", "")
        ]

        if web_urls:

            extracted_pages = extract_web_pages(
                urls=web_urls[:4],
                max_chars=6000,
            )

            public_pages = [
                page
                for page in extracted_pages
                if page.success
                and page.text.strip()
            ]

except Exception as web_error:

    st.warning(
        "Public web intelligence could not be retrieved: "
        f"{web_error}"
    )


# =================================================
# EVIDENCE FUSION
# =================================================

try:

    fused_evidence = fuse_evidence(
        private_documents=private_documents,
        public_results=public_pages,
    )

    evidence_context = fused_evidence.get(
        "context",
        "",
    )

except Exception as evidence_error:

    st.warning(
        "Evidence could not be assembled: "
        f"{evidence_error}"
    )

    evidence_context = ""


# -------------------------------------------------
# GEMINI ANALYSIS
# -------------------------------------------------

with st.spinner(
    "ðŸ§  AI is evaluating your decision..."
):

    response = analyze_business_decision(
        decision_for_ai,
        evidence_context=evidence_context,
    )


    result = parse_ai_response(
        response
    )

    # =================================================
    # RESULT HEADER
    # =================================================

    st.html(
        """
<div style="
    margin-top:45px;
    margin-bottom:18px;
    display:flex;
    justify-content:space-between;
    align-items:end;
">

    <div>

        <div style="
            color:#6366f1;
            font-size:11px;
            font-weight:900;
            letter-spacing:1.6px;
            text-transform:uppercase;
        ">
            AI ASSESSMENT
        </div>

        <div style="
            margin-top:5px;
            font-family:'Manrope',sans-serif;
            font-size:29px;
            font-weight:800;
            letter-spacing:-.8px;
            color:#172033;
        ">
            Decision Analysis
        </div>

    </div>


    <div style="
        padding:8px 13px;
        border-radius:999px;
        background:#ecfdf5;
        border:1px solid #bbf7d0;
        color:#15803d;
        font-size:11px;
        font-weight:850;
    ">
        ✓ ANALYSIS COMPLETE
    </div>

</div>
"""
    )


    # =================================================
    # METRICS
    # =================================================

    risk, risk_color, risk_bg, risk_caption = risk_data(
        result["risk"]
    )

    confidence = confidence_number(
        result["confidence"]
    )

    m1, m2, m3 = st.columns(
        3,
        gap="medium",
    )


    # -------------------------------------------------
    # RISK
    # -------------------------------------------------

    with m1:

        st.html(
            f"""
<div style="
    min-height:138px;
    padding:22px;
    border-radius:22px;
    background:rgba(255,255,255,.92);
    border:1px solid rgba(226,232,240,.95);
    box-shadow:
        0 15px 38px rgba(15,23,42,.065);
    animation:slideUp .5s ease;
">

    <div style="
        color:#94a3b8;
        font-size:10px;
        font-weight:900;
        letter-spacing:1.2px;
        text-transform:uppercase;
    ">
        Risk Level
    </div>


    <div style="
        margin-top:13px;
        display:flex;
        align-items:center;
        gap:10px;
    ">

        <div style="
            width:13px;
            height:13px;
            border-radius:50%;
            background:{risk_color};
            box-shadow:
                0 0 15px {risk_color};
        "></div>


        <div style="
            color:{risk_color};
            font-size:25px;
            font-weight:900;
        ">
            {risk}
        </div>

    </div>


    <div style="
        margin-top:8px;
        color:#94a3b8;
        font-size:12px;
    ">
        {risk_caption}
    </div>

</div>
"""
        )


    # -------------------------------------------------
    # CONFIDENCE
    # -------------------------------------------------

    with m2:

        st.html(
            f"""
<div style="
    min-height:138px;
    padding:22px;
    border-radius:22px;
    background:
        linear-gradient(
            145deg,
            #ffffff,
            #f5f3ff
        );
    border:1px solid #e0e7ff;
    box-shadow:
        0 15px 38px rgba(79,70,229,.07);
    animation:slideUp .6s ease;
">

    <div style="
        color:#94a3b8;
        font-size:10px;
        font-weight:900;
        letter-spacing:1.2px;
        text-transform:uppercase;
    ">
        AI Confidence
    </div>


    <div style="
        margin-top:6px;
        color:#4338ca;
        font-family:'Manrope',sans-serif;
        font-size:34px;
        font-weight:900;
    ">
        {confidence:.0f}%
    </div>


    <div style="
        height:7px;
        margin-top:9px;
        overflow:hidden;
        border-radius:999px;
        background:#e0e7ff;
    ">

        <div style="
            width:{min(confidence,100):.0f}%;
            height:100%;
            border-radius:999px;
            background:
                linear-gradient(
                    90deg,
                    #4338ca,
                    #6366f1,
                    #06b6d4
                );
        "></div>

    </div>

</div>
"""
        )


    # -------------------------------------------------
    # MODE
    # -------------------------------------------------

    with m3:

        st.html(
            """
<div style="
    min-height:138px;
    padding:22px;
    border-radius:22px;
    background:
        linear-gradient(
            145deg,
            #ecfeff,
            #ffffff
        );
    border:1px solid #cffafe;
    box-shadow:
        0 15px 38px rgba(6,182,212,.065);
    animation:slideUp .7s ease;
">

    <div style="
        color:#94a3b8;
        font-size:10px;
        font-weight:900;
        letter-spacing:1.2px;
        text-transform:uppercase;
    ">
        Intelligence Mode
    </div>


    <div style="
        margin-top:12px;
        color:#0e7490;
        font-family:'Manrope',sans-serif;
        font-size:21px;
        font-weight:900;
    ">
        AI Evaluation
    </div>


    <div style="
        margin-top:7px;
        color:#94a3b8;
        font-size:12px;
    ">
        Business decision reasoning
    </div>

</div>
"""
        )


    # =================================================
    # SUMMARY
    # =================================================

    st.html(
        f"""
<div style="
    margin-top:22px;
    padding:29px;
    border-radius:23px;
    background:rgba(255,255,255,.94);
    border:1px solid #e5eaf2;
    box-shadow:
        0 15px 40px rgba(15,23,42,.055);
    animation:slideUp .8s ease;
">

    <div style="
        display:flex;
        align-items:center;
        gap:10px;
        color:#4f46e5;
        font-size:12px;
        font-weight:900;
        letter-spacing:1.2px;
        text-transform:uppercase;
        margin-bottom:13px;
    ">
        ◈ Decision Summary
    </div>


    <div style="
        color:#334155;
        font-size:16px;
        line-height:1.85;
        font-weight:500;
    ">
        {html.escape(result["summary"])}
    </div>

</div>
"""
    )


    # =================================================
    # REASONS
    # =================================================

    if result["reasons"]:

        reason_html = ""

        for index, reason in enumerate(
            result["reasons"],
            start=1,
        ):

            reason_html += f"""
<div style="
    display:flex;
    gap:15px;
    padding:15px 0;
    border-bottom:1px solid #eef2f7;
">

    <div style="
        min-width:33px;
        height:33px;
        display:flex;
        align-items:center;
        justify-content:center;
        border-radius:11px;
        background:
            linear-gradient(
                135deg,
                #eef2ff,
                #e0f2fe
            );
        color:#4338ca;
        font-size:12px;
        font-weight:900;
    ">
        {index}
    </div>


    <div style="
        color:#475569;
        font-size:15px;
        line-height:1.75;
        padding-top:2px;
    ">
        {html.escape(reason)}
    </div>

</div>
"""

        st.html(
            f"""
<div style="
    margin-top:22px;
    padding:29px;
    border-radius:23px;
    background:rgba(255,255,255,.94);
    border:1px solid #e5eaf2;
    box-shadow:
        0 15px 40px rgba(15,23,42,.055);
    animation:slideUp .9s ease;
">

    <div style="
        color:#0891b2;
        font-size:12px;
        font-weight:900;
        letter-spacing:1.2px;
        text-transform:uppercase;
    ">
        Why AI reached this assessment
    </div>


    <div style="
        color:#94a3b8;
        font-size:12px;
        margin-top:5px;
        margin-bottom:8px;
    ">
        Key factors identified from the decision.
    </div>


    {reason_html}

</div>
"""
        )


    # =================================================
    # RECOMMENDATION
    # =================================================

    st.html(
        f"""
<div style="
    position:relative;
    overflow:hidden;
    margin-top:22px;
    padding:31px;
    border-radius:25px;
    background:
        linear-gradient(
            115deg,
            #eef2ff,
            #ecfeff 55%,
            #fdf2f8
        );
    border:1px solid #c7d2fe;
    box-shadow:
        0 18px 45px rgba(79,70,229,.10);
    animation:slideUp 1s ease;
">


    <!-- DECORATIVE MOVING SPOT ONLY -->

    <div style="
        position:absolute;
        right:-40px;
        top:-50px;
        width:150px;
        height:150px;
        border-radius:50%;
        background:
            radial-gradient(
                circle,
                rgba(99,102,241,.10),
                transparent 72%
            );
        animation:
            cinematicOrbOne 16s ease-in-out infinite;
    "></div>


    <div style="
        position:relative;
        z-index:2;
    ">

        <div style="
            color:#db2777;
            font-size:12px;
            font-weight:900;
            letter-spacing:1.3px;
            text-transform:uppercase;
            margin-bottom:12px;
        ">
            🎯 Recommended Next Step
        </div>


        <div style="
            color:#1e293b;
            font-family:'Manrope',sans-serif;
            font-size:17px;
            line-height:1.85;
            font-weight:650;
            max-width:950px;
        ">
            {html.escape(result["recommendation"])}
        </div>

    </div>

</div>
"""
    )


    # =================================================
    # DECISION ARCHITECTURE
    # =================================================

    st.html(
        """
<div style="
    margin-top:31px;
    padding:22px;
    border-radius:21px;
    background:rgba(255,255,255,.82);
    border:1px solid #e5eaf2;
    box-shadow:
        0 10px 30px rgba(15,23,42,.045);
">

    <div style="
        color:#64748b;
        font-size:10px;
        font-weight:900;
        letter-spacing:1.3px;
        text-transform:uppercase;
        margin-bottom:15px;
    ">
        Decision Intelligence Flow
    </div>


    <div style="
        display:flex;
        justify-content:center;
        align-items:center;
        gap:9px;
        flex-wrap:wrap;
    ">


        <span style="
            padding:9px 13px;
            border-radius:12px;
            background:#eef2ff;
            color:#4338ca;
            font-size:11px;
            font-weight:800;
        ">
            🏢 Context
        </span>


        <span style="
            color:#cbd5e1;
            font-weight:800;
        ">
            →
        </span>


        <span style="
            padding:9px 13px;
            border-radius:12px;
            background:#ecfeff;
            color:#0e7490;
            font-size:11px;
            font-weight:800;
        ">
            🧠 AI Reasoning
        </span>


        <span style="
            color:#cbd5e1;
            font-weight:800;
        ">
            →
        </span>


        <span style="
            padding:9px 13px;
            border-radius:12px;
            background:#fff7ed;
            color:#c2410c;
            font-size:11px;
            font-weight:800;
        ">
            📊 Risk
        </span>


        <span style="
            color:#cbd5e1;
            font-weight:800;
        ">
            →
        </span>


        <span style="
            padding:9px 13px;
            border-radius:12px;
            background:#fdf2f8;
            color:#be185d;
            font-size:11px;
            font-weight:800;
        ">
            🎯 Action
        </span>

    </div>

</div>
"""
    )


# =========================================================
# PREMIUM FOOTER
# =========================================================

st.html(
    """
<div style="
    margin-top:60px;
    padding-top:25px;
    text-align:center;
    border-top:1px solid rgba(148,163,184,.18);
">

    <div style="
        color:#94a3b8;
        font-size:10px;
        letter-spacing:1.4px;
        text-transform:uppercase;
        font-weight:700;
    ">
        Business DecisionAI
    </div>


    <div style="
        margin-top:8px;
        font-family:'DM Sans',sans-serif;
        font-size:11px;
        font-style:italic;
        font-weight:500;
        letter-spacing:.8px;
        color:#8b91a7;
    ">
        — made by Jyoti Chaudhary —
    </div>


    <div style="
        margin-top:6px;
        color:#cbd5e1;
        font-size:10px;
    ">
        AI • Business Intelligence • Decision Support
    </div>

</div>
"""
)