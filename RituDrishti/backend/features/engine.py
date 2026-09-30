"""Physics-aware scalar feature engine, shared by training and live inference."""
import numpy as np

FEATURES = ['spread','flipflop','padi','efi','bimodality','jet','moisture','growth','hard_regime','memory','orography','land_sea','lead','region_id','model_version','underdispersion','wd_interaction','ridge','soil','shear']
MONOTONE = [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def transform(d):
    d = d.copy()
    for a,b in [('spread','member_std'),('flipflop','cycle_jump'),('padi','ai_distance'),('efi','tail_index'),('jet','jet_proxy'),('moisture','ivt_proxy'),('growth','growth_proxy'),('memory','recent_error'),('soil','soil_moisture')]: d[a]=d[b]
    d['bimodality'] = np.clip((d.member_std+d.ai_distance)/2-.2,0,1)
    d['hard_regime'] = d.phase.isin([3,4,7]).astype(float)
    d['underdispersion'] = ((d.member_std<.15)&(d.ai_distance>.45)).astype(float)
    d['wd_interaction'] = d.jet*d.moisture*d.orography
    return d