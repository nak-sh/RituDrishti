import numpy as np
from regions import DEMO

SCENARIOS=[{'id':'biparjoy','title':'Cyclone Biparjoy','subtitle':'Arabian Sea → Gujarat coast','date':'15 June 2023','event_date':'2023-06-15','hazard':2,'region':4,'period':['2023-06-08','2023-06-15'],'summary':'Competing circulation scenarios and growing cross-model disagreement before a coastal landfall.','icon':'cyclone','drivers':['ENS_TRACK_SPLIT','PADI_HIGH','FLIPFLOP_HIGH']},{'id':'himachal','title':'The Himalayan rainfall episode','subtitle':'Himachal Pradesh & North India','date':'8–10 July 2023','event_date':'2023-07-09','hazard':0,'region':0,'period':['2023-07-05','2023-07-12'],'summary':'Orographic moisture transport interacting with a western disturbance during the monsoon.','icon':'rain','drivers':['OROGRAPHIC_IVT_HIGH','WD_MONSOON_INTERACTION','RAPID_ERROR_GROWTH']},{'id':'heatwave','title':'North India’s prolonged heat','subtitle':'Northwest & Indo-Gangetic Plain','date':'May–June 2024','event_date':'2024-06-01','hazard':1,'region':1,'period':['2024-05-25','2024-06-01'],'summary':'Uncertain ridge persistence and land-surface moisture sensitivity during pre-monsoon heat.','icon':'heat','drivers':['RIDGE_PERSISTENCE_UNCERTAIN','SOIL_MOISTURE_BIAS','FLIPFLOP_HIGH']}]

def build_cases(engine):
    out=[]
    for spec in SCENARIOS:
        d=engine.test;sub=d[(d.region_id==spec['region'])&(d.hazard_id==spec['hazard'])&d.date.between(*spec['period'])].copy()
        m=engine.systems[spec['hazard']];sub['p']=m.predict(sub);timeline=[]
        for date,g in sub.groupby('date'):
            g=g.sort_values('lead');target=max(1,min(10,(np.datetime64(spec['event_date'])-np.datetime64(str(date.date()))).astype('timedelta64[D]').astype(int)+1));r=g[g.lead==target].iloc[0];low=g[100*(1-g.p)<65]
            timeline.append({'date':str(date.date()),'day':f'{date.day} {date.strftime("%b")}','fci':round(100*(1-float(r.p))),'lead':target,'trust_horizon':int(low.lead.min()) if len(low) else None,'flipflop':round(float(r.flipflop),3),'growth':round(float(r.growth),3),'padi':round(float(r.padi),3),'realised_error':round(float(r.abs_error),2)})
        peak=sub.sort_values('p',ascending=False).iloc[:1]
        out.append({**spec,'timeline':timeline,'analogs':m.analogs(peak,1),'label':'Illustrative back-test with synthetic scenario data','data_mode':DEMO})
    return out