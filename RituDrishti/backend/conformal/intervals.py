"""One-sided conformal error intervals. Coverage is empirical, not an unconditional guarantee."""
import numpy as np

def finite_quantile(residuals, alpha=.1):
    n=len(residuals)
    q=min(1,np.ceil((n+1)*(1-alpha))/n)
    return float(np.quantile(residuals,q,method='higher'))

class AdaptiveConformal:
    def fit(self, y, head, leads):
        self.alpha=.1
        self.residuals={l:list((np.asarray(y)-np.asarray(head))[np.asarray(leads)==l]) for l in range(1,11)}
        return self

    def intervals(self, head, leads):
        return np.array([[0., max(.01,float(v)+finite_quantile(self.residuals[int(l)],self.alpha))] for v,l in zip(head,leads)])

    def update(self, observed, head, leads):
        intervals=self.intervals(head,leads)
        miss=float(np.mean(np.asarray(observed)>intervals[:,1]))
        self.alpha=float(np.clip(self.alpha+.02*(.1-miss),.02,.2))
        for y,h,l in zip(observed,head,leads):
            self.residuals[int(l)]=(self.residuals[int(l)]+[float(y-h)])[-3000:]
        return miss