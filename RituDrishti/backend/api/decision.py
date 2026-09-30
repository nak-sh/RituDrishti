import numpy as np
from regions import DEMO,INIT_TIMES

def decision(engine,cost_loss,init=INIT_TIMES[0]):
    d=engine.evaluation;y=d.bust.to_numpy();p=d.prediction.to_numpy()
    climatology=float(y.mean());reference=min(cost_loss,climatology);perfect=cost_loss*climatology
    expense=float(np.mean(np.where(p>=cost_loss,cost_loss,y)))
    value=(reference-expense)/(reference-perfect) if reference>perfect else 0
    alerts=[]
    for r in engine.confidence(init)['regions']:
        ls=[l for l in r['leads'] if l['p_bust']>=cost_loss]
        if ls:
            peak=max(ls,key=lambda l:l['p_bust'])
            alerts.append({'region':r['id'],'name':r['name'],'onset':ls[0]['day'],'duration':len(ls),'peak_probability':peak['p_bust'],'lead':peak['day'],'hazard':peak['hazard']})
    return {'cost_loss':cost_loss,'alert_threshold':cost_loss,'relative_economic_value':round(value,4),'forecast_expense':round(expense,4),'reference_expense':round(reference,4),'perfect_expense':round(perfect,4),'test_prevalence':round(climatology,4),'alerts':sorted(alerts,key=lambda a:-a['peak_probability']),'data_mode':DEMO,'assumption':'Protect against the decision loss from a forecast bust when P(bust) ≥ C/L. Unit loss, constant protective cost, binary event. This is not a calibrated hazard-event probability or reservoir operating policy.'}