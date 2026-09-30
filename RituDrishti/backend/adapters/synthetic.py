"""Seeded, vectorised physical proxy generator. These are NOT measured forecasts."""
import numpy as np
import pandas as pd
from adapters.base import ForecastAdapter

class SyntheticAdapter(ForecastAdapter):
    def __init__(self, seed=26079):
        self.seed = seed

    def load(self, start='2019-01-01', end='2024-12-31'):
        rng = np.random.default_rng(self.seed)
        dates = pd.date_range(start, end, freq='D')
        idx = pd.MultiIndex.from_product([dates, range(12), range(1,11), range(3)], names=['date','region_id','lead','hazard_id'])
        d = idx.to_frame(index=False)
        n = len(d); month = d.date.dt.month.to_numpy(); lead = d.lead.to_numpy(); reg = d.region_id.to_numpy(); h = d.hazard_id.to_numpy()
        d['season'] = (month % 12 // 3).astype(int)
        d['phase'] = ((d.date.dt.dayofyear.to_numpy()//6 + reg//3) % 8 + 1)
        hard = np.isin(d.phase, [3,4,7]).astype(float)
        episode = np.zeros(n)
        for a,b,regions,hazard in [('2023-06-08','2023-06-16',[4,11],2),('2023-07-05','2023-07-12',[0,2],0),('2024-05-20','2024-06-18',[1,2],1)]:
            episode += (d.date.between(a,b) & d.region_id.isin(regions) & (h==hazard)).to_numpy()*0.6
        # Active monsoon demo cycle; broad, lead-dependent deterioration.
        if dates.min().year >= 2026:
            regional = np.array([.58,.12,.31,.05,.29,.72,.02,.35,.2,.41,.43,.12])[reg]
            episode += regional * np.clip((lead-1)/6,0,1) + .1*np.sin(d.date.dt.dayofyear.to_numpy())
        instability = rng.beta(1.5,4.5,n) + .018*lead + .12*hard + episode
        d['member_std'] = np.clip(instability + rng.normal(0,.1,n),.01,1.8)
        d['cycle_jump'] = np.clip(instability*.75 + rng.normal(0,.12,n),.01,1.8)
        d['ai_distance'] = np.clip(instability*.85 + rng.normal(0,.15,n),.01,1.8)
        d['tail_index'] = np.clip(rng.beta(2,4,n)+episode*.6,0,1.8)
        d['jet_proxy'] = rng.uniform(0,1,n)
        d['ivt_proxy'] = np.clip(rng.beta(2,3,n)+((month==7)&np.isin(reg,[0,5,7]))*.3,0,1.5)
        d['growth_proxy'] = np.clip(.035*lead + instability*.4 + rng.normal(0,.09,n),0,1.5)
        d['recent_error'] = np.clip(instability*.7+rng.normal(0,.15,n),0,1.5)
        d['orography'] = np.array([1,.1,.15,.3,.15,.6,.4,.7,.25,.85,0,0])[reg]
        d['land_sea'] = np.isin(reg,[4,5,7,8,10,11]).astype(float)
        d['soil_moisture'] = rng.uniform(0,1,n)
        d['ridge'] = rng.uniform(0,1,n)
        d['shear'] = rng.uniform(0,1,n)
        d['model_version'] = (d.date >= '2024-07-01').astype(int)
        # A small under-dispersive subset: low spread despite high witness disagreement.
        under = rng.random(n)<.035
        d.loc[under,'member_std'] *= .15
        latent = 1.65*d.member_std + 1.1*d.cycle_jump + 1.5*d.ai_distance + .35*hard + .4*d.growth_proxy + .18*d.ivt_proxy + .4*under + .22*d.model_version
        scale = np.choose(h,[5.5,.42,17.]) * (1+.06*lead)
        seasonal = 1 + .3*((h==1)&np.isin(month,[4,5,6])) + .25*((h==0)&(month==7)&np.isin(reg,[5,7]))
        d['abs_error'] = scale*seasonal*np.exp(latent-2.9+rng.normal(0,.38,n))
        d['observation'] = np.choose(h,[rng.gamma(1.5,12,n),rng.normal(34,4,n),rng.uniform(0,400,n)])
        d['forecast'] = np.maximum(0,d.observation+d.abs_error*rng.choice([-1,1],n))
        # Neighbourhood fractions are synthetic spatial summaries, not full grids.
        d['observed_fraction'] = np.clip(d.observation/np.choose(h,[100,50,400]),0,1)
        d['forecast_fraction'] = np.clip(d.observed_fraction + rng.normal(0,.1,n)+d.abs_error/np.choose(h,[300,25,800]),0,1)
        return d