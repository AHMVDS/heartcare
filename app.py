import pandas as pd
import plotly.graph_objects as go
import streamlit as st
 
from core import ROOT, predict
 
 
# =========================================================
# PAGE CONFIG
# =========================================================
 
st.set_page_config(
    page_title="HeartCare",
    layout="wide",
    initial_sidebar_state="auto",
)
 
 
# =========================================================
# LANGUAGE STATE
# =========================================================
 
if "language" not in st.session_state:
    st.session_state.language = "English"
 
 
def switch_language():
    if st.session_state.language == "English":
        st.session_state.language = "العربية"
    else:
        st.session_state.language = "English"
 
 
language = st.session_state.language
AR = language == "العربية"
 
 
# =========================================================
# TRANSLATIONS (unchanged)
# =========================================================
 
translations = {
    "English": {
        "title": "HeartCare",
        "subtitle": "PATIENT OVERVIEW / SINGLE & BULK ANALYSIS",
        "warning": "DEMONSTRATION ONLY • Both models use synthetic data. "
        "Risk scores and levels are not medical risk estimates "
        "and must not guide patient care.",
        "single_patient": "Single Patient",
        "prediction_model": "Prediction Model",
        "age": "Age (years)",
        "sex": "Sex",
        "male": "M",
        "female": "F",
        "bp": "Systolic Blood Pressure (mmHg)",
        "cholesterol": "Total Cholesterol (mg/dL)",
        "bmi": "BMI (kg/m²)",
        "smoker": "Smoker",
        "no": "No",
        "yes": "Yes",
        "predict": "Predict Risk Score",
        "units": "Units above are assumptions to confirm "
        "with the final model.",
        "dashboard": "Patient Dashboard",
        "score": "Risk Score",
        "band": "Risk Level",
        "model_used": "Model Used",
        "patient_details": "Patient Details",
        "bands": "Risk levels: Low <30%, Medium 30\u2013<60%, High \u226560%. "
        "These thresholds are for demonstration purposes only.",
        "enter_patient": "Enter the patient information in the sidebar "
        "and select \u201cPredict Risk Score\u201d to display the result.",
        "bulk": "Bulk Patient Analysis",
        "bulk_description": "Upload a CSV file to calculate a risk score for every "
        "patient using the selected model.",
        "upload": "Patient CSV · up to 5 MB / 10,000 rows",
        "download_sample": "Download Sample CSV",
        "use_sample": "Use 10-Patient Sample",
        "csv_format": "CSV Format & Validation",
        "csv_help": "Required model fields: age, sex, blood_pressure, "
        "cholesterol, bmi and smoker. Sex must be M/F and "
        "Smoker must be Yes/No. patient_id is optional; "
        "if supplied, IDs must be unique. Invalid or incomplete "
        "batches are rejected. Extra columns are retained but "
        "are not used by the models.",
        "file_limit": "File exceeds the 5 MB limit.",
        "patients": "Patients",
        "low": "Low",
        "medium": "Medium",
        "high": "High",
        "low_risk": "Low Risk",
        "medium_risk": "Medium Risk",
        "high_risk": "High Risk",
        "bulk_model": "Bulk Model",
        "synthetic_demo": "Synthetic Demonstration",
        "score_column": "Risk Score (%)",
        "distribution": "Distribution of Risk Levels",
        "patients_axis": "Patients",
        "download_results": "Download Results",
        "error": "Unable to process this batch",
        "footer": "HeartCare AI · Uploaded records are processed during "
        "the current session only. This application does not "
        "contain a patient-history database.",
    },
    "العربية": {
        "title": "Heart Care",
        "subtitle": "نظرة عامة على المريض / التحليل الفردي والجماعي",
        "warning": "لأغراض العرض فقط • يستخدم كلا النموذجين بيانات صناعية "
        "تجريبية. نسب ومستويات الخطر لا تمثل تقديرًا طبيًا حقيقيًا "
        "ولا يجب استخدامها لاتخاذ قرارات علاجية.",
        "single_patient": "إدخال مريض واحد",
        "prediction_model": "نموذج التنبؤ",
        "age": "العمر (بالسنوات)",
        "sex": "الجنس",
        "male": "ذكر",
        "female": "أنثى",
        "bp": "ضغط الدم الانقباضي (mmHg)",
        "cholesterol": "الكوليسترول الكلي (mg/dL)",
        "bmi": "مؤشر كتلة الجسم BMI (kg/m²)",
        "smoker": "هل المريض مدخن؟",
        "no": "لا",
        "yes": "نعم",
        "predict": "توقع نسبة الخطر",
        "units": "الوحدات المستخدمة افتراضية ويجب تأكيدها "
        "مع النموذج النهائي.",
        "dashboard": "لوحة بيانات المريض",
        "score": "نسبة الخطر",
        "band": "مستوى الخطر",
        "model_used": "النموذج المستخدم",
        "patient_details": "بيانات المريض",
        "bands": "مستويات الخطر: منخفض أقل من 30%، "
        "متوسط من 30% إلى أقل من 60%، "
        "ومرتفع 60% أو أكثر. هذه الحدود مخصصة "
        "للعرض التجريبي فقط.",
        "enter_patient": "أدخل بيانات المريض من القائمة الجانبية، "
        "ثم اضغط \u00abتوقع نسبة الخطر\u00bb لعرض النتيجة.",
        "bulk": "تحليل مجموعة من المرضى",
        "bulk_description": "ارفع ملف CSV لحساب نسبة الخطر لكل مريض "
        "باستخدام نموذج التنبؤ المحدد.",
        "upload": "ملف CSV للمرضى · بحد أقصى 5 MB / 10,000 صف",
        "download_sample": "تحميل ملف CSV تجريبي",
        "use_sample": "استخدام عينة 10 مرضى",
        "csv_format": "تنسيق ملف CSV والتحقق من البيانات",
        "csv_help": "الحقول المطلوبة للنموذج هي: العمر، الجنس، ضغط الدم، "
        "الكوليسترول، BMI والتدخين. داخل ملف CSV يجب أن تكون "
        "قيمة الجنس M أو F، والتدخين Yes أو No. معرف المريض "
        "patient_id اختياري، وإذا تم إدخاله فيجب أن يكون فريدًا. "
        "سيتم رفض الملفات التي تحتوي على بيانات ناقصة أو غير صحيحة.",
        "file_limit": "حجم الملف يتجاوز الحد المسموح وهو 5 MB.",
        "patients": "عدد المرضى",
        "low": "منخفض",
        "medium": "متوسط",
        "high": "مرتفع",
        "low_risk": "خطر منخفض",
        "medium_risk": "خطر متوسط",
        "high_risk": "خطر مرتفع",
        "bulk_model": "نموذج التحليل",
        "synthetic_demo": "عرض تجريبي ببيانات صناعية",
        "score_column": "نسبة الخطر (%)",
        "distribution": "توزيع مستويات الخطر",
        "patients_axis": "عدد المرضى",
        "download_results": "تحميل نتائج التحليل",
        "error": "تعذر معالجة البيانات",
        "footer": "HeartCare AI · تتم معالجة البيانات المرفوعة خلال "
        "الجلسة الحالية فقط، ولا يحتوي التطبيق على قاعدة "
        "بيانات لتخزين تاريخ المرضى.",
    },
}
 
t = translations[language]
 
 
# =========================================================
# RTL / LTR
# =========================================================
 
direction = "rtl" if AR else "ltr"
text_align = "right" if AR else "left"
 
 
# =========================================================
# DESIGN SYSTEM — deep red / burgundy / navy / soft gray
# =========================================================
 
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,500;9..144,650&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
 
:root {
    --red: #991B1B;
    --red-bright: #C0262D;
    --burgundy: #5B0F1E;
    --navy: #0B1424;
    --navy-2: #14213A;
    --ink: #1E293B;
    --muted: #64748B;
    --mist: #F6F1F2;
    --line: rgba(91, 15, 30, 0.12);
    --glass: rgba(255, 255, 255, 0.72);
    --shadow: 0 1px 2px rgba(91,15,30,.06), 0 12px 32px -12px rgba(91,15,30,.22);
    --shadow-hover: 0 2px 4px rgba(91,15,30,.08), 0 22px 44px -14px rgba(91,15,30,.34);
    --ease: cubic-bezier(.22,.8,.26,1);
}
 
/* ---------- Type ---------- */
html, body, .stApp, .stApp p, .stApp label, .stApp li,
.stApp input, .stApp textarea, .stApp button,
[data-baseweb] div, [data-testid="stCaptionContainer"] {
    font-family: 'Plus Jakarta Sans', 'Cairo', system-ui, sans-serif;
}
h1, h2, h3, [data-testid="stHeading"] {
    font-family: 'Fraunces', 'Cairo', Georgia, serif !important;
}
[data-testid="stIconMaterial"] {
    font-family: 'Material Symbols Rounded' !important;
}
 
/* ---------- Ambient stage ---------- */
.stApp {
    direction: __DIR__;
    background:
        radial-gradient(900px 520px at 88% -8%, rgba(192,38,45,.13), transparent 60%),
        radial-gradient(760px 520px at -6% 28%, rgba(91,15,30,.09), transparent 62%),
        radial-gradient(700px 480px at 70% 108%, rgba(20,33,58,.10), transparent 60%),
        linear-gradient(180deg, #FFFFFF 0%, #F7F2F3 100%);
    background-attachment: fixed;
}
.stApp::before {
    content: "";
    position: fixed;
    inset: auto auto -180px -140px;
    width: 460px; height: 460px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(192,38,45,.16), transparent 68%);
    animation: breathe 5.2s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}
.stApp p, .stApp label { text-align: __ALIGN__; }
 
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 3.6rem; padding-bottom: 3rem; max-width: 1250px; }
 
/* ---------- Headings ---------- */
h1 {
    font-size: 3.1rem !important;
    font-weight: 650 !important;
    letter-spacing: -1px;
    margin-bottom: .1rem !important;
    background: linear-gradient(100deg, var(--burgundy) 10%, var(--red-bright) 85%);
    -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent;
}
h1, h2, h3 { text-align: __ALIGN__; }
h2, h3 {
    color: var(--burgundy) !important;
    font-weight: 600 !important;
    letter-spacing: -.3px;
}
[data-testid="stCaptionContainer"] { color: var(--muted); }
 
/* ---------- Hero heartbeat ---------- */
.hc-hero {
    display: flex; align-items: center; gap: 14px;
    margin: .2rem 0 .4rem;
    direction: __DIR__;
}
.hc-heart { width: 42px; height: 42px; flex: none; transform-origin: center;
    animation: heartbeat 1.6s ease-in-out infinite;
    filter: drop-shadow(0 6px 10px rgba(153,27,27,.38)); }
.hc-ecg { direction: ltr; flex: 1; height: 46px; min-width: 0; }
.hc-ecg path {
    fill: none; stroke: var(--red); stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;
    stroke-dasharray: 700; stroke-dashoffset: 700;
    animation: trace 3.4s var(--ease) infinite;
}
.hc-ecg .ghost { stroke: rgba(91,15,30,.14); stroke-dasharray: none; animation: none; }
 
/* ---------- Alerts (demo warning stays prominent) ---------- */
[data-testid="stAlert"] {
    border-radius: 16px;
    border: 1px solid var(--line);
    backdrop-filter: blur(10px);
    box-shadow: var(--shadow);
    animation: rise .6s var(--ease) both;
}
 
/* ---------- Sidebar: navy glass ---------- */
[data-testid="stSidebar"] {
    direction: __DIR__;
    background:
        radial-gradient(420px 320px at 100% 0%, rgba(192,38,45,.28), transparent 65%),
        linear-gradient(185deg, var(--navy-2) 0%, var(--navy) 100%);
    border-inline-end: 1px solid rgba(255,255,255,.06);
}
[data-testid="stSidebar"] > div { padding-top: 1rem; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label, [data-testid="stSidebar"] p,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #F3E8EA !important;
    -webkit-text-fill-color: #F3E8EA;
    background: none;
}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color: #A8B3C7 !important; -webkit-text-fill-color: #A8B3C7; }
[data-testid="stSidebar"] [data-testid="stForm"] {
    background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 18px;
    padding: 1.1rem 1rem .9rem;
    backdrop-filter: blur(14px);
}
[data-testid="stSidebar"] [data-baseweb="input"],
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,.96) !important;
    border-radius: 12px;
    border: 1px solid transparent;
    transition: box-shadow .25s var(--ease), border-color .25s var(--ease);
}
[data-testid="stSidebar"] [data-baseweb="input"] input,
[data-testid="stSidebar"] [data-baseweb="select"] div { color: var(--ink) !important; -webkit-text-fill-color: var(--ink); }
[data-testid="stSidebar"] [data-baseweb="input"]:focus-within,
[data-testid="stSidebar"] [data-baseweb="select"] > div:hover {
    box-shadow: 0 0 0 3px rgba(192,38,45,.45);
}
[data-baseweb="input"], [data-baseweb="select"] { border-radius: 12px; }
 
/* ---------- Metric cards: layered glass ---------- */
[data-testid="stMetric"] {
    position: relative;
    background: var(--glass);
    backdrop-filter: blur(14px);
    padding: 20px 22px;
    border-radius: 20px;
    border: 1px solid var(--line);
    border-inline-start: 4px solid var(--red);
    box-shadow: var(--shadow);
    animation: rise .7s var(--ease) both;
    transition: transform .35s var(--ease), box-shadow .35s var(--ease);
}
[data-testid="stMetric"]:hover { transform: translateY(-4px); box-shadow: var(--shadow-hover); }
[data-testid="stMetricLabel"] { font-weight: 600; color: var(--muted); }
[data-testid="stMetricValue"] {
    font-family: 'Fraunces', 'Cairo', serif;
    color: var(--burgundy);
    font-weight: 650;
}
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"] { animation-delay: .12s; }
 
/* ---------- Charts, tables, uploader, expander as soft cards ---------- */
[data-testid="stPlotlyChart"] {
    background: var(--glass);
    border: 1px solid var(--line);
    border-radius: 22px;
    box-shadow: var(--shadow);
    padding: 8px;
    animation: rise .8s var(--ease) both;
}
[data-testid="stDataFrame"] {
    border-radius: 18px; overflow: hidden;
    border: 1px solid var(--line);
    box-shadow: var(--shadow);
    animation: rise .8s var(--ease) both;
}
[data-testid="stFileUploader"] section {
    background: var(--glass);
    border: 1.5px dashed rgba(153,27,27,.4);
    border-radius: 20px;
    transition: all .3s var(--ease);
}
[data-testid="stFileUploader"] section:hover {
    border-color: var(--red);
    background: rgba(255,255,255,.95);
    box-shadow: 0 0 0 5px rgba(192,38,45,.10);
}
[data-testid="stExpander"] {
    background: var(--glass);
    border: 1px solid var(--line) !important;
    border-radius: 18px;
    box-shadow: var(--shadow);
}
[data-testid="stExpander"] summary { font-weight: 600; color: var(--burgundy); }
.stApp pre, .stApp code { border-radius: 12px; }
 
/* ---------- Buttons ---------- */
.stDownloadButton button,
[data-testid="stFormSubmitButton"] button {
    border-radius: 14px !important;
    font-weight: 650 !important;
    min-height: 48px;
    letter-spacing: .1px;
    transition: transform .25s var(--ease), box-shadow .25s var(--ease), background .25s var(--ease);
}
.stDownloadButton button {
    background: #FFFFFF; color: var(--burgundy); border: 1px solid rgba(153,27,27,.45);
}
.stDownloadButton button:hover {
    background: var(--burgundy); color: #fff; border-color: var(--burgundy);
    transform: translateY(-2px); box-shadow: var(--shadow-hover);
}
[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, var(--red-bright), var(--burgundy)) !important;
    border: none !important; color: #fff !important;
    animation: ring 2.8s ease-out infinite;
}
[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-2px) scale(1.015);
    box-shadow: 0 16px 30px -10px rgba(192,38,45,.7);
    animation: none;
}
[data-testid="stFormSubmitButton"] button:active, .stDownloadButton button:active { transform: scale(.98); }
 
div[data-testid="stButton"] > button {
    background: rgba(255,255,255,.9) !important;
    color: var(--red) !important;
    border: 1px solid var(--red) !important;
    border-radius: 22px !important;
    font-weight: 650 !important;
    min-height: 42px !important;
    padding: .45rem 1rem !important;
    transition: all .3s var(--ease);
    backdrop-filter: blur(8px);
}
div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, var(--red-bright), var(--burgundy)) !important;
    color: #fff !important; border-color: transparent !important;
    transform: translateY(-2px); box-shadow: var(--shadow-hover);
}
div[data-testid="stButton"] > button:active { transform: scale(.98); }
.stApp button:focus-visible, .stApp input:focus-visible { outline: 3px solid rgba(192,38,45,.5) !important; outline-offset: 2px; }
 
hr {
    margin: 2.2rem 0 !important; border: 0 !important; height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(153,27,27,.4), transparent) !important;
}
 
/* ---------- Motion ---------- */
@keyframes rise { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: none; } }
@keyframes heartbeat {
    0%, 100% { transform: scale(1); } 14% { transform: scale(1.16); }
    28% { transform: scale(1); } 42% { transform: scale(1.1); } 56% { transform: scale(1); }
}
@keyframes trace { 0% { stroke-dashoffset: 700; } 55%, 85% { stroke-dashoffset: 0; } 100% { stroke-dashoffset: -700; } }
@keyframes breathe { 0%, 100% { transform: scale(1); opacity: .7; } 50% { transform: scale(1.18); opacity: 1; } }
@keyframes ring { 0% { box-shadow: 0 0 0 0 rgba(192,38,45,.55); } 70%, 100% { box-shadow: 0 0 0 16px rgba(192,38,45,0); } }
 
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation: none !important; transition: none !important; }
    .hc-ecg path { stroke-dashoffset: 0; }
}
 
/* ---------- Mobile / tablet ---------- */
@media (max-width: 768px) {
    .block-container { padding: 3.4rem 1rem 2rem !important; }
    h1 { font-size: 2.2rem !important; line-height: 1.2 !important; }
    h2 { font-size: 1.5rem !important; }
    h3 { font-size: 1.25rem !important; }
    p, label { font-size: .95rem !important; }
    .stButton button, .stDownloadButton button, [data-testid="stFormSubmitButton"] button {
        min-height: 46px !important; font-size: .95rem !important;
    }
    input, textarea, [data-baseweb="select"] { font-size: 16px !important; }
    [data-testid="stMetric"] { padding: 14px !important; border-radius: 16px !important; }
    [data-testid="stMetricValue"] { font-size: 1.45rem !important; }
    [data-testid="stPlotlyChart"] { width: 100% !important; max-width: 100% !important; overflow: hidden !important; }
    [data-testid="stDataFrame"] { width: 100% !important; max-width: 100% !important; overflow-x: auto !important; }
    [data-testid="stAlert"] { font-size: .9rem !important; }
    .hc-heart { width: 34px; height: 34px; }
}
@media (max-width: 480px) {
    .block-container { padding-left: .7rem !important; padding-right: .7rem !important; }
    h1 { font-size: 1.8rem !important; }
    h2 { font-size: 1.3rem !important; }
    h3 { font-size: 1.1rem !important; }
    [data-testid="stMetricValue"] { font-size: 1.25rem !important; }
    [data-testid="stMetric"] { padding: 10px !important; }
    div[data-testid="stButton"] > button { font-size: .88rem !important; padding: .35rem .7rem !important; }
}
</style>
"""
 
st.markdown(
    CSS.replace("__DIR__", direction).replace("__ALIGN__", text_align),
    unsafe_allow_html=True,
)
 
 
# =========================================================
# LANGUAGE SWITCH
# =========================================================
 
top_space, language_column = st.columns([7.5, 2.5])
 
with language_column:
 
    st.button(
        "اللغة: English" if AR else "Language: العربية",
        key="language_switch",
        on_click=switch_language,
        width="stretch",
    )
 
 
# =========================================================
# HEADER (decorative heartbeat + original text)
# =========================================================
 
st.markdown(
    """
<div class="hc-hero" aria-hidden="true">
  <svg class="hc-heart" viewBox="0 0 32 32">
    <defs><linearGradient id="hg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#D93A41"/><stop offset="1" stop-color="#5B0F1E"/></linearGradient></defs>
    <path fill="url(#hg)" d="M16 28.5C5 20.6 2.5 14.4 2.5 10.2 2.5 6.2 5.6 3.5 9.2 3.5c2.7 0 5 1.5 6.8 4.1 1.8-2.6 4.1-4.1 6.8-4.1 3.6 0 6.7 2.7 6.7 6.7 0 4.2-2.5 10.4-13.5 18.3z"/>
  </svg>
  <svg class="hc-ecg" viewBox="0 0 600 46" preserveAspectRatio="none">
    <path class="ghost" d="M0 23H150l12-4 10 4h40l10-20 14 40 12-20h30l14-6 14 6h340"/>
    <path d="M0 23H150l12-4 10 4h40l10-20 14 40 12-20h30l14-6 14 6h340"/>
  </svg>
</div>
""",
    unsafe_allow_html=True,
)
 
st.title(t["title"])
 
st.caption(t["subtitle"])
 
st.warning(t["warning"])
 
 
# =========================================================
# SIDEBAR — SINGLE PATIENT
# =========================================================
 
with st.sidebar:
 
    st.header(t["single_patient"])
 
    model_label = st.selectbox(
        t["prediction_model"],
        [
            "XGBoost",
            "Logistic Regression",
        ],
    )
 
    if model_label == "XGBoost":
        model = "xgboost"
    else:
        model = "lr"
 
    with st.form("single_patient"):
 
        age = st.number_input(
            t["age"],
            min_value=18,
            max_value=120,
            value=45,
        )
 
        sex_display = st.selectbox(
            t["sex"],
            [
                t["male"],
                t["female"],
            ],
        )
 
        if sex_display == t["male"]:
            sex = "M"
        else:
            sex = "F"
 
        bp = st.number_input(
            t["bp"],
            min_value=60,
            max_value=260,
            value=120,
        )
 
        cholesterol = st.number_input(
            t["cholesterol"],
            min_value=70,
            max_value=600,
            value=200,
        )
 
        bmi = st.number_input(
            t["bmi"],
            min_value=10.0,
            max_value=70.0,
            value=24.5,
            step=0.1,
        )
 
        smoker_display = st.selectbox(
            t["smoker"],
            [
                t["no"],
                t["yes"],
            ],
        )
 
        if smoker_display == t["yes"]:
            smoker = "Yes"
        else:
            smoker = "No"
 
        submitted = st.form_submit_button(
            t["predict"],
            type="primary",
            width="stretch",
        )
 
    st.caption(t["units"])
 
 
# =========================================================
# SINGLE PATIENT PREDICTION
# =========================================================
 
if submitted:
 
    record = pd.DataFrame(
        [
            {
                "age": age,
                "sex": sex,
                "blood_pressure": bp,
                "cholesterol": cholesterol,
                "bmi": bmi,
                "smoker": smoker,
            }
        ]
    )
 
    try:
 
        prediction = predict(
            record,
            model,
        )
 
        st.session_state["single"] = (
            prediction
            .iloc[0]
            .to_dict()
        )
 
    except (
        ValueError,
        FileNotFoundError,
    ) as exc:
 
        st.error(str(exc))
 
 
# =========================================================
# PATIENT DASHBOARD
# =========================================================
 
st.subheader(t["dashboard"])
 
 
if "single" in st.session_state:
 
    row = st.session_state["single"]
 
    gauge = go.Figure(
 
        go.Indicator(
 
            mode="gauge+number",
 
            value=row["demo_score_percent"],
 
            number={
                "suffix": "%",
                "font": {
                    "size": 44,
                    "color": "#5B0F1E",
                },
            },
 
            title={
                "text": t["score"],
                "font": {
                    "size": 16,
                    "color": "#64748B",
                },
            },
 
            gauge={
 
                "axis": {
                    "range": [0, 100],
                    "tickcolor": "#94A3B8",
                },
 
                "bar": {
                    "color": "#991B1B",
                    "thickness": 0.28,
                },
 
                "borderwidth": 0,
 
                "steps": [
 
                    {
                        "range": [0, 30],
                        "color": "#DDEBE7",
                    },
 
                    {
                        "range": [30, 60],
                        "color": "#F4E9CC",
                    },
 
                    {
                        "range": [60, 100],
                        "color": "#F3D6D8",
                    },
                ],
            },
        )
    )
 
    gauge.update_layout(
 
        height=300,
 
        margin=dict(
            t=65,
            b=20,
            l=30,
            r=30,
        ),
 
        paper_bgcolor="rgba(0,0,0,0)",
 
        font_color="#334155",
 
        font_family="Plus Jakarta Sans, Cairo, sans-serif",
    )
 
    gauge_col, info_col = st.columns(
        [1.5, 1],
        gap="large",
    )
 
    with gauge_col:
 
        st.plotly_chart(
            gauge,
            width="stretch",
        )
 
    with info_col:
 
        risk_translation = {
 
            "Low": t["low"],
 
            "Medium": t["medium"],
 
            "High": t["high"],
        }
 
        displayed_risk = risk_translation.get(
            row["demo_band"],
            row["demo_band"],
        )
 
        st.metric(
            t["band"],
            displayed_risk,
        )
 
        st.write(
            f'**{t["model_used"]}:** '
            f'{row["model"]}'
        )
 
        if AR:
 
            if row["sex"] == "M":
                patient_sex = "ذكر"
            else:
                patient_sex = "أنثى"
 
            if row["smoker"] == "Yes":
                patient_smoker = "نعم"
            else:
                patient_smoker = "لا"
 
            st.caption(
                f'**{t["patient_details"]}:**  '
                f'العمر {row["age"]} سنة · '
                f'الجنس {patient_sex} · '
                f'ضغط الدم {row["blood_pressure"]} · '
                f'الكوليسترول {row["cholesterol"]} · '
                f'BMI {row["bmi"]} · '
                f'مدخن {patient_smoker}'
            )
 
        else:
 
            st.caption(
                f'**{t["patient_details"]}:**  '
                f'Age {row["age"]} · '
                f'Sex {row["sex"]} · '
                f'BP {row["blood_pressure"]} · '
                f'Cholesterol {row["cholesterol"]} · '
                f'BMI {row["bmi"]} · '
                f'Smoker {row["smoker"]}'
            )
 
        st.caption(
            t["bands"]
        )
 
else:
 
    st.info(
        t["enter_patient"]
    )
 
 
# =========================================================
# BULK PATIENT ANALYSIS
# =========================================================
 
st.divider()
 
st.subheader(
    t["bulk"]
)
 
st.write(
    t["bulk_description"]
)
 
uploaded = st.file_uploader(
    t["upload"],
    type=["csv"],
)
 
download_col, sample_col = st.columns(2)
 
with download_col:
 
    st.download_button(
        t["download_sample"],
        (ROOT / "data.csv").read_bytes(),
        "data.csv",
        "text/csv",
        width="stretch",
    )
 
with sample_col:
 
    use_sample = st.checkbox(
        t["use_sample"],
        value=False,
    )
 
with st.expander(
    t["csv_format"]
):
 
    st.code(
        "patient_id,age,sex,blood_pressure,cholesterol,bmi,smoker\n"
        "101,45,M,120,200,24.5,No",
        language="text",
    )
 
    st.write(
        t["csv_help"]
    )
 
if uploaded is not None:
 
    source = uploaded
 
elif use_sample:
 
    source = ROOT / "data.csv"
 
else:
 
    source = None
 
 
# =========================================================
# BULK PROCESSING
# =========================================================
 
if source is not None:
 
    try:
 
        if uploaded is not None:
 
            if uploaded.size > 5 * 1024 * 1024:
 
                raise ValueError(
                    t["file_limit"]
                )
 
        frame = pd.read_csv(
 
            source,
 
            dtype={
                "patient_id": "string"
            },
 
            nrows=10001,
        )
 
        result = predict(
            frame,
            model,
        )
 
        total_patients = len(result)
 
        low_count = int(
            result.demo_band
            .eq("Low")
            .sum()
        )
 
        medium_count = int(
            result.demo_band
            .eq("Medium")
            .sum()
        )
 
        high_count = int(
            result.demo_band
            .eq("High")
            .sum()
        )
 
        metric1, metric2 = st.columns(2)
 
        metric3, metric4 = st.columns(2)
 
        metric1.metric(
            t["patients"],
            total_patients,
        )
 
        metric2.metric(
            t["low_risk"],
            low_count,
        )
 
        metric3.metric(
            t["medium_risk"],
            medium_count,
        )
 
        metric4.metric(
            t["high_risk"],
            high_count,
        )
 
        st.caption(
            f'{t["bulk_model"]}: '
            f'{model_label} · '
            f'{t["synthetic_demo"]}'
        )
 
        st.dataframe(
 
            result,
 
            hide_index=True,
 
            width="stretch",
 
            column_config={
 
                "demo_score_percent":
                    st.column_config.ProgressColumn(
 
                        t["score_column"],
 
                        min_value=0,
 
                        max_value=100,
 
                        format="%.2f%%",
                    )
            },
        )
 
        counts = (
            result.demo_band
            .value_counts()
            .reindex(
                [
                    "Low",
                    "Medium",
                    "High",
                ],
                fill_value=0,
            )
        )
 
        chart_labels = [
            t["low"],
            t["medium"],
            t["high"],
        ]
 
        chart = go.Figure(
 
            go.Bar(
 
                x=chart_labels,
 
                y=counts.values,
 
                marker_color=[
                    "#688F81",
                    "#BA9545",
                    "#991B1B",
                ],
 
                marker_line_width=0,
            )
        )
 
        chart.update_layout(
 
            title=t["distribution"],
 
            yaxis_title=t["patients_axis"],
 
            yaxis_dtick=1,
 
            yaxis_gridcolor="rgba(91,15,30,0.08)",
 
            height=300,
 
            margin=dict(
                t=55,
                b=25,
                l=30,
                r=20,
            ),
 
            paper_bgcolor=
                "rgba(0,0,0,0)",
 
            plot_bgcolor=
                "rgba(0,0,0,0)",
 
            font_color=
                "#334155",
 
            font_family=
                "Plus Jakarta Sans, Cairo, sans-serif",
 
            bargap=0.35,
        )
 
        st.plotly_chart(
            chart,
            width="stretch",
        )
 
        exported = result.copy()
 
        for col in exported.select_dtypes(
            include=[
                "object",
                "string",
            ]
        ).columns:
 
            exported[col] = (
                exported[col]
                .map(
                    lambda x:
                        "'" + x
 
                        if (
                            isinstance(x, str)
 
                            and x
                            .lstrip()
                            .startswith(
                                (
                                    "=",
                                    "+",
                                    "-",
                                    "@",
                                )
                            )
                        )
 
                        else x
                )
            )
 
        csv_output = (
            exported
            .to_csv(index=False)
            .encode("utf-8")
        )
 
        st.download_button(
 
            t["download_results"],
 
            csv_output,
 
            "heartcare_results.csv",
 
            "text/csv",
 
            width="stretch",
        )
 
    except (
        ValueError,
        pd.errors.ParserError,
        UnicodeDecodeError,
        FileNotFoundError,
    ) as exc:
 
        st.error(
            f'{t["error"]}: {exc}'
        )
 
 
# =========================================================
# FOOTER (kept exactly as in the original, including repeat)
# =========================================================
 
st.divider()
 
st.caption(
    t["footer"]
)
 
st.divider()
 
st.caption(
    t["footer"]
)
