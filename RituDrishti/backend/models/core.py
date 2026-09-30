"""Monotone LightGBM + nearest-neighbour tier + held-out logistic stacking.

Chronology: train 2019–2021; stack Jan–Jun 2022; calibrate Jul–Dec 2022;
test 2023–2024. Ten-day embargo before each later block.
"""
import numpy as np
from lightgbm import LGBMClassifier, LGBMRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import LogisticRegression
from calibration.isotonic import LeadCalibrator
from conformal.intervals import AdaptiveConformal
from features.engine import FEATURES, MONOTONE

class HazardModel:
    def __init__(self, without_padi=False):
        self.features=[f for f in FEATURES if not(without_padi and f=='padi')]
        self.constraints=[m for f,m in zip(FEATURES,MONOTONE) if f in self.features]

    def fit(self, train, stack, cal):
        self.normal=train[self.features].median()
        self.tree=LGBMClassifier(n_estimators=110,num_leaves=15,max_depth=5,learning_rate=.055,min_child_samples=90,monotone_constraints=self.constraints,verbosity=-1,n_jobs=2,random_state=26079)
        self.tree.fit(train[self.features],train.bust)
        self.archive=train.iloc[::max(1,len(train)//5500)].copy().reset_index(drop=True)
        self.scaler=StandardScaler().fit(self.archive[self.features])
        self.nn=NearestNeighbors(n_neighbors=5,n_jobs=2).fit(self.scaler.transform(self.archive[self.features]))
        self.meta=LogisticRegression(C=1,max_iter=200).fit(self.tiers(stack),stack.bust)
        self.cal=LeadCalibrator().fit(self.raw(stack=cal),cal.bust,cal.lead)
        self.head=LGBMRegressor(objective='quantile',alpha=.9,n_estimators=80,num_leaves=15,verbosity=-1,n_jobs=2,random_state=26079).fit(train[self.features],train.abs_error)
        self.conformal=AdaptiveConformal().fit(cal.abs_error,self.head.predict(cal[self.features]),cal.lead)
        return self

    def neighbors(self,d):
        return self.nn.kneighbors(self.scaler.transform(d[self.features]))

    def tiers(self,d):
        _,inds=self.neighbors(d)
        analog=self.archive.bust.to_numpy()[inds].mean(axis=1)
        return np.column_stack([self.tree.predict_proba(d[self.features])[:,1],analog])

    def raw(self,stack):
        return self.meta.predict_proba(self.tiers(stack))[:,1]

    def predict(self,d):
        return self.cal.predict(self.raw(d),d.lead)

    def intervals(self,d):
        return self.conformal.intervals(self.head.predict(d[self.features]),d.lead)

    def contributions(self,d):
        # LightGBM's exact TreeSHAP implementation: last column is expected value.
        return self.tree.booster_.predict(d[self.features],pred_contrib=True)[:,:-1]

    def analogs(self,d,k=5):
        distances,indices=self.nn.kneighbors(self.scaler.transform(d[self.features]),n_neighbors=k)
        rows=[]
        for distance,i in zip(distances[0],indices[0]):
            r=self.archive.iloc[i]
            rows.append({'date':str(r.date.date()),'region_id':int(r.region_id),'lead':int(r.lead),'similarity':round(float(100/(1+distance)),1),'error':round(float(r.abs_error),2),'outcome':'Over-forecast' if r.forecast>r.observation else 'Under-forecast','bust':bool(r.bust),'regime':f'BSISO phase {int(r.phase)}','forecast':round(float(r.forecast),2),'observed':round(float(r.observation),2),'synthetic':True})
        return rows