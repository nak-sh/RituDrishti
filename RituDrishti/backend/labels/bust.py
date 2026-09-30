"""Fit thresholds on TRAIN ONLY; apply unchanged to future seasons."""
import numpy as np
GROUP = ['region_id','season','lead','hazard_id']

def fit_thresholds(train):
    return train.groupby(GROUP).abs_error.quantile([.9,.95]).unstack().rename(columns={.9:'q90',.95:'q95'})

def label(d, thresholds):
    d = d.join(thresholds,on=GROUP)
    d['relative_moderate'] = d.abs_error > d.q90
    d['relative_severe'] = d.abs_error > d.q95
    rain = (d.hazard_id==0)&((d.forecast>=64.5)!=(d.observation>=64.5))&(d.abs_error>=30)
    heat = (d.hazard_id==1)&((d.forecast>=40)!=(d.observation>=40))&(d.abs_error>=4.5)
    cyclone = (d.hazard_id==2)&(d.abs_error>=150)
    d['impact_bust'] = rain|heat|cyclone
    d['neighbourhood_error'] = (d.forecast_fraction-d.observed_fraction)**2/(d.forecast_fraction**2+d.observed_fraction**2+1e-6)
    # Severe errors or impact errors remain positive; neighbourhood score contextualises displacement.
    d['bust'] = (d.relative_severe | d.impact_bust).astype(int)
    d['error_class'] = np.where(d.relative_severe,'Severe',np.where(d.relative_moderate,'Moderate','Typical'))
    return d