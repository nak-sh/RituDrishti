import json
from functools import lru_cache
import numpy as np
import pandas as pd
from adapters.synthetic import SyntheticAdapter
from features.engine import transform
from labels.bust import label
from models.pipeline import load_models,DATA
from regions import REGIONS,HAZARDS,INIT_TIMES,DEMO,region_dicts
from explain.taxonomy import BY_FEATURE
from explain.narrative import narrative

def band(f): return 'High' if f>=80 else 'Moderate' if f>=65 else 'Low' if f>=45 else 'Very low'

class Engine:
    def __init__(self):
        self.artifact=load_models(); self.systems=self.artifact['systems']; self.test=pd.read_parquet(DATA/'test.parquet')

    @lru_cache(maxsize=12)
    def frame(self,init):
        seed=26079+sum(ord(c) for c in init)
        d=label(transform(SyntheticAdapter(seed).load(init[:10],init[:10])),self.artifact['thresholds'])
        d['p_bust']=0.;d['lower']=0.;d['upper']=0.
        for h,model in self.systems.items():
            mask=d.hazard_id==h; sub=d[mask]
            d.loc[mask,'p_bust']=model.predict(sub)
            bounds=model.intervals(sub); d.loc[mask,'lower']=bounds[:,0];d.loc[mask,'upper']=bounds[:,1]
        d['fci']=100*(1-d.p_bust)
        return d

    def selected(self,init,hazard='auto'):
        d=self.frame(init)
        if hazard!='auto':return d[d.hazard_id==HAZARDS.index(hazard)]
        return d.loc[d.groupby(['region_id','lead']).p_bust.idxmax()]

    def confidence(self,init=INIT_TIMES[0],hazard='auto',region=None):
        d=self.selected(init,hazard); out=[]
        for i,r in enumerate(REGIONS):
            if region and region!=r[0]:continue
            rows=d[d.region_id==i].sort_values('lead'); below=rows[rows.fci<65]
            leads=[]
            for _,v in rows.iterrows():
                fci=round(float(v.fci))
                leads.append({'day':int(v.lead),'fci':fci,'p_bust':round(float(v.p_bust),4),'hazard':HAZARDS[int(v.hazard_id)],'band':band(float(v.fci)),'conformal_interval':[round(float(v.lower),2),round(float(v.upper),2)],'error_unit':['mm','°C','km'][int(v.hazard_id)],'error_p90_class':'Severe' if v.upper>v.q95 else 'Moderate' if v.upper>v.q90 else 'Typical'})
            out.append({**region_dicts()[i],'trust_horizon_day':int(below.lead.min()) if len(below) else None,'leads':leads})
        return {'init':init,'hazard':hazard,'regions':out,'data_mode':DEMO,'regime':'Active monsoon · BSISO phase 3','init_times':INIT_TIMES,'model':'Monotone LightGBM + analogues · isotonic calibrated'}

    def hotspots(self,init=INIT_TIMES[0],min_prob=.35,hazard='auto'):
        out=[]
        for r in self.confidence(init,hazard)['regions']:
            leads=[l for l in r['leads'] if l['p_bust']>=min_prob]
            if leads:
                peak=max(leads,key=lambda l:l['p_bust'])
                out.append({'region':r['id'],'name':r['name'],'onset':leads[0]['day'],'duration':len(leads),'peak_day':peak['day'],'peak_probability':peak['p_bust'],'hazard':peak['hazard'],'fci':peak['fci']})
        return sorted(out,key=lambda r:-r['peak_probability'])

    def row(self,region,lead,init,hazard='auto'):
        d=self.selected(init,hazard)
        return d[(d.region_id==[r[0] for r in REGIONS].index(region))&(d.lead==lead)]

    def explain(self,region,lead,lang='en',init=INIT_TIMES[0],hazard='auto'):
        d=self.row(region,lead,init,hazard);v=d.iloc[0];h=int(v.hazard_id);model=self.systems[h]
        contrib=model.contributions(d)[0];positive=np.maximum(contrib,0); denom=float(positive.sum()) or 1
        order=np.argsort(-positive)[:3];drivers=[]
        for i in order:
            name=model.features[i]; spec=BY_FEATURE[name]
            drivers.append({'id':spec[0],'feature':name,'name':spec[4] if lang=='hi' else spec[3],'share':round(float(positive[i]/denom)*100,1),'shap_log_odds':round(float(contrib[i]),3),'value':round(float(v[name]),2),'threshold':spec[2],'triggered':bool(v[name]>=spec[2]),'explanation':spec[6] if lang=='hi' else spec[5]})
        feature=drivers[0]['feature'];normal=d.copy();normal[feature]=model.normal[feature];cf=float(model.predict(normal)[0])
        fci=round(float(v.fci)); risk=round(float(v.p_bust)*100,1)
        grounded=narrative({'region':REGIONS[int(v.region_id)][2 if lang=='hi' else 1],'day':lead,'fci':fci,'risk':risk,'driver':drivers[0]['name']},lang)
        allrows=self.selected(init,HAZARDS[h]);allrows=allrows[allrows.region_id==v.region_id].sort_values('lead')
        evidence=[{'day':int(r.lead),'physics':round(float(r.forecast),2),'ai':round(float(max(0,r.forecast-r.padi*[15,2,60][h])),2),'spread':round(float(r.spread*[12,2,45][h]),2),'flipflop':round(float(r.flipflop),2),'padi':round(float(r.padi),2)} for _,r in allrows.iterrows()]
        return {'init':init,'region':region,'name':REGIONS[int(v.region_id)][1],'day':lead,'fci':fci,'band':band(v.fci),'p_bust':float(v.p_bust),'hazard':HAZARDS[h],'conformal_interval':[0,round(float(v.upper),2)],'error_unit':['mm','°C','km'][h],'coverage_target':.9,'error_p90_class':'Severe' if v.upper>v.q95 else 'Moderate' if v.upper>v.q90 else 'Typical','drivers':drivers,'counterfactual':{'driver':drivers[0]['name'],'feature':feature,'normal_value':round(float(model.normal[feature]),3),'p_bust_if_normal':round(cf,4),'original':round(float(v.p_bust),4),'note':'Single-feature re-scoring of the full stack; not a causal intervention.'},'narrative':grounded,'evidence':evidence,'analogs':model.analogs(d),'data_mode':DEMO}

    def geojson(self,init,hazard,lead):
        geo=json.loads((DATA/'india-government.geojson').read_text())
        values={r['id']:r for r in self.confidence(init,hazard)['regions']}
        for f in geo['features']:
            name=f['properties']['STNAME'];r=next(r for r in REGIONS if name in r[3]);v=values[r[0]]
            f['properties']={'state':name,'region':r[0],**v['leads'][lead-1],'trust_horizon_day':v['trust_horizon_day'],'data_mode':DEMO}
        for rid,coords in [('bay',[[86,17],[90,17],[90,21],[86,21],[86,17]]),('arabian',[[68.5,12],[71.5,12],[72.5,18],[69,18],[68.5,12]])]:
            v=values[rid];geo['features'].append({'type':'Feature','geometry':{'type':'Polygon','coordinates':[coords]},'properties':{'region':rid,**v['leads'][lead-1],'trust_horizon_day':v['trust_horizon_day'],'illustrative_sea_region':True,'data_mode':DEMO}})
        return geo