"""Create reproducible synthetic demonstration models. No clinical training data."""
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from core import ROOT, FEATURES

rng = np.random.default_rng(42)
n = 4000
frame = pd.DataFrame({'age': rng.integers(18, 90, n), 'sex': rng.choice(['M','F'], n), 'blood_pressure': rng.uniform(90,190,n), 'cholesterol': rng.uniform(120,330,n), 'bmi': rng.uniform(17,42,n), 'smoker': rng.choice(['Yes','No'], n)})
# Arbitrary demonstration relationship, NOT a medical equation.
z = -1.3 + (frame.age-50)/22 + (frame.blood_pressure-130)/35 + (frame.cholesterol-220)/80 + (frame.bmi-27)/10 + frame.smoker.eq('Yes')*.7
labels = rng.binomial(1, 1/(1+np.exp(-z)))
(ROOT/'models').mkdir(exist_ok=True)
for name, estimator in [('lr', LogisticRegression(max_iter=1000, random_state=42)), ('xgboost', XGBClassifier(n_estimators=90, max_depth=3, learning_rate=.06, random_state=42, n_jobs=2))]:
    prep = ColumnTransformer([('numeric', StandardScaler(), ['age','blood_pressure','cholesterol','bmi']), ('categorical', OneHotEncoder(handle_unknown='error', sparse_output=False), ['sex','smoker'])])
    pipe = Pipeline([('preprocessing',prep),('classifier',estimator)])
    pipe.fit(frame[FEATURES], labels)
    joblib.dump({'pipeline':pipe, 'features':FEATURES, 'mode':'synthetic_demo'}, ROOT/'models'/f'{name}.joblib')
metadata = {'mode':'synthetic_demo', 'seed':42, 'rows':n, 'clinical_validation':False, 'target':'Arbitrary synthetic binary label; no disease endpoint or time horizon', 'bands':'Low <30%, Medium 30–<60%, High >=60%; arbitrary UI demonstration thresholds', 'units_assumed':{'blood_pressure':'systolic mmHg','cholesterol':'total mg/dL','bmi':'kg/m²'}}
(ROOT/'models'/'metadata.json').write_text(json.dumps(metadata, indent=2))
print('Generated both synthetic demo models.')
