"""Runtime metrics from untouched, chronologically held-out synthetic seasons."""
import numpy as np
from sklearn.metrics import brier_score_loss,roc_auc_score,average_precision_score
from sklearn.calibration import calibration_curve
from sklearn.isotonic import IsotonicRegression
from regions import DEMO

def metric(y,p,clim):
    bs=float(brier_score_loss(y,p)); ref=float(brier_score_loss(y,np.full(len(y),clim)))
    return {'brier':round(bs,4),'brier_skill':round(1-bs/ref,4),'roc_auc':round(float(roc_auc_score(y,p)),4) if len(np.unique(y))>1 else None,'pr_auc':round(float(average_precision_score(y,p)),4),'count':len(y),'bust_rate':round(float(np.mean(y)),4)}

def build_verification(engine):
    # Systematic sample of held-out records, every 7th row. No metric constants.
    d=engine.test.iloc[::7].copy();d['prediction']=0.;d['without_padi']=0.;d['upper']=0.;d['raw']=0.
    for h,m in engine.systems.items():
        mask=d.hazard_id==h;s=d[mask]
        d.loc[mask,'prediction']=m.predict(s)
        d.loc[mask,'without_padi']=engine.artifact['ablated'][h].predict(s)
        d.loc[mask,'upper']=m.intervals(s)[:,1]
        d.loc[mask,'raw']=m.tree.predict_proba(s[m.features])[:,1]
    engine.evaluation=d
    return summarise(engine,d)

def summarise(engine,d):
    clim=engine.artifact['train_rate']; y=d.bust.to_numpy();p=d.prediction.to_numpy()
    metrics=metric(y,p,clim)
    frac,mean=calibration_curve(y,p,n_bins=10,strategy='uniform')
    reliability=[{'predicted':round(float(a),3),'observed':round(float(b),3),'ideal':round(float(a),3)} for a,b in zip(mean,frac)]
    coverage=float((d.abs_error<=d.upper).mean());extreme=d[d.relative_severe]
    by_lead=[{'lead':int(k),**metric(g.bust,g.prediction,clim),'coverage':round(float((g.abs_error<=g.upper).mean()),4)} for k,g in d.groupby('lead')]
    by_phase=[{'phase':f'Phase {int(k)}',**metric(g.bust,g.prediction,clim)} for k,g in d.groupby('phase')]
    # Fixed rules fitted to archive-scale proxies, deliberately simple baselines.
    baseline={'Climatology':np.full(len(d),clim),'Raw spread':np.clip(d.spread*.15,0,1),'Persistence':np.clip(d.memory*.17,0,1),'EFI only':np.clip(d.efi*.15,0,1),'Full stack':p}
    baselines=[{'name':k,**metric(y,v,clim)} for k,v in baseline.items()]
    ablation=[{'name':'Without PADI',**metric(y,d.without_padi,clim)},{'name':'With PADI',**metrics}]
    months=[]
    for month,g in d.groupby(d.date.dt.to_period('M')):
        months.append({'month':str(month),'brier':round(float(brier_score_loss(g.bust,g.prediction)),4),'coverage':round(float((g.abs_error<=g.upper).mean()),3),'version':int(g.model_version.max())})
    # Controlled drift experiment: deliberate score underconfidence after an upgrade.
    full=engine.evaluation
    old=full[full.model_version==0];new=full[full.model_version==1].sort_values('date')
    cut=len(new)//2;cal=new.iloc[:cut];hold=new.iloc[cut:]
    shifted_cal=np.clip(cal.prediction*.55,0,1);shifted_hold=np.clip(hold.prediction*.55,0,1)
    recal=IsotonicRegression(out_of_bounds='clip').fit(shifted_cal,cal.bust)
    before=float(brier_score_loss(hold.bust,shifted_hold));after=float(brier_score_loss(hold.bust,recal.predict(shifted_hold)))
    drift={'upgrade_date':'2024-07-01','description':'Synthetic model-version change; additional controlled score-compression stress test. Recalibrator fitted to earlier post-upgrade records, evaluated on later records.','before_brier':round(before,4),'after_brier':round(after,4),'old_rate':round(float(old.bust.mean()),4),'new_rate':round(float(new.bust.mean()),4),'alarm':bool(abs(new.bust.mean()-old.bust.mean())>.015),'recalibration_samples':len(cal),'evaluation_samples':len(hold),'timeline':months}
    return {'data_mode':DEMO,'metrics':metrics,'reliability':reliability,'coverage':{'target':.9,'overall':round(coverage,4),'extremes':round(float((extreme.abs_error<=extreme.upper).mean()),4),'extreme_n':len(extreme),'note':'One-sided absolute-error intervals [0, upper], not intervals on bust probability. Empirical coverage only; distribution shift can invalidate exchangeability.'},'by_lead':by_lead,'by_phase':by_phase,'baselines':baselines,'ablation':ablation,'drift':drift,'protocol':{'training':'2019–2021','stacking':'Jan–Jun 2022','calibration':'Jul–Dec 2022','test':'2023–2024','embargo_days':10,'archive_rows':engine.artifact['rows'],'evaluation_rows':len(d),'sampling':'Every seventh held-out row, chronology preserved','synthetic_seed':26079,'limitations':['No operational NCMRWF validation','Conformal coverage is measured, not guaranteed under drift','Regional monsoon/terrain proxies are simplified','PADI ablation removes the direct feature; correlated witnesses remain','Recent-skill proxy is generated, not an assimilated real-time verification history']}}