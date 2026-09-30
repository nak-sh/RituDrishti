from adapters.base import ForecastAdapter

class NCUMAdapter(ForecastAdapter):
    def load(self, start, end):
        raise NotImplementedError('NCUM/NEPS access is not configured. Supply licensed grids, region aggregation, units, valid times and observed truth. No live NCMRWF data is available in this demo.')