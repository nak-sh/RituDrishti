from pathlib import Path
import joblib
from adapters.synthetic import SyntheticAdapter
from features.engine import transform
from labels.bust import fit_thresholds, label
from models.core import HazardModel

DATA=Path(__file__).resolve().parents[1]/'data'

def train_all():
    print('Generating physically structured synthetic archive...',flush=True)
    d=transform(SyntheticAdapter().load())
    train_mask=d.date<'2021-12-22'
    thresholds=fit_thresholds(d[train_mask])
    d=label(d,thresholds)
    systems={}; ablated={}
    for hazard in range(3):
        h=d[d.hazard_id==hazard]
        train=h[h.date<'2021-12-22']
        stack=h[h.date.between('2022-01-01','2022-06-20')]
        cal=h[h.date.between('2022-07-01','2022-12-21')]
        print(f'Training hazard {hazard}; rate={train.bust.mean():.3f}',flush=True)
        systems[hazard]=HazardModel().fit(train,stack,cal)
        ablated[hazard]=HazardModel(without_padi=True).fit(train,stack,cal)
    test=d[d.date>='2023-01-01'].copy()
    test.to_parquet(DATA/'test.parquet',index=False)
    artifact={'systems':systems,'ablated':ablated,'thresholds':thresholds,'rows':len(d),'train_rate':float(d[train_mask].bust.mean()),'seed':26079}
    joblib.dump(artifact,DATA/'models.joblib',compress=3)
    print('Training complete.',flush=True)
    return artifact

def load_models():
    if not (DATA/'models.joblib').exists(): return train_all()
    return joblib.load(DATA/'models.joblib')