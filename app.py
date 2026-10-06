import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core import ROOT, predict


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="HeartCare AI",
    page_icon="♥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# LANGUAGE
# =========================================================
if "language" not in st.session_state:
    st.session_state.language = "English"

# Language selector at the TOP of the main page
top_left, top_middle, top_right = st.columns([5, 1.5, 0.2])

with top_middle:
    language = st.selectbox(
        "🌐 Language / اللغة",
        ["English", "العربية"],
        key="language",
        label_visibility="collapsed",
    )

AR = language == "العربية"


# =========================================================
# TRANSLATIONS
# =========================================================
translations = {
    "English": {
        "title": "♥ HeartCare AI",
        "subtitle": "PATIENT OVERVIEW  /  SINGLE & BULK ANALYSIS",

        "warning": (
            "DEMONSTRATION ONLY • Both models use synthetic data. "
            "Scores and bands are not medical risk estimates and "
            "must not guide patient care."
        ),

        "single_patient": "Single patient",
        "prediction_model": "Prediction model",

        "age": "Age (years)",
        "sex": "Sex",
        "male": "M",
        "female": "F",

        "bp": "Systolic blood pressure (mmHg)",
        "cholesterol": "Total cholesterol (mg/dL)",
        "bmi": "BMI (kg/m²)",

        "smoker": "Smoker",
        "no": "No",
        "yes": "Yes",

        "predict": "Predict demo score",

        "units": (
            "Units above are assumptions to confirm "
            "with your final model."
        ),

        "dashboard": "Patient dashboard",

        "score": "Synthetic demo score",
        "band": "Demo band",

        "model_used": "Model used",

        "submitted": "Submitted patient",

        "age_short": "age",
        "gender_short": "sex",
        "bp_short": "BP",
        "chol_short": "cholesterol",
        "smoker_short": "smoker",

        "bands": (
            "Bands: Low <30%, Medium 30–<60%, High ≥60%. "
            "These are arbitrary demo thresholds."
        ),

        "enter_patient": (
            "Enter a patient in the sidebar, then select "
            "“Predict demo score” to display the gauge."
        ),

        "bulk": "Bulk patient analysis",

        "bulk_description": (
            "Upload a CSV to calculate a demo score for every "
            "patient with the selected model."
        ),

        "upload": "Patient CSV · up to 5 MB / 10,000 rows",

        "download_sample": "Download sample CSV",

        "use_sample": "Use the 10-patient sample",

        "csv_format": "CSV format & validation",

        "csv_help": (
            "Sex: M/F. Smoker: Yes/No. Patient IDs are optional; "
            "if supplied, they must be unique. Incomplete or invalid "
            "batches are rejected with an error. Extra columns are "
            "retained but not used by the models."
        ),

        "file_limit": "File exceeds the 5 MB limit.",

        "patients": "Patients",

        "low": "Low",
        "medium": "Medium",
        "high": "High",

        "low_band": "Low demo band",
        "medium_band": "Medium demo band",
        "high_band": "High demo band",

        "bulk_model": "Bulk model",

        "synthetic_demo": "synthetic demonstration",

        "score_column": "Demo score (%)",

        "distribution": "Distribution of demo bands",

        "download_results": "Download demo results",

        "error": "Unable to process this batch",

        "footer": (
            "HeartCare AI · Uploaded records are processed in this "
            "session; this application has no database or "
            "patient-history storage."
        ),
    },

    "العربية": {
        "title": "♥ HeartCare AI",
        "subtitle": "نظرة عامة على المريض  /  التحليل الفردي والجماعي",

        "warning": (
            "لأغراض العرض فقط • يستخدم كلا النموذجين بيانات صناعية "
            "تجريبية. النتائج والتصنيفات لا تمثل تقديرًا طبيًا حقيقيًا "
            "للمخاطر ولا يجب استخدامها لاتخاذ قرارات علاجية."
        ),

        "single_patient": "بيانات المريض",
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

        "predict": "احسب النتيجة التجريبية",

        "units": (
            "الوحدات المستخدمة افتراضية ويجب تأكيدها "
            "مع النموذج النهائي."
        ),

        "dashboard": "لوحة بيانات المريض",

        "score": "النتيجة التجريبية",
        "band": "التصنيف التجريبي",

        "model_used": "النموذج المستخدم",

        "submitted": "بيانات المريض",

        "age_short": "العمر",
        "gender_short": "الجنس",
        "bp_short": "ضغط الدم",
        "chol_short": "الكوليسترول",
        "smoker_short": "التدخين",

        "bands": (
            "التصنيفات: منخفض أقل من 30%، متوسط من 30% إلى أقل من 60%، "
            "ومرتفع 60% أو أكثر. هذه الحدود مخصصة للعرض التجريبي فقط."
        ),

        "enter_patient": (
            "أدخل بيانات المريض من القائمة الجانبية، ثم اضغط "
            "«احسب النتيجة التجريبية» لعرض النتيجة."
        ),

        "bulk": "تحليل مجموعة من المرضى",

        "bulk_description": (
            "ارفع ملف CSV لحساب نتيجة تجريبية لكل مريض "
            "باستخدام النموذج المحدد."
        ),

        "upload": "ملف CSV للمرضى · بحد أقصى 5 MB / 10,000 صف",

        "download_sample": "تحميل ملف CSV تجريبي",

        "use_sample": "استخدام عينة من 10 مرضى",

        "csv_format": "تنسيق ملف CSV والتحقق من البيانات",

        "csv_help": (
            "في ملف CSV يجب أن تكون قيمة الجنس M أو F، "
            "وقيمة التدخين Yes أو No. معرف المريض اختياري، "
            "ولكن إذا تم إدخاله فيجب أن يكون فريدًا. "
            "سيتم رفض البيانات الناقصة أو غير الصحيحة."
        ),

        "file_limit": "حجم الملف يتجاوز الحد المسموح وهو 5 MB.",

        "patients": "عدد المرضى",

        "low": "منخفض",
        "medium": "متوسط",
        "high": "مرتفع",

        "low_band": "منخفض",
        "medium_band": "متوسط",
        "high_band": "مرتفع",

        "bulk_model": "النموذج المستخدم",

        "synthetic_demo": "عرض تجريبي باستخدام بيانات صناعية",

        "score_column": "النتيجة التجريبية (%)",

        "distribution": "توزيع التصنيفات التجريبية",

        "download_results": "تحميل نتائج التحليل",

        "error": "تعذر معالجة البيانات",

        "footer": (
            "HeartCare AI · تتم معالجة البيانات المرفوعة خلال الجلسة "
            "الحالية فقط، ولا يحتوي التطبيق على قاعدة بيانات "
            "أو نظام لتخزين تاريخ المرضى."
        ),
    },
}

t = translations[language]


# =========================================================
# DESIGN / CSS
# =========================================================
direction = "rtl" if AR else "ltr"
text_align = "right" if AR else "left"

st.markdown(
    f"""
    <style>

    /* Main page */
    .block-container {{
        padding-top: 1.2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }}

    /* Headings */
    h1, h2, h3 {{
        color: #8B0000 !important;
        font-weight: 750 !important;
        letter-spacing: -0.3px;
    }}

    h1 {{
        margin-bottom: 0.2rem !important;
    }}

    /* Main app direction */
    .stApp {{
        direction: {direction};
    }}

    /* Text alignment */
    .stApp p,
    .stApp label {{
        text-align: {text_align};
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        direction: {direction};
    }}

    [data-testid="stSidebar"] > div {{
        padding-top: 1rem;
    }}

    /* Metrics */
    [data-testid="stMetric"] {{
        background: #F8F1F2;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #F0DDDF;
        box-shadow: 0 2px 8px rgba(0,0,0,0.025);
    }}

    /* Buttons */
    .stButton button,
    .stDownloadButton button,
    [data-testid="stFormSubmitButton"] button {{
        border-radius: 10px !important;
        font-weight: 600 !important;
    }}

    /* Inputs */
    [data-baseweb="input"],
    [data-baseweb="select"] {{
        border-radius: 10px;
    }}

    /* Warning */
    [data-testid="stAlert"] {{
        border-radius: 12px;
    }}

    /* Divider */
    hr {{
        margin-top: 2rem !important;
        margin-bottom: 2rem !important;
    }}

    </style>
    """,
    unsafe_allow_html=True,
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
        ["XGBoost", "Logistic Regression"],
    )

    model = (
        "xgboost"
        if model_label == "XGBoost"
        else "lr"
    )

    with st.form("single_patient"):

        age = st.number_input(
            t["age"],
            min_value=18,
            max_value=120,
            value=45,
        )

        sex_display = st.selectbox(
            t["sex"],
            [t["male"], t["female"]],
        )

        # Keep values expected by the model
        sex = (
            "M"
            if sex_display == t["male"]
            else "F"
        )

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
            [t["no"], t["yes"]],
        )

        # Keep values expected by the model
        smoker = (
            "No"
            if smoker_display == t["no"]
            else "Yes"
        )

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

        st.session_state["single"] = (
            predict(record, model)
            .iloc[0]
            .to_dict()
        )

    except (ValueError, FileNotFoundError) as exc:

        st.error(str(exc))


# =========================================================
# PATIENT DASHBOARD
# =========================================================
st.subheader(t["dashboard"])


if "single" in st.session_state:

    row = st.session_state["single"]

    left, right = st.columns(
        [1.5, 1],
        gap="large",
    )

    # -----------------------------------------------------
    # Gauge
    # -----------------------------------------------------
    with left:

        fig = go.Figure(
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
                        "color": "#8B0000",
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

        fig.update_layout(
            height=310,
            margin=dict(
                t=70,
                b=20,
                l=45,
                r=45,
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#334155",
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )


    # -----------------------------------------------------
    # Patient information
    # -----------------------------------------------------
    with right:

        band_translation = {
            "Low": t["low"],
            "Medium": t["medium"],
            "High": t["high"],
        }

        displayed_band = band_translation.get(
            row["demo_band"],
            row["demo_band"],
        )

        st.metric(
            t["band"],
            displayed_band,
        )

        st.write(
            f'**{t["model_used"]}:** {row["model"]}'
        )

        if AR:

            sex_text = (
                "ذكر"
                if row["sex"] == "M"
                else "أنثى"
            )

            smoker_text = (
                "نعم"
                if row["smoker"] == "Yes"
                else "لا"
            )

            st.caption(
                f'{t["submitted"]}: '
                f'{t["age_short"]} {row["age"]}، '
                f'{t["gender_short"]} {sex_text}، '
                f'{t["bp_short"]} {row["blood_pressure"]}، '
                f'{t["chol_short"]} {row["cholesterol"]}، '
                f'BMI {row["bmi"]}، '
                f'{t["smoker_short"]} {smoker_text}.'
            )

        else:

            st.caption(
                f'{t["submitted"]}: '
                f'age {row["age"]}, '
                f'{row["sex"]}, '
                f'BP {row["blood_pressure"]}, '
                f'cholesterol {row["cholesterol"]}, '
                f'BMI {row["bmi"]}, '
                f'smoker {row["smoker"]}.'
            )

        st.caption(t["bands"])


else:

    st.info(t["enter_patient"])


# =========================================================
# BULK ANALYSIS
# =========================================================
st.divider()

st.subheader(t["bulk"])

st.write(t["bulk_description"])


upload_column, actions_column = st.columns(
    [3, 1],
    gap="large",
)


with upload_column:

    uploaded = st.file_uploader(
        t["upload"],
        type=["csv"],
    )


with actions_column:

    st.download_button(
        t["download_sample"],
        (ROOT / "data.csv").read_bytes(),
        "data.csv",
        "text/csv",
        width="stretch",
    )

    use_sample = st.checkbox(
        t["use_sample"],
        value=False,
    )


# =========================================================
# CSV HELP
# =========================================================
with st.expander(t["csv_format"]):

    st.code(
        "patient_id,age,sex,blood_pressure,cholesterol,bmi,smoker\n"
        "101,45,M,120,200,24.5,No",
        language="text",
    )

    st.write(t["csv_help"])


source = (
    uploaded
    if uploaded is not None
    else (
        ROOT / "data.csv"
        if use_sample
        else None
    )
)


# =========================================================
# BULK PROCESSING
# =========================================================
if source is not None:

    try:

        if (
            uploaded is not None
            and uploaded.size > 5 * 1024 * 1024
        ):
            raise ValueError(t["file_limit"])


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


        # -------------------------------------------------
        # Metrics
        # -------------------------------------------------
        metrics = st.columns(4)

        metrics[0].metric(
            t["patients"],
            len(result),
        )

        metrics[1].metric(
            t["low_band"],
            int(
                result.demo_band
                .eq("Low")
                .sum()
            ),
        )

        metrics[2].metric(
            t["medium_band"],
            int(
                result.demo_band
                .eq("Medium")
                .sum()
            ),
        )

        metrics[3].metric(
            t["high_band"],
            int(
                result.demo_band
                .eq("High")
                .sum()
            ),
        )


        st.caption(
            f'{t["bulk_model"]}: '
            f'{model_label} · '
            f'{t["synthetic_demo"]}'
        )


        # -------------------------------------------------
        # Table
        # -------------------------------------------------
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


        # -------------------------------------------------
        # Chart
        # -------------------------------------------------
        counts = (
            result.demo_band
            .value_counts()
            .reindex(
                ["Low", "Medium", "High"],
                fill_value=0,
            )
        )


        graph_labels = [
            t["low"],
            t["medium"],
            t["high"],
        ]


        chart = go.Figure(
            go.Bar(
                x=graph_labels,
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
            yaxis_title=t["patients"],
            yaxis_dtick=1,
            height=300,

            margin=dict(
                t=55,
                b=25,
                l=30,
                r=20,
            ),

            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",

            font_color="#334155",
        )


        st.plotly_chart(
            chart,
            width="stretch",
        )


        # -------------------------------------------------
        # Safe CSV export
        # -------------------------------------------------
        exported = result.copy()


        for col in exported.select_dtypes(
            include=["object", "string"]
        ).columns:

            exported[col] = exported[col].map(
                lambda x:
                    "'" + x
                    if (
                        isinstance(x, str)
                        and x.lstrip().startswith(
                            ("=", "+", "-", "@")
                        )
                    )
                    else x
            )


        st.download_button(
            t["download_results"],

            exported
            .to_csv(index=False)
            .encode("utf-8"),

            "heartcare_demo_results.csv",

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

st.caption(t["footer"])
