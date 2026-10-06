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
# TRANSLATIONS
# =========================================================

translations = {

    # =====================================================
    # ENGLISH
    # =====================================================

    "English": {

        "title": "HeartCare AI",

        "subtitle":
            "PATIENT OVERVIEW / SINGLE & BULK ANALYSIS",

        "warning":
            "DEMONSTRATION ONLY • Both models use synthetic data. "
            "Risk scores and levels are not medical risk estimates "
            "and must not guide patient care.",

        "single_patient":
            "Single Patient",

        "prediction_model":
            "Prediction Model",

        "age":
            "Age (years)",

        "sex":
            "Sex",

        "male":
            "M",

        "female":
            "F",

        "bp":
            "Systolic Blood Pressure (mmHg)",

        "cholesterol":
            "Total Cholesterol (mg/dL)",

        "bmi":
            "BMI (kg/m²)",

        "smoker":
            "Smoker",

        "no":
            "No",

        "yes":
            "Yes",

        "predict":
            "Predict Risk Score",

        "units":
            "Units above are assumptions to confirm "
            "with the final model.",

        "dashboard":
            "Patient Dashboard",

        "score":
            "Risk Score",

        "band":
            "Risk Level",

        "model_used":
            "Model Used",

        "patient_details":
            "Patient Details",

        "bands":
            "Risk levels: Low <30%, Medium 30–<60%, High ≥60%. "
            "These thresholds are for demonstration purposes only.",

        "enter_patient":
            "Enter the patient information in the sidebar "
            "and select “Predict Risk Score” to display the result.",

        "bulk":
            "Bulk Patient Analysis",

        "bulk_description":
            "Upload a CSV file to calculate a risk score for every "
            "patient using the selected model.",

        "upload":
            "Patient CSV · up to 5 MB / 10,000 rows",

        "download_sample":
            "Download Sample CSV",

        "use_sample":
            "Use 10-Patient Sample",

        "csv_format":
            "CSV Format & Validation",

        "csv_help":
            "Required model fields: age, sex, blood_pressure, "
            "cholesterol, bmi and smoker. Sex must be M/F and "
            "Smoker must be Yes/No. patient_id is optional; "
            "if supplied, IDs must be unique. Invalid or incomplete "
            "batches are rejected. Extra columns are retained but "
            "are not used by the models.",

        "file_limit":
            "File exceeds the 5 MB limit.",

        "patients":
            "Patients",

        "low":
            "Low",

        "medium":
            "Medium",

        "high":
            "High",

        "low_risk":
            "Low Risk",

        "medium_risk":
            "Medium Risk",

        "high_risk":
            "High Risk",

        "bulk_model":
            "Bulk Model",

        "synthetic_demo":
            "Synthetic Demonstration",

        "score_column":
            "Risk Score (%)",

        "distribution":
            "Distribution of Risk Levels",

        "patients_axis":
            "Patients",

        "download_results":
            "Download Results",

        "error":
            "Unable to process this batch",

        "footer":
            "HeartCare AI · Uploaded records are processed during "
            "the current session only. This application does not "
            "contain a patient-history database.",
    },


    # =====================================================
    # ARABIC
    # =====================================================

    "العربية": {

        "title":
            "HeartCare AI",

        "subtitle":
            "نظرة عامة على المريض / التحليل الفردي والجماعي",

        "warning":
            "لأغراض العرض فقط • يستخدم كلا النموذجين بيانات صناعية "
            "تجريبية. نسب ومستويات الخطر لا تمثل تقديرًا طبيًا حقيقيًا "
            "ولا يجب استخدامها لاتخاذ قرارات علاجية.",

        "single_patient":
            "إدخال مريض واحد",

        "prediction_model":
            "نموذج التنبؤ",

        "age":
            "العمر (بالسنوات)",

        "sex":
            "الجنس",

        "male":
            "ذكر",

        "female":
            "أنثى",

        "bp":
            "ضغط الدم الانقباضي (mmHg)",

        "cholesterol":
            "الكوليسترول الكلي (mg/dL)",

        "bmi":
            "مؤشر كتلة الجسم BMI (kg/m²)",

        "smoker":
            "هل المريض مدخن؟",

        "no":
            "لا",

        "yes":
            "نعم",

        "predict":
            "توقع نسبة الخطر",

        "units":
            "الوحدات المستخدمة افتراضية ويجب تأكيدها "
            "مع النموذج النهائي.",

        "dashboard":
            "لوحة بيانات المريض",

        "score":
            "نسبة الخطر",

        "band":
            "مستوى الخطر",

        "model_used":
            "النموذج المستخدم",

        "patient_details":
            "بيانات المريض",

        "bands":
            "مستويات الخطر: منخفض أقل من 30%، "
            "متوسط من 30% إلى أقل من 60%، "
            "ومرتفع 60% أو أكثر. هذه الحدود مخصصة "
            "للعرض التجريبي فقط.",

        "enter_patient":
            "أدخل بيانات المريض من القائمة الجانبية، "
            "ثم اضغط «توقع نسبة الخطر» لعرض النتيجة.",

        "bulk":
            "تحليل مجموعة من المرضى",

        "bulk_description":
            "ارفع ملف CSV لحساب نسبة الخطر لكل مريض "
            "باستخدام نموذج التنبؤ المحدد.",

        "upload":
            "ملف CSV للمرضى · بحد أقصى 5 MB / 10,000 صف",

        "download_sample":
            "تحميل ملف CSV تجريبي",

        "use_sample":
            "استخدام عينة 10 مرضى",

        "csv_format":
            "تنسيق ملف CSV والتحقق من البيانات",

        "csv_help":
            "الحقول المطلوبة للنموذج هي: العمر، الجنس، ضغط الدم، "
            "الكوليسترول، BMI والتدخين. داخل ملف CSV يجب أن تكون "
            "قيمة الجنس M أو F، والتدخين Yes أو No. معرف المريض "
            "patient_id اختياري، وإذا تم إدخاله فيجب أن يكون فريدًا. "
            "سيتم رفض الملفات التي تحتوي على بيانات ناقصة أو غير صحيحة.",

        "file_limit":
            "حجم الملف يتجاوز الحد المسموح وهو 5 MB.",

        "patients":
            "عدد المرضى",

        "low":
            "منخفض",

        "medium":
            "متوسط",

        "high":
            "مرتفع",

        "low_risk":
            "خطر منخفض",

        "medium_risk":
            "خطر متوسط",

        "high_risk":
            "خطر مرتفع",

        "bulk_model":
            "نموذج التحليل",

        "synthetic_demo":
            "عرض تجريبي ببيانات صناعية",

        "score_column":
            "نسبة الخطر (%)",

        "distribution":
            "توزيع مستويات الخطر",

        "patients_axis":
            "عدد المرضى",

        "download_results":
            "تحميل نتائج التحليل",

        "error":
            "تعذر معالجة البيانات",

        "footer":
            "HeartCare AI · تتم معالجة البيانات المرفوعة خلال "
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
# CSS — PREMIUM + MOBILE RESPONSIVE
# =========================================================

st.markdown(
    f"""
<style>

/* ==========================================
   GENERAL
   ========================================== */

.block-container {{
    padding-top: 1rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}}


/* ==========================================
   LANGUAGE DIRECTION
   ========================================== */

.stApp {{
    direction: {direction};
}}

.stApp p,
.stApp label {{
    text-align: {text_align};
}}


/* ==========================================
   HEADINGS
   ========================================== */

h1,
h2,
h3 {{
    color: #991B1B !important;
    font-weight: 750 !important;
}}

h1 {{
    margin-bottom: 0.2rem !important;
    letter-spacing: -0.5px;
}}


/* ==========================================
   SIDEBAR
   ========================================== */

[data-testid="stSidebar"] {{
    direction: {direction};
}}

[data-testid="stSidebar"] > div {{
    padding-top: 1rem;
}}


/* ==========================================
   METRIC CARDS
   ========================================== */

[data-testid="stMetric"] {{
    background: #F8F1F2;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #F0DDDF;
    box-shadow: 0 2px 8px rgba(0,0,0,0.025);
}}

[data-testid="stMetricLabel"] {{
    font-weight: 600;
}}


/* ==========================================
   NORMAL BUTTONS
   ========================================== */

.stDownloadButton button,
[data-testid="stFormSubmitButton"] button {{
    border-radius: 10px !important;
    font-weight: 600 !important;
    min-height: 44px;
}}


/* ==========================================
   PREMIUM LANGUAGE BUTTON
   ========================================== */

div[data-testid="stButton"] > button {{
    background: #FFFFFF !important;
    color: #991B1B !important;
    border: 1px solid #991B1B !important;
    border-radius: 22px !important;
    font-weight: 650 !important;
    min-height: 42px !important;
    padding: 0.45rem 1rem !important;
    transition: all 0.2s ease;
}}

div[data-testid="stButton"] > button:hover {{
    background: #991B1B !important;
    color: #FFFFFF !important;
    border-color: #991B1B !important;
}}

div[data-testid="stButton"] > button:active {{
    transform: scale(0.98);
}}


/* ==========================================
   INPUTS
   ========================================== */

[data-baseweb="input"],
[data-baseweb="select"] {{
    border-radius: 10px;
}}


/* ==========================================
   ALERTS
   ========================================== */

[data-testid="stAlert"] {{
    border-radius: 12px;
}}


/* ==========================================
   DIVIDERS
   ========================================== */

hr {{
    margin-top: 2rem !important;
    margin-bottom: 2rem !important;
}}


/* ==========================================
   MOBILE / TABLET
   ========================================== */

@media (max-width: 768px) {{

    .block-container {{
        padding-top: 0.6rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-bottom: 2rem !important;
    }}

    h1 {{
        font-size: 2rem !important;
        line-height: 1.2 !important;
    }}

    h2 {{
        font-size: 1.5rem !important;
    }}

    h3 {{
        font-size: 1.25rem !important;
    }}

    p,
    label {{
        font-size: 0.95rem !important;
    }}

    .stButton button,
    .stDownloadButton button,
    [data-testid="stFormSubmitButton"] button {{
        min-height: 46px !important;
        font-size: 0.95rem !important;
    }}

    input,
    textarea,
    [data-baseweb="select"] {{
        font-size: 16px !important;
    }}

    [data-testid="stMetric"] {{
        padding: 12px !important;
        border-radius: 12px !important;
    }}

    [data-testid="stMetricValue"] {{
        font-size: 1.45rem !important;
    }}

    [data-testid="stPlotlyChart"] {{
        width: 100% !important;
        max-width: 100% !important;
        overflow: hidden !important;
    }}

    [data-testid="stDataFrame"] {{
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: auto !important;
    }}

    [data-testid="stAlert"] {{
        font-size: 0.9rem !important;
    }}
}}


/* ==========================================
   SMALL PHONES
   ========================================== */

@media (max-width: 480px) {{

    .block-container {{
        padding-left: 0.7rem !important;
        padding-right: 0.7rem !important;
    }}

    h1 {{
        font-size: 1.7rem !important;
    }}

    h2 {{
        font-size: 1.3rem !important;
    }}

    h3 {{
        font-size: 1.1rem !important;
    }}

    [data-testid="stMetricValue"] {{
        font-size: 1.25rem !important;
    }}

    [data-testid="stMetric"] {{
        padding: 10px !important;
    }}

    div[data-testid="stButton"] > button {{
        font-size: 0.88rem !important;
        padding: 0.35rem 0.7rem !important;
    }}
}}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# PREMIUM LANGUAGE SWITCH
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
# HEADER
# =========================================================

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


    # =====================================================
    # PATIENT FORM
    # =====================================================

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


    # =====================================================
    # RISK GAUGE
    # =====================================================

    gauge = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=row["demo_score_percent"],

            number={
                "suffix": "%",
                "font": {
                    "size": 38,
                },
            },

            title={
                "text": t["score"],
            },

            gauge={

                "axis": {
                    "range": [0, 100],
                },

                "bar": {
                    "color": "#991B1B",
                },

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
    )


    # =====================================================
    # DASHBOARD COLUMNS
    # =====================================================

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


        # =================================================
        # PATIENT DETAILS
        # =================================================

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


# =========================================================
# CSV UPLOAD
# =========================================================

uploaded = st.file_uploader(
    t["upload"],
    type=["csv"],
)


# =========================================================
# SAMPLE CSV ACTIONS
# =========================================================

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


# =========================================================
# CSV FORMAT
# =========================================================

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


# =========================================================
# SELECT SOURCE
# =========================================================

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

        # -------------------------------------------------
        # FILE SIZE
        # -------------------------------------------------

        if uploaded is not None:

            if uploaded.size > 5 * 1024 * 1024:

                raise ValueError(
                    t["file_limit"]
                )


        # -------------------------------------------------
        # READ CSV
        # -------------------------------------------------

        frame = pd.read_csv(

            source,

            dtype={
                "patient_id": "string"
            },

            nrows=10001,
        )


        # -------------------------------------------------
        # PREDICTION
        # -------------------------------------------------

        result = predict(
            frame,
            model,
        )


        # -------------------------------------------------
        # COUNTS
        # -------------------------------------------------

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


        # =================================================
        # METRICS
        # =================================================

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


        # =================================================
        # RESULTS TABLE
        # =================================================

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


        # =================================================
        # RISK DISTRIBUTION CHART
        # =================================================

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
            )
        )


        chart.update_layout(

            title=t["distribution"],

            yaxis_title=t["patients_axis"],

            yaxis_dtick=1,

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
        )


        st.plotly_chart(
            chart,
            width="stretch",
        )


        # =================================================
        # SAFE CSV EXPORT
        # =================================================

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


        # =================================================
        # DOWNLOAD RESULTS
        # =================================================

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
# FOOTER
# =========================================================

st.divider()

st.caption(
    t["footer"]
)

st.divider()

st.caption(
    t["footer"]
)
