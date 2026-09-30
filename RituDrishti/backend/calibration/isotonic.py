import numpy as np
from sklearn.isotonic import IsotonicRegression

class LeadCalibrator:
    def fit(self, scores, y, leads):
        self.models={}
        for lead in range(1,11):
            mask=np.asarray(leads)==lead
            self.models[lead]=IsotonicRegression(out_of_bounds='clip',y_min=.001,y_max=.999).fit(np.asarray(scores)[mask],np.asarray(y)[mask])
        return self

    def predict(self, scores, leads):
        scores=np.asarray(scores);leads=np.asarray(leads);out=np.empty(len(scores))
        for l in np.unique(leads):
            mask=leads==l;out[mask]=self.models[int(l)].predict(scores[mask])
        return out