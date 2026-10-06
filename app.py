from io import BytesIO
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from core import ROOT, predict, validate

st.set_page_config(page_title='HeartCare AI', page_icon='♥', layout='wide')
st.markdown('''<style>h1,h2,h3{color:#D00000 !important;} .block-container{padding-top:2rem} [data-testid="stMetric"]{background:#F8F1F2;padding:18px;border-radius:12px;border:1px solid #F0DDDF}</style>''', unsafe_allow_html=True)
st.title('♥ HeartCare AI')
st.caption('PATIENT OVERVIEW  /  SINGLE & BULK ANALYSIS')
st.warning('DEMONSTRATION ONLY • Both models use synthetic data. Scores and bands are not medical risk estimates and must not guide patient care.')
with st.sidebar:
    st.header('Single patient')
    model_label = st.selectbox('Prediction model', ['XGBoost','Logistic Regression'])
    model = 'xgboost' if model_label == 'XGBoost' else 'lr'
    with st.form('single_patient'):
        age = st.number_input('Age (years)',18,120,45)
        sex = st.selectbox('Sex', ['M','F'])
        bp = st.number_input('Systolic blood pressure (mmHg)',60,260,120)
        cholesterol = st.number_input('Total cholesterol (mg/dL)',70,600,200)
        bmi = st.number_input('BMI (kg/m²)',10.0,70.0,24.5,step=.1)
        smoker = st.selectbox('Smoker', ['No','Yes'])
        submitted = st.form_submit_button('Predict demo score', type='primary', width='stretch')
    st.caption('Units above are assumptions to confirm with your final model.')
if submitted:
    record = pd.DataFrame([dict(age=age, sex=sex, blood_pressure=bp, cholesterol=cholesterol, bmi=bmi, smoker=smoker)])
    try:
        st.session_state['single'] = predict(record, model).iloc[0].to_dict()
    except (ValueError, FileNotFoundError) as exc:
        st.error(str(exc))

st.subheader('Patient dashboard')
if 'single' in st.session_state:
    row = st.session_state['single']
    a,b = st.columns([1.4,1])
    with a:
        fig = go.Figure(go.Indicator(mode='gauge+number',value=row['demo_score_percent'],number={'suffix':'%'},title={'text':'Synthetic demo score'},gauge={'axis':{'range':[0,100]},'bar':{'color':'#991B1B'},'steps':[{'range':[0,30],'color':'#DDEBE7'},{'range':[30,60],'color':'#F4E9CC'},{'range':[60,100],'color':'#F3D6D8'}]}))
        fig.update_layout(height=290, margin=dict(t=60,b=20,l=40,r=40),paper_bgcolor='rgba(0,0,0,0)',font_color='#334155')
        st.plotly_chart(fig, width='stretch')
    with b:
        st.metric('Demo band',row['demo_band'])
        st.write('Model used: **'+row['model']+'**')
        st.caption(f"Submitted patient: age {row['age']}, {row['sex']}, BP {row['blood_pressure']}, cholesterol {row['cholesterol']}, BMI {row['bmi']}, smoker {row['smoker']}.")
        st.caption('Bands: Low <30%, Medium 30–<60%, High ≥60%. These are arbitrary demo thresholds.')
else:
    st.info('Enter a patient in the sidebar, then select “Predict demo score” to display the gauge.')

st.divider()
st.subheader('Bulk patient analysis')
st.write('Upload a CSV to calculate a demo score for every patient with the selected model.')
a,b = st.columns([3,1])
with a:
    uploaded = st.file_uploader('Patient CSV · up to 5 MB / 10,000 rows', type=['csv'])
with b:
    st.download_button('Download sample CSV', (ROOT/'data.csv').read_bytes(), 'data.csv', 'text/csv')
    use_sample = st.checkbox('Use the 10-patient sample', value=False)
with st.expander('CSV format & validation'):
    st.code('patient_id,age,sex,blood_pressure,cholesterol,bmi,smoker\n101,45,M,120,200,24.5,No', language='text')
    st.write('Sex: M/F. Smoker: Yes/No. Patient IDs are optional; if supplied, they must be unique. Incomplete or invalid batches are rejected with an error. Extra columns are retained but not used by the models.')
source = uploaded if uploaded is not None else (ROOT/'data.csv' if use_sample else None)
if source is not None:
    try:
        if uploaded is not None and uploaded.size > 5*1024*1024:
            raise ValueError('File exceeds the 5 MB limit.')
        frame = pd.read_csv(source, dtype={'patient_id':'string'}, nrows=10001)
        result = predict(frame, model)
        cols = st.columns(4)
        cols[0].metric('Patients', len(result))
        for col,band in zip(cols[1:],['Low','Medium','High']):
            col.metric(band+' demo band',int(result.demo_band.eq(band).sum()))
        st.caption(f'Bulk model: {model_label} · synthetic demonstration')
        st.dataframe(result, hide_index=True, width='stretch', column_config={'demo_score_percent':st.column_config.ProgressColumn('Demo score (%)',min_value=0,max_value=100,format='%.2f%%')})
        counts = result.demo_band.value_counts().reindex(['Low','Medium','High'], fill_value=0)
        fig = go.Figure(go.Bar(x=counts.index,y=counts.values,marker_color=['#688F81','#BA9545','#991B1B']))
        fig.update_layout(title='Distribution of demo bands', yaxis_title='Patients',yaxis_dtick=1, height=280,margin=dict(t=45,b=20),font_color='#334155')
        st.plotly_chart(fig,width='stretch')
        # Escape spreadsheet formulas in user-supplied text columns on export.
        exported = result.copy()
        for col in exported.select_dtypes(include=['object','string']).columns:
            exported[col] = exported[col].map(lambda x: "'"+x if isinstance(x,str) and x.lstrip().startswith(('=','+','-','@')) else x)
        st.download_button('Download demo results',exported.to_csv(index=False).encode('utf-8'), 'heartcare_demo_results.csv','text/csv')
    except (ValueError, pd.errors.ParserError, UnicodeDecodeError, FileNotFoundError) as exc:
        st.error(f'Unable to process this batch: {exc}')
st.caption('HeartCare AI · Uploaded records are processed in this session; this application has no database or patient-history storage.')
