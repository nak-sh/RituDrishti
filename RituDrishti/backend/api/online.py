"""Sequential synthetic verification loop, separate from frozen offline test metrics."""
from datetime import datetime,timezone
import numpy as np
from sklearn.metrics import brier_score_loss
from sklearn.isotonic import IsotonicRegression

async def run_verification(engine,db,run_id):
    try:
        prior=await db.verification_runs.count_documents({'status':'completed'})
        dates=sorted(engine.test.date.unique());index=min(len(dates)-1,30+prior)
        date=dates[index];frame=engine.test[engine.test.date==date];window=engine.test[(engine.test.date<date)&(engine.test.date>=dates[max(0,index-30)])]
        predicted=[];observed=[];misses=[]
        for h,m in engine.systems.items():
            d=frame[frame.hazard_id==h];w=window[window.hazard_id==h]
            p=m.predict(d);predicted.extend(p);observed.extend(d.bust)
            misses.append(m.conformal.update(d.abs_error,m.head.predict(d[m.features]),d.lead))
            raw=m.raw(w)
            for lead in range(1,11):
                mask=w.lead==lead
                if w[mask].bust.nunique()>1:
                    m.cal.models[lead]=IsotonicRegression(out_of_bounds='clip',y_min=.001,y_max=.999).fit(raw[mask],w[mask].bust)
        engine.frame.cache_clear()
        row={'status':'completed','verified_date':str(np.datetime_as_string(date,unit='D')),'count':len(observed),'brier':float(brier_score_loss(observed,predicted)),'coverage':1-float(np.mean(misses)),'bust_rate':float(np.mean(observed)),'drift_alarm':bool(abs(np.mean(observed)-engine.artifact['train_rate'])>.05),'completed_at':datetime.now(timezone.utc).isoformat(),'data_mode':'synthetic','note':'Recalibration uses only the previous 30 synthetic observed days. Updates are in-memory for this worker; persistent audit is stored.'}
        await db.verification_runs.update_one({'id':run_id},{'$set':row})
    except Exception as e:
        await db.verification_runs.update_one({'id':run_id},{'$set':{'status':'failed','error':type(e).__name__}})
        raise