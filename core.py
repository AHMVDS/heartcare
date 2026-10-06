from pathlib import Path
import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).parent
FEATURES = ['age', 'sex', 'blood_pressure', 'cholesterol', 'bmi', 'smoker']
LIMITS = {'age': (18, 120), 'blood_pressure': (60, 260), 'cholesterol': (70, 600), 'bmi': (10, 70)}

def validate(frame):
    frame = frame.copy()
    frame.columns = frame.columns.str.strip()
    if frame.columns.duplicated().any():
        raise ValueError('Duplicate column names are not allowed.')
    missing = set(FEATURES) - set(frame.columns)
    if missing:
        raise ValueError('Missing columns: ' + ', '.join(sorted(missing)))
    if not 1 <= len(frame) <= 10000:
        raise ValueError('Provide between 1 and 10,000 patients.')
    for col, (lo, hi) in LIMITS.items():
        values = pd.to_numeric(frame[col], errors='coerce')
        bad = ~np.isfinite(values) | ~values.between(lo, hi)
        if col == 'age':
            bad |= values.mod(1).ne(0)
        if bad.any():
            rows = ', '.join(str(i + 2) for i in np.flatnonzero(bad)[:8])
            raise ValueError(f'{col}: expected {lo}–{hi}; check CSV lines {rows}.')
        frame[col] = values
    for col, mapping in [('sex', {'m': 'M', 'f': 'F'}), ('smoker', {'yes': 'Yes', 'no': 'No'})]:
        normalized = frame[col].astype(str).str.strip().str.lower().map(mapping)
        if normalized.isna().any():
            raise ValueError(f'{col}: allowed values are {list(mapping.values())}.')
        frame[col] = normalized
    if 'patient_id' not in frame:
        frame.insert(0, 'patient_id', [str(i) for i in range(1, len(frame) + 1)])
    if frame.patient_id.isna().any() or frame.patient_id.astype(str).str.strip().eq('').any() or frame.patient_id.duplicated().any():
        raise ValueError('patient_id must be nonempty and unique.')
    return frame

def predict(frame, model_name):
    clean = validate(frame)
    bundle = joblib.load(ROOT / f'{model_name}.joblib')
    if bundle['features'] != FEATURES or bundle['mode'] != 'synthetic_demo':
        raise ValueError('Unexpected model metadata. Review the model integration first.')
    result = clean.copy()
    scores = bundle['pipeline'].predict_proba(clean[FEATURES])[:, 1] * 100
    result['demo_score_percent'] = scores.round(2)
    result['demo_band'] = pd.cut(scores, [-1, 30, 60, 101], labels=['Low', 'Medium', 'High'], right=False).astype(str)
    result['model'] = model_name
    result['mode'] = 'SYNTHETIC DEMO — not clinical risk'
    return result
