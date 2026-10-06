from io import BytesIO
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from core import ROOT, predict, validate

st.set_page_config(page_title='HeartCare AI', page_icon='♥', layout='wide')

# -----------------------------
# Language selector
# -----------------------------
language = st.sidebar.selectbox('🌐 Language / اللغة', ['English', 'العربية'])
ar = language == 'العربية'

# -----------------------------
# Translations
# -----------------------------
T = {
    'title': '♥ HeartCare AI',
    'caption': 'نظرة عامة على المريض / تحليل فردي وجماعي' if ar else 'PATIENT OVERVIEW / SINGLE & BULK ANALYSIS',
    'warning': 'للعرض التوضيحي فقط • كلا النموذجين يستخدمان بيانات صناعية. النتائج لا تمثل تقديرًا طبيًا للمخاطر ولا يجب استخدامها لاتخاذ قرارات علاجية.'
               if ar else
               'DEMONSTRATION ONLY • Both models use synthetic data. Scores and bands are not medical risk estimates and must not guide patient care.',

    'single_patient': 'مريض واحد' if ar else 'Single patient',
    'prediction_model': 'نموذج التنبؤ' if ar else 'Prediction model',
    'age': 'العمر (بالسنوات)' if ar else 'Age (years)',
    'sex': 'الجنس' if ar else 'Sex',
    'male': 'ذكر' if ar else 'M',
    'female': 'أنثى' if ar else 'F',
    'bp': 'ضغط الدم الانقباضي (mmHg)' if ar else 'Systolic blood pressure (mmHg)',
    'cholesterol': 'الكوليسترول الكلي (mg/dL)' if ar else 'Total cholesterol (mg/dL)',
    'bmi': 'مؤشر كتلة الجسم BMI (kg/m²)' if ar else 'BMI (kg/m²)',
    'smoker': 'مدخن' if ar else 'Smoker',
    'no': 'لا' if ar else 'No',
    'yes': 'نعم' if ar else 'Yes',
    'predict': 'احسب النتيجة التجريبية' if ar else 'Predict demo score',
    'units_note': 'الوحدات المستخدمة هنا افتراضات ويجب تأكيدها مع النموذج النهائي.'
                  if ar else
                  'Units above are assumptions to confirm with your final model.',

    'patient_dashboard': 'لوحة بيانات المريض' if ar else 'Patient dashboard',
    'synthetic_demo_score': 'النتيجة التجريبية الصناعية' if ar else 'Synthetic demo score',
    'demo_band': 'فئة النتيجة' if ar else 'Demo band',
    'model_used': 'النموذج المستخدم' if ar else 'Model used',
    'submitted_patient': 'بيانات المريض المُدخلة' if ar else 'Submitted patient',
    'bands_note': 'الفئات: منخفض أقل من 30%، متوسط من 30% إلى أقل من 60%، مرتفع 60% فأكثر. هذه حدود تجريبية فقط.'
                  if ar else
                  'Bands: Low <30%, Medium 30–<60%, High ≥60%. These are arbitrary demo thresholds.',
    'enter_patient': 'أدخل بيانات المريض من القائمة الجانبية ثم اضغط زر حساب النتيجة التجريبية لعرض المؤشر.'
                     if ar else
                     'Enter a patient in the sidebar, then select “Predict demo score” to display the gauge.',

    'bulk_analysis': 'تحليل مجموعة مرضى' if ar else 'Bulk patient analysis',
    'bulk_desc': 'ارفع ملف CSV لحساب نتيجة تجريبية لكل مريض باستخدام النموذج المحدد.'
                 if ar else
                 'Upload a CSV to calculate a demo score for every patient with the selected model.',
    'upload_csv': 'ملف CSV للمرضى · حد أقصى 5 MB / 10,000 صف'
                  if ar else
                  'Patient CSV · up to 5 MB / 10,000 rows',
    'download_sample': 'تحميل ملف CSV تجريبي' if ar else 'Download sample CSV',
    'use_sample': 'استخدم عينة من 10 مرضى' if ar else 'Use the 10-patient sample',
    'csv_validation': 'تنسيق CSV والتحقق' if ar else 'CSV format & validation',
    'csv_help': 'الجنس: M/F. التدخين: Yes/No. رقم المريض اختياري، وإذا تم استخدامه يجب أن يكون فريدًا. يتم رفض الملفات غير المكتملة أو غير الصالحة. الأعمدة الإضافية يتم الاحتفاظ بها ولكن لا يستخدمها النموذج.'
                if ar else
                'Sex: M/F. Smoker: Yes/No. Patient IDs are optional; if supplied, they must be unique. Incomplete or invalid batches are rejected with an error. Extra columns are retained but not used by the models.',
    'patients': 'المرضى' if ar else 'Patients',
    'low': 'منخفض' if ar else 'Low',
    'medium': 'متوسط' if ar else 'Medium',
    'high': 'مرتفع' if ar else 'High',
    'demo_band_suffix': 'فئة تجريبية' if ar else 'demo band',
    'bulk_model': 'نموذج التحليل الجماعي' if ar else 'Bulk model',
    'distribution': 'توزيع فئات النتائج التجريبية' if ar else 'Distribution of demo bands',
    'download_results': 'تحميل النتائج التجريبية' if ar else 'Download demo results',
    'unable_batch': 'تعذر معالجة الملف' if ar else 'Unable to process this batch',
    'footer': 'HeartCare AI · تتم معالجة السجلات المرفوعة داخل هذه الجلسة فقط، ولا يحتوي التطبيق على قاعدة بيانات أو تخزين لتاريخ المرضى.'
              if ar else
              'HeartCare AI · Uploaded records are processed in this session; this application has no database or patient-history storage.'
}

# -----------------------------
# CSS
# -----------------------------
direction = 'rtl' if ar else 'ltr'
text_align = 'right' if ar else 'left'

st.markdown(
    f'''
    <style>
        h1,h2,h3 {{
            color:#8B0000 !important;
        }}

        .block-container {{
            padding-top:2rem;
        }}

        [data-testid="stMetric"] {{
            background:#F8F1F2;
            padding:18px;
            border-radius:12px;
            border:1px solid #F0DDDF;
        }}

        html, body, [class*="css"] {{
            direction:{direction};
        }}

        .stApp {{
            direction:{direction};
            text-align:{text_align};
        }}

        section[data-testid="stSidebar"] {{
            direction:{direction};
            text-align:{text_align};
        }}
    </style>
    ''',
    unsafe_allow_html=True
)

# -----------------------------
# Header
# -----------------------------
st.title(T['title'])
st.caption(T['caption'])
st.warning(T['warning'])

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header(T['single_patient'])

    model_label = st.selectbox(
        T['prediction_model'],
        ['XGBoost', 'Logistic Regression']
    )

    model = 'xgboost' if model_label == 'XGBoost' else 'lr'

    with st.form('single_patient'):
        age = st.number_input(T['age'], 18, 120, 45)

        sex_label = st.selectbox(
            T['sex'],
            [T['male'], T['female']]
        )
        sex = 'M' if sex_label == T['male'] else 'F'

        bp = st.number_input(T['bp'], 60, 260, 120)
        cholesterol = st.number_input(T['cholesterol'], 70, 600, 200)
        bmi = st.number_input(T['bmi'], 10.0, 70.0, 24.5, step=.1)

        smoker_label = st.selectbox(
            T['smoker'],
            [T['no'], T['yes']]
        )
        smoker = 'No' if smoker_label == T['no'] else 'Yes'

        submitted = st.form_submit_button(
            T['predict'],
            type='primary',
            width='stretch'
        )

    st.caption(T['units_note'])

# -----------------------------
# Single prediction
# -----------------------------
if submitted:
    record = pd.DataFrame([
        dict(
            age=age,
            sex=sex,
            blood_pressure=bp,
            cholesterol=cholesterol,
            bmi=bmi,
            smoker=smoker
        )
    ])

    try:
        st.session_state['single'] = predict(record, model).iloc[0].to_dict()
    except (ValueError, FileNotFoundError) as exc:
        st.error(str(exc))

# -----------------------------
# Dashboard
# -----------------------------
st.subheader(T['patient_dashboard'])

if 'single' in st.session_state:
    row = st.session_state['single']

    a, b = st.columns([1.4, 1])

    with a:
        fig = go.Figure(
            go.Indicator(
                mode='gauge+number',
                value=row['demo_score_percent'],
                number={'suffix': '%'},
                title={'text': T['synthetic_demo_score']},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': '#991B1B'},
                    'steps': [
                        {'range': [0, 30], 'color': '#DDEBE7'},
                        {'range': [30, 60], 'color': '#F4E9CC'},
                        {'range': [60, 100], 'color': '#F3D6D8'}
                    ]
                }
            )
        )

        fig.update_layout(
            height=290,
            margin=dict(t=60, b=20, l=40, r=40),
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#334155'
        )

        st.plotly_chart(fig, width='stretch')

    with b:
        band_map = {
            'Low': T['low'],
            'Medium': T['medium'],
            'High': T['high']
        }

        translated_band = band_map.get(row['demo_band'], row['demo_band'])

        st.metric(T['demo_band'], translated_band)
        st.write(f"{T['model_used']}: **{row['model']}**")

        if ar:
            st.caption(
                f"{T['submitted_patient']}: "
                f"العمر {row['age']}، "
                f"الجنس {row['sex']}، "
                f"الضغط {row['blood_pressure']}، "
                f"الكوليسترول {row['cholesterol']}، "
                f"BMI {row['bmi']}، "
                f"التدخين {row['smoker']}."
            )
        else:
            st.caption(
                f"{T['submitted_patient']}: age {row['age']}, "
                f"{row['sex']}, BP {row['blood_pressure']}, "
                f"cholesterol {row['cholesterol']}, "
                f"BMI {row['bmi']}, smoker {row['smoker']}."
            )

        st.caption(T['bands_note'])

else:
    st.info(T['enter_patient'])

# -----------------------------
# Bulk analysis
# -----------------------------
st.divider()
st.subheader(T['bulk_analysis'])
st.write(T['bulk_desc'])

a, b = st.columns([3, 1])

with a:
    uploaded = st.file_uploader(
        T['upload_csv'],
        type=['csv']
    )

with b:
    st.download_button(
        T['download_sample'],
        (ROOT / 'data.csv').read_bytes(),
        'data.csv',
        'text/csv'
    )

    use_sample = st.checkbox(
        T['use_sample'],
        value=False
    )

with st.expander(T['csv_validation']):
    st.code(
        'patient_id,age,sex,blood_pressure,cholesterol,bmi,smoker\n'
        '101,45,M,120,200,24.5,No',
        language='text'
    )
    st.write(T['csv_help'])

source = uploaded if uploaded is not None else (
    ROOT / 'data.csv' if use_sample else None
)

if source is not None:
    try:
        if uploaded is not None and uploaded.size > 5 * 1024 * 1024:
            raise ValueError(
                'حجم الملف أكبر من الحد المسموح وهو 5 MB.'
                if ar else
                'File exceeds the 5 MB limit.'
            )

        frame = pd.read_csv(
            source,
            dtype={'patient_id': 'string'},
            nrows=10001
        )

        result = predict(frame, model)

        cols = st.columns(4)
        cols[0].metric(T['patients'], len(result))

        band_labels = {
            'Low': T['low'],
            'Medium': T['medium'],
            'High': T['high']
        }

        for col, band in zip(cols[1:], ['Low', 'Medium', 'High']):
            col.metric(
                f"{band_labels[band]} {T['demo_band_suffix']}",
                int(result.demo_band.eq(band).sum())
            )

        if ar:
            st.caption(f"{T['bulk_model']}: {model_label} · عرض تجريبي باستخدام بيانات صناعية")
        else:
            st.caption(f'{T["bulk_model"]}: {model_label} · synthetic demonstration')

        display_result = result.copy()

        if ar and 'demo_band' in display_result.columns:
            display_result['demo_band'] = display_result['demo_band'].map(
                band_labels
            )

        st.dataframe(
            display_result,
            hide_index=True,
            width='stretch',
            column_config={
                'demo_score_percent': st.column_config.ProgressColumn(
                    'النتيجة التجريبية (%)' if ar else 'Demo score (%)',
                    min_value=0,
                    max_value=100,
                    format='%.2f%%'
                )
            }
        )

        counts = result.demo_band.value_counts().reindex(
            ['Low', 'Medium', 'High'],
            fill_value=0
        )

        x_labels = [
            band_labels['Low'],
            band_labels['Medium'],
            band_labels['High']
        ]

        fig = go.Figure(
            go.Bar(
                x=x_labels,
                y=counts.values,
                marker_color=['#688F81', '#BA9545', '#991B1B']
            )
        )

        fig.update_layout(
            title=T['distribution'],
            yaxis_title=T['patients'],
            yaxis_dtick=1,
            height=280,
            margin=dict(t=45, b=20),
            font_color='#334155'
        )

        st.plotly_chart(fig, width='stretch')

        exported = result.copy()

        for col in exported.select_dtypes(include=['object', 'string']).columns:
            exported[col] = exported[col].map(
                lambda x: "'" + x
                if isinstance(x, str)
                and x.lstrip().startswith(('=', '+', '-', '@'))
                else x
            )

        st.download_button(
            T['download_results'],
            exported.to_csv(index=False).encode('utf-8'),
            'heartcare_demo_results.csv',
            'text/csv'
        )

    except (
        ValueError,
        pd.errors.ParserError,
        UnicodeDecodeError,
        FileNotFoundError
    ) as exc:
        st.error(f"{T['unable_batch']}: {exc}")

st.caption(T['footer'])
